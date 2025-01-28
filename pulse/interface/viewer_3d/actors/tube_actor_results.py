import numpy as np
from vtkmodules.vtkCommonDataModel import vtkPolyData
from pulse.utils import cross_section_sources
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

        pipe_section = element.element_type == "pipe_1"
        expansion_joint = element.element_type == "expansion_joint"
        valve = element.element_type == "valve"
        tube_sides = self._get_tube_sides()

        # In acoustic plots we need to show the fluids, not the pipe
        if self.acoustic_plot and (pipe_section or valve):
            d_out, t, *_ = cross_section.section_parameters
            d_inner = d_out - 2 * t
            return cross_section_sources.closed_pipe_data(element.length, d_inner, sides=tube_sides)

        elif self.acoustic_plot and expansion_joint:
            _, d_eff, *_ = element.section_parameters_render
            return cross_section_sources.closed_pipe_data(element.length, d_eff, sides=tube_sides)

        return super().create_element_data(element)