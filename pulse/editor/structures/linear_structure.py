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
        start = self.start
        end = self.end
        delta = np.array([dx, dy, dz])
        
        if not invert_origin:
            intermediary_projection_point = start + delta
        else:
            delta = - delta
            intermediary_projection_point = end + delta

        structure_vector = end - start
        intermediary_projection_point = start + delta
        mid_point = start + (np.dot(delta, structure_vector) / np.linalg.norm(structure_vector)**2) * structure_vector
        alfa = np.arccos(np.dot(structure_vector / np.linalg.norm(structure_vector), delta / np.linalg.norm(delta))) 
        projection_length = np.linalg.norm(delta) * np.tan(alfa)
        normal_vector = np.cross(delta, mid_point - (start + delta)) # (to the plane)
        projection_point = intermediary_projection_point + np.cross(normal_vector, delta) / np.linalg.norm(np.cross(delta, normal_vector)) * projection_length

        return intermediary_projection_point, projection_point
    

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }
