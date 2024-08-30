
from pulse.model.line import Line
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

import os
import gmsh 
import numpy as np

from collections import defaultdict

window_title_1 = "Error"

class Mesh:
    def __init__(self, preprocessor):
        super().__init__()

        self.preprocessor = preprocessor

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
        self.nodes_from_line = defaultdict(list)

        self.elements_from_gmsh_lines = dict()
        self.nodes_from_gmsh_lines = dict()

        self.lines_mapping = dict()

    def set_element_size(self, element_size):
        self.element_size = element_size

    def set_mesher_setup(self, mesh_setup=dict()):
        self.element_size = mesh_setup.get('element size', 0.01)
        self.tolerance = mesh_setup.get('tolerance', 1e-6)
        self.length_unit = mesh_setup.get('length unit', 'meter')
        self.import_type = mesh_setup.get("import type", 1)
        self.geometry_path = mesh_setup.get('geometry path', "")

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
        self._concatenate_line_nodes()

        self._save_geometry_points()
        self._finalize_gmsh()
    
    def _load_cad_geometry_on_gmsh(self):
        """
        This method initializes mesher algorithm gmsh.

        Parameters
        ----------

        """
        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(self.length_unit)
        geometry_handler.open_cad_file(str(self.geometry_path))

    def _create_gmsh_geometry(self):
        """
        This method creates the GMSH geometry based on entity file data.

        Parameters
        ----------

        """

        geometry_handler = GeometryHandler()
        geometry_handler.set_length_unit(self.length_unit) 
        geometry_handler.process_pipeline()
        geometry_handler.create_geometry()

        self.lines_mapping = geometry_handler.lines_mapping

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

            self.preprocessor._create_nodes(node_indexes, coords, self.map_nodes)
            self.preprocessor._create_structural_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)
            self.preprocessor._create_acoustic_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)                       
            self.preprocessor.update_number_divisions()

        except Exception as log_error:

            print(str(log_error))

    def _process_gmsh_lines_mesh_data(self):
        """
        This method maps entities to elements.

        """
        # t0 = time()

        self.elements_from_gmsh_lines.clear()
        self.nodes_from_gmsh_lines.clear()

        for dim, tag in gmsh.model.getEntities(1):

            _, list_line_elements, _ = gmsh.model.mesh.getElements(dim, tag)
            if list_line_elements:

                line_elements = list_line_elements[0]
                self.elements_from_gmsh_lines[tag] = [self.map_elements[element] for element in line_elements]

            line_nodes, _, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            self.nodes_from_gmsh_lines[tag] = [self.map_nodes[node] for node in line_nodes]

        # dt = time() - t0
        # print(f"Time to process : {dt}")

    def _concatenate_line_elements(self):

        """
        """
        print(self.lines_mapping)
        
        self.elements_from_line.clear()
        self.line_from_element.clear()
        
        for tag, line_elements in self.elements_from_gmsh_lines.items():
            line_id = self.lines_mapping[tag]
            self.elements_from_line[line_id].extend(line_elements)

        for _line_id, element_ids in self.elements_from_line.items():
            for element_id in element_ids:
                self.line_from_element[element_id] = _line_id

        self.lines_from_model = list(self.elements_from_line.keys())

    def _concatenate_line_nodes(self):

        self.nodes_from_line.clear()

        for tag, line_nodes in self.nodes_from_gmsh_lines.items():
            line_id = self.lines_mapping[tag]
            self.nodes_from_line[line_id].extend(line_nodes)

        # for tag, nodes in self.nodes_from_line.items():
        #     print(tag, nodes)

    def _save_geometry_points(self):
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