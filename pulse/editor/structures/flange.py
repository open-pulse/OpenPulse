from molde.colors import GREEN_7

from .point import Point
from .linear_structure import LinearStructure


class Flange(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # I am adding 0.02 to the diameter just to appear nicer as
        # a default thickness in the presentation
        self.diameter = kwargs.get("diameter", 0.1 + 0.02)
        self.thickness = kwargs.get("thickness", 0.01 + 0.02)
        self.offset_y = kwargs.get("offset_y", 0)
        self.offset_z = kwargs.get("offset_z", 0)

        self.color = GREEN_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }
    
    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import FlangeActor

        return FlangeActor(self)
    
    @classmethod
    def load_from_data(cls, data: dict) -> "Flange":
        start = Point(*data['start_coords'])
        end = Point(*data['end_coords'])
        section_parameters = data["section_parameters"]
        structure = Flange(
            start,
            end,
            diameter = section_parameters[0],
            thickness = section_parameters[1],
            offset_y = section_parameters[2],
            offset_z = section_parameters[3],
        )
        section_info = {
            "section_type_label" : data["section_type_label"],
            "section_parameters" : section_parameters
        }
        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"
        return structure
