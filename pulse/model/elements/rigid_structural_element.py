
import numpy as np

from pulse.model.cross_section import CrossSection
from pulse.model.node import DOF_PER_NODE_STRUCTURAL, Node
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.structural_element import StructuralElement

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

decoupling_matrix = np.ones((DOF_PER_ELEMENT,DOF_PER_ELEMENT), dtype=int)
zeros_3x3 = np.zeros((3,3), dtype=float)


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

        self.first_node = first_node
        self.last_node = last_node
        self.index = index

        self.element_type = "rigid_element"

        self.material: Material | None = kwargs.get('material')
        self.cross_section: CrossSection | None  = kwargs.get('cross_section')
        self.fluid: Fluid | None  = kwargs.get('fluid')

        self.k_factor: float = kwargs.get("k_factor", 1.0)

        self.section_parameters_render = None

        self._initialize()


    def _initialize(self):

        self.deformed_rotation_xyz = None
        self.deformed_length = None
        self.beam_xaxis_rotation = 0
        
        self.transf_mat = None
        self.mean_rotation_results = None
        self.rotation_matrix_results_at_lcs = None


    def matrices_gcs(self, material: Material):
        """
        This method returns the element stiffness and mass matrices of
        the rigid element.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.
            
        mass : array
            Element mass matrix in the global coordinate system.

        See also
        --------
        stiffness_matrix_rigid_element : Element stiffness matrix in the global coordinate system.
        
        mass_matrix_rigid_element : Element mass matrix in the global coordinate system.
        """

        stiffness = self.stiffness_matrix_rigid_element()
        mass = self.mass_matrix_rigid_element()
         
        return stiffness, mass


    def stiffness_matrix_rigid_element(self):
        
        d = self.length
        k = self.k_factor
        
        T = np.array([
            [ 1, 0, 0, 0, 0, -d],
            [ 0, 1, 0, 0, 0, 0 ],
            [ 0, 0, 1, 0, 0, 0 ],
            [-d, 0, 0, 1, 0, 0 ],
            [ 0, 0, 0, 0, 1, 0 ],
            [ 0, 0, 0, 0, 0, 1 ]],
        dtype = float)

        stiffness = np.block([
            [T * k, T * k],
            [T * k, T * k]
            ], dtype=float)

        return stiffness


    def mass_matrix_rigid_element(self):
        return 0.