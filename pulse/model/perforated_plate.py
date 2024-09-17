import numpy as np
from math import pi
from scipy.special import jv

def Foks_function(x):
    a = np.array([1 ,  -1.40925 , 0 , 0.33818, 0 , 0.06793, -0.02287 , 0.03015 , -0.01641 , 0.01729 , -0.01248 , 0.01205 , -0.00985])
    b = np.arange(13)
    return np.sum(np.dot(a,x**b))

class PerforatedPlate:
    def __init__(self, pp_data: dict):
        
        self.type = pp_data.get("type", 0)
        self.hole_diameter = pp_data.get("hole_diameter", None)
        self.thickness = pp_data.get("plate_thickness", None)
        self.porosity = pp_data.get("area_porosity", None)
        self.linear_discharge_coefficient = pp_data.get("discharge_coefficient", 1)
        self.single_hole = pp_data.get("single_hole", False)
        self.nonlinear_effects = pp_data.get("nonlinear_effects", False)
        self.nonlinear_discharge_coefficient = pp_data.get("nonlinear_discharge_coefficient", 0.76)
        self.correction_factor = pp_data.get("correction_factor", 1)
        self.bias_flow_effects = pp_data.get("bias_flow_effects", True)
        self.bias_flow_coefficient = pp_data.get("bias_flow_coefficient", 1)
        self.dimensionless_impedance = pp_data.get("dimensionless_impedance", None)
        self.dimensionless_impedance_table_name = None

    @property
    def foks_delta(self):
        if self.single_hole:
            return pi * self.hole_diameter / 4 
        else:
            return pi * self.hole_diameter * Foks_function(np.sqrt(self.porosity)) / 4 

    def radiation_impedance(self, wave_number):
        dividend = jv(1,wave_number * self.hole_diameter)
        divisor = wave_number * self.hole_diameter / 2
        return (1 - dividend / divisor ) /self.porosity

    # def flow_impedance(self, mach):
    #     return 4*mach / (3*pi * self.porosity * self.linear_discharge_coefficient**2)

    def nonlinear_impedance(self, speed_of_sound, u_n):
        return u_n*(1 - self.porosity**2)*self.correction_factor/(2*speed_of_sound*(self.porosity*self.nonlinear_discharge_coefficient)**2)

    def bias_impedance(self, mach):
        den = (1 - self.porosity**2) * (self.bias_coefficient * mach)
        num = (self.porosity * self.linear_discharge_coefficient**2)
        return den / num