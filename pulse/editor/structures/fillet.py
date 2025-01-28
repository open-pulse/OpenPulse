import gmsh
import numpy as np
from typing import Callable

from .point import Point
from .structure import Structure


def normalize(vector):
    return vector / np.linalg.norm(vector)


class Fillet(Structure):
    """
    Abstract class to handle structures represented by arcs that are
    inserted to smooth corners.
    """

    start: Point
    end: Point
    corner: Point
    curvature_radius: float

    def __init__(self, start: Point, end: Point, corner: Point, curvature_radius: float, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.corner = corner
        self.curvature_radius = curvature_radius
        self.auto = True

        self.center_coords = None

    @property
    def center(self):
        if self.is_colapsed():
            return self.corner.copy()

        u = normalize(self.start.coords() - self.corner.coords())
        v = normalize(self.end.coords() - self.corner.coords())
        n = np.cross(u, v)

        A = np.array([u, v, n], dtype=float)
        b = np.array(
            [
                np.sum(u * self.start.coords()),
                np.sum(v * self.end.coords()),
                np.sum(n * self.start.coords()),
            ],
            dtype=float,
        )
        center_coords = np.linalg.solve(A, b)

        # TODO @vitorslongo please refactor this.
        # Some variable names are conflicting with the ones above,
        # and others are being unnecessarily repeated.
        middle_coords = (self.start.coords() + self.end.coords()) / 2
        normal_vector = np.cross(self.end.coords() - self.start.coords(), center_coords - self.start.coords())
        bisector_direction = np.cross(normal_vector, self.end.coords() - self.start.coords())

        u = center_coords - middle_coords
        v = bisector_direction
        projection_uv = (np.dot(u, v) / (np.linalg.norm(v)**2)) * v
        corrected_center_coords = middle_coords + projection_uv

        return Point(*corrected_center_coords)

    @property
    def arc_length(self):
        u = self.start.coords() - self.center.coords()
        v = self.end.coords() - self.center.coords()

        norm_u = np.linalg.norm(u)
        norm_v = np.linalg.norm(v)
        cos_alpha = np.dot(u, v) / (norm_u * norm_v)

        average_radius = (norm_u + norm_v) / 2
        return np.arccos(cos_alpha) * average_radius

    def update_corner_from_center(self, center):
        self.auto = False
        a_vector = self.start - center
        b_vector = self.end - center
        a_vector_normalized = a_vector / np.linalg.norm(a_vector)
        b_vector_normalized = b_vector / np.linalg.norm(b_vector)
        c_vector = a_vector_normalized + b_vector_normalized
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        magic = np.dot(a_vector, b_vector) + self.curvature_radius**2
        corner_distance = (self.curvature_radius**2) * np.sqrt(2 / magic)
        corner = center + c_vector_normalized * corner_distance
        self.corner.set_coords(*corner)

    def get_points(self):
        return [
            self.start,
            self.end,
            self.corner,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def normalize_values_vector(self, vec_a: np.ndarray, vec_b: np.ndarray):
        '''
        Updates the start and end points of a curve based on the curvature radius
        and the tangencies of each connection.
        '''
        # The outward tangency of the curve is in the oposite
        # direction of the structure connected to it.
        vec_a, vec_b = -vec_a, -vec_b

        sin_angle = np.linalg.norm(vec_a - vec_b) / 2
        angle = np.arcsin(sin_angle)
        corner_distance = np.cos(angle) * self.curvature_radius / np.sin(angle)
        self.start.set_coords(*(self.corner.coords() + corner_distance * vec_a))
        self.end.set_coords(*(self.corner.coords() + corner_distance * vec_b))

    def colapse(self):
        self.start.set_coords(*self.corner.coords())
        self.end.set_coords(*self.corner.coords())

    def is_colapsed(self):
        a = np.allclose(self.start.coords(), self.corner.coords())
        b = np.allclose(self.corner.coords(), self.end.coords())
        return a and b

    def interpolate(self, t: float):
        # t is the percentage of the bend traveled
        intermediary_projection_point = self.start + t * (self.end - self.start)
        direction = normalize(intermediary_projection_point - self.center)
        return self.center + direction * self.curvature_radius

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "corner": self.corner,
            "curvature_radius": self.curvature_radius,
            "auto": self.auto,
        }

    def add_to_gmsh(
        self,
        cad: gmsh.model.occ | gmsh.model.geo = gmsh.model.occ,
        convert_unit: Callable[[float], float] = lambda x: x,
    ) -> list[int]:

        if self.is_colapsed():
            return []

        start = cad.add_point(*convert_unit(self.start.coords()))
        end = cad.add_point(*convert_unit(self.end.coords()))
        middle = cad.add_point(*convert_unit(self.center.coords()))
        return [cad.add_circle_arc(start, middle, end)]
        