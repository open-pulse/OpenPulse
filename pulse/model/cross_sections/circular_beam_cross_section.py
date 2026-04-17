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
    
    @property
    def section_points_to_draw(self):

        N = 60
        d_out, thickness, offset_y, offset_z = self.section_parameters

        if thickness == 0:
            d_in = 0
        else:
            d_in = d_out - 2*thickness
        
        d_theta = np.pi/N
        theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)

        Zp_out = (d_out / 2) * np.cos(theta)
        Yp_out = (d_out / 2) * np.sin(theta)
        Zp_in = (d_in / 2) * np.cos(-theta)
        Yp_in = (d_in / 2) * np.sin(-theta)

        Zp_list = [list(Zp_out), list(Zp_in), [-(d_out/2)]]
        Yp_list = [list(Yp_out), list(Yp_in), [0]]

        Zp_right = [value for _list in Zp_list for value in _list]
        Yp_right = [value for _list in Yp_list for value in _list]

        Zp_left = -np.flip(Zp_right)
        Yp_left =  np.flip(Yp_right)

        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z
        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y

        Zc, Yc = self.centroid

        Zc_offset = Zc + offset_z    
        Yc_offset = Yc + offset_y

        return Zp, Yp, Zc_offset, Yc_offset