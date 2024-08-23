import numpy as np
from opps.interface.viewer_3d.utils import cross_section_sources
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIntArray,
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import vtkPlane, vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper

from pulse import app
from pulse.interface.utils import ColorMode
from pulse.interface.viewer_3d.coloring.color_table import ColorTable
from pulse.interface.viewer_3d.actors import TubeActor


class TubeActorResults(TubeActor):
    def __init__(self, acoustic_plot=False, show_deformed=False, **kwargs) -> None:
        self.acoustic_plot = acoustic_plot
        self.show_deformed = show_deformed
        super().__init__(**kwargs)

    def get_element_coordinates(self, element) -> tuple[float, float, float]:
        if self.show_deformed:
            return element.first_node.deformed_coordinates
        else:
            return element.first_node.coordinates

    def get_element_rotations(self, element) -> tuple[float, float, float]:
        if self.show_deformed:
            return element.deformed_rotation_xyz
        else:
            return element.section_rotation_xyz_undeformed

    def create_element_data(self, element):
        cross_section = element.cross_section
        if cross_section is None:
            return vtkPolyData()
        
        pipe_section = ("Pipe" in cross_section.section_type_label)

        # In acoustic plots we need to show the fluids, not the pipe
        if self.acoustic_plot and pipe_section:
            d_out, t, *_ = cross_section.section_parameters
            d_inner = d_out - 2 * t
            return cross_section_sources.closed_pipe_data(element.length, d_inner, sides=30)

        return super().create_element_data(element)
