import vtk
import random
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.cross_section import CrossSection

import numpy as np

class PostProcessingLines:
    def __init__(self, project, coord_def, color_table):

        self.project = project
        self.coord_def = coord_def
        self.colorTable = color_table
        self.elements = self.project.getElements()

        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

        self._line_actor = vtk.vtkActor()

    def assembly(self):
        self._source()
        self._filter()
        self._map()
        self._actor()

    def _source(self):
        indice = self.coord_def[:,0]
        x = self.coord_def[:,1]
        y = self.coord_def[:,2]
        z = self.coord_def[:,3]

        for i in range(len(indice)):
            id_ = int(indice[i])
            self._nodes.InsertPoint(id_, x[i], y[i], z[i])

        for key, element in self.elements.items():
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, element.first_node_id)
            line.GetPointIds().SetId(1, element.last_node_id)
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def _filter(self):
        indice = self.coord_def[:,0]
        for i in range(len(indice)):
            id_ = int(indice[i])
            self._colorFilter.InsertTypedTuple(id_, self.colorTable.get_color_by_id(i))
        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.05)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.SetCapping(True)
        self._tubeFilter.Update()

    def _map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)

    def get_actor(self):
        return self._line_actor