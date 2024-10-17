import numpy as np

from molde.colors import PURPLE_7

from .point import Point
from .simple_curve import SimpleCurve


class Bend(SimpleCurve):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.center_coords = kwargs.get("center_coords")
        self.color = PURPLE_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import BendActor

        return BendActor(self)
