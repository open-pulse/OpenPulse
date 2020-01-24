from pulse.utils import split_sequence
import gmsh 

class Mesh:
    def __init__(self, min_len=0, max_len=1e+022):
        self.min_len = min_len
        self.max_len = max_len 

        self.nodes = []
        self.edges = []

    def generate(self, path):
        self.__initialize_gmsh(path)
        self.__set_gmsh_options()
        self.__generate_meshes()
        self.__read_nodes()
        self.__read_edges()
        self.__finalize()

    def __initialize_gmsh(self, path):
        gmsh.initialize('', False)
        gmsh.logger.stop()
        gmsh.merge(path)

    def __set_gmsh_options(self):
        gmsh.option.setNumber('Mesh.CharacteristicLengthMin', 0)
        gmsh.option.setNumber('Mesh.CharacteristicLengthMax', 100)
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