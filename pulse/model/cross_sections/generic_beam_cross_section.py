from dataclasses import dataclass

@dataclass
class GenericBeamCrossSection:

    area: float
    Iyy: float
    Izz: float
    Iyz: float
    shear_coefficient: float = 1
    Yc: float = 0.
    Zc: float = 0.
    section_type_label: str = "generic_beam"

    @property
    def section_parameters(self):
        return None

    @property
    def properties_list(self):
        return [self.area, self.Iyy, self.Izz, self.Iyz, self.shear_coefficient, self.Yc, self.Zc]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):

        return {  
            "area" : self.area, 
            "Iyy" : self.Iyy, 
            "Izz" : self.Izz, 
            "Iyz" : self.Iyz,
            "shear_coefficient" : self.shear_coefficient,
            "Yc" : self.Yc, 
            "Zc" : self.Zc,
            }

    @property
    def section_points_to_draw(self):
        return None
    
    def as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
            "section_properties" : self.section_properties,
        }