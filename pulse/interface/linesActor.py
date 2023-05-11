import vtk 
import numpy as np
from time import time 

from pulse.interface.vtkActorBase import vtkActorBase

class LinesActor(vtkActorBase):
    def __init__(self, project, *args, **kwargs):
        super().__init__()

        self.project = project
        self.elements = project.get_structural_elements()
        # self.elements = project.preprocessor.structural_elements
        self.hidden_elements = kwargs.get('hidden_elements', set())

        # self._key_index = {j:i for i,j in enumerate(self.elements.keys())}
        self._data = vtk.vtkPolyData()
        self._source = vtk.vtkAppendPolyData()
        self._mapper = vtk.vtkPolyDataMapper()
        self._colors = vtk.vtkUnsignedCharArray()
        self._colors.SetNumberOfComponents(3)
        self._colors.SetNumberOfTuples(len(self.elements))
        
    def source(self):
        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray() 

        visible_elements = {i:e for i, e in self.elements.items() if (i not in self.hidden_elements)}
        self._key_index  = {j:i for i,j in enumerate(visible_elements)}

        current_point = 0
        for key, element in visible_elements.items():
            points.InsertPoint(current_point, *element.first_node.coordinates)
            points.InsertPoint(current_point + 1, *element.last_node.coordinates)
            
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, current_point)
            line.GetPointIds().SetId(1, current_point + 1)

            lines.InsertNextCell(line)
            current_point += 2  # two points are added every element
        
        data.SetPoints(points)
        data.SetLines(lines)
        self._data = data

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
            index = self._key_index.get(key)
            if index is not None:
                c.SetTuple(index, color)
        self._data.GetCellData().SetScalars(c)
        self._colors = c