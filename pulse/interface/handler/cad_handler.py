import gmsh
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange

from pulse.tools.utils import m_to_mm, in_to_mm
import numpy as np


class CADHandler:
    def __init__(self):
        pass

    def save(self, path, pipeline, unit="meter"):
        gmsh.initialize("", False)
        for structure in pipeline.structures: 

            if isinstance(structure, Pipe):
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                
                if unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                
                elif unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)

                start_coords = gmsh.model.occ.add_point(*start_coords)
                end_coords = gmsh.model.occ.add_point(*end_coords)

                gmsh.model.occ.add_line(start_coords, end_coords)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                _center_coords = structure.center.coords()

                if unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                    center_coords = m_to_mm(_center_coords)
                
                elif unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)
                    center_coords = in_to_mm(_center_coords)

                start_coords = gmsh.model.occ.add_point(*start_coords)
                end_coords = gmsh.model.occ.add_point(*end_coords)
                center_point = gmsh.model.occ.add_point(*center_coords)

                gmsh.model.occ.add_circle_arc(start_coords, center_point, end_coords)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))
        gmsh.finalize()