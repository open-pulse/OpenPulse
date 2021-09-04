from collections import deque
from random import choice
from collections import defaultdict
import re
from libs.gmsh import gmsh 
import numpy as np
from scipy.spatial.transform import Rotation
from time import time
from pulse.preprocessing import structural_element

from pulse.preprocessing.entity import Entity
from pulse.preprocessing.node import Node, DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.structural_element import StructuralElement, NODES_PER_ELEMENT
from pulse.preprocessing.acoustic_element import AcousticElement, NODES_PER_ELEMENT
from pulse.preprocessing.compressor_model import CompressorModel
from pulse.preprocessing.before_run import BeforeRun
from data.user_input.project.printMessageInput import PrintMessageInput

from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer, _transformation_matrix_3x3xN, _transformation_matrix_Nx3x3_by_angles, check_is_there_a_group_of_elements_inside_list_elements

window_title_1 = "ERROR"

class Preprocessor:
    """A preprocessor class.
    This class creates a acoustic and structural preprocessor object.
    """
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        """
        This method reset the class default values.
        """
        self.DOFS_ELEMENT = DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        self.nodes = {}
        self.structural_elements = {}
        self.acoustic_elements = {}
        # self.neighbors = {}
        self.dict_tag_to_entity = {}
        self.line_to_elements = {}
        self.elements_to_line = {}
        self.elements_with_expansion_joint = []
        self.number_expansion_joints_by_lines = {}
        self.group_elements_with_length_correction = {}
        self.group_elements_with_capped_end = {}
        self.group_elements_with_perforated_plate = {}
        self.group_elements_with_stress_stiffening = {}
        self.group_elements_with_expansion_joints = {}
        self.group_lines_with_capped_end = {}        
        self.dict_lines_with_stress_stiffening = {}
        self.dict_lines_with_expansion_joints = {}
        self.dict_B2PX_rotation_decoupling = {}
        self.entities = []
        self.connectivity_matrix = []
        self.nodal_coordinates_matrix = []
        self.nodes_with_nodal_loads = []
        self.nodes_with_prescribed_dofs = []
        self.nodes_with_constrained_dofs = []
        self.nodes_with_masses = []
        self.nodes_connected_to_springs = []
        self.nodes_connected_to_dampers = []
        self.pair_of_nodes_with_elastic_nodal_links = []
        self.nodes_with_acoustic_pressure = []
        self.nodes_with_volume_velocity = []
        self.nodes_with_specific_impedance = []
        self.nodes_with_radiation_impedance = []
        self.element_with_length_correction = []
        self.element_with_perforated_plate = []
        self.element_with_capped_end = []
        self.dict_elements_with_B2PX_rotation_decoupling = defaultdict(list)
        self.dict_nodes_with_B2PX_rotation_decoupling = defaultdict(list)

        self.dict_structural_element_type_to_lines = defaultdict(list)
        self.dict_acoustic_element_type_to_lines = defaultdict(list)
        self.dict_beam_xaxis_rotating_angle_to_lines = defaultdict(list)

        self.dict_coordinate_to_update_bc_after_remesh = {}
        self.dict_element_info_to_update_indexes_in_entity_file = {}
        self.dict_element_info_to_update_indexes_in_element_info_file = {}
        self.dict_list_elements_to_subgroups = {}
        self.dict_old_to_new_node_external_indexes = {}

        self.nodes_with_elastic_link_stiffness = {}
        self.nodes_with_elastic_link_dampings = {}
        self.lines_with_capped_end = []
        self.lines_with_stress_stiffening = []
        self.elements_with_adding_mass_effect = []
        self.radius = {}
        self.element_type = "pipe_1" # defined as default
        self.all_lines = []
        self.flag_fluid_mass_effect = False
        self.stress_stiffening_enabled = False
        self.group_index = 0
        self.volume_velocity_table_index = 0
        
        self.beam_gdofs = None
        self.pipe_gdofs = None

    def generate(self, path, element_size, tolerance=1e-6):
        """
        This method evaluates the Lamé's first parameter `lambda`.

        Parameters
        ----------
        path : str
            CAD file path. '.igs' is the only format file supported.

        element_size : float
            Element size to be used to build the preprocessor.
        """
        self.element_size = element_size
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size, tolerance=tolerance)
        self._create_entities()
        self._map_lines_to_elements()
        self._finalize_gmsh()

        # t0 = time()
        self._load_neighbors()
        # dt = time() - t0
        # print(f"Time to process _load_neighbors: {dt}")

        # t0 = time()
        self._order_global_indexes()
        # dt = time() - t0
        # print(f"Time to process _order_global_indexes: {dt}")
        
        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        self.get_dict_nodes_to_element_indexes()
        self.get_list_edge_nodes(element_size)
        self.get_principal_diagonal_structure_parallelepiped()
        # self.get_dict_line_to_nodes()
        
        # t0 = time()
        self.process_all_rotation_matrices()
        self.create_dict_lines_to_rotation_angles()
        # dt = time() - t0
        # print("Time to process all rotations matrices: ", dt)
        

    def neighbor_elements_diameter(self):
        """
        This method maps the elements outer diameters that each node belongs to. The maping is done according to the node external index.

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
    
    def neighboor_elements_of_node(self, node_ID):
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
        node = self.nodes[node_ID]
        neighboor_elments = defaultdict(list)      
        for element in self.acoustic_elements.values():
            first = element.first_node
            last = element.last_node
            if node in [first, last]:
                neighboor_elments[node].append(element.index)
        return neighboor_elments[node]

    def _initialize_gmsh(self, path):
        """
        This method initializes mesher algorithm gmsh.

        Parameters
        ----------
        str
            CAD file path. '.igs' is the only format file supported.
        """
        gmsh.initialize('', False)
        gmsh.open(path)

    def _set_gmsh_options(self, element_size, tolerance=1e-6):
        """
        This method sets the mesher algorithm configuration.

        Parameters
        ----------
        float
            Element size.
        """
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Geometry.Tolerance', tolerance)

    def _create_entities(self):
        """
        This method generate the mesh entities, nodes, structural elements, acoustic elements 
        and their connectivity.
        """
        gmsh.model.mesh.generate(3)

        for dim, tag in gmsh.model.getEntities(1):
            newEntity = Entity(tag)

            #Element
            _, node_indexes, connectivity = gmsh.model.mesh.getElements(dim, tag) 
            node_indexes = node_indexes[0]
            connectivity = split_sequence(connectivity[0], 2)

            for index, (start, end) in zip(node_indexes, connectivity):
                edges = index, start, end
                newEntity.insertEdge(edges)

            #Nodes
            element_indexes, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            coordinates = split_sequence(coordinates, 3)

            for index, (x, y, z) in zip(element_indexes, coordinates):
                node = index, mm_to_m(x), mm_to_m(y), mm_to_m(z)
                newEntity.insertNode(node)
                
            self.all_lines.append(tag)
            self.entities.append(newEntity)
            self.dict_tag_to_entity[tag] = newEntity

        gmsh.model.mesh.removeDuplicateNodes()

        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivity = gmsh.model.mesh.getElements()

        self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
        self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))
       
        self._create_nodes(node_indexes, coords, self.map_nodes)
        self._create_structural_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)
        self._create_acoustic_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements) 

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
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.acoustic_elements[map_elements[i]] = AcousticElement(first_node, last_node, map_elements[i])
            self.number_acoustic_elements = len(self.acoustic_elements)

    # def _create_dict_gdofs_to_external_indexes(self):
    #     # t0 = time()
    #     self.dict_gdofs_to_external_indexes = {}
    #     for external_index, node in self.nodes.items():
    #         for gdof in node.global_dof:
    #             self.dict_gdofs_to_external_indexes[gdof] = external_index
    #     # dt = time()-t0
    #     # print(len(self.dict_gdofs_to_external_indexes))
    #     # print("Time to process: ", dt)

    def _map_lines_to_elements(self, mesh_loaded=False):
        """
        This method maps entities to elements.

        Parameters
        ----------
        mesh_loaded : boll, optional.
            True if the mesh was already generated (internally or externally). False otherwise.
        """
        if mesh_loaded:
            self.line_to_elements[1] = list(self.structural_elements.keys())
            for element in list(self.structural_elements.keys()):
                self.elements_to_line[element] = 1
        else: 
            # t0 = time()   
            mapping = self.map_elements
            for dim, tag in gmsh.model.getEntities(1):
                elements_of_entity = gmsh.model.mesh.getElements(dim, tag)[1][0]
                list_elements = np.array([mapping[element] for element in elements_of_entity], dtype=int)
                self.line_to_elements[tag] = list_elements
                for element_id in list_elements:
                    self.elements_to_line[element_id] = tag 
            # dt = time() - t0
            # print(f"Time to process : {dt}")


    def get_line_length(self, line_ID):
        first_element_ID = self.line_to_elements[line_ID][0]
        last_element_ID = self.line_to_elements[line_ID][-1]

        node1_first_element = self.structural_elements[first_element_ID].first_node
        node2_first_element = self.structural_elements[first_element_ID].last_node

        node1_last_element = self.structural_elements[last_element_ID].first_node
        node2_last_element = self.structural_elements[last_element_ID].last_node

        list_nodes = [  node1_first_element, node2_first_element, 
                        node1_last_element, node2_last_element  ]

        length = 0
        for index in range(1, len(list_nodes)):
            length_i = np.linalg.norm(list_nodes[0].coordinates - list_nodes[index].coordinates)
            if length_i > length:
                length = length_i
        
        return length

    def _finalize_gmsh(self):
        """
        This method finalize the mesher gmsh algorithm.
        """
        gmsh.finalize()

    def _load_neighbors(self):
        """
        This method updates the structural elements neighbors dictionary. The dictionary's keys and values are nodes objects.
        """
        self.neighbors = defaultdict(list)
        # self.nodes_with_multiples_neighbors = {}
        for element in self.structural_elements.values():
            self.neighbors[element.first_node].append(element.last_node)
            self.neighbors[element.last_node].append(element.first_node)
            # if len(self.neighbors[element.first_node]) > 2:
            #     self.nodes_with_multiples_neighbors[element.first_node] = self.neighbors[element.first_node]
            # if len(self.neighbors[element.last_node]) > 2:
            #     self.nodes_with_multiples_neighbors[element.last_node] = self.neighbors[element.last_node]


    def get_list_edge_nodes(self, size, tolerance=1e-5):
        
        coord_matrix = self.nodal_coordinates_matrix_external
        # self.list_edge_nodes = []
        list_node_ids = []
        for node, neigh_nodes in self.neighbors.items():
            if len(neigh_nodes) == 1:
                # self.list_edge_nodes.append(node.external_index)
                coord = node.coordinates
                diff = np.linalg.norm(coord_matrix[:,1:] - np.array(coord), axis=1)
                mask = diff < ((size/2) + tolerance)
                if True in mask:
                    try:
                        list_external_indexes = coord_matrix[:,0][mask]
                        if len(list_external_indexes) > 1:
                            for external_index in list_external_indexes:
                                if len(self.neighbors[self.nodes[external_index]]) == 1:
                                    list_node_ids.append(int(external_index))
                    except Exception as _log_error:
                        PrintMessageInput(["Error while checking mesh at the line edges", str(_log_error), window_title_1])
        
        if len(list_node_ids)>0:
            title = "Problem detected in connectivity between neighbor nodes"
            message = "At least one disconnected node has been detected at the edge of one line due "
            message += "to the mismatch between the geometry 'keypoints' and the current mesh setup. " 
            message += "We strongly recommend reducing the element size or correcting the problem "
            message += "in the geometry file before proceeding with the model setup.\n\n"
            message += f"List of disconnected node(s): \n{list_node_ids}"
            PrintMessageInput([title, message, window_title_1])                
        
 
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

        # dt = time()-t0
        # print("Time to process the global matrices bandwidth reduction: ", dt)


    def load_mesh(self, coordinates, connectivity):
        """
        This method creates mesh data from nodes coordinates and connectivity matrix.

        Parameters
        ----------
        coordinates : array.
            Nodes' coordinates. Each row presents the nodes' index, x-coordinate, y-coordinate, and z-coordinate. Coordinates matrix row structure:
            ''[Node index, x-coordinate, y-coordinate, z-coordinate]''.
            
        connectivity : array.
            Connectivity matrix. Each row presents the elements' index, first node index, and last node index. Connectivity matrix row structure:
            ''[Element index, first node index, last node index]''.
        """

        coordinates = np.loadtxt(coordinates)
        connectivity = np.loadtxt(connectivity, dtype=int).reshape(-1,3)
        self.number_structural_elements = connectivity.shape[0]
        self.number_acoustic_elements = connectivity.shape[0]

        newEntity = Entity(1)
        map_indexes = dict(zip(coordinates[:,0], np.arange(1, len(coordinates[:,0])+1, 1)))

        for i, x, y, z in coordinates:
            self.nodes[int(map_indexes[i])] = Node(x, y, z, external_index = int(map_indexes[i]))
            node = int(map_indexes[i]), x, y, z
            newEntity.insertNode(node)
        self.number_nodes = len(self.nodes)

        for i, nodes in enumerate(connectivity[:,1:]):
            first_node = self.nodes[map_indexes[nodes[0]]]
            last_node  = self.nodes[map_indexes[nodes[1]]]
            self.structural_elements[i+1] = StructuralElement(first_node, last_node, i+1)
            self.acoustic_elements[i+1] = AcousticElement(first_node, last_node, i+1)
            edges = i+1, map_indexes[nodes[0]], map_indexes[nodes[1]]
            newEntity.insertEdge(edges)
            
        self.entities.append(newEntity)
        self.dict_tag_to_entity[1] = newEntity
        #Ordering global indexes
        for index, node in enumerate(self.nodes.values()):
            node.global_index = index

        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        self.get_dict_nodes_to_element_indexes()
        self.get_principal_diagonal_structure_parallelepiped()
        self.all_lines.append(1)
        self._map_lines_to_elements(mesh_loaded=True)
        self.process_all_rotation_matrices()
        self.create_dict_lines_to_rotation_angles()
        # self._create_dict_gdofs_to_external_indexes()

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
        reordering : boll, optional.
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
        reordering : boll, optional.
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
        dict_structural_to_acoustic_elements = {}
        for key, element in self.structural_elements.items():
            dict_structural_to_acoustic_elements[element] = self.acoustic_elements[key]
        return dict_structural_to_acoustic_elements 

    def get_neighbor_nodes_and_elements_by_node(self, node_id, length, tolerance=1e-5):
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

    def set_structural_element_type_by_element(self, elements, element_type, remove=False):
        """
        This method attributes structural element type to a list of elements.

        Parameters
        ----------
        elements : list
            Structural elements indexes.
            
        element_type : str, ['pipe_1', 'pipe_2', 'beam_1', 'expansion_joint']
            Structural element type to be attributed to the listed elements.
            
        remove : boll, optional
            True if the element_type have to be removed from the structural element type dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.structural_elements, elements):
            element.element_type = element_type
        if remove:
            self.dict_structural_element_type_to_lines.pop(element_type)
    
    def set_acoustic_element_type_by_element(self, elements, element_type, proportional_damping=None, remove=False):
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
            
        remove : boll, optional
            True if the element_type have to be removed from the acoustic element type dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.acoustic_elements, elements):
            element.element_type = element_type
            element.proportional_damping = proportional_damping
        if remove:
            self.dict_acoustic_element_type_to_lines.pop(element_type)
    
    def set_cross_section_by_element(self, elements, cross_section, update_cross_section=False):
        """
        This method attributes cross section object to a list of acoustic and structural elements.

        Parameters
        ----------
        elements : list
            Acoustic and structural elements indexes.
            
        cross_section : Cross section object
            Tube cross section data.
            
        update_cross_section : boll, optional
            True if the cross section data have to be evaluated or updated. False otherwise.
            Default is False.
        """
        if update_cross_section:
            cross_section.update_properties()

        if isinstance(cross_section, list):
            for i, element in enumerate(elements):
                _cross_section = cross_section[i]
                _element = [element]
                for element in slicer(self.structural_elements, _element):
                    element.cross_section = _cross_section
                for element in slicer(self.acoustic_elements, _element):
                    element.cross_section = _cross_section
        else:    
            for element in slicer(self.structural_elements, elements):
                element.cross_section = cross_section
            for element in slicer(self.acoustic_elements, elements):
                element.cross_section = cross_section

    def set_cross_section_by_line(self, line, cross_section):
        """
        This method attributes cross section object to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        cross_section : Cross section object
            Tube cross section data.
        """
        for elements in slicer(self.line_to_elements, line):
            self.set_cross_section_by_element(elements, cross_section)
    
    def set_structural_element_type_by_line(self, line, element_type, remove=False):
        """
        This method attributes structural element type to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        element_type : str, ['pipe_1', 'pipe_2', 'beam_1']
            Structural element type to be attributed to elements.
            
        remove : boll, optional
            True if the element_type have to be removed from the structural element type dictionary. False otherwise.
            Default is False.
        """
        for elements in slicer(self.line_to_elements, line):
            self.set_structural_element_type_by_element(elements, element_type)

        if remove:
            self.dict_structural_element_type_to_lines.pop(element_type)
        elif element_type != "":
            temp_dict = self.dict_structural_element_type_to_lines.copy()
            if element_type not in list(temp_dict.keys()):
                self.dict_structural_element_type_to_lines[element_type].append(line)
                for key, lines in temp_dict.items():
                    if key != element_type:
                        if line in lines:
                            self.dict_structural_element_type_to_lines[key].remove(line)
            else:
                for key, lines in temp_dict.items():
                    if key != element_type:
                        if line in lines:
                            self.dict_structural_element_type_to_lines[key].remove(line)
                    else:
                        if line not in lines:
                            self.dict_structural_element_type_to_lines[key].append(line)
                    if self.dict_structural_element_type_to_lines[key] == []:
                        self.dict_structural_element_type_to_lines.pop(key)

    def set_acoustic_element_type_by_line(self, line, element_type, proportional_damping=None, remove=False):
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
            
        remove : boll, optional
            True if the element_type have to be removed from the acoustic element type dictionary. False otherwise.
            Default is False.
        """
        for elements in slicer(self.line_to_elements, line):
            self.set_acoustic_element_type_by_element(elements, element_type, proportional_damping=proportional_damping)

        if remove:
            self.dict_acoustic_element_type_to_lines.pop(element_type)
        elif element_type != "":
            temp_dict = self.dict_acoustic_element_type_to_lines.copy()
            if element_type not in list(temp_dict.keys()):
                self.dict_acoustic_element_type_to_lines[element_type].append(line)
                for key, lines in temp_dict.items():
                    if key != element_type:
                        if line in lines:
                            self.dict_acoustic_element_type_to_lines[key].remove(line)
            else:
                for key, lines in temp_dict.items():
                    if key != element_type:
                        if line in lines:
                            self.dict_acoustic_element_type_to_lines[key].remove(line)
                    else:
                        if line not in lines:
                            self.dict_acoustic_element_type_to_lines[key].append(line)
                    if self.dict_acoustic_element_type_to_lines[key] == []:
                        self.dict_acoustic_element_type_to_lines.pop(key)

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

    def set_material_by_line(self, lines, material):
        """
        This method attributes material object to all elements that belongs to a line/entity.

        Parameters
        ----------
        line : list
            Entities tag.
            
        material : Material object
            Material data.
        """
        for elements in slicer(self.line_to_elements, lines):
            self.set_material_by_element(elements, material)

    def set_force_by_element(self, elements, loads):
        for element in slicer(self.structural_elements, elements):
            element.loaded_forces = loads
    
    def set_structural_load_bc_by_node(self, nodes_id, data):
        """
        This method attributes structural force and moment loads to a list of nodes.

        Parameters
        ----------
        nodes_id : list
            Nodes external indexes.
            
        values : complex or array
            Force and moment loads. Complex valued input corresponds to a constant load with respect to the frequency. Array valued input corresponds to a variable load with respect to the frequency.
        """
        [values, table_names] = data
        for node in slicer(self.nodes, nodes_id):
            node.nodal_loads = values
            node.nodal_loads_table_names = table_names            
            node.prescribed_dofs = [None, None, None, None, None, None]
            self.process_nodes_to_update_indexes_after_remesh(node)
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_nodal_loads = True
                node.there_are_nodal_loads = True
                if not node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.append(node)
                continue
                # return
            else:
                node.loaded_table_for_nodal_loads = False
            # Checking complex single values    
            check_values = [isinstance(bc, complex) for bc in values]
            if True in check_values:
                node.there_are_nodal_loads = True
                if not node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.append(node)
            else:
                node.there_are_nodal_loads = False
                if node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.remove(node)

    def add_mass_to_node(self, nodes, data):
        """
        This method attributes structural lumped mass to a list of nodes.

        Parameters
        ----------
        nodes_id : list
            Nodes external indexes.
            
        values : complex or array
            Lumped mass. Complex valued input corresponds to a constant mass with respect to the frequency. Array valued input corresponds to a variable mass with respect to the frequency.
        """
        [values, table_names] = data
        for node in slicer(self.nodes, nodes):
            node.lumped_masses = values
            node.lumped_masses_table_names = table_names
            self.process_nodes_to_update_indexes_after_remesh(node)
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_masses = True
                node.there_are_lumped_masses = True
                if not node in self.nodes_with_masses:
                    self.nodes_with_masses.append(node)
                continue
            else:
                node.loaded_table_for_lumped_masses = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_masses = True
                if not node in self.nodes_with_masses:
                    self.nodes_with_masses.append(node)
            else:
                node.there_are_lumped_masses = False
                if node in self.nodes_with_masses:
                    self.nodes_with_masses.remove(node)

    def add_spring_to_node(self, nodes, data):
        """
        This method attributes structural lumped stiffness (spring) to a list of nodes.

        Parameters
        ----------
        nodes_id : list
            Nodes external indexes.
            
        values : complex or array
            Lumped stiffness. Complex valued input corresponds to a constant stiffness with respect to the frequency. Array valued input corresponds to a variable stiffness with respect to the frequency.
        """
        [values, table_names] = data
        for node in slicer(self.nodes, nodes):
            node.lumped_stiffness = values
            node.lumped_stiffness_table_names = table_names
            self.process_nodes_to_update_indexes_after_remesh(node)
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_stiffness = True
                node.there_are_lumped_stiffness = True
                if not node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.append(node)
                continue
            else:
                node.loaded_table_for_lumped_stiffness = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_stiffness = True
                if not node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.append(node)
            else:
                node.there_are_lumped_stiffness = False
                if node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.remove(node)
    
    def add_damper_to_node(self, nodes, data):
        """
        This method attributes structural lumped damping (damper) to a list of nodes.

        Parameters
        ----------
        nodes_id : list
            Nodes external indexes.
            
        values : complex or array
            Lumped damping. Complex valued input corresponds to a constant damping with respect to the frequency. Array valued input corresponds to a variable damping with respect to the frequency.
        """
        [values, table_names] = data
        for node in slicer(self.nodes, nodes):
            node.lumped_dampings = values
            node.lumped_dampings_table_names = table_names
            self.process_nodes_to_update_indexes_after_remesh(node)
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_dampings = True
                node.there_are_lumped_dampings = True
                if not node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.append(node)
                continue
            else:
                node.loaded_table_for_lumped_dampings = False
            # Checking complex single values    
            check_values = [False if bc is None else True for bc in values]
            if True in check_values:
                node.there_are_lumped_dampings = True
                if not node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.append(node)
            else:
                node.there_are_lumped_dampings = False
                if node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.remove(node)

    def set_prescribed_dofs_bc_by_node(self, nodes, data):
        """
        This method attributes structural displacement and rotation boundary condition to a list of nodes.

        Parameters
        ----------
        nodes_id : list
            Nodes external indexes.
            
        values : complex or array
            Displacement and rotation. Complex valued input corresponds to a constant boundary condition with respect to the frequency. Array valued input corresponds to a variable boundary condition with respect to the frequency.
        """
        [values, table_names] = data
        for node in slicer(self.nodes, nodes):
            node.prescribed_dofs = values
            node.prescribed_dofs_table_names = table_names
            node.nodal_loads = [None,None,None,None,None,None]
            self.process_nodes_to_update_indexes_after_remesh(node)
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_prescribed_dofs = True
                node.there_are_prescribed_dofs = True
                if not node in self.nodes_with_constrained_dofs:
                    self.nodes_with_constrained_dofs.append(node)
                if not node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.append(node)
                continue
                # return
            else:
                node.loaded_table_for_prescribed_dofs = False
            # Checking complex single values    
            check_values = [isinstance(bc, complex) for bc in values]
            if True in check_values:
                node.there_are_prescribed_dofs = True
                if complex(0) in values:
                    node.there_are_constrained_dofs = True
                    if not node in self.nodes_with_constrained_dofs:
                        self.nodes_with_constrained_dofs.append(node)
                if not node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.append(node)              
            else:
                node.there_are_prescribed_dofs = False
                node.there_are_constrained_dofs = False
                if node in self.nodes_with_constrained_dofs:
                    self.nodes_with_constrained_dofs.remove(node)
                if node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.remove(node) 

    def set_B2PX_rotation_decoupling(self, element_ID, node_ID, rotations_to_decouple=[False, False, False], remove=False):
        """
        This method .

        Parameters
        ----------
        element_ID : list
            Element indexes.

        nodes_id : list
            Nodes external indexes.

        rotations_to_decouple : list of bollean, optional
            ?????
            Default is [False, False, False]
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        DOFS_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        N = DOF_PER_NODE_STRUCTURAL
        mat_ones = np.ones((DOFS_PER_ELEMENT,DOFS_PER_ELEMENT), dtype=int)

        neighboor_elements = self.neighboor_elements_of_node(node_ID)
        if len(neighboor_elements)<3:
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
        
        node = self.nodes[node_ID]
        element = self.structural_elements[element_ID]
        
        if rotations_to_decouple.count(False) == 3 or remove:
            mat_out = mat_ones

        elif rotations_to_decouple.count(True) == 3:  
            mat_out = mat_base

        elif node in [element.first_node]:
  
            temp = mat_base[:int(N/2), :int(N/2)].copy()
            mat_base[:N,:N] = np.zeros((N,N), dtype=int)
            mat_base[:int(N/2), :int(N/2)] = temp

            for index, value in enumerate(rotations_to_decouple):
                if not value:
                    ij = index + int(N/2)
                    mat_base[:, [ij, ij+N]] = np.ones((DOFS_PER_ELEMENT, 2), dtype=int)
                    mat_base[[ij, ij+N], :] = np.ones((2, DOFS_PER_ELEMENT), dtype=int) 
            mat_out = mat_base

        elif node in [element.last_node]:
   
            temp = mat_base[N:int(3*N/2), N:int(3*N/2)].copy()
            mat_base[N:,N:] = np.zeros((N,N), dtype=int)
            mat_base[N:int(3*N/2), N:int(3*N/2)] = temp

            for index, value in enumerate(rotations_to_decouple):
                if not value:
                    ij = index + int(3*N/2)
                    mat_base[:, [ij-N, ij]] = np.ones((DOFS_PER_ELEMENT, 2), dtype=int)
                    mat_base[[ij-N, ij], :] = np.ones((2, DOFS_PER_ELEMENT), dtype=int) 
            mat_out = mat_base

        section = str(rotations_to_decouple)
        element.decoupling_matrix = mat_out
        element.decoupling_info = [element_ID, node_ID, rotations_to_decouple]

        if remove:

            if element_ID in self.dict_elements_with_B2PX_rotation_decoupling[section]:
                self.dict_elements_with_B2PX_rotation_decoupling[section].remove(element_ID)  
            if node_ID in self.dict_nodes_with_B2PX_rotation_decoupling[section]:
                self.dict_nodes_with_B2PX_rotation_decoupling[section].remove(node_ID)
            
            element.decoupling_info = None

        else: 
                     
            if section not in list(self.dict_elements_with_B2PX_rotation_decoupling.keys()):
                self.dict_elements_with_B2PX_rotation_decoupling[section].append(element_ID)
                self.dict_nodes_with_B2PX_rotation_decoupling[section].append(node_ID)  

            count = 0
            temp_dict = self.dict_elements_with_B2PX_rotation_decoupling.copy()
            for key, elements in temp_dict.items(): 
                count += 1
                temp_list_nodes = self.dict_nodes_with_B2PX_rotation_decoupling[key].copy()
                temp_list_elements = self.dict_elements_with_B2PX_rotation_decoupling[key].copy()  
                
                if key == str([False, False, False]):
                    if element_ID in elements:
                        for index, element in enumerate(elements):
                            if element == element_ID:
                                temp_list_nodes.remove(node_ID)
                                temp_list_elements.remove(element_ID)
                                self.dict_nodes_with_B2PX_rotation_decoupling[key] = temp_list_nodes
                                self.dict_elements_with_B2PX_rotation_decoupling[key] = temp_list_elements

                elif key == section:
                    if element_ID in elements:
                        for index, element in enumerate(elements):
                            if element == element_ID:
                                temp_list_nodes[index] = node_ID
                                self.dict_nodes_with_B2PX_rotation_decoupling[key] = temp_list_nodes
                                self.dict_elements_with_B2PX_rotation_decoupling[key] = temp_list_elements
                    else:
                        self.dict_elements_with_B2PX_rotation_decoupling[section].append(element_ID)
                        self.dict_nodes_with_B2PX_rotation_decoupling[section].append(node_ID) 

                elif key != section:
                    if element_ID in elements:
                        for index, element in enumerate(elements):
                            if element == element_ID:
                                temp_list_nodes.remove(node_ID)
                                temp_list_elements.remove(element_ID)
                                self.dict_nodes_with_B2PX_rotation_decoupling[key] = temp_list_nodes
                                self.dict_elements_with_B2PX_rotation_decoupling[key] = temp_list_elements
                
        return mat_out  

    def enable_fluid_mass_adding_effect(self, reset=False):
        """
        This method enables or disables the addition of fluid mass in the structural element mass.

        Parameters
        ----------            
        reset : boll, optional
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

    def set_capped_end_by_elements(self, elements, value, selection):
        """
        This method enables or disables the capped end effect in a list of acoustic elements.

        Parameters
        ----------
        elements : list
            Acoustic elements indexes.
            
        value : boll
            True if the capped end effect have to be activated. False otherwise.

        selection : ?????
            ??????
        """      
        for element in slicer(self.structural_elements, elements):
            element.capped_end = value
            if value:
                if element not in self.element_with_capped_end:
                    self.element_with_capped_end.append(element)
            else:
                if element in self.element_with_capped_end:
                    self.element_with_capped_end.remove(element)
        if value:
            self.group_elements_with_capped_end[selection] = elements
        else:
            if selection in self.group_elements_with_capped_end.keys():
                self.group_elements_with_capped_end.pop(selection) 

    # def set_capped_end_line_to_element(self, lines, value):
    #     for elements in slicer(self.line_to_elements, lines):
    #         for element in slicer(self.structural_elements, elements):
    #             element.capped_end = value
 
    def set_capped_end_by_line(self, lines, value):
        """
        This method enables or disables the capped end effect to all acoustic elements that belongs to a line.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        value : boll
            True if the capped end effect have to be activated. False otherwise.
        """
        # self.set_capped_end_line_to_element(lines, value)
        if isinstance(lines, int):
            lines = [lines]

        for elements in slicer(self.line_to_elements, lines):
            for element in slicer(self.structural_elements, elements):
                element.capped_end = value
        if lines == "all":
            self.group_elements_with_capped_end = {}
            self.lines_with_capped_end = []
            if value:
                for line in self.all_lines:
                    self.lines_with_capped_end.append(line)
        else:
            for tag in lines:
                if value:
                    if tag not in self.lines_with_capped_end:
                        self.lines_with_capped_end.append(tag)
                else:
                    if tag in self.lines_with_capped_end:
                        self.lines_with_capped_end.remove(tag)

    # def set_capped_end_all_lines(self, value):
    #     self.set_capped_end_line_to_element("all", value)
    #     self.group_elements_with_capped_end = {}
    #     self.lines_with_capped_end = []
    #     if value:
    #         for line in self.all_lines:
    #             self.lines_with_capped_end.append(line)

    def set_stress_stiffening_by_line(self, lines, pressures, remove=False):
        """
        This method .

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        parameters : list
            ????????.
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if isinstance(lines, int):
            lines = [lines]
        for elements in slicer(self.line_to_elements, lines):
            self.set_stress_stiffening_by_elements(elements, pressures)
        if lines == "all":
            self.group_elements_with_stress_stiffening = {}
            self.lines_with_stress_stiffening = []
            if not remove:
                for line in self.all_lines:
                    self.lines_with_stress_stiffening.append(line)
                    self.dict_lines_with_stress_stiffening[line] = pressures
        else:
            for line in lines:
                if remove:
                    if line in self.lines_with_stress_stiffening:
                        self.lines_with_stress_stiffening.remove(line) 
                        self.dict_lines_with_stress_stiffening.pop(line)               
                else:
                    if line not in self.lines_with_stress_stiffening:
                        self.lines_with_stress_stiffening.append(line)
                        self.dict_lines_with_stress_stiffening[line] = pressures

    def set_stress_stiffening_by_elements(self, elements, pressures, section=None, remove=False):
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
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        self.stress_stiffening_enabled = True
        
        for element in slicer(self.structural_elements, elements):
            element.external_pressure = pressures[0]
            element.internal_pressure = pressures[1]
            
            if section is not None:
                if remove:
                    if section in self.group_elements_with_stress_stiffening.keys():
                        self.group_elements_with_stress_stiffening.pop(section) 
                else:
                    self.group_elements_with_stress_stiffening[section] = [pressures, elements]


    def add_expansion_joint_by_elements(self, 
                                        list_elements, 
                                        parameters, 
                                        remove=False, 
                                        aux_line_id=None, 
                                        reset_cross=True):
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
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        if aux_line_id is not None:
            elements_from_line = self.line_to_elements[aux_line_id]
            temp_dict = self.group_elements_with_expansion_joints.copy()
            for key, [_list_elements_ids, _] in temp_dict.items():
                for element_id in _list_elements_ids:
                    if element_id in elements_from_line:
                        self.group_elements_with_expansion_joints.pop(key)
                        break

        list_lines = []
        for element_id in list_elements:
            line_id = self.elements_to_line[element_id]
            if line_id not in list_lines:
                list_lines.append(line_id)

        if remove:
            for element in slicer(self.structural_elements, list_elements):
                element.reset_expansion_joint_parameters()
                if reset_cross:
                    element.cross_section = None
                if element in self.elements_with_expansion_joint:
                    self.elements_with_expansion_joint.remove(element)
            
            for line_id in list_lines:
                if line_id in self.number_expansion_joints_by_lines.keys():
                    self.number_expansion_joints_by_lines.pop(line_id)

        else:

            for line_id in list_lines:
                if line_id in self.number_expansion_joints_by_lines.keys():
                    self.number_expansion_joints_by_lines[line_id] += 1
                else:
                    self.number_expansion_joints_by_lines[line_id] = 1

            [joint_length, effective_diameter, joint_mass, axial_locking_criteria, rods_included] = parameters[0]
            [axial_stiffness, transversal_stiffness, torsional_stiffness, angular_stiffness] = parameters[1]
            list_stiffness_table_names = parameters[2]

            for element in slicer(self.structural_elements, list_elements):
                element.joint_length = joint_length
                element.joint_effective_diameter = effective_diameter
                element.joint_mass = joint_mass
                element.joint_axial_locking_criteria = axial_locking_criteria
                element.joint_rods_included = rods_included
                element.joint_axial_stiffness = axial_stiffness
                element.joint_transversal_stiffness = transversal_stiffness
                element.joint_torsional_stiffness = torsional_stiffness
                element.joint_angular_stiffness = angular_stiffness
                element.joint_stiffness_table_names = list_stiffness_table_names
                element.expansion_joint_parameters = parameters
                if element not in self.elements_with_expansion_joint:
                    self.elements_with_expansion_joint.append(element)
                
            if aux_line_id is None:
                size = len(self.group_elements_with_expansion_joints)
                key = f"group-{size+1}"
                self.group_elements_with_expansion_joints[key] = [list_elements, parameters]


    def add_expansion_joint_by_line(self, line_id, parameters, remove=False):
        """
        This method .

        Parameters
        ----------
        lines : list
            Lines/entities indexes.

        parameters : list
            ????????.
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        for elements in slicer(self.line_to_elements, line_id):
            self.add_expansion_joint_by_elements(elements, parameters, remove=remove, aux_line_id=line_id)
        if remove:
            if line_id in list(self.dict_lines_with_expansion_joints.keys()):
                self.dict_lines_with_expansion_joints.pop(line_id)
            if line_id in self.number_expansion_joints_by_lines.keys():
                self.number_expansion_joints_by_lines.pop(line_id)
        else:
            self.dict_lines_with_expansion_joints[line_id] = parameters
            self.number_expansion_joints_by_lines[line_id] = 1
        
    def set_stress_intensification_by_element(self, elements, value):
        """
        This method enables or disables the stress intensification effect in a list of structural elements.

        Parameters
        ----------
        elements : list
            Elements indexes.
            
        value : boll
            True if the stress intensification effect have to be activated. False otherwise.
        """  
        for element in slicer(self.structural_elements, elements):
            element.stress_intensification = value

    def set_stress_intensification_by_line(self, lines, value):
        """
        This method enables or disables the stress intensification effect to all structural elements that belongs to a line.

        Parameters
        ----------
        lines : list
            Lines/entities indexes.
            
        value : boll
            True if the stress intensification effect have to be activated. False otherwise.
        """
        for elements in slicer(self.line_to_elements, lines):
            self.set_stress_intensification_by_element(elements, value)
            
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
    
    def set_fluid_by_line(self, lines, fluid):
        """
        This method attributes fluid object to all acoustic elements that belongs to a line/entity.

        Parameters
        ----------
        line/entity : list
            Lines/entities tags.
            
        fluid : Fluid object
            Fluid data.
        """
        for elements in slicer(self.line_to_elements, lines):
            self.set_fluid_by_element(elements, fluid)

    def set_perforated_plate_by_elements(self, elements, perforated_plate, section, delete_from_dict=False):
        for element in slicer(self.acoustic_elements, elements):
            element.perforated_plate = perforated_plate
            element.delta_pressure = 0
            element.pp_impedance = None
            if element not in self.element_with_perforated_plate:
                self.element_with_perforated_plate.append(element)
            if perforated_plate is None:
                if element in self.element_with_perforated_plate:
                    self.element_with_perforated_plate.remove(element)
        if delete_from_dict:
            self.group_elements_with_perforated_plate.pop(section) 
        else:
            self.group_elements_with_perforated_plate[section] = [perforated_plate, elements]

    def set_length_correction_by_element(self, elements, value, section, delete_from_dict=False):
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
            
        remove : boll, optional
            True if the ???????? have to be removed from the ???????? dictionary. False otherwise.
            Default is False.
        """
        for element in slicer(self.acoustic_elements, elements):
            element.acoustic_length_correction = value
            if element not in self.element_with_length_correction:
                self.element_with_length_correction.append(element)
            if value is None:
                if element in self.element_with_length_correction:
                    self.element_with_length_correction.remove(element)
        if delete_from_dict:
            self.group_elements_with_length_correction.pop(section) 
        else:
            self.group_elements_with_length_correction[section] = [value, elements]
            
    def set_acoustic_pressure_bc_by_node(self, nodes, data):
        """
        This method attributes acoustic pressure boundary condition to a list of nodes.

        Parameters
        ----------
        nodes : list
            Nodes external indexes.
            
        values : complex or array
            Acoustic pressure. Complex valued input corresponds to a constant pressure boundary condition with respect to the frequency. Array valued input corresponds to a variable pressure boundary condition with respect to the frequency.
        """
        try:
            [value, table_name] = data
            for node in slicer(self.nodes, nodes):
                node.acoustic_pressure = value
                node.acoustic_pressure_table_name = table_name
                if not node in self.nodes_with_acoustic_pressure:
                    self.nodes_with_acoustic_pressure.append(node)
                if value is None:
                    if node in self.nodes_with_acoustic_pressure:
                        self.nodes_with_acoustic_pressure.remove(node)
                node.volume_velocity = None
                node.volume_velocity_table = None
                if node in self.nodes_with_volume_velocity:
                    self.nodes_with_volume_velocity.remove(node)
                
                self.process_nodes_to_update_indexes_after_remesh(node)
                
        except Exception as log_error:
            title = "Error while setting acoustic pressure"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            return True  


    def set_volume_velocity_bc_by_node(self, nodes, data, additional_info=None):
        """
        This method attributes acoustic volume velocity load to a list of nodes.

        Parameters
        ----------
        nodes : list
            Nodes external indexes.
            
        values : complex or array
            Volume velocity. Complex valued input corresponds to a constant volume velocity load with respect to the frequency. Array valued input corresponds to a variable volume velocity load with respect to the frequency.
        """
        try:
            [values, table_name] = data
            for node in slicer(self.nodes, nodes):
                if node.volume_velocity is None or values is None:
                    node.volume_velocity = values
                    node.volume_velocity_table_name = table_name
                elif isinstance(node.volume_velocity, np.ndarray) and isinstance(values, np.ndarray):
                    if node.volume_velocity.shape == values.shape:
                        node.volume_velocity += values 
                    else:
                        title = "Error while setting volume velocity"
                        message = "The arrays lengths mismatch. It is recommended to check the frequency setup before continue."
                        message += "\n\nActual array length: {}\n".format(str(node.volume_velocity.shape).replace(",", ""))
                        message += "New array length: {}".format(str(values.shape).replace(",", ""))
                        PrintMessageInput([title, message, window_title_1])
                        return True 
                node.compressor_connection_info = None        
                if additional_info is not None:
                    node.compressor_connection_info = additional_info
                if node not in self.nodes_with_volume_velocity:
                    self.nodes_with_volume_velocity.append(node)
                if values is None:
                    self.volume_velocity_table_index = 0
                    if node in self.nodes_with_volume_velocity:
                        self.nodes_with_volume_velocity.remove(node)
                elif isinstance(values, np.ndarray):
                    self.volume_velocity_table_index += 1 
                node.acoustic_pressure = None
                node.acoustic_pressure_table_name = None
                if node in self.nodes_with_acoustic_pressure:
                    self.nodes_with_acoustic_pressure.remove(node)
                
                self.process_nodes_to_update_indexes_after_remesh(node)

        except Exception as error:
            title = "Error while setting volume velocity"
            message = str(error)
            PrintMessageInput([title, message, window_title_1])
            return True  

    def set_specific_impedance_bc_by_node(self, nodes, data):
        """
        This method attributes acoustic lumped specific impedance to a list of nodes.

        Parameters
        ----------
        nodes : list
            Nodes external indexes.
            
        values : complex or array, None
            Specific impedance. Complex valued input corresponds to a constant specific impedance with respect to the frequency. Array valued input corresponds to a variable specific impedance with respect to the frequency.

            If None is attributed, then no specific impedance is considered.
        """
        try:
            [values, table_name] = data
            for node in slicer(self.nodes, nodes):
                node.specific_impedance = values
                node.specific_impedance_table_name = table_name
                node.radiation_impedance = None
                node.radiation_impedance_type = None
                if not node in self.nodes_with_specific_impedance:
                    self.nodes_with_specific_impedance.append(node)
                if values is None:
                    if node in self.nodes_with_specific_impedance:
                        self.nodes_with_specific_impedance.remove(node)
                if node in self.nodes_with_radiation_impedance:
                    self.nodes_with_radiation_impedance.remove(node)
                
                self.process_nodes_to_update_indexes_after_remesh(node) 
        except Exception as error:
            title = "Error while setting specific impedance"
            message = str(error)
            PrintMessageInput([title, message, window_title_1])
            return True  


    def set_radiation_impedance_bc_by_node(self, nodes, impedance_type):
        """
        This method attributes acoustic lumped radiation impedance to a list of nodes according to the anechoic, flanged, and unflanged prescription.

        Parameters
        ----------
        nodes : list
            Nodes external indexes.
            
        impedance_type : [None, 0, 1, 2]
            Acoustic length correction due to acoustic discontinuities. The prescription is done through the following labeling:
            0 : anechoic termination
            1 : unflanged pipe
            2 : flanged pipe

            If None is attributed, then no radiation impedance is considered.
        """
        for node in slicer(self.nodes, nodes):
            node.radiation_impedance_type = impedance_type
            node.specific_impedance = None
            if not node in self.nodes_with_radiation_impedance:
                self.nodes_with_radiation_impedance.append(node)
            if impedance_type is None:
                if node in self.nodes_with_radiation_impedance:
                    self.nodes_with_radiation_impedance.remove(node)
            if node in self.nodes_with_specific_impedance:
                self.nodes_with_specific_impedance.remove(node)

            self.process_nodes_to_update_indexes_after_remesh(node)

    def get_radius(self):
        """
        This method updates and returns the ????.

        Returns
        ----------
        dictionary
            Radius at certain node.
        """
        self.radius = {}
        for element in self.structural_elements.values():
            first = element.first_node.global_index
            last  = element.last_node.global_index
            radius = element.cross_section.external_radius
            if self.radius.get(first, -1) == -1:
                self.radius[first] = radius
            elif self.radius[first] < radius:
                self.radius[first] = radius
            if self.radius.get(last, -1) == -1:
                self.radius[last] = radius
            elif self.radius[last] < radius:
                self.radius[last] = radius
        return self.radius


    def get_pipe_and_expansion_joint_elements_global_dofs(self):
        """
        This method returns the acoustic global degrees of freedom of the nodes associated to structural beam elements. 
        This method helps to exclude those degrees of freedom from acoustic analysis.

        Returns
        ----------
        list
            Acoustic global degrees of freedom associated to beam element.
        """
        # list_pipe_gdofs = []  
        pipe_gdofs = {}
        for element in self.structural_elements.values():
            if element.element_type in ['pipe_1', 'pipe_2', 'expansion_joint']:
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
        boll
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
        dict_structural_to_acoustic_elements = self.map_structural_to_acoustic_elements()
        for element in self.structural_elements.values():
            if element.element_type not in ['beam_1']:
                acoustic_element = dict_structural_to_acoustic_elements[element]
                acoustic_elements.append(acoustic_element)
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
        
    def get_gdofs_from_nodes(self, nodeID_1, nodeID_2):
        """
        This method returns the ordered global degrees of freedom of two nodes.

        Parameters
        ----------
        nodeID_1 : int
            Node 1 external index.

        nodeID_2 : int
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
        node_1 = self.nodes[nodeID_1]
        node_2 = self.nodes[nodeID_2]
        nodes_gdofs = np.array([node_1.global_dof, node_2.global_dof]).flatten()
        reord_gdofs = np.sort(nodes_gdofs)
        if  list(nodes_gdofs) == list(reord_gdofs):
            first_node = node_1
            last_node = node_2
        else:
            first_node = node_2
            last_node = node_1
        return reord_gdofs, first_node, last_node          

    def add_elastic_nodal_link(self, nodeID_1, nodeID_2, data, _stiffness=False, _damping=False):
        """
        This method ???????

        Parameters
        ----------
        nodeID_1 : int
            Node 1 external index.

        nodeID_2 : int
            Node 2 external index.

        parameters : ??????
            ???????.

        _stiffness : boll, optional
            True if ???????. False otherwise.
            Default is False.

        _damping : boll, optional
            True if ???????. False otherwise.
            Default is False.
        """
        if not (_stiffness or _damping):
            return

        [parameters, table_names] = data
        gdofs, node1, node2 = self.get_gdofs_from_nodes(nodeID_1, nodeID_2)        
        gdofs_node1 = gdofs[:DOF_PER_NODE_STRUCTURAL]
        gdofs_node2 = gdofs[DOF_PER_NODE_STRUCTURAL:]

        self.process_nodes_to_update_indexes_after_remesh(node1)
        self.process_nodes_to_update_indexes_after_remesh(node2)
        
        pos_data = parameters
        neg_data = [-value if value is not None else None for value in parameters]
        mask = [False if value is None else True for value in parameters]

        check_tables = [isinstance(value, np.ndarray) for value in parameters]

        if True in check_tables:
            node1.loaded_table_for_elastic_link_stiffness = True
            node2.loaded_table_for_elastic_link_stiffness = True
            node1.loaded_table_for_elastic_link_dampings = True
            node2.loaded_table_for_elastic_link_dampings = True
            value_labels = table_names
        else:
            value_labels = parameters
            node1.loaded_table_for_elastic_link_stiffness = False
            node2.loaded_table_for_elastic_link_stiffness = False
            node1.loaded_table_for_elastic_link_dampings = False
            node2.loaded_table_for_elastic_link_dampings = False

        indexes_i = [ [ gdofs_node1, gdofs_node2 ], [ gdofs_node1, gdofs_node2 ] ] 
        indexes_j = [ [ gdofs_node1, gdofs_node1 ], [ gdofs_node2, gdofs_node2 ] ] 
        out_data = [ [ pos_data, neg_data ], [ neg_data, pos_data ] ]
        element_matrix_info_node1 = [ indexes_i[0], indexes_j[0], out_data[0] ] 
        element_matrix_info_node2 = [ indexes_i[1], indexes_j[1], out_data[1] ] 

        min_node_ID = min(node1.external_index, node2.external_index)
        max_node_ID = max(node1.external_index, node2.external_index)
        key = "{}-{}".format(min_node_ID, max_node_ID)
        
        if _stiffness:
            self.nodes_with_elastic_link_stiffness[key] = [element_matrix_info_node1, element_matrix_info_node2]
            node1.elastic_nodal_link_stiffness[key] = [mask, value_labels]
            node2.elastic_nodal_link_stiffness[key] = [mask, value_labels]
            node1.there_are_elastic_nodal_link_stiffness = True
            node2.there_are_elastic_nodal_link_stiffness = True
        
        if _damping:
            self.nodes_with_elastic_link_dampings[key] = [element_matrix_info_node1, element_matrix_info_node2]
            node1.elastic_nodal_link_dampings[key] = [mask, value_labels]
            node2.elastic_nodal_link_dampings[key] = [mask, value_labels]
            node1.there_are_elastic_nodal_link_dampings = True
            node2.there_are_elastic_nodal_link_dampings = True


    def process_element_cross_sections_orientation_to_plot(self):
        """
        This method ???????
        """
        rotation_data = np.zeros((self.number_structural_elements, 3), dtype=float)
        for index, element in enumerate(self.structural_elements.values()):
            rotation_data[index,:] = element.mean_rotations_at_local_coordinate_system()   
        
        rotation_results_matrices = _transformation_matrix_Nx3x3_by_angles(rotation_data[:, 0], rotation_data[:, 1], rotation_data[:, 2])  
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
            xaxis_rotation_angle[index] = element.xaxis_beam_rotation 

        self.transformation_matrices = _transformation_matrix_3x3xN(delta_data[:,0], 
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

    def set_beam_xaxis_rotation_by_line(self, line, delta_angle, gimball_deviation=1e-5):

        self.dict_lines_to_rotation_angles[line] += delta_angle
        angle = self.dict_lines_to_rotation_angles[line]
        str_angle = str(angle)

        if angle in [90, 270]:
            angle -= gimball_deviation
        elif angle in [-90, -270]:
            angle += gimball_deviation
        angle *= np.pi/180

        for elements in slicer(self.line_to_elements, line):
            self.set_beam_xaxis_rotation_by_elements(elements, angle)
    
        if str_angle != "":
            temp_dict = self.dict_beam_xaxis_rotating_angle_to_lines.copy()
            if str_angle not in list(temp_dict.keys()):
                self.dict_beam_xaxis_rotating_angle_to_lines[str_angle].append(line)
                for key, lines in temp_dict.items():
                    if key != str_angle:
                        if line in lines:
                            self.dict_beam_xaxis_rotating_angle_to_lines[key].remove(line)
                    if self.dict_beam_xaxis_rotating_angle_to_lines[key] == []:
                        self.dict_beam_xaxis_rotating_angle_to_lines.pop(key)                            
            else:
                for key, lines in temp_dict.items():
                    if key != str_angle:
                        if line in lines:
                            self.dict_beam_xaxis_rotating_angle_to_lines[key].remove(line)
                    else:
                        if line not in lines:
                            self.dict_beam_xaxis_rotating_angle_to_lines[key].append(line)
                    if self.dict_beam_xaxis_rotating_angle_to_lines[key] == []:
                        self.dict_beam_xaxis_rotating_angle_to_lines.pop(key)

        temp_dict = self.dict_beam_xaxis_rotating_angle_to_lines.copy()              
        for key in ["0", "0.0"]:
            if key in list(temp_dict.keys()):
                self.dict_beam_xaxis_rotating_angle_to_lines.pop(key)
        
    def set_beam_xaxis_rotation_by_elements(self, elements, angle):
        for element in slicer(self.structural_elements, elements):
            element.xaxis_beam_rotation = angle

    def create_dict_lines_to_rotation_angles(self):
        self.dict_lines_to_rotation_angles = {}
        for line in self.all_lines:
            self.dict_lines_to_rotation_angles[line] = 0

    def process_nodes_to_update_indexes_after_remesh(self, node):
        """
        This method ...
        """        
        str_coord = str(node.coordinates)
        self.dict_coordinate_to_update_bc_after_remesh[str_coord] = node.external_index

    def update_node_ids_after_remesh(self, dict_cache, tolerance=1e-8):
        coord_matrix = self.nodal_coordinates_matrix_external
        list_coordinates = coord_matrix[:,1:].tolist()
        new_external_indexes = coord_matrix[:,0]
        self.dict_non_mapped_bcs = {}

        for key, old_external_index in dict_cache.items():
            list_key = key[1:-1].split(" ")
            coord = [float(_key) for _key in list_key if _key != ""]
            if coord in list_coordinates:
                ind = list_coordinates.index(coord)
                new_external_index = int(new_external_indexes[ind])
                self.dict_old_to_new_node_external_indexes[str(old_external_index)] = new_external_index
            else:
                diff = np.linalg.norm(coord_matrix[:,1:] - np.array(coord), axis=1)
                mask = diff < tolerance
                try:
                    new_external_index = int(coord_matrix[:,0][mask])
                    self.dict_old_to_new_node_external_indexes[str(old_external_index)] = new_external_index
                except:
                    self.dict_non_mapped_bcs[key] = old_external_index
        self.get_nodal_coordinates_matrix()
        return [self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs]


    def process_elements_to_update_indexes_after_remesh_in_entity_file(self, list_elements, reset_line=False, line_id=None, dict_map_cross={}, dict_map_expansion_joint={}):
        """
        This method ...
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
                line_id = self.elements_to_line[first_element_id]
                key = f"{first_element_id}-{last_element_id}||{line_id}"
                self.dict_element_info_to_update_indexes_in_entity_file[key] = [    list(first_node_coordinates),
                                                                                    list(last_node_coordinates),
                                                                                    subgroup_elements   ]


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
                line_id = self.elements_to_line[first_element_id]
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
                line = self.elements_to_line[element_id]
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


    def update_element_ids_after_remesh(self, dict_cache, tolerance=1e-8):
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

        return dict_old_to_new_list_of_elements, dict_non_mapped_subgroups


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


    # def get_model_checks(self):
    #     return BeforeRun(self)
                

    def deformed_amplitude_control_in_expansion_joints(self):
        """This method evaluates the deformed amplitudes in expansion joints nodes
        and reduces the amplitude through rescalling if higher levels are observed."""
        for element in self.elements_with_expansion_joint:

            results_lcs = element.element_results_lcs()
            delta_yz = sum(results_lcs[1:3]**2)**(1/2)
            
            if delta_yz > 3*self.element_size:
                value = element.joint_effective_diameter/6
                # print(f"Element: {element.index} <==> delta_yz: {delta_yz}")
                return True, value
            
            first_node = element.first_node
            last_node = element.last_node
            delta_x = abs(  (last_node.x + results_lcs[6]) - 
                            (first_node.x + results_lcs[0]) )

            if delta_x < self.element_size/3 or delta_x > 2*self.element_size: 
                value = self.element_size/2
                # print(f"Element: {element.index} <==> delta_yz: {delta_x}")
                return True, value

        return False, None


    #TODO: remove the following methods if they are not necessary anymore

    # def get_dict_line_to_nodes(self):
    #     # t0 = time()
    #     self.dict_line_to_nodes = {}
    #     for line_ID, list_elements in self.line_to_elements.items():
    #         # list_nodes = []
    #         list_nodes = np.zeros(len(list_elements)+1, dtype=int)
    #         for i, _id in enumerate(list_elements):
    #             element = self.structural_elements[_id]
    #             first_node_id = element.first_node.external_index
    #             last_node_id = element.last_node.external_index
    #             if i==0:
    #                 list_nodes[i] = first_node_id
    #             list_nodes[i+1] = last_node_id
    #             # if first_node_id not in list_nodes:
    #             #     list_nodes.append(first_node_id)
    #             # if last_node_id not in list_nodes:
    #             #     list_nodes.append(last_node_id)
    #         self.dict_line_to_nodes[line_ID] = list_nodes  
    #         # if line_ID in [1,2,3]:
    #         #     print(self.dict_line_to_nodes[line_ID])  
    #     # dt = time() - t0
    #     # print(f"Time to process : {dt}")


    # def get_beam_nodes_and_indexes(self, list_beam_elements):
    #     """
    #     This method returns the global indexes of the nodes associated to structural beam elements.

    #     Returns
    #     ----------
    #     list
    #         Nodes global indexes associated to beam element.
    #     """
    #     list_beam_nodes = []
    #     list_node_ids = []
    #     # print(len(list_beam_elements))
    #     self.get_nodes_connected_to_beam_and_pipe()#list_beam_elements)
    #     # list(self.nodes_with_multiples_neighbors.keys())
        
    #     # for element in self.structural_elements.values():
    #     for element in list_beam_elements:
    #         # if element.element_type in ['beam_1']:
            
    #         node_first = element.first_node
    #         node_last = element.last_node
            
    #         if node_first not in list_beam_nodes:
    #             list_beam_nodes.append(node_first)
    #             list_node_ids.append(node_first.global_index)
            
    #         if node_last not in list_beam_nodes:
    #             list_beam_nodes.append(node_last)
    #             list_node_ids.append(node_last.global_index)
                        
    #         if node_first in self.nodes_connected_to_beam_and_pipe:
    #             print(f'First node: {node_first.external_index}')
    #             list_beam_nodes.remove(node_first)
    #             list_node_ids.remove(node_first.global_index)

    #         if node_last in self.nodes_connected_to_beam_and_pipe:
    #             print(f'Last node: {node_last.external_index}')
    #             list_beam_nodes.remove(node_last) 
    #             list_node_ids.remove(node_last.global_index) 

    #     print(len(list_node_ids))
    #     return list_node_ids

    # def get_nodes_connected_to_beam_and_pipe(self):
    #     list_nodes_with_multiples_neighbors = list(self.nodes_with_multiples_neighbors.keys())
    #     self.dict_node_to_multiple_element_types = defaultdict(list)
    #     self.nodes_connected_to_beam_and_pipe = []
    #     for element in self.structural_elements.values():#list_beam_elements:
    #         first_node = element.first_node
    #         last_node = element.last_node
    #         if first_node in list_nodes_with_multiples_neighbors:
    #             self.dict_node_to_multiple_element_types[first_node].append(element.element_type)
    #         if last_node in list_nodes_with_multiples_neighbors:
    #             self.dict_node_to_multiple_element_types[last_node].append(element.element_type)
    #     for node, element_types in self.dict_node_to_multiple_element_types.items():
    #         if "beam_1" in element_types:
    #             if ("pipe_1" or "pipe_2") in element_types:
    #                 print(f"Node to remove: {node.external_index}")
    #                 # print(element_types)
    #                 self.nodes_connected_to_beam_and_pipe.append(node)
    #     print(len(self.nodes_connected_to_beam_and_pipe))