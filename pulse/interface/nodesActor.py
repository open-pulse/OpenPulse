import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase

class NodesActor(vtkActorBase):
    def __init__(self, project, *args, **kwargs):
        super().__init__()

        self.project = project
        self.nodes = project.get_nodes()
        
        # self.nodes = project.preprocessor.nodes
        self.hidden_nodes = kwargs.get('hidden_nodes', set())

        # self._key_index = {j:i for i,j in enumerate(self.nodes.keys())}
        self._data = vtk.vtkPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.SetNumberOfTuples(len(self.nodes))

    def source(self):
        points = vtk.vtkPoints()
        data = vtk.vtkPolyData()

        visible_nodes = {i:e for i,e in self.nodes.items() if (i not in self.hidden_nodes)}
        self._key_index = {j:i for i,j in enumerate(visible_nodes)}

        for index, node in visible_nodes.items():
            x,y,z = node.x, node.y, node.z
            points.InsertNextPoint(x,y,z)
            self._colors.InsertNextTuple((255,255,255))
        data.SetPoints(points)

        vertexFilter = vtk.vtkVertexGlyphFilter()
        vertexFilter.SetInputData(data)
        vertexFilter.Update()
        self._data.DeepCopy(vertexFilter.GetOutput())

    def filter(self):
        pass 
    
    def map(self):
        self._mapper.SetInputData(self._data)
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().RenderPointsAsSpheresOn()
        self._actor.GetProperty().SetPointSize(6)
        self._actor.GetProperty().LightingOff()

    def setColor(self, color, keys=None):
        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        keys = keys if keys else self.nodes.keys()
        for key in keys:
            index = self._key_index.get(key)
            if index is not None:
                c.SetTuple(index, color)
        self._data.GetPointData().SetScalars(c)
        self._colors = c
