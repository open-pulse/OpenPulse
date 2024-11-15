from .point import Point
from .structure import Structure
import numpy as np


class LinearStructure(Structure):
    """
    Abstract class to handle common stuff to most structures.
    """

    def __init__(self, start: Point, end: Point, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end

    def get_points(self):
        return [
            self.start,
            self.end,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def interpolate(self, t: float):
        # t is the percentage of the structure traveled
        return self.start + t * (self.end - self.start)

    def get_division_point_from_line(self, selected_point: str, division_data: list):

        start_coords = self.start.coords()
        end_coords = self.end.coords()

        if selected_point == "start_point":
            selected_coords = start_coords
        else:
            selected_coords = end_coords

        t = None
        v = (end_coords - start_coords)

        for i, d in enumerate(division_data):
            if isinstance(d, float | int):

                if i < 3:
                    abs_vi = abs(v[i])
                else:
                    abs_vi = np.linalg.norm(v)

                if abs(d) < abs_vi:

                    if list(start_coords) == list(selected_coords):
                        t = d / abs_vi
                    else:
                        t = (abs_vi - d) / abs_vi
                    break

                else:
                    # print(f"Invalid distance typed.")
                    return None

        if t is None:
            return None
        
        internal_coords = start_coords + t * v

        return Point(*internal_coords)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }