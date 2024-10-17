from .beam import Beam


class RectangularBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness_width = kwargs.get("thickness_width", 0.01)
        self.thickness_height = kwargs.get("thickness_height", 0.01)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "height": self.height,
            "width": self.width,
            "thickness_width": self.thickness_width,
            "thickness_height": self.thickness_height,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import RectangularBeamActor

        return RectangularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
