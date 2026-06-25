
from dataclasses import dataclass, field

import numpy as np

from pulse.model.cross_section import CrossSection
from pulse.model.data_classes.data_classes import ExpansionJointData, PerforatedPlateData, ValveData
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.structural_element import DOF_PER_ELEMENT, DOF_PER_NODE_STRUCTURAL

decoupling_matrix_default = np.ones((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=int)


@dataclass
class StructuralElementAttributes:

    element_type: str = "pipe_1"

    fluid: Fluid | None = None
    material: Material | None = None
    cross_section: CrossSection | None = None

    loaded_forces: np.ndarray = field(default_factory = lambda:np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float))

    wall_formulation: str = "thin_wall"
    capped_end: bool = True
    turned_off: bool = False
    adding_mass_effect: bool = False
    force_offset: bool = False

    decoupling_matrix: np.ndarray = field(default_factory = lambda: decoupling_matrix_default)
    decoupling_info: list | None = None # field(default_factory=list)

    xaxis_rotation_angle: float = 0

    # valve data
    valve_data: None | ValveData = None

    # expansion joint data
    expansion_joint_data: None | ExpansionJointData = None

    # perforated plate data
    perforated_plate: None | PerforatedPlateData = None

    # rigid element
    k_factor: float | None = None

    # stress stiffening attributes
    internal_pressure: float = 0
    external_pressure: float = 0


    @property
    def is_section_variable(self):
        if isinstance(self.cross_section, CrossSection):
            return self.cross_section.section_info.section_type_label == "reducer"

        return False