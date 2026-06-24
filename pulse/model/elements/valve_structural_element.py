
import numpy as np

from pulse.model.cross_section import CrossSection
from pulse.model.node import DOF_PER_NODE_STRUCTURAL, Node
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.structural_element import StructuralElement, DOF_PER_ELEMENT



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

        self.first_node = first_node
        self.last_node = last_node
        self.index = index

        self.element_type = "valve"
        self.wall_formulation: str = kwargs.get('wall_formulation', 'thin_wall')

        self.material: Material | None  = kwargs.get('material')
        self.cross_section: CrossSection | None  = kwargs.get('cross_section')
        self.loaded_forces: np.ndarray = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))

        self.fluid: Fluid | None = kwargs.get('fluid')
        self.adding_mass_effect: bool = kwargs.get('adding_mass_effect', False)

        self.capped_end: bool = kwargs.get('capped_end', True)
        self.stress_intensification: bool = kwargs.get('stress_intensification', True)
        self.turned_off: bool = kwargs.get("turned_off", False)

        self.valve_data: dict = dict()

        self.section_parameters_render = None

        self._initialize()

        self.reset_valve_data()

    def _initialize(self):

        # self.section_rotation_xyz_undeformed = None
        self.deformed_rotation_xyz = None
        self.deformed_length = None
        self.beam_xaxis_rotation = 0
        
        self.internal_pressure = 0
        self.external_pressure = 0

        self._Dab = None
        self._Bab = None
        self._Dts = None
        self._Bts = None

        self.transf_mat = None
        self.mean_rotation_results = None
        self.rotation_matrix_results_at_lcs = None

        self.transf_matrix_offset_shear_left = None
        self.transf_matrix_offset_shear_right = None
        self.results_at_global_coordinate_system = None

        self.stress = None
        self.internal_load = None
        self.static_analysis_evaluated = False
        self.perforated_plate = None

        self.variable_section = False
        self.force_offset = True


    def reset_valve_data(self):
        self.valve_length = 0
        self.valve_stiffening_factor = 10
        self.valve_mass = 0


    def set_valve_data(self, data):
        if not isinstance(data, dict):
            return

        self.valve_data = data
        self.valve_length = data.get("valve_length")
        self.valve_stiffening_factor = data.get("stiffening_factor")
        self.valve_mass = data.get("valve_mass")


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
        return self.valve_stiffening_factor * self.stiffness_matrix_pipes() 


    def mass_matrix_valve(self):
        L_e = self.valve_length / self.length
        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        M1 = M2 = M3 = self.valve_mass / (2 * L_e)
        indexes = np.array([0,1,2,6,7,8], dtype=int)

        M_matrix[indexes,indexes] = [M1, M2, M3, M1, M2, M3]
        return M_matrix