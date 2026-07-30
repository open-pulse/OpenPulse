import numpy as np
from vtkmodules.vtkCommonDataModel import vtkPolyData

from pulse.interface.viewer_3d.actors import TubeActor
from pulse.model.cross_section import CrossSection
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.node import Node
from pulse.utils import cross_section_sources


class TubeActorResults(TubeActor):
    def __init__(self, acoustic_plot: bool = False, show_deformed: bool = False, **kwargs) -> None:
        self.acoustic_plot = acoustic_plot
        self.show_deformed = show_deformed
        super().__init__(**kwargs)

    def get_all_elements_coordinates(self) -> np.ndarray:
        if self.show_deformed:
            mesh = self.model.mesh
            return self.deformed_coordinates[mesh.lines_connectivity[:, 4], 1:]
        return super().get_all_elements_coordinates()

    def get_all_elements_rotations(self):
        if self.show_deformed:
            self.preprocessor.deformed_section_rotations
        return super().get_all_elements_rotations()

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

            if pipe_section or valve:
                d_out, t, offset_y, offset_z, *_ = np.round(cross_section.section_parameters, 5)
                d_inner = d_out - 2 * t
                return cross_section_sources.closed_pipe_data(length, d_inner, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

            elif expansion_joint:
                d_eff, offset_y, offset_z, *_ = np.round(element_attributes.section_parameters_render, 5)
                return cross_section_sources.closed_pipe_data(length, d_eff, offset_y=offset_y, offset_z=offset_z, sides=tube_sides)

        return super().create_element_data(element_attributes)
