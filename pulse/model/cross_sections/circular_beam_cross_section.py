from dataclasses import dataclass

import numpy as np


@dataclass
class CircularBeamCrossSection:

    d_out: float
    t: float
    offset_y: float = 0.
    offset_z: float = 0.

    @property
    def section_parameters(self):
        return [self.d_out, self.t, self.offset_y, self.offset_z]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):

        [d_out, t, offset_y, offset_z] = self.section_parameters
        
        if t == 0:
            d_in = 0
        else:
            d_in = d_out - 2 * t

        area = np.pi * ((d_out**2) - (d_in**2)) / 4
        Iyy = np.pi * ((d_out**4) - (d_in**4)) / 64
        Izz = np.pi * ((d_out**4) - (d_in**4)) / 64
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