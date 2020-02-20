from collections import deque
from random import choice

import gmsh 
import numpy as np

from pulse.geometry.node import Node
from pulse.geometry.element import Element
from pulse.utils import split_sequence, m_to_mm, mm_to_m


class Mesh:
    def __init__(self):
        self.reset_variables()

    def reset_variables(self):
        self.nodes = {}
        self.elements = {}
        self.neighbours = {}
        self.line_to_elements = {}

    def generate(self, path, element_size):
        self.reset_variables()
        self._initialize_gmsh(path)
        self._set_gmsh_options(element_size)
        self._create_entities()
        self._finalize_gmsh()
        self._load_neighbours()
        self._order_global_indexes()

    def prescribed_dof(self):
        global_prescribed = []
        for node in self.nodes.values():
            prescribed = node.boundary_condition.prescribed_dof + node.global_index
            global_prescribed.append(prescribed)
        return np.array(global_prescribed).flatten()

    def set_material_by_line(self, lines, material):
        if isinstance(lines, str) and lines == 'all':
            self.set_cross_section_by_element('all', material)

    def set_cross_section_by_line(self, lines, cross_section):
        if isinstance(lines, str) and lines == 'all':
            self.set_cross_section_by_element('all', cross_section)

    def set_material_by_element(self, elements, material):
        if isinstance(elements, str) and elements == 'all':
            for element in self.elements.values():
                element.material = material

    def set_cross_section_by_element(self, elements, cross_section):
        if isinstance(elements, str) and elements == 'all':
            for element in self.elements.values():
                element.cross_section = cross_section


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
        gmsh.model.mesh.removeDuplicateNodes()
        
        node_indexes, coords, _ = gmsh.model.mesh.getNodes(1, -1, True)
        _, element_indexes, connectivities = gmsh.model.mesh.getElements()

        self._create_nodes(node_indexes, coords)
        self._create_elements(element_indexes[0], connectivities[0])

    def _map_lines_to_elements(self):
        for dim, tag in gmsh.model.getEntities(1):
            self.line_to_elements[tag] = gmsh.model.mesh.getElements(dim, tag)[1][0]

    def _finalize_gmsh(self):
        gmsh.finalize()
    
    def _create_nodes(self, indexes, coords):
        for index, coord in zip(indexes, split_sequence(coords, 3)):
            x = mm_to_m(coord[0])
            y = mm_to_m(coord[1])
            z = mm_to_m(coord[2])
            self.nodes[index] = Node(x, y, z)

    def _create_elements(self, indexes, connectivities):
        for index, connectivity in zip(indexes, split_sequence(connectivities, 2)):
            first_node = self.nodes[connectivity[0]]
            last_node = self.nodes[connectivity[1]]
            self.elements[index] = Element(first_node, last_node)

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