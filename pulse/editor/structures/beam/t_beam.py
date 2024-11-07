from ..point import Point
from .beam import Beam


class TBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness_1 = kwargs.get("thickness_1", 0.01)
        self.thickness_2 = kwargs.get("thickness_2", 0.01)
        self.angle = 0

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

    @classmethod
    def load_from_data(cls, data: dict) -> "TBeam":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = TBeam(
            start,
            end,
            height=section_parameters[0],
            width=section_parameters[1],
            thickness_1=section_parameters[2],
            thickness_2=section_parameters[3],
        )

        section_info = {
            "section_parameters": section_parameters,
            "section_type_label": data["section_type_label"],
            "section_properties": data["section_properties"],
        }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "beam_1"

        return structure
