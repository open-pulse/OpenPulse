from pulse.model.node import DOF_PER_NODE_STRUCTURAL

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.model.model import Model


import numpy as np
from math import pi

# from time import perf_counter

# LOCAL_DOFS = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)
DISP_LOCAL_DOFS = np.arange(int(DOF_PER_NODE_STRUCTURAL/2), dtype=int)


class StructuralPostprocessing:
    def __init__(self, model: "Model"):
        # if not isinstance(model, Model):
        #     raise ValueError("The model argument must be of type Model.")

        self.model = model

        self.n_div = 20
        
        # scaling factor
        self.scf = model.preprocessor.structure_principal_diagonal / 50

        # create a matrix (n_node x 3) containing the displacements ux, uy, uz indexes for all nodes
        n_nodes = self.model.mesh.nodal_coordinates.shape[0]
        self.uxyz_indexes = np.arange(n_nodes, dtype=int).reshape(-1, 1) * DOF_PER_NODE_STRUCTURAL + DISP_LOCAL_DOFS

    @property
    def solution(self) -> None | np.ndarray:
        return self.model.structural_solution

    def get_structural_response_spectrum(self, node_id: int, ldof_index: int, **kwargs) -> np.ndarray:

        absolute = kwargs.get("absolute", False)
        real_values = kwargs.get("real_values", False)
        imag_values = kwargs.get("imag_values", False)

        node = self.model.preprocessor.nodes.get(node_id)
        dof_index = node.structural_global_dof[ldof_index]

        if absolute:
            return np.abs(self.solution[dof_index])
        elif real_values:
            return np.real(self.solution[dof_index])
        elif imag_values:
            return np.imag(self.solution[dof_index])
        else:
            return self.solution[dof_index]

    def get_min_max_resultant_displacements(self, column: int):

        absolute = self.model.color_scale_setup.get("absolute", False)
        ux_abs_values = self.model.color_scale_setup.get("ux_abs_values", False)
        uy_abs_values = self.model.color_scale_setup.get("uy_abs_values", False)
        uz_abs_values = self.model.color_scale_setup.get("uz_abs_values", False)
        ux_real_values = self.model.color_scale_setup.get("ux_real_values", False)
        uy_real_values = self.model.color_scale_setup.get("uy_real_values", False)
        uz_real_values = self.model.color_scale_setup.get("uz_real_values", False)
        ux_imag_values = self.model.color_scale_setup.get("ux_imag_values", False)
        uy_imag_values = self.model.color_scale_setup.get("uy_imag_values", False)
        uz_imag_values = self.model.color_scale_setup.get("uz_imag_values", False)
        # absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)
        ux_animation = self.model.color_scale_setup.get("ux_animation", False)
        uy_animation = self.model.color_scale_setup.get("uy_animation", False)
        uz_animation = self.model.color_scale_setup.get("uz_animation", False)

        ind = np.arange(0, self.solution.shape[0], DOF_PER_NODE_STRUCTURAL)
        u_x, u_y, u_z = self.solution[ind+0, column], self.solution[ind+1, column], self.solution[ind+2, column]

        r_xyz_max = np.max((((np.abs(u_x))**2 + (np.abs(u_y))**2 + (np.abs(u_z))**2)**(1/2)))

        r_xyz = None

        if absolute:
            r_xyz = ((np.abs(u_x))**2 + (np.abs(u_y))**2 + (np.abs(u_z))**2)**(1/2)

        elif ux_abs_values:
            r_xyz = np.abs(u_x)

        elif uy_abs_values:
            r_xyz = np.abs(u_y)
        
        elif uz_abs_values:
            r_xyz = np.abs(u_z)
        
        elif ux_real_values:
            r_xyz = np.real(u_x)

        elif uy_real_values:
            r_xyz = np.real(u_y)
        
        elif uz_real_values:
            r_xyz = np.real(u_z)

        elif ux_imag_values:
            r_xyz = np.imag(u_x)

        elif uy_imag_values:
            r_xyz = np.imag(u_y)
        
        elif uz_imag_values:
            r_xyz = np.imag(u_z)

        if r_xyz is None:

            r_min, r_max = 1, 0

            amplitudes = np.abs(self.solution[:, column])
            phases_rad = np.angle(self.solution[:, column])
            phase_steps = np.arange(0, self.n_div + 1, 1) * ((2 * pi) / self.n_div)

            for phase_step in phase_steps:
                _nodal_solution = amplitudes * np.cos(phases_rad + phase_step)

                if ux_animation:
                    r_xyz = _nodal_solution[self.uxyz_indexes[:, 0]]

                elif uy_animation:
                    r_xyz = _nodal_solution[self.uxyz_indexes[:, 1]]

                elif uz_animation:
                    r_xyz = _nodal_solution[self.uxyz_indexes[:, 2]]

                else:
                    r_xyz = np.linalg.norm(_nodal_solution[self.uxyz_indexes.flatten()].reshape(-1, 3), axis=1)

                min_r_xyz = min(r_xyz)
                max_r_xyz = max(r_xyz)

                if min_r_xyz < r_min:
                    r_min = min_r_xyz

                if max_r_xyz > r_max:
                    r_max = max_r_xyz

        else:

            r_min = min(r_xyz)
            r_max = max(r_xyz)

        return r_xyz, r_min, r_max, r_xyz_max

    def get_structural_response(
        self, column: int, phase_step: float = 0, r_max: float | None = None, magnification_factor: float = 1.0, normalize: bool = True
    ) -> np.ndarray:

        absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)
        ux_animation = self.model.color_scale_setup.get("ux_animation", False)
        uy_animation = self.model.color_scale_setup.get("uy_animation", False)
        uz_animation = self.model.color_scale_setup.get("uz_animation", False)

        coords = self.model.preprocessor.mesh.nodal_coordinates

        if r_max is None:
            _, r_max = self.get_min_max_resultant_displacements(column)

        amplitudes = np.abs(self.solution[:, column])
        phases_rad = np.angle(self.solution[:, column])

        phase_shift = -phases_rad[np.argmax(amplitudes)]
        cossines_phases = np.cos(phases_rad + phase_step + phase_shift)

        _nodal_solution = amplitudes * cossines_phases

        if absolute_animation:
            r_xyz_plot = np.linalg.norm(_nodal_solution[self.uxyz_indexes.flatten()].reshape(-1, 3), axis=1)

        elif ux_animation:
            r_xyz_plot = _nodal_solution[self.uxyz_indexes[:, 0]]

        elif uy_animation:
            r_xyz_plot = _nodal_solution[self.uxyz_indexes[:, 1]]

        elif uz_animation:
            r_xyz_plot = _nodal_solution[self.uxyz_indexes[:, 2]]

        else:
            r_xyz_plot, *args = self.get_min_max_resultant_displacements(column)

        if normalize:
            if r_max == 0:
                r_max = 1
        else:
            r_max, self.scf = 1, 1

        # amplification factor
        mag_fact = magnification_factor * (self.scf / r_max)

        modif_nodal_solution = _nodal_solution * mag_fact

        # t0 = perf_counter()

        # deformed coordinates
        coord_def = coords.copy()
        coord_def[:, 1:] += modif_nodal_solution[self.uxyz_indexes]
        self.model.preprocessor.deformed_coordinates = coord_def

        # dt = perf_counter() - t0
        # print(f"Elapsed time (A): {dt : .8f} s")

        # t0 = perf_counter()

        for node in self.model.preprocessor.nodes.values():
            node.nodal_solution_gcs = modif_nodal_solution[node.structural_global_dof]

        self.model.preprocessor.process_element_cross_sections_orientation_to_plot(modif_nodal_solution)

        # dt = perf_counter() - t0
        # print(f"Elapsed time (B): {dt : .8f} s")

        return r_xyz_plot, mag_fact, phase_shift
    
    def get_min_max_stresses_values(self, stresses_data: dict | None = None):

        if stresses_data is None:
            stresses_data = self.model.stresses_values_for_color_table

        if isinstance(stresses_data, dict):
            values = np.array(list(stresses_data.values()))

        absolute = self.model.color_scale_setup.get("absolute", False)
        real_values = self.model.color_scale_setup.get("real_values", False)
        imag_values = self.model.color_scale_setup.get("imag_values", False)
        absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)

        if absolute:
            _values = np.abs(values)
            return np.min(_values), np.max(_values)
        
        elif real_values:
            _values = np.real(values)
            return np.min(_values), np.max(_values)
        
        elif imag_values:
            _values = np.imag(values)
            return np.min(_values), np.max(_values)

        stress_min = 1
        stress_max = 0
        _stresses = np.abs(values)
        phase = np.angle(values)
        thetas = np.arange(0, self.n_div + 1, 1) * (2 * pi / self.n_div)

        for theta in thetas:
            
            stresses = _stresses*np.cos(theta + phase)

            if absolute_animation:
                stresses = np.absolute(stresses)
            
            _stress_min = min(stresses)
            _stress_max = max(stresses)
            
            if _stress_min < stress_min:
                stress_min = _stress_min

            if _stress_max > stress_max:
                stress_max = _stress_max

        return stress_min, stress_max

    def get_stresses_to_plot(self, phase_step: float = 0.0, shift_phase: float = 0.0, stresses_data: dict | np.ndarray | None = None):

        absolute = self.model.color_scale_setup.get("absolute", False)
        real_values = self.model.color_scale_setup.get("real_values", False)
        imag_values = self.model.color_scale_setup.get("imag_values", False)
        absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)

        if stresses_data is None:
            stresses_data = self.model.stresses_values_for_color_table

        if isinstance(stresses_data, dict):
            keys = stresses_data.keys()
            values = np.array(list(stresses_data.values()))

        if absolute:
            stresses = np.abs(values)

        elif real_values:
            stresses = np.real(values)

        elif imag_values:
            stresses = np.imag(values)

        else:
            _stresses = np.abs(values)
            _phase = np.angle(values)

            # NOTE: the shift_phase variable is used to synchronize both 
            # the displacement and stress fields while computing
            # the animation-related data
            stresses = _stresses * np.cos(phase_step + _phase + shift_phase)

            if absolute_animation:
                stresses = np.absolute(stresses)

        stresses_data = dict(zip(keys, stresses))
        min_max_values = [min(stresses), max(stresses)]

        return stresses_data, min_max_values

    def get_reaction_spectrum(
        self, reactions: dict, node_id: int, ldof_index: int, absolute: bool = False, real_values: bool = False, imag_values: bool = False
    ):
        """
        This function returns a dictionary containing global dofs as its keys and the reactions as its values.
        """

        dof_index = self.model.preprocessor.nodes[node_id].index * DOF_PER_NODE_STRUCTURAL + ldof_index

        if absolute:
            results = np.abs(reactions[dof_index])
        elif real_values:
            results = np.real(reactions[dof_index])
        elif imag_values:
            results = np.imag(reactions[dof_index])
        else:
            results = reactions[dof_index]

        return results

def get_stress_spectrum_data(stresses: dict, element_id: int, stress_key: str, absolute: bool = False, real_values: bool = False, imag_values: bool = False) -> np.ndarray:

    if absolute:
        return np.abs(np.array(stresses[element_id][stress_key,:]))

    elif real_values:
        return np.real(np.array(stresses[element_id][stress_key,:]))

    elif imag_values:
        return np.imag(np.array(stresses[element_id][stress_key,:]))

    else:
        return np.array(stresses[element_id][stress_key,:])