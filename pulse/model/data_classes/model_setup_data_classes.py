from dataclasses import dataclass, field
from enum import IntEnum
from typing import TYPE_CHECKING

import numpy as np

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