import vtk
import random

class Point:
    def __init__(self, x, y, z, tag = -1):

        self.x = x
        self.y = y
        self.z = z
        self.tag = tag

        self.sphere = vtk.vtkSphereSource()

        self._object = vtk.vtkPolyData()

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
        self.sphere.SetRadius(0.005)
        self.sphere.SetCenter(self.x, self.y, self.z)
        self.sphere.SetPhiResolution(11)
        self.sphere.SetThetaResolution(21)

    def _filter(self):
        pass
        # color = [0,255,0]
        # for _ in range(self._nodes.GetNumberOfPoints()):
        #     self._colorFilter.InsertNextTypedTuple(color)

        # self._object.GetPointData().SetScalars(self._colorFilter)

    def _map(self):
        self._mapper.SetInputConnection(self.sphere.GetOutputPort())

    def _actor(self):
        self._line_actor.SetMapper(self._mapper)
        self._line_actor.GetProperty().SetDiffuseColor(1,0,.5)
        self._line_actor.GetProperty().SetDiffuse(.8)
        self._line_actor.GetProperty().SetSpecular(.5)
        self._line_actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        self._line_actor.GetProperty().SetSpecularPower(30.0)

    def get_actor(self):
        return self._line_actor