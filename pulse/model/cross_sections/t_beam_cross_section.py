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

    @property
    def section_parameters(self):
        return [self.h, self.w1, self.t1, self.tw, self.offset_y, self.offset_z]

    @property
    def centroid(self):

        [h, w1, t1, tw, offset_y, offset_z] = self.section_parameters

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

        [h, w1, t1, tw, offset_y, offset_z] = self.section_parameters

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
            "Zc" : Zc,
            "Yc" : Yc, 
            }