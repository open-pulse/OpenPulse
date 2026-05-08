from dataclasses import dataclass

import numpy as np


@dataclass
class RectangularBeamCrossSection:

    b: float
    h: float
    b_in: float
    h_in: float
    offset_y: float = 0.
    offset_z: float = 0.
    section_type_label: str = "rectangular_beam"

    @property
    def section_parameters(self):
        return [self.b, self.h, self.b_in, self.h_in, self.offset_y, self.offset_z]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):

        b, h, b_in, h_in, offset_y, offset_z = self.section_parameters

        area = b * h - b_in * h_in
        Iyy = ((b**3)*h/12) - ((b_in**3)*h_in/12)
        Izz = ((h**3)*b/12) - ((h_in**3)*b_in/12)
        Iyz = 0.

        Zc, Yc = self.centroid 

        return {  
            "area" : area,
            "Iyy" : Iyy,
            "Izz" : Izz,
            "Iyz" : Iyz,
            "Yc" : Yc,
            "Zc" : Zc,
            }
    
    @property
    def section_points_to_draw(self):

        b, h, b_in, h_in, offset_y, offset_z = self.section_parameters

        Zp_right = [0, (b/2), (b/2), 0, 0, (b_in/2), (b_in/2), 0, 0]
        Yp_right = [-(h/2), -(h/2), (h/2), (h/2), (h_in/2), (h_in/2), -(h_in/2), -(h_in/2), -(h/2)]

        Zp_left = -np.flip(Zp_right)
        Yp_left =  np.flip(Yp_right)

        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z
        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y

        Zc, Yc = self.centroid

        Zc_offset = Zc + offset_z    
        Yc_offset = Yc + offset_y

        return Zp, Yp, Zc_offset, Yc_offset
    
    def as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
            "section_properties" : self.section_properties,
        }