from os.path import isfile
from pulse.utils import split_sequence
from pulse.entity import Entity
from collections import deque
import gmsh 

class Mesh:
    def __init__(self, path=''):
        self.path = path
        self.nodes = []
        self.edges = []
        self.entities = []

    def reset_variables(self):
        self.nodes = []
        self.edges = []

    def generate(self, min_element_size=0, max_element_size=1e+019):
        if isfile(self.path):
            self.reset_variables()
            self.__initialize_gmsh()
            self.__set_gmsh_options(min_element_size, max_element_size)
            self.__generate_meshes()
            self.__read_nodes()
            self.__read_edges()
            self.__finalize()
        else:
            return FileNotFoundError

    def reorder_index_bfs(self):
        neighbors = self.get_neighbors()
        translator = {}
        stack = deque()
        index = 1

        stack.appendleft(self.nodes[0][0])

        while stack:
            top = stack.pop()

            if top not in translator:
                translator[top] = index
                index += 1
            else:
                continue 
            
            for neighbor in neighbors[top]:
                if neighbor not in translator:
                    stack.appendleft(neighbor)

        self.translate_index(translator)


    def reorder_index_dfs(self):
        neighbors = self.get_neighbors()
        translator = {}
        stack = deque()
        index = 0

        stack.append(self.nodes[0][0])

        while stack:
            top = stack.pop()

            if top not in translator:
                translator[top] = index
                index += 1
            else:
                continue 
            
            for neighbor in neighbors[top]:
                if neighbor not in translator:
                    stack.append(neighbor)

        self.translate_index(translator)

    def translate_index(self, translator):
        translated_nodes = []
        translated_edges = []

        for (index, x, y, z) in self.nodes:
            if index in translator:
                node = (translator[index], x/1000, y/1000, z/1000)
                translated_nodes.append(node)

        for index, (_, start, end) in enumerate(self.edges):
            if start and end in translator:
                edge = (index+1, translator[start], translator[end])
                translated_edges.append(edge)

        self.nodes = translated_nodes
        self.edges = translated_edges

    def get_neighbors(self):
        neighbors = {}

        for _, start, end in self.edges:
            if start not in neighbors:
                neighbors[start] = []

            if end not in neighbors:
                neighbors[end] = []

            neighbors[start].append(end)
            neighbors[end].append(start)

        return neighbors

    def __initialize_gmsh(self):
        gmsh.initialize('', False)
        gmsh.logger.stop()
        gmsh.merge(self.path)

    def __set_gmsh_options(self, min_element_size, max_element_size):
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', float(min_element_size) * 1000)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', float(max_element_size) * 1000)
        gmsh.option.setNumber('Mesh.Optimize', 1)
        gmsh.option.setNumber('Mesh.OptimizeNetgen', 0)
        gmsh.option.setNumber('Mesh.HighOrderOptimize', 0)
        gmsh.option.setNumber('Mesh.ElementOrder', 1)
        gmsh.option.setNumber('Mesh.Algorithm', 2)
        gmsh.option.setNumber('Mesh.Algorithm3D', 1)
        gmsh.option.setNumber('Geometry.Tolerance', 1e-06)

    def __generate_meshes(self):
        gmsh.model.mesh.generate(3)
        if (len(self.entities) != 0):
            self._reload_entities()
        else:
            self._create_entities()
        gmsh.model.mesh.removeDuplicateNodes()

    def __read_nodes(self):
        index, coordinates, _ = gmsh.model.mesh.getNodes(1, -1, True)
        coordinates = split_sequence(coordinates, 3)

        for index, (x, y, z) in zip(index, coordinates):
            node = index, x, y, z
            self.nodes.append(node)

    def __read_edges(self):
        for i in gmsh.model.getEntities(1):
            dim = i[0]
            tag = i[1]
            _, index, connectivity = gmsh.model.mesh.getElements(dim, tag) 
            index = index[0]
            connectivity = connectivity[0]
            connectivity = split_sequence(connectivity, 2)

            for index, (start, end) in zip(index, connectivity):
                edges = index, start, end, tag
                self.edges.append(edges)

    def _reload_entities(self):
        for i in gmsh.model.getEntities(1):
            dim = i[0]
            tag = i[1]

            newEntity = Entity(tag)
            for entity in self.entities:
                if (entity.tag == tag):
                    newEntity = entity
                    break

            newEntity.nodes = []
            newEntity.edges = []

            #Element
            _, index, connectivity = gmsh.model.mesh.getElements(dim, tag) 
            index = index[0]
            connectivity = connectivity[0]
            connectivity = split_sequence(connectivity, 2)

            for index, (start, end) in zip(index, connectivity):
                edges = index, start, end
                newEntity.insertEdge(edges)

            #Nodes
            index, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            coordinates = split_sequence(coordinates, 3)

            for index, (x, y, z) in zip(index, coordinates):
                node = index, x/1000, y/1000, z/1000
                newEntity.insertNode(node)

            #self.entities.append(newEntity)

    def _create_entities(self):
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
                newEntity.insertEdge(edges)

            #Nodes
            index, coordinates, _ = gmsh.model.mesh.getNodes(dim, tag, True)
            coordinates = split_sequence(coordinates, 3)

            for index, (x, y, z) in zip(index, coordinates):
                node = index, x/1000, y/1000, z/1000
                newEntity.insertNode(node)

            self.entities.append(newEntity)

    def __finalize(self):
        gmsh.finalize()
