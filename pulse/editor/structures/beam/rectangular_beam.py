from ..point import Point
from .beam import Beam


class RectangularBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness_width = kwargs.get("thickness_width", 0.01)
        self.thickness_height = kwargs.get("thickness_height", 0.01)
        self.angle = 0

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

    @classmethod
    def load_from_data(cls, data: dict) -> "RectangularBeam":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = RectangularBeam(
            start,
            end,
            width=section_parameters[0],
            height=section_parameters[1],
            thickness_width=(section_parameters[0] - section_parameters[2]) / 2,
            thickness_height=(section_parameters[0] - section_parameters[3]) / 2,
        )

        section_info = {
            "section_parameters": section_parameters,
            "section_type_label": data["section_type_label"],
            "section_properties": data["section_properties"],
        }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "beam_1"

        return structure
