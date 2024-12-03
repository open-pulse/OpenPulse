import numpy as np
import gmsh
from typing import Callable

from .point import Point
from .structure import Structure
import numpy as np


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
        self.offset_y = kwargs.get("offset_y", 0)
        self.offset_z = kwargs.get("offset_z", 0)

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

    def get_division_point_from_line(self, selected_point: str, division_data: list) -> Point | None:

        """
            
            This method returns the division point evaluated by distance from a reference point. If the
            entered distance is out-of the line bounds the returned value is None.

        
            The equation of a straight line can be written in parametric form as follows:

                P = Po + v * t,

            where v = [a, b, c] is the directional vector of line. The parametric equation can be
            expressed in terms of each coordinate in the form: 

                X = Xo +  a * t
                Y = Yo +  b * t
                Z = Zo +  c * t

            For a given distance dX between the reference point X_start and X we have dX = |X - X_start|, therefore
            if we are interested in t >= 0 once dX >= 0 we get from the parametric relation:

                dX = |X - X_start| = |a| * t
                t = dX / |a|.

            Considering dX as the distance between points X and X_end, and defining dX' = |X - X_start| we obtain, 
            in a similar way:

                dX = |X - X_end|
                dX' = |a - dX| = a * t
                t = dX' / |a|.

        """

        start_coords = self.start.coords()
        end_coords = self.end.coords()

        t = None
        v = (end_coords - start_coords)

        for i, d in enumerate(division_data):
            if isinstance(d, float | int):

                if i < 3:
                    abs_vi = abs(v[i])
                else:
                    abs_vi = np.linalg.norm(v)

                if abs(d) < abs_vi:

                    if selected_point == "start_point":
                        t = d / abs_vi
                    else:
                        t = (abs_vi - d) / abs_vi
                    break

                else:
                    # print(f"Invalid distance typed.")
                    return None

        if t is None:
            return None
        
        internal_coords = start_coords + t * v

        return Point(*internal_coords)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }
    
    def add_to_gmsh(
        self,
        cad: gmsh.model.occ | gmsh.model.geo = gmsh.model.occ,
        convert_unit: Callable[[float], float] = lambda x: x,
    ) -> list[int]:

        start = cad.add_point(*convert_unit(self.start.coords()))
        end = cad.add_point(*convert_unit(self.end.coords()))
        return [cad.add_line(start, end)]
