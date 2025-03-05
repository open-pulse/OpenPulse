from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pulse.editor.structures import Valve

import numpy as np
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

from pulse.utils.cell_utils import paint_data
from pulse.utils.cross_section_sources import valve_data
from pulse.utils.rotations import align_vtk_geometry


class ValveActor(vtkActor):
    def __init__(self, valve: "Valve"):
        self.valve = valve
        self.create_geometry()

    def create_geometry(self):
        a = self.valve.start.coords()
        b = self.valve.end.coords()

        vector = b - a
        length = np.linalg.norm(vector)
        source = valve_data(
            length, 
            self.valve.diameter, 
            self.valve.thickness,
            self.valve.flange_outer_diameter,
            self.valve.flange_length,
        )
        
        # this makes the valve handle always point up
        angle = 0
        if vector[0] >= 0:
            angle = np.pi

        data = align_vtk_geometry(source, a, vector, angle)
        paint_data(data, self.valve.color.to_rgb())

        mapper = vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
