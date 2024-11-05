import numpy as np

from .point import Point
from .structure import Structure
from pulse.utils.math_utils import normalize


class Curve(Structure):
    def __init__(self, start: Point, end: Point, mid: Point, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.mid = mid

    @classmethod
    def from_tangency(cls, start: Point, end: Point, tangency: np.ndarray) -> "Curve":
        mid = Point(0, 0, 0)
        return cls(start, end, mid)

    @property
    def center(self) -> Point:
        pass

    @property
    def curvature_radius(self) -> Point:
        return np.linalg.norm(self.center - self.start)
