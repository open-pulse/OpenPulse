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
        '''
        https://github.com/hello.world
        '''

        _start = start.coords()
        _end = end.coords()

        strucutre_vector = _end - _start
        norm_structure_vector = np.linalg.norm(strucutre_vector)

        n = np.cross(strucutre_vector, tangency)
        v = np.cross(tangency, n)
        v = v / np.linalg.norm(v)
        
        theta = np.arccos(np.dot(v, strucutre_vector) / norm_structure_vector)
        print(f"{theta = }")
        if theta == 0:
            r = norm_structure_vector / 2
            c = _start + v * r
            i = c + tangency * r
            mid = Point(*i)
        else:
            r = norm_structure_vector * np.sin(theta) / np.sin(np.pi - 2 * theta)
            c = _start + v * r

            m = strucutre_vector/2 + _start
            w = m - c
            w = w / np.linalg.norm(w)

            i = c + w * r
            mid = Point(*i)
        return cls(start, end, mid, *args, **kwargs)

    @property
    def center(self) -> Point:
        v1 = self.start.coords() - self.mid.coords()
        v2 = self.end.coords() - self.mid.coords()

        v11 = np.dot(v1, v1)
        v22 = np.dot(v2, v2)
        v12 = np.dot(v1, v2)

        b = (1/(2*(v11*v22 - v12**2)))

        k1 = b * v22*(v11 - v12)
        k2 = b * v11*(v22 - v12)

        P0 = self.mid.coords() + k1*v1 + k2*v2
        return Point(*P0)

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
