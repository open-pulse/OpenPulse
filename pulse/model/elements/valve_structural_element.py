
from typing import TYPE_CHECKING

import numpy as np

from pulse.model.node import Node
from pulse.model.structural_element import DOF_PER_ELEMENT, StructuralElement

if TYPE_CHECKING:
    from pulse.model.elements.structural_element_attributes import StructuralElementAttributes


class ValveStructuralElement(StructuralElement):
    """A structural element.
    This class creates a structural element from input data.

    Parameters
    ----------
    first_node : Node object
        Fist node of element.

    last_node : Node object
        Last node of element.

    index : int
        Element index.

    element_type : str, ['pipe_1', 'beam_1', 'expansion_joint', 'valve'], optional
        Element type
        Default is 'pipe_1'.

    material : Material object, optional
        Element structural material.
        Default is 'None'.

    fluid : Fluid object, optional
        Element acoustic fluid.
        Default is 'None'.

    cross_section : CrossSection object, optional
        Element cross section.
        Default is 'None'.

    loaded_forces : array, optional
        Structural forces and moments on the nodes.
        Default is zeros(12).
    """
    def __init__(self, first_node: Node, last_node: Node, index: int, **kwargs):
        super().__init__(first_node, last_node, index, **kwargs)

        self.element_type = "valve"


    def matrices_gcs(self, element_attributes: "StructuralElementAttributes"):
        """
        This method returns the element stiffness and mass matrices according to the 
        3D Timoshenko beam theory in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.
            
        mass : array
            Element mass matrix in the global coordinate system.

        See also
        --------
        stiffness_matrix_gcs : Element stiffness matrix in the global coordinate system.
        
        mass_matrix_gcs : Element mass matrix in the global coordinate system.
        """

        self.element_attributes = element_attributes

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        stiffness = Rt @ self.stiffness_matrix_valve(element_attributes) @ R
        mass = Rt @ self.mass_matrix_valve(element_attributes) @ R

        return stiffness, mass


    def stiffness_matrix_valve(self, element_attributes: "StructuralElementAttributes"):
        k_stiff = element_attributes.valve_data.valve_stiffening_factor
        return k_stiff * self.stiffness_matrix_pipes(element_attributes) 


    def mass_matrix_valve(self, element_attributes: "StructuralElementAttributes"):

        valve_data = element_attributes.valve_data
        L_e = valve_data.valve_length / self.length

        indexes = np.array([0, 1, 2, 6, 7, 8], dtype=int)
        M1 = M2 = M3 = valve_data.valve_mass / (2 * L_e)

        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        M_matrix[indexes, indexes] = [M1, M2, M3, M1, M2, M3]

        return M_matrix