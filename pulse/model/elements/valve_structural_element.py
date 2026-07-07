
from typing import TYPE_CHECKING

import numpy as np

from pulse.model.elements.structural_element import DOF_PER_ELEMENT, StructuralElement
from pulse.model.elements.pipe_structural_element import PipeStructuralElement

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


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
    def __init__(self, element_attributes: "ElementAttributes", **kwargs):
        super().__init__(element_attributes, **kwargs)

        self.valve_data = element_attributes.valve_data


    def matrices_gcs(self):
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

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        stiffness = Rt @ self.stiffness_matrix_valve() @ R
        mass = Rt @ self.mass_matrix_valve() @ R

        return stiffness, mass


    def stiffness_matrix_valve(self):
        """
        This method returns the valve stiffness elementary matrix in local coordinates system
        computed as the pipe stiffness and amplified by the valve stiffness factor.
        """
        Ke_pipe = PipeStructuralElement(self.element_attributes).stiffness_matrix_pipes()
        k_stiff = self.valve_data.valve_stiffening_factor
        return k_stiff * Ke_pipe


    def mass_matrix_valve(self):
        """
        This method returns the valve mass elementary matrix in local coordinates system.
        """
        L_e = self.valve_data.valve_length / self.element_attributes.length

        indexes = np.array([0, 1, 2, 6, 7, 8], dtype=int)
        M1 = M2 = M3 = self.valve_data.valve_mass / (2 * L_e)

        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        M_matrix[indexes, indexes] = [M1, M2, M3, M1, M2, M3]

        return M_matrix