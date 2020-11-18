import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase

class LinesActor(vtkActorBase):
    def __init__(self, elements, project):
        super().__init__()

        self.elements = elements 
        self.project = project

        self._key_index = {j:i for i,j in enumerate(self.elements.keys())}
        self._data = vtk.vtkPolyData()
        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.SetNumberOfTuples(len(self.elements))
        
    def source(self):
        for element in self.elements.values():
            points = vtk.vtkPoints()
            edges = vtk.vtkCellArray()
            line = vtk.vtkLine()
            obj = vtk.vtkPolyData()

            points.InsertPoint(0, *element.first_node.coordinates)
            points.InsertPoint(1, *element.last_node.coordinates)
            line.GetPointIds().SetId(0,0)
            line.GetPointIds().SetId(1,1)
            edges.InsertNextCell(line)

            obj.SetPoints(points)
            obj.SetLines(edges)
            self._source.AddInputData(obj)

        self._source.Update()
        self._data.DeepCopy(self._source.GetOutput())

    def filter(self):
        pass 
    
    def map(self):
        # self._source.Update()
        self._mapper.SetInputData(self._data)
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetLineWidth(3)
        self._actor.GetProperty().SetColor((0.1, 0.1, 0.1))
        self.setColor((0,255,0))

    def setColor(self, color, keys=None):
        c = vtk.vtkUnsignedCharArray()
        c.DeepCopy(self._colors)
        keys = keys if keys else self.elements.keys()
        for key in keys:
            index = self._key_index[key]
            c.SetTuple(index, color)
        self._data.GetCellData().SetScalars(c)
        self._colors = c