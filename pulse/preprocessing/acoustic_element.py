from math import sqrt, pi
import numpy as np
from scipy.special import jv, struve
from pulse.preprocessing.node import Node, distance

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

def poly_function(x):
    a = np.array([0.6110035017201978, 0.028476407937161143, -0.26371506544764184, 0.24363292796929378, -0.11627424586622058, 0.027516286514019005, -0.00254838451051438])
    b = np.arange(7)
    x = x.reshape(-1, 1) @ np.ones([1,7])
    return (x**b ) @ a

def unflanged_termination_impedance(wave_number, pipe_radius, fluid_impedance):
    kr = wave_number * pipe_radius
    mask = kr<=1
    
    kr_less_t_1 = kr[mask]
    gamma = np.exp(0.5772)
    aux_1_1 = np.abs(np.exp((-kr_less_t_1**2)/2) * (1 + kr_less_t_1**4 / 6 * np.log(1 / (gamma * kr_less_t_1) + 19/12)))

    kr_great_t_1 = kr[~mask]
    aux_1_2 = np.abs(np.sqrt(pi * kr_great_t_1) * np.exp(-kr_great_t_1) * (1 + 3 / (32 * kr_great_t_1**2)))

    aux_1 = np.r_[aux_1_1, aux_1_2]

    aux_2 = - aux_1 * np.exp( -2j * kr * poly_function(kr))

    return fluid_impedance * (1 + aux_2)/(1 - aux_2) +0j

def flanged_termination_impedance(wave_number, pipe_radius, fluid_impedance):
    kr = wave_number * pipe_radius
    return fluid_impedance * (1 - jv(1,2*kr)/ kr  + 1j * struve(1,2*kr)/ kr  ) +0j

class AcousticElement:
    def __init__(self, first_node, last_node, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))
        self.acoustic_length_correction = kwargs.get('acoustic_length_correction', None)

    @property
    def length(self):
        return distance(self.first_node, self.last_node) 

    @property
    def orientation(self):
        return self.last_node.coordinates - self.first_node.coordinates

    @property
    def impedance(self):
        ''' Returns acoustic impedance as a ratio between specific_impedance and area '''
        return self.fluid.impedance / self.cross_section.area_fluid

    @property
    def global_dof(self):
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE] = self.first_node.global_index
        global_dof[DOF_PER_NODE:] = self.last_node.global_index
        return global_dof

    def global_matrix_indexes(self):
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows, cols

    def speed_of_sound_corrected(self):
        factor = self.cross_section.internal_diameter * self.fluid.bulk_modulus / (self.material.young_modulus * self.cross_section.thickness)
        return (1 / sqrt(1 + factor))*self.fluid.speed_of_sound
        
    def matrix(self, frequencies, ones, length_correction = 0):
        wave_number = 2*pi*frequencies / self.speed_of_sound_corrected()
        kLe = wave_number * (self.length + length_correction)
        sine = np.sin(kLe, dtype='float64')
        cossine = np.cos(kLe, dtype='float64')
        matrix = ((1j/(sine*self.impedance))*np.array([-cossine, ones, ones, -cossine])).T
        
        if self.first_node.radiation_impedance_type == 0:
            self.first_node.radiation_impedance = self.fluid.impedance + 0j
        elif self.first_node.radiation_impedance_type == 1:
            radius = self.cross_section.internal_diameter / 2
            fluid_impedance = self.fluid.impedance
            self.first_node.radiation_impedance = unflanged_termination_impedance(wave_number, radius, fluid_impedance)
        elif self.first_node.radiation_impedance_type == 2:
            radius = self.cross_section.internal_diameter / 2
            fluid_impedance = self.fluid.impedance
            self.first_node.radiation_impedance = flanged_termination_impedance(wave_number, radius, fluid_impedance)

        if self.last_node.radiation_impedance_type == 0:
            self.last_node.radiation_impedance = self.fluid.impedance + 0j
        elif self.last_node.radiation_impedance_type == 1:
            radius = self.cross_section.internal_diameter / 2
            fluid_impedance = self.fluid.impedance
            self.last_node.radiation_impedance = unflanged_termination_impedance(wave_number, radius, fluid_impedance)
        elif self.last_node.radiation_impedance_type == 2:
            radius = self.cross_section.internal_diameter / 2
            fluid_impedance = self.fluid.impedance
            self.last_node.radiation_impedance = flanged_termination_impedance(wave_number, radius, fluid_impedance)
        
        return matrix