from molde.colors import PURPLE_7
from .arc import Arc


class ArcBend(Arc):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.color = PURPLE_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ArcBendActor

        return ArcBendActor(self)
