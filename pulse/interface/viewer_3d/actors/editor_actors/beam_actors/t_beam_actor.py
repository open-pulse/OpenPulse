import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.cross_section_sources import t_beam_data
from pulse.utils.rotations import align_vtk_geometry
from pulse.editor.structures import TBeam


class TBeamActor(vtkActor):
    def __init__(self, beam: TBeam):
        self.beam = beam
        self.create_geometry()

    def create_geometry(self):
        vector = self.beam.end.coords() - self.beam.start.coords()
        length = np.linalg.norm(vector)
        source = t_beam_data(
            length,
            self.beam.height,
            self.beam.width,
            self.beam.thickness_1,
            self.beam.thickness_2,
            offset_y=self.beam.offset_y,
            offset_z=self.beam.offset_z,
        )

        data = align_vtk_geometry(source, self.beam.start.coords(), vector, angle=self.beam.angle)
        paint_data(data, self.beam.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
