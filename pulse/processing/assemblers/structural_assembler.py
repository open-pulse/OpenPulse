import numpy as np
from scipy.sparse import spmatrix
from scipy.sparse.linalg import eigs

from pulse.model.model import Model
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.processing.assemblers.base import Assembler


class StructuralAssembler(Assembler):
    """
    Assembler for structural physics.

    Encapsulates all structural matrix assembly logic and boundary
    conditions, exposing the generic Assembler interface so that
    StaticSolver, ModalSolver and HarmonicSolver can consume it
    without knowing physics details.

    Parameters
    ----------
    model : Model
    acoustic_solution : np.ndarray | None
        Acoustic solution for coupled analysis. When provided, acoustic
        pressure loads are included in the force vector.
    """

    def __init__(self, model: Model, acoustic_solution: np.ndarray | None = None):

        self.model = model
        self.frequencies = model.frequencies
        self.acoustic_solution = acoustic_solution

        self._assembly = AssemblyStructural(
            model, acoustic_solution=acoustic_solution
        )

        # Global matrices (frequency-independent)
        (
            self._K,
            self._M,
            self._Kr,
            self._Mr,
        ) = self._assembly.get_global_matrices()

        (
            self._K_lump,
            self._M_lump,
            self._C_lump,
            self._Kr_lump,
            self._Mr_lump,
            self._Cr_lump,
            self.flag_Clump,
        ) = self._assembly.get_lumped_matrices()

        (
            self._K_exp_joint,
            self._M_exp_joint,
            self._Kr_exp_joint,
            self._Mr_exp_joint,
        ) = self._assembly.get_expansion_joint_global_matrices()

        self._prescribed_indexes = self._assembly.get_prescribed_indexes()
        self._prescribed_values, self._array_prescribed_values = (
            self._assembly.get_prescribed_values()
        )
        self._unprescribed_indexes = self._assembly.get_unprescribed_indexes()

        # Pre-compute combined loads for all frequencies
        self._F_harmonic: np.ndarray | None = None  # (n_unprescribed, n_freqs)
        self._F_static: np.ndarray | None = None    # (n_unprescribed, 1)

    # ── Internal matrix access properties ────────────────────────────────

    @property
    def global_damping(self) -> tuple[float, float, float]:
        return self.model.global_damping

    @property
    def prescribed_indexes(self):
        return self._prescribed_indexes

    @property
    def unprescribed_indexes(self):
        return self._unprescribed_indexes

    @property
    def Kr(self):
        return self._Kr

    @property
    def Mr(self):
        return self._Mr

    @property
    def Kr_exp_joint(self):
        return self._Kr_exp_joint

    @property
    def Mr_exp_joint(self):
        return self._Mr_exp_joint

    @property
    def Kr_lump(self):
        return self._Kr_lump

    @property
    def Mr_lump(self):
        return self._Mr_lump

    @property
    def Cr_lump(self):
        return self._Cr_lump

    # ── Assembler interface ───────────────────────────────────────────────

    def get_stiffness_matrix(self) -> spmatrix:
        """K + K_exp_joint[0] + K_lump[0]  (for modal and static analysis)."""
        return self._K + self._K_exp_joint[0] + self._K_lump[0]

    def get_mass_matrix(self) -> spmatrix:
        """M + M_exp_joint + M_lump[0]  (for modal analysis)."""
        return self._M + self._M_exp_joint + self._M_lump[0]

    def get_system_matrix(self, index: int, omega: float) -> spmatrix:
        """
        Structural dynamic system matrix at step `index`:
            A = (K + K_exp[i] + K_lump[i])
              - ω²·(M + M_exp + M_lump[i])
              + i·C_prop(ω)
              + i·ω·C_lump[i]
        """
        alpha, beta, eta = self.model.global_damping

        K_tot = self._K + self._K_exp_joint[index] + self._K_lump[index]
        M_tot = self._M + self._M_exp_joint + self._M_lump[index]

        F_K = K_tot
        F_M = (-(omega ** 2)) * M_tot
        F_C = 1j * (
            (eta + omega * beta) * (self._K + self._K_exp_joint[index])
            + (omega * alpha) * (self._M + self._M_exp_joint)
        )
        F_Clump = 1j * omega * self._C_lump[index]

        return F_K + F_M + F_C + F_Clump

    def get_load_vector(self, index: int, omega: float) -> np.ndarray:
        """
        Combined load vector for step `index`.
        For static analysis call with index=0, omega=0.
        """
        if omega == 0.0:
            # Static analysis — pre-compute once
            if self._F_static is None:
                self._F_static = self._compute_combined_loads(static_analysis=True)
            return self._F_static[:, 0]
        else:
            # Harmonic analysis — pre-compute once for all frequencies
            if self._F_harmonic is None:
                self._F_harmonic = self._compute_combined_loads(static_analysis=False)
            return self._F_harmonic[:, index]

    def reinsert_prescribed_dofs(
        self, solution: np.ndarray, modal: bool = False
    ) -> np.ndarray:
        """Reinsert prescribed DOFs into the reduced solution."""
        rows = solution.shape[0] + len(self._prescribed_indexes)
        cols = solution.shape[1]
        full_solution = np.zeros((rows, cols), dtype=complex)
        full_solution[self._unprescribed_indexes, :] = solution

        if len(self._prescribed_indexes) > 0:
            if modal:
                full_solution[self._prescribed_indexes, :] = np.zeros(
                    (len(self._prescribed_values), cols)
                )
            else:
                full_solution[self._prescribed_indexes, :] = (
                    self._array_prescribed_values[:, :cols]
                )
        return full_solution

    def stop_processing(self) -> bool:
        return bool(self.model.preprocessor.stop_processing)

    # ── Stress stiffening ─────────────────────────────────────────────────

    def apply_stress_stiffening(self, static_solution: np.ndarray) -> None:
        """
        Updates global matrices to account for stress stiffening.

        Should be called by project.py before ModalSolver or HarmonicSolver
        when preprocessor.stress_stiffening_enabled == True.
        """
        self.model.preprocessor.update_nodal_solution_info(
            np.real(static_solution)
        )
        (
            self._K,
            self._M,
            self._Kr,
            self._Mr,
        ) = self._assembly.get_global_matrices()

        # Invalidate load cache
        self._F_harmonic = None
        self._F_static = None

    def get_loads_matrix(self, loads_matrix3D: bool = True) -> np.ndarray:
        """Load matrix for mode superposition (without prescribed correction)."""
        return self._assembly.get_global_loads(loads_matrix3D=loads_matrix3D)

    def has_no_table(self) -> bool:
        return self._assembly.no_table

    def get_loads_for_stress_stiffening(self) -> np.ndarray:
        return self._assembly.get_global_loads_for_stress_stiffening()

    # ── Private: combined load vector assembly ────────────────────────────

    def _compute_combined_loads(self, static_analysis: bool = False) -> np.ndarray:
        """
        Computes F_combined = F - F_eq for all frequencies.
        Combines external loads with prescribed DOF equivalent forces.
        Returns array of shape (n_unprescribed, n_freqs).
        """
        alpha, beta, eta = self.model.global_damping
        unprescribed = self._unprescribed_indexes

        F = self._assembly.get_global_loads(static_analysis=static_analysis)

        if static_analysis:
            _frequencies = np.array([0.0], dtype=float)
        else:
            _frequencies = self.frequencies

        cols = len(_frequencies)
        rows = len(unprescribed)
        F_eq = np.zeros((rows, cols), dtype=complex)

        if np.sum(self._array_prescribed_values):

            Kr_add_lump = complex(0)
            Mr_add_lump = complex(0)
            Cr_add_lump = complex(0)

            lumped_masses = False
            lumped_stiffness = False
            lumped_dampings = False

            for (_property, *_args) in self.model.properties.nodal_properties.items():
                if _property == "lumped_masses":
                    lumped_masses = True
                elif _property == "lumped_stiffness":
                    lumped_stiffness = True
                elif _property == "lumped_dampings":
                    lumped_dampings = True

            Kr = (self._Kr.toarray())[unprescribed, :]
            _Mr = (self._Mr.toarray())[unprescribed, :] + (
                self._Mr_exp_joint.toarray()
            )[unprescribed, :]

            for i, freq in enumerate(_frequencies):
                _Kr = Kr + (self._Kr_exp_joint[i].toarray())[unprescribed, :]
                pv_i = self._array_prescribed_values[:, i]

                Kr_add = np.sum(_Kr * pv_i, axis=1)
                Mr_add = np.sum(_Mr * pv_i, axis=1)

                if lumped_stiffness:
                    Kr_lump_i = (self._Kr_lump[i].toarray())[unprescribed, :]
                    Kr_add_lump = np.sum(Kr_lump_i * pv_i, axis=1)

                if lumped_masses:
                    Mr_lump_i = (self._Mr_lump[i].toarray())[unprescribed, :]
                    Mr_add_lump = np.sum(Mr_lump_i * pv_i, axis=1)

                if lumped_dampings:
                    Cr_lump_i = (self._Cr_lump[i].toarray())[unprescribed, :]
                    Cr_add_lump = np.sum(Cr_lump_i * pv_i, axis=1)

                omega = 2 * np.pi * freq
                F_Kadd = Kr_add + Kr_add_lump
                F_Madd = (-(omega ** 2)) * (Mr_add + Mr_add_lump)
                F_Cadd = 1j * (
                    (eta + omega * beta) * Kr_add + (omega * alpha) * Mr_add
                )
                F_Cadd_lump = 1j * omega * Cr_add_lump
                F_eq[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        F_combined = F[unprescribed, :] - F_eq
        return F_combined
