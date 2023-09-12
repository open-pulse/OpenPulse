import numpy as np
from math import pi
from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC
N_div = 20

def get_acoustic_frf(preprocessor, solution, node, absolute=False, real=False, imag=False, dB=False):
    position = preprocessor.nodes[node].global_index * DOF_PER_NODE_ACOUSTIC
    if absolute:
        results = np.abs(solution[position])
    elif real:
        results = np.real(solution[position])
    elif imag:
        results = np.imag(solution[position])
    elif dB:
        p_ref = 20e-6
        results = 20*np.log10(np.abs(solution[position]/(np.sqrt(2)*p_ref)))
    else:
        results = solution[position]
    return results

def get_max_min_values_of_pressures(solution, column, absolute=False):
    
    _pressures = np.abs(solution.T[column])
    _phases = np.angle(solution.T)[column]
    
    p_min = 1
    p_max = 0
    thetas = np.arange(0, N_div+1, 1)*(2*pi/N_div)

    for theta in thetas:
        pressures = _pressures*np.cos(theta + _phases)
        
        if absolute:
            pressures = np.abs(pressures)

        p_min_i = min(pressures)
        p_max_i = max(pressures)

        if p_min_i < p_min:
            p_min = p_min_i
        if p_max_i > p_max:
            p_max = p_max_i
   
    return p_min, p_max

def get_acoustic_response(preprocessor, solution, column, phase_step=None, absolute=True):
    
    # if absolute:
    #     data = np.abs(solution.T)
    # else:
    #     data = np.real(solution.T)
    
    data = np.abs(solution.T)

    _pressures = data[column]
    _phases = np.angle(solution.T)[column]

    rows = int(solution.shape[0])
    pressure = np.zeros((rows, 2))
    pressure[:,0] = np.arange( 0, rows, 1 )
    pressure[:,1] = _pressures

    pressures_plot = _pressures*np.cos(phase_step + _phases)
    
    if absolute:
        pressures_plot = np.abs(pressures_plot)

    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix

    min_max_values = [min(_pressures), max(_pressures)]
        
    return pressure, connect, coord, pressures_plot, min_max_values

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
