from math import sqrt, pi
import numpy as np
from pulse.preprocessing.node import Node, distance

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2
PI = pi

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
        kLe = 2*PI*frequencies*(self.length + length_correction)  / self.speed_of_sound_corrected()
        sine = np.sin(kLe, dtype='float64')
        cossine = np.cos(kLe, dtype='float64')
        matrix = ((1j/(sine*self.impedance))*np.array([-cossine, ones, ones, -cossine])).T
        return matrix