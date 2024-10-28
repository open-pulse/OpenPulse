from molde.colors import GREEN_7

from .linear_structure import LinearStructure


class Flange(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # I am adding 0.02 to the diameter just to appear nicer as
        # a default thickness in the presentation
        self.diameter = kwargs.get("diameter", 0.1 + 0.02)
        self.thickness = kwargs.get("thickness", 0.01 + 0.02)
        self.color = GREEN_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }
    
    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import FlangeActor

        return FlangeActor(self)
