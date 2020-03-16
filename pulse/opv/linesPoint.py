import vtk
import random

class LinesPoint:
    def __init__(self, nodes = [], edges = [], tag = -1):

        self.nodesList = nodes
        self.edgesList = edges
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
        for node in self.nodesList:
            self._nodes.InsertPoint(int(node[0]), node[1]/1000, node[2]/1000, node[3]/1000)

        for edge in self.edgesList:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, edge[1])
            line.GetPointIds().SetId(1, edge[2])
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def _filter(self):
        color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        for _ in range(self._nodes.GetNumberOfPoints()):
            self._colorFilter.InsertNextTypedTuple(color)

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.001)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.Update()


    def _map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)

    def get_actor(self):
        return self._line_actor