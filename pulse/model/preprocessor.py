
from typing import TYPE_CHECKING

from pulse.interface.user_input.model.setup.structural.expansion_joint_input import get_cross_sections_to_plot_expansion_joint
from pulse.interface.user_input.model.setup.structural.valves_input import get_V_linear_distribution
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_pressure_unit
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.cross_sections.valve_cross_section import ValveCrossSection
from pulse.model.data_classes.model_setup_data_classes import AcousticLinkData, ExpansionJointData, ValveData
from pulse.model.data_classes.perforated_plate_data_class import PerforatedPlateData
from pulse.model.data_classes.project_setup_data_classes import ImportType
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.elements.structural_element import NODES_PER_ELEMENT
from pulse.model.node import DOF_PER_NODE_ACOUSTIC, DOF_PER_NODE_STRUCTURAL, Node, NodePosition
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.reciprocating_compressor_model import ReciprocatingCompressorModel
from pulse.utils.common_utils import get_linear_distribution_for_variable_section, slicer
from pulse.utils.rotations import rotation_matrix_3x3_by_angles, rotation_matrix_3x3_by_deltas

if TYPE_CHECKING:
    from pulse.model.mesh import Mesh

import logging
from collections import defaultdict
from time import perf_counter

import numpy as np
from scipy.spatial.transform import Rotation


class Preprocessor:
    """A preprocessor class.
    This class creates a acoustic and structural preprocessor object.
    """
    def __init__(self, mesh: 'Mesh'):

        self.mesh = mesh
        self.reset_variables()

    def reset_variables(self):
        """
        This method reset the class default values.
        """

        self.nodes: dict[int, Node] = dict()

        self.elements_attributes: dict[int, ElementAttributes] = dict()
        self.elements_deltas: np.ndarray | None = None

        self.neighbors_nodes: dict[int, list[int]] = defaultdict(list)
        self.elements_connected_to_node: defaultdict[int, list[int]] = defaultdict(list)

        self.mesh.reset_variables()

        self.deformed_coordinates: None | np.ndarray = None
        self.deformed_section_rotations = None
        self.undeformed_section_rotations = None
        self.rotation_matrix_gcs_to_lcs = None

        self.stress_stiffening_enabled = False

        self.structure_principal_diagonal = None

        self.pipe_gdofs = None
        self.unprescribed_pipe_indexes = None
        self.stop_processing = False

    @property
    def number_acoustic_elements(self):
        return len(self.elements_attributes)

    @property
    def number_structural_elements(self):
        return len(self.elements_attributes)

    def generate(self, import_type: ImportType, geometry_path: str = ""):
        """
        It loads geometry file or data and process the mesh.            
        """

        t0 = perf_counter()

        self.reset_variables()
        self.mesh.generate(import_type, geometry_path = geometry_path)

        self.create_nodes()
        self.create_elements_attributes()

        self.map_neighbors_nodes()
        self.compute_structure_bounding_box_diagonal()

        dt = perf_counter() - t0
        print(f"Time to process the generate method of the Preprocessor class: {dt} s")

    def create_nodes(self):
        """
        This method generate the mesh nodes.

        Parameters
        ----------
        indexes : List
            Nodes global indexes.
            
        coords : array
            Nodes coordinates.
            
        map_nodes : dict
            Dictionary maps global indexes to external indexes.
        """
        self.nodes.clear()
        for node_id, x, y, z in self.mesh.nodal_coordinates:
            self.nodes[int(node_id)] = Node(int(node_id), x, y, z)

    def create_elements_attributes(self):
        """
        This method generate the mesh structural elements.

        Parameters
        ----------
        indexes : List
            Nodes global indexes.
            
        connectivities : array
            Connectivity matrix that relates the elements and its nodes.
            
        map_nodes : dict
            Dictionary maps global indexes to external indexes.
            
        map_elements : dict
            Dictionary maps global element indexes.
        """
        self.elements_attributes.clear()

        # print()
        for element_index, _, _, _, *connect in self.mesh.lines_connectivity:
            first_node = self.nodes.get(connect[0])
            last_node  = self.nodes.get(connect[1])
            # first_node = Node(connect[0], *self.mesh.get_node_coordinates(connect[0]))
            # last_node = Node(connect[1], *self.mesh.get_node_coordinates(connect[1]))

            # print(first_node.index - first_node_A.index, first_node.coordinates - first_node_A.coordinates)
            # print(last_node.index - last_node_A.index, last_node.coordinates - last_node_A.coordinates)

            self.elements_attributes[element_index] = ElementAttributes(element_index, first_node, last_node)

        self.update_number_divisions()

    def get_element_material(self, element_id: int) -> Material | None:
        element_attributes = self.elements_attributes.get(element_id)
        return None if element_attributes is None else element_attributes.material

    def get_element_fluid(self, element_id: int) -> Fluid | None:
        element_attributes = self.elements_attributes.get(element_id)
        return None if element_attributes is None else element_attributes.fluid

    def get_element_cross_section(self, element_id: int) -> CrossSection | None:
        element_attributes = self.elements_attributes.get(element_id)
        return None if element_attributes is None else element_attributes.cross_section

    def get_structural_element_type(self, element_id: int) -> str | None:
        element_attributes = self.elements_attributes.get(element_id)
        return None if element_attributes is None else element_attributes.structural_element_type

    def get_acoustic_element_type(self, element_id: int) -> str | None:
        element_attributes = self.elements_attributes.get(element_id)
        return None if element_attributes is None else element_attributes.acoustic_element_type

    def get_model_statistics(self):
        return len(self.nodes), self.number_acoustic_elements, self.number_structural_elements

    def get_line_length(self, line_id: int) -> tuple[float, list[Node]]:
        """
        This method returns the length of a given line ID.

        Parameters
        ----------
        line_id : int
        
        """
        first_element_ID = self.mesh.elements_from_line[line_id][0]
        last_element_ID = self.mesh.elements_from_line[line_id][-1]

        element_attributes_first = self.elements_attributes.get(first_element_ID)
        element_attributes_last = self.elements_attributes.get(last_element_ID)

        list_nodes = [
            element_attributes_first.first_node,
            element_attributes_first.last_node,
            element_attributes_last.first_node,
            element_attributes_last.last_node,
        ]

        length = 0
        for index in range(1, len(list_nodes)):
            length_i = np.linalg.norm(list_nodes[0].coordinates - list_nodes[index].coordinates)
            if length_i > length:
                length = length_i
                _node = list_nodes[index]

        edge_nodes = [list_nodes[0], _node]

        return length, edge_nodes

    def get_lines_vertex_coordinates(self, _array: bool = True):
        """
        This method returns a dictionary containing line IDs as keys and its vertex node coordinates as values.
        """
        line_to_vertex_coords = defaultdict(list)
        if self.mesh.nodes_from_line:
            for line_id in self.mesh.lines_from_model:
                _, vertex_nodes = self.get_line_length(line_id)
                for vertex_node in vertex_nodes:
                    if _array:
                        line_to_vertex_coords[line_id].append(vertex_node.coordinates)
                    else:
                        line_to_vertex_coords[line_id].append(list(vertex_node.coordinates))

        return line_to_vertex_coords

    def map_neighbors_nodes(self):
        """
        This method updates the structural elements neighbors dictionary. The dictionary's keys and values are nodes objects.
        """
        self.neighbors_nodes.clear()
        self.elements_connected_to_node.clear()

        for index, element_attributes in self.elements_attributes.items():
            first_node_index = element_attributes.first_node.index
            last_node_index = element_attributes.last_node.index

            self.neighbors_nodes[first_node_index].append(last_node_index)
            self.neighbors_nodes[last_node_index].append(first_node_index)

            self.elements_connected_to_node[first_node_index].append(index)
            self.elements_connected_to_node[last_node_index].append(index)

    def update_number_divisions(self):
        """
        This method updates the number of divisions of pipe and circular beam cross-sections based on model size. This adds some
        compensation for the computational effort spent to render vtk actors in models with millions of degrees of freedom.
        """
        number_elements = self.number_structural_elements
        if number_elements <= 1e3:
            self.section_number_of_divisions = 36 
        if number_elements <= 5e3:
            self.section_number_of_divisions = 24        
        elif number_elements <= 1e4:
            self.section_number_of_divisions = 16
        elif number_elements <= 5e4:
            self.section_number_of_divisions = 10
        elif number_elements <= 2e4:
            self.section_number_of_divisions = 8
        else:
            self.section_number_of_divisions = 6

    def neighbor_elements_diameter(self):
        """
        This method maps the elements outer diameters that each node belongs to. The maping is done 
        according to the node external index.

        Returns
        ----------
        dict
            Outer diameters at a certain node. Giving a node external index, returns a list of diameters.
        """
        neighbor_diameters = defaultdict(list)

        for index, element_attributes in self.elements_attributes.items():
            first_node = element_attributes.first_node
            last_node = element_attributes.last_node

            cross_section = self.get_element_cross_section(index)
            outer_diameter = cross_section.outer_diameter
            inner_diameter = cross_section.inner_diameter

            neighbor_diameters[first_node.index].append((index, outer_diameter, inner_diameter))
            neighbor_diameters[last_node.index].append((index, outer_diameter, inner_diameter))

        return neighbor_diameters

    def neighbor_elements_diameter_global(self):
        """
        This method maps the elements inner diameters that each node belongs to. The maping is done according to the node global index.

        Returns
        ----------
        Dict
            Inner diameters at a certain node. Giving a node global index, returns a list of diameters.
        """

        neighbor_diameters = defaultdict(list)
        for index, element_attributes in self.elements_attributes.items():

            #TODO: remove as soon as possible
            if element_attributes.structural_element_type == "ridig_element":
                continue

            cross_section = element_attributes.cross_section
            if cross_section is None:
                continue

            first = element_attributes.first_node.index
            last = element_attributes.last_node.index
            outer_diameter = cross_section.outer_diameter
            inner_diameter = cross_section.inner_diameter

            neighbor_diameters[first].append((index, outer_diameter, inner_diameter))
            neighbor_diameters[last].append((index, outer_diameter, inner_diameter))

        return neighbor_diameters

    def check_disconnected_lines(self, tolerance=1e-6):
        """
        This methods shearchs for disconnected lines inside sphere of radius r < (size/2) + tolerance.
        """
        element_size = self.mesh.element_size
        if not isinstance(self.mesh.nodal_coordinates, np.ndarray):
            return

        disconnected_nodes = list()
        for node_id, neigh_nodes in self.neighbors_nodes.items():
            if len(neigh_nodes) != 1:
                continue

            nodal_coords = self.mesh.nodal_coordinates
            diff = np.linalg.norm(nodal_coords[:, 1:] - nodal_coords[node_id, 1:], axis=1)
            mask = diff < (element_size / 2) + tolerance

            if not np.any(mask):
                continue

            try:
                external_indexes = nodal_coords[:, 0][mask]
                if len(external_indexes) != 1:
                    continue

                for external_index in external_indexes:
                    if external_indexes == node_id:
                        continue

                    if len(self.neighbors_nodes[external_index]) == 1:
                        disconnected_nodes.append(int(external_index))

            except Exception as _log_error:
                title = "Error while checking mesh at the line edges"
                message = str(_log_error)
                PrintMessageInput(["error", title, message])

        if disconnected_nodes:
            title = "Problem detected in connectivity between neighbor nodes"
            message = "At least one disconnected node has been detected at the edge of one line due "
            message += "to the mismatch between the geometry 'keypoints' and the current mesh setup. " 
            message += "We strongly recommend reducing the element size or correcting the problem "
            message += "in the geometry file before proceeding with the model setup.\n\n"
            message += f"List of disconnected node(s): \n{disconnected_nodes}"
            PrintMessageInput(["warning", title, message])                
        
    def get_line_from_node_id(self, node_ids: int | list[int]) -> list[int]:

        if isinstance(node_ids, int):
            node_ids = [node_ids]
        
        line_ids = list()
        for node_id in node_ids:
            line_ids.extend(self.mesh.lines_from_node.get(node_id))

        return list(np.unique(line_ids).astype(int))

    def get_node_id_by_coordinates(self, coords: np.ndarray, radius=None):
        """
            This method returns the external node ids inside a influence sphere centered in 'coords' point.

        Parameters:
        ------------

            coordinates : list, np.ndarray or tuple
                represents the nodal coordinates of interest

            radius: float (default None)
                the radius of interest considered. The sphere default radius is equal to element_size / 20.

        Returns:
        --------

            external_index: int
                this value correspond to the 
        
        """

        external_indexes = self.mesh.nodal_coordinates[:, 0]
        list_coordinates = self.mesh.nodal_coordinates[:, 1:].tolist()

        if isinstance(coords, (np.ndarray, tuple)):
            coords = list(coords)

        if radius is None:
            radius = self.mesh.element_size / 20

        if coords in list_coordinates:
            ind = list_coordinates.index(coords)
            external_index = int(external_indexes[ind])

        else:
            diff = np.linalg.norm(self.mesh.nodal_coordinates[:,1:] - np.array(coords), axis=1)
            mask = diff < radius

            if not external_indexes[mask].any():
                return None

            try:
                external_index = int(external_indexes[mask].item())
            except Exception as error_log:
                logging.error(str(error_log))
                return None

        return external_index

    def compute_structure_bounding_box_diagonal(self):
        """
        This method updates the principal structure diagonal parallelepiped attribute. 
        
        """
        xyz_min = np.min(self.mesh.nodal_coordinates[:, 1:], axis=0)
        xyz_max = np.max(self.mesh.nodal_coordinates[:, 1:], axis=0)
        self.structure_principal_diagonal = np.linalg.norm(xyz_max - xyz_min)
        # print('The base length is: {}[m]'.format(round(self.structure_principal_diagonal,6)))

    def get_global_structural_indexes(self):
        """
        This method returns the placement of the rows and columns of the structural global degrees of freedom in the global matrices.

        Returns
        ----------
        row : array.
            Integers that place the rows.
            
        column : array.
            Integers that place the columns.
        """

        rows, cols = self.number_structural_elements, DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
        cols_nodes = self.mesh.lines_connectivity[:, 4:]
        cols_dofs = cols_nodes.reshape(-1, 1) * DOF_PER_NODE_STRUCTURAL + np.arange(6, dtype=int)
        cols_dofs = cols_dofs.reshape(rows, cols)

        ind_j = np.tile(cols_dofs, cols)
        ind_i = cols_dofs.reshape(-1, 1) @ np.ones((1, cols), dtype=int) 

        return ind_i.flatten(), ind_j.flatten()

    def get_global_acoustic_indexes(self):
        """
        This method returns the placement of the rows and columns of the acoustic global degrees of freedom in the global matrices.

        Returns
        ----------
        row : array.
            Integers that place the rows.
            
        column : array.
            Integers that place the columns.
        """

        rows, cols = len(self.elements_attributes), DOF_PER_NODE_ACOUSTIC * NODES_PER_ELEMENT
        cols_nodes = self.mesh.lines_connectivity[:, 4:]
        cols_dofs = cols_nodes.reshape(-1, 1)
        cols_dofs = cols_dofs.reshape(rows, cols)

        ind_j = np.tile(cols_dofs, cols)
        ind_i = cols_dofs.reshape(-1, 1) @ np.ones((1, cols), dtype=int)

        return ind_i.flatten(), ind_j.flatten()

    def set_structural_element_type_by_element(self, elements: list[int], element_type: str):
        """
        This method attributes structural element type to a list of elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        element_type : str, ['pipe_1', 'beam_1', 'expansion_joint', 'valve']
            Structural element type to be attributed to the listed elements.
            
        remove : bool, optional
            True if the element_type have to be removed from the structural element type dictionary. False otherwise.
            Default is False.
        """

        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.structural_element_type = element_type

    def set_structural_element_force_offset_by_elements(self, elements: list[int], force_offset: bool):
        """
        This method assigns a structural element wall formulation to a list of selected elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        force_offset : int, [0, 1]
            Structural element type to be attributed to the listed elements.

        """
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.force_offset = bool(force_offset)

    def set_structural_element_wall_formulation_by_elements(self, elements: list[int], wall_formulation: str):
        """
        This method assigns a structural element wall formulation to a list of selected elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        wall_formulation : str, ['thick_wall', 'thin_wall']
            Structural element type to be attributed to the listed elements.

        """
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.wall_formulation = wall_formulation

    def set_acoustic_element_type_by_element(
        self, elements: list[int], element_type: str, proportional_damping: float | None = None, volumetric_flow_rate: float | None = None
    ):
        """
        This method attributes acoustic element type to a list of elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.

        element_type : str, ['undamped', 'proportional', 'wide_duct', 'LRF_fluid_equivalent', 'LRF_full']
            Acoustic element type to be attributed to the listed elements.

        proportional_damping : float, optional
            Acoustic proportional damping coefficient. It must be attributed to the elements of type 'proportional'.
            Default is None.

        remove : bool, optional
            True if the element_type have to be removed from the acoustic element type dictionary. False otherwise.
            Default is False.
        """
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.acoustic_element_type = element_type
            element_attributes.proportional_damping = proportional_damping
            element_attributes.volumetric_flow_rate = volumetric_flow_rate if element_attributes.structural_element_type != "beam_1" else None

    def set_cross_section_by_elements(
        self,
        elements: list[int],
        cross_section: CrossSection | list[CrossSection],
        update_properties: bool = False,
        sections_mapping: bool = False,
    ):
        """
        This method attributes cross section object to a list of acoustic and structural elements.

        Parameters
        ----------
        elements : list
            Acoustic and structural elements indexes.

        cross_section : Cross section object
            Tube cross section data.

        update_properties : bool, optional
            True if the cross section properties have to be evaluated or updated. False otherwise.
            Default is False.
        """

        if cross_section is None:
            return

        if isinstance(cross_section, CrossSection) and update_properties:
            cross_section.update_properties()

        if isinstance(cross_section, list):
            for i, element in enumerate(elements):

                _cross_section = cross_section[i]
                if not isinstance(_cross_section, CrossSection):
                    continue

                for element_attributes in slicer(self.elements_attributes, [element]):

                    # reset the section parameters for rendering
                    element_attributes.cross_section = _cross_section

                    if not sections_mapping:
                        element_attributes.section_parameters_render = None
                        if _cross_section.section_type_label == "expansion_joint":
                            element_attributes.section_parameters_render = _cross_section.expansion_joint_info._as_list()

                        elif _cross_section.section_type_label == "valve":
                            element_attributes.section_parameters_render = _cross_section.section_parameters

        else:

            for element_attributes in slicer(self.elements_attributes, elements):
                element_attributes.cross_section = cross_section

                if not sections_mapping:
                    # reset the section parameters for rendering
                    element_attributes.section_parameters_render = None

    def set_cross_section_by_lines(self, lines: list[int], cross_section: CrossSection):
        """
        This method attributes cross section object to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        cross_section : Cross section object
            Tube cross section data.
        """
        if isinstance(lines, int):
            lines = [lines]

        for elements in slicer(self.mesh.elements_from_line, lines):
            self.set_cross_section_by_elements(elements, cross_section)

    def set_variable_cross_section_by_line(self, line_ids: int | list, section_data: dict):
        """
        This method sets the variable section info by line selection.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        if not isinstance(section_data, dict):
            return

        section_parameters = section_data.get("section_parameters")
        if section_parameters is None:
            return

        if len(section_parameters) != 10:
            return

        [
            outer_diameter_initial,
            thickness_initial,
            offset_y_initial,
            offset_z_initial,
            outer_diameter_final,
            thickness_final,
            offset_y_final,
            offset_z_final,
            insulation_thickness,
            insulation_density,
        ] = section_parameters

        for line_id in line_ids:
            elements_from_line = self.mesh.elements_from_line[line_id]

            element_attributes_first = self.elements_attributes.get(elements_from_line[0])
            element_attributes_last = self.elements_attributes.get(elements_from_line[-1])

            coord_first_1 = element_attributes_first.first_node.coordinates
            coord_last_1 = element_attributes_last.last_node.coordinates

            coord_first_2 = element_attributes_last.first_node.coordinates
            coord_last_2 = element_attributes_first.last_node.coordinates

            lines_vertex_coords = self.get_lines_vertex_coordinates(_array=False)
            vertex_coords = lines_vertex_coords[line_id]

            N = len(elements_from_line)
            if list(coord_first_1) in vertex_coords and list(coord_last_1) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(
                    outer_diameter_initial, outer_diameter_final, N
                )
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_initial, thickness_final, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_initial, offset_y_final, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_initial, offset_z_final, N)

            elif list(coord_first_2) in vertex_coords and list(coord_last_2) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(
                    outer_diameter_final, outer_diameter_initial, N
                )
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_final, thickness_initial, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_final, offset_y_initial, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_final, offset_z_initial, N)

            cross_sections_first = list()
            # cross_sections_last = list()

            for index, element_id in enumerate(elements_from_line):

                element_attributes = self.elements_attributes[element_id]
                first_node = element_attributes.first_node
                last_node = element_attributes.last_node

                section_parameters_first = [
                    outer_diameter_first[index],
                    thickness_first[index],
                    offset_y_first[index],
                    offset_z_first[index],
                    insulation_thickness,
                    insulation_density,
                    "reducer",
                    ]

                section_parameters_last = [
                    outer_diameter_last[index],
                    thickness_last[index],
                    offset_y_last[index],
                    offset_z_last[index],
                    insulation_thickness,
                    insulation_density,
                    "reducer",
                    ]

                cross_section_first = CrossSection(element_type="pipe_1", pipe_section_info=PipeCrossSection(*section_parameters_first))
                cross_section_last = CrossSection(element_type="pipe_1", pipe_section_info=PipeCrossSection(*section_parameters_last))

                cross_sections_first.append(cross_section_first)
                # cross_sections_last.append(cross_section_last)

                first_node.cross_section = cross_section_first
                last_node.cross_section = cross_section_last

            self.set_cross_section_by_elements(elements_from_line, cross_sections_first)

    def set_cross_sections_to_valve_elements(self, line_id: int, data: dict):

        start_coords = np.array(data["start_coords"], dtype=float)
        end_coords = np.array(data["end_coords"], dtype=float)

        line_elements = self.mesh.elements_from_line[line_id]

        valve_info = data.get("valve_info")
        if not isinstance(valve_info, dict):
            return

        valve_body_elements = list()
        valve_flange_elements = list()

        if "flange_length" in valve_info.keys():

            flange_length = valve_info.get("flange_length")
            d_out_flange, t_flange, offset_y_flange, offset_z_flange, *_ = valve_info.get("flange_section_parameters")

            for element_id in line_elements:
                element_attributes = self.elements_attributes.get(element_id)
                center_coords = element_attributes.center_coordinates

                if np.linalg.norm(center_coords-start_coords) <= flange_length:
                    valve_flange_elements.append(element_id)
                elif np.linalg.norm(center_coords-end_coords) <= flange_length:
                    valve_flange_elements.append(element_id)
                else:
                    valve_body_elements.append(element_id)

        else:

            for element_id in line_elements:
                valve_body_elements.append(element_id)

        body_section_info = ValveCrossSection(*valve_info.get("body_section_parameters", list()))
        body_cross_section = CrossSection(valve_section_info=body_section_info)
        self.set_cross_section_by_elements(valve_body_elements, body_cross_section)

        if "flange_section_parameters" in valve_info.keys():
            flange_section_info = ValveCrossSection(*valve_info.get("flange_section_parameters", list()))
            flange_cross_section = CrossSection(valve_section_info=flange_section_info)
            self.set_cross_section_by_elements(valve_flange_elements, flange_cross_section)

        N = len(valve_body_elements)
        d_out_body, t_body, offset_y_body, offset_z_body, *_ = valve_info.get("body_section_parameters")
        diameters = get_V_linear_distribution(d_out_body, N)

        for i, element_id in enumerate(valve_flange_elements):
            self.elements_attributes.get(element_id).section_parameters_render = [d_out_flange, t_flange, offset_y_flange, offset_z_flange, 0, 0]

        for i, element_id in enumerate(valve_body_elements):
            self.elements_attributes.get(element_id).section_parameters_render = [diameters[i], t_body, offset_y_body, offset_z_body, 0, 0]

    def set_cross_sections_to_expansion_joint(self, line_id: int, expansion_joint_info: dict):

        joint_elements = self.mesh.elements_from_line[line_id]

        if not isinstance(expansion_joint_info, dict):
            return

        cross_sections = get_cross_sections_to_plot_expansion_joint(
            joint_elements,
            expansion_joint_info["effective_diameter"],
            expansion_joint_info["offset_y"],
            expansion_joint_info["offset_z"],
        )

        self.set_cross_section_by_elements(joint_elements, cross_sections)

    def set_structural_element_type_by_lines(self, line_ids: int | list, element_type: str):
        """
        This method attributes structural element type to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        element_type : str, ['pipe_1', 'beam_1', 'expansion_joint', 'valve']
            Structural element type to be attributed to elements.
            
        remove : bool, optional
            True if the element_type have to be removed from the structural element type dictionary. False otherwise.
            Default is False.
        """

        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            self.set_structural_element_type_by_element(elements, element_type)

    def set_acoustic_element_type_by_lines(
        self,
        line_ids: (int | list | tuple),
        element_type: str,
        proportional_damping=None,
        volumetric_flow_rate=None,
    ):
        """
        This method attributes acoustic element type to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        element_type : str, ['undamped', 'proportional', 'wide_duct', 'LRF_fluid_equivalent', 'LRF_full']
            Acoustic element type to be attributed to the listed elements.
            
        proportional_damping : float, optional
            Acoustic proportional damping coefficient. It must be attributed to the elements of type 'proportional'.
            Default is None.

        """

        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            self.set_acoustic_element_type_by_element(  elements, 
                                                        element_type, 
                                                        proportional_damping = proportional_damping, 
                                                        volumetric_flow_rate = volumetric_flow_rate  )

    # Structural physical quantities
    def set_material_by_element(self, elements: list[int], material: Material):
        """
        This method attributes material object to a list of acoustic and structural elements.

        Parameters
        ----------
        elements : list
            Acoustic and structural elements indexes.
            
        material : Material object
            Material data.
        """
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.material = material

    def set_material_by_lines(self, line_ids: (int | list | tuple), material):
        """
        This method attributes material object to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        material : Material object
            Material data.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            self.set_material_by_element(elements, material)

    def set_force_by_element(self, elements, loads):
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.loaded_forces = loads

    def set_B2P_rotation_decoupling(self, element_id: int, data: dict):
        """
        This method .

        Parameters
        ----------
        element_id : list
            Element indexes.

        nodes_id : list
            Nodes external indexes.

        rotations_to_decouple : list of boolean, optional
            ?????
            Default is [False, False, False]

        """

        coords = np.array(data["coords"], dtype=float)
        node_id = self.get_node_id_by_coordinates(coords)
        if node_id is None:
            return

        decoupled_rotations: list = data.get("decoupled_rotations")
        if decoupled_rotations is None:
            return

        element_ids = self.elements_connected_to_node[node_id]
        if len(element_ids) < 3:
            return

        mat_base = np.array([
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            ], dtype=float)

        node = self.nodes[node_id]
        element_attributes = self.elements_attributes.get(element_id)
        local_dofs = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)

        if node in [element_attributes.first_node]:
            node_position = NodePosition.FIRST
            indexes = local_dofs[3:]

        elif node in [element_attributes.last_node]:
            node_position = NodePosition.LAST
            indexes = local_dofs[3:] + DOF_PER_NODE_STRUCTURAL

        else:
            return

        ij = indexes[decoupled_rotations]

        mat_base[ij, :] = 0
        mat_base[:, ij] = 0

        element_attributes = self.elements_attributes.get(element_id)

        element_attributes.decoupling_matrix = mat_base
        element_attributes.decoupling_info = [element_id, node_id, node_position, decoupled_rotations]

    def enable_fluid_mass_adding_effect(self, enable: bool = True):
        """
        This method enables or disables the addition of fluid mass in the structural element mass.

        Parameters
        ----------            
        reset : bool, optional
            True if the fluid mass effect have to be disable. False to enable.
            Default is False.
        """

        for element_attributes in self.elements_attributes.values():
            element_attributes.adding_mass_effect = enable

    def set_capped_end_by_elements(self, elements, value):
        """
        This method enables or disables the capped end effect in a list of acoustic elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        value : bool
            True if the capped end effect have to be activated. False otherwise.

        selection : ?????
            ??????
        """      
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.capped_end = value
 
    def set_capped_end_by_lines(self, line_ids: (int | list | tuple), value: bool):
        """
        This method enables or disables the capped end effect to all acoustic elements that belongs to a line.

        Parameters
        ----------
        line_ids : list
            Lines/entities indexes.
            
        value : bool
            True if the capped end effect have to be activated. False otherwise.
        """

        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            for element_attributes in slicer(self.elements_attributes, elements):
                element_attributes.capped_end = value


    def set_structural_element_wall_formulation_by_lines(self, lines: int | list[int], wall_formulation: str):
        """
        This method assign a strutural element wall formulation to the selected lines.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        wall_formulation : str, ['thick_wall', 'thin_wall']
            Structural element type to be attributed to the listed elements. 
        """
        if isinstance(lines, int):
            lines = [lines]

        for elements in slicer(self.mesh.elements_from_line, lines):
            for element_attributes in slicer(self.elements_attributes, elements):
                element_attributes.wall_formulation = wall_formulation

    def set_structural_element_force_offset_by_lines(self, lines: int | list[int], force_offset: bool):
        """
        This method assign a strutural element force offset to the selected lines.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        force offset : bool
            This argument controls when the structural element force offset will be activated. 
        """
        if isinstance(lines, int):
            lines = [lines]

        for elements in slicer(self.mesh.elements_from_line, lines):
            for element_attributes in slicer(self.elements_attributes, elements):
                element_attributes.force_offset = bool(force_offset)

    def modify_stress_stiffening_effect(self, _bool):
        self.stress_stiffening_enabled = _bool

    def set_stress_stiffening_by_lines(self, lines: int | list, data: dict):
        """
        This method sets the stress stiffening property data to the entered lines.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        data : dict
            The stress stiffening property data.
        """
        if isinstance(lines, int):
            lines = [lines]

        pressure_unit = data.get("pressure_unit", "Pa (a)")
        external_pressure = data.get("external_pressure")
        internal_pressure = data.get("internal_pressure")

        external_pressure_Pa = convert_pressure_unit(external_pressure, pressure_unit, "Pa")
        internal_pressure_Pa = convert_pressure_unit(internal_pressure, pressure_unit, "Pa")

        for elements in slicer(self.mesh.elements_from_line, lines):
            self.set_stress_stiffening_by_elements(elements, external_pressure_Pa, internal_pressure_Pa)

    def set_stress_stiffening_by_elements(self, elements: list[int], external_pressure: float, internal_pressure: float):
        """
        This method sets the stress stiffening internal and external pressures to the elements.

        Parameters
        ----------
        elements : list
            List of elements indexes.

        external_pressure : float
            The internal pressure scaled in Pa units.

        internal_pressure : float
            The internal pressure scaled in Pa units.
        """
        self.modify_stress_stiffening_effect(True)

        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.external_pressure = external_pressure
            element_attributes.internal_pressure = internal_pressure

    def add_expansion_joint_by_lines(self, line_ids: (int | list), data: (None | dict)):
        """
        This method .

        Parameters
        ----------
        line_ids : list
            Lines/entities indexes.

        data : dict or None
            ????????.
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        expansion_joint_data = ExpansionJointData(**data) if isinstance(data, dict) else None

        for line_id in line_ids:
            for elements in slicer(self.mesh.elements_from_line, line_id):
                for element_attributes in slicer(self.elements_attributes, elements):
                    element_attributes.expansion_joint_data = expansion_joint_data

    def add_valve_by_lines(self, line_ids: (int | list), data: dict):
        """
        This method .

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        data : dict
            ????????.
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        valve_data = ValveData(**data) if isinstance(data, dict) else None

        for line_id in line_ids:
            for elements in slicer(self.mesh.elements_from_line, line_id):
                for element_attributes in slicer(self.elements_attributes, elements):
                    element_attributes.valve_data = valve_data

    # Acoustic physical quantities
    def set_fluid_by_element(self, elements: list[int], fluid: Fluid):
        """
        This method attributes fluid object to a list of acoustic elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        fluid : Fluid object
            Fluid data.
        """
        #TODO: check inconsistencies for beam elements
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.fluid = fluid

    def set_fluid_by_lines(self, line_ids: (int | list | tuple), fluid):
        """
        This method attributes fluid object to all acoustic elements that belongs to a line/entity.

        Parameters
        ----------
        line/entity : list
            Lines/entities tags.
            
        fluid : Fluid object
            Fluid data.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            self.set_fluid_by_element(elements, fluid)

    def set_element_length_correction_by_element(self, element_ids: list, data: dict):
        """
        This method enables or disables the acoustic length correction effect in a list of acoustic elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        value : [None, 0, 1, 2]
            Acoustic length correction due to acoustic discontinuities. The prescription is done through the following labeling:
            None: disable
            0 : expansion
            1 : side_branch
            2 : loop 

        section : ?????
            ??????
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        for element_attributes in slicer(self.elements_attributes, element_ids):
            element_attributes.length_correction_data = data

    def set_perforated_plate_by_elements(self, elements: int | list | tuple, perforated_plate: PerforatedPlateData):

        if isinstance(elements, int):
            elements = [elements]

        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.perforated_plate_data = perforated_plate
            element_attributes.delta_pressure = 0
            element_attributes.pp_impedance = None

    def set_beam_xaxis_rotation_by_lines(self, line_ids: (int | list), angle: float, gimball_shift=1e-5):
        """
        """
        # promotes a small angle shift to avoid the gimbal lock rotation problems
        if angle in [90, 270]:
            angle -= gimball_shift
        elif angle in [-90, -270]:
            angle += gimball_shift
        angle *= np.pi / 180

        for elements in slicer(self.mesh.elements_from_line, line_ids):
            self.set_beam_xaxis_rotation_by_elements(elements, angle)

    def set_beam_xaxis_rotation_by_elements(self, elements, angle):
        for element_attributes in slicer(self.elements_attributes, elements):
            element_attributes.beam_xaxis_rotation = angle

    def set_elements_to_ignore_in_acoustic_analysis(self, element_ids: int | list, turned_off: bool):
        """
        """
        if isinstance(element_ids, int):
            element_ids = [element_ids]

        for element_attributes in slicer(self.elements_attributes, element_ids):
            element_attributes.turned_off = turned_off

    def get_acoustic_elements_global_dofs(self):
        """
        This method returns the acoustic global degrees of freedom of the nodes associated to structural beam elements. 
        This method helps to exclude those degrees of freedom from acoustic analysis.

        Returns
        ----------
        list
            Acoustic global degrees of freedom associated to beam element.
        """ 
        pipe_gdofs = dict()
        for index, element_attributes in self.elements_attributes.items():

            if element_attributes.turned_off:
                continue

            if element_attributes.structural_element_type in ['pipe_1', 'expansion_joint', 'valve']:
                gdofs_node_first = element_attributes.first_node.index
                gdofs_node_last = element_attributes.last_node.index
                pipe_gdofs[gdofs_node_first] = gdofs_node_first 
                pipe_gdofs[gdofs_node_last] = gdofs_node_last

        return list(pipe_gdofs.keys())


    def get_beam_and_non_beam_elements_global_dofs(self):
        """
        This method returns the acoustic global degrees of freedom of the nodes associated to structural pipe elements. This method helps to keep only those degrees of freedom in acoustic analysis.

        Returns
        ----------
        list
            Acoustic global degrees of freedom associated to pipe element.
        """
        acoustic_elements_global_dofs = self.get_acoustic_elements_global_dofs()
        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.nodes)
        all_indexes = np.arange(total_dof)
        beam_gdofs = np.delete(all_indexes, acoustic_elements_global_dofs)
        return beam_gdofs, acoustic_elements_global_dofs

    
    def _process_beam_nodes_and_indexes(self):
        """
        This method ?????.

        Returns
        ----------
        bool
            ?????
        """
        number_nodes = len(self.nodes)
        beam_gdofs, self.pipe_gdofs = self.get_beam_and_non_beam_elements_global_dofs()

        return len(beam_gdofs) == number_nodes

    def get_acoustic_elements(self) -> list[int]:
        """
        This method returns a list of acoustic elements.

        Returns
        ----------
        list
            Acoustic elements list.
        """
        acoustic_elements = list()

        for index, element_attributes in self.elements_attributes.items():
            if element_attributes.structural_element_type == "beam_1":
                continue

            if element_attributes.turned_off:
                continue

            acoustic_elements.append(index)

        return acoustic_elements

    def get_nodes_relative_to_acoustic_elements(self) -> list:
        """
        This method returns a dictionary that maps the acoustic node indexes to the acoustic elements.

        Returns
        -------
        list
            Dictionary of nodes relative to the acoustic elements.
        """

        acoustic_nodes = dict()

        for index in self.get_acoustic_elements():
            element_attributes = self.elements_attributes.get(index)
            first_node = element_attributes.first_node.index
            last_node = element_attributes.last_node.index
            acoustic_nodes[first_node] = element_attributes.first_node
            acoustic_nodes[last_node] = element_attributes.last_node

        return acoustic_nodes  

    def get_beam_elements(self) -> list:
        """
        This method returns a list of structural beam elements objects.

        Returns
        ----------
        list
            Beam elements objects.
        """
        list_elements = list()
        for index, element_attributes in self.elements_attributes.items():
            if element_attributes.structural_element_type == 'beam_1':
                list_elements.append(index)

        return list_elements

    def add_compressor_excitation(self, parameters):
        """
        This method ???????

        Parameters
        ----------
        ??????
            ???????
        """
        list_parameters = list()
        for key, parameter in parameters.items():
            if key != 'cylinder label':
                list_parameters.append(parameter)

        if 'cylinder label' in parameters.keys():
            ReciprocatingCompressorModel(list_parameters, active_cyl=parameters['cylinder label'])
        else:
            ReciprocatingCompressorModel(list_parameters)

    def get_gdofs_from_nodes(self, node_id1, node_id2):
        """
        This method returns the ordered global degrees of freedom of two nodes.

        Parameters
        ----------
        node_id1 : int
            Node 1 external index.

        node_id2 : int
            Node 2 external index.

        Returns
        ----------
        reord_gdofs : list
            Global degrees of freedom ordered according to its indexes.

        first_node : Node object
            First node. 

        last_node : Node object
            Last node.
        """
        node_1 = self.nodes[node_id1]
        node_2 = self.nodes[node_id2]

        nodes_gdofs = np.array([node_1.structural_global_dof, node_2.structural_global_dof], dtype=int).flatten()
        reord_gdofs = np.sort(nodes_gdofs)

        is_equal = np.array_equal(nodes_gdofs, reord_gdofs)

        first_node = node_1 if is_equal else node_2
        last_node = node_2 if is_equal else node_1

        return reord_gdofs, first_node, last_node

    def get_structural_links_data(self, node_ids: list, data: dict):
        """
        This method ???????

        Parameters
        ----------
        node_id1 : int
            Node 1 external index.

        node_id2 : int
            Node 2 external index.

        parameters : ??????
            ???????.

        _stiffness : bool, optional
            True if ???????. False otherwise.
            Default is False.

        _damping : bool, optional
            True if ???????. False otherwise.
            Default is False.
        """
        if len(node_ids) == 2:

            link_data = dict()

            ext_id1 = min(node_ids) 
            ext_id2 = max(node_ids)
            gdofs, *_ = self.get_gdofs_from_nodes(*node_ids)     

            gdofs_node1 = gdofs[:DOF_PER_NODE_STRUCTURAL]
            gdofs_node2 = gdofs[DOF_PER_NODE_STRUCTURAL:]
            
            if "values" in data.keys():
                values = data["values"]

                pos_data = [ value if isinstance(value, complex | np.ndarray) else None for value in values]
                neg_data = [-value if isinstance(value, complex | np.ndarray) else None for value in values]

                indexes_i = [ gdofs_node1, gdofs_node1, gdofs_node2, gdofs_node2 ] 
                indexes_j = [ gdofs_node1, gdofs_node2, gdofs_node1, gdofs_node2 ] 

                out_data = list()
                for pn_data in [ pos_data, neg_data, neg_data, pos_data ]:
                    for _data in pn_data:
                        out_data.append(_data)

                indexes_i = np.array(indexes_i, dtype=int).flatten()
                indexes_j = np.array(indexes_j, dtype=int).flatten()

                coords_1 = self.nodes[ext_id1].coordinates
                coords_2 = self.nodes[ext_id2].coordinates

                coords = list()
                coords.append(list(np.round(coords_1, 5)))
                coords.append(list(np.round(coords_2, 5)))

                node_ids = (ext_id1, ext_id2)

                link_data = {
                            "coords" : coords,
                            "indexes_i" : indexes_i,
                            "indexes_j" : indexes_j,
                            "data" : out_data
                            }

            return link_data


    def get_psd_acoustic_link_data(self, node_ids: list) -> None | AcousticLinkData:
        """
        """
        if len(node_ids) != 2:
            return

        coords = list()
        
        ext_id1 = min(node_ids) 
        ext_id2 = max(node_ids)

        neigh_elem_node_1 = self.elements_connected_to_node.get(ext_id1)
        neigh_elem_node_2 = self.elements_connected_to_node.get(ext_id2)

        if len(neigh_elem_node_1) == 1:
            element_pipe = neigh_elem_node_1[0]
            element_volume = neigh_elem_node_2[0]

            cross_section_pipe = self.get_element_cross_section(element_pipe)
            cross_section_volume = self.get_element_cross_section(element_volume)

            d_minor = cross_section_pipe.inner_diameter
            d_major = cross_section_volume.inner_diameter

        elif len(neigh_elem_node_2) == 1:
            element_pipe = neigh_elem_node_2[0]
            element_volume = neigh_elem_node_1[0]

            cross_section_pipe = self.get_element_cross_section(element_pipe)
            cross_section_volume = self.get_element_cross_section(element_volume)

            d_minor = cross_section_pipe.inner_diameter
            d_major = cross_section_volume.inner_diameter

        else:
            return
        
        node_1 = self.nodes[ext_id1]
        node_2 = self.nodes[ext_id2]

        int_id1 = node_1.index
        int_id2 = node_2.index

        indexes_i = [ int_id1, int_id2, int_id1, int_id2 ] 
        indexes_j = [ int_id1, int_id1, int_id2, int_id2 ]

        pipe_element_attributes = self.elements_attributes.get(element_pipe)
        pipe_element_attributes.acoustic_link_diameters = [d_minor, d_major]

        coords_1 = node_1.coordinates
        coords_2 = node_2.coordinates

        coords.append(list(np.round(coords_1, 5)))
        coords.append(list(np.round(coords_2, 5)))
        length = np.linalg.norm(coords_2 - coords_1)

        node_ids = (ext_id1, ext_id2)
        diameters = [d_minor, d_major]

        return AcousticLinkData(coords, indexes_i, indexes_j, pipe_element_attributes, diameters, length)

    def get_psd_structural_link_data(self, node_ids: list, k=1e9, kr=1e8):
        """
        """
        if len(node_ids) == 2:

            coords = list()

            ext_id1 = min(node_ids) 
            ext_id2 = max(node_ids)

            gdofs, *args = self.get_gdofs_from_nodes(ext_id1, ext_id2)
            gdofs_node1 = gdofs[:DOF_PER_NODE_STRUCTURAL]
            gdofs_node2 = gdofs[DOF_PER_NODE_STRUCTURAL:]

            stiffness = np.array([k, k, k, kr, kr, kr], dtype=float)
            pos_data = np.ones(DOF_PER_NODE_STRUCTURAL, dtype=float) * stiffness
            neg_data = -pos_data

            indexes_i = [ gdofs_node1, gdofs_node1, gdofs_node2, gdofs_node2 ] 
            indexes_j = [ gdofs_node1, gdofs_node2, gdofs_node1, gdofs_node2 ] 
            out_data = [ pos_data, neg_data, neg_data, pos_data ]

            indexes_i = np.array(indexes_i, dtype=int).flatten()
            indexes_j = np.array(indexes_j, dtype=int).flatten()
            out_data = np.array(out_data, dtype=float).flatten()

            coords_1 = self.nodes[ext_id1].coordinates
            coords_2 = self.nodes[ext_id2].coordinates

            coords.append(list(np.round(coords_1, 5)))
            coords.append(list(np.round(coords_2, 5)))

            node_ids = (ext_id1, ext_id2)

            data = {
                    "coords" : coords,
                    "indexes_i" : indexes_i,
                    "indexes_j" : indexes_j,
                    "data" : out_data
                    }

            return data


    def get_acoustic_transfer_element_data(self, node_ids: list, data: dict):
        """
        """
        if len(node_ids) == 2:

            coords = list()
            input_node_id, output_node_id = node_ids

            int_id1 = self.nodes[input_node_id].index
            int_id2 = self.nodes[output_node_id].index

            indexes_i = [ int_id1, int_id1, int_id2, int_id2 ] 
            indexes_j = [ int_id1, int_id2, int_id1, int_id2 ]

            coords_1 = self.nodes[input_node_id].coordinates
            coords_2 = self.nodes[output_node_id].coordinates

            coords.append(list(np.round(coords_1, 5)))
            coords.append(list(np.round(coords_2, 5)))

            if data["element_transfer_data_source"] == "admittance_matrix":
                a11, a12, a21, a22 = data["values"]

            else:
                H11, H21, H12, H22 = data["values"]

                if output_node_id > input_node_id:

                    _det = (H11*H22 - H21*H12)
                    a11 =  H22 / _det
                    a12 = -H12 / _det
                    a21 = -H21 / _det
                    a22 =  H11 / _det

                else:

                    #TODO: validate this case
                    _det = (H12*H21 - H11*H22)
                    a11 =  H12 / _det
                    a12 = -H22 / _det
                    a21 = -H11 / _det
                    a22 =  H21 / _det

            Te = np.array([a11, a12, a21, a22], dtype=complex).T

            data = {
                    "coords" : coords,
                    "indexes_i" : indexes_i,
                    "indexes_j" : indexes_j,
                    "data_Te" : Te
                    }

            return data


    def process_cross_sections_mapping(self):

        indexes = [0, 1]
        label_etypes = ['pipe_1', 'valve']

        map_cross_section_to_elements = defaultdict(list)
        map_etype_to_index = dict(zip(label_etypes, indexes))
        map_index_to_etype = dict(zip(indexes, label_etypes))

        logging.info("Processing the cross-sections [25%]")

        for index, element_attributes in self.elements_attributes.items():
            e_type = element_attributes.structural_element_type

            if e_type in ["beam_1", "expansion_joint", "rigid_element"]:
                continue

            if e_type == "pipe_1" and element_attributes.is_section_variable:
                continue

            if e_type is None:
                e_type = "pipe_1"
                self.acoustic_analysis = True

            index_etype = map_etype_to_index.get(e_type)

            material = element_attributes.material
            poisson = material.poisson_ratio
            if poisson is None:
                poisson = 0

            cross_section = element_attributes.cross_section
            section_parameters = cross_section.section_info.section_parameters
            section_parameters.extend([poisson, index_etype])

            map_cross_section_to_elements[str(section_parameters)].append(index)
            if self.stop_processing:
                return

        logging.info("Processing the cross-sections [80%]")

        for key, elements in map_cross_section_to_elements.items():

            cross_strings = key[1:-1].split(",")
            section_parameters = [float(value) for value in cross_strings[:6]]

            index_etype = int(cross_strings[-1])
            el_type = map_index_to_etype.get(index_etype)

            if el_type == "pipe_1":
                pipe_section_info = PipeCrossSection(*section_parameters)
                cross_section = CrossSection(pipe_section_info=pipe_section_info)

            elif el_type == "valve":
                valve_section_info = ValveCrossSection(*section_parameters)
                cross_section = CrossSection(valve_section_info=valve_section_info)

            if self.stop_processing:
                return True

            logging.info("Processing the cross-sections [95%]")

            self.set_cross_section_by_elements(
                elements, cross_section, update_properties=True, sections_mapping=True
            )

    def get_number_of_elements_by_element_type(self):
        """" This method returns """
        acoustic_etype_to_number_elements = {
            "undamped": 0,
            "proportional": 0,
            "wide_duct": 0,
            "LRF_fluid_equivalent": 0,
            "LRF_full": 0,
            "undamped_mean_flow": 0,
            "howe": 0,
            "peters": 0,
            None: 0,
        }

        structural_etype_to_number_elements = {"pipe_1": 0, "beam_1": 0, "expansion_joint": 0, "valve": 0, None: 0}
        
        acoustic_etype_to_elements = defaultdict(list)
        structural_etype_to_elements = defaultdict(list)

        for index, element_attributes in self.elements_attributes.items():
            structural_element_type = element_attributes.structural_element_type
            structural_etype_to_number_elements[structural_element_type] += 1
            structural_etype_to_elements[structural_element_type].append(index)

            if structural_element_type == 'beam_1':
                continue

            acoustic_element_type = element_attributes.acoustic_element_type
            acoustic_etype_to_number_elements[acoustic_element_type] += 1
            acoustic_etype_to_elements[acoustic_element_type].append(index)

        return structural_etype_to_number_elements, acoustic_etype_to_number_elements

    def set_unprescribed_pipe_indexes(self, indexes):
        self.unprescribed_pipe_indexes = indexes
    
    def get_unprescribed_pipe_indexes(self):
        return self.unprescribed_pipe_indexes

    def update_nodal_solution_info(self, nodal_solution: np.ndarray):
        """ This method sets the static nodal solution for 
            stress stiffening analysis.
        Parameters
        ----------
        nodal_solution: complex array of values
        """

        for node in self.nodes.values():  
            node.static_nodal_solution_gcs = nodal_solution[node.structural_global_dof, 0]

        for element_attributes in self.elements_attributes.values():
            element_attributes.static_analysis_evaluated = True

    def get_cross_sections_from_node(self, node_id: int) -> list[CrossSection]:

        cross_sections_from_node = list()
        for element_id in self.elements_connected_to_node.get(node_id, list()):
            cross_section = self.get_element_cross_section(element_id)
            if cross_section not in cross_sections_from_node:
                cross_sections_from_node.append(cross_section)

        return cross_sections_from_node

    def process_all_transformation_matrices(self):
        """
        This method processes the element and cross-section rotations. 
        """
        n_el = self.number_structural_elements
        delta_data = np.zeros((n_el, 3), dtype=float)
        xaxis_rotation_angle = np.zeros(n_el, dtype=float)
   
        for index, (element_id, element_attributes) in enumerate(self.elements_attributes.items()):
            delta_data[index, :] = element_attributes.delta_x, element_attributes.delta_y, element_attributes.delta_z
            xaxis_rotation_angle[index] = element_attributes.xaxis_rotation_angle

        self.rotation_matrix_gcs_to_lcs = rotation_matrix_3x3_by_deltas(
            delta_data[:, 0],
            delta_data[:, 1],
            delta_data[:, 2],
            gamma = xaxis_rotation_angle,
            )

        # # old version to compute the normal vector rotation angles
        # rot = Rotation.from_matrix(self.rotation_matrix_gcs_to_lcs)
        # rot_angles = -rot.as_euler('zxy', degrees=True)

        # new version to compute the normal vector rotation angles
        rot = Rotation.from_matrix(self.rotation_matrix_gcs_to_lcs.transpose(0, 2, 1))
        rot_angles = rot.as_euler('yxz', degrees=True)

        self.undeformed_section_rotations = np.array([rot_angles[:, 1], rot_angles[:, 0], rot_angles[:, 2]], dtype=float).T

    def process_element_cross_sections_orientation_to_plot(self, modif_nodal_solution: np.ndarray):
        """
        This method processes each element cross-seciton in accordance with
        the element rotation matrix.
        """
        rotation_data = np.zeros((self.number_structural_elements, 3), dtype=float)

        for i, (index, element_attributes) in enumerate(self.elements_attributes.items()):

            # first_node = element_attributes.first_node
            # last_node = element_attributes.last_node

            # first_node.nodal_solution_gcs = modif_nodal_solution[first_node.structural_global_dof]
            # last_node.nodal_solution_gcs = modif_nodal_solution[last_node.structural_global_dof]

            if element_attributes.decoupling_info is None:
                rotation_data[i, :] = element_attributes.mean_rotations_at_local_coordinate_system()
            else:
                rotation_data[i, :] = element_attributes.rotations_at_local_coordinate_system_decoupled()

        rotation_results_matrices = rotation_matrix_3x3_by_angles(rotation_data[:, 0], rotation_data[:, 1], rotation_data[:, 2])
        matrix_resultant = rotation_results_matrices @ self.rotation_matrix_gcs_to_lcs

        r = Rotation.from_matrix(matrix_resultant)
        rot_angles = -r.as_euler('zxy', degrees=True)

        self.deformed_section_rotations = np.array([rot_angles[:, 1], rot_angles[:, 2], rot_angles[:, 0]], dtype=float).T

    def get_geometry_points(self) -> dict[int, Node]:
        points = dict()
        for i in self.mesh.geometry_points:
            points[i] = self.nodes[i]

        return points
    


    ## TODO: Please, just remove these lines once we're convinced that everything is fine.

    # def _create_nodes(self, indexes, coords, map_nodes):
    #     """
    #     This method generate the mesh nodes.

    #     Parameters
    #     ----------
    #     indexes : List
    #         Nodes global indexes.
            
    #     coords : array
    #         Nodes coordinates.
            
    #     map_nodes : dict
    #         Dictionary maps global indexes to external indexes.
    #     """
    #     self.map_nodes = map_nodes
    #     self.nodes.clear()
    #     for i, coords in zip(indexes, split_sequence(coords, 3)):
    #         # x = convert_length_unit(coord[0], "mm", "m")
    #         # y = convert_length_unit(coord[1], "mm", "m")
    #         # z = convert_length_unit(coord[2], "mm", "m")
    #         x, y, z = convert_length_unit(coords, "mm", "m")

    #         self.nodes[map_nodes[i]] = Node(x, y, z, external_index=int(map_nodes[i]))

    #     self.number_nodes = len(self.nodes)

    # def _create_elements_attributes(self, indexes, connectivities, map_nodes: dict, map_elements: dict):
    #     """
    #     This method generate the mesh structural elements.

    #     Parameters
    #     ----------
    #     indexes : List
    #         Nodes global indexes.
            
    #     connectivities : array
    #         Connectivity matrix that relates the elements and its nodes.
            
    #     map_nodes : dict
    #         Dictionary maps global indexes to external indexes.
            
    #     map_elements : dict
    #         Dictionary maps global element indexes.
    #     """
    #     self.map_elements = map_elements
    #     self.elements_attributes.clear()

    #     # self.element_coordinates = np.array((2, len(map_elements), 3), dtype=float)
    #     for i, connect in zip(indexes, split_sequence(connectivities, 2)):
    #         first_node_id = map_nodes.get(connect[0])
    #         last_node_id = map_nodes.get(connect[1])

    #         first_node = self.nodes.get(first_node_id)
    #         last_node  = self.nodes.get(last_node_id)

    #         element_index = map_elements[i]
    #         self.elements_attributes[element_index] = ElementAttributes(element_index, first_node, last_node)

    # def _order_global_indexes(self):
    #     """
    #     This method updates the nodes global indexes numbering.
    #     """
    #     # t0 = perf_counter()
    #     index = 0
    #     stack = deque()
    #     list_nodes = list(self.nodes.values())

    #     stack.appendleft(list_nodes[0].index) 

    #     while stack:
        
    #         top = self.nodes[stack.pop()]
    
    #         if top.index is None:
    #             top.index = index
    #             index += 1
    #         else:
    #             continue
            
    #         for neighbor in self.neighbors_nodes[top.index]:
    #             if neighbor.index is None:
    #                 if neighbor.index not in stack:
    #                     stack.appendleft(neighbor.index)
                    
    #         if len(stack) != 0:
    #             continue

    #         if index < self.number_nodes - 1:
    #             for node in list_nodes:
    #                 if node.index is None:
    #                     stack.appendleft(node.index)
    #                     break

    #             #TODO: uncomment to begin from start or end nodes
    #             # for node in list_nodes:
    #             #     if len(self.neighbors_nodes[node]) == 1:
    #             #         stack.appendleft(node)   

    # def _mapping_nodes_indexes(self):
    #     self.map_global_to_external_index = {node.index:node.index for node in self.nodes.values()}

    # def get_dict_nodes_to_element_indexes(self):
    #     """
    #     This method updates the dictionary that maps the external node to the element index.
    #     """
    #     self.dict_first_node_to_element_index = defaultdict(list)
    #     self.dict_last_node_to_element_index = defaultdict(list)
    #     for index, element_attributes in self.elements_attributes.items():
    #         first_node_index = element_attributes.first_node.index
    #         last_node_index = element_attributes.last_node.index
    #         self.dict_first_node_to_element_index[first_node_index].append(index)
    #         self.dict_last_node_to_element_index[last_node_index].append(index)

    # def get_nodal_coordinates_matrix(self, reordering=True):
    #     """
    #     This method updates the mesh nodes coordinates data. Coordinates matrix row structure:
    #     ''[Node index, x-coordinate, y-coordinate, z-coordinate]''.

    #     Parameters
    #     ----------
    #     reordering : bool, optional.
    #         True if the nodes numbering is according to the global indexing. False otherwise.
    #         Default is True.
    #     """
    #     # self.number_nodes = len(self.nodes)
    #     nodal_coordinates = np.zeros((self.number_nodes, 4))
    #     nodal_coordinates_external = nodal_coordinates

    #     # if reordering:
    #     for external_index, node in self.nodes.items():
    #         index = self.nodes[external_index].index
    #         nodal_coordinates[index,:] = index, node.x, node.y, node.z
    #         nodal_coordinates_external[index,:] = external_index, node.x, node.y, node.z
    #     # else:               
    #     #     for external_index, node in self.nodes.items():
    #     #         index = self.nodes[external_index].index
    #     #         nodal_coordinates[index,:] = external_index, node.x, node.y, node.z

    #     self.nodal_coordinates_matrix = nodal_coordinates
    #     self.nodal_coordinates_matrix_external = nodal_coordinates_external

    # def get_connectivity_matrix(self, reordering=True):
    #     """
    #     This method updates the mesh connectivity data. Connectivity matrix row structure:
    #     ''[Element index, first node index, last node index]''.

    #     Parameters
    #     ----------
    #     reordering : bool, optional.
    #         True if the nodes numbering is according to the global indexing. False otherwise.
    #         Default is True.
    #     """
    #     connectivity = np.zeros((self.number_structural_elements, NODES_PER_ELEMENT+1))
    #     if reordering:
    #         for i, element_attributes in enumerate(self.elements_attributes.values()):
    #             first_node = element_attributes.first_node
    #             last_node  = element_attributes.last_node
    #             # first_external = element.first_node.index
    #             # last_external  = element.last_node.index
    #             connectivity[i, :] = i + 1, first_node.index, last_node.index

    #     else:
    #         for i, element_attributes in enumerate(self.elements_attributes.values()):
    #             first_node = element_attributes.first_node
    #             last_node  = element_attributes.last_node
    #             connectivity[i, :] = i + 1, first_node.index, last_node.index

    #     self.connectivity_matrix = connectivity.astype(int) 
    
    # def get_neighbor_nodes_and_elements_by_node(self, node_id: int, length: float, tolerance: float = 1e-6):
    #     """ This method returns two lists of nodes ids and elements ids at the neighborhood of the 
    #         node_id in the range of -(length/2) - tolerance and (length/2) + tolerance. The tolerance 
    #         avoids the problem of element size deviations resultant in the mesh generation algorithm.
        
    #     Parameters
    #     ----------

    #     Returns
    #     ---------- 

    #     """ 
    #     half_length = (length/2) + tolerance
    #     node_central = self.nodes[node_id]
    #     list_nodes_ids = [node_id]
    #     stack = deque()
    #     stack.appendleft(node_id)

    #     while stack:

    #         node_ids = self.neighbors_nodes[self.nodes[stack.pop()].index]
    #         if len(node_ids) > 2:
    #             return None, None

    #         for node_id in node_ids:
    #             if np.linalg.norm((node_central.coordinates - self.mesh.nodal_coordinates[node_id, 1:])) > half_length:
    #                 continue

    #             if node_id in list_nodes_ids:
    #                 continue

    #             list_nodes_ids.append(node_id)
    #             stack.appendleft(node_id)                    

    #     list_elements_ids = list()
    #     for index, element_attributes in self.elements_attributes.items():
    #         if element_attributes.first_node.index in list_nodes_ids:
    #             if element_attributes.last_node.index in list_nodes_ids:
    #                 list_elements_ids.append(index)

    #         if len(list_elements_ids) == len(list_nodes_ids) - 1:
    #             break

    #     return list_nodes_ids, list_elements_ids

    # def get_neighbor_nodes_and_elements_by_element(self, element_id, length, tolerance=1e-5):
    #     """ This method returns two lists of nodes ids and elements ids at the neighborhood of the 
    #         element_id in the range of -(length/2) - tolerance and (length/2) + tolerance. The tolerance 
    #         avoids the problem of element size deviations resultant in the mesh generation algorithm.

    #     Parameters
    #     ---------- 

    #     Returns
    #     ---------- 
                               
    #     """
    #     element_attributes = self.elements_attributes.get(element_id)
    #     node_id = element_attributes.first_node.index
    #     last_node = element_attributes.last_node

    #     length_t = length + element_attributes.length
    #     list_nodes_ids, list_elements_ids = self.get_neighbor_nodes_and_elements_by_node(node_id, length_t, tolerance=tolerance)

    #     if list_nodes_ids is not None:
                
    #         for external_index in list_nodes_ids:
    #             node = self.nodes[external_index]
    #             if np.linalg.norm((last_node.coordinates - node.coordinates)) > ((length_t/2) + tolerance):
    #                 list_nodes_ids.remove(node.index)

    #         for index in list_elements_ids:
    #             if element_attributes.first_node.index in list_nodes_ids:
    #                 continue
                
    #             index = element_attributes.index
    #             if index in list_elements_ids:
    #                 list_elements_ids.remove(index)

    #             if element_attributes.last_node.index in list_nodes_ids:
    #                 continue

    #             if index in list_elements_ids: 
    #                 list_elements_ids.remove(index)
                    
    #         return list_nodes_ids, list_elements_ids
    #     else:
    #         return None, None