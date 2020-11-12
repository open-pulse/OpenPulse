import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase

class LinesActor(vtkActorBase):
    def __init__(self, elements, project):
        super().__init__()

        self.elements = elements 
        self.project = project

        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        for element in self.elements:
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

    def filter(self):
        pass 
    
    def map(self):
        self._source.Update()
        self._mapper.SetInputData(self._source.GetOutput())
    
    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetLineWidth(5)
