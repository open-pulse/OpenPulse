import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase
from pulse.utils import split_sequence, unwrap
import gmsh

class RawLinesActor(vtkActorBase):
    def __init__(self):
        super().__init__()
        self._data = vtk.vtkPolyData()
        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._segments = []

    def load_file(self, path):
        '''
        segments are an index with a pairs of coordinates [i, (x0, y0, z0), (x1, y1, z1)]
        '''
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber("Mesh.MeshSizeFactor", 0.02)
        gmsh.open(str(path))
        gmsh.model.mesh.generate(dim=2)

        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        all_nodes = {i:c for i, c in zip(indexes, coords.reshape(-1, 3))}

        segments = []

        for dim, tag in gmsh.model.getEntities(dim=1):
            _, indexes, points = gmsh.model.mesh.getElements(dim, tag)
            indexed_segments = list(split_sequence(unwrap(points), 2))
            for a, b in indexed_segments:
                segment = (tag, all_nodes[a], all_nodes[b])
                segments.append(segment)

        gmsh.finalize()
        self.set_data(segments)

    def set_data(self, segments):
        self._segments = segments

    def source(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        data.Allocate(len(self._segments))

        current_point = 0
        for i, origin, target in self._segments:
            points.InsertPoint(current_point, *origin)
            points.InsertPoint(current_point + 1, *target)
            data.InsertNextCell(vtk.VTK_LINE, 2, [current_point, current_point + 1])
            current_point += 2

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
        self._actor.GetProperty().SetColor((0.8, 0.8, 0.8))
