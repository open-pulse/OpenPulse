from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper


class SectionPlaneActor(vtkActor):
    def __init__(self, size=1):
        self.size = size
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        plane = vtkCubeSource()

        plane.SetCenter(0, 0, 0)
        plane.SetXLength(self.size * 0.005)
        plane.SetYLength(self.size)
        plane.SetZLength(self.size)
        plane.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(plane.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.333, 0.867)
        self.GetProperty().LightingOff()