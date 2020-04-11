import vtk
import random
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.cross_section import CrossSection

class PreProcessingLines:
    def __init__(self, color_table, entity = Entity(-1)):

        self.colorTable = color_table
        self.nodesList = entity.getNodes()
        self.elementsList = entity.getElements()
        self.tag = entity.getTag()
        self.cross = entity.getCrossSection()
        self.externalRadius = float(self.cross.external_diameter)

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
        for node in self.nodesList:
            self._nodes.InsertPoint(int(node[0]), node[1], node[2], node[3])

        for element in self.elementsList:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, element[1])
            line.GetPointIds().SetId(1, element[2])
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def _filter(self):
        for node in self.nodesList:
            self._colorFilter.InsertTypedTuple(int(node[0]), self.colorTable.get_color_by_id(node[0]))
        # for _ in range(self._nodes.GetNumberOfPoints()):
        #     self._colorFilter.InsertNextTypedTuple([255,255,255])

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(self.externalRadius)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.SetCapping(True)
        self._tubeFilter.Update()

    def _map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())
        #self._mapper.ScalarVisibilityOff()

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)
        #self._line_actor.GetProperty().SetColor(self.normalizedColor)

    def get_actor(self):
        return self._line_actor