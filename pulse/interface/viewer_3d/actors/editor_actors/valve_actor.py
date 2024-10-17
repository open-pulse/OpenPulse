from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.editor.structures import Valve

import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.interface.viewer_3d.utils.cell_utils import paint_data
from pulse.interface.viewer_3d.utils.cross_section_sources import valve_data
from pulse.interface.viewer_3d.utils.rotations import align_vtk_geometry


class ValveActor(vtkActor):
    def __init__(self, valve: "Valve"):
        self.valve = valve
        self.create_geometry()

    def create_geometry(self):
        a = self.valve.start.coords()
        b = self.valve.end.coords()
        if b[0] > a[0]:
            a, b = b, a

        vector = b - a
        length = np.linalg.norm(vector)
        source = valve_data(length, self.valve.diameter, self.valve.thickness)

        data = align_vtk_geometry(source, a, vector)
        paint_data(data, self.valve.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
