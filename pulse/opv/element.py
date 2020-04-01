import vtk
import random
from pulse.preprocessing.element import Element
from pulse.preprocessing.node import Node

class Element:
    def __init__(self, element, tag=-1):
        self.element = element
        self.tag = tag

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
        self._nodes.InsertPoint(0, self.element.first_node.x, self.element.first_node.y, self.element.first_node.z)
        self._nodes.InsertPoint(1, self.element.last_node.x, self.element.last_node.y, self.element.last_node.z)

        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def _filter(self):
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for _ in range(self._nodes.GetNumberOfPoints()):
            self._colorFilter.InsertNextTypedTuple(color)

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.01)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.Update()


    def _map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)

    def get_actor(self):
        return self._line_actor