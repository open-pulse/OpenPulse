from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING

import numpy as np
from scipy.special import jv

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


class AcousticBehavior(IntEnum):
    OPEN = 0
    PARTIALLY_CLOSED = 1
    CLOSED = 2


@dataclass
class ExpansionJointData:
    ejoint_name: str = ""
    ejoint_length: float = 0
    ejoint_mass: float = 0
    effective_diameter: float = 0
    offset_y: float = 0
    offset_z: float = 0
    values: list = field(default_factory=list)
    rods_included: bool = False
    axial_locking_criteria: float = 1


@dataclass
class ValveData:
    valve_name: str = ""
    valve_length: float = 0
    valve_mass: float = 0
    valve_stiffening_factor: float = 10
    effective_diameter: float = 0,
    wall_thickness: float = 0,
    offset_y: float = 0,
    offset_z: float = 0,
    flange_diameter: float = 0,
    flange_length: float = 0,
    body_section_parameters: list = field(default_factory=list)
    flange_section_parameters: list = field(default_factory=list)

    acoustic_behavior: AcousticBehavior = AcousticBehavior.CLOSED,
    orifice_plate_thickness: float = 0,
    blocking_length: float = 0,


@dataclass
class AcousticLinkData:
    coords: np.ndarray
    indexes_rows: list | np.ndarray
    indexes_cols:  list | np.ndarray
    element_attributes : "ElementAttributes"
    diameters: list
    length: float


@dataclass
class PerforatedPlateData:
    type: int = 0
    hole_diameter: float | None = None
    thickness: float | None = None
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


class PerforatedPlateFormulation(IntEnum):
    OPENPULSE = 0
    MELLING = 1
    COMMON_PIPE = 2


def Foks_function(x):
    a = np.array([1 ,  -1.40925 , 0 , 0.33818, 0 , 0.06793, -0.02287 , 0.03015 , -0.01641 , 0.01729 , -0.01248 , 0.01205 , -0.00985])
    b = np.arange(13)
    return np.sum(np.dot(a,x**b))