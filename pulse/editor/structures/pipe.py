from molde.colors import WHITE

from .point import Point
from .linear_structure import LinearStructure


class Pipe(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.offset_y = kwargs.get("offset_y", 0)
        self.offset_z = kwargs.get("offset_z", 0)

        self.color = WHITE

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import PipeActor

        return PipeActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "Pipe":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = Pipe(
            start,
            end,
            diameter=section_parameters[0],
            thickness=section_parameters[1],
            offset_y=section_parameters[2],
            offset_z=section_parameters[3],
        )
        section_info = {
            "section_type_label": data["section_type_label"],
            "section_parameters": section_parameters,
        }
        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"

        if "psd_name" in data.keys():
            structure.extra_info["psd_name"] = data["psd_name"]
        
        if "pulsation_damper_name" in data.keys():
            structure.extra_info["pulsation_damper_name"] = data["pulsation_damper_name"]
        
        return structure
