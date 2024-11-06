import numpy as np

from .point import Point
from .structure import Structure
from pulse.utils.math_utils import normalize


class Arc(Structure):
    def __init__(self, start: Point, end: Point, mid: Point, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.mid = mid

    @classmethod
    def from_tangency(cls, start: Point, end: Point, tangency: np.ndarray, *args, **kwargs) -> "Curve":
        mid = Point(0, 0, 0)
        return cls(start, end, mid, *args, **kwargs)

    @property
    def center(self) -> Point:
        return self.start + [0, 1, 0]

    @property
    def corner(self) -> Point | None:
        return Point(0, 0, 0)

    @property
    def curvature_radius(self) -> Point:
        return np.linalg.norm(self.center - self.start)

    def get_points(self):
        return [
            self.start,
            self.end,
            self.mid,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

        elif self.mid == old:
            self.mid = new
