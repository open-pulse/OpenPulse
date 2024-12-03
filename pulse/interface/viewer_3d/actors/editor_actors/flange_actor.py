import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.cross_section_sources import flange_data
from pulse.utils.rotations import align_vtk_geometry
from pulse.editor.structures import Flange


class FlangeActor(vtkActor):
    def __init__(self, flange: Flange):
        self.flange = flange
        self.create_geometry()

    def create_geometry(self):
        vector = self.flange.end.coords() - self.flange.start.coords()
        length = np.linalg.norm(vector)
        source = flange_data(
            length,
            self.flange.diameter,
            self.flange.thickness,
            offset_y = self.flange.offset_y,
            offset_z = self.flange.offset_z,
        )

        data = align_vtk_geometry(source, self.flange.start.coords(), vector)
        paint_data(data, self.flange.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
