import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.cross_section_sources import closed_pipe_data
from pulse.utils.rotations import align_vtk_geometry
from pulse.editor.structures import Pipe


class PipeActor(vtkActor):
    def __init__(self, pipe: Pipe):
        self.pipe = pipe
        self.create_geometry()

    def create_geometry(self):
        vector = self.pipe.end.coords() - self.pipe.start.coords()
        length = np.linalg.norm(vector)
        source = closed_pipe_data(length, self.pipe.diameter)

        data = align_vtk_geometry(source, self.pipe.start.coords(), vector)
        paint_data(data, self.pipe.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
