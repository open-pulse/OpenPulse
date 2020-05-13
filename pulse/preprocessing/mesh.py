from collections import deque
from random import choice

import gmsh 
import numpy as np

from pulse.preprocessing.entity import Entity
from pulse.preprocessing.node import Node, DOF_PER_NODE_STRUCTURAL
from pulse.preprocessing.element import Element, NODES_PER_ELEMENT
from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer

class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.nodes = {}
        self.elements = {}
        self.neighbours = {}
        self.line_to_elements = {}
        self.entities = []
        self.nodesBC = []
        self.connectivity_matrix = []
        self.nodal_coordinates_matrix = []

    def generate(self, path, element_size):
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size)
        self._create_entities()
        self._map_lines_to_elements()
        self._finalize_gmsh()
        self._load_neighbours()
        self._order_global_indexes()
    
    # generate
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
        gmsh.option.setNumber('Geometry.Tolerance', 1e-06)

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

            self.entities.append(newEntity)

        gmsh.model.mesh.removeDuplicateNodes()

        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivity = gmsh.model.mesh.getElements()

        self.map_nodes = dict(zip(node_indexes, np.arange(1, len(node_indexes)+1, 1)))
        self.map_elements = dict(zip(element_indexes[0], np.arange(1, len(element_indexes[0])+1, 1)))
        
        self._create_nodes(node_indexes, coords, self.map_nodes)
        self._create_elements(element_indexes[0], connectivity[0], self.map_nodes, self.map_elements)  
        
    def _create_nodes(self, indexes, coords, map_nodes):
        for i, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[map_nodes[i]] = Node(x, y, z, external_index=int(map_nodes[i]))

    def _create_elements(self, indexes, connectivities, map_nodes, map_elements):
        for i, connect in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[map_nodes[connect[0]]]
            last_node  = self.nodes[map_nodes[connect[1]]]
            self.elements[map_elements[i]] = Element(first_node, last_node)

    def _map_lines_to_elements(self):
        mapping = self.map_elements
        for dim, tag in gmsh.model.getEntities(1):
            elements_of_entity = gmsh.model.mesh.getElements(dim, tag)[1][0]
            self.line_to_elements[tag] = np.array([mapping[element] for element in elements_of_entity], dtype=int)
 
    def _finalize_gmsh(self):
        gmsh.finalize()

    def _load_neighbours(self):
        self.neighbours = {}
        for element in self.elements.values():
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

    def load_mesh(self, coordinates, connectivity):

        coordinates = np.loadtxt(coordinates)
        connectivity = np.loadtxt(connectivity, dtype=int)

        newEntity = Entity(1)
        map_indexes = dict(zip(coordinates[:,0], np.arange(1, len(coordinates[:,0])+1, 1)))

        for i, x, y, z in coordinates:
            self.nodes[int(map_indexes[i])] = Node(x, y, z, external_index = int(map_indexes[i]))
            node = int(map_indexes[i]), x, y, z
            newEntity.insertNode(node)

        for i, nodes in enumerate(connectivity[:,1:]):
            first_node = self.nodes[map_indexes[nodes[0]]]
            last_node  = self.nodes[map_indexes[nodes[1]]]
            self.elements[i+1] = Element(first_node, last_node)
            edges = i+1, map_indexes[nodes[0]], map_indexes[nodes[1]]
            newEntity.insertEdge(edges)
            
        self.entities.append(newEntity)
        #Ordering global indexes
        for index, node in enumerate(self.nodes.values()):
            node.global_index = index

        self.get_nodal_coordinates_matrix()
        self.get_connectivity_matrix()

    def get_nodal_coordinates_matrix(self, reordering=True):
    # Returns the coordinates matrix for all nodes
    # output -> [index(internal), coord_x, coord_y, coord_z] if reordering=True
    # output -> [index(external), coord_x, coord_y, coord_z] if reordering=False
        self.nodesBC = []
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
    # Returns the connectivity matrix for all elements
    # output -> [index, first_node(internal), last_node(internal)] if reordering=True
    # output -> [index, first_node(external), last_node(external)] if reordering=False 
        number_elements = len(self.elements)
        connectivity = np.zeros((number_elements, NODES_PER_ELEMENT+1))
        if reordering:
            for index, element in enumerate(self.elements.values()):
                first = element.first_node.global_index
                last  = element.last_node.global_index
                connectivity[index,:] = index+1, first, last
        else:
            for index, element in enumerate(self.elements.values()):
                first = element.first_node.external_index
                last  = element.last_node.external_index
                connectivity[index,:] = index+1, first, last
        self.connectivity_matrix = connectivity.astype(int) 
        return 

    def get_global_indexes(self):
    # Returns the complete I and J indexes vector for assembly process
        # connect = self.get_connectivity_matrix()
        rows, cols = len(self.elements), DOF_PER_NODE_STRUCTURAL*NODES_PER_ELEMENT
        cols_nodes = self.connectivity_matrix[:,1:].astype(int)
        cols_dofs = cols_nodes.reshape(-1,1)*DOF_PER_NODE_STRUCTURAL + np.arange(6, dtype=int)
        cols_dofs = cols_dofs.reshape(rows, cols)
        J = np.tile(cols_dofs, cols)
        I = cols_dofs.reshape(-1,1)@np.ones((1,cols), dtype=int) 
        return I.flatten(), J.flatten()

    def _reset_global_indexes(self):
        for node in self.nodes.values():
            node.global_index = None

    def set_material_by_line(self, lines, material):
        for elements in slicer(self.line_to_elements, lines):
            self.set_material_by_element(elements, material)

    def set_cross_section_by_line(self, lines, cross_section):
        for elements in slicer(self.line_to_elements, lines):
            self.set_cross_section_by_element(elements, cross_section)

    def set_material_by_element(self, elements, material):
        for element in slicer(self.elements, elements):
            element.material = material

    def set_cross_section_by_element(self, elements, cross_section):
        for element in slicer(self.elements, elements):
            element.cross_section = cross_section

    def set_force_by_element(self, elements, loaded_force):
        for element in slicer(self.elements, elements):
            element.loaded_forces = loaded_force
    
    def set_force_by_node(self, nodes, loaded_force):
        for node in slicer(self.nodes, nodes):
            node.forces = loaded_force

    def add_mass_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.mass = values

    def add_spring_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.spring = values
    
    def add_damper_to_node(self, nodes, values):
        for node in slicer(self.nodes, nodes):
            node.damper = values

    def set_structural_boundary_condition_by_node(self, nodes, boundary_condition):
        for node in slicer(self.nodes, nodes):
            node.structural_boundary_condition = boundary_condition
            self.nodesBC.append(node)

# from collections import deque
# from random import choice

# import gmsh 
# import numpy as np

# from pulse.preprocessing.entity import Entity
# from pulse.preprocessing.node import Node, DOF_PER_NODE_STRUCTURAL
# from pulse.preprocessing.element import Element, NODES_PER_ELEMENT
# from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer

# class Mesh:
#     def __init__(self):
#         self.reset_variables()

#     def reset_variables(self):
#         self.nodes = {}
#         self.nodes_color = {}  #Nodes with duplicates
#         self.elements = {}
#         self.neighbours = {}
#         self.line_to_elements = {}
#         self.entities = []
#         self.nodesBC = []

#     def generate(self, path, element_size):
#         self.reset_variables()
#         self._initialize_gmsh(path)
#         self._set_gmsh_options(element_size)
#         self._create_entities()
#         self._map_lines_to_elements()
#         self._finalize_gmsh()
#         self._load_neighbours()
#         self._order_global_indexes()
    
#     def load_mesh(self, coordinates, connectivity):
#         newEntity = Entity(1)
#         for i, x, y, z in np.loadtxt(coordinates):
#             self.nodes[int(i)] = Node(x, y, z, external_index = int(i))
#             node = int(i), x, y, z
#             newEntity.insertNode(node)

#         for i, first, last in np.loadtxt(connectivity, dtype=int):
#             first_node = self.nodes[first]
#             last_node = self.nodes[last]
#             self.elements[i] = Element(first_node, last_node, first, last)
#             edges = i, first, last
#             newEntity.insertEdge(edges)
            
#         self.entities.append(newEntity)
#         self._simple_ordering()
      

#     def _simple_ordering(self):
#         for index, node in enumerate(self.nodes.values()):
#             node.global_index = index

#     def set_material_by_line(self, lines, material):
#         for elements in slicer(self.line_to_elements, lines):
#             self.set_material_by_element(elements, material)

#     def set_cross_section_by_line(self, lines, cross_section):
#         for elements in slicer(self.line_to_elements, lines):
#             self.set_cross_section_by_element(elements, cross_section)

#     def set_material_by_element(self, elements, material):
#         for element in slicer(self.elements, elements):
#             element.material = material

#     def set_cross_section_by_element(self, elements, cross_section):
#         for element in slicer(self.elements, elements):
#             element.cross_section = cross_section

#     def set_force_by_element(self, elements, loaded_force):
#         for element in slicer(self.elements, elements):
#             element.loaded_forces = loaded_force
    
#     def set_force_by_node(self, nodes, loaded_force):
#         for node in slicer(self.nodes, nodes):
#             node.forces = loaded_force

#     def add_mass_to_node(self, nodes, values):
#         for node in slicer(self.nodes, nodes):
#             node.mass = values

#     def add_spring_to_node(self, nodes, values):
#         for node in slicer(self.nodes, nodes):
#             node.spring = values
    
#     def add_damper_to_node(self, nodes, values):
#         for node in slicer(self.nodes, nodes):
#             node.damper = values

#     def set_structural_boundary_condition_by_node(self, nodes, boundary_condition):
#         for node in slicer(self.nodes, nodes):
#             node.structural_boundary_condition = boundary_condition

#     # generate
#     def _initialize_gmsh(self, path):
#         gmsh.initialize('', False)
#         gmsh.open(path)

#     def _set_gmsh_options(self, element_size):
#         gmsh.option.setNumber('Mesh.CharacteristicLengthMin', m_to_mm(element_size))
#         gmsh.option.setNumber('Mesh.CharacteristicLengthMax', m_to_mm(element_size))
#         gmsh.option.setNumber('Mesh.Optimize', 1)
#         gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
#         gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
#         gmsh.option.setNumber('Mesh.ElementOrder', 1)
#         gmsh.option.setNumber('Mesh.Algorithm', 2)
#         gmsh.option.setNumber('Mesh.Algorithm3D', 1)
#         gmsh.option.setNumber('Geometry.Tolerance', 1e-06)

#     def _create_entities(self):
#         gmsh.model.mesh.generate(3)
#         self._create_vector_entidades()
#         gmsh.model.mesh.removeDuplicateNodes()
        
#         node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
#         _, element_indexes, connectivities = gmsh.model.mesh.getElements()

#         self._create_nodes(node_indexes, coords)
#         self._create_elements(element_indexes[0], connectivities[0])

#     def _create_vector_entidades(self):
#         #Apenas temporario - Cópia do antigo mesh para gerar as linhas
#         #Atualizar futuramente

#         for i in gmsh.model.getEntities(1):
#             dim = i[0]
#             tag = i[1]

#             newEntity = Entity(tag)

#             #Element
#             _, index, connectivity = gmsh.model.mesh.getElements(dim, tag) 
#             index = index[0]
#             connectivity = connectivity[0]
#             connectivity = split_sequence(connectivity, 2)

#             for index, (start, end) in zip(index, connectivity):
#                 edges = index, start, end
#                 # print(edges)
#                 newEntity.insertEdge(edges)

#             #Nodes
#             index, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
#             coordinates = split_sequence(coordinates, 3)

#             for index, (x, y, z) in zip(index, coordinates):
#                 self.nodes_color[index] = Node(x/1000, y/1000, z/1000)
#                 node = index, x/1000, y/1000, z/1000
#                 newEntity.insertNode(node)

#             self.entities.append(newEntity)

#     def get_nodal_coordinates_matrix(self, reordering=True):
#     # Returns the coordinates matrix for all nodes
#     # output = [index, coord_x, coord_y, coord_z] 
#         self.nodesBC = []
#         number_nodes = len(self.nodes)
#         coordinates = np.zeros((number_nodes, 4))
#         if reordering:
#             for external_index, node in self.nodes.items():
#                 index = self.nodes[external_index].global_index
#                 if self.nodes[external_index].haveBoundaryCondition():
#                     self.nodesBC.append(self.nodes[external_index])
#                 coordinates[index,:] = index, node.x, node.y, node.z
#         else:               
#             for external_index, node in self.nodes.items():
#                 index = self.nodes[external_index].global_index
#                 if self.nodes[external_index].haveBoundaryCondition():
#                     self.nodesBC.append(self.nodes[external_index])
#                 coordinates[index,:] = external_index, node.x, node.y, node.z
#         return coordinates


#     def get_connectivity_matrix(self, reordering=True):
#     # Returns the connectivity matrix for all elements
#     # output = [index, first_node, last_node] 
#         number_elements = len(self.elements)
#         connectivity = np.zeros((number_elements, NODES_PER_ELEMENT+1))
#         ind = 0
#         if reordering:
#             for index, element in enumerate(self.elements.values()):
#                 first = element.first_node.global_index
#                 last  = element.last_node.global_index
#                 connectivity[ind,:] = index+1, first, last
#                 ind += 1
#         else:
#             for index, element in enumerate(self.elements.values()):
#                 first = element.first_node.external_index
#                 last  = element.last_node.external_index
#                 connectivity[ind,:] = index+1, first, last
#                 ind += 1
#         return connectivity.astype(int)

#     def _map_lines_to_elements(self):
#         for dim, tag in gmsh.model.getEntities(1):
#             self.line_to_elements[tag] = gmsh.model.mesh.getElements(dim, tag)[1][0]

#     def _finalize_gmsh(self):
#         gmsh.finalize()
    
#     def _create_nodes(self, indexes, coords):
#         for i, coord in zip(indexes, split_sequence(coords, 3)):
#             x = mm_to_m(coord[0])
#             y = mm_to_m(coord[1])
#             z = mm_to_m(coord[2])
#             self.nodes[i] = Node(x, y, z, external_index=int(i))

#     def _create_elements(self, indexes, connectivities):
#         for index, connectivity in zip(indexes, split_sequence(connectivities, 2)):
#             first_node = self.nodes[connectivity[0]]
#             last_node = self.nodes[connectivity[1]]
#             self.elements[index] = Element(first_node, last_node, connectivity[0], connectivity[1])

#     def _load_neighbours(self):
#         self.neighbours = {}
#         for element in self.elements.values():
#             if element.first_node not in self.neighbours:
#                 self.neighbours[element.first_node] = []

#             if element.last_node not in self.neighbours:
#                 self.neighbours[element.last_node] = []

#             self.neighbours[element.first_node].append(element.last_node)
#             self.neighbours[element.last_node].append(element.first_node)

#     def _order_global_indexes(self):
#         stack = deque()
#         index = 0
#         start_node = list(self.nodes.values())[0]
#         stack.appendleft(start_node)
#         while stack:
#             top = stack.pop()
            
#             if top.global_index is None:
#                 top.global_index = index
#                 index += 1
#             else:
#                 continue
            
#             for neighbour in self.neighbours[top]:
#                 if neighbour.global_index is None:
#                     stack.appendleft(neighbour)

#     def _reset_global_indexes(self):
#         for node in self.nodes.values():
#             node.global_index = None

