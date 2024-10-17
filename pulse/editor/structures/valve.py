from molde.colors import PINK_6
from .linear_structure import LinearStructure


class Valve(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.flange_outer_diameter = kwargs.get("flange_outer_diameter", 0.2)
        self.flange_length = kwargs.get("flange_length", 0.05)
        self.color = PINK_6

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }
    
    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ValveActor

        return ValveActor(self)
