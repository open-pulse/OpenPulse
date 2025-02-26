import numpy as np
import gmsh
from typing import Callable
from collections import deque
from itertools import pairwise

from molde.colors import PINK_6
from .point import Point
from .linear_structure import LinearStructure


class Valve(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.flange_outer_diameter = kwargs.get("flange_outer_diameter", 0.2)
        self.flange_length = kwargs.get("flange_length", 0.05)
        self.color = PINK_6

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import ValveActor

        return ValveActor(self)

    def add_to_gmsh(
        self,
        cad: gmsh.model.occ | gmsh.model.geo = gmsh.model.occ,
        convert_unit: Callable[[float], float] = lambda x: x,
    ) -> list[int]:

        valve_info: dict = self.extra_info.get("valve_info")
        if valve_info is None:
            return []

        valve_coords = self._process_valve_points(
            convert_unit(self.start.coords()),
            convert_unit(self.end.coords()),
            valve_info,
        )

        point_tags = []
        for x, y, z in valve_coords:
            tag = cad.add_point(x, y, z)
            point_tags.append(tag)

        line_tags = []
        for p0, p1 in pairwise(point_tags):
            tag = cad.add_line(p0, p1)
            line_tags.append(tag)

        return line_tags

    def _process_valve_points(
        self, start: np.ndarray, end: np.ndarray, valve_info: dict
    ) -> list[np.ndarray]:
        """
        The geometry of a Valve is a bit more complicated.

        If all the possible points are defined the point
        of the valve will look like this:

        ```
        s   ┌──╮      ╭───╮     ╭──┐
        t   │  ├──────┤   ├─────┤  │   e
        a  Ⓐ  Ⓒ     Ⓔ  Ⓕ    Ⓓ  Ⓑ  n
        r   │  ├──────┤   ├─────┤  │   d
        t   └──╯      ╰───╯     ╰──┘
        ```
        """

        A = start
        B = end
        size = np.linalg.norm(B - A)
        v = (B - A) / size

        # If I add the points from the middle to the
        # borders they will always be in the correct
        # sequence, even if some points do not exist
        coord_sequence = deque()

        # Internal points
        if "orifice_plate_thickness" in valve_info.keys():
            internal_length = 1e3 * valve_info["orifice_plate_thickness"]
            E = A + v * (size - internal_length) / 2
            F = A + v * (size + internal_length) / 2
            coord_sequence.appendleft(E)
            coord_sequence.append(F)

        elif "blocking_length" in valve_info.keys():
            internal_length = 1e3 * valve_info["blocking_length"]
            E = A + v * (size - internal_length) / 2
            F = A + v * (size + internal_length) / 2
            coord_sequence.appendleft(E)
            coord_sequence.append(F)

        # Flange points
        if "flange_length" in valve_info.keys():
            flange_length = 1e3 * valve_info["flange_length"]
            C = A + v * flange_length
            D = A + v * (size - flange_length)
            coord_sequence.appendleft(C)
            coord_sequence.append(D)

        # External points
        coord_sequence.appendleft(A)
        coord_sequence.append(B)

        return coord_sequence

    @classmethod
    def load_from_data(cls, data: dict) -> "Valve":
        start = Point(*data["start_coords"])
        end = Point(*data["end_coords"])

        valve_info = data["valve_info"]
        d_out, t, *_ = valve_info["body_section_parameters"]
        flange_outer_diameter, *_ = valve_info["flange_section_parameters"]
        flange_length = valve_info["flange_length"]

        structure = Valve(
            start,
            end,
            diameter=d_out,
            thickness=t,
            flange_outer_diameter=flange_outer_diameter,
            flange_length=flange_length,
        )

        section_info = {"section_type_label" : "valve"}
        structure.extra_info["cross_section_info"] = section_info

        structure.extra_info["valve_info"] = valve_info
        structure.extra_info["structural_element_type"] = "valve"

        return structure
