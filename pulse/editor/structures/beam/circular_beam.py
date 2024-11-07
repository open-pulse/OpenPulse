from ..point import Point
from .beam import Beam


class CircularBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.1)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import CircularBeamActor

        return CircularBeamActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "CircularBeam":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = CircularBeam(
            start,
            end,
            diameter=section_parameters[0],
            thickness=section_parameters[1],
        )

        section_info = {
            "section_parameters": section_parameters,
            "section_type_label": data["section_type_label"],
            "section_properties": data["section_properties"],
        }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "beam_1"

        return structure
