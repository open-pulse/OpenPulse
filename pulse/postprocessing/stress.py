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
        self.acoustic_solution = kwargs.get('acoustic_solution', deepcopy(zeros))
        self.external_pressure = kwargs.get('external_pressure', 0)

        self.internal_load_axial = deepcopy(zeros)
        self.internal_load_bending_y = deepcopy(zeros)
        self.internal_load_bending_z = deepcopy(zeros)

        self.internal_load_torsion = deepcopy(zeros)
        self.internal_load_transversal_xy = deepcopy(zeros)
        self.internal_load_transversal_xz = deepcopy(zeros)

        self.normal_axial = deepcopy(zeros)
        self.normal_bending_y = deepcopy(zeros)
        self.normal_bending_z = deepcopy(zeros)

        self.shear_torsion = deepcopy(zeros)
        self.shear_transversal_xy = deepcopy(zeros)
        self.shear_transversal_xz = deepcopy(zeros)

    def get(self):

        elements = self.mesh.structural_elements.values()

        for element in elements:
            ro = element.cross_section.external_diameter/2
            area = element.cross_section.area
            Iy = element.cross_section.second_moment_area_y
            Iz = element.cross_section.second_moment_area_z
            J = element.cross_section.polar_moment_area

            structural_dofs = np.r_[element.first_node.global_dof, element.last_node.global_dof]
            first_global_index = element.first_node.global_index

            u = self.structural_solution[structural_dofs, :]
            
            Dab = element._Dab
            Bab = element._Bab

            Dts = element._Dts
            Bts = element._Bts

            rot = element._rot
            T = element.cross_section.principal_axis_translation
            
            normal = Dab @ Bab @ T @ rot @ u
            shear = Dts @ Bts @ T @ rot @ u

            self.internal_load_axial[first_global_index] = normal[0]
            self.internal_load_bending_y[first_global_index] = normal[1]
            self.internal_load_bending_z[first_global_index] = normal[2]

            self.internal_load_torsion[first_global_index] = shear[0]
            self.internal_load_transversal_xz[first_global_index] = shear[1]
            self.internal_load_transversal_xy[first_global_index] = shear[2]

            self.normal_axial[first_global_index] = normal[0] / area
            self.normal_bending_y[first_global_index] = normal[1] * ro / Iy
            self.normal_bending_z[first_global_index] = normal[2] * ro / Iz

            self.shear_torsion[first_global_index] = shear[0] * ro / J
            self.shear_transversal_xz[first_global_index] = shear[1] / area
            self.shear_transversal_xy[first_global_index] = shear[2] / area