

from molde.colors import PURPLE_7

from pulse.editor.structures.linear_structure import LinearStructure
from pulse.editor.structures.point import Point


class CouplingElement(LinearStructure):
    def __init__(self, start, end, *args, **kwargs):
        super().__init__(start, end, *args, **kwargs)
        self.color = PURPLE_7

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import CouplingElementActor
        return CouplingElementActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "CouplingElement":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        structure = cls(start, end)
        structure.extra_info["structural_element_type"] = "coupling_element"
        return structure

    