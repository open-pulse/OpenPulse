
from typing import TYPE_CHECKING

import numpy as np

from pulse.model.node import DOF_PER_NODE_STRUCTURAL, Node
from pulse.model.elements.structural_element import StructuralElement

if TYPE_CHECKING:
    from pulse.model.elements.structural_element_attributes import StructuralElementAttributes


NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


class RigidStructuralElement(StructuralElement):
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

        self.element_type = "rigid_element"


    def matrices_gcs(self, element_attributes: "StructuralElementAttributes"):
        """
        This method returns the element stiffness and mass matrices of
        the rigid element.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.
            
        mass : array
            Element mass matrix in the global coordinate system.

        """

        stiffness = self.stiffness_matrix_rigid_element(element_attributes)
        mass = self.mass_matrix_rigid_element()

        return stiffness, mass


    def stiffness_matrix_rigid_element(self, element_attributes: "StructuralElementAttributes"):
        
        material = element_attributes.material
        cross_section = element_attributes.cross_section

        E = material.elasticity_modulus
        Iyy = cross_section.second_moment_area_y
        # Izz = cross_section.second_moment_area_y
        # Iyz = cross_section.second_moment_area_yz

        d = self.length
        k = element_attributes.k_factor

        T = np.array([
            [ 1, 0, 0, 0, 0, -d],
            [ 0, 1, 0, 0, 0, 0 ],
            [ 0, 0, 1, 0, 0, 0 ],
            [-d, 0, 0, 1, 0, 0 ],
            [ 0, 0, 0, 0, 1, 0 ],
            [ 0, 0, 0, 0, 0, 1 ]
            ], dtype = float)

        stiffness = ((E * Iyy) / (k - 1)) * np.block([
            [T * k, T * k],
            [T * k, T * k]
            ], dtype=float)

        return stiffness


    def mass_matrix_rigid_element(self):
        return 0.