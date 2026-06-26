
# from dataclasses import dataclass, field
from typing import Literal
import numpy as np

from pulse.model.node import Node
from pulse.model.cross_section import CrossSection
from pulse.model.data_classes.data_classes import ExpansionJointData, PerforatedPlateData, ValveData
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.elements.structural_element import DOF_PER_ELEMENT, DOF_PER_NODE_STRUCTURAL
from pulse.utils.rotations import rotation_matrix_3x3_by_deltas

decoupling_matrix_default = np.ones((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=int)


# @dataclass
class ElementAttributes:
    def __init__(self, index: int, first_node: Node, last_node: Node):

        self.index = index
        self.first_node = first_node
        self.last_node = last_node

        self.reset_common_attributes()
        self.reset_structural_element_attributes()
        self.reset_acoustic_element_attributes()

        self.reset_render_related_attributes()

    def reset_common_attributes(self):
        self.fluid: Fluid | None = None
        self.material: Material | None = None
        self.cross_section: CrossSection | None = None

    def reset_structural_element_attributes(self):

        self.structural_element_type: Literal["pipe_1", "beam_1", "expansion_joint", "valve", "rigid_element"] = "pipe_1"

        # pipe-related attributes
        self.wall_formulation: str = "thin_wall"
        self.capped_end: bool = True
        self.turned_off: bool = False
        self.adding_mass_effect: bool = False
        self.force_offset: bool = False

        self.decoupling_matrix: np.ndarray = decoupling_matrix_default
        self.decoupling_info: list | None = None

        # this attribute controls the element rotation about its own axis
        self.xaxis_rotation_angle: float = 0

        # valve data
        self.valve_data: None | ValveData = None

        # expansion joint data
        self.expansion_joint_data: None | ExpansionJointData = None

        # perforated plate data
        self.perforated_plate_data: None | PerforatedPlateData = None

        # rigid element
        self.k_factor: float | None = None

        # stress stiffening attributes
        self.internal_pressure: float = 0
        self.external_pressure: float = 0
        self.static_analysis_evaluated: bool = False

        # internal loads
        self.loaded_forces = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

        self.transf_mat = None


    def reset_acoustic_element_attributes(self):

        self.acoustic_element_type: Literal["undamped"] = "undamped"
        self.proportional_damping: str | None = 0
        self.volumetric_flow_rate: float = 0
        self.length_correction_data: str | None = None

        self.pp_impedance = None

        self.flag_plane_wave: bool = False
        self.flag_wide_duct: bool = False
        self.flag_lrf_fluid_eq: bool = False
        self.flag_lrf_full: bool = False
        self.flag_unflanged_radiation_impedance: bool = False

        self.max_valid_freq: np.ndarray = np.inf
        self.min_valid_freq: float = 0
        self.delta_pressure: float = 0

        self.acoustic_link_diameters = list()


    def reset_render_related_attributes(self):
    
        self.undeformed_rotation_rx: None | np.ndarray = None
        self.undeformed_rotation_ry: None | np.ndarray = None
        self.undeformed_rotation_rz: None | np.ndarray = None

        self.section_parameters_render: list | None = list()


    def update_delta_pressure(self, delta_pressure):
        self.delta_pressure = delta_pressure


    @property
    def is_section_variable(self):
        if isinstance(self.cross_section, CrossSection):
            return self.cross_section.section_info.section_type_label == "reducer"

        return False

    @property
    def length(self) -> float:
        """
        This method returns the element length.

        Returns
        -------
        float
            Element length.
        """
        return np.linalg.norm(self.last_node.coordinates - self.first_node.coordinates)


    @ property
    def delta_x(self) -> np.ndarray:
        return self.last_node.x - self.first_node.x


    @ property
    def delta_y(self) -> np.ndarray:
        return self.last_node.y - self.first_node.y


    @ property
    def delta_z(self) -> np.ndarray:
        return self.last_node.z - self.first_node.z


    @ property
    def center_coordinates(self) -> np.ndarray:
        return np.array([(self.last_node.x + self.first_node.x) / 2, 
                         (self.last_node.y + self.first_node.y) / 2,
                         (self.last_node.z + self.first_node.z) / 2 ], dtype=float)

    @property
    def directional_vector(self):
        return np.array([self.delta_x, self.delta_y, self.delta_z], dtype=float)

    @property
    def normalized_directional_vector(self):
        v = np.array([self.delta_x, self.delta_y, self.delta_z], dtype=float)
        return v / np.linalg.norm(v)

    @ property
    def element_rotation_matrix(self) -> np.ndarray:
        """
        This method returns the transformation matrix that perform a rotation from the element's local coordinate system to the global coordinate system.

        Returns
        -------
        array
            Rotation matrix
        """
        R = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        if self.transf_mat is None:
            self.transf_mat = self.compute_transf_submatrix()
            # print(f"The transf_mat from element {self.index} has been updated.")

        R[0:3, 0:3] = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = self.transf_mat
        return R

    @property
    def element_rotation_matrix_inverse(self) -> np.ndarray:
        return self.element_rotation_matrix.T

    def compute_transf_submatrix(self) -> np.ndarray:
        return rotation_matrix_3x3_by_deltas(self.delta_x, self.delta_y, self.delta_z, self.xaxis_rotation_angle)

    def element_results_gcs(self) -> np.ndarray:
        values = np.zeros(DOF_PER_ELEMENT, dtype=float)
        values[:DOF_PER_NODE_STRUCTURAL] = self.first_node.nodal_solution_gcs
        values[DOF_PER_NODE_STRUCTURAL:] = self.last_node.nodal_solution_gcs
        return values

    def element_results_lcs(self):
        return self.element_rotation_matrix @ self.element_results_gcs()

    def mean_rotations_at_local_coordinate_system(self) -> np.ndarray:
        results_lcs = self.element_results_lcs()
        theta_x = (results_lcs[3] + results_lcs[-3]) / 2
        theta_y = (results_lcs[4] + results_lcs[-2]) / 2
        theta_z = (results_lcs[5] + results_lcs[-1]) / 2
        return np.array([theta_x, theta_y, theta_z], dtype=float)

    def rotations_at_local_coordinate_system_decoupled(self) -> np.ndarray:

        results_lcs = self.element_results_lcs()
        [_, node_id, _, decoupled_rotations] = self.decoupling_info

        avg_rotation = np.zeros(3, dtype=float)

        for j, value in enumerate(decoupled_rotations):
            if value:
                if node_id == self.last_node.external_i:
                    theta = results_lcs[3 + j]
                else:
                    theta = results_lcs[-3 + j]
            else:
                theta = (results_lcs[3 + j] + results_lcs[-3 + j]) / 2

            avg_rotation[j] = theta

        # print(f"Rotations (first node #{self.first_node.external_index}): {np.array([results_lcs[:3]], dtype=float)}")
        # print(f"Rotations (last node #{self.last_node.external_index}): {np.array([results_lcs[-3:]], dtype=float)}")

        return avg_rotation

    def section_normal_vectors_at_lcs(self) -> np.ndarray:
        theta_x, theta_y, theta_z = self.mean_rotations_at_local_coordinate_system()
        L_ = np.sqrt(1-(np.sin(theta_y)**2))
        L = 1
        dx = L_*np.cos(theta_z)
        dy = L_*np.sin(theta_z)
        dz = -L*np.sin(theta_y)
        uvw = np.array([dx, dy*np.cos(theta_x) - dz*np.sin(theta_x), dy*np.sin(theta_x) + dz*np.cos(theta_x)], dtype=float)   
        return uvw
    
    # used for render

    @property
    def deformed_rotation_rxyz(self):
        return [self.deformed_rotation_rx, self.deformed_rotation_ry, self.deformed_rotation_rz]


    @property
    def undeformed_rotation_rxyz(self):
        return [self.undeformed_rotation_rx, self.undeformed_rotation_ry, self.undeformed_rotation_rz]


    def set_deformed_rotations(self, rot_x: float, rot_y: float, rot_z: float):
        self.deformed_rotation_rx = rot_x
        self.deformed_rotation_ry = rot_y
        self.deformed_rotation_rz = rot_z