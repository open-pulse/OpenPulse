from vtkmodules.vtkCommonDataModel import vtkPolyData
from pulse.utils import cross_section_sources
from pulse.interface.viewer_3d.actors import TubeActor
from pulse.model.node import Node


class TubeActorResults(TubeActor):
    def __init__(self, acoustic_plot: bool = False, show_deformed: bool = False, **kwargs) -> None:
        self.acoustic_plot = acoustic_plot
        self.show_deformed = show_deformed
        super().__init__(**kwargs)

    def get_element_coordinates(self, node: Node) -> tuple[float, float, float]:
        if self.show_deformed:
            return node.deformed_coordinates

        return node.coordinates

    def get_element_rotations(self, element_index: int) -> tuple[float, float, float]:
        section_rotations = self.model.section_rotations.get(element_index)
        if self.show_deformed:
            return section_rotations.deformed_rotation_rxyz

        return section_rotations.undeformed_rotation_rxyz

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
            d_out, t, offset_y, offset_z, *_ = cross_section.section_parameters
            d_inner = d_out - 2 * t
            return cross_section_sources.closed_pipe_data(element.length, d_inner, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        elif self.acoustic_plot and expansion_joint:
            d_eff, offset_y, offset_z, *_ = element.section_parameters_render
            return cross_section_sources.closed_pipe_data(element.length, d_eff, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        return super().create_element_data(element)