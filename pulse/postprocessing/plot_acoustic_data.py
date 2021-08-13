import numpy as np
from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC

def get_acoustic_frf(preprocessor, solution, node, absolute=False, real=False, imag=False, dB=False):
    position = preprocessor.nodes[node].global_index * DOF_PER_NODE_ACOUSTIC
    if absolute:
        results = np.abs(solution[position])
    elif real:
        results = np.real(solution[position])
    elif imag:
        results = np.imag(solution[position])
    else:
        results = solution[position]
    if dB:
        p_ref = 20e-6
        results = 20*np.log10(np.abs(results/(np.sqrt(2)*p_ref)))
    return results

def get_acoustic_response(preprocessor, solution, column, real_part = True):
    if real_part:
        data = np.real(solution.T)
    else:
        data = np.abs(solution.T)
    rows = int(solution.shape[0])
    pressure = np.zeros((rows, 2))
    pressure[:,0] = np.arange( 0, rows, 1 )
    pressure[:,1] = data[column]
    
    u_def = data[column]

    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix
        
    return pressure, connect, coord, u_def

def get_acoustic_absortion(element, frequencies):
    if isinstance(element.pp_impedance, np.ndarray):
        zpp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies, False)
        zpp = -element.pp_impedance
    z0 = element.fluid.impedance
    R = (zpp - z0)/(zpp + z0)
    alpha = 1 - R*np.conj(R)
    return np.real(alpha)

def get_perforated_plate_impedance(element, frequencies, real_part):
    if isinstance(element.pp_impedance, np.ndarray):
        zpp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies, False)
        zpp = -element.pp_impedance
    z0 = element.fluid.impedance
    if real_part:
        data = np.real(zpp)/z0
    else:
        data = np.imag(zpp)/z0
    return data
