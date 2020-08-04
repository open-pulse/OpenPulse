import numpy as np
from math import pi
from numpy import sqrt
from copy import deepcopy
from scipy.linalg import inv

from pulse.preprocessing.node import Node
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.mesh import Mesh
from pulse.preprocessing.structural_element import StructuralElement
from pulse.processing.assembly_acoustic import AssemblyAcoustic

class Stress:
    def __init__(self, mesh, frequencies, structural_solution, **kwargs):

        self.mesh = mesh
        self.frequencies = frequencies
        self.structural_solution = structural_solution
        
        zeros = np.zeros([len(self.mesh.nodes.keys()), len(self.frequencies)], dtype=complex)
        self.global_damping = kwargs.get('acoustic_solution', (0,0,0,0) )
        self.acoustic_solution = kwargs.get('acoustic_solution', zeros)
        self.external_pressure = kwargs.get('external_pressure', 0)

    def get(self, damping_flag = False):
        if damping_flag:
            _, betaH, _, betaV = self.global_damping
        else:
            betaH = betaV = 0
        elements = self.mesh.structural_elements.values()
        omega = 2 * pi * self.frequencies.reshape(1,-1)
        damping = np.ones([6,1]) @  (1 + 1j*( betaH + omega * betaV ))
        p0 = self.external_pressure

        for element in elements:
            # Internal Loads
            structural_dofs = np.r_[element.first_node.global_dof, element.last_node.global_dof]
            u = self.structural_solution[structural_dofs, :]
            Dab = element._Dab
            Bab = element._Bab

            Dts = element._Dts
            Bts = element._Bts

            rot = element._rot
            T = element.cross_section.principal_axis_translation
            
            normal = Dab @ Bab @ T @ rot @ u
            shear = Dts @ Bts @ T @ rot @ u

            element.internal_load = np.multiply(np.r_[normal, shear],damping)
            # Stress
            do = element.cross_section.external_diameter
            di = element.cross_section.internal_diameter
            ro = do/2
            area = element.cross_section.area
            Iy = element.cross_section.second_moment_area_y
            Iz = element.cross_section.second_moment_area_z
            J = element.cross_section.polar_moment_area

            acoustic_dofs = np.r_[element.first_node.global_index, element.last_node.global_index]
            
            p = self.acoustic_solution[acoustic_dofs, :]
            pm = np.sum(p,axis=0)/2
            hoop_stress = (2*pm*di**2 - p0*(do**2 + di**2))/(do**2 - di**2)

            element.stress = np.c_[element.internal_load[0]/area,
                                   element.internal_load[2] * ro/Iy,
                                   element.internal_load[1] * ro/Iz,
                                   hoop_stress,
                                   element.internal_load[3] * ro/J,
                                   element.internal_load[4]/area,
                                   element.internal_load[5]/area].T
