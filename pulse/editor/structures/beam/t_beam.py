from .beam import Beam


class TBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness_1 = kwargs.get("thickness_1", 0.01)
        self.thickness_2 = kwargs.get("thickness_2", 0.01)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "width": self.width,
            "height": self.height,
            "thickness_1": self.thickness_1,
            "thickness_2": self.thickness_2,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import TBeamActor

        return TBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
