import vtk
from pulse.uix.vtk.vtkActorBase import vtkActorBase

class ActorElement(vtkActorBase):
    def __init__(self, element, tag=-1):
        super().__init__()
        self.element = element
        self.tag = tag

        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()

        self.normalizedColor = [0,1,1]

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        self._nodes.InsertPoint(0, self.element.first_node.x, self.element.first_node.y, self.element.first_node.z)
        self._nodes.InsertPoint(1, self.element.last_node.x, self.element.last_node.y, self.element.last_node.z)

        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, 0)
        line.GetPointIds().SetId(1, 1)
        self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def filter(self):
        color = [0,0,255]
        for _ in range(self._nodes.GetNumberOfPoints()):
            self._colorFilter.InsertNextTypedTuple(color)

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(0.01)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.Update()

    def map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)