import vtk
import math
from pulse.interface.viewer_3d.actors.actor_base import ActorBase

class ActorSpring(ActorBase):
    def __init__(self, node, radius, base_length, xyz=1, u_def=[]):
        super().__init__()
        self.nV = 256
        self.nCyc = 8
        self.rT1 = 0.1
        self.rT2 = 0.5
        self.rS = 0.8
        self.h = 8.7
        self.nTv = 8

        self.node = node
        self.radius = radius
        self.base_length = base_length 

        self.xyz = xyz
        if u_def == []:
            self.x = node.x
            self.y = node.y
            self.z = node.z
        else:
            self.x = u_def[0]
            self.y = u_def[1]
            self.z = u_def[2]

        self.shiftValue = 0
        self.normalizedColor = [1,0.647,0]

        self.points = vtk.vtkPoints()
        self.lines = vtk.vtkCellArray()    
        self.data = vtk.vtkPolyData()
        self.tubeRadius = vtk.vtkDoubleArray()
        self.tube = vtk.vtkTubeFilter()
        self.mapper = vtk.vtkPolyDataMapper()

    def source(self):
        for i in range(self.nV):
            vX = self.rS * math.cos(2 * math.pi * self.nCyc * i / (self.nV - 1))
            vY = self.rS * math.sin(2 * math.pi * self.nCyc * i / (self.nV - 1))
            vZ = self.h * i / self.nV
            self.points.InsertPoint(i, vX, vY, vZ)

        self.lines.InsertNextCell(self.nV)
        for i in range(self.nV):
            self.lines.InsertCellPoint(i)

        self.data.SetPoints(self.points)
        self.data.SetLines(self.lines)

    def filter(self):
        self.tubeRadius.SetName("TubeRadius")
        self.tubeRadius.SetNumberOfTuples(self.nV)
        for i in range(self.nV):
            self.tubeRadius.SetTuple1(i, 0.2)
        
        self.data.GetPointData().AddArray(self.tubeRadius)
        self.data.GetPointData().SetActiveScalars("TubeRadius")

        self.tube.SetInputData(self.data)
        self.tube.SetNumberOfSides(self.nTv)
        self.tube.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

    def map(self):
        self.mapper.SetInputConnection(self.tube.GetOutputPort())
        self.mapper.ScalarVisibilityOff()

    def actor(self):
        self._actor.SetMapper(self.mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)
        self.transform()

    def setNormalizedColor(self, color):
        self.normalizedColor = color

    def setShiftValue(self, value):
        self.shiftValue = value

    def transform(self):
        scale = self.base_length/20
        self._actor.SetScale(scale, scale, scale)
        transform = vtk.vtkTransform()
        self.translate(transform)
        self.rotate(transform)
        self._actor.SetUserTransform(transform)

    def translate(self, transform):
        
        if self.xyz == -1:
            transform.Translate(self.x +self.shiftValue, self.y, self.z)
        elif self.xyz == -2:
            transform.Translate(self.x, self.y +self.shiftValue, self.z)
        elif self.xyz == -3:
            transform.Translate(self.x, self.y, self.z + self.shiftValue)

        if self.xyz == 1:
            transform.Translate(self.x -self.shiftValue, self.y, self.z)
        elif self.xyz == 2:
            transform.Translate(self.x, self.y -self.shiftValue, self.z)
        elif self.xyz == 3:
            transform.Translate(self.x, self.y, self.z - self.shiftValue)

    def rotate(self, transform):
        if self.xyz == -1:
            transform.RotateY(90)
        elif self.xyz == -2:
            transform.RotateX(-90)

        if self.xyz == 1:
            transform.RotateY(-90)
        elif self.xyz == 2:
            transform.RotateX(90)
        elif self.xyz == 3:
            transform.RotateY(180)