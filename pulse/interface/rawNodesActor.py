import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase
from pulse.utils import split_sequence, unwrap
from libs.gmsh import gmsh


class RawNodesActor(vtkActorBase):
    def __init__(self):
        super().__init__()
        self._data = vtk.vtkPolyData()
        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._nodes = []

    def load_file(self, path):
        '''
        nodes are an index and 3 coordinates (i, x, y, z)
        '''
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(path)
        gmsh.model.mesh.generate(dim=2)

        indexes, coords, _ = gmsh.model.mesh.getNodes(includeBoundary=True)
        all_nodes = {i:c for i, c in zip(indexes, coords.reshape(-1, 3))}

        nodes = []

        for dim, tag in gmsh.model.getEntities(dim=0):
            _, indexes, points = gmsh.model.mesh.getElements(dim, tag)
            indexed_nodes = list(unwrap(points))
            for a in indexed_nodes:
                node = [tag, *all_nodes[a]]
                nodes.append(node)

        gmsh.finalize()
        self.set_data(nodes)

    def set_data(self, nodes):
        self._nodes = nodes

    def source(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        data.Allocate(len(self._nodes))
        
        current_point = 0
        for i, x, y, z in self._nodes:
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
        self._actor.GetProperty().SetColor((0.9, 0.4, 0.6))
        self._actor.GetProperty().SetPointSize(6)
