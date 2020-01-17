import numpy as np 

class UnvReader:
    def __init__(self, path):
        self.path = path
        self.lines = None

        self.edges = dict()
        self.vertices = dict()

        self.read_lines()

    def get_edges_matrix(self):
        matrix = []
        for key, value in self.edges.items():
            line = [key, *value]
            matrix.append(line)
        return np.matrix(matrix)


    def get_vertice_matrix(self):
        matrix = []
        for key, value in self.vertices.items():
            line = [key, *value]
            matrix.append(line)
        return np.matrix(matrix)


    def read_lines(self):
        with open(self.path) as file:
            self.lines = file.readlines()
            self.lines = [i.strip() for i in self.lines]     

        if '2411' in self.lines:
            start = self.lines.index('2411')
            self.vertices = self.read_vertices(start)

        if '2412' in self.lines:
            start = self.lines.index('2412')
            self.edges = self.read_edges(start)

    def read_vertices(self, start):
        pos = start
        vertices = dict()

        while True:
            record1 = self.lines[pos+1].split()
            record2 = self.lines[pos+2].split()

            right_size = [
                len(record1) == 4,
                len(record2) == 3,
            ]

            if all(right_size):
                vertice_label = int(record1[0])
                x, y, z = self.get_coordinates(record2)
                vertices[vertice_label] = (x,y,z)
                pos += 2 
            else:
                return vertices
            
    def get_coordinates(self, line):
        x = line[0].replace('D', 'e')
        y = line[1].replace('D', 'e')
        z = line[2].replace('D', 'e')
        
        x, y, z = float(x), float(y), float(z)
        return x, y, z


    def read_edges(self, start):
        pos = start
        edges = dict()

        while True:
            record1 = self.lines[pos+1].split()
            record2 = self.lines[pos+2].split()
            record3 = self.lines[pos+3].split()

            right_size = [
                len(record1) == 6,
                len(record3) == 2,
            ]

            if all(right_size):
                edge_label = int(record1[0])
                start, end = record3
                start, end = int(start), int(end)
                edges[edge_label] = (start, end)
                pos += 3
            else:
                return edges
        