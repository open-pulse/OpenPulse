from molde.colors import TURQUOISE_7

from .point import Point
from .linear_structure import LinearStructure


class ExpansionJoint(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.color = TURQUOISE_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ExpansionJointActor

        return ExpansionJointActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "ExpansionJoint":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])

        expansion_joint_info = data["expansion_joint_info"]
        diameter = expansion_joint_info["effective_diameter"]

        structure = ExpansionJoint(
            start, end, diameter=diameter, thickness=0.05 * diameter
        )

        section_info = {"section_type_label" : "expansion_joint"}
        structure.extra_info["cross_section_info"] = section_info

        structure.extra_info["expansion_joint_info"] = expansion_joint_info
        structure.extra_info["structural_element_type"] = "expansion_joint"

        return structure
