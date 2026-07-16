from dataclasses import dataclass, field
from enum import IntEnum

import numpy as np
from scipy.special import jv


class PerforatedPlateFormulation(IntEnum):
    OPENPULSE = 0
    MELLING = 1
    COMMON_PIPE = 2


@dataclass
class PerforatedPlateData:
    type: int = 0
    coords: list = field(default_factory=list)
    hole_diameter: float | None = None
    plate_thickness: float | None = None
    area_porosity: float | None = None
    discharge_coefficient: float = 1
    single_hole: bool = False
    nonlinear_effects: bool = False
    nonlinear_discharge_coefficient: float = 0.76
    correction_factor: float = 1
    bias_flow_effects: bool = True
    bias_flow_coefficient: float = 1
    dimensionless_impedance: float | None = None
    dimensionless_impedance_table_name: str | None = None

    @property
    def foks_delta(self):
        if self.single_hole:
            return np.pi * self.hole_diameter / 4

        return np.pi * self.hole_diameter * Foks_function(np.sqrt(self.area_porosity)) / 4

    def radiation_impedance(self, wave_number):
        dividend = jv(1, wave_number * self.hole_diameter)
        divisor = wave_number * self.hole_diameter / 2
        return (1 - dividend / divisor) / self.area_porosity

    def flow_impedance(self, mach):
        return (4 * mach) / (3 * np.pi * self.area_porosity * self.discharge_coefficient**2)

    def nonlinear_impedance(self, speed_of_sound, u_n):
        num = u_n * (1 - self.area_porosity**2) * self.correction_factor
        den = 2 * speed_of_sound * ((self.area_porosity * self.nonlinear_discharge_coefficient) ** 2)
        return num / den

    def bias_impedance(self, mach):
        num = (1 - self.area_porosity**2) * (self.bias_flow_coefficient * mach)
        den = self.area_porosity * self.discharge_coefficient**2
        return num / den
    
    def as_dict(self):

        return {
            "type" : self.type,
            "coords" : self.coords,
            "hole_diameter" : self.hole_diameter,
            "plate_thickness" : self.plate_thickness,
            "area_porosity" : self.area_porosity,
            "discharge_coefficient" : self.discharge_coefficient,
            "single_hole" : self.single_hole,
            "nonlinear_effects" : self.nonlinear_effects,
            "nonlinear_discharge_coefficient" : self.nonlinear_discharge_coefficient,
            "correction_factor" : self.correction_factor,
            "bias_flow_effects" : self.bias_flow_effects,
            "bias_flow_coefficient" : self.bias_flow_coefficient,
            "dimensionless_impedance" : self.dimensionless_impedance,
            "dimensionless_impedance_table_name" : self.dimensionless_impedance_table_name,
            }


def Foks_function(x):
    a = np.array([1 ,  -1.40925 , 0 , 0.33818, 0 , 0.06793, -0.02287 , 0.03015 , -0.01641 , 0.01729 , -0.01248 , 0.01205 , -0.00985])
    b = np.arange(13)
    return np.sum(np.dot(a,x**b))