from dataclasses import dataclass


@dataclass
class RectangularBeamCrossSection:

    b: float
    h: float
    b_in: float
    h_in: float
    offset_y: float = 0.
    offset_z: float = 0.

    @property
    def section_parameters(self):
        return [self.b, self.h, self.b_in, self.h_in, self.offset_y, self.offset_z]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):

        [b, h, b_in, h_in, offset_y, offset_z] = self.section_parameters

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
            "Zc" : Zc,
            "Yc" : Yc,
            }