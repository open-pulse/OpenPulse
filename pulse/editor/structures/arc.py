import numpy as np
import gmsh
from typing import Callable

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

        if np.allclose(v, [0,0,0]):
            mid_coords = _start + strucutre_vector / 2
            mid = Point(*mid_coords)
            return cls(start, end, mid, *args, **kwargs)

        v = v / np.linalg.norm(v)
        theta = np.arccos(np.dot(v, strucutre_vector) / norm_structure_vector)

        if theta == 0:
            r = norm_structure_vector / 2
            center = _start + v * r
            mid_coords = center + tangency * r

        else:
            r = norm_structure_vector * np.sin(theta) / np.sin(np.pi - 2 * theta)
            m = strucutre_vector / 2 + _start
            center = _start + v * r
            mid_point_direction = normalize(m - center)

            if np.dot(tangency, strucutre_vector) < 0:
                mid_point_direction *= -1

            mid_coords = center + mid_point_direction * r

        mid = Point(*mid_coords)
        return cls(start, end, mid, *args, **kwargs)

    @property
    def center(self) -> Point | None:
        v1 = self.start.coords() - self.mid.coords()
        v2 = self.end.coords() - self.mid.coords()

        v11 = np.dot(v1, v1)
        v22 = np.dot(v2, v2)
        v12 = np.dot(v1, v2)

        a = 2 * (v11*v22 - v12**2)
        if a == 0:
            return None

        b = (1 / a)
        k1 = b * v22*(v11 - v12)
        k2 = b * v11*(v22 - v12)

        P0 = self.mid.coords() + k1*v1 + k2*v2
        return Point(*P0)

    @property
    def curvature_radius(self) -> Point:
        return np.linalg.norm(self.center - self.start)

    @property
    def arc_length(self):
        u = self.start.coords() - self.center.coords()
        v = self.end.coords() - self.center.coords()

        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        cos_alpha = np.dot(u, v) / (norm_u * norm_v)

        average_radius = (norm_u + norm_v) / 2
        return np.arccos(cos_alpha) * average_radius

    def angle(self) -> float:
        center = self.center
        if center is None:
            return 0
        
        u = normalize(self.start.coords() - center.coords())
        v = normalize(self.end.coords() - center.coords())
        n = np.cross(u, v)
        angle = np.arccos(np.dot(u, v))

        if np.dot(n, self.normal()) > 0:
            return angle
        return 2 * np.pi - angle

    def normal(self) -> np.ndarray:
        u = normalize(self.start.coords() - self.mid.coords())
        v = normalize(self.end.coords() - self.mid.coords())
        return np.cross(v, u)

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

    def add_to_gmsh(
        self,
        cad: gmsh.model.occ | gmsh.model.geo = gmsh.model.occ,
        convert_unit: Callable[[float], float] = lambda x: x,
    ) -> list[int]:

        start = cad.add_point(*convert_unit(self.start.coords()))
        end = cad.add_point(*convert_unit(self.end.coords()))
        mid = cad.add_point(*convert_unit(self.mid.coords()))
        return [cad.add_circle_arc(start, mid, end, center=False)]
