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

    def __init__(self, model: Model, harmonic_method: str = "fetm"):

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
        self._harmonic_method = harmonic_method

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
        self._volume_velocity_fem: np.ndarray | None = None
        self._array_prescribed_values: np.ndarray | None = None

        # FEM matrices (modal) — pre-computed on demand
        self._K_modal: spmatrix | None = None
        self._M_modal: spmatrix | None = None
        self._C_modal: spmatrix | None = None

        # FEM harmonic matrices — only populated when harmonic_method == "fem"
        self._K_fem: spmatrix | None = None
        self._M_fem: spmatrix | None = None
        self._Kr_fem: spmatrix | None = None
        self._Mr_fem: spmatrix | None = None
        self._T_link_fem: list | None = None   # FETM transfer per freq [n_u × n_u]
        self._Tr_link_fem: list | None = None  # prescribed coupling per freq [n_u × n_p]
        self._C_lump_fem: list | None = None
        self._Cr_lump_fem: list | None = None
        self._K_pp_fem: list | None = None     # FETM admittance for non-COMMON_PIPE PP [n_u × n_u]
        self._Kr_pp_fem: list | None = None    # prescribed coupling for PP [n_u × n_p]

        # Perforated plate nonlinearity
        self._nl_elements: list = self._detect_nl_pp_elements()
        self.convergence_target: float = 0.10  # 10 %
        self.convergence_data_log: list | None = None
        self.convergence_plot = None  # set by HarmonicSolver after the run
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
        if self._harmonic_method == "fem":
            self._build_fem_harmonic_matrices()
            self._volume_velocity_fem = None
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
        if self._harmonic_method == "fem":
            self._ensure_fem_harmonic_matrices()
            return (self._K_fem
                    - (omega ** 2) * self._M_fem
                    + 1j * omega * self._C_lump_fem[index]
                    + self._T_link_fem[index]
                    + self._K_pp_fem[index])
        # default: FETM
        self._ensure_fetm_matrices()
        return self._Kadd_lump[index]

    def get_load_vector(self, index: int, omega: float) -> np.ndarray:
        if self._harmonic_method == "fem":
            return self._get_fem_load_vector(index, omega)
        # default: FETM
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

    # ── FEM harmonic matrix construction ─────────────────────────────────

    def _ensure_fem_harmonic_matrices(self) -> None:
        if self._K_fem is None:
            self._build_fem_harmonic_matrices()

    def _build_fem_harmonic_matrices(self) -> None:
        """Hybrid: FEM for pipe/link elements + FETM for transfer elements and non-COMMON_PIPE PP."""
        K, Kr, M, Mr = self._assembly.get_global_matrices_modal()
        K_link, M_link = self._assembly.get_link_global_matrices_modal()
        T_link, Tr_link = self._assembly.get_fetm_transfer_matrices()
        C_lump, Cr_lump = self._assembly.get_lumped_matrices_for_FEM()
        K_pp, Kr_pp = self._assembly.get_fetm_pp_matrices()

        self._K_fem  = K + K_link
        self._Kr_fem = Kr
        self._M_fem  = M + M_link
        self._Mr_fem = Mr
        self._T_link_fem  = T_link
        self._Tr_link_fem = [m[self._unprescribed_indexes, :] for m in Tr_link]
        self._C_lump_fem  = C_lump
        self._Cr_lump_fem = [m[self._unprescribed_indexes, :] for m in Cr_lump]
        self._K_pp_fem  = K_pp
        self._Kr_pp_fem = Kr_pp

    def _get_fem_load_vector(self, index: int, omega: float) -> np.ndarray:
        """FEM load vector: iω·Q_ext - (Kr - ω²Mr + iωCr + Tr_link) @ p_presc

        The iω factor arises from the weak form of the Helmholtz equation: a
        volume velocity source Q [m³/s] at a boundary node contributes iω·Q
        to the nodal load vector (boundary integral of v_n against the test
        function, with harmonic e^{iωt} convention).
        """
        self._ensure_fem_harmonic_matrices()
        self._ensure_volume_velocity_fem()

        f = 1j * omega * self._volume_velocity_fem[:, index].copy()

        if len(self._prescribed_values) != 0:
            p_presc = self._array_prescribed_values[:, index]
            f -= (self._Kr_fem
                  - (omega ** 2) * self._Mr_fem
                  + 1j * omega * self._Cr_lump_fem[index]
                  + self._Tr_link_fem[index]
                  + self._Kr_pp_fem[index]) @ p_presc
        return f

    def _ensure_volume_velocity_fem(self) -> None:
        if self._volume_velocity_fem is None:
            self._build_volume_velocity_fem()

    def _build_volume_velocity_fem(self) -> None:
        """External volume velocity for FEM path; prescribed-DOF correction in get_load_vector."""
        volume_velocity = self._assembly.get_global_volume_velocity()

        if len(self._prescribed_values) != 0:
            aux_ones = np.ones(len(self.frequencies), dtype=complex)
            pv_list = []
            for value in self._prescribed_values:
                if isinstance(value, complex):
                    pv_list.append(aux_ones * value)
                elif isinstance(value, np.ndarray):
                    pv_list.append(value)
            self._array_prescribed_values = np.array(pv_list)

        self._volume_velocity_fem = volume_velocity.T  # (n_unprescribed, n_freqs)

    # ── FEM matrix construction (modal) ──────────────────────────────────

    def _ensure_modal_matrices(self) -> None:
        if self._K_modal is None:
            self._build_modal_matrices()

    def _build_modal_matrices(self) -> None:
        K, _Kr, M, _Mr = self._assembly.get_global_matrices_modal()
        K_link, M_link = self._assembly.get_link_global_matrices_modal()
        C, _ = self._assembly.get_lumped_matrices_for_FEM()

        self._K_modal = K + K_link
        self._M_modal = M + M_link
        self._C_modal = C

