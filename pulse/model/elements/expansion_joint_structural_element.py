
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



def symmetrize(a):
    """ This function receives matrix and makes it symmetric.

    Parameters
    ----------
    array
        Matrix.

    Returns
    -------
    array
        Symmetric matrix.    
    """
    return a + a.T - np.diag(a.diagonal())

class ExpansionJointStructuralElement(StructuralElement):
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

        self.element_type = "expansion_joint"

        self.fluid: Fluid | None = kwargs.get('fluid')
        self.material: Material | None = kwargs.get('material')
        self.cross_section: CrossSection | None = kwargs.get('cross_section')
        self.loaded_forces: np.ndarray = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))

        self.adding_mass_effect: bool = kwargs.get('adding_mass_effect', False)

        self.section_parameters_render = None

        self._initialize()


    def _initialize(self):

        self.deformed_length = None
        self.beam_xaxis_rotation = 0
        
        self.transf_mat = None
        self.mean_rotation_results = None
        self.rotation_matrix_results_at_lcs = None

        self.transf_matrix_offset_shear_left = None
        self.transf_matrix_offset_shear_right = None
        self.results_at_global_coordinate_system = None

        self.stress = None
        self.internal_load = None
        self.static_analysis_evaluated = False

        self.force_offset = True

        self.expansion_joint_data = dict()
        self.joint_effective_diameter = 0
        self.joint_axial_locking_criteria = 0
        self.joint_rods_included = False
        self.joint_stiffness_table_names = list()


    def set_expansion_joint_data(self, data):
        if not isinstance(data, dict):
            return

        self.expansion_joint_data = data
        self.joint_effective_diameter = data.get("effective_diameter")
        self.joint_rods_included = data.get("rods", False)
        self.joint_axial_locking_criteria = data.get("axial_locking_criteria", 0)


    def matrices_gcs(self, frequencies: np.ndarray | None = None):
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

        stiffness = Rt @ self.stiffness_matrix_expansion_joint_harmonic(frequencies=frequencies) @ R
        mass = Rt @ self.mass_matrix_expansion_joint() @ R
         
        return stiffness, mass


    def stiffness_matrix_gcs(self, frequencies: np.ndarray | None = None):
        """
        This method returns the element stiffness matrix according to the 3D Timoshenko beam theory 
        in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.

        See also
        --------
        matrices_gcs : Element stiffness and mass matrices in the global coordinate system.
        
        mass_matrix_gcs : Element mass matrix in the global coordinate system.

        stiffness_matrix_pipes : Pipe element stiffness matrix in the local coordinate system.

        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        return Rt @ self.stiffness_matrix_expansion_joint_harmonic(frequencies=frequencies) @ R
            

    def mass_matrix_gcs(self):
        """
        This method returns the element mass matrix according to the 3D Timoshenko beam theory 
        in the global coordinate system.

        Returns
        -------
        mass : array
            Element mass matrix in the global coordinate system.

        See also
        --------
        matrices_gcs : Element stiffness and mass matrices in the global coordinate system.

        stiffness_matrix_gcs : Element stiffness matrix in the global coordinate system.
        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        return Rt @ self.mass_matrix_expansion_joint() @ R  


    def stiffness_matrix_expansion_joint_harmonic(self, frequencies: np.ndarray | None = None):

        joint_length  = self.expansion_joint_data.get("joint_length")

        L_e = joint_length / self.length
        n_freq = 1 if frequencies is None else frequencies.size

        kx, kyz, krx, kryz = self.expansion_joint_data.get("values")
        K_matrix = np.zeros((n_freq, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=complex)

        K1 = kx * L_e
        K2 = K3 = kyz / L_e
        K4 = krx * L_e
        K5 = K6 = kryz / L_e

        K1 = get_array_values(K1, n_freq)
        K2 = get_array_values(K2, n_freq)
        K3 = K2
        K4 = get_array_values(K4, n_freq)
        K5 = get_array_values(K5, n_freq)
        K6 = K5   

        Ks = np.array([K1, K2, K3, K4, K5, K6], dtype=complex).T.reshape(n_freq, DOF_PER_NODE_STRUCTURAL)
        indexes_1 = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)
        indexes_2 = indexes_1 + DOF_PER_NODE_STRUCTURAL

        K_matrix[:,indexes_1,indexes_1] = K_matrix[:,indexes_2,indexes_2] = Ks
        K_matrix[:,indexes_1,indexes_2] = K_matrix[:,indexes_2,indexes_1] = -Ks

        return K_matrix


    def mass_matrix_expansion_joint(self):

        joint_mass = self.expansion_joint_data.get("joint_mass")
        joint_length  = self.expansion_joint_data.get("joint_length")

        L_e = joint_length / self.length
        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        M1 = M2 = M3 = joint_mass / (2 * L_e)
        indexes = np.array([0,1,2,6,7,8], dtype=int)

        M_matrix[indexes,indexes] = [M1, M2, M3, M1, M2, M3]

        return M_matrix


def get_array_values(values: np.ndarray | float, number_frequencies: int):
    if isinstance(values, np.ndarray):
        if number_frequencies == 1:
            return values[0]
        else:
            return values

    return values * np.ones(number_frequencies, dtype = float)