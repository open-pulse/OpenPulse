from dataclasses import dataclass, field

import numpy as np


@dataclass
class SectionDataForRenders:

    undeformed_rotation_rx: np.ndarray
    undeformed_rotation_ry: np.ndarray
    undeformed_rotation_rz: np.ndarray

    section_parameters_render: list | None = field(default_factory=list)

    def set_deformed_rotations(self, rot_x: float, rot_y: float, rot_z: float):
        self.deformed_rotation_rx = rot_x
        self.deformed_rotation_ry = rot_y
        self.deformed_rotation_rz = rot_z

    @property
    def deformed_rotation_rxyz(self):
        return [self.deformed_rotation_rx, self.deformed_rotation_ry, self.deformed_rotation_rz]

    @property
    def undeformed_rotation_rxyz(self):
        return [self.undeformed_rotation_rx, self.undeformed_rotation_ry, self.undeformed_rotation_rz]
