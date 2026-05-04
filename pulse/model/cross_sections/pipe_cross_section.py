from dataclasses import dataclass

import numpy as np


@dataclass
class PipeCrossSection:

    d_out: float
    thickness: float
    offset_y: float = 0.
    offset_z: float = 0.
    insulation_thickness: float = 0.
    insulation_density: float = 0.
    section_type_label: str = "pipe"


    @property
    def section_parameters(self):
        return [self.d_out, self.thickness, self.offset_y, self.offset_z, self.insulation_thickness, self.insulation_density]

    @property
    def centroid(self):
        return 0., 0.

    @property
    def section_properties(self):

        [d_out, thickness, offset_y, offset_z, *_] = self.section_parameters
        
        d_in = d_out - 2 * thickness

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
        [d_out, thickness, offset_y, offset_z, insulation_thickness, *_] = self.section_parameters

        d_theta = np.pi/N
        theta = np.arange(-np.pi/2, (np.pi/2)+d_theta, d_theta)
        d_in = d_out - 2 * thickness

        Zp_out = (d_out / 2) * np.cos(theta)
        Yp_out = (d_out / 2) * np.sin(theta)
        Zp_in = (d_in / 2) * np.cos(-theta)
        Yp_in = (d_in / 2) * np.sin(-theta)

        Zp_list = [list(Zp_out), list(Zp_in),[0]]
        Yp_list = [list(Yp_out), list(Yp_in), [-(d_out/2)]]

        Zp_right = [value for _list in Zp_list for value in _list]
        Yp_right = [value for _list in Yp_list for value in _list]

        Zp_left = -np.flip(Zp_right)
        Yp_left =  np.flip(Yp_right)

        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z
        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y

        Zc, Yc = self.centroid

        Yc_offset = Yc + offset_y
        Zc_offset = Zc + offset_z
        
        if insulation_thickness != float(0):
            
            t_ins = insulation_thickness
            Zp_out_ins = ((d_out + 2 * t_ins)/2) * np.cos(theta)
            Yp_out_ins = ((d_out + 2 * t_ins)/2) * np.sin(theta)
            Zp_in_ins = (d_out / 2) * np.cos(-theta)
            Yp_in_ins = (d_out / 2) * np.sin(-theta)

            Zp_list_ins = [list(Zp_out_ins), list(Zp_in_ins), [0]]
            Yp_list_ins = [list(Yp_out_ins), list(Yp_in_ins), [-(d_out/2)]]

            Zp_right_ins = [value for _list in Zp_list_ins for value in _list]
            Yp_right_ins = [value for _list in Yp_list_ins for value in _list]

            Zp_left_ins = -np.flip(Zp_right_ins)
            Yp_left_ins =  np.flip(Yp_right_ins)

            Yp_ins = np.array([Yp_right_ins, Yp_left_ins]).flatten() + offset_y
            Zp_ins = np.array([Zp_right_ins, Zp_left_ins]).flatten() + offset_z

            return Zp, Yp, Zp_ins, Yp_ins, Zc_offset, Yc_offset

        return Zp, Yp, None, None, Zc_offset, Yc_offset
    
    def as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
        }