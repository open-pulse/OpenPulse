import vtk
import random
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.cross_section import CrossSection

class PostProcessingLines:
    def __init__(self, project, matriz, color_table):

        self.project = project
        self.projectNodes = self.project.getNodes()
        self.matriz = matriz
        self.colorTable = color_table
        self.elements = self.project.getElements()
        self.nodes = matriz

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
        for node in self.nodes:
            id_ = int(node[0])
            self._nodes.InsertPoint(id_, node[1] + self.projectNodes[id_].x, node[2] + self.projectNodes[id_].y, node[3] + self.projectNodes[id_].z)

        for key, element in self.elements.items():
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, element.first_node_id)
            line.GetPointIds().SetId(1, element.last_node_id)
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def _filter(self):
        for node in self.nodes:
            #self._colorFilter.InsertNextTypedTuple([255,255,255])
            self._colorFilter.InsertTypedTuple(int(node[0]), self.colorTable.get_color_by_id(node[0]))
        # for _ in range(self._nodes.GetNumberOfPoints()):
        #     self._colorFilter.InsertNextTypedTuple([255,255,255])

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.2)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.SetCapping(True)
        self._tubeFilter.Update()

    def _map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)

    def get_actor(self):
        return self._line_actor