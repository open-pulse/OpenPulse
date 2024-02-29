from opps.model import Pipe, Bend, Point, Flange

from pulse.tools.utils import m_to_mm, in_to_mm
from pulse import app

import numpy as np
import sys
import gmsh

np.loadtxt

class GeometryHandler:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self.length_unit = "meter"
        self.pipeline = list()

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def set_length_unit(self, unit):
        if unit in ["meter", "milimiter", "inch"]:
            self.length_unit = unit

    def create_geometry(self):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)
        for structure in self.pipeline.structures: 

            if isinstance(structure, Pipe):
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                
                if self.length_unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                
                elif self.length_unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)

                start_point = gmsh.model.occ.add_point(*start_coords)
                end_point = gmsh.model.occ.add_point(*end_coords)

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                
                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                _center_coords = structure.center.coords()

                if self.length_unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                    center_coords = m_to_mm(_center_coords)
                
                elif self.length_unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)
                    center_coords = in_to_mm(_center_coords)

                start_point = gmsh.model.occ.add_point(*start_coords)
                end_point = gmsh.model.occ.add_point(*end_coords)
                center_point = gmsh.model.occ.add_point(*center_coords)

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()

    def process_pipeline(self, build_data : dict):
        """ This method builds structures based on entity file data.
        
        Parameters:
        -----------
        build_data: dictionary
            
            a dictionary containing all required data to build the pipeline structures.

        Returns
        -------
        pipeline: Pipeline type

            pipeline data to...
        """
        
        editor = app().geometry_toolbox.editor
        editor.reset()

        structures = []
        for key, data in build_data.items():

            self.cross_section_info = { 
                "section label" : data['section label'],
                "section parameters" : data['section parameters'],
            }
            self.material_id = data['material id']

            if data["section label"] == "pipe (constant)":
                diameter = data["section parameters"][0]
            else:
                diameter = 0.01

            if key[1] == "Bend":

                start_coords = data['start point']
                start = Point(*start_coords)

                end_coords = data['end point']
                end = Point(*end_coords)

                corner_coords = data['corner point']
                corner = Point(*corner_coords)

                curvature = data['curvature']

                bend = Bend(start, end, corner, curvature)
                bend.extra_info["cross_section_info"] = self.cross_section_info
                bend.extra_info["material_info"] = self.material_id
                bend.set_diameter(diameter)

                structures.append(bend)

            else:

                start_coords = data['start point']
                start = Point(*start_coords)

                end_coords = data['end point']
                end = Point(*end_coords)

                pipe = Pipe(start, end)
                pipe.extra_info["cross_section_info"] = self.cross_section_info
                pipe.extra_info["material_info"] = self.material_id
                pipe.set_diameter(diameter)

                structures.append(pipe)

        pipeline = app().geometry_toolbox.pipeline
        pipeline.structures.clear()

        if len(structures):
            pipeline.structures.extend(structures)
            editor.merge_coincident_points()

        return pipeline
    
    def export_cad_file(self, path):
        self.create_geometry()

        # if '-nopopup' not in sys.argv:
        #     gmsh.option.setNumber('General.FltkColorScheme', 1)
        #     gmsh.fltk.run()

        gmsh.write(str(path))
        gmsh.finalize()