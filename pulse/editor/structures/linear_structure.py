import numpy as np

from .point import Point
from .structure import Structure


class LinearStructure(Structure):
    """
    Abstract class to handle structures represented by a stright line.
    """

    start: Point
    end: Point

    def __init__(self, start: Point, end: Point, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end

    @property
    def arc_length(self):
        return np.linalg.norm(self.end - self.start)

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

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }
