import gmsh

from pulse.editor.structures import Bend, Pipe
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_length_unit


class CADHandler:
    def __init__(self):
        pass

    def save(self, path, pipeline, unit="meter"):
        gmsh.initialize("", False)
        for structure in pipeline.structures: 

            if isinstance(structure, Pipe):
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()

                # converting the units
                start_coords = convert_length_unit(_start_coords, unit, "mm")
                end_coords = convert_length_unit(_end_coords, unit, "mm")
    
                start_coords = gmsh.model.occ.add_point(*start_coords)
                end_coords = gmsh.model.occ.add_point(*end_coords)

                gmsh.model.occ.add_line(start_coords, end_coords)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                _center_coords = structure.center.coords()

                # converting the units
                start_coords = convert_length_unit(_start_coords, unit, "mm")
                end_coords = convert_length_unit(_end_coords, unit, "mm")
                center_coords = convert_length_unit(_center_coords, unit, "mm")

                start_coords = gmsh.model.occ.add_point(*start_coords)
                end_coords = gmsh.model.occ.add_point(*end_coords)
                center_point = gmsh.model.occ.add_point(*center_coords)

                gmsh.model.occ.add_circle_arc(start_coords, center_point, end_coords)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))
        gmsh.finalize()