from dataclasses import dataclass


@dataclass
class ExpansionJointCrossSection:

    effective_diameter: float
    offset_y: float = 0.
    offset_z: float = 0.
    plot_key: str | None = None
    section_type_label: str = "expansion_joint"

    @property
    def section_parameters(self):
        return [self.effective_diameter, self.offset_y, self.offset_z]

    def _as_list(self):
        return [self.effective_diameter, self.offset_y, self.offset_z, self.plot_key]