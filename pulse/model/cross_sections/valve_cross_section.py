from dataclasses import dataclass

# import numpy as np


@dataclass
class ValveCrossSection:

    d_out: float
    thickness: float
    offset_y: float = 0.
    offset_z: float = 0.
    insulation_thickness: float = 0.
    insulation_density: float = 0.
    section_type_label: str = "valve"


    @property
    def section_parameters(self):
        return [self.d_out, self.thickness, self.offset_y, self.offset_z, self.insulation_thickness, self.insulation_density]

    @property
    def centroid(self):
        return 0., 0.

    def as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
        }