import vtk
from pulse.interface.viewer_3d.actors.actor_base import ActorBase

class ActorEntityPoints(ActorBase):
    def __init__(self, nodes, size, tag = -1):
        super().__init__()

        self.nodes = nodes
        self.size = size
        self.color = [0,0,255]
        self.special = True
        self.tag = tag

        self._object = vtk.vtkAppendPolyData()

        self._colorFilter = vtk.vtkUnsignedCharArray()
        self._colorFilter.SetNumberOfComponents(3)
        self._colorFilter.SetName("Colors")

        self._mapper = vtk.vtkPolyDataMapper()

    def setColor(self, node):
        self.special = False
        # self.special = True
        # self.color = [0,0,255]
        # if node.haveBoundaryCondition() and node.haveForce():
        #     self.color = [0,255,0]
        # elif node.haveBoundaryCondition():
        #     if sum([value for value in node.prescribed_dofs_bc if value != None])==0:
        #         self.color = [0,0,0]
        #     else:
        #         self.color = [255,255,255]
        # elif node.haveForce():
        #     self.color = [0,255,255]
        # else:
        #     self.special = False

    def source(self):
        for node in self.nodes:
            self.setColor(node)

            colors = vtk.vtkUnsignedCharArray()
            colors.SetNumberOfComponents(3)
            colors.SetName("Colors")

            if self.special:
                self.sphere = vtk.vtkSphereSource()
                self.sphere.SetRadius(self.size*1.2)
                self.sphere.SetCenter(node.x, node.y, node.z)
                self.sphere.SetPhiResolution(11)
                self.sphere.SetThetaResolution(21)
                self.sphere.Update()
                sp = self.sphere.GetOutput()
                self.sphere.Update()
                for _ in range(self.sphere.GetOutput().GetNumberOfPoints()):
                    colors.InsertNextTypedTuple(self.color)
                sp.GetPointData().SetScalars(colors)
                self._object.AddInputData(sp)
                #self._object.AddInputConnection(self.sphere.GetOutputPort())
                self._object.Update()
            else:
                self.cube = vtk.vtkCubeSource()
                self.cube.SetXLength(self.size)
                self.cube.SetYLength(self.size)
                self.cube.SetZLength(self.size)
                self.cube.SetCenter(node.x, node.y, node.z)
                self.cube.Update()
                sp = self.cube.GetOutput()
                self.cube.Update()
                for _ in range(self.cube.GetOutput().GetNumberOfPoints()):
                    colors.InsertNextTypedTuple(self.color)
                sp.GetPointData().SetScalars(colors)

                self._object.AddInputData(sp)
                self._object.Update()

    def filter(self):
        pass

    def map(self):
        self._mapper.SetInputConnection(self._object.GetOutputPort())
        self._mapper.SetColorModeToDirectScalars()

    def actor(self):
        self._actor.SetMapper(self._mapper)
        self._actor.GetProperty().SetDiffuse(.8)
        self._actor.GetProperty().SetSpecular(.5)
        self._actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        self._actor.GetProperty().SetSpecularPower(30.0)