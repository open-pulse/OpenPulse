from pulse import app
from pulse.model.node import DOF_PER_NODE_STRUCTURAL

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.model.preprocessor import Preprocessor

import numpy as np
from math import pi

N_div = 20


def get_preprocessor():
    project = app().main_window.project
    return project.model.preprocessor


def get_structural_solution():
    project = app().main_window.project
    return project.get_structural_solution()


def get_color_scale_setup():
    project = app().main_window.project
    return project.color_scale_setup


def get_structural_frf(preprocessor: "Preprocessor", solution: np.ndarray, node_id: int, dof_index: int, **kwargs) -> np.ndarray:

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)

    position = preprocessor.nodes[node_id].global_index * DOF_PER_NODE_STRUCTURAL + dof_index

    if absolute:
        return np.abs(solution[position])
    elif real_values:
        return np.real(solution[position])
    elif imag_values:
        return np.imag(solution[position])
    else:
        return solution[position]


def get_min_max_resultant_displacements(solution: np.ndarray, column: int, **kwargs):

    absolute = kwargs.get("absolute", False)
    ux_abs_values = kwargs.get("ux_abs_values", False)
    uy_abs_values = kwargs.get("uy_abs_values", False)
    uz_abs_values = kwargs.get("uz_abs_values", False)
    ux_real_values = kwargs.get("ux_real_values", False)
    uy_real_values = kwargs.get("uy_real_values", False)
    uz_real_values = kwargs.get("uz_real_values", False)
    ux_imag_values = kwargs.get("ux_imag_values", False)
    uy_imag_values = kwargs.get("uy_imag_values", False)
    uz_imag_values = kwargs.get("uz_imag_values", False)
    absolute_animation = kwargs.get("absolute_animation", False)
    
    try:
        color_scale_setup = get_color_scale_setup()
        if color_scale_setup:
            absolute = color_scale_setup["absolute"]
            ux_abs_values = color_scale_setup["ux_abs_values"]
            uy_abs_values = color_scale_setup["uy_abs_values"]
            uz_abs_values = color_scale_setup["uz_abs_values"]
            ux_real_values = color_scale_setup["ux_real_values"]
            uy_real_values = color_scale_setup["uy_real_values"]
            uz_real_values = color_scale_setup["uz_real_values"]
            ux_imag_values = color_scale_setup["ux_imag_values"]
            uy_imag_values = color_scale_setup["uy_imag_values"]
            uz_imag_values = color_scale_setup["uz_imag_values"]
            absolute_animation = color_scale_setup["absolute_animation"]
            ux_animation = color_scale_setup["ux_animation"]
            uy_animation = color_scale_setup["uy_animation"]
            uz_animation = color_scale_setup["uz_animation"]
    except:
        absolute_animation = True

    ind = np.arange(0, solution.shape[0], DOF_PER_NODE_STRUCTURAL)
    u_x, u_y, u_z = solution[ind+0, column], solution[ind+1, column], solution[ind+2, column]

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

        phases = np.angle(solution)
        _phases = np.array([phases[ind+0, column], phases[ind+1, column], phases[ind+2, column], 
                            phases[ind+3, column], phases[ind+4, column], phases[ind+5, column]]).T

        r_min = 1
        r_max = 0
        thetas = np.arange(0, N_div + 1, 1)*(2 * pi / N_div)
        for theta in thetas:

            factor = np.cos(theta + _phases)

            if absolute_animation:
                # absolute r_xyz = |[Ux, Uy, Uz]|
                r_xyz = ((np.abs(u_x)*factor[:, 0])**2 + (np.abs(u_y)*factor[:, 1])**2 + (np.abs(u_z)*factor[:, 2])**2)**(1/2)
            
            elif ux_animation:
                r_xyz = np.abs(u_x)*factor[:, 0]
            
            elif uy_animation:
                r_xyz = np.abs(u_y)*factor[:, 1]
            
            elif uz_animation:
                r_xyz = np.abs(u_z)*factor[:, 2]
            
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


def get_structural_response(preprocessor: "Preprocessor", solution: np.ndarray, column: int, **kwargs) -> np.ndarray:

    phase_step = kwargs.get("phase_step", None)
    r_max = kwargs.get("r_max", None)
    new_scf = kwargs.get("new_scf", None)
    Normalize = kwargs.get("Normalize", True)

    absolute_animation = kwargs.get("absolute_animation", False)
    ux_animation = kwargs.get("ux_animation", False)
    uy_animation = kwargs.get("uy_animation", False)
    uz_animation = kwargs.get("uz_animation", False)

    color_scale_setup = get_color_scale_setup()
    try:
        if color_scale_setup:
            absolute_animation = color_scale_setup["absolute_animation"]
            ux_animation = color_scale_setup["ux_animation"]
            uy_animation = color_scale_setup["uy_animation"]
            uz_animation = color_scale_setup["uz_animation"]
    except:
        absolute_animation = True

    rows = int(solution.shape[0]/DOF_PER_NODE_STRUCTURAL)
    ind = np.arange(0, solution.shape[0], DOF_PER_NODE_STRUCTURAL, dtype=int)

    u_x, u_y, u_z = solution[ind+0, column], solution[ind+1, column], solution[ind+2, column]
    
    if r_max is None:
        _, r_max = get_min_max_resultant_displacements(solution, column)
    
    # min_max_values_all = [r_min, r_max]

    phases = np.angle(solution)
    _phases = np.array([phases[ind+0, column], phases[ind+1, column], phases[ind+2, column], 
                        phases[ind+3, column], phases[ind+4, column], phases[ind+5, column]]).T

    if new_scf is None:
        scf = preprocessor.structure_principal_diagonal / 50

    if Normalize:
        if r_max == 0:
            r_max = 1
    else:
        r_max, scf = 1, 1

    coord_def = np.zeros((rows,4), dtype=float)
    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix

    magnif_factor = scf/r_max
    if phase_step is None:
        factor = magnif_factor
    else:
        factor = magnif_factor*np.cos(phase_step + _phases)
    
    coord_def[:,0] = coord[:,0]
    coord_def[:,1] = coord[:,1] + np.abs(u_x)*factor[:, 0]
    coord_def[:,2] = coord[:,2] + np.abs(u_y)*factor[:, 1]
    coord_def[:,3] = coord[:,3] + np.abs(u_z)*factor[:, 2]
    
    if absolute_animation:
        # absolute r_xyz_plot = |[Ux, Uy, Uz]|
        r_xyz_plot = ((np.abs(u_x)*factor[:, 0])**2 + (np.abs(u_y)*factor[:, 1])**2 + (np.abs(u_z)*factor[:, 2])**2)**(1/2)/magnif_factor
    elif ux_animation:
        r_xyz_plot = np.abs(u_x)*factor[:, 0]/magnif_factor
    elif uy_animation:
        r_xyz_plot = np.abs(u_y)*factor[:, 1]/magnif_factor
    elif uz_animation:
        r_xyz_plot = np.abs(u_z)*factor[:, 2]/magnif_factor
    else:
        r_xyz_plot, *args = get_min_max_resultant_displacements(solution, column)
    
    data = np.abs(solution)
    nodal_solution_gcs = np.array([ data[ind+0, column], data[ind+1, column], data[ind+2, column],
                                    data[ind+3, column], data[ind+4, column], data[ind+5, column] ]).T*factor
 
    nodes = preprocessor.nodes
    for node in nodes.values():
        global_index = node.global_index
        node.deformed_coordinates = coord_def[global_index, 1:]       
        node.nodal_solution_gcs = nodal_solution_gcs[global_index, :]
        node.deformed_displacements_xyz_gcs =  nodal_solution_gcs[global_index, [0,1,2]]
        node.deformed_rotations_xyz_gcs =  nodal_solution_gcs[global_index, [3,4,5]]

    preprocessor.process_element_cross_sections_orientation_to_plot()

    return connect, coord_def, r_xyz_plot, magnif_factor


def get_reactions(reactions: dict, node_id: int, dof_index: int, **kwargs):
    """ This function returns a dictionary containing global dofs 
        as its keys and the reactions as its values. 
    """

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)

    preprocessor = get_preprocessor()

    key = preprocessor.nodes[node_id].global_index * DOF_PER_NODE_STRUCTURAL + dof_index
    if absolute:
        results = np.abs(reactions[key])
    elif real_values:
        results = np.real(reactions[key])
    elif imag_values:
        results = np.imag(reactions[key])
    else:
        results = reactions[key]
    return results


def get_stress_spectrum_data(stresses: dict, element_id: int, stress_key: str, **kwargs) -> np.array:

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)

    if absolute:
        return np.abs(np.array(stresses[element_id][stress_key,:]))
    elif real_values:
        return np.real(np.array(stresses[element_id][stress_key,:]))
    elif imag_values:
        return np.imag(np.array(stresses[element_id][stress_key,:]))
    else:
        return np.array(stresses[element_id][stress_key,:])


def get_min_max_stresses_values(**kwargs):

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)
    absolute_animation = kwargs.get("absolute_animation", False)
    stresses_data = kwargs.get("stresses_data", None)

    if stresses_data is None:
        project = app().main_window.project
        stresses_data = project.stresses_values_for_color_table

    if isinstance(stresses_data, dict):
        values = np.array(list(stresses_data.values()))

    color_scale_setup = get_color_scale_setup()
    if color_scale_setup:
        absolute = color_scale_setup["absolute"]
        real_values = color_scale_setup["real_values"]
        imag_values = color_scale_setup["imag_values"]
        absolute_animation = color_scale_setup["absolute_animation"]

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
    thetas = np.arange(0, N_div+1, 1)*(2*pi/N_div)

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


def get_stresses_to_plot(**kwargs):

    phase_step = kwargs.get("phase_step", False)
    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)
    absolute_animation = kwargs.get("absolute_animation", False)
    stresses_data = kwargs.get("stresses_data", None)

    if stresses_data is None:
        project = app().main_window.project
        stresses_data = project.stresses_values_for_color_table

    if isinstance(stresses_data, dict):
        keys = stresses_data.keys()
        values = np.array(list(stresses_data.values()))

    color_scale_setup = get_color_scale_setup()
    if color_scale_setup:
        absolute = color_scale_setup["absolute"]
        real_values = color_scale_setup["real_values"]
        imag_values = color_scale_setup["imag_values"]
        absolute_animation = color_scale_setup["absolute_animation"]

    if absolute:
        stresses = np.abs(values)

    elif real_values:
        stresses = np.real(values)

    elif imag_values:
        stresses = np.imag(values)

    else:
        _stresses = np.abs(values)
        _phase = np.angle(values)
        stresses = _stresses*np.cos(phase_step + _phase)

        if absolute_animation:
            stresses = np.absolute(stresses)
    
    stresses_data = dict(zip(keys, stresses))
    min_max_values = [min(stresses), max(stresses)]

    return stresses_data, min_max_values

# def get_internal_loads_data(preprocessor, column, absolute=False, real=False, imaginary=False):

#     elements = preprocessor.structural_elements
#     internal_loads = [np.r_[i, elements[i].internal_load[:, column]] for i in elements ]
#     if absolute:
#         return np.abs(np.array(internal_loads))
#     elif real:
#         return np.real(np.array(internal_loads))
#     elif imaginary:
#         return np.imag(np.array(internal_loads))
#     else:
#         return np.array(internal_loads) 