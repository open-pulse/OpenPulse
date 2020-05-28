from math import sqrt, pi
import numpy as np
from pulse.preprocessing.node import Node, distance

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2
PI = pi

class Element:
    def __init__(self, first_node, last_node, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.material = kwargs.get('material', None)
        self.fluid = kwargs.get('fluid', None)   
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))

    @property
    def length(self):
        return distance(self.first_node, self.last_node) 

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
        
    # def matrix(self, frequencies, ones):
    #     kLe = 2*PI*frequencies*(self.length / self.fluid.sound_velocity) 
    #     matrix = ((1j/(np.sin(kLe, dtype='float64')*self.impedance))*np.array([-np.cos(kLe, dtype='float64'), ones, ones, -np.cos(kLe, dtype='float64')])).T
    #     # matrix = np.zeros([len(frequencies), ENTRIES_PER_ELEMENT], dtype = complex)
    #     # for i, value in enumerate(kLe):
    #     #     matrix[i,:] = 1j / (sin(value) * Z) * np.array([-cos(value), 1, 1, -cos(value)])   
    #     return matrix

    def sound_velocity_corrected(self):
        factor = self.cross_section.internal_diameter * self.fluid.bulk_modulus / (self.material.young_modulus * self.cross_section.thickness)
        return (1 / sqrt(1 + factor))*self.fluid.sound_velocity
        
    def matrix(self, frequencies, ones):
        kLe = 2*PI*frequencies*self.length / self.sound_velocity_corrected()
        sine = np.sin(kLe, dtype='float64')
        cossine = np.cos(kLe, dtype='float64')
        matrix = ((1j/(sine*self.impedance))*np.array([-cossine, ones, ones, -cossine])).T
        return matrix