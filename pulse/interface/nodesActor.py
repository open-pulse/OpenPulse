import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase

class NodesActor(vtkActorBase):
    def __init__(self, nodes, project):
        super().__init__()

        self.nodes = nodes 
        self.project = project

        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        points = vtk.vtkPoints()
        data = vtk.vtkPolyData()
        for node in self.nodes:
            x,y,z = node.x, node.y, node.z
            points.InsertNextPoint(x,y,z)
        data.SetPoints(points)

        vertexFilter = vtk.vtkVertexGlyphFilter()
        vertexFilter.SetInputData(data)
        vertexFilter.Update()

        self._data.ShallowCopy(vertexFilter.GetOutput())

    def filter(self):
        pass 
    
    def map(self):
        self._mapper.SetInputData(self._data)
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().RenderPointsAsSpheresOn()
        self._actor.GetProperty().SetPointSize(10)
        self._actor.GetProperty().LightingOff()
