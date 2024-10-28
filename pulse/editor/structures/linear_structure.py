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
    
    def interpolate_projection(self, dx: float, dy: float, dz : float, invert_origin : bool):
        if not invert_origin:
            guide_point = self.start + [dx, dy, dz]
        else:
            guide_point = self.end + [dx, dy, dz]

        tube_vector = self.end - self.start
        guide_vector = guide_point - self.start

        projection = np.dot((np.dot(guide_vector, tube_vector) / np.linalg.norm(tube_vector)**2), tube_vector)
        projection_point = Point(projection[0], projection[1], projection[2])

        return guide_point, projection_point

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }
