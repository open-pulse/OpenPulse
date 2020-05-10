from collections import deque
from random import choice

import gmsh 
import numpy as np

from pulse.preprocessing.entity import Entity
from pulse.preprocessing.node import Node, DOF_PER_NODE
from pulse.preprocessing.element import Element, NODES_PER_ELEMENT
from pulse.utils import split_sequence, m_to_mm, mm_to_m, slicer


class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.nodes = {}
        self.nodes_color = {}  #Nodes with duplicates
        self.elements = {}
        self.neighbours = {}
        self.line_to_elements = {}
        self.entities = []

    def generate(self, path, element_size):
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size)
        self._create_entities()
        self._map_lines_to_elements()
        self._finalize_gmsh()
        self._load_neighbours()
        self._order_global_indexes()
    
    def load_mesh(self, coordinates, connectivity):
        newEntity = Entity(1)
        for i, x, y, z in np.loadtxt(coordinates):
            self.nodes[int(i)] = Node(x, y, z, external_index = int(i))
            node = int(i), x, y, z
            newEntity.insertNode(node)

        for i, first, last in np.loadtxt(connectivity, dtype=int):
            first_node = self.nodes[first]
            last_node = self.nodes[last]
            self.elements[i] = Element(first_node, last_node, first, last)
            edges = i, first, last
            newEntity.insertEdge(edges)
            
        self.entities.append(newEntity)
        self._simple_ordering()
      

    def _simple_ordering(self):
        for index, node in enumerate(self.nodes.values()):
            node.global_index = index

    def get_prescribed_indexes(self):
        global_prescribed = []
        for node in self.nodes.values():
            starting_position = node.global_index * DOF_PER_NODE
            dofs = np.array(node.get_boundary_condition_indexes()) + starting_position
            global_prescribed.extend(dofs)
        return global_prescribed

    def get_unprescribed_indexes(self):
        total_dof = DOF_PER_NODE * len(self.nodes)
        all_indexes = np.arange(total_dof)
        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = np.delete(all_indexes, prescribed_indexes)
        return unprescribed_indexes

    def get_prescribed_values(self):
        global_prescribed = []
        for node in self.nodes.values():
            global_prescribed.extend(node.get_boundary_condition_values())
        return global_prescribed

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

    def set_boundary_condition_by_node(self, nodes, boundary_condition):
        for node in slicer(self.nodes, nodes):
            node.boundary_condition = boundary_condition

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
        self._create_vector_entidades()
        gmsh.model.mesh.removeDuplicateNodes()
        
        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivities = gmsh.model.mesh.getElements()

        self._create_nodes(node_indexes, coords)
        self._create_elements(element_indexes[0], connectivities[0])

    def _create_vector_entidades(self):
        #Apenas temporario - Cópia do antigo mesh para gerar as linhas
        #Atualizar futuramente

        for i in gmsh.model.getEntities(1):
            dim = i[0]
            tag = i[1]

            newEntity = Entity(tag)

            #Element
            _, index, connectivity = gmsh.model.mesh.getElements(dim, tag) 
            index = index[0]
            connectivity = connectivity[0]
            connectivity = split_sequence(connectivity, 2)

            for index, (start, end) in zip(index, connectivity):
                edges = index, start, end
                # print(edges)
                newEntity.insertEdge(edges)

            #Nodes
            index, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            coordinates = split_sequence(coordinates, 3)

            for index, (x, y, z) in zip(index, coordinates):
                self.nodes_color[index] = Node(x/1000, y/1000, z/1000)
                node = index, x/1000, y/1000, z/1000
                newEntity.insertNode(node)

            self.entities.append(newEntity)

    def get_nodal_coordinates_matrix(self, reordering=True):
    # Returns the coordinates matrix for all nodes
    # output = [index, coord_x, coord_y, coord_z] 
        number_nodes = len(self.nodes)
        coordinates = np.zeros((number_nodes, 4))
        if reordering:
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                coordinates[index,:] = index, node.x, node.y, node.z
        else:               
            for external_index, node in self.nodes.items():
                index = self.nodes[external_index].global_index
                coordinates[index,:] = external_index, node.x, node.y, node.z
        return coordinates



    def get_connectivity_matrix(self, reordering=True):
    # Returns the connectivity matrix for all elements
    # output = [index, first_node, last_node] 
        number_elements = len(self.elements)
        connectivity = np.zeros((number_elements, NODES_PER_ELEMENT+1))
        ind = 0
        if reordering:
            for index, element in enumerate(self.elements.values()):
                first = element.first_node.global_index
                last  = element.last_node.global_index
                connectivity[ind,:] = index+1, first, last
                ind += 1
        else:
            for index, element in enumerate(self.elements.values()):
                first = element.first_node.external_index
                last  = element.last_node.external_index
                connectivity[ind,:] = index+1, first, last
                ind += 1
        return connectivity.astype(int)

    def _map_lines_to_elements(self):
        for dim, tag in gmsh.model.getEntities(1):
            self.line_to_elements[tag] = gmsh.model.mesh.getElements(dim, tag)[1][0]

    def _finalize_gmsh(self):
        gmsh.finalize()
    
    def _create_nodes(self, indexes, coords):
        for i, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[i] = Node(x, y, z, external_index=int(i))

    def _create_elements(self, indexes, connectivities):
        for index, connectivity in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[connectivity[0]]
            last_node = self.nodes[connectivity[1]]
            self.elements[index] = Element(first_node, last_node, connectivity[0], connectivity[1])

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

    def _reset_global_indexes(self):
        for node in self.nodes.values():
            node.global_index = None