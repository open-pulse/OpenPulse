
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.utils.common_utils import *
from pulse.utils.unit_conversion import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pulse.project.project import Project

import os
import gmsh 
import numpy as np

from collections import defaultdict

window_title_1 = "Error"


class Mesh:
    def __init__(self, project: 'Project'):
        super().__init__()

        self.project = project
        # self.preprocessor = project.model.preprocessor

        self.reset_variables()
        self.set_mesher_setup()

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

    def set_element_size(self, element_size):
        self.element_size = element_size

    def set_mesher_setup(self, **kwargs):
        mesher_setup = kwargs.get("mesher_setup", dict())
        self.element_size = mesher_setup.get('element_size', 0.01)
        self.tolerance = mesher_setup.get('geometry_tolerance', 1e-6)
        self.length_unit = mesher_setup.get('length_unit', 'meter')
        self.import_type = mesher_setup.get("import_type", 1)
        self.geometry_path = mesher_setup.get('geometry_path', "")

    def generate(self):
        """
        This method loads geometry file or data and process the mesh.

        Parameters
        ----------
        import_type : int
            This number is equal to 0 if there is an imported geometry file or
            assumes value equals to 1 otherwise.

        geometry_path : str
            CAD file path '*.igs' and '*.step' are the file formats supported.

        element_size : float
            Element size to be used to build the preprocessor.
        
        tolerance: : float
            A small float number that represents the geometry tolerance in GMSH.

        gmsh_geometry : bool
            This variable reaches True value if the geometry is created by user or False if it is imported.

        length_unit: : str
            The length unit in use.
            
        """
        self.reset_variables()

        if self.import_type == 0:
            if os.path.exists(self.geometry_path):
                self._load_cad_geometry_on_gmsh()
            else:
                return

        self._create_gmsh_geometry()
        self._set_gmsh_options()

        self._process_mesh()
        self._process_gmsh_lines_mesh_data()
        self._concatenate_line_elements()
        # self._concatenate_line_nodes()

        self._save_geometry_points()
        self._finalize_gmsh()
    
    def _load_cad_geometry_on_gmsh(self):
        """
        This method initializes mesher algorithm gmsh.

        Parameters
        ----------

        """
        geometry_handler = GeometryHandler(self.project)
        geometry_handler.set_length_unit(self.length_unit)
        geometry_handler.open_cad_file(str(self.geometry_path))

    def _create_gmsh_geometry(self):
        """
        This method creates the GMSH geometry based on entity file data.

        Parameters
        ----------

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

        Parameters
        ----------

        """
        try:
            gmsh.option.setNumber("General.NumThreads", 4)
        except:
            pass

        if self.length_unit == 'meter':
            length = m_to_mm(self.element_size)
        elif self.length_unit == 'inch':
            length = in_to_mm(self.element_size)
        else:
            length = self.element_size

        gmsh.option.setNumber('Geometry.Tolerance', self.tolerance)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 0.5*length)
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

            gmsh.model.mesh.generate(3)
            gmsh.model.mesh.removeDuplicateNodes()

            node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
            _, element_indexes, connectivity = gmsh.model.mesh.getElements()

            self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
            self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))

            self.project.model.preprocessor._create_nodes(node_indexes, coords, self.map_nodes)
            self.project.model.preprocessor._create_structural_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)
            self.project.model.preprocessor._create_acoustic_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)                       
            self.project.model.preprocessor.update_number_divisions()

        except Exception as log_error:
            from traceback import print_exception
            print_exception(log_error)

    def _process_gmsh_lines_mesh_data(self):
        """
        This method maps the elements and nodes for each GMSH line.

        """
        # t0 = time()

        self.elements_from_gmsh_lines.clear()
        self.nodes_from_gmsh_lines.clear()

        for dim, tag in gmsh.model.getEntities(1):

            _, list_line_elements, _ = gmsh.model.mesh.getElements(dim, tag)
            if list_line_elements:

                line_elements = list_line_elements[0]
                self.elements_from_gmsh_lines[tag] = [self.map_elements[element] for element in line_elements]

            line_nodes, _coords, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            self.nodes_from_gmsh_lines[tag] = [self.map_nodes[node] for node in line_nodes]

        # dt = time() - t0
        # print(f"Time to process : {dt}")

    def _concatenate_line_elements(self):
        """
        """
        self.elements_from_line.clear()
        elements_to_ignore_on_acoustic_analysis = list()
        for tag, line_elements in self.elements_from_gmsh_lines.items():
            line_id = self.lines_mapping[tag]
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
        for node_id, elements in self.project.model.preprocessor.structural_elements_connected_to_node.items():
            for element in elements:

                line_id = self.line_from_element[element.index]
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
        self.length_unit = "meter"

    def get_geometry_statistics(self):
        return len(self.geometry_points), len(self.lines_from_model)