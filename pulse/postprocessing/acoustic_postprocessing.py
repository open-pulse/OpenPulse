from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.model.model import Model
    from pulse.model.elements.acoustic.acoustic_element import AcousticElement


import numpy as np
from math import pi

N_div = 20


class AcousticPostprocessing:
    def __init__(self, model: "Model"):
        # if not isinstance(model, Model):
        #     raise ValueError("The model argument must be of type Model.")

        self.model = model

    @property
    def solution(self) -> None | np.ndarray:
        return self.model.acoustic_solution

    def get_acoustic_response_spectrum(
        self, node_id: int, absolute: bool = False, real_values: bool = False, imag_values: bool = False, dB_scale: bool = False
    ):

        node = self.model.preprocessor.nodes.get(node_id)
        dof_index = node.acoustic_global_dof[0]

        if absolute:
            return np.abs(self.solution[dof_index])

        elif real_values:
            return np.real(self.solution[dof_index])

        elif imag_values:
            return np.imag(self.solution[dof_index])

        elif dB_scale:
            p_ref = 20e-6
            return 20 * np.log10(np.abs(self.solution[dof_index] / (np.sqrt(2) * p_ref)))

        else:
            return self.solution[dof_index]

    def get_max_min_values_of_pressures(self, column: int):

        absolute = self.model.color_scale_setup.get("absolute", False)
        real_values = self.model.color_scale_setup.get("real_values", False)
        imag_values = self.model.color_scale_setup.get("imag_values", False)
        absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)
        
        data = self.solution.T[column]
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

    def get_acoustic_response(self, column: int, phase_step: float = 0):

        absolute = self.model.color_scale_setup.get("absolute", False)
        real_values = self.model.color_scale_setup.get("real_values", False)
        imag_values = self.model.color_scale_setup.get("imag_values", False)
        absolute_animation = self.model.color_scale_setup.get("absolute_animation", False)

        data = self.solution.T[column]

        if any([absolute, real_values, imag_values]):
            min_max_values = self.get_max_min_values_of_pressures(column)

        if absolute:
            pressures_to_plot = np.abs(data)
            return pressures_to_plot, min_max_values

        elif real_values:
            pressures_to_plot = np.real(data)
            return pressures_to_plot, min_max_values

        elif imag_values:
            pressures_to_plot = np.imag(data)
            return pressures_to_plot, min_max_values

        _pressures = np.abs(data)
        _phases = np.angle(data)
        _delta = -_phases[np.argmax(_pressures)]

        pressures_plot = _pressures*np.cos(_phases + phase_step + _delta)
        
        if absolute_animation:
            pressures_plot = np.abs(pressures_plot)

        min_max_values = [min(_pressures), max(_pressures)]
            
        return pressures_plot, min_max_values

def get_perforated_plate_acoustic_absortion(element: "AcousticElement", frequencies: np.ndarray):
    """
    """
    if isinstance(element.pp_impedance, np.ndarray):
        Z_pp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies)
        Z_pp = -element.pp_impedance

    Z_0 = element.fluid.impedance
    R = (Z_pp - Z_0)/(Z_pp + Z_0)
    alpha = 1 - R*np.conj(R)

    return np.real(alpha)

def get_perforated_plate_impedance(element: "AcousticElement", frequencies: np.ndarray):
    """
    """
    if isinstance(element.pp_impedance, np.ndarray):
        Z_pp = -element.pp_impedance
    else:
        element.update_pp_impedance(frequencies)
        Z_pp = -element.pp_impedance

    Z_0 = element.fluid.impedance

    return Z_pp / Z_0