
import numpy as np
from dataclasses import dataclass, field

from pulse.model.structural_element import DOF_PER_NODE_STRUCTURAL, decoupling_matrix
from pulse.model.cross_section import CrossSection
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material


@dataclass
class StructuralElementAttributes:

    element_type: str = "pipe_1"

    fluid: Fluid | None = None
    material: Material | None = None
    cross_section: CrossSection | None = None
    loaded_forces: np.ndarray = field(default_factory = lambda:np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float))

    wall_formulation: str = "thin_wall"
    capped_end: bool = True
    stress_intensification: bool = True
    turned_off: bool = False
    adding_mass_effect: bool = False

    decoupling_matrix: np.ndarray = field(default_factory = lambda: decoupling_matrix)
    decoupling_info: list | None = field(default_factory=list)

    section_parameters_render = None