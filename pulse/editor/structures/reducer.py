from molde.colors import TEAL_7

from .point import Point
from .linear_structure import LinearStructure


class Reducer(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.initial_diameter = kwargs.get("initial_diameter", 0.1)
        self.final_diameter = kwargs.get("final_diameter", 0.05)
        self.initial_offset_y = kwargs.get("initial_offset_y", 0)
        self.initial_offset_z = kwargs.get("initial_offset_z", 0)
        self.final_offset_y = kwargs.get("final_offset_y", 0)
        self.final_offset_z = kwargs.get("final_offset_z", 0)
        self.thickness = kwargs.get("thickness", 0.01)
        self.color = TEAL_7

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ReducerActor

        return ReducerActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "Reducer":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        section_parameters = data["section_parameters"]
        structure = Reducer(
            start,
            end,
            initial_diameter=section_parameters[0],
            final_diameter=section_parameters[4],
            thickness=section_parameters[1],
            initial_offset_y=section_parameters[2],
            initial_offset_z=section_parameters[3],
            final_offset_y=section_parameters[6],
            final_offset_z=section_parameters[7],
        )
        section_info = {
            "section_type_label": data["section_type_label"],
            "section_parameters": section_parameters,
        }
        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"
        return structure
