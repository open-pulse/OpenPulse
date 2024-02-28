from pulse import app
from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC

import numpy as np
from math import pi

N_div = 20


def get_preprocessor():
    project = app().main_window.project
    return project.preprocessor

def get_acoustic_solution():
    project = app().main_window.project
    return project.get_acoustic_solution()

def get_acoustic_frf(node, absolute=False, real=False, imag=False, dB=False):

    preprocessor = get_preprocessor()
    solution = get_acoustic_solution()

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

def get_max_min_values_of_pressures(column, absolute=False):

    solution = get_acoustic_solution()
    
    data = solution.T[column]
    _pressures = np.abs(data)
    _phases = np.angle(data)
    
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

def get_acoustic_response(column, phase_step=None, absolute=False):

    preprocessor = get_preprocessor()
    solution = get_acoustic_solution()

    data = solution.T[column]

    _pressures = np.abs(data)
    _phases = np.angle(data)

    pressures_plot = _pressures*np.cos(_phases + phase_step)
    
    if absolute:
        pressures_plot = np.abs(pressures_plot)

    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix

    min_max_values = [min(_pressures), max(_pressures)]
        
    return connect, coord, pressures_plot, min_max_values

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
