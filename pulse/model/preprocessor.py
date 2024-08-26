from pulse.model.cross_section import *
from pulse.model.line import Line
# from pulse.model.geometry import Geometry
# from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.model.node import Node, DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.model.acoustic_element import AcousticElement, NODES_PER_ELEMENT
from pulse.model.structural_element import StructuralElement, NODES_PER_ELEMENT
from pulse.model.compressor_model import CompressorModel
from pulse.model.perforated_plate import PerforatedPlate

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

from pulse.model.mesh import Mesh

import numpy as np
from time import time
from collections import defaultdict, deque
from scipy.spatial.transform import Rotation

window_title_1 = "Error"

class Preprocessor:
    """A preprocessor class.
    This class creates a acoustic and structural preprocessor object.
    """
    def __init__(self):

        # self.project = project
        self.mesh = None

        self.reset_variables()

    def reset_variables(self):
        """
        This method reset the class default values.
        """

        self.DOFS_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT

        self.nodes = dict()
        self.line_to_nodes = dict()

        self.structural_elements = dict()
        self.acoustic_elements = dict()

        self.connectivity_matrix = list()
        self.nodal_coordinates_matrix = list()

        self.neighbors = defaultdict(list)
        self.elements_connected_to_node = defaultdict(list)

        self.number_structural_elements = 0
        self.number_acoustic_elements = 0

        self.transformation_matrices = None
        self.section_rotations_xyz = None

        self.dict_element_info_to_update_indexes_in_entity_file = dict()
        self.dict_element_info_to_update_indexes_in_element_info_file = dict()
        self.dict_list_elements_to_subgroups = dict()

        self.element_type = "pipe_1" # defined as default
        self.flag_fluid_mass_effect = False
        self.stress_stiffening_enabled = False
        self.group_index = 0

        self.structure_principal_diagonal = None
        self.nodal_coordinates_matrix_external = None

        self.beam_gdofs = None
        self.pipe_gdofs = None
        self.unprescribed_pipe_indexes = None
        self.stop_processing = False

    def set_mesh(self, mesh: Mesh):
        self.mesh = mesh

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
        self.mesh.generate()

        # self._map_lines_to_elements()
        self._map_lines_to_nodes()

        # t0 = time()
        self._load_neighbors()
        # dt = time() - t0
        # print(f"Time to process _load_neighbors: {dt}")

        # t0 = time()
        self._order_global_indexes()
        self._mapping_nodes_indexes()
        # dt = time() - t0
        # print(f"Time to process _order_global_indexes: {dt}")

        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        self.get_dict_nodes_to_element_indexes()
        self.get_principal_diagonal_structure_parallelepiped()

        # t0 = time()
        self.process_all_rotation_matrices()
        # dt = time() - t0
        # print("Time to process all rotations matrices: ", dt)

    def _create_nodes(self, indexes, coords, map_nodes):
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
        self.map_nodes = map_nodes
        self.nodes.clear()
        for i, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[map_nodes[i]] = Node(x, y, z, external_index=int(map_nodes[i]))
        self.number_nodes = len(self.nodes)

    def _create_structural_elements(self, indexes, connectivities, map_nodes, map_elements):
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
        self.map_elements = map_elements
        self.structural_elements.clear()
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.structural_elements[map_elements[i]] = StructuralElement(first_node, last_node, map_elements[i])
            self.number_structural_elements = len(self.structural_elements)

    def _create_acoustic_elements(self, indexes, connectivities, map_nodes, map_elements):
        """
        This method generate the mesh acoustic elements.

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
        self.map_elements = map_elements
        self.acoustic_elements.clear()
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.acoustic_elements[map_elements[i]] = AcousticElement(first_node, last_node, map_elements[i])
            self.number_acoustic_elements = len(self.acoustic_elements)

    def _map_lines_to_nodes(self):
        """
        This method maps entities to nodes.
        """
        # t0 = time()
        self.line_to_nodes = dict()
        for line_ID, list_elements in self.mesh.line_to_elements.items():
            list_nodes = np.zeros(len(list_elements)+1, dtype=int)
            for i, _id in enumerate(list_elements):
                element = self.structural_elements[_id]
                first_node_id = element.first_node.external_index
                last_node_id = element.last_node.external_index
                if i==0:
                    list_nodes[i] = first_node_id
                list_nodes[i+1] = last_node_id
            self.line_to_nodes[line_ID] = np.sort(list_nodes)              
        # dt = time() - t0
        # print(f"Time to process : {dt}")

    def get_model_statistics(self):
        return len(self.nodes), len(self.acoustic_elements), len(self.structural_elements)

    def _create_dict_gdofs_to_external_indexes(self):
        # t0 = time()
        self.dict_gdofs_to_external_indexes = {}
        for external_index, node in self.nodes.items():
            for gdof in node.global_dof:
                self.dict_gdofs_to_external_indexes[gdof] = external_index
        # dt = time()-t0
        # print(len(self.dict_gdofs_to_external_indexes))
        # print("Time to process: ", dt)

    def get_line_length(self, line_id: int):
        """
        This method returns the length of a given line ID.

        Parameters
        ----------
        line_id : int
        
        """
        first_element_ID = self.mesh.line_to_elements[line_id][0]
        last_element_ID = self.mesh.line_to_elements[line_id][-1]

        node1_first_element = self.structural_elements[first_element_ID].first_node
        node2_first_element = self.structural_elements[first_element_ID].last_node

        node3_last_element = self.structural_elements[last_element_ID].first_node
        node4_last_element = self.structural_elements[last_element_ID].last_node

        list_nodes = [  node1_first_element, node2_first_element, 
                        node3_last_element, node4_last_element  ]

        length = 0
        for index in range(1, len(list_nodes)):
            length_i = np.linalg.norm(list_nodes[0].coordinates - list_nodes[index].coordinates)
            if length_i > length:
                length = length_i
                _node = list_nodes[index]
        edge_nodes = [list_nodes[0], _node]
        return length, edge_nodes

    def get_lines_vertex_coordinates(self, _array=True):
        """
        This method returns a dictionary containing line IDs as keys and its vertex node coordinates as values.
        """
        dict_line_to_vertex_coords = defaultdict(list)
        if self.line_to_nodes:
            for line_id in self.mesh.lines_from_model.keys():
                _, vertex_nodes = self.get_line_length(line_id)
                for vertex_node in vertex_nodes:
                    if _array:
                        dict_line_to_vertex_coords[line_id].append(vertex_node.coordinates)
                    else:
                        dict_line_to_vertex_coords[line_id].append(list(vertex_node.coordinates))         
        return dict_line_to_vertex_coords

    def _load_neighbors(self):
        """
        This method updates the structural elements neighbors dictionary. The dictionary's keys and values are nodes objects.
        """
        self.neighbors.clear()
        self.elements_connected_to_node.clear()
        for element in self.structural_elements.values():
            self.neighbors[element.first_node].append(element.last_node)
            self.neighbors[element.last_node].append(element.first_node)
            self.elements_connected_to_node[element.first_node].append(element)
            self.elements_connected_to_node[element.last_node].append(element)

    def update_number_divisions(self):
        """
        This method updates the number of divisions of pipe and circular beam cross-sections based on model size. This adds some
        compensation for the computational effort spent to render vtk actors in models with millions of degrees of freedom.
        """
        if self.number_structural_elements <= 1e3:
            self.section_number_of_divisions = 36 
        if self.number_structural_elements <= 5e3:
            self.section_number_of_divisions = 24        
        elif self.number_structural_elements <= 1e4:
            self.section_number_of_divisions = 16
        elif self.number_structural_elements <= 5e4:
            self.section_number_of_divisions = 10
        elif self.number_structural_elements <= 2e4:
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
        neighbor_diameters = dict()

        for index, element in self.structural_elements.items():
            first = element.first_node.external_index
            last = element.last_node.external_index
            neighbor_diameters.setdefault(first, [])
            neighbor_diameters.setdefault(last, [])

            outer_diameter = element.cross_section.outer_diameter
            inner_diameter = element.cross_section.inner_diameter

            neighbor_diameters[first].append((index, outer_diameter, inner_diameter))
            neighbor_diameters[last].append((index, outer_diameter, inner_diameter))

        return neighbor_diameters

    def neighbor_elements_diameter_global(self):
        """
        This method maps the elements inner diameters that each node belongs to. The maping is done according to the node global index.

        Returns
        ----------
        Dict
            Inner diameters at a certain node. Giving a node global index, returns a list of diameters.
        """
        neighbor_diameters = dict()
        for index, element in self.acoustic_elements.items():
            first = element.first_node.global_index
            last = element.last_node.global_index
            neighbor_diameters.setdefault(first, [])
            neighbor_diameters.setdefault(last, [])
            outer_diameter = element.cross_section.outer_diameter
            inner_diameter = element.cross_section.inner_diameter
            neighbor_diameters[first].append((index, outer_diameter, inner_diameter))
            neighbor_diameters[last].append((index, outer_diameter, inner_diameter))
        return neighbor_diameters    
    
    def neighboor_elements_of_node(self, node_id: int):
        """
        This method returns the acoustic elements that a node belongs to.

        Parameters
        ----------
        int
            Node external indexes.

        Returns
        ----------
        List
            List of acoustic elements indexes.
        """
        node = self.nodes[node_id]
        neighboor_elements = defaultdict(list) 

        for element in self.acoustic_elements.values():
            first = element.first_node
            last = element.last_node
            if node in [first, last]:
                neighboor_elements[node].append(element)#.index)
        return neighboor_elements[node]

    def check_disconnected_lines(self, tolerance=1e-6):
        """
        This methods shearchs for disconnected lines inside sphere of radius r < (size/2) + tolerance.
        """
        element_size = self.mesh.element_size
        if self.nodal_coordinates_matrix_external is not None:
            coord_matrix = self.nodal_coordinates_matrix_external
            list_node_ids = []
            for node, neigh_nodes in self.neighbors.items():
                if len(neigh_nodes) == 1:
                    coord = node.coordinates
                    diff = np.linalg.norm(coord_matrix[:,1:] - np.array(coord), axis=1)
                    mask = diff < ((element_size / 2) + tolerance)
                    if True in mask:
                        try:
                            external_indexes = coord_matrix[:,0][mask]
                            if len(external_indexes) > 1:
                                for external_index in external_indexes:
                                    if len(self.neighbors[self.nodes[external_index]]) == 1:
                                        list_node_ids.append(int(external_index))
                        except Exception as _log_error:
                            title = "Error while checking mesh at the line edges"
                            message = str(_log_error)
                            PrintMessageInput([window_title_1, title, message])

            if len(list_node_ids)>0:
                title = "Problem detected in connectivity between neighbor nodes"
                message = "At least one disconnected node has been detected at the edge of one line due "
                message += "to the mismatch between the geometry 'keypoints' and the current mesh setup. " 
                message += "We strongly recommend reducing the element size or correcting the problem "
                message += "in the geometry file before proceeding with the model setup.\n\n"
                message += f"List of disconnected node(s): \n{list_node_ids}"
                PrintMessageInput([window_title_2, title, message])                
        
    def get_line_from_node_id(self, node_ids):

        if isinstance(node_ids, int):
            node_ids = [node_ids]
        
        line_ids = list()
        for node_id in node_ids:

            if node_id in self.dict_first_node_to_element_index.keys():
                element_id = self.dict_first_node_to_element_index[node_id]
                for _id in element_id:
                    line_id = self.mesh.elements_to_line[_id]
                    if line_id not in line_ids:
                        line_ids.append(line_id)
            
            if node_id in self.dict_last_node_to_element_index.keys():
                element_id = self.dict_last_node_to_element_index[node_id]
                for _id in element_id:
                    line_id = self.mesh.elements_to_line[_id]
                    if line_id not in line_ids:
                        line_ids.append(line_id)

        return line_ids
         
    def _order_global_indexes(self):
        """
        This method updates the nodes global indexes numbering.
        """
        # t0 = time()
        index = 0
        stack = deque()
        list_nodes = list(self.nodes.values())
        old_version = False

        if old_version:

            stack.appendleft(list_nodes[0])

            while stack:

                top = stack.pop()

                if top in list_nodes:
                    list_nodes.remove(top)

                if top.global_index is None:
                    # list_nodes.remove(top)
                    top.global_index = index
                    index += 1
                else:
                    continue
                
                for neighbor in self.neighbors[top]:
                    if neighbor.global_index is None:
                        stack.appendleft(neighbor)
                
                if len(stack) == 0:
                    if len(list_nodes) > 0:
                        stack.appendleft(list_nodes[0])
                        
                        #TODO: uncomment to rebegin from start or end nodes
                        # for node in list_nodes:
                        #     if len(self.neighbors[node]) == 1:
                        #         stack.appendleft(node)
        else:

            stack.appendleft(list_nodes[0].external_index) 

            while stack:
            
                top = self.nodes[stack.pop()]
        
                if top.global_index is None:
                    top.global_index = index
                    index += 1
                else:
                    continue
                
                for neighbor in self.neighbors[top]:
                    if neighbor.global_index is None:
                        if neighbor.external_index not in stack:
                            stack.appendleft(neighbor.external_index)
                        
                if len(stack) == 0:
                    if index < self.number_nodes-1:
                        for node in list_nodes:
                            if node.global_index is None:
                                stack.appendleft(node.external_index)
                                break
                        
                        #TODO: uncomment to begin from start or end nodes
                        # for node in list_nodes:
                        #     if len(self.neighbors[node]) == 1:
                        #         stack.appendleft(node)   

    def _mapping_nodes_indexes(self):
        self.map_global_to_external_index = {node.global_index:node.external_index for node in self.nodes.values()}

    def get_dict_nodes_to_element_indexes(self):
        """
        This method updates the dictionary that maps the external node to the element index.
        """
        self.dict_first_node_to_element_index = defaultdict(list)
        self.dict_last_node_to_element_index = defaultdict(list)
        for index, element in self.structural_elements.items():
            first_node_index = element.first_node.external_index
            last_node_index = element.last_node.external_index
            self.dict_first_node_to_element_index[first_node_index].append(index)
            self.dict_last_node_to_element_index[last_node_index].append(index)

    def get_nodal_coordinates_matrix(self, reordering=True):
        """
        This method updates the mesh nodes coordinates data. Coordinates matrix row structure:
        ''[Node index, x-coordinate, y-coordinate, z-coordinate]''.

        Parameters
        ----------
        reordering : bool, optional.
            True if the nodes numbering is according to the global indexing. False otherwise.
            Default is True.
        """
        # self.number_nodes = len(self.nodes)
        nodal_coordinates = np.zeros((self.number_nodes, 4))
        nodal_coordinates_external = nodal_coordinates

        # if reordering:
        for external_index, node in self.nodes.items():
            index = self.nodes[external_index].global_index
            nodal_coordinates[index,:] = index, node.x, node.y, node.z
            nodal_coordinates_external[index,:] = external_index, node.x, node.y, node.z
        # else:               
        #     for external_index, node in self.nodes.items():
        #         index = self.nodes[external_index].global_index
        #         nodal_coordinates[index,:] = external_index, node.x, node.y, node.z

        self.nodal_coordinates_matrix = nodal_coordinates
        self.nodal_coordinates_matrix_external = nodal_coordinates_external

    def get_connectivity_matrix(self, reordering=True):
        """
        This method updates the mesh connectivity data. Connectivity matrix row structure:
        ''[Element index, first node index, last node index]''.

        Parameters
        ----------
        reordering : bool, optional.
            True if the nodes numbering is according to the global indexing. False otherwise.
            Default is True.
        """
        connectivity = np.zeros((self.number_structural_elements, NODES_PER_ELEMENT+1))
        if reordering:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.global_index
                last  = element.last_node.global_index
                first_external = element.first_node.external_index
                last_external  = element.last_node.external_index
                connectivity[index,:] = index+1, first, last
        else:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.external_index
                last  = element.last_node.external_index
                connectivity[index,:] = index+1, first, last

        self.connectivity_matrix = connectivity.astype(int) 

    def get_node_id_by_coordinates(self, coords, radius=None):
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

        coord_matrix = self.nodal_coordinates_matrix_external
        list_coordinates = coord_matrix[:,1:].tolist()
        external_indexes = coord_matrix[:,0]

        if isinstance(coords, (np.ndarray, tuple)):
            coords = list(coords)

        if radius is None:
            radius = self.mesh.element_size / 20

        if coords in list_coordinates:
            ind = list_coordinates.index(coords)
            external_index = int(external_indexes[ind])
        else:
            diff = np.linalg.norm(coord_matrix[:,1:] - np.array(coords), axis=1)
            mask = diff < radius
            try:
                external_index = int(external_indexes[mask])
            except:
                return None
        
        return external_index

    def get_element_center_coordinates_matrix(self):
        """
        This method updates the center coordinates matrix attribute. 
        
        Element center coordinates matrix row structure:

        [Element index, x-element_center_coordinate, y-element_center_coordinate, z-element_center_coordinate].

        """
        self.center_coordinates_matrix = np.zeros((len(self.structural_elements), 4))
        for index, element in self.structural_elements.items():
            self.center_coordinates_matrix[index-1, 0] = index
            self.center_coordinates_matrix[index-1, 1:] = element.element_center_coordinates

    def get_principal_diagonal_structure_parallelepiped(self):
        """
        This method updates the principal structure diagonal parallelepiped attribute. 
        
        """
        nodal_coordinates = self.nodal_coordinates_matrix.copy()
        x_min, y_min, z_min = np.min(nodal_coordinates[:,1:], axis=0)
        x_max, y_max, z_max = np.max(nodal_coordinates[:,1:], axis=0)
        self.structure_principal_diagonal = np.sqrt((x_max-x_min)**2 + (y_max-y_min)**2 + (z_max-z_min)**2)
        self.camera_rotation_center = [ (x_max + x_min)/2,
                                        (y_max + y_min)/2,
                                        (z_max + z_min)/2 ]
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
        # Process the I and J indexes vector for assembly process
        rows, cols = self.number_structural_elements, DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)*DOF_PER_NODE_STRUCTURAL + np.arange(6, dtype=int)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()
    
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
        rows, cols = len(self.acoustic_elements), DOF_PER_NODE_ACOUSTIC*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()

    def map_structural_to_acoustic_elements(self):
        self.dict_structural_to_acoustic_elements = {}
        for key, element in self.structural_elements.items():
            self.dict_structural_to_acoustic_elements[element] = self.acoustic_elements[key]
        return self.dict_structural_to_acoustic_elements 

    def get_neighbor_nodes_and_elements_by_node(self, node_id, length, tolerance=1e-6):
        """ This method returns two lists of nodes ids and elements ids at the neighborhood of the 
            node_id in the range of -(length/2) - tolerance and (length/2) + tolerance. The tolerance 
            avoids the problem of element size deviations resultant in the mesh generation algorithm.
        
        Parameters
        ----------

        Returns
        ---------- 

        """ 
        half_length = (length/2) + tolerance
        node_central = self.nodes[node_id]
        list_nodes_ids = [node_id]
        stack = deque()
        stack.appendleft(node_id)

        while stack:
            nodes = self.neighbors[self.nodes[stack.pop()]]
            if len(nodes) <= 2:
                for node in nodes:
                    if np.linalg.norm((node_central.coordinates - node.coordinates)) <= half_length:
                        if node.external_index not in list_nodes_ids:
                            list_nodes_ids.append(node.external_index)
                            stack.appendleft(node.external_index)                    
            else:
                return None, None

        list_elements_ids = []
        for element in self.structural_elements.values():
            if element.first_node.external_index in list_nodes_ids:
                if element.last_node.external_index in list_nodes_ids:
                    list_elements_ids.append(element.index)
            if len(list_elements_ids) == len(list_nodes_ids) - 1:
                break

        return list_nodes_ids, list_elements_ids

    def get_neighbor_nodes_and_elements_by_element(self, element_id, length, tolerance=1e-5):
        """ This method returns two lists of nodes ids and elements ids at the neighborhood of the 
            element_id in the range of -(length/2) - tolerance and (length/2) + tolerance. The tolerance 
            avoids the problem of element size deviations resultant in the mesh generation algorithm.

        Parameters
        ---------- 

        Returns
        ---------- 
                               
        """         
        node_id = self.structural_elements[element_id].first_node.external_index
        last_node = self.structural_elements[element_id].last_node
        
        length_t = length + (self.structural_elements[element_id].length)
        list_nodes_ids, list_elements_ids = self.get_neighbor_nodes_and_elements_by_node(node_id, length_t, tolerance=tolerance)

        if list_nodes_ids is not None:
                
            for external_index in list_nodes_ids:
                node = self.nodes[external_index]
                if np.linalg.norm((last_node.coordinates - node.coordinates)) > ((length_t/2) + tolerance):
                    list_nodes_ids.remove(node.external_index)

            for index in list_elements_ids:
                element = self.structural_elements[index]
                if element.first_node.external_index not in list_nodes_ids:
                    if element.index in list_elements_ids:
                        list_elements_ids.remove(element.index)
                        
                if element.last_node.external_index not in list_nodes_ids:
                    if element.index in list_elements_ids: 
                        list_elements_ids.remove(element.index)
                        
            return list_nodes_ids, list_elements_ids
        else:
            return None, None

    def _reset_global_indexes(self):
        """
        This method attributes None to global index of all mesh nodes.
        """
        for node in self.nodes.values():
            node.global_index = None

    def set_structural_element_type_by_element(self, elements, element_type):
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
        for element in slicer(self.structural_elements, elements):
            element.element_type = element_type
    
    def set_structural_element_force_offset_by_elements(self, elements, force_offset, remove=False):
        """
        This method assigns a structural element wall formulation to a list of selected elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        force_offset : int, [0, 1]
            Structural element type to be attributed to the listed elements.
            
        remove : bool, optional
            True if the element_force_offset should to be removed from the _________ dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.structural_elements, elements):
            element.force_offset = bool(force_offset)
        #TODO: check if it is necessary
        # if remove:
        #     return
            # self.dict_structural_element_force_offset_to_lines.pop(force_offset)

    def set_structural_element_wall_formulation_by_elements(self, elements, wall_formulation, remove=False):
        """
        This method assigns a structural element wall formulation to a list of selected elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        wall_formulation : str, ['thick_wall', 'thin_wall']
            Structural element type to be attributed to the listed elements.
            
        remove : bool, optional
            True if the element_wall_formulation should to be removed from the _________ dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.structural_elements, elements):
            element.wall_formulation = wall_formulation
        #TODO: check if it is necessary
        # if remove:
        #     return
            # self.dict_structural_element_wall_formulation_to_lines.pop(wall_formulation)

    def set_acoustic_element_type_by_element(self, elements, element_type, proportional_damping=None, vol_flow=None, remove=False):
        """
        This method attributes acoustic element type to a list of elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        element_type : str, ['undamped', 'proportional', 'wide-duct', 'LRF fluid equivalent', 'LRF full']
            Acoustic element type to be attributed to the listed elements.
            
        proportional_damping : float, optional
            Acoustic proportional damping coefficient. It must be attributed to the elements of type 'proportional'.
            Default is None.
            
        remove : bool, optional
            True if the element_type have to be removed from the acoustic element type dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.acoustic_elements, elements):
            element.element_type = element_type
            element.proportional_damping = proportional_damping
            element.vol_flow = vol_flow

    def set_cross_section_by_elements(  self, 
                                        elements, 
                                        cross_section, 
                                        update_cross_section = False, 
                                        update_section_points = True, 
                                        variable_section = False  ):
        """
        This method attributes cross section object to a list of acoustic and structural elements.

        Parameters
        ----------
        elements : list
            Acoustic and structural elements indexes.
            
        cross_section : Cross section object
            Tube cross section data.
            
        update_cross_section : bool, optional
            True if the cross section data have to be evaluated or updated. False otherwise.
            Default is False.
        """
        if cross_section is None:
            return

        if isinstance(cross_section, CrossSection) and update_cross_section:
            cross_section.update_properties()

        if isinstance(cross_section, list):
            for i, element in enumerate(elements):

                _element = [element]
                _cross_section = cross_section[i]

                for element in slicer(self.structural_elements, _element):
                    element.cross_section = _cross_section
                    element.variable_section = variable_section
                    element.section_parameters_render = _cross_section.section_parameters

                for element in slicer(self.acoustic_elements, _element):
                    element.cross_section = _cross_section

        else:    

            for element in slicer(self.structural_elements, elements):
                element.cross_section = cross_section
                element.variable_section = variable_section
                element.section_parameters_render = cross_section.section_parameters

            for element in slicer(self.acoustic_elements, elements):
                element.cross_section = cross_section
    
        # if update_section_points:

        #     N = self.section_number_of_divisions
        #     if isinstance(cross_section, list):
        #         for i, element in enumerate(elements):

        #             _element = [element]
        #             _cross_section = cross_section[i]
        #             _cross_section: CrossSection

        #             _cross_section_points = _cross_section.get_cross_section_points(N)
        #             for element in slicer(self.structural_elements, _element):
        #                 element.cross_section_points = _cross_section_points

        #             for element in slicer(self.acoustic_elements, _element):
        #                 element.cross_section_points = _cross_section_points

        #     else:

        #         cross_section_points = cross_section.get_cross_section_points(N)
        #         for element in slicer(self.structural_elements, elements):
        #             element.cross_section_points = cross_section_points

        #         for element in slicer(self.acoustic_elements, elements):
        #             element.cross_section_points = cross_section_points

    def set_cross_section_by_lines(self, lines, cross_section):
        """
        This method attributes cross section object to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        cross_section : Cross section object
            Tube cross section data.
        """
        for elements in slicer(self.mesh.line_to_elements, lines):
            self.set_cross_section_by_elements(elements, cross_section)
    
    def set_variable_cross_section_by_line(self, line_id, section_data: dict):
        """
        This method sets the variable section info by line selection.
        """
        if isinstance(section_data, dict):

            [   outer_diameter_initial, thickness_initial, offset_y_initial, offset_z_initial,
                outer_diameter_final, thickness_final, offset_y_final, offset_z_final,
                insulation_thickness, insulation_density  ] = section_data["section_parameters"]

            elements_from_line = self.mesh.line_to_elements[line_id]
            self.add_expansion_joint_by_lines(line_id, None, remove=True)

            first_element = self.structural_elements[elements_from_line[0]]
            last_element = self.structural_elements[elements_from_line[-1]]
            
            coord_first_1 = first_element.first_node.coordinates
            coord_last_1 = last_element.last_node.coordinates
            
            coord_first_2 = last_element.first_node.coordinates
            coord_last_2 = first_element.last_node.coordinates
            
            lines_vertex_coords = self.get_lines_vertex_coordinates(_array=False)
            vertex_coords = lines_vertex_coords[line_id]

            N = len(elements_from_line)
            if list(coord_first_1) in vertex_coords and list(coord_last_1) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_initial, outer_diameter_final, N)
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_initial, thickness_final, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_initial, offset_y_final, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_initial, offset_z_final, N)

            elif list(coord_first_2) in vertex_coords and list(coord_last_2) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_final, outer_diameter_initial, N)
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_final, thickness_initial, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_final, offset_y_initial, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_final, offset_z_initial, N)
            
            cross_sections_first = list()
            cross_sections_last = list()
            for index, element_id in enumerate(elements_from_line):
                
                element = self.structural_elements[element_id]
                first_node = element.first_node
                last_node = element.last_node
                
                section_parameters_first = [outer_diameter_first[index],
                                            thickness_first[index],
                                            offset_y_first[index],
                                            offset_z_first[index],
                                            insulation_thickness,
                                            insulation_density]
                
                pipe_section_info_first = { "section_type_label" : "Reducer" ,
                                            "section_parameters" : section_parameters_first }

                section_parameters_last = [outer_diameter_last[index],
                                            thickness_last[index],
                                            offset_y_last[index],
                                            offset_z_last[index],
                                            insulation_thickness,
                                            insulation_density]
                
                pipe_section_info_last = { "section_type_label" : "Reducer" ,
                                            "section_parameters" : section_parameters_last }

                cross_section_first = CrossSection(pipe_section_info = pipe_section_info_first)
                cross_section_last = CrossSection(pipe_section_info = pipe_section_info_last)

                cross_sections_first.append(cross_section_first)
                # cross_sections_last.append(cross_section_last)

                first_node.cross_section = cross_section_first
                last_node.cross_section = cross_section_last

            self.set_cross_section_by_elements( elements_from_line,
                                                cross_sections_first,
                                                variable_section = True )

    # def set_cross_section_plot_info_by_element(self, elements, cross_section):
    #     """
    #     This method attributes cross section object to a list of acoustic and structural elements.

    #     Parameters
    #     ----------
    #     elements : list
    #         Acoustic and structural elements indexes.
            
    #     cross_section : Cross section object
    #         Tube cross section data.
            
    #     update_cross_section : bool, optional
    #         True if the cross section data have to be evaluated or updated. False otherwise.
    #         Default is False.
    #     """

    #     if isinstance(cross_section, list):
    #         for i, element in enumerate(elements):
    #             _cross_section = cross_section[i]
    #             _element = [element]
    #             for element in slicer(self.structural_elements, _element):
    #                 element.cross_section_plot_info = _cross_section
    #             for element in slicer(self.acoustic_elements, _element):
    #                 element.cross_section_plot_info = _cross_section
    #     else:    
    #         for element in slicer(self.structural_elements, elements):
    #             element.cross_section_plot_info = cross_section
    #         for element in slicer(self.acoustic_elements, elements):
    #             element.cross_section_plot_info = cross_section

    # def set_cross_section_plot_info_by_line(self, lines, cross_section):
    #     """
    #     This method attributes cross section plot info object to all elements that belongs to a line/entity.

    #     Parameters
    #     ----------
    #     line : list
    #         Entities tag.
            
    #     cross_section : Cross section plot info object
    #         Tube cross section data.
    #     """
    #     for elements in slicer(self.mesh.line_to_elements, lines):
    #         self.set_cross_section_plot_info_by_element(elements, cross_section)

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

        for elements in slicer(self.mesh.line_to_elements, line_ids):
            self.set_structural_element_type_by_element(elements, element_type)

    def set_acoustic_element_type_by_lines( 
                                            self, 
                                            line_ids: (int | list | tuple), 
                                            element_type: str, 
                                            proportional_damping = None, 
                                            vol_flow = None, 
                                           ):
        """
        This method attributes acoustic element type to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        element_type : str, ['undamped', 'proportional', 'wide-duct', 'LRF fluid equivalent', 'LRF full']
            Acoustic element type to be attributed to the listed elements.
            
        proportional_damping : float, optional
            Acoustic proportional damping coefficient. It must be attributed to the elements of type 'proportional'.
            Default is None.

        """

        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.line_to_elements, line_ids):
            self.set_acoustic_element_type_by_element(  elements, 
                                                        element_type, 
                                                        proportional_damping = proportional_damping, 
                                                        vol_flow = vol_flow  )

    # Structural physical quantities
    def set_material_by_element(self, elements, material):
        """
        This method attributes material object to a list of acoustic and structural elements.

        Parameters
        ----------
        elements : list
            Acoustic and structural elements indexes.
            
        material : Material object
            Material data.
        """
        for element in slicer(self.structural_elements, elements):
            element.material = material
        for element in slicer(self.acoustic_elements, elements):
            element.material = material

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

        for elements in slicer(self.mesh.line_to_elements, line_ids):
            self.set_material_by_element(elements, material)

    def set_force_by_element(self, elements, loads):
        for element in slicer(self.structural_elements, elements):
            element.loaded_forces = loads

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
        DOFS_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
        N = DOF_PER_NODE_STRUCTURAL
        mat_ones = np.ones((DOFS_PER_ELEMENT,DOFS_PER_ELEMENT), dtype=int)

        node_id = data["T-joint_node"]
        decoupled_rotations = data["decoupled_rotations"]


        neighboor_elements = self.neighboor_elements_of_node(node_id)
        if len(neighboor_elements) < 3:
            return mat_ones
        
        mat_base = np.array([[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
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
                             [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0]]  )
        
        node = self.nodes[node_id]
        element = self.structural_elements[element_id]
        
        if decoupled_rotations.count(False) == 3:
            mat_out = mat_ones

        elif decoupled_rotations.count(True) == 3:  
            mat_out = mat_base

        elif node in [element.first_node]:
  
            temp = mat_base[:int(N/2), :int(N/2)].copy()
            mat_base[:N,:N] = np.zeros((N,N), dtype=int)
            mat_base[:int(N/2), :int(N/2)] = temp

            for index, value in enumerate(decoupled_rotations):
                if not value:
                    ij = index + int(N/2)
                    mat_base[:, [ij, ij+N]] = np.ones((DOFS_PER_ELEMENT, 2), dtype=int)
                    mat_base[[ij, ij+N], :] = np.ones((2, DOFS_PER_ELEMENT), dtype=int) 
            mat_out = mat_base

        elif node in [element.last_node]:
   
            temp = mat_base[N:int(3*N/2), N:int(3*N/2)].copy()
            mat_base[N:,N:] = np.zeros((N,N), dtype=int)
            mat_base[N:int(3*N/2), N:int(3*N/2)] = temp

            for index, value in enumerate(decoupled_rotations):
                if not value:
                    ij = index + int(3*N/2)
                    mat_base[:, [ij-N, ij]] = np.ones((DOFS_PER_ELEMENT, 2), dtype=int)
                    mat_base[[ij-N, ij], :] = np.ones((2, DOFS_PER_ELEMENT), dtype=int) 
            mat_out = mat_base

        element.decoupling_matrix = mat_out
        element.decoupling_info = [element_id, node_id, decoupled_rotations]
                
        return mat_out  

    def enable_fluid_mass_adding_effect(self, reset=False):
        """
        This method enables or disables the addition of fluid mass in the structural element mass.

        Parameters
        ----------            
        reset : bool, optional
            True if the fluid mass effect have to be disable. False to enable.
            Default is False.
        """
        flag = self.flag_fluid_mass_effect
        
        if reset and flag:
            self.flag_fluid_mass_effect = False
            for element in self.structural_elements.values():
                element.adding_mass_effect = False
        elif not reset:
            self.flag_fluid_mass_effect = True
            for element in self.structural_elements.values():
                element.adding_mass_effect = True

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
        for element in slicer(self.structural_elements, elements):
            element.capped_end = value

    # def set_capped_end_line_to_element(self, lines, value):
    #     for elements in slicer(self.mesh.line_to_elements, lines):
    #         for element in slicer(self.structural_elements, elements):
    #             element.capped_end = value
 
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
        # self.set_capped_end_line_to_element(line_ids, value)
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for elements in slicer(self.mesh.line_to_elements, line_ids):
            for element in slicer(self.structural_elements, elements):
                element.capped_end = value

    def set_structural_element_wall_formulation_by_lines(self, lines, formulation):
        """
        This method assign a strutural element wall formulation to the selected lines.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        wall_formulation : str, ['thick_wall', 'thin_wall']
            Structural element type to be attributed to the listed elements. 
        """
        try:
            if isinstance(lines, int):
                lines = [lines]

            for elements in slicer(self.mesh.line_to_elements, lines):
                for element in slicer(self.structural_elements, elements):
                    element.wall_formulation = formulation

        except Exception as _error:
            print(str(_error))

    def set_structural_element_force_offset_by_lines(self, lines, force_offset):
        """
        This method assign a strutural element force offset to the selected lines.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        force offset : int, [0, 1]
            Structural element force offset to be attributed to the listed elements. 
        """
        try:
            if isinstance(lines, int):
                lines = [lines]

            for elements in slicer(self.mesh.line_to_elements, lines):
                for element in slicer(self.structural_elements, elements):
                    element.force_offset = bool(force_offset)

        except Exception as _error:
            print(str(_error))

    def modify_stress_stiffening_effect(self, _bool):
        self.stress_stiffening_enabled = _bool

    def set_stress_stiffening_by_lines(self, lines: int | list, pressures: list | tuple):
        """
        This method .

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        parameters : list
            ????????.
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(lines, int):
            lines = [lines]
        for elements in slicer(self.mesh.line_to_elements, lines):
            self.set_stress_stiffening_by_elements(elements, pressures)

    def set_stress_stiffening_by_elements(self, elements, data: dict):
        """
        This method .

        Parameters
        ----------
        lines : list
            Elements indexes.

        parameters : list
            ????????.

        section : ?????
            ??????
            Default is None
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """

        self.modify_stress_stiffening_effect(True)

        for element in slicer(self.structural_elements, elements):
            element.external_pressure = data["external_pressure"]
            element.internal_pressure = data["internal_pressure"]

    def add_expansion_joint_by_lines(self, line_ids: (int | list), parameters: (None | dict)):
        """
        This method .

        Parameters
        ----------
        line_ids : list
            Lines/entities indexes.

        parameters : list
            ????????.
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for line_id in line_ids:
            for elements in slicer(self.mesh.line_to_elements, line_id):
                for element in slicer(self.structural_elements, elements):
                    element.set_expansion_joint_data(parameters)


    def add_valve_by_lines(self, line_ids: (int | list), valve_data: dict):
        """
        This method .

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        valve_data : list
            ????????.
            
        remove : bool, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(line_ids, int):
            line_ids = [line_ids]

        for line_id in line_ids:
            for elements in slicer(self.mesh.line_to_elements, line_id):
                for element in slicer(self.structural_elements, elements):
                    element.valve_valve_data = valve_data


    def set_stress_intensification_by_line(self, line_ids: (int | list), value: bool):
        """
        This method enables or disables the stress intensification effect to all structural elements that belongs to a line.

        Parameters
        ----------
        line_ids : list
            Lines/entities indexes.
            
        value : bool
            True if the stress intensification effect have to be activated. False otherwise.
        """
        for elements in slicer(self.mesh.line_to_elements, line_ids):
            for element in slicer(self.structural_elements, elements):
                element.stress_intensification = value


    # Acoustic physical quantities
    def set_fluid_by_element(self, elements, fluid):
        """
        This method attributes fluid object to a list of acoustic elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        fluid : Fluid object
            Fluid data.
        """
        for element in slicer(self.acoustic_elements, elements):
            if 'beam_1' not in self.structural_elements[element.index].element_type:
                element.fluid = fluid
            else:
                element.fluid = None

        for element in slicer(self.structural_elements, elements):
            if element.element_type not in ['beam_1']:
                element.fluid = fluid
            else:
                element.fluid = None
    
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

        for elements in slicer(self.mesh.line_to_elements, line_ids):
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
        for element in slicer(self.acoustic_elements, element_ids):
            element.length_correction_data = data

    def set_vol_flow_by_element(self, elements, vol_flow):
        for element in slicer(self.acoustic_elements, elements):
            if 'beam_1' not in self.structural_elements[element.index].element_type:
                element.vol_flow = vol_flow
            else:
                element.vol_flow = None
    
    def set_vol_flow_by_line(self, lines, vol_flow):
        for elements in slicer(self.mesh.line_to_elements, lines):
            self.set_vol_flow_by_element(elements, vol_flow)

    def set_perforated_plate_by_elements(self, elements: list | tuple, perforated_plate: PerforatedPlate):

        for element in slicer(self.structural_elements, elements):
            element.perforated_plate = perforated_plate

        for element in slicer(self.acoustic_elements, elements):
            element.perforated_plate = perforated_plate
            element.delta_pressure = 0
            element.pp_impedance = None

    def set_beam_xaxis_rotation_by_lines(self, line_ids: (int | list), angle: float, gimball_shift=1e-5):
        """
        """
        # promotes a small angle shift to avoid the gimbal lock rotation problems
        if angle in [90, 270]:
            angle -= gimball_shift
        elif angle in [-90, -270]:
            angle += gimball_shift
        angle *= np.pi/180

        for elements in slicer(self.mesh.line_to_elements, line_ids):
            self.set_beam_xaxis_rotation_by_elements(elements, angle)

    def set_beam_xaxis_rotation_by_elements(self, elements, angle):
        for element in slicer(self.structural_elements, elements):
            element.beam_xaxis_rotation = angle

    # def get_radius(self):
    #     """
    #     This method updates and returns the ????.

    #     Returns
    #     ----------
    #     dictionary
    #         Radius at certain node.
    #     """
    #     self.radius = {}
    #     for element in self.structural_elements.values():
    #         first = element.first_node.global_index
    #         last  = element.last_node.global_index
    #         radius = element.cross_section.external_radius
    #         if self.radius.get(first, -1) == -1:
    #             self.radius[first] = radius
    #         elif self.radius[first] < radius:
    #             self.radius[first] = radius
    #         if self.radius.get(last, -1) == -1:
    #             self.radius[last] = radius
    #         elif self.radius[last] < radius:
    #             self.radius[last] = radius
    #     return self.radius

    def get_pipe_and_expansion_joint_elements_global_dofs(self):
        """
        This method returns the acoustic global degrees of freedom of the nodes associated to structural beam elements. 
        This method helps to exclude those degrees of freedom from acoustic analysis.

        Returns
        ----------
        list
            Acoustic global degrees of freedom associated to beam element.
        """ 
        pipe_gdofs = dict()
        for element in self.structural_elements.values():
            if element.element_type in ['pipe_1', 'expansion_joint', 'valve']:
                gdofs_node_first = element.first_node.global_index
                gdofs_node_last = element.last_node.global_index
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
        self.pipe_and_expansion_joint_gdofs = self.get_pipe_and_expansion_joint_elements_global_dofs()
        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.nodes)
        all_indexes = np.arange(total_dof)
        self.beam_gdofs = np.delete(all_indexes, self.pipe_and_expansion_joint_gdofs)
        return self.beam_gdofs, self.pipe_and_expansion_joint_gdofs

    
    def _process_beam_nodes_and_indexes(self):
        """
        This method ?????.

        Returns
        ----------
        bool
            ?????
        """
        self.beam_gdofs, self.pipe_gdofs = self.get_beam_and_non_beam_elements_global_dofs()
        if len(self.beam_gdofs) == self.number_nodes:
            return True
        else:
            return False
    
    def get_acoustic_elements(self):
        """
        This method returns a list of acoustic elements.

        Returns
        ----------
        list
            Acoustic elements list.
        """
        acoustic_elements = []
        self.map_structural_to_acoustic_elements()
        for element in self.structural_elements.values():
            if element.element_type not in ['beam_1']:
                acoustic_element = self.dict_structural_to_acoustic_elements[element]
                acoustic_elements.append(acoustic_element)
                # if element.element_type == "valve":
                #     print(element.element_type, element.index)
        return acoustic_elements   

    def get_nodes_relative_to_acoustic_elements(self):
        """
        This method returns a dictionary that maps the acoustic node indexes to the acoustic elements.

        Returns
        ----------
        list
            Dictionary of nodes relative to the acoustic elements.
        """
        acoustic_elements = self.get_acoustic_elements()
        acoustic_nodes = {}
        
        for element in acoustic_elements:
            first_node = element.first_node.external_index
            last_node = element.last_node.external_index
            acoustic_nodes[first_node] = element.first_node
            acoustic_nodes[last_node] = element.last_node

        return acoustic_nodes  

    def get_beam_elements(self):
        """
        This method returns a list of structural beam elements objects.

        Returns
        ----------
        list
            Beam elements objects.
        """
        list_elements = []
        for element in self.structural_elements.values():
            if element.element_type in ['beam_1']:
                list_elements.append(element)
        return list_elements

    def add_compressor_excitation(self, parameters):
        """
        This method ???????

        Parameters
        ----------
        ??????
            ???????
        """
        list_parameters = []
        for key, parameter in parameters.items():
            if key != 'cylinder label':
                list_parameters.append(parameter)

        if 'cylinder label' in parameters.keys():
            CompressorModel(list_parameters, active_cyl=parameters['cylinder label'])
        else:
            CompressorModel(list_parameters)

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

        nodes_gdofs = np.array([node_1.global_dof, node_2.global_dof]).flatten()
        reord_gdofs = np.sort(nodes_gdofs)
        if  list(nodes_gdofs) == list(reord_gdofs):
            first_node = node_1
            last_node = node_2
        else:
            first_node = node_2
            last_node = node_1
        return reord_gdofs, first_node, last_node

    def get_nodes_and_elements_with_expansion(self, ratio=10):
        title = "Incomplete model setup"
        message = "Dear user, you should should to apply a cross-setion to all 'pipe_1' elements to proceed."
        self.nodes_with_cross_section_transition = dict()
        for node, neigh_elements in self.elements_connected_to_node.items():
            check_complete = False
            if len(neigh_elements) == 2:

                if neigh_elements[0].element_type == "pipe_1":
                    if neigh_elements[0].cross_section is None:
                        PrintMessageInput([window_title_1, title, message])
                        return
                    else:
                        check_complete = True
                        diameter_first = neigh_elements[0].cross_section.outer_diameter
                        
                if neigh_elements[1].element_type == "pipe_1":
                    if neigh_elements[1].cross_section is None:
                        PrintMessageInput([window_title_1, title, message])
                        return
                    else:
                        check_complete = True
                        diameter_last = neigh_elements[1].cross_section.outer_diameter
                
                if check_complete:
                    diameters = [diameter_first, diameter_last]
                    diameters_ratio = max(diameters)/min(diameters)
                    if diameters_ratio > 2:
                        self.nodes_with_cross_section_transition[node] = neigh_elements
                        # print(node.external_index, diameters_ratio)


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

                pos_data = values
                neg_data = [-value if value is not None else None for value in values]
                # mask = [False if value is None else True for value in values]

                indexes_i = [ gdofs_node1, gdofs_node1, gdofs_node2, gdofs_node2 ] 
                indexes_j = [ gdofs_node1, gdofs_node2, gdofs_node1, gdofs_node2 ] 
                out_data = [ pos_data, neg_data, neg_data, pos_data ]

                indexes_i = np.array(indexes_i, dtype=int).flatten()
                indexes_j = np.array(indexes_j, dtype=int).flatten()
                out_data = np.array(out_data, dtype=float).flatten()

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


    def get_psd_acoustic_link_data(self, node_ids: list):
        """
        """
        if len(node_ids) == 2:

            coords = list()
            
            ext_id1 = min(node_ids) 
            ext_id2 = max(node_ids)

            neigh_elem_node_1 = self.neighboor_elements_of_node(ext_id1)
            neigh_elem_node_2 = self.neighboor_elements_of_node(ext_id2)

            if len(neigh_elem_node_1) == 1:

                element_pipe = neigh_elem_node_1[0]
                d_minor = element_pipe.cross_section.inner_diameter

                element_volume = neigh_elem_node_2[0]
                d_major = element_volume.cross_section.inner_diameter

            elif len(neigh_elem_node_2) == 1:

                element_pipe = neigh_elem_node_2[0]
                d_minor = element_pipe.cross_section.inner_diameter

                element_volume = neigh_elem_node_1[0]
                d_major = element_volume.cross_section.inner_diameter

            else:
                return

            int_id1 = self.nodes[ext_id1].global_index
            int_id2 = self.nodes[ext_id2].global_index

            indexes_i = [ int_id1, int_id2, int_id1, int_id2 ] 
            indexes_j = [ int_id1, int_id1, int_id2, int_id2 ]

            element_pipe.acoustic_link_diameters = [d_minor, d_major]

            coords_1 = self.nodes[ext_id1].coordinates
            coords_2 = self.nodes[ext_id2].coordinates

            coords.append(list(np.round(coords_1, 5)))
            coords.append(list(np.round(coords_2, 5)))

            node_ids = (ext_id1, ext_id2)

            data = {
                    "coords" : coords,
                    "indexes_i" : indexes_i,
                    "indexes_j" : indexes_j,
                    "element_pipe" : element_pipe,
                    "diameters" : [d_minor, d_major]
                    }

            return data


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


    def process_cross_sections_mapping(self):  

        label_etypes = ['pipe_1', 'valve']
        indexes = [0, 1]

        dict_etype_index = dict(zip(label_etypes,indexes))
        dict_index_etype = dict(zip(indexes,label_etypes))
        map_cross_section_to_elements = defaultdict(list)

        for index, element in self.structural_elements.items():

            # if None not in [element.first_node.cross_section, element.last_node.cross_section]:
            #     continue

            if element.variable_section:
                continue

            e_type  = element.element_type
            if e_type in ['beam_1', 'expansion_joint']:
                continue

            elif e_type is None:
                e_type = 'pipe_1'
                self.acoustic_analysis = True
        
            index_etype = dict_etype_index[e_type]

            poisson = element.material.poisson_ratio
            if poisson is None:
                poisson = 0

            outer_diameter = element.cross_section.outer_diameter
            thickness = element.cross_section.thickness
            offset_y = element.cross_section.offset_y
            offset_z = element.cross_section.offset_z
            insulation_thickness = element.cross_section.insulation_thickness
            insulation_density = element.cross_section.insulation_density
           
            map_cross_section_to_elements[str([ outer_diameter, thickness, offset_y, offset_z, poisson,
                                                index_etype, insulation_thickness, insulation_density ])].append(index)
            
            if self.stop_processing:
                return

        for key, elements in map_cross_section_to_elements.items():

            cross_strings = key[1:-1].split(',')
            vals = [float(value) for value in cross_strings]
            el_type = dict_index_etype[vals[5]]

            section_parameters = [vals[0], vals[1], vals[2], vals[3], vals[6], vals[7]]

            if el_type == 'pipe_1':
                pipe_section_info = {   
                                     "section_type_label" : "Pipe",
                                     "section_parameters" : section_parameters
                                    }
                cross_section = CrossSection(pipe_section_info = pipe_section_info)                             

            elif el_type == 'valve':
                valve_section_info = {  
                                      "section_type_label" : "Valve section",
                                      "section_parameters" : section_parameters,  
                                      "diameters_to_plot" : [None, None]
                                      }
                cross_section = CrossSection(valve_section_info = valve_section_info)            

            if self.stop_processing:
                return

            self.set_cross_section_by_elements(
                                                elements, 
                                                cross_section, 
                                                update_cross_section = True, 
                                                update_section_points = False
                                               )  

    def process_element_cross_sections_orientation_to_plot(self):
        """
        This method processes each element cross-seciton in accordance with
        the element rotation matrix.
        """
        rotation_data = np.zeros((self.number_structural_elements, 3), dtype=float)
        for index, element in enumerate(self.structural_elements.values()):
            rotation_data[index,:] = element.mean_rotations_at_local_coordinate_system()   
        
        rotation_results_matrices = transformation_matrix_Nx3x3_by_angles(rotation_data[:, 0], rotation_data[:, 1], rotation_data[:, 2])  
        matrix_resultant = rotation_results_matrices@self.transformation_matrices 
        r = Rotation.from_matrix(matrix_resultant)
        angles = -r.as_euler('zxy', degrees=True)
        
        for index, element in enumerate(self.structural_elements.values()):
            element.deformed_rotation_xyz = [angles[index,1], angles[index,2], angles[index,0]]

    def process_all_rotation_matrices(self):
        """
        This method ???????
        """
        delta_data = np.zeros((self.number_structural_elements, 3), dtype=float)
        xaxis_rotation_angle = np.zeros(self.number_structural_elements, dtype=float)
        for index, element in enumerate(self.structural_elements.values()):
            delta_data[index,:] = element.delta_x, element.delta_y, element.delta_z
            xaxis_rotation_angle[index] = element.beam_xaxis_rotation 

        self.transformation_matrices = transformation_matrix_3x3xN( delta_data[:,0], 
                                                                    delta_data[:,1], 
                                                                    delta_data[:,2], 
                                                                    gamma = xaxis_rotation_angle)

        # output_data = inverse_matrix_Nx3x3(self.transformation_matrices)
        r = Rotation.from_matrix(self.transformation_matrices)
        rotations = -r.as_euler('zxy', degrees=True)
        rotations_xyz = np.array([rotations[:,1], rotations[:,2], rotations[:,0]]).T
        self.section_rotations_xyz = rotations_xyz.copy()
        
        for index, element in enumerate(self.structural_elements.values()):
            element.sub_transformation_matrix = self.transformation_matrices[index, :, :]
            element.section_directional_vectors = self.transformation_matrices[index, :, :]
            element.section_rotation_xyz_undeformed = self.section_rotations_xyz[index,:]

    def process_elements_to_update_indexes_after_remesh_in_entity_file(self, list_elements, reset_line=False, line_id=None, dict_map_cross={}, dict_map_expansion_joint={}):
        """
        This methods ...
        """
        list_groups_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)

        if reset_line:
            self.reset_list_elements_from_line(line_id, dict_map_cross, dict_map_expansion_joint)
        else:
            for subgroup_elements in list_groups_elements:
                first_element_id = subgroup_elements[0]
                last_element_id = subgroup_elements[-1]
                start_node_id, end_node_id = self.get_distantest_nodes_from_elements([first_element_id, last_element_id]) 
                first_node_coordinates = self.nodes[start_node_id].coordinates
                last_node_coordinates = self.nodes[end_node_id].coordinates
                line_id = self.mesh.elements_to_line[first_element_id]
                key = f"{first_element_id}-{last_element_id}||{line_id}"
                self.dict_element_info_to_update_indexes_in_entity_file[key] = [list(first_node_coordinates),
                                                                                list(last_node_coordinates),
                                                                                subgroup_elements]


    def reset_list_elements_from_line(self, line_id, dict_map_cross, dict_map_expansion_joint):
        
        if line_id is None:
            return
        if len(dict_map_cross) == 0:
            return
        if len(dict_map_expansion_joint) == 0:
            return

        temp_dict = self.dict_element_info_to_update_indexes_in_entity_file.copy()
        for key in temp_dict.keys():
            key_line_id = int(key.split("||")[1])
            if line_id == key_line_id:
                self.dict_element_info_to_update_indexes_in_entity_file.pop(key)
        
        list_group_elements = []
        for key, list_elements_cross in dict_map_cross.items():
            list_group_elements.append(list_elements_cross)
        
        for (_, list_elements_joint, _) in dict_map_expansion_joint.values():
            list_group_elements.append(list_elements_joint)
        
        for _list_elements in list_group_elements:    
            list_subgroups_elements = check_is_there_a_group_of_elements_inside_list_elements(_list_elements) 
            for subgroup_elements in list_subgroups_elements:
                first_element_id = subgroup_elements[0]
                last_element_id = subgroup_elements[-1]
                start_node_id, end_node_id = self.get_distantest_nodes_from_elements([first_element_id, last_element_id]) 
                first_node_coordinates = self.nodes[start_node_id].coordinates
                last_node_coordinates = self.nodes[end_node_id].coordinates
                line_id = self.mesh.elements_to_line[first_element_id]
                key = f"{first_element_id}-{last_element_id}||{line_id}"
                self.dict_element_info_to_update_indexes_in_entity_file[key] = [    list(first_node_coordinates),
                                                                                    list(last_node_coordinates),
                                                                                    subgroup_elements   ]


    def process_elements_to_update_indexes_after_remesh_in_element_info_file(self, list_elements):
        """
        This method ...
        """
        input_groups_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)
        output_subgroups_elements = []
        for input_group in input_groups_elements:
            line_to_elements = defaultdict(list)
            for element_id in input_group:
                line = self.mesh.elements_to_line[element_id]
                line_to_elements[line].append(element_id)
            for line, elements in line_to_elements.items():
                output_subgroups_elements.append(elements)
        
        self.dict_list_elements_to_subgroups[str(list_elements)] = output_subgroups_elements

        for output_subgroup in output_subgroups_elements:
       
            first_element_id = output_subgroup[0]
            last_element_id = output_subgroup[-1]
            start_node_id, end_node_id = self.get_distantest_nodes_from_elements([first_element_id, last_element_id]) 
            first_node_coordinates = self.nodes[start_node_id].coordinates
            last_node_coordinates = self.nodes[end_node_id].coordinates

            key = f"{first_element_id}-{last_element_id}"
            
            self.dict_element_info_to_update_indexes_in_element_info_file[key] = [  list(first_node_coordinates),
                                                                                    list(last_node_coordinates),
                                                                                    output_subgroup ]


    def update_element_ids_after_remesh(self, dict_cache, tolerance=1e-7):
        """
        This method ...
        """      
        coord_matrix = self.nodal_coordinates_matrix_external
        list_coordinates = coord_matrix[:,1:].tolist()
        new_external_indexes = coord_matrix[:,0]
        dict_old_to_new_list_of_elements = {}
        dict_non_mapped_subgroups = {}
        dict_subgroups_old_to_new_group_nodes = defaultdict(list)

        for key, data in dict_cache.items():

            [first_node_coord, last_node_coord, subgroup_elements] = data

            if first_node_coord in list_coordinates:

                ind = list_coordinates.index(first_node_coord)
                new_external_index = int(new_external_indexes[ind])
                dict_subgroups_old_to_new_group_nodes[str(subgroup_elements)].append(new_external_index)          
            
            else:

                diff = np.linalg.norm(coord_matrix[:,1:] - np.array(first_node_coord), axis=1)
                mask = diff < tolerance
                
                try:
                    new_external_index = int(coord_matrix[:,0][mask])
                    dict_subgroups_old_to_new_group_nodes[str(subgroup_elements)].append(new_external_index)
                except:
                    dict_non_mapped_subgroups[str(subgroup_elements)] = subgroup_elements
                           
            if last_node_coord in list_coordinates:

                ind = list_coordinates.index(last_node_coord)
                new_external_index = int(new_external_indexes[ind])
                dict_subgroups_old_to_new_group_nodes[str(subgroup_elements)].append(new_external_index)           
            
            else:

                diff = np.linalg.norm(coord_matrix[:,1:] - np.array(last_node_coord), axis=1)
                mask = diff < tolerance
                
                try:
                    new_external_index = int(coord_matrix[:,0][mask])
                    dict_subgroups_old_to_new_group_nodes[str(subgroup_elements)].append(new_external_index)
                except:
                    dict_non_mapped_subgroups[str(subgroup_elements)] = subgroup_elements
            
        for str_subgroup_elements, edge_nodes_from_group in dict_subgroups_old_to_new_group_nodes.items():
            if str_subgroup_elements not in dict_non_mapped_subgroups.keys():
                start_element_index, end_element_index = self.get_elements_inside_nodes_boundaries(edge_nodes_from_group)
                new_list_elements = list(np.arange(start_element_index, end_element_index+1, dtype=int))
                dict_old_to_new_list_of_elements[str_subgroup_elements] = new_list_elements

        return [dict_old_to_new_list_of_elements, dict_non_mapped_subgroups]


    def get_distantest_nodes_from_elements(self, list_elements):
        """"This method returns the more distant nodes from selected elements
        
        """
        if len(list_elements) == 1:
            element_id = list_elements[0]
            first_node_id = self.structural_elements[element_id].first_node.external_index
            last_node_id = self.structural_elements[element_id].last_node.external_index

        if len(list_elements) == 2:
            [element_id1, element_id2] = list_elements
            element_1 = self.structural_elements[element_id1]
            element_2 = self.structural_elements[element_id2]
            diff_1 = element_1.first_node.coordinates - element_2.last_node.coordinates
            diff_2 = element_2.first_node.coordinates - element_1.last_node.coordinates
            
            if np.linalg.norm(diff_1) > np.linalg.norm(diff_2):
                first_node_id = element_1.first_node.external_index
                last_node_id = element_2.last_node.external_index 
            else:
                first_node_id = element_1.last_node.external_index
                last_node_id = element_2.first_node.external_index

        list_nodes = [first_node_id, last_node_id]
        return min(list_nodes), max(list_nodes)


    def get_elements_inside_nodes_boundaries(self, list_nodes):
        
        start_node, end_node = list_nodes
        element_1_start_node = self.dict_first_node_to_element_index[start_node]
        element_2_start_node = self.dict_last_node_to_element_index[start_node]
        
        if len(element_1_start_node) > 1 or len(element_2_start_node) > 1:
            elements_start_node = element_1_start_node
            for element_id in element_2_start_node:
                elements_start_node.append(element_id)
        elif element_1_start_node == []:
            elements_start_node = element_2_start_node
        elif element_2_start_node == []:
            elements_start_node = element_1_start_node
        else:
            elements_start_node = [element_1_start_node[0], element_2_start_node[0]]
        
        element_1_end_node = self.dict_first_node_to_element_index[end_node]
        element_2_end_node = self.dict_last_node_to_element_index[end_node]

        if len(element_1_end_node) > 1 or len(element_2_end_node) > 1:
            elements_end_node = element_1_end_node
            for element_id in element_2_end_node:
                elements_end_node.append(element_id)
        elif element_1_end_node == []:
            elements_end_node = element_2_end_node
        elif element_2_end_node == []:
            elements_end_node = element_1_end_node
        else:
            elements_end_node = [element_1_end_node[0], element_2_end_node[0]]
                
        first = True
        for element_start in elements_start_node:
            for element_end in elements_end_node:
                
                difference = self.structural_elements[element_start].element_center_coordinates - self.structural_elements[element_end].element_center_coordinates
                distance = np.linalg.norm(difference)
                
                if first:
                    first = False
                    previous_distance = distance
                    output_indexes = [element_start, element_end]
                
                if previous_distance > distance:
                    previous_distance = distance
                    output_indexes = [element_start, element_end]
     
        return min(output_indexes), max(output_indexes)             

    def deformed_amplitude_control_in_expansion_joints(self):
        """This method evaluates the deformed amplitudes in expansion joints nodes
        and reduces the amplitude through rescalling if higher levels are observed."""

        element_size = self.mesh.element_size

        for element in self.elements_with_expansion_joint:

            results_lcs = element.element_results_lcs()
            delta_yz = sum(results_lcs[1:3]**2)**(1/2)

            if delta_yz > 3 * element_size:
                value = element.joint_effective_diameter/6
                return True, value

            first_node = element.first_node
            last_node = element.last_node
            delta_x = abs(  (last_node.x + results_lcs[6]) - 
                            (first_node.x + results_lcs[0]) )

            if delta_x < element_size / 3 or delta_x > 2 * element_size:
                value = element_size / 2
                return True, value

        return False, None

    def get_number_of_elements_by_element_type(self):
        """" This method returns """
        acoustic_etype_to_number_elements = {   'undamped' : 0, 
                                                'proportional' : 0, 
                                                'wide-duct' : 0, 
                                                'LRF fluid equivalent' : 0, 
                                                'LRF full' : 0, 
                                                'undamped mean flow' : 0, 
                                                'howe' : 0, 
                                                'peters' : 0, 
                                                None : 0    }

        structural_etype_to_number_elements = { "pipe_1" : 0, 
                                                "beam_1" : 0, 
                                                "expansion_joint" : 0, 
                                                "valve" : 0, 
                                                None : 0 }

        structural_etype_to_elements = defaultdict(list)
        for element in self.structural_elements.values():
            structural_etype_to_number_elements[element.element_type] += 1
            structural_etype_to_elements[element.element_type].append(element.index)

        acoustic_etype_to_elements = defaultdict(list)
        for index, element in self.acoustic_elements.items():
            if self.structural_elements[index].element_type != 'beam_1':
                acoustic_etype_to_number_elements[element.element_type] += 1
                acoustic_etype_to_elements[element.element_type].append(element.index)

        return structural_etype_to_number_elements, acoustic_etype_to_number_elements

    def set_unprescribed_pipe_indexes(self, indexes):
        self.unprescribed_pipe_indexes = indexes
    
    def get_unprescribed_pipe_indexes(self):
        return self.unprescribed_pipe_indexes

    def update_nodal_solution_info(self, nodal_solution):
        """ This method sets the static nodal solution for 
            stress stiffening analysis.
        Parameters
        ----------
        nodal_solution: complex array of values
        """

        for node in self.nodes.values():  
            global_indexes = node.global_dof
            node.static_nodal_solution_gcs = nodal_solution[global_indexes, 0]

        for element in self.structural_elements.values():
            element.static_analysis_evaluated = True