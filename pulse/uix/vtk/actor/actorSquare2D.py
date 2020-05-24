import vtk
from pulse.uix.vtk.vtkActorBase import vtkActorBase

class ActorSquare2D(vtkActorBase):
    def __init__(self, posA, posB):
        super().__init__()

        self.color = [1,0,0]
        self.normalizedColor = [1,0,0]

        self._actor = vtk.vtkActor2D()

        self.posA = posA
        self.posB = posB

        self._nodes = vtk.vtkPoints()
        self._poly = vtk.vtkPolygon()
        self._edges = vtk.vtkCellArray()
        self._object = vtk.vtkPolyData()

        self._tubeFilter = vtk.vtkTubeFilter()
        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)

        self._mapper = vtk.vtkPolyDataMapper2D()

    def source(self):
        pointA = [self.posA[0], self.posA[1]]
        pointB = [self.posB[0], self.posB[1]]
        pointC = [self.posA[0], self.posB[1]]
        pointD = [self.posB[0], self.posA[1]]

        self._nodes.InsertNextPoint(pointA[0], pointA[1], 0)
        self._nodes.InsertNextPoint(pointD[0], pointD[1], 0)
        self._nodes.InsertNextPoint(pointB[0], pointB[1], 0)
        self._nodes.InsertNextPoint(pointC[0], pointC[1], 0)

        self._poly.GetPointIds().SetNumberOfIds(4)
        self._poly.GetPointIds().SetId(0, 0)
        self._poly.GetPointIds().SetId(1, 1)
        self._poly.GetPointIds().SetId(2, 2)
        self._poly.GetPointIds().SetId(3, 3)

        self._edges.InsertNextCell(self._poly)

        self._object.SetPoints(self._nodes)
        self._object.SetPolys(self._edges)

    def filter(self):
        pass

    def map(self):
        self._mapper.SetInputData(self._object)
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)
        self._actor.GetProperty().SetOpacity(0.3)