
from typing import TYPE_CHECKING

from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_length_unit
# from pulse.model.mesh_utils import ElementConnectivityData, get_connectivity
from pulse.model.data_classes.project_setup_data_classes import MesherSetup

if TYPE_CHECKING:
    from pulse.project.project import Project

import os
from collections import defaultdict
from enum import IntEnum

import gmsh
import numpy as np
# from time import perf_counter

class ImportType(IntEnum):
    CAD_FILE = 0
    BUILT_IN = 1


class Mesh:
    def __init__(self, project: 'Project'):
        super().__init__()

        self.project = project
        # self.preprocessor = project.model.preprocessor

        self.mesher_setup = MesherSetup()

        self.reset_variables()

    def reset_variables(self):
        """
        This method reset the class default values.
        """

        self.geometry_points = list()
        self.lines_from_model = list()

        self.line_from_element = dict()
        self.elements_from_line = defaultdict(list)
        self.lines_from_node = defaultdict(list)
        self.nodes_from_line = defaultdict(list)

        self.elements_from_gmsh_lines = dict()
        self.nodes_from_gmsh_lines = dict()

        self.lines_mapping = dict()
        self.curve_length = dict()
        self.valve_internal_lines = dict()

        self.section_nodal_coordinates = np.array([])
        self.section_connectivities = dict()

    @property
    def element_size(self):
        return self.mesher_setup.element_size

    @property
    def geometry_tolerance(self):
        return self.mesher_setup.geometry_tolerance

    @property
    def length_unit(self):
        return self.mesher_setup.length_unit

    def set_mesher_setup(self, mesher_setup: MesherSetup):
        self.mesher_setup = mesher_setup

    def generate(self, import_type: ImportType, geometry_path: str = ""):
        """
        This method loads geometry file or data and process the mesh.
        """
        self.reset_variables()

        if import_type == ImportType.CAD_FILE:
            if not os.path.exists(geometry_path):
                return

            self._load_cad_geometry_on_gmsh(geometry_path)

        self._create_gmsh_geometry()
        self._set_gmsh_options()

        self._process_mesh()
        self._process_gmsh_lines_mesh_data()
        self._concatenate_line_elements()
        # self._concatenate_line_nodes()

        self._save_geometry_points()
        self._finalize_gmsh()
    
    def _load_cad_geometry_on_gmsh(self, geometry_path: str):
        """
        This method initializes mesher algorithm gmsh.
        """
        geometry_handler = GeometryHandler(self.project)
        geometry_handler.set_length_unit(self.length_unit)
        geometry_handler.open_cad_file(str(geometry_path))

    def _create_gmsh_geometry(self):
        """
        This method creates the GMSH geometry based on entity file data.
        """
        geometry_handler = GeometryHandler(self.project)
        geometry_handler.set_length_unit(self.length_unit) 
        geometry_handler.process_pipeline()
        geometry_handler.create_geometry()

        self.lines_mapping = geometry_handler.lines_mapping
        self.curve_length = geometry_handler.curve_length
        self.valve_internal_lines = geometry_handler.valve_internal_lines

    def _set_gmsh_options(self):
        """
        This method sets the mesher algorithm configuration.
        """
        try:
            gmsh.option.setNumber("General.NumThreads", 4)
        except Exception:
            pass

        length = convert_length_unit(self.element_size, self.length_unit, "mm")

        # if self.length_unit == 'meter':
        #     length = m_to_mm(self.element_size)
        # elif self.length_unit == 'inch':
        #     length = in_to_mm(self.element_size)
        # else:
        #     length = self.element_size

        gmsh.option.setNumber('Geometry.Tolerance', self.geometry_tolerance)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 0.5 * length)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', length)
        gmsh.option.setNumber('Mesh.CharacteristicLengthExtendFromBoundary', 1)
        gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 1)
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        # gmsh.option.setNumber('Mesh.RecombineAll', 1)

    def _process_mesh(self):
        """
        This method generate the mesh entities, nodes, structural elements, acoustic elements 
        and their connectivity.
        """

        try:

            # Remove coincident geometric entities (geometry level)
            # NOTE: check the tags coherence carefully after removing the duplicates
            gmsh.model.occ.removeAllDuplicates() 
            gmsh.model.occ.synchronize()

            # Apply per-structure mesh constraints
            from pulse.editor.structures.rigid_element import RigidElement
            for structure in self.project.pipeline.structures:
                if isinstance(structure, RigidElement):
                    structure.define_gmsh_mesh_constraints()()

            # self._remove_orphan_points()

            # generate mesh for 1D elements
            gmsh.model.mesh.generate(1)

            nodes_tags, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
            _, elements_tags, connectivity = gmsh.model.mesh.getElements()

            _nodes_tags = np.unique(nodes_tags)
            _elements_tags = np.unique(elements_tags[0])

            # self.map_nodes = dict(zip(_nodes_tags, np.arange(_nodes_tags.size, dtype=int)))
            # self.map_elements = dict(zip(_elements_tags, np.arange(_elements_tags.size, dtype=int)))

            self.map_nodes = dict(zip(_nodes_tags, np.arange(1, _nodes_tags.size + 1, 1, dtype=int)))
            self.map_elements = dict(zip(_elements_tags, np.arange(1, _elements_tags.size + 1, 1, dtype=int)))

            # self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
            # self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))

            ## TODO: we can replace the self.nodes attribute with a proper coordinates matrix
            # and the connectivity matrix should be used to build actors rather than looping self.elements_attributes

            self.project.model.preprocessor._create_nodes(nodes_tags, coords, self.map_nodes)
            self.project.model.preprocessor._create_elements_attributes(elements_tags[0], connectivity[0], self.map_nodes, self.map_elements)                    
            self.project.model.preprocessor.update_number_divisions()

        except Exception as log_error:
            from traceback import print_exception
            print_exception(log_error)

    def _remove_orphan_points(self):

        orphan_points = list()
        for dim, tag in gmsh.model.getEntities(dim=0):
            upward, _ = gmsh.model.getAdjacencies(dim, tag)

            if len(upward) == 0:
                orphan_points.append(tag)

        # for orphan_point in orphan_points:
        #     point_coords = gmsh.model.getValue(0, orphan_point, [])
        #     print(orphan_point, point_coords)

        dim_tags = [(0, orphan_point) for orphan_point in orphan_points]
        gmsh.model.occ.remove(dim_tags, recursive=False)
        gmsh.model.occ.synchronize()

    def _process_section_mesh(self):
        """
        This method generate the section mesh and processes the nodal 
        coordinates and the connectivity.
        """

        try:

            gmsh.model.mesh.generate(3)
            gmsh.model.mesh.removeDuplicateNodes()

            # gmsh.option.setNumber('General.FltkColorScheme', 1)
            # gmsh.fltk.run()

            # process the nodal coordinates
            node_indexes, coords, _ = gmsh.model.mesh.getNodes(2, -1, True)
            self.process_section_nodal_coordinates(node_indexes, coords)

            # process the connectivity
            element_types, element_indexes, element_nodes = gmsh.model.mesh.getElements(2, -1)

            if len(element_indexes) > 1:
                print("multiple element type detected")

            for i in range(len(element_nodes)):
                element_name, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_types[i])
                self.process_section_connectivity(element_indexes[i], element_nodes[i], element_name, nodes_per_element)

        except Exception as log_error:
            from traceback import print_exception
            print_exception(log_error)

    def process_section_nodal_coordinates(self, node_indexes: np.ndarray, coords: np.ndarray):
        """ 
        it processes the nodal coordinates from section mesh.
        """
        n_nodes = len(node_indexes)
        n_indexes = np.arange(n_nodes, dtype=int)
        self.section_nodal_coordinates = np.zeros((n_nodes, 4))
        self.section_nodal_coordinates[n_indexes, 1:] = convert_length_unit(coords.reshape(-1, 3), "mm", "m")
        self.section_nodal_coordinates[n_indexes, :1] = node_indexes.reshape(-1, 1) - 1

    def process_section_connectivity(self, element_indexes: np.ndarray, element_nodes: np.ndarray, element_name: str, nodes_per_element: int):
        """ 
        It processes the connectivity from section mesh.
        """
        n_elements = len(element_indexes)
        e_indexes = np.arange(n_elements, dtype=int)
        cols = nodes_per_element

        section_connectivity = np.zeros((n_elements, cols+1))
        section_connectivity[:, 0] = e_indexes
        section_connectivity[:, 1:] = element_nodes.reshape(-1, cols) - 1

        self.section_connectivities.clear()
        self.section_connectivities[element_name] = section_connectivity

    def _process_gmsh_lines_mesh_data(self):
        """
        This method maps the elements and nodes for each GMSH line.

        """
        # t0 = perf_counter()

        self.elements_from_gmsh_lines.clear()
        self.nodes_from_gmsh_lines.clear()

        for dim, tag in gmsh.model.getEntities(1):

            _, elements_tags, _ = gmsh.model.mesh.getElements(dim, tag)
            if not elements_tags:
                continue

            self.elements_from_gmsh_lines[tag] = [self.map_elements[element] for element in elements_tags[0]]

            line_nodes, _coords, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            self.nodes_from_gmsh_lines[tag] = [self.map_nodes[node] for node in line_nodes]

        # dt = perf_counter() - t0
        # print(f"Time to process '_process_gmsh_lines_mesh_data': {dt}")

        # t0 = perf_counter()

        # nodes_tags, nodes_coords, _ = gmsh.model.mesh.getNodes(1, -1, includeBoundary=True)
        # total_nodes = np.unique(nodes_tags).size

        # self.nodal_coordinates = np.zeros((total_nodes, 4))
        # self.nodal_coordinates[nodes_tags - 1, 1:] = convert_length_unit(nodes_coords.reshape(-1, 3), "mm", "meter")
        # self.nodal_coordinates[nodes_tags - 1, :1] = nodes_tags.reshape(-1, 1) - 1
        # # print(total_nodes, np.min(nodes_tags), np.max(nodes_tags))

        # # # nodes_from_lines = gmsh.model.mesh.getNodes(dim=1, includeBoundary=True)[0]

        # # # if isinstance(nodes_from_lines, np.ndarray):
        # # #     self.nodes_from_lines = np.unique(nodes_from_lines) - 1

        # connectivity_data = dict()

        # for dim, tag in gmsh.model.getEntities(1):
        #     elements_data = dict()
        #     element_types, element_indexes, connectivities = gmsh.model.mesh.getElements(dim, tag)

        #     if not element_indexes:
        #         continue

        #     for i, element_type in enumerate(element_types):
        #         _, _, _, nodes_per_element, _, _ = gmsh.model.mesh.getElementProperties(element_type)

        #         array_connectivities = np.array(connectivities[i]).reshape(-1, nodes_per_element)
        #         array_connectivities -= 1

        #         elements_data[element_type] = ElementConnectivityData(element_indexes[i], array_connectivities) 

        #     connectivity_data[dim, tag] = elements_data

        # self.lines_connectivity, self.map_line_elements = get_connectivity(connectivity_data)
  
        # dt = perf_counter() - t0
        # print(f"Time to process : {dt}")

        # # print(self.nodal_coordinates)
        # # print(np.unique(self.lines_connectivity[:, 4:]))
        # # self.map_elements_from_lines()

    def map_elements_from_lines(self):
        self.elements_from_line.clear()
        for line_id in np.unique(self.lines_connectivity[:, 1]).astype(int):
            rows = np.where(self.lines_connectivity[:, 1] == line_id)[0]
            self.elements_from_line[line_id] = self.lines_connectivity[rows, 0]

    def _concatenate_line_elements(self):
        """
        """
        self.elements_from_line.clear()
        elements_to_ignore_on_acoustic_analysis = list()
        for tag, line_elements in self.elements_from_gmsh_lines.items():
            line_id = self.lines_mapping.get(tag)
            if line_id is None:
                continue

            self.elements_from_line[line_id].extend(line_elements)
            if tag in self.valve_internal_lines.keys():
                elements_to_ignore_on_acoustic_analysis.extend(line_elements)

        self.line_from_element.clear()
        for _line_id, element_ids in self.elements_from_line.items():
            for element_id in element_ids:
                self.line_from_element[element_id] = _line_id

        self.lines_from_model = list(self.elements_from_line.keys())
        self.project.model.preprocessor.set_elements_to_ignore_in_acoustic_analysis(elements_to_ignore_on_acoustic_analysis, True)

    def _concatenate_line_nodes(self):
        """
        """
        self.lines_from_node.clear()
        self.nodes_from_line.clear()
        for tag, line_nodes in self.nodes_from_gmsh_lines.items():
            line_id = self.lines_mapping[tag]
            self.nodes_from_line[line_id].extend(line_nodes)
            for node_id in line_nodes:
                self.lines_from_node[node_id].append(line_id)

    def _process_line_nodes(self):
        """
        """
        self.lines_from_node.clear()
        self.nodes_from_line.clear()
        for node_id, element_ids in self.project.model.preprocessor.elements_connected_to_node.items():
            for element_id in element_ids:

                line_id = self.line_from_element.get(element_id)
                if line_id is None:
                    continue

                if line_id in self.nodes_from_line.keys():
                    if node_id not in self.nodes_from_line[line_id]:
                        self.nodes_from_line[line_id].append(node_id)
                else:
                    self.nodes_from_line[line_id].append(node_id)

                if node_id in self.lines_from_node.keys():
                    if line_id not in self.lines_from_node[node_id]:
                        self.lines_from_node[node_id].append(line_id)
                else:
                    self.lines_from_node[node_id].append(line_id)

    def _save_geometry_points(self):
        """
        It gathers the nodes of the structure in the 'geometry_points' attribute.
        """
        self.geometry_points.clear()
        node_ids, *_ = gmsh.model.mesh.getNodes(0, -1)
        for tag in node_ids:
            index = self.map_nodes.get(tag)
            if index is None:
                continue
            self.geometry_points.append(index)

    def _finalize_gmsh(self):
        """
        This method finalize the mesher gmsh algorithm.
        """
        gmsh.finalize()

    def get_geometry_statistics(self):
        return len(self.geometry_points), len(self.lines_from_model)