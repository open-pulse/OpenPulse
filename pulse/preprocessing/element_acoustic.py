from math import pi, sqrt, sin, cos

import numpy as np

from pulse.preprocessing.node import Node, distance

DOF_PER_NODE = 1
NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


class Element:
    def __init__(self, first_node, last_node, first_node_id = -1, last_node_id = -1, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.first_node_id = first_node_id
        self.last_node_id = last_node_id
        self.fluid = kwargs.get('fluid', None)
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_pressure = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE))

    @property
    def length(self):
        return distance(self.first_node, self.last_node) 

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

    @property
    def impedance(self):
        area = self.cross_section.area_fluid
        specific_impedance = self.fluid.impedance
        return specific_impedance / area
    
    def matrix(self, frequencies):
        omega = 2 * pi * frequencies
        wave_number = omega / self.fluid.sound_velocity
        kLe = wave_number * self.length
        Z = self.impedance
        matrix = np.zeros([len(frequencies), ENTRIES_PER_ELEMENT], dtype = complex)

        for i, value in enumerate(kLe):
            matrix[i,:] = 1j / (sin(value) * Z) * np.array([-cos(value), 1, 1, -cos(value)])
            
        return matrix