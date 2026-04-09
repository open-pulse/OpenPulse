import logging

import numpy as np
from pulse.interface.user_input.project.print_message import PrintMessageInput


_ERROR_TITLE = "Error"


class StructuralPostProcessor:
    """
    Post-processor for structural results.

    Computes reactions at constrained DOFs, reactions at springs/dampers,
    and element stress fields from the solution obtained by any solver.

    Parameters
    ----------
    source : solver instance or Project
        Either a HarmonicSolver / StaticSolver / ModalSolver instance whose
        ``assembler`` and ``solution`` attributes hold the relevant data, or a
        Project instance from which ``structural_solver`` is retrieved live.
    """

    def __init__(self, source):
        self._source = source
        self.reactions_at_constrained_dofs: dict | None = None
        self.dict_reactions_at_springs: dict | None = None
        self.dict_reactions_at_dampers: dict | None = None
        self.stress_field_dict: dict = {}

    # ── Solver / delegation properties ───────────────────────────────────

    @property
    def solver(self):
        """Return the solver, deriving it from a Project if that was passed."""
        src = self._source
        if hasattr(src, "structural_solver"):
            return src.structural_solver
        return src

    @property
    def model(self):
        return self.solver.assembler.model

    @property
    def assembler(self):
        return self.solver.assembler

    @property
    def solution(self):
        return self.solver.solution

    @property
    def frequencies(self):
        return self.solver.frequencies

    # ── Reactions at constrained DOFs ────────────────────────────────────

    def get_reactions_at_constrained_dofs(
        self, static_analysis: bool = False
    ) -> dict | None:
        """
        Compute reaction forces and moments at nodes with prescribed DOFs.

        Parameters
        ----------
        static_analysis : bool
            If True, treats the solution as a static analysis result
            (single column, zero frequency).

        Returns
        -------
        dict  {global_dof_index: np.ndarray of reactions per frequency}
        """
        if self.solution is None:
            return None

        Kr = self.assembler.Kr
        Mr = self.assembler.Mr
        Mr_exp_joint = self.assembler.Mr_exp_joint
        Kr_exp_joint = self.assembler.Kr_exp_joint
        prescribed_indexes = self.assembler.prescribed_indexes

        if Kr == [] or Mr == []:
            return None

        alpha, beta, eta = self.assembler.global_damping

        if static_analysis:
            _frequencies = np.array([0.0])
        else:
            _frequencies = self.frequencies

        n_freq = len(_frequencies)
        cols = len(prescribed_indexes)
        _reactions = np.zeros((n_freq, cols), dtype=complex)

        Ut = self.solution.T
        Kr_arr = Kr.toarray()
        Mr_arr = Mr.toarray() + Mr_exp_joint.toarray()
        Ut_Mr = Ut @ Mr_arr

        for j, freq in enumerate(_frequencies):
            logging.info(
                f"Evaluating structural reactions for constrained dofs "
                f"[{j + 1}/{n_freq}]"
            )
            omega = 2 * np.pi * freq
            Ut_Kr = Ut[j, :] @ (Kr_arr + Kr_exp_joint[j].toarray())

            F_K = Ut_Kr
            F_M = -(omega ** 2) * Ut_Mr[j, :]
            F_C = 1j * (
                (eta + omega * beta) * Ut_Kr
                + (omega * alpha) * Ut_Mr[j, :]
            )
            _reactions[j, :] = F_K + F_M + F_C

        load_reactions = {
            prescribed_indexes[i]: _reactions[:, i]
            for i in range(len(prescribed_indexes))
        }
        self.reactions_at_constrained_dofs = load_reactions
        return load_reactions

    # ── Reactions at springs and dampers ──────────────────────────────────

    def get_reactions_at_springs_and_dampers(
        self, static_analysis: bool = False
    ) -> tuple[dict, dict]:
        """
        Compute reactions at dampers and springs connected to ground.

        Returns
        -------
        (dict_reactions_at_springs, dict_reactions_at_dampers)
        """
        dict_springs: dict = {}
        dict_dampers: dict = {}

        if self.solution is None:
            return dict_springs, dict_dampers

        U = self.solution

        if static_analysis:
            cols = 1
            _frequencies = np.array([0.0])
        else:
            cols = len(self.frequencies)
            _frequencies = self.frequencies

        omega = 2 * np.pi * _frequencies

        springs_stiffness = []
        dampers_dampings = []
        global_dofs_springs = []
        global_dofs_dampers = []

        for (prop, *args), data in self.model.properties.nodal_properties.items():
            if prop == "lumped_stiffness":
                node_id = args[0]
                node = self.model.preprocessor.nodes[node_id]
                global_dofs_springs.append(node.global_dof)
                values = data["values"]
                if "table_names" in data:
                    springs_stiffness.append(
                        [
                            np.zeros_like(self.frequencies) if v is None else v
                            for v in values
                        ]
                    )
                else:
                    springs_stiffness.append(
                        [
                            np.zeros_like(self.frequencies) if v is None
                            else np.ones_like(self.frequencies) * v
                            for v in values
                        ]
                    )

            elif prop == "lumped_dampings":
                node_id = args[0]
                node = self.model.preprocessor.nodes[node_id]
                global_dofs_dampers.append(node.global_dof)
                values = data["values"]
                if "table_names" in data:
                    dampers_dampings.append(
                        [
                            np.zeros_like(self.frequencies) if v is None else v
                            for v in values
                        ]
                    )
                else:
                    dampers_dampings.append(
                        [
                            np.zeros_like(self.frequencies) if v is None
                            else np.ones_like(self.frequencies) * v
                            for v in values
                        ]
                    )

        if springs_stiffness:
            gdofs = np.array(global_dofs_springs).flatten()
            stiff = np.array(springs_stiffness).reshape(-1, cols)
            reactions = stiff * U[gdofs, :]
            for i, gdof in enumerate(gdofs):
                dict_springs[gdof] = reactions[i, :]
            self.dict_reactions_at_springs = dict_springs

        if dampers_dampings:
            gdofs = np.array(global_dofs_dampers).flatten()
            damp = np.array(dampers_dampings).reshape(-1, cols)
            reactions = (1j * omega) * damp * U[gdofs, :]
            for i, gdof in enumerate(gdofs):
                dict_dampers[gdof] = reactions[i, :]
            self.dict_reactions_at_dampers = dict_dampers

        return dict_springs, dict_dampers

    # ── Stress field ──────────────────────────────────────────────────────

    def stress_calculate(
        self,
        external_pressure: float = 0.0,
        damping: bool = False,
        static_analysis: bool = False,
        real_values: bool = False,
    ) -> dict:
        """
        Compute the stress field across all structural elements.

        Parameters
        ----------
        external_pressure : float
            Static external pressure (atm - fluid difference).
        damping : bool
            If True, includes damping effect in the stress computation.
        static_analysis : bool
            If True, treats the solution as a static result.
        real_values : bool
            If True, returns only the real part of the stresses.

        Returns
        -------
        dict  {element_index: stress_array (7 × n_freqs)}
            Rows: axial, bending-y, bending-z, hoop, torsional,
                  shear-xy, shear-xz.
        """
        self.stress_field_dict = {}

        if damping:
            _, beta, eta = self.assembler.global_damping
        else:
            beta = eta = 0.0

        if static_analysis:
            _frequencies = np.array([0], dtype=float)
        else:
            _frequencies = self.frequencies

        structural_elements = self.model.preprocessor.structural_elements.values()
        omega = 2 * np.pi * _frequencies.reshape(1, -1)
        damp_factor = np.ones([6, 1]) @ (1 + 1j * (eta + omega * beta))

        acoustic_solution = self.assembler.acoustic_solution
        p0 = external_pressure

        for element in structural_elements:

            if element.element_type in ["beam_1", "expansion_joint", "valve"]:
                element.stress = np.zeros((7, len(_frequencies)))

            elif element.element_type == "pipe_1":
                struct_dofs = np.r_[
                    element.first_node.global_dof,
                    element.last_node.global_dof,
                ]

                if self.solution is None:
                    PrintMessageInput(
                        [
                            _ERROR_TITLE,
                            "Empty solution",
                            "A structural analysis must be performed to obtain the stress field.",
                        ]
                    )
                    return {}

                u = self.solution[struct_dofs, :]
                Dab = element._Dab
                Bab = element._Bab
                Dts = element._Dts
                Bts = element._Bts
                rot = element.element_rotation_matrix
                T = element.cross_section.principal_axis_translation

                normal = Dab @ Bab @ T @ rot @ u
                shear = Dts @ Bts @ T @ rot @ u
                element.internal_load = np.multiply(np.r_[normal, shear], damp_factor)

                do = element.cross_section.outer_diameter
                di = element.cross_section.inner_diameter
                ro = do / 2
                area = element.cross_section.area
                Iy = element.cross_section.second_moment_area_y
                Iz = element.cross_section.second_moment_area_z
                J = element.cross_section.polar_moment_area
                nu = element.material.poisson_ratio

                acoustic_dofs = np.r_[
                    element.first_node.global_index,
                    element.last_node.global_index,
                ]
                if acoustic_solution is not None:
                    p = acoustic_solution[acoustic_dofs, :]
                else:
                    p = np.zeros((2, len(_frequencies)))

                pm = np.sum(p, axis=0) / 2

                if element.wall_formulation == "thick_wall":
                    hoop_stress = (
                        2 * pm * di ** 2 - p0 * (do ** 2 + di ** 2)
                    ) / (do ** 2 - di ** 2)
                    radial_stress = (
                        -2 * nu * (pm * di ** 2 - p0 * do ** 2)
                        / (do ** 2 - di ** 2)
                    )
                else:  # thin_wall
                    hoop_stress = pm
                    radial_stress = -nu * np.pi * (do / (do - di) - 1)

                stress_data = np.c_[
                    element.internal_load[0] / area - radial_stress,
                    element.internal_load[1] * ro / Iy,
                    element.internal_load[2] * ro / Iz,
                    hoop_stress,
                    element.internal_load[3] * ro / J,
                    element.internal_load[4] / area,
                    element.internal_load[5] / area,
                ].T

                element.stress = np.real(stress_data) if real_values else stress_data

            self.stress_field_dict[element.index] = element.stress

        return self.stress_field_dict
