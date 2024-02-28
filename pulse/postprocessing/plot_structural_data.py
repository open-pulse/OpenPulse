from pulse import app
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL

import numpy as np
from math import pi

N_div = 20


def get_preprocessor():
    project = app().main_window.project
    return project.preprocessor

def get_acoustic_solution():
    project = app().main_window.project
    return project.get_structural_solution()

def get_structural_frf(preprocessor, 
                       solution, 
                       node, 
                       dof, 
                       absolute=False, 
                       real=False, 
                       imaginary=False):

    position = preprocessor.nodes[node].global_index * DOF_PER_NODE_STRUCTURAL + dof
    if absolute:
        results = np.abs(solution[position])
    elif real:
        results = np.real(solution[position])
    elif imaginary:
        results = np.imag(solution[position])
    else:
        results = solution[position]
    return results


def get_max_min_values_of_resultant_displacements(solution, 
                                                  column, 
                                                  current_scaling):
    
    data = np.abs(solution)
    phases = np.angle(solution)
    ind = np.arange( 0, data.shape[0], DOF_PER_NODE_STRUCTURAL )
    #
    if current_scaling is None:
        scaling_type = "absolute"
    else:
        scaling_type = current_scaling

    #
    u_x, u_y, u_z = data[ind+0, column], data[ind+1, column], data[ind+2, column]
    _phases = np.array([phases[ind+0, column], phases[ind+1, column], phases[ind+2, column], 
                        phases[ind+3, column], phases[ind+4, column], phases[ind+5, column]]).T
    #
    r_min = 1
    r_max = 0
    thetas = np.arange(0, N_div+1, 1)*(2*pi/N_div)
    for theta in thetas:

        factor = np.cos(theta + _phases)
        if scaling_type == "absolute":
            # absolute r_xyz = |[Ux, Uy, Uz]|
            r_xyz = ((u_x*factor[:, 0])**2 + (u_y*factor[:, 1])**2 + (u_z*factor[:, 2])**2)**(1/2)
        elif scaling_type == "real_ux":
            # real part Ux
            r_xyz = u_x*factor[:, 0]
        elif scaling_type == "real_uy":
            # real part Uy
            r_xyz = u_y*factor[:, 1]
        elif scaling_type == "real_uz":
            # real part Uz
            r_xyz = u_z*factor[:, 2]
        else:
            NotImplementedError("Not supported scaling type.")

        min_r_xyz = min(r_xyz)
        max_r_xyz = max(r_xyz)

        if min_r_xyz < r_min:
            r_min = min_r_xyz
        if max_r_xyz > r_max:
            r_max = max_r_xyz
 
    return r_min, r_max


def get_structural_response(preprocessor, 
                            solution, 
                            column, 
                            phase_step = None, 
                            r_max = None,
                            new_scf = None, 
                            Normalize = True, 
                            scaling_type = None):
    
    # if r_max is None:
    _, r_max = get_max_min_values_of_resultant_displacements(solution, column, None)
    #
    data = np.abs(solution)
    phases = np.angle(solution)
    ind = np.arange( 0, data.shape[0], DOF_PER_NODE_STRUCTURAL )
    rows = int(data.shape[0]/DOF_PER_NODE_STRUCTURAL)
    u_x, u_y, u_z = data[ind+0, column], data[ind+1, column], data[ind+2, column]
    #
    if scaling_type is None:
        scaling_type = "absolute"
    #
    _phases = np.array([phases[ind+0, column], phases[ind+1, column], phases[ind+2, column], 
                        phases[ind+3, column], phases[ind+4, column], phases[ind+5, column]]).T
    #
    if new_scf is None:
        scf = preprocessor.structure_principal_diagonal/50
    # else:
    #     scf = new_scf

    if Normalize:
        # r_max = max(r_xyz)
        if r_max==0:
            r_max=1
    else:
        r_max, scf = 1, 1

    coord_def = np.zeros((rows,4))
    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix

    magnif_factor = scf/r_max
    if phase_step is None:
        factor = magnif_factor
    else:
        factor = magnif_factor*np.cos(phase_step + _phases)
    
    coord_def[:,0] = coord[:,0]
    coord_def[:,1] = coord[:,1] + u_x*factor[:, 0]
    coord_def[:,2] = coord[:,2] + u_y*factor[:, 1]
    coord_def[:,3] = coord[:,3] + u_z*factor[:, 2]

    if scaling_type == "absolute":
        # absolute r_xyz_plot = |[Ux, Uy, Uz]|
        r_xyz_plot = (((u_x*factor[:, 0])**2 + (u_y*factor[:, 1])**2 + (u_z*factor[:, 2])**2)**(1/2))/magnif_factor
    elif scaling_type == "real_ux":
        # real part Ux
        r_xyz_plot = u_x*factor[:, 0]/magnif_factor
    elif scaling_type == "real_uy":
        # real part Uy
        r_xyz_plot = u_y*factor[:, 1]/magnif_factor
    elif scaling_type == "real_uz":
        # real part Uz
        r_xyz_plot = u_z*factor[:, 2]/magnif_factor
    else:
        NotImplementedError("Not implemented scaling type.")
        
    min_max_values = [min(r_xyz_plot), max(r_xyz_plot)]

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

    return connect, coord_def, r_xyz_plot, magnif_factor, min_max_values


def get_reactions(preprocessor, 
                  reactions, 
                  node, 
                  dof, 
                  absolute=False, 
                  real=False, 
                  imaginary=False):
    """ This function returns a dictionary containing global dofs 
        as its keys and the reactions as its values. 
    """
    key = preprocessor.nodes[node].global_index * DOF_PER_NODE_STRUCTURAL + dof
    if absolute:
        results = np.abs(reactions[key])
    elif real:
        results = np.real(reactions[key])
    elif imaginary:
        results = np.imag(reactions[key])
    else:
        results = reactions[key]
    return results


def get_stress_spectrum_data(stresses, 
                             element_id, 
                             stress_key, 
                             absolute = False, 
                             real = False, 
                             imaginary = False):

    if absolute:
        return np.abs(np.array(stresses[element_id][stress_key,:]))
    elif real:
        return np.real(np.array(stresses[element_id][stress_key,:]))
    elif imaginary:
        return np.imag(np.array(stresses[element_id][stress_key,:]))
    else:
        return np.array(stresses[element_id][stress_key,:])


def get_min_max_stresses_values(data, scaling_type):

    if isinstance(data, dict):
        values = np.array(list(data.values()))

    if scaling_type is None:
        scaling_type = "absolute"

    stress_min = 1
    stress_max = 0
    _stresses = np.abs(values)
    phase = np.angle(values)
    thetas = np.arange(0, N_div+1, 1)*(2*pi/N_div)

    for theta in thetas:
        
        stresses = _stresses*np.cos(theta + phase)

        if scaling_type == "absolute":
            stresses = np.absolute(stresses)
        
        _stress_min = min(stresses)
        _stress_max = max(stresses)
        
        if _stress_min < stress_min:
            stress_min = _stress_min

        if _stress_max > stress_max:
            stress_max = _stress_max

    return stress_min, stress_max 


def get_stresses_to_plot(data, phase_step=None):
    if isinstance(data, dict):
        keys = data.keys()
        values = np.array(list(data.values()))
        
    _stresses = np.abs(values)
    _phase = np.angle(values)
    stresses = _stresses*np.cos(phase_step + _phase)
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