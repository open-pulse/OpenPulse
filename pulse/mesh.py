from os.path import isfile
from pulse.utils import split_sequence
import gmsh 

class Mesh:
    def __init__(self, path=''):
        self.path = path
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

    def reset_variables(self):
        self.nodes = []
        self.edges = []

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
        gmsh.model.mesh.removeDuplicateNodes()

    def __read_nodes(self):
        index, coordinates, _ = gmsh.model.mesh.getNodes()
        coordinates = split_sequence(coordinates, 3)

        for index, (x, y, z) in zip(index, coordinates):
            node = index, x, y, z
            self.nodes.append(node)

    def __read_edges(self):
        _, index, connectivity = gmsh.model.mesh.getElements() 
        index = index[0]
        connectivity = connectivity[0]
        connectivity = split_sequence(connectivity, 2)

        for index, (start, end) in zip(index, connectivity):
            edges = index, start, end
            self.edges.append(edges)

    def __finalize(self):
        gmsh.finalize()