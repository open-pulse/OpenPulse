import numpy as np
from scipy.sparse import spmatrix

from pulse.model.model import Model
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.assemblers.base import Assembler


class AcousticAssembler(Assembler):
    """
    Assembler for acoustic physics.

    Encapsulates all acoustic matrix assembly logic (FETM for harmonic
    analysis, FEM for modal analysis) and boundary conditions, exposing
    the generic Assembler interface for StaticSolver, ModalSolver and
    HarmonicSolver.

    Also manages the nonlinear iteration logic for perforated plate
    elements, exposing the auxiliary methods used by
    HarmonicSolver.nonlinear_direct_method.

    Parameters
    ----------
    model : Model
    """

    def __init__(self, model: Model):

        self.model = model

        frequencies = model.frequencies
        if isinstance(frequencies, np.ndarray | list):
            if frequencies[0] == 0:
                frequencies[0] = float(1e-4)
        self.frequencies = frequencies

        self._assembly = AssemblyAcoustic(model)
        self._acoustic_elements = model.preprocessor.acoustic_elements

        self._all_dofs = len(model.preprocessor.nodes)
        self._prescribed_indexes = self._assembly.get_prescribed_indexes()
        self._prescribed_values = self._assembly.get_prescribed_values()
        self._unprescribed_indexes = self._assembly.get_pipe_and_unprescribed_indexes()

        # FETM matrices (harmonic) — pre-computed
        self._K: list | None = None
        self._Kr: list | None = None
        self._K_lump: list | None = None
        self._Kr_lump: list | None = None
        self._K_link: list | None = None
        self._Kr_link: list | None = None
        self._T_link: list | None = None
        self._Tr_link: list | None = None
        self._Kadd_lump: list | None = None  # K + K_link + K_lump + T_link

        # Combined load vector (harmonic) — pre-computed
        self._volume_velocity: np.ndarray | None = None  # (n_unprescribed, n_freqs)
        self._array_prescribed_values: np.ndarray | None = None

        # FEM matrices (modal) — pre-computed on demand
        self._K_modal: spmatrix | None = None
        self._M_modal: spmatrix | None = None
        self._C_modal: spmatrix | None = None

        # Perforated plate nonlinearity
        self._nl_elements: list = self._detect_nl_pp_elements()
        self.convergence_target: float = 0.10  # 10 %
        self.convergence_data_log: list | None = None
        self._max_iter: int = 100

    # ── Nonlinearity ──────────────────────────────────────────────────────

    @property
    def nl_elements(self) -> list:
        """List of perforated plate elements with nonlinear effects."""
        return self._nl_elements

    def _detect_nl_pp_elements(self) -> list:
        elements = []
        for (prop, element_id) in self.model.properties.element_properties.keys():
            if prop == "perforated_plate":
                el = self._acoustic_elements[element_id]
                if el.perforated_plate.nonlinear_effects:
                    elements.append(el)
        return elements

    def update_after_iteration(self) -> None:
        """
        Rebuilds FETM matrices after nonlinear element state has been updated.

        Called by HarmonicSolver.nonlinear_direct_method at each iteration,
        after element.update_delta_pressure() has already been called for each
        nonlinear element.
        """
        self._build_fetm_matrices()
        self._volume_velocity = None  # Force load recomputation

    def check_convergence(
        self,
        iterations: list,
        pressure_residues: list,
        delta_residues: list,
        unstable_frequencies: dict,
        delta_residue_criteria: bool = True,
    ) -> bool:
        """
        Checks convergence criteria for the nonlinear iteration.
        """
        ordinal = {1: "st", 2: "nd", 3: "rd"}
        count = iterations[-1]

        if count == 1:
            label = "\n      ---------------------------------------------------------------\n"
            label += "      ||>>>>>    PERFORATED PLATE: CONVERGENCE INFORMATION    <<<<<||"
            label += "\n      ---------------------------------------------------------------\n"
            print(label)

        sfx = ordinal.get(count, "th")
        print(
            f"Evaluated pressure residue criteria: "
            f"{round(pressure_residues[-1], 2)}[%] @ {count}{sfx} iteration"
        )
        print(
            f"Evaluated delta pressure residue criteria: "
            f"{round(delta_residues[-1], 2)}[%] @ {count}{sfx} iteration\n"
        )

        target_pct = 100 * self.convergence_target

        if count >= self._max_iter:
            if pressure_residues[-1] < target_pct:
                log = f"The solution converged after {count} iterations."
                if unstable_frequencies:
                    log += f"\nUnstable freqs: {list(unstable_frequencies.values())}"
                log += "\nPressure residues: converged"
                log += "\nDelta pressure residues: not converged\n"
                print(log)
            else:
                log = f"The solution did not converge after {count} iterations."
                log += f"\nLast pressure residue: {round(pressure_residues[-1], 2)}[%]"
                log += f"\nLast delta pressure residue: {round(delta_residues[-1], 2)}[%]"
                log += f"\nTarget: {round(target_pct, 2)}[%]\n"
                if unstable_frequencies:
                    log += f"\nUnstable freqs: {list(unstable_frequencies.values())}"
                print(log)

            self.convergence_data_log = [
                iterations, pressure_residues, delta_residues, target_pct
            ]
            return True

        if delta_residue_criteria:
            if pressure_residues[-1] < target_pct:
                if len(delta_residues) >= 4:
                    if max(delta_residues[-5:]) <= target_pct:
                        if max(pressure_residues[-3:]) <= 10:
                            if (
                                pressure_residues[-3]
                                >= pressure_residues[-2]
                                >= pressure_residues[-1]
                            ):
                                log = f"The solution converged after {count} iterations."
                                if unstable_frequencies:
                                    log += f"\nUnstable freqs: {list(unstable_frequencies.values())}"
                                log += "\nPressure residues: converged"
                                log += "\nDelta pressure residues: converged\n"
                                print(log)
                                self.convergence_data_log = [
                                    iterations, pressure_residues,
                                    delta_residues, target_pct,
                                ]
                                return True
        else:
            if max(pressure_residues[-5:]) <= target_pct:
                log = f"The solution converged after {count} iterations."
                if unstable_frequencies:
                    log += f"\nUnstable freqs: {list(unstable_frequencies.values())}"
                log += "\nPressure residues: converged"
                log += "\nDelta pressure residues: not converged\n"
                print(log)
                self.convergence_data_log = [
                    iterations, pressure_residues, delta_residues, target_pct
                ]
                return True

        return False

    # ── Assembler Interface ───────────────────────────────────────────────

    def get_stiffness_matrix(self) -> spmatrix:
        """K_add = K_fem + K_link_fem  (for FEM modal analysis)."""
        self._ensure_modal_matrices()
        return self._K_modal

    def get_mass_matrix(self) -> spmatrix:
        """M_add = M_fem + M_link_fem  (for FEM modal analysis)."""
        self._ensure_modal_matrices()
        return self._M_modal

    def get_damping_matrix(self) -> spmatrix | None:
        """
        C_lump for acoustic damping (external impedances).
        Returns None if C ≈ 0 (no nonproportional damping).
        """
        self._ensure_modal_matrices()
        if self._C_modal is not None and np.sum(self._C_modal[0]):
            return self._C_modal[0]
        return None

    def get_system_matrix(self, index: int, omega: float) -> spmatrix:
        """
        FETM admittance matrix for step `index`:
            Kadd_lump[index] = K[index] + K_link[index] + K_lump[index] + T_link[index]
        """
        self._ensure_fetm_matrices()
        return self._Kadd_lump[index]

    def get_load_vector(self, index: int, omega: float) -> np.ndarray:
        """Combined volume velocity for step `index`."""
        self._ensure_volume_velocity()
        return self._volume_velocity[:, index]

    def reinsert_prescribed_dofs(
        self, solution: np.ndarray, modal: bool = False
    ) -> np.ndarray:
        rows = self._all_dofs
        cols = solution.shape[1]
        full = np.zeros((rows, cols), dtype=complex)
        full[self._unprescribed_indexes, :] = solution

        if modal:
            full[self._prescribed_indexes, :] = np.zeros(
                (len(self._prescribed_values), cols)
            )
        else:
            if len(self._prescribed_indexes) != 0:
                full[self._prescribed_indexes, :] = self._array_prescribed_values

        return full

    def stop_processing(self) -> bool:
        return bool(self.model.preprocessor.stop_processing)

    # ── Nonlinear PP initialization ───────────────────────────────────────

    def reset_nl_elements(self) -> None:
        """Resets the nonlinear PP elements before starting the iteration."""
        for (prop, element_id) in self.model.properties.element_properties.keys():
            if prop == "perforated_plate":
                el = self._acoustic_elements[element_id]
                el.reset()

    # ── FETM matrix construction ──────────────────────────────────────────

    def _ensure_fetm_matrices(self) -> None:
        if self._Kadd_lump is None:
            self._build_fetm_matrices()

    def _build_fetm_matrices(self) -> None:
        K, Kr = self._assembly.get_global_matrices()
        K_lump, Kr_lump = self._assembly.get_lumped_matrices()
        K_link, Kr_link = self._assembly.get_fetm_link_matrices()
        T_link, Tr_link = self._assembly.get_fetm_transfer_matrices()

        self._K = K
        self._Kr = Kr
        self._K_lump = K_lump
        self._Kr_lump = Kr_lump
        self._K_link = K_link
        self._Kr_link = Kr_link
        self._T_link = T_link
        self._Tr_link = Tr_link

        self._Kadd_lump = [
            K[i] + K_link[i] + K_lump[i] + T_link[i]
            for i in range(len(self.frequencies))
        ]

    # ── Volume velocity (loads) ───────────────────────────────────────────

    def _ensure_volume_velocity(self) -> None:
        if self._volume_velocity is None:
            self._ensure_fetm_matrices()
            self._build_volume_velocity()

    def _build_volume_velocity(self) -> None:
        """
        Combines external volume velocity with prescribed acoustic pressure effects.
        Computes the combined load vector for all frequencies.
        """
        volume_velocity = self._assembly.get_global_volume_velocity()

        Kr = [
            (m.toarray())[self._unprescribed_indexes, :]
            for m in self._Kr
        ]
        Kr_link = [
            (m.toarray())[self._unprescribed_indexes, :]
            for m in self._Kr_link
        ]
        Kr_lump = [
            (m.toarray())[self._unprescribed_indexes, :]
            for m in self._Kr_lump
        ]
        Tr_link = [
            (m.toarray())[self._unprescribed_indexes, :]
            for m in self._Tr_link
        ]

        rows = Kr[0].shape[0]
        cols = len(self.frequencies)
        aux_ones = np.ones(cols, dtype=complex)
        vv_eq = np.zeros((rows, cols), dtype=complex)

        if len(self._prescribed_values) != 0:
            pv_list = []
            for value in self._prescribed_values:
                if isinstance(value, complex):
                    pv_list.append(aux_ones * value)
                elif isinstance(value, np.ndarray):
                    pv_list.append(value)

            self._array_prescribed_values = np.array(pv_list)
            for i in range(cols):
                pv_i = self._array_prescribed_values[:, i]
                vv_eq[:, i] = np.sum(
                    (Kr[i] + Kr_link[i] + Kr_lump[i] + Tr_link[i]) * pv_i,
                    axis=1,
                )

        self._volume_velocity = volume_velocity.T - vv_eq

    # ── FEM matrix construction (modal) ──────────────────────────────────

    def _ensure_modal_matrices(self) -> None:
        if self._K_modal is None:
            self._build_modal_matrices()

    def _build_modal_matrices(self) -> None:
        K, M = self._assembly.get_global_matrices_modal()
        K_link, M_link = self._assembly.get_link_global_matrices_modal()
        C, _ = self._assembly.get_lumped_matrices_for_FEM()

        self._K_modal = K + K_link
        self._M_modal = M + M_link
        self._C_modal = C

