from molde.colors import PURPLE_7
from .arc import Arc
from .point import Point


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

    @classmethod
    def load_from_data(cls, data: dict) -> "ArcBend":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        mid = Point(*data["mid_coords"])
        section_parameters = data["section_parameters"]
        structure = ArcBend(
            start,
            end,
            mid,
            diameter=section_parameters[0],
            thickness=section_parameters[1],
        )
        section_info = {
            "section_type_label": data["section_type_label"],
            "section_parameters": section_parameters,
        }
        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"
        return structure
