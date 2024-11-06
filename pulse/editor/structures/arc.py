import numpy as np

from .point import Point
from .structure import Structure
from pulse.utils.math_utils import normalize


class Arc(Structure):
    """
    Abstract class to handle structures represented by arcs inserted at any position. 
    Arcs are represented as a 3 point arc.
    """

    start: Point
    end: Point
    mid: Point

    def __init__(self, start: Point, end: Point, mid: Point, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.mid = mid

    @classmethod
    def from_tangency(cls, start: Point, end: Point, tangency: np.ndarray, *args, **kwargs) -> "Arc":
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

    @property
    def arc_length(self):
        u = self.start.coords() - self.center()
        v = self.end.coords() - self.center()

        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        cos_alpha = np.dot(u, v) / (norm_u * norm_v)

        average_radius = (norm_u + norm_v) / 2
        return np.arccos(cos_alpha) * average_radius

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
