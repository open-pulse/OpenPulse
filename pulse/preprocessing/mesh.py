from collections import deque
from random import choice
from collections import defaultdict
import gmsh 
import numpy as np
from time import time

from pulse.preprocessing.entity import Entity
from pulse.preprocessing.node import Node, DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.structural_element import StructuralElement, NODES_PER_ELEMENT
from pulse.preprocessing.acoustic_element import AcousticElement, NODES_PER_ELEMENT
from pulse.preprocessing.compressor_model import CompressorModel
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput

from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer, error, inverse_matrix_3x3, inverse_matrix_3x3xN, _rotation_matrix_3x3, _rotation_matrix_3x3xN

window_title1 = "ERROR"

class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.nodes = {}
        self.structural_elements = {}
        self.acoustic_elements = {}
        self.neighbours = {}
        self.dict_entities = {}
        self.line_to_elements = {}
        self.elements_to_line = {}
        self.group_elements_with_length_correction = {}
        self.group_elements_with_capped_end = {}
        self.group_elements_with_stress_stiffening = {}
        self.group_lines_with_capped_end = {}
        self.dict_lines_with_stress_stiffening = {}
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
        self.element_with_capped_end = []
        self.dict_elements_with_B2PX_rotation_decoupling = defaultdict(list)
        self.dict_nodes_with_B2PX_rotation_decoupling = defaultdict(list)

        self.dict_structural_element_type_to_lines = defaultdict(list)
        self.dict_acoustic_element_type_to_lines = defaultdict(list)

        self.dict_nodes_with_elastic_link_stiffness = {}
        self.dict_nodes_with_elastic_link_damping = {}
        self.lines_with_capped_end = []
        self.lines_with_stress_stiffening = []
        self.elements_with_adding_mass_effect = []
        self.radius = {}
        self.element_type = "pipe_1" # defined as default
        self.all_lines = []
        self.flag_fluid_mass_effect = False
        self.group_index = 0
        self.volume_velocity_table_index = 0
        self.DOFS_ELEMENT = DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT

    def generate(self, path, element_size):
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size)
        self._create_entities()
        self._map_lines_to_elements()
        self._finalize_gmsh()
        self._load_neighbours()
        self._order_global_indexes()
    
    def neighbour_elements_diameter(self):
        neighbour_diameters = dict()

        for index, element in self.structural_elements.items():
            first = element.first_node.external_index
            last = element.last_node.external_index
            neighbour_diameters.setdefault(first, [])
            neighbour_diameters.setdefault(last, [])

            external = element.cross_section.external_diameter
            internal = element.cross_section.internal_diameter

            neighbour_diameters[first].append((index, external, internal))
            neighbour_diameters[last].append((index, external, internal))

        return neighbour_diameters

    def neighbor_elements_diameter_global(self):
        neighbor_diameters = dict()
        for index, element in self.acoustic_elements.items():
            first = element.first_node.global_index
            last = element.last_node.global_index
            neighbor_diameters.setdefault(first, [])
            neighbor_diameters.setdefault(last, [])
            external = element.cross_section.external_diameter
            internal = element.cross_section.internal_diameter
            neighbor_diameters[first].append((index, external, internal))
            neighbor_diameters[last].append((index, external, internal))
        return neighbor_diameters    
    
    def neighboor_elements_of_node(self, node_ID):
        node = self.nodes[node_ID]
        neighboor_elments = defaultdict(list)      
        for element in self.acoustic_elements.values():
            first = element.first_node
            last = element.last_node
            if node in [first, last]:
                neighboor_elments[node].append(element.index)
        return neighboor_elments[node]

    def _initialize_gmsh(self, path):
        gmsh.initialize('', False)
        gmsh.open(path)

    def _set_gmsh_options(self, element_size):
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', m_to_mm(element_size))
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Geometry.Tolerance', 1e-08)

    def _create_entities(self):

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
            self.dict_entities[tag] = newEntity

        gmsh.model.mesh.removeDuplicateNodes()

        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivity = gmsh.model.mesh.getElements()

        self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
        self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))
        
        self._create_nodes(node_indexes, coords, self.map_nodes)
        self._create_structural_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)
        self._create_acoustic_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements) 
        
    def _create_nodes(self, indexes, coords, map_nodes):
        for i, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[map_nodes[i]] = Node(x, y, z, external_index=int(map_nodes[i]))

    def _create_structural_elements(self, indexes, connectivities, map_nodes, map_elements):
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.structural_elements[map_elements[i]] = StructuralElement(first_node, last_node, map_elements[i])

    def _create_acoustic_elements(self, indexes, connectivities, map_nodes, map_elements):
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.acoustic_elements[map_elements[i]] = AcousticElement(first_node, last_node, map_elements[i])

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
        if mesh_loaded:
            self.line_to_elements[1] = list(self.structural_elements.keys())
            for element in list(self.structural_elements.keys()):
                self.elements_to_line[element] = 1
        else:    
            mapping = self.map_elements
            for dim, tag in gmsh.model.getEntities(1):
                elements_of_entity = gmsh.model.mesh.getElements(dim, tag)[1][0]
                self.line_to_elements[tag] = np.array([mapping[element] for element in elements_of_entity], dtype=int)
                for element in elements_of_entity:
                    self.elements_to_line[mapping[element]] = tag 

    def _finalize_gmsh(self):
        gmsh.finalize()

    def _load_neighbours(self):
        self.neighbours = {}
        for element in self.structural_elements.values():
            if element.first_node not in self.neighbours:
                self.neighbours[element.first_node] = []

            if element.last_node not in self.neighbours:
                self.neighbours[element.last_node] = []

            self.neighbours[element.first_node].append(element.last_node)
            self.neighbours[element.last_node].append(element.first_node)

    def _order_global_indexes(self):
        stack = deque()
        index = 0
        start_node = list(self.nodes.values())[0]
        stack.appendleft(start_node)
        while stack:
            top = stack.pop()
            
            if top.global_index is None:
                top.global_index = index
                index += 1
            else:
                continue
            
            for neighbour in self.neighbours[top]:
                if neighbour.global_index is None:
                    stack.appendleft(neighbour)
        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        # t0 = time()
        self.process_all_rotation_matrices()
        # print("Time to process: ", time()-t0)
        # self._create_dict_gdofs_to_external_indexes()

    def load_mesh(self, coordinates, connectivity):

        coordinates = np.loadtxt(coordinates)
        connectivity = np.loadtxt(connectivity, dtype=int).reshape(-1,3)

        newEntity = Entity(1)
        map_indexes = dict(zip(coordinates[:,0], np.arange(1, len(coordinates[:,0])+1, 1)))

        for i, x, y, z in coordinates:
            self.nodes[int(map_indexes[i])] = Node(x, y, z, external_index = int(map_indexes[i]))
            node = int(map_indexes[i]), x, y, z
            newEntity.insertNode(node)

        for i, nodes in enumerate(connectivity[:,1:]):
            first_node = self.nodes[map_indexes[nodes[0]]]
            last_node  = self.nodes[map_indexes[nodes[1]]]
            self.structural_elements[i+1] = StructuralElement(first_node, last_node, i+1)
            self.acoustic_elements[i+1] = AcousticElement(first_node, last_node, i+1)
            edges = i+1, map_indexes[nodes[0]], map_indexes[nodes[1]]
            newEntity.insertEdge(edges)
            
        self.entities.append(newEntity)
        self.dict_entities[1] = newEntity
        #Ordering global indexes
        for index, node in enumerate(self.nodes.values()):
            node.global_index = index

        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()
        self.all_lines.append(1)
        self._map_lines_to_elements(mesh_loaded=True)
        self.process_all_rotation_matrices()
        # self._create_dict_gdofs_to_external_indexes()

    def get_nodal_coordinates_matrix(self, reordering=True):
    # Process the coordinates matrix for all nodes
    # if reordering=True  -> [index(internal), coord_x, coord_y, coord_z] 
    # if reordering=False -> [index(external), coord_x, coord_y, coord_z] 
        number_nodes = len(self.nodes)
        nodal_coordinates = np.zeros((number_nodes, 4))
        if reordering:
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                nodal_coordinates[index,:] = index, node.x, node.y, node.z
        else:               
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                nodal_coordinates[index,:] = external_index, node.x, node.y, node.z
        self.nodal_coordinates_matrix = nodal_coordinates
        return

    def get_connectivity_matrix(self, reordering=True):
        # process the connectivity matrix for all elements
        # if reordering=True  -> [index, first_node(internal), last_node(internal)] 
        # if reordering=False -> [index, first_node(external), last_node(external)]  
        number_elements = len(self.structural_elements)
        connectivity = np.zeros((number_elements, NODES_PER_ELEMENT+1))
        if reordering:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.global_index
                last  = element.last_node.global_index
                connectivity[index,:] = index+1, first, last
        else:
            for index, element in enumerate(self.structural_elements.values()):
                first = element.first_node.external_index
                last  = element.last_node.external_index
                connectivity[index,:] = index+1, first, last
        self.connectivity_matrix = connectivity.astype(int) 
        return 

    def get_global_structural_indexes(self):
        # Process the I and J indexes vector for assembly process
        rows, cols = len(self.structural_elements), DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)*DOF_PER_NODE_STRUCTURAL + np.arange(6, dtype=int)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()
    
    def get_global_acoustic_indexes(self):
        # Returns the I and J indexes vector for assembly process
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

    def get_dict_of_entities(self):
        dict_tag_entity={}
        for entity in self.entities:
            dict_tag_entity[entity.tag] = entity
        return dict_tag_entity

    def _reset_global_indexes(self):
        for node in self.nodes.values():
            node.global_index = None

    def set_structural_element_type_by_element(self, elements, element_type, remove=False):
        for element in slicer(self.structural_elements, elements):
            element.element_type = element_type
        if remove:
            self.dict_structural_element_type_to_lines.pop(element_type)
    
    def set_acoustic_element_type_by_element(self, elements, element_type, hysteretic_damping=None, remove=False):
        for element in slicer(self.acoustic_elements, elements):
            element.element_type = element_type
            element.hysteretic_damping = hysteretic_damping
        if remove:
            self.dict_acoustic_element_type_to_lines.pop(element_type)
    
    def set_cross_section_by_element(self, elements, cross_section, update_cross_section=False):
        if update_cross_section:
            # t0 = time()
            cross_section.update_properties()
            # dt = time() - t0
            # print("Time to process Cross-section: {} [s]".format(round(dt, 6)))
        for element in slicer(self.structural_elements, elements):
            element.cross_section = cross_section
        for element in slicer(self.acoustic_elements, elements):
            element.cross_section = cross_section

    def set_cross_section_by_line(self, line, cross_section):
        for elements in slicer(self.line_to_elements, line):
            self.set_cross_section_by_element(elements, cross_section)
    
    def set_structural_element_type_by_line(self, line, element_type, remove=False):
        for elements in slicer(self.line_to_elements, line):
            self.set_structural_element_type_by_element(elements, element_type)

        if remove:
            self.dict_structural_element_type_to_lines.pop(element_type)
        elif element_type != "":
            temp_dict = self.dict_structural_element_type_to_lines.copy()
            if element_type not in list(temp_dict.keys()):
                self.dict_structural_element_type_to_lines[element_type].append(line)
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

    def set_acoustic_element_type_by_line(self, line, element_type, hysteretic_damping=None, remove=False):
        for elements in slicer(self.line_to_elements, line):
            self.set_acoustic_element_type_by_element(elements, element_type, hysteretic_damping=hysteretic_damping)

        if remove:
            self.dict_acoustic_element_type_to_lines.pop(element_type)
        elif element_type != "":
            temp_dict = self.dict_acoustic_element_type_to_lines.copy()
            if element_type not in list(temp_dict.keys()):
                self.dict_acoustic_element_type_to_lines[element_type].append(line)
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
        for element in slicer(self.structural_elements, elements):
            element.material = material
        for element in slicer(self.acoustic_elements, elements):
            element.material = material

    def set_material_by_line(self, lines, material):
        for elements in slicer(self.line_to_elements, lines):
            self.set_material_by_element(elements, material)

    def set_force_by_element(self, elements, loads):
        for element in slicer(self.structural_elements, elements):
            element.loaded_forces = loads
    
    def set_structural_load_bc_by_node(self, nodes_id, values):
        for node in slicer(self.nodes, nodes_id):
            node.nodal_loads = values
            node.prescribed_dofs = [None,None,None,None,None,None]
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_nodal_loads = True
                node.there_are_nodal_loads = True
                if not node in self.nodes_with_nodal_loads:
                    self.nodes_with_nodal_loads.append(node)
                return
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

    def add_mass_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_masses = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_masses = True
                node.there_are_lumped_masses = True
                if not node in self.nodes_with_masses:
                    self.nodes_with_masses.append(node)
                return
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

    def add_spring_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_stiffness = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_stiffness = True
                node.there_are_lumped_stiffness = True
                if not node in self.nodes_connected_to_springs:
                    self.nodes_connected_to_springs.append(node)
                return
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
    
    def add_damper_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.lumped_dampings = values
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_lumped_dampings = True
                node.there_are_lumped_dampings = True
                if not node in self.nodes_connected_to_dampers:
                    self.nodes_connected_to_dampers.append(node)
                return
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

    def set_prescribed_dofs_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.prescribed_dofs = values
            node.nodal_loads = [None,None,None,None,None,None]
            # Checking imported tables 
            check_array = [isinstance(bc, np.ndarray) for bc in values]
            if True in check_array:
                node.loaded_table_for_prescribed_dofs = True
                node.there_are_prescribed_dofs = True
                if not node in self.nodes_with_constrained_dofs:
                    self.nodes_with_constrained_dofs.append(node)
                if not node in self.nodes_with_prescribed_dofs:
                    self.nodes_with_prescribed_dofs.append(node)
                return
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
        DOFS_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        N = DOF_PER_NODE_STRUCTURAL
        mat_ones = np.ones((DOFS_PER_ELEMENT,DOFS_PER_ELEMENT), dtype=int)

        neighboor_elements = self.neighboor_elements_of_node(node_ID)
        if len(neighboor_elements)<3:
            return mat_ones
        
        mat_base = np.array(  [[1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0],
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

    def set_stress_stiffening_by_line(self, lines, parameters, remove=False):
        if isinstance(lines, int):
            lines = [lines]
        for elements in slicer(self.line_to_elements, lines):
            self.set_stress_stiffening_by_elements(elements, parameters)
        if lines == "all":
            self.group_elements_with_stress_stiffening = {}
            self.lines_with_stress_stiffening = []
            if not remove:
                for line in self.all_lines:
                    self.lines_with_stress_stiffening.append(line)
                    self.dict_lines_with_stress_stiffening[line] = parameters
        else:
            for line in lines:
                if remove:
                    if line in self.lines_with_stress_stiffening:
                        self.lines_with_stress_stiffening.remove(line) 
                        self.dict_lines_with_stress_stiffening.pop(line)               
                else:
                    if line not in self.lines_with_stress_stiffening:
                        self.lines_with_stress_stiffening.append(line)
                        self.dict_lines_with_stress_stiffening[line] = parameters

    def set_stress_stiffening_by_elements(self, elements, parameters, section=None, remove=False):
        for element in slicer(self.structural_elements, elements):
            element.external_temperature = parameters[0]
            element.internal_temperature = parameters[1]
            element.external_pressure = parameters[2]
            element.internal_pressure = parameters[3]
            
            if section is not None:
                if remove:
                    if section in self.group_elements_with_stress_stiffening.keys():
                        self.group_elements_with_stress_stiffening.pop(section) 
                else:
                    self.group_elements_with_stress_stiffening[section] = [parameters, elements]

    def set_stress_intensification_by_element(self, elements, value):       
        for element in slicer(self.structural_elements, elements):
            element.stress_intensification = value

    def set_stress_intensification_by_line(self, lines, value):
        for elements in slicer(self.line_to_elements, lines):
            self.set_stress_intensification_by_element(elements, value)
            
    # Acoustic physical quantities
    def set_fluid_by_element(self, elements, fluid):
        for element in slicer(self.acoustic_elements, elements):
            element.fluid = fluid
        for element in slicer(self.structural_elements, elements):
            element.fluid = fluid
    
    def set_fluid_by_line(self, lines, fluid):
        for elements in slicer(self.line_to_elements, lines):
            self.set_fluid_by_element(elements, fluid)

    def set_length_correction_by_element(self, elements, value, section, delete_from_dict=False):

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
            
    def set_acoustic_pressure_bc_by_node(self, nodes, value):
        for node in slicer(self.nodes, nodes):
            node.acoustic_pressure = value
            node.volume_velocity = None
            if not node in self.nodes_with_acoustic_pressure:
                self.nodes_with_acoustic_pressure.append(node)
            if value is None:
                if node in self.nodes_with_acoustic_pressure:
                    self.nodes_with_acoustic_pressure.remove(node)

    def set_volume_velocity_bc_by_node(self, nodes, values):
        try:
            for node in slicer(self.nodes, nodes):
                if node.volume_velocity is None or values is None:
                    node.volume_velocity = values
                elif isinstance(node.volume_velocity, np.ndarray) and isinstance(values, np.ndarray):
                    if node.volume_velocity.shape == values.shape:
                        node.volume_velocity += values 
                    else:
                        title = "ERROR WHILE SETTING VOLUME VELOCITY"
                        message = "The arrays lengths mismatch. It is recommended to check the frequency setup before continue."
                        message += "\n\nActual array length: {}\n".format(str(node.volume_velocity.shape).replace(",", ""))
                        message += "New array length: {}".format(str(values.shape).replace(",", ""))
                        PrintMessageInput([title, message, window_title1])
                        return True  
                node.acoustic_pressure = None
                if not node in self.nodes_with_volume_velocity:
                    self.nodes_with_volume_velocity.append(node)
                if values is None:
                    if node in self.nodes_with_volume_velocity:
                        self.nodes_with_volume_velocity.remove(node)
                elif isinstance(values, np.ndarray):
                    self.volume_velocity_table_index += 1 
        except Exception as error:
            title = "ERROR WHILE SET VOLUME VELOCITY"
            message = str(error)
            PrintMessageInput([title, message, window_title1])
            return True  

    def set_specific_impedance_bc_by_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.specific_impedance = values
            node.radiation_impedance = None
            node.radiation_impedance_type = None
            if not node in self.nodes_with_specific_impedance:
                self.nodes_with_specific_impedance.append(node)
            if values is None:
                if node in self.nodes_with_specific_impedance:
                    self.nodes_with_specific_impedance.remove(node)
            if node in self.nodes_with_radiation_impedance:
                self.nodes_with_radiation_impedance.remove(node)
                    
    def set_radiation_impedance_bc_by_node(self, nodes, impedance_type):
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

    def get_radius(self):
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

    def get_beam_elements_global_dofs(self):
        list_gdofs = []  
        for element in self.structural_elements.values():
            if element.element_type in ['beam_1']:
                
                gdofs_node_first = element.first_node.global_index
                gdofs_node_last = element.last_node.global_index
                
                if gdofs_node_first not in list_gdofs:
                    list_gdofs.append(gdofs_node_first)
                
                if gdofs_node_last not in list_gdofs:
                    list_gdofs.append(gdofs_node_last)
                
                elements_node_first = self.neighboor_elements_of_node(element.first_node.external_index)
                elements_node_last = self.neighboor_elements_of_node(element.last_node.external_index)

                if len(elements_node_first) > 2:
                    list_gdofs.remove(gdofs_node_first)
                if len(elements_node_last) > 2:
                    list_gdofs.remove(gdofs_node_last) 

        beam_gdofs = np.array(list_gdofs).flatten()
        return beam_gdofs

    def get_pipe_elements_global_dofs(self):
        self.beam_gdofs = self.get_beam_elements_global_dofs()
        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.nodes)
        all_indexes = np.arange(total_dof)
        pipe_gdofs = np.delete(all_indexes, self.beam_gdofs)
        return pipe_gdofs

    def get_beam_nodes_and_indexes(self):
        list_beam_nodes = []
        list_node_ids = []
        for element in self.structural_elements.values():
            if element.element_type in ['beam_1']:
                
                node_first = element.first_node
                node_last = element.last_node
                
                if node_first not in list_beam_nodes:
                    list_beam_nodes.append(node_first)
                    list_node_ids.append(node_first.global_index)
                
                if node_last not in list_beam_nodes:
                    list_beam_nodes.append(node_last)
                    list_node_ids.append(node_last.global_index)
                
                elements_node_first = self.neighboor_elements_of_node(element.first_node.external_index)
                elements_node_last = self.neighboor_elements_of_node(element.last_node.external_index)

                if len(elements_node_first) > 2:
                    list_beam_nodes.remove(node_first)
                    list_node_ids.remove(node_first.global_index)

                if len(elements_node_last) > 2:
                    list_beam_nodes.remove(node_last) 
                    list_node_ids.remove(node_last.global_index) 

        # return list_beam_nodes, list_node_ids
        return list_node_ids
        
    def _process_beam_nodes_and_indexes(self):
        list_beam_elements = self.get_beam_elements()
        if len(list_beam_elements) == len(self.structural_elements):
            self.list_beam_node_ids = list(np.arange(len(self.nodes)))
            return True
        else:
            self.list_beam_node_ids = self.get_beam_nodes_and_indexes()
            return False

    def get_pipe_elements(self):
        list_elements = []
        dict_structural_to_acoustic_elements = self.map_structural_to_acoustic_elements()
        for element in self.structural_elements.values():
            if element.element_type not in ['beam_1']:
                list_elements.append(dict_structural_to_acoustic_elements[element])
        return list_elements   
    
    def get_beam_elements(self):
        list_elements = []
        dict_structural_to_acoustic_elements = self.map_structural_to_acoustic_elements()
        for element in self.structural_elements.values():
            if element.element_type in ['beam_1']:
                list_elements.append(dict_structural_to_acoustic_elements[element])
        return list_elements

    def check_material_all_elements(self):
        self.check_set_material = False
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return

    def check_poisson_all_elements(self):
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material.poisson_ratio == 0:
                self.check_poisson = True
                return

    def check_material_and_cross_section_in_all_elements(self):
        self.check_set_material = False
        self.check_set_crossSection = False
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return
            if element.cross_section is None:
                self.check_set_crossSection = True
                return
            if element.cross_section.thickness == 0:
                if element.cross_section.area == 0:
                    self.check_set_crossSection = True
                    return

    def check_fluid_and_cross_section_in_all_elements(self):
        self.check_set_fluid = False
        self.check_set_crossSection = False
        for element in self.acoustic_elements.values():
            if element.fluid is None:
                self.check_set_fluid = True
                return
            if element.cross_section is None:
                self.check_set_crossSection = True
                return
            if element.cross_section.thickness == 0:
                if element.cross_section.area == 0:
                    self.check_set_crossSection = True
                    return

    
    def check_nodes_attributes(self, acoustic=False, structural=False, coupled=False):
        self.is_there_loads = False
        self.is_there_prescribed_dofs = False
        self.is_there_acoustic_pressure = False
        self.is_there_volume_velocity = False
        for node in self.nodes.values():

            if structural:
                if node.there_are_nodal_loads:
                    self.is_there_loads = True
                    return

                if node.there_are_prescribed_dofs:
                    if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                        self.is_there_prescribed_dofs = True
                        return

                    elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                        self.is_there_prescribed_dofs = True
                        return

            if acoustic or coupled:
                if node.acoustic_pressure is not None:
                    self.is_there_acoustic_pressure = True
                    return

                if node.volume_velocity is not None:
                    self.is_there_volume_velocity = True
                    return    
    
    def get_cross_section_points(self, element_ID):

        labels = ["Pipe section", "Rectangular section", "Circular section", "C-section", "I-section", "T-section", "Generic section"]
        dict_sections = dict(zip(labels, np.arange(7)))

        element = self.structural_elements[element_ID]
        section_label, section_parameters, *args = element.cross_section.additional_section_info
        section_type = dict_sections[section_label]

        if section_type == 0: # Pipe section - It's a pipe section, so ignore for beam plots
            # return 0, 0, 0, 0
            N = element.cross_section.division_number
            d_out, thickness, offset_y, offset_z, insulation_thickness = section_parameters
            Yc, Zc = offset_y, offset_z

            d_theta = np.pi/N
            theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)
            d_in = d_out - 2*thickness

            Yp_out = (d_out/2)*np.cos(theta)
            Zp_out = (d_out/2)*np.sin(theta)
            Yp_in = (d_in/2)*np.cos(-theta)
            Zp_in = (d_in/2)*np.sin(-theta)

            Yp_list = [list(Yp_out), list(Yp_in),[0]]
            Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]
            Yp_left = -np.flip(Yp_right)
            Zp_left = np.flip(Zp_right)

            Ys = np.array([Yp_right, Yp_left]).flatten() + Yc
            Zs = np.array([Zp_right, Zp_left]).flatten() + Zc

            if insulation_thickness != float(0):
                Yp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.cos(theta)
                Zp_out_ins = ((d_out + 2*insulation_thickness)/2)*np.sin(theta)
                Yp_in_ins = (d_out/2)*np.cos(-theta)
                Zp_in_ins = (d_out/2)*np.sin(-theta)

                Yp_list_ins = [list(Yp_out_ins), list(Yp_in_ins), [0]]
                Zp_list_ins = [list(Zp_out_ins), list(Zp_in_ins), [-(d_out/2)]]

                Yp_right_ins = [value for _list in Yp_list_ins for value in _list]
                Zp_right_ins = [value for _list in Zp_list_ins for value in _list]
                Yp_left_ins = -np.flip(Yp_right_ins)
                Zp_left_ins = np.flip(Zp_right_ins)

                Ys = np.array([Yp_right_ins, Yp_left_ins]).flatten() + Zc
                Zs = np.array([Zp_right_ins, Zp_left_ins]).flatten() + Yc

        if section_type == 1: # Rectangular section

            b, h, b_in, h_in, Yc, Zc = section_parameters
            if b_in == 0:
                Ys = [(b/2), (b/2), -(b/2), -(b/2)]
                Zs = [-(h/2), (h/2), (h/2), -(h/2)]
            else:
                Ys = [(b/2), (b/2), -(b/2), -(b/2), (b_in/2), (b_in/2), -(b_in/2),  -(b_in/2)]
                Zs = [-(h/2), (h/2), (h/2), -(h/2), -(h_in/2), (h_in/2), (h_in/2), -(h_in/2)]

        elif section_type == 2: # Circular section
            
            N = 60# element.cross_section.division_number
            d_out, d_in, Yc, Zc = section_parameters
            
            d_theta = np.pi/N
            theta = np.arange(0, (2*np.pi)+d_theta, d_theta)

            Yp_out = (d_out/2)*np.cos(theta)
            Zp_out = (d_out/2)*np.sin(theta)
            Yp_in = (d_in/2)*np.cos(-theta)
            Zp_in = (d_in/2)*np.sin(-theta)

            Yp_list = [list(Yp_out), list(Yp_in), [0]]
            Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]

            Yp_right = [value for _list in Yp_list for value in _list]
            Zp_right = [value for _list in Zp_list for value in _list]

            Yp_left = -np.flip(Yp_right)
            Zp_left = np.flip(Zp_right)

            Ys = np.array([Yp_right, Yp_left]).flatten()
            Zs = np.array([Zp_right, Zp_left]).flatten()

        elif section_type == 3: # Beam: C-section

            h, w1, w2, w3, t1, t2, t3, _, Yc, Zc = section_parameters
            Yp = [0, w3, w3, w2, w2, w1, w1, 0]
            Zp = [-(h/2), -(h/2), -((h-t3)/2), -((h-t3)/2), ((h-t1)/2), ((h-t1)/2), (h/2), (h/2)]

            Ys = list(np.array(Yp)-Yc)
            Zs = list(np.array(Zp)-Zc)

        elif section_type == 4: # Beam: I-section

            h, w1, w2, w3, t1, t2, t3, _, Yc, Zc = section_parameters
            Yp = [(w3/2), (w3/2), (w2/2), (w2/2), (w1/2), (w1/2), -(w1/2), -(w1/2), -(w2/2), -(w2/2), -((w3/2)), -((w3/2))]
            Zp = [-(h/2), -(h/2)+t3, -(h/2)+t3, (h/2)-t1, (h/2)-t1, (h/2), (h/2), (h/2)-t1, (h/2)-t1, -(h/2)+t3, -(h/2)+t3, -(h/2)]

            Ys = list(np.array(Yp)-Yc)
            Zs = list(np.array(Zp)-Zc)

        elif section_type == 5: # Beam: T-section

            h, w1, w2, t1, t2, _, Yc, Zc = section_parameters
            Yp = [(w2/2), (w2/2), (w1/2), (w1/2), -(w1/2), -(w1/2), -(w2/2), -(w2/2)]
            Zp = [-(t2/2), (t2/2), (t2/2), (t2/2)+t1, (t2/2)+t1, (t2/2), (t2/2), -(t2/2)]

            Ys = list(np.array(Yp)-Yc)
            Zs = list(np.array(Zp)-Zc)
        
        else:
            # A very small triangle to prevent bugs
            Ys = [0, 1e-10, 0]
            Zs = [0, 0, 1e-10]

        # elif section_type == 6: # Beam: Generic section
    
            # message = "The GENERIC BEAM SECTION cannot be ploted."
            # title = "Error while graphing cross-section"
            # info_text = [title, message]
            # PrintMessageInput(info_text)

            # return 0, 0, 0, 0

        
        # for k in range(len(Yp)):
        #     dict_lines_to_points[k+1] = [list_indexes[k], list_indexes[k+1]] 

        return Ys, Zs#, Yc, Zc, dict_lines_to_points

    def add_compressor_excitation(self, parameters):
                
        list_parameters = []
        for key, parameter in parameters.items():
            if key != 'cylinder label':
                list_parameters.append(parameter)

        if 'cylinder label' in parameters.keys():
            CompressorModel(list_parameters, active_cyl=parameters['cylinder label'])
        else:
            CompressorModel(list_parameters)
        
    def get_gdofs_from_nodes(self, nodeID_1, nodeID_2):
        
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

    def add_elastic_nodal_link(self, nodeID_1, nodeID_2, parameters, _stiffness=False, _damping=False):

        if not (_stiffness or _damping):
            return

        gdofs, node1, node2 = self.get_gdofs_from_nodes(nodeID_1, nodeID_2)        
        gdofs_node1 = gdofs[:DOF_PER_NODE_STRUCTURAL]
        gdofs_node2 = gdofs[DOF_PER_NODE_STRUCTURAL:]

        pos_data = parameters
        neg_data = [-value if value is not None else None for value in parameters]
        mask = [False if value is None else True for value in parameters]

        check_tables = [isinstance(value, np.ndarray) for value in parameters]

        if True in check_tables:
            node1.loaded_table_for_elastic_link_stiffness = True
            node2.loaded_table_for_elastic_link_damping = True
            value_labels = ["Table"]*check_tables.count(True)
        else:
            value_labels = np.array(parameters)[mask]
            node1.loaded_table_for_elastic_link_stiffness = False
            node2.loaded_table_for_elastic_link_stiffness = False
            node1.loaded_table_for_elastic_link_damping = False
            node2.loaded_table_for_elastic_link_damping = False
            
        indexes_i = [ [ gdofs_node1, gdofs_node2 ], [ gdofs_node1, gdofs_node2 ] ] 
        indexes_j = [ [ gdofs_node1, gdofs_node1 ], [ gdofs_node2, gdofs_node2 ] ] 
        out_data = [ [ pos_data, neg_data ], [ neg_data, pos_data ] ]
        element_matrix_info_node1 = [ indexes_i[0], indexes_j[0], out_data[0] ] 
        element_matrix_info_node2 = [ indexes_i[1], indexes_j[1], out_data[1] ] 

        key = "{}-{}".format(node1.external_index, node2.external_index)
        
        if _stiffness:
            self.dict_nodes_with_elastic_link_stiffness[key] = [element_matrix_info_node1, element_matrix_info_node2]
            node1.elastic_nodal_link_stiffness[key] = [mask, value_labels]
            node2.elastic_nodal_link_stiffness[key] = [mask, value_labels]
            node1.there_are_elastic_nodal_link_stiffness = True
            node2.there_are_elastic_nodal_link_stiffness = True
        
        if _damping:
            self.dict_nodes_with_elastic_link_damping[key] = [element_matrix_info_node1, element_matrix_info_node2]
            node1.elastic_nodal_link_damping[key] = [mask, value_labels]
            node2.elastic_nodal_link_damping[key] = [mask, value_labels]
            node1.there_are_elastic_nodal_link_damping = True
            node2.there_are_elastic_nodal_link_damping = True

    def process_inverse_of_all_deformed_elements(self):
        delta_data = np.zeros((len(self.structural_elements), 3), dtype=float)
        for index, element in enumerate(self.structural_elements.values()):
            delta_data[index, :] = element.last_node.deformed_coordinates - element.first_node.deformed_coordinates 
            # element.deformed_center_element_coordinates = (element.last_node.deformed_coordinates + element.first_node.deformed_coordinates)/2 
        mat_rotation_data = _rotation_matrix_3x3xN(delta_data[:,0], delta_data[:,1], delta_data[:,2])    
        output_data = inverse_matrix_3x3xN(mat_rotation_data)
        for index, element in enumerate(self.structural_elements.values()):
            element.deformed_directional_vectors = output_data[index,:,:]
 
    def process_all_rotation_matrices(self):
        delta_data = np.zeros((len(self.structural_elements), 3), dtype=float)
        for index, element in enumerate(self.structural_elements.values()):
            delta_data[index,:] = element.delta_x, element.delta_y, element.delta_z
        mat_rotation_data = _rotation_matrix_3x3xN(delta_data[:,0], delta_data[:,1], delta_data[:,2])
        output_data = inverse_matrix_3x3xN(mat_rotation_data)
        for index, element in enumerate(self.structural_elements.values()):
            element.sub_rotation_matrix = mat_rotation_data[index, :, :]
            element.directional_vectors = output_data[index, :, :]
             
    # def process_all_rotation_matrices(self):
    #     for element in self.structural_elements.values():
    #         element.sub_rotation_matrix = _rotation_matrix_3x3(element.delta_x, element.delta_y, element.delta_z)
