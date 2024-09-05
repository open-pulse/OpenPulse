from pulse import app
from pulse.model.node import DOF_PER_NODE_ACOUSTIC

import numpy as np
from math import pi

N_div = 20


def get_preprocessor():
    project = app().main_window.project
    return project.preprocessor


def get_acoustic_solution():
    project = app().main_window.project
    return project.get_acoustic_solution()


def get_color_scale_setup():
    project = app().main_window.project
    return project.color_scale_setup


def get_acoustic_frf(preprocessor, solution, node, **kwargs):

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)
    dB_scale = kwargs.get("dB_scale", False)

    position = preprocessor.nodes[node].global_index * DOF_PER_NODE_ACOUSTIC
    if absolute:
        return np.abs(solution[position])
    elif real_values:
        return np.real(solution[position])
    elif imag_values:
        return np.imag(solution[position])
    elif dB_scale:
        p_ref = 20e-6
        return 20*np.log10(np.abs(solution[position]/(np.sqrt(2)*p_ref)))
    else:
        return solution[position]


def get_max_min_values_of_pressures(solution, column, **kwargs):

    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)
    absolute_animation = kwargs.get("absolute_animation", False)
    
    color_scale_setup = get_color_scale_setup()
    if color_scale_setup:
        absolute = color_scale_setup["absolute"]
        real_values = color_scale_setup["real_values"]
        imag_values = color_scale_setup["imag_values"]
        absolute_animation = color_scale_setup["absolute_animation"]
    
    data = solution.T[column]
    _pressures = np.abs(data)
    _phases = np.angle(data)
    
    p_min = 1
    p_max = 0
    thetas = np.arange(0, N_div+1, 1)*(2*pi/N_div)

    if absolute:
        return min(np.abs(data)), max(np.abs(data))

    if real_values:
        return min(np.real(data)), max(np.real(data))

    if imag_values:
        return min(np.imag(data)), max(np.imag(data))

    for theta in thetas:
        pressures = _pressures*np.cos(theta + _phases)
        
        if absolute_animation:
            pressures = np.abs(pressures)

        p_min_i = min(pressures)
        p_max_i = max(pressures)

        if p_min_i < p_min:
            p_min = p_min_i
        if p_max_i > p_max:
            p_max = p_max_i
   
    return p_min, p_max


def get_acoustic_response(preprocessor, solution, column, **kwargs):

    phase_step = kwargs.get("phase_step", False)
    absolute = kwargs.get("absolute", False)
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)
    absolute_animation = kwargs.get("absolute_animation", False)
    
    color_scale_setup = get_color_scale_setup()
    if color_scale_setup:
        absolute = color_scale_setup["absolute"]
        real_values = color_scale_setup["real_values"]
        imag_values = color_scale_setup["imag_values"]
        absolute_animation = color_scale_setup["absolute_animation"]
    
    coord = preprocessor.nodal_coordinates_matrix
    connect = preprocessor.connectivity_matrix

    data = solution.T[column]
    
    if absolute:
        pressures_to_plot = np.abs(data)
        min_max_values = get_max_min_values_of_pressures(solution, column, **kwargs)
        return connect, coord, pressures_to_plot, min_max_values

    if real_values:
        pressures_to_plot = np.real(data)
        min_max_values = get_max_min_values_of_pressures(solution, column, **kwargs)
        return connect, coord, pressures_to_plot, min_max_values

    if imag_values:
        pressures_to_plot = np.imag(data)
        min_max_values = get_max_min_values_of_pressures(solution, column, **kwargs)
        return connect, coord, pressures_to_plot, min_max_values

    _pressures = np.abs(data)
    _phases = np.angle(data)

    pressures_plot = _pressures*np.cos(_phases + phase_step)
    
    if absolute_animation:
        pressures_plot = np.abs(pressures_plot)

    min_max_values = [min(_pressures), max(_pressures)]
        
    return connect, coord, pressures_plot, min_max_values


def get_acoustic_absortion(element, frequencies):
    """
    """
    if isinstance(element.pp_impedance, np.ndarray):
        zpp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies, False)
        zpp = -element.pp_impedance
    z0 = element.fluid.impedance
    R = (zpp - z0)/(zpp + z0)
    alpha = 1 - R*np.conj(R)
    return np.real(alpha)


def get_perforated_plate_impedance(element, frequencies, **kwargs):
    """
    """
    real_values = kwargs.get("real_values", False)
    imag_values = kwargs.get("imag_values", False)

    if isinstance(element.pp_impedance, np.ndarray):
        zpp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies, False)
        zpp = -element.pp_impedance

    z0 = element.fluid.impedance

    if real_values:
        return np.real(zpp)/z0
    elif imag_values:
        return np.imag(zpp)/z0
    else:
        return zpp/z0