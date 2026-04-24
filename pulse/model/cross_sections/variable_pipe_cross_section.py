from dataclasses import dataclass
# from pulse.utils.common_utils import get_linear_distribution_for_variable_section


@dataclass
class VariablePipeCrossSection:

    d_out_initial: float
    thickness_initial: float
    offset_y_initial: float
    offset_z_initial: float
    d_out_final: float
    thickness_final: float
    offset_y_final: float
    offset_z_final: float
    insulation_thickness: float = 0.
    insulation_density: float = 0.
    section_type_label: str = "reducer"
    number_of_sections: int = -1

    @property
    def section_parameters(self):
        return [
            self.d_out_initial,
            self.thickness_initial,
            self.offset_y_initial,
            self.offset_z_initial,
            self.d_out_final,
            self.thickness_final,
            self.offset_y_final,
            self.offset_z_final,
            self.insulation_thickness,
            self.insulation_density,
            ]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):
       return None

    @property
    def section_points_to_draw(self):
        return None

    def _as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
        }