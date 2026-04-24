from dataclasses import dataclass

import numpy as np


@dataclass
class TBeamCrossSection:

    h: float
    w1: float
    t1: float
    tw: float
    offset_y: float = 0.
    offset_z: float = 0.
    section_type_label: str = "t_beam"

    @property
    def section_parameters(self):
        return [self.h, self.w1, self.t1, self.tw, self.offset_y, self.offset_z]

    @property
    def centroid(self):

        h, w1, t1, tw, offset_y, offset_z = self.section_parameters
        hw = h - t1

        A_i = np.array([w1*t1, tw*hw])
        A_t = np.sum(A_i)

        z_ci = np.array([0, 0])
        y_ci = np.array([((t1+hw)/2), 0])

        Yc = (y_ci@A_i) / A_t
        Zc = (z_ci@A_i) / A_t

        return Zc, Yc

    @property
    def section_properties(self):

        h, w1, t1, tw, offset_y, offset_z = self.section_parameters
        hw = h - t1

        A_i = np.array([w1*t1, tw*hw])
        A_t = np.sum(A_i)

        z_ci = np.array([0, 0])
        y_ci = np.array([((t1+hw)/2), 0])

        Yc = (y_ci@A_i) / A_t
        Zc = (z_ci@A_i) / A_t

        I_zi = np.array([(w1*t1**3)/12, (tw*hw**3)/12])
        I_yi = np.array([(t1*w1**3)/12, (hw*tw**3)/12])
        I_yzi = np.array([0, 0])  

        area = A_t
        Iyy = np.sum(I_yi + ((z_ci-Zc)**2)*A_i)
        Izz = np.sum(I_zi + ((y_ci-Yc)**2)*A_i)
        Iyz = np.sum(I_yzi + ((y_ci-Yc)*(z_ci-Zc))*A_i)

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

        h, w1, t1, tw, offset_y, offset_z = self.section_parameters
        hw = h - t1

        Zp_right = [0, tw/2, tw/2, w1/2, w1/2, 0]
        Yp_right = [-(hw/2), -(hw/2), (hw/2), (hw/2), (hw/2)+t1, (hw/2)+t1]

        Zp_left = -np.flip(Zp_right)
        Yp_left =  np.flip(Yp_right)

        Zp = np.array([Zp_right, Zp_left]).flatten() + offset_z
        Yp = np.array([Yp_right, Yp_left]).flatten() + offset_y

        Zc, Yc = self.centroid

        Zc_offset = Zc + offset_z    
        Yc_offset = Yc + offset_y

        return Zp, Yp, Zc_offset, Yc_offset

    def _as_dict(self):
        return {
            "section_type_label" : self.section_type_label,
            "section_parameters" : self.section_parameters,
            "section_properties" : self.section_properties,
        }