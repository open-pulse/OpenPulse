import vtk
from pulse.uix.vtk.vtkActorBase import vtkActorBase
from pulse.preprocessing.entity import Entity

class ActorLine(vtkActorBase):
    def __init__(self, entity = Entity(-1), plotRadius = False):
        super().__init__()

        self.entity = entity
        self.color = entity.getColor()
        self.normalizedColor = entity.getNormalizedColor()
        self.nodesList = entity.get_nodes()
        self.elementsList = entity.get_elements()
        self.tag = entity.getTag()
        self.plotRadius = plotRadius
        self.radius = 0.01
        self.changeRadius()

        self._nodes = vtk.vtkPoints()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper()

    def changeRadius(self):
        if self.plotRadius:
            if self.entity.crossSection is not None:
                self.radius = self.entity.crossSection.external_radius

    def source(self):
        for node in self.nodesList:
            self._nodes.InsertPoint(int(node[0]), node[1], node[2], node[3])

        for element in self.elementsList:
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, element[1])
            line.GetPointIds().SetId(1, element[2])
            self._edges.InsertNextCell(line)

        self._object.SetPoints(self._nodes)
        self._object.SetLines(self._edges)

    def filter(self):
        for _ in range(self._nodes.GetNumberOfPoints()):
            self._colorFilter.InsertNextTypedTuple(self.color)

        self._object.GetPointData().SetScalars(self._colorFilter)

        self._tubeFilter.SetInputData(self._object)
        self._tubeFilter.SetRadius(self.radius)
        self._tubeFilter.SetNumberOfSides(50)
        self._tubeFilter.Update()

    def map(self):
        self._mapper.SetInputData(self._tubeFilter.GetOutput())
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)

    def setRadius(self, value):
        self.radius = value