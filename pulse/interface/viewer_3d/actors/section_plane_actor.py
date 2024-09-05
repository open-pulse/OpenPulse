from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper
import numpy as np

from pulse.interface.utils import rotation_matrices, lerp


class SectionPlaneActor(vtkActor):
    def __init__(self, bounds):
        self.bounds = bounds
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        plane = vtkCubeSource()

        plane.SetCenter(0, 0, 0)
        plane.SetXLength(0.005)
        plane.SetYLength(1)
        plane.SetZLength(1)
        plane.Update()

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(plane.GetOutput())
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetColor(0, 0.333, 0.867)
        self.GetProperty().LightingOff()

    def configure_section_plane(self, position, orientation):
        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)

        x0, x1, y0, y1, z0, z1 = self.bounds
        size = np.max(np.abs([x1 - x0, y1 - y0, z1 - z0]))

        self.SetPosition(x, y, z)
        self.SetOrientation(orientation)
        self.SetScale(size)

    def calculate_normal_vector(self, orientation):
        # https://forum.gamemaker.io/index.php?threads/solved-3d-rotations-with-a-shader-matrix-or-a-matrix-glsl-es.61064/

        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return normal[:3]

    def calculate_xyz_position(self, position):
        x = lerp(self.bounds[0], self.bounds[1], position[0] / 100)
        y = lerp(self.bounds[2], self.bounds[3], position[1] / 100)
        z = lerp(self.bounds[4], self.bounds[5], position[2] / 100)
        return x, y, z
