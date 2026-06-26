from vtkmodules.vtkCommonDataModel import vtkPolyData

from pulse.interface.viewer_3d.actors import TubeActor
from pulse.model.cross_section import CrossSection
from pulse.model.node import Node
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.utils import cross_section_sources


class TubeActorResults(TubeActor):
    def __init__(self, acoustic_plot: bool = False, show_deformed: bool = False, **kwargs) -> None:
        self.acoustic_plot = acoustic_plot
        self.show_deformed = show_deformed
        super().__init__(**kwargs)

    def get_element_coordinates(self, node: Node) -> tuple[float, float, float]:
        return node.deformed_coordinates if self.show_deformed else node.coordinates

    def get_element_rotations(self, element_id: int) -> tuple[float, float, float]:
        if self.show_deformed:
            return self.preprocessor.deformed_section_rotations[element_id - 1, :]

        return self.preprocessor.undeformed_section_rotations[element_id - 1, :]

    def create_element_data(self, element_attributes: ElementAttributes):

        cross_section = element_attributes.cross_section

        if not isinstance(cross_section, CrossSection):
            return vtkPolyData()

        section_type_label = cross_section.section_type_label

        pipe_section = section_type_label in ["pipe", "bend", "arc_bend", "reducer"]
        expansion_joint = section_type_label == "expansion_joint"
        valve = section_type_label == "valve"

        tube_sides = self._get_tube_sides()

        # In acoustic plots we need to show the fluids, not the pipe
        if self.acoustic_plot:
            length = element_attributes.length
            section_parameters_render = element_attributes.section_parameters_render

            if pipe_section or valve:
                d_out, t, offset_y, offset_z, *_ = cross_section.section_parameters
                d_inner = d_out - 2 * t
                return cross_section_sources.closed_pipe_data(length, d_inner, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

            elif expansion_joint:
                d_eff, offset_y, offset_z, *_ = section_parameters_render
                return cross_section_sources.closed_pipe_data(length, d_eff, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        return super().create_element_data(element_attributes)