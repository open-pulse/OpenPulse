from ..point import Point
from .beam import Beam


class IBeam(Beam):
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
        from pulse.interface.viewer_3d.actors import IBeamActor

        return IBeamActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "IBeam":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = IBeam(
            start,
            end,
            height=section_parameters[0],
            width_1=section_parameters[1],
            width_2=section_parameters[3],
            thickness_1=section_parameters[2],
            thickness_2=section_parameters[4],
            thickness_3=section_parameters[5],
        )

        section_info = {
            "section_parameters": section_parameters,
            "section_type_label": data["section_type_label"],
            "section_properties": data["section_properties"],
        }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "beam_1"

        return structure
