import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.cross_section_sources import reducer_data
from pulse.utils.rotations import align_vtk_geometry
from pulse.editor.structures import Reducer


class ReducerActor(vtkActor):
    def __init__(self, reducer: Reducer):
        self.reducer = reducer
        self.create_geometry()

    def create_geometry(self):
        vector = self.reducer.end.coords() - self.reducer.start.coords()
        length = np.linalg.norm(vector)
        source = reducer_data(
            length,
            self.reducer.initial_diameter,
            self.reducer.final_diameter,
            self.reducer.initial_offset_y,
            self.reducer.initial_offset_z,
            self.reducer.final_offset_y,
            self.reducer.final_offset_z,
        )

        data = align_vtk_geometry(source, self.reducer.start.coords(), vector)
        paint_data(data, self.reducer.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
