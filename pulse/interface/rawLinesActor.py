import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase
from pulse.utils import split_sequence, unwrap
from libs.gmsh import gmsh


class RawLinesActor(vtkActorBase):
    def __init__(self, path, project):
        super().__init__()

        self.path = path
        self.project = project

        self._data = vtk.vtkPolyData()
        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()

        self._nodes = []
        self._segments = []

        # PLACEHOLDER!!!
        # DO IT EXTERNALLY
        nodes, segments = self.test()
        self.set_data(nodes, segments)

    def test(self):
        '''
        REMOVE THIS LATER

        This example function returns two values: list of nodes, list of segments

        nodes are triples of numbers (x, y, z)
        segments are pairs of coordinates [(x0, y0, z0), (x1, y1, z1)]
        '''
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(self.path)
        gmsh.model.mesh.generate(dim=2)

        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        all_nodes = {i:c for i, c in zip(indexes, coords.reshape(-1, 3))}

        segments = []
        nodes = []

        for dim, tag in gmsh.model.getEntities(dim=1):
            _, indexes, points = gmsh.model.mesh.getElements(dim, tag)
            indexed_segments = list(split_sequence(unwrap(points), 2))
            for a, b in indexed_segments:
                segment = (all_nodes[a], all_nodes[b])
                segments.append(segment)

        for dim, tag in gmsh.model.getEntities(dim=0):
            _, indexes, points = gmsh.model.mesh.getElements(dim, tag)
            indexed_nodes = list(unwrap(points))
            for a in indexed_nodes:
                node = all_nodes[a]
                nodes.append(node)

        gmsh.finalize()
        return nodes, segments

    def set_data(self, nodes, segments):
        self._nodes = nodes
        self._segments = segments

    def source(self):
        segments = self._segments

        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        data.Allocate(len(segments))

        current_point = 0
        for origin, target in segments:
            points.InsertPoint(current_point, *origin)
            points.InsertPoint(current_point + 1, *target)
            data.InsertNextCell(vtk.VTK_LINE, 2, [current_point, current_point + 1])
            current_point += 2
        
        for x, y, z in self._nodes:
            points.InsertPoint(current_point, x, y, z)
            data.InsertNextCell(vtk.VTK_VERTEX, 1, [current_point])
            current_point += 1

        data.SetPoints(points)
        self._data = data

    def filter(self):
        pass 
    
    def map(self):
        self._source.Update()
        self._mapper.SetInputData(self._data)
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetLineWidth(3)
        self._actor.GetProperty().SetColor((0, 1, 0))
        self._actor.GetProperty().SetPointSize(6)
