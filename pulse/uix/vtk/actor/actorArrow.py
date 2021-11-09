import vtk
import math
from pulse.uix.vtk.vtkActorBase import vtkActorBase

class ActorArrow(vtkActorBase):
    def __init__(self, node, radius, base_length, xyz=1, u_def=[]):
        super().__init__()
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

        self.arrowSource = vtk.vtkArrowSource()
        self.arrowSource.SetTipLength(0.2)
        self.arrowSource.SetShaftRadius(0.015)
        self.arrowSource.InvertOn()

        self.shiftValue = 0
        self.normalizedColor = [1,1,0]

        self._mapper = vtk.vtkPolyDataMapper()

    def source(self):
        pass

    def filter(self):
        pass

    def removeShaftRadius(self):
        self.arrowSource.SetShaftRadius(0)

    def removeTipLength(self):
        self.arrowSource.SetTipLength(0)
        self.arrowSource.SetTipRadius(0)

    def transform(self):
        scale = self.base_length/2
        self._actor.SetScale(scale, scale, scale)
        transform = vtk.vtkTransform()
        self.translate(transform)
        self.rotate(transform)
        self._actor.SetUserTransform(transform)

    def translate(self, transform):
        
        if self.xyz == -1:
            transform.Translate(self.x + self.shiftValue, self.y, self.z)
        elif self.xyz == -2:
            transform.Translate(self.x, self.y + self.shiftValue, self.z)
        elif self.xyz == -3:
            transform.Translate(self.x, self.y, self.z + self.shiftValue)

        if self.xyz == 1:
            transform.Translate(self.x - self.shiftValue, self.y, self.z)
        elif self.xyz == 2:
            transform.Translate(self.x, self.y - self.shiftValue, self.z)
        elif self.xyz == 3:
            transform.Translate(self.x, self.y, self.z - self.shiftValue)

    def rotate(self, transform):
        if self.xyz == -2:
            transform.RotateZ(90)
        elif self.xyz == -3:
            transform.RotateY(-90)

        if self.xyz == 1:
            transform.RotateY(180)
        elif self.xyz == 2:
            transform.RotateZ(-90)
        elif self.xyz == 3:
            transform.RotateY(90)

    def setNormalizedColor(self, color):
        self.normalizedColor = color

    def setShiftValue(self, value):
        self.shiftValue = value

    def map(self):
        self._mapper.SetInputConnection(self.arrowSource.GetOutputPort())
        self._mapper.ScalarVisibilityOff()

    def actor(self):
        self.transform()
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetColor(self.normalizedColor)