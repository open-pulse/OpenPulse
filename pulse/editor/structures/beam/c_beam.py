from .beam import Beam


class CBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.height = kwargs.get("height", 0.1)
        self.width_1 = kwargs.get("width_1", 0.1)
        self.width_2 = kwargs.get("width_2", 0.1)
        self.thickness_1 = kwargs.get("thickness_1", 0.01)
        self.thickness_2 = kwargs.get("thickness_2", 0.01)
        self.thickness_3 = kwargs.get("thickness_3", 0.01)
        self.angle = 0

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "height": self.height,
            "width_1": self.width_1,
            "width_2": self.width_2,
            "thickness_1": self.thickness_1,
            "thickness_2": self.thickness_2,
            "thickness_3": self.thickness_3,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import CBeamActor

        return CBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
