from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    x: float
    y: float
    z: float

    def coords(self):
        return np.array(tuple(self))

    def set_coords(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Point(self.x, self.y, self.z)

    def as_dict(self) -> dict:
        return {
            "x": float(self.x),
            "y": float(self.y),
            "z": float(self.z),
        }

    def __add__(self, other):
        point = self.copy()
        point += other
        return point

    def __sub__(self, other):
        point = self.copy()
        point -= other
        return point

    def __mul__(self, other):
        point = self.copy()
        point *= other
        return point

    def __div__(self, other):
        point = self.copy()
        point /= other
        return point

    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return self - other

    def __rmul__(self, other):
        return self * other

    def __rdiv__(self, other):
        return self / other

    def __iadd__(self, other):
        new_coords = self.coords() + other
        self.set_coords(*new_coords)
        return self

    def __isub__(self, other):
        new_coords = self.coords() - other
        self.set_coords(*new_coords)
        return self

    def __imul__(self, other):
        new_coords = self.coords() * other
        self.set_coords(*new_coords)
        return self

    def __idiv__(self, other):
        new_coords = self.coords() / other
        self.set_coords(*new_coords)
        return self

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __array__(self, *args, **kwargs):
        return np.array([self.x, self.y, self.z], *args, **kwargs)

    def __hash__(self) -> int:
        return id(self)
