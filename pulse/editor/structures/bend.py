from molde.colors import PURPLE_7
from .fillet import Fillet
from .point import Point


class Bend(Fillet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.center_coords = kwargs.get("center_coords")
        self.color = PURPLE_7

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import BendActor

        return BendActor(self)

    @classmethod
    def load_from_data(cls, data: dict) -> "Bend":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])
        corner = Point(*data["corner_coords"])
        curvature_radius = data["curvature_radius"]
        center_coords = data.get("center_coords")
        section_parameters = data["section_parameters"]
        structure = Bend(
            start,
            end,
            corner,
            curvature_radius,
            center_coords=center_coords,
            diameter=section_parameters[0],
            thickness=section_parameters[1],
        )

        # This should not be necessary anymore
        if center_coords is None:
            structure.center_coords = structure.center.coords()

        section_info = {
            "section_type_label": data["section_type_label"],
            "section_parameters": section_parameters,
        }
        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"
        return structure
