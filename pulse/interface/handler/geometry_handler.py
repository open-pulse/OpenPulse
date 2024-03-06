from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import m_to_mm, in_to_mm, mm_to_m

from opps.model import Pipe, Bend, Point, Flange

import math
import gmsh
import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

def normalize(vector):
    return vector / np.linalg.norm(vector)

class GeometryHandler:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self.length_unit = "meter"
        self.pipeline = list()
        self.merged_points = list()
        self.points_coords = dict()
        self.points_coords_cache = dict()

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

            if "structural_element_type" not in data.keys():
                continue

            if "section_type_label" not in data.keys():
                continue

            if "section_parameters" not in data.keys():
                continue

            structural_element_type = data["structural_element_type"]
            section_type_label = data["section_type_label"]
            section_parameters = data["section_parameters"]

            if structural_element_type == "pipe_1":
                section_info = {"section_type_label" : "Pipe section",
                                "section_parameters" : section_parameters}
            
            elif structural_element_type == "beam_1":
                if section_type_label == "Generic section":
                    section_parameters = None
                
                section_properties = data["section_properties"]
                section_info = {"section_type_label" : section_type_label,
                                "section_parameters" : section_parameters,
                                "section_properties" : section_properties  }

            else:
                continue

            if "material_id" in data.keys():
                material_id = data['material_id']

            if data["section_type_label"] == "Pipe section":
                diameter = data["section_parameters"][0]
            else:
                diameter = 0.01

            if key[1] == "Bend":

                start_coords = data['start_point']
                start = Point(*start_coords)

                end_coords = data['end_point']
                end = Point(*end_coords)

                corner_coords = data['corner_point']
                corner = Point(*corner_coords)

                curvature = data['curvature']

                bend = Bend(start, end, corner, curvature)
                bend.extra_info["cross_section_info"] = section_info
                bend.extra_info["structural_element_type"] = structural_element_type
                if "material_id" in data.keys():
                    bend.extra_info["material_info"] = material_id
                bend.set_diameter(diameter)

                structures.append(bend)

            else:

                start_coords = data['start_point']
                start = Point(*start_coords)

                end_coords = data['end_point']
                end = Point(*end_coords)

                pipe = Pipe(start, end)
                pipe.extra_info["cross_section_info"] = section_info
                pipe.extra_info["structural_element_type"] = structural_element_type
                if "material_id" in data.keys():
                    pipe.extra_info["material_info"] = material_id
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

    
    def open_cad_file(self, path):

        gmsh.initialize('', False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber('Geometry.Tolerance', 0.001)
        gmsh.open(str(path))

        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)

        self.points_coords = dict()
        for point in points:
            coords = gmsh.model.getValue(*point, [])
            self.points_coords[point[1]] = mm_to_m(coords)

        self.points_coords_cache = self.points_coords.copy()
        self.map_points_according_to_coordinates()

        associated_points = []
        for line in lines:
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][0])
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][1])

        unconnected_points = []
        for point in points:
            if point[1] not in associated_points:
                unconnected_points.append(point[1])

        # # # temporary
        # N = len(points_coords)
        # _data = np.zeros((N, 4), dtype=float)
        # for i, _index, _coords in enumerate(points_coords.items()):
        #     _data[i, 0 ] = _index
        #     _data[i, 1:] = _coords

        # np.savetxt("coordenadas_pontos.dat", _data, delimiter=",", fmt="%i %e %e %e")

        editor = app().geometry_toolbox.editor
        editor.reset()

        structures = list()

        for structure_a in self.process_curved_lines(lines):
            structures.append(structure_a)

        for structure_b in self.process_straight_lines(lines):
            structures.append(structure_b)

        editor.pipeline.structures = structures
        # editor.structures.extend(structures)
        editor.merge_coincident_points()

        if len(self.merged_points):
            self.print_merged_nodes_message()
    
    def process_curved_lines(self, lines):

        curved_structures = []

        for line in lines:

            try:

                start_point = gmsh.model.get_adjacencies(*line)[1][0]
                end_point = gmsh.model.get_adjacencies(*line)[1][1]
                line_type = gmsh.model.get_type(*line)

                start_coords = self.get_point_coords(start_point)
                end_coords = self.get_point_coords(end_point)

                start = Point(*start_coords)
                end = Point(*end_coords)

                line_length = math.dist(start_coords, end_coords)
                
                if line_length < 0.001:
                    self.print_warning_for_small_length(line, line_length)

                if line_type == 'Circle':

                    if len(self.get_point_by_coords(start_coords)) < 2:
                        self.merge_near_points(start_coords)
                        start_coords = self.get_point_coords(start_point)

                    if len(self.get_point_by_coords(end_coords)) < 2:
                        self.merge_near_points(end_coords)
                        end_coords = self.get_point_coords(end_point)                    

                    corner_coords = self.get_corner_point_coords(start_point, end_point)

                    if corner_coords is None:
                        message = f"The connecting lines from 'Circle curve' {line} are parallel "
                        message += "and will be ignored in geometry construction."
                        print(message)
                        continue

                    radius = self.get_radius(corner_coords, start_point, end_point)
                    
                    corner = Point(*corner_coords)

                    pipe = Bend(start, end, corner, radius)
                    curved_structures.append(pipe)

            except Exception as error_log:

                title = "Error while processing curved structures"
                message = str(error_log)
                message += f"\n\nLine: {line}"
                PrintMessageInput([window_title_1, title, message])
                
                continue
        
        return curved_structures

    def process_straight_lines(self, lines):

        straight_structures = []

        for line in lines:

            try:

                start_point = gmsh.model.get_adjacencies(*line)[1][0]
                end_point = gmsh.model.get_adjacencies(*line)[1][1]
                line_type = gmsh.model.get_type(*line)

                start_coords = self.get_point_coords(start_point)
                end_coords = self.get_point_coords(end_point)

                line_length = math.dist(start_coords, end_coords)
                
                if line_length < 0.001:
                    self.print_warning_for_small_length(line, line_length)

                if line_type == 'Line':

                    start = Point(*start_coords)
                    end = Point(*end_coords)

                    pipe = Pipe(start, end)
                    straight_structures.append(pipe)

            except Exception as error_log:

                title = "Error while processing straight structures"
                message = str(error_log)
                message += f"\n\nLine: {line}"
                PrintMessageInput([window_title_1, title, message])
                
                continue

        return straight_structures

    def map_points_according_to_coordinates(self):
        """ This method maps points according to its nodal coordinates.
        """
        self.points_map  = defaultdict(list)
        for index, coords in self.points_coords.items():
            key = str(list(np.round(coords, 8)))
            self.points_map[key].append(index)

    def get_point_coords(self, point):
        return self.points_coords[point]

    def get_point_by_coords(self, coords):
        """ This method returns the points with 'coords' nodal coordinates. 
        """
        key = str(list(np.round(coords, 8)))
        try:
            points = self.points_map[key]
            return points
        except:
            return None

    def get_connecting_line_data(self, coords, point_i):
        """ This method returns the line and its points of duplicated point
            'point_i', where 'point_i' belongs to the line and curve simultaneously.
        """
        line = None
        points = None
        for point in self.get_point_by_coords(coords):
            if point != point_i:
                line = gmsh.model.get_adjacencies(0, point)[0][0]
                points = list(gmsh.model.get_adjacencies(1, line)[1])
        return line, points
    
    def get_corner_point_coords(self, start_point, end_point):
        """
            Reference: https://mathworld.wolfram.com/Line-LineIntersection.html
        """

        coords_start = mm_to_m(gmsh.model.getValue(0, start_point, []))
        coords_end = mm_to_m(gmsh.model.getValue(0, end_point, []))

        _, points_Lstart = self.get_connecting_line_data(coords_start, start_point)
        _, points_Lend = self.get_connecting_line_data(coords_end, end_point)

        X1 = mm_to_m(gmsh.model.getValue(0, points_Lstart[0], []))
        X2 = mm_to_m(gmsh.model.getValue(0, points_Lstart[1], []))

        X3 = mm_to_m(gmsh.model.getValue(0, points_Lend[0], []))
        X4 = mm_to_m(gmsh.model.getValue(0, points_Lend[1], []))

        a = X2 - X1
        b = X4 - X3
        c = X3 - X1

        cross_ab = np.cross(a, b)
        cross_cb = np.cross(c, b)

        if np.round(np.linalg.norm(cross_ab), 8) != 0:
            s = np.dot(cross_cb, cross_ab)/(((np.linalg.norm(cross_ab)))**2)
            Xc = X1 + a*s
            return Xc
        else:
            return None

    def get_radius(self, corner_coords, start_point, end_point):
        """
        """
        start_coords = mm_to_m(gmsh.model.getValue(0, start_point, []))
        end_coords = mm_to_m(gmsh.model.getValue(0, end_point, []))

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords
        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        corner_distance = norm_a_vector / np.sqrt(0.5 * ((np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector)) + 1))

        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = math.dist(center_coords, start_coords)
        end_curve_radius = math.dist(center_coords, end_coords)
        radius = (start_curve_radius + end_curve_radius) / 2

        return radius

    def print_warning_for_small_length(self, line, line_length):

        title = "Small line length detected"
        message = f"The line {line} has a small length which may cause problems "
        message += "in model processing. We reccomend to check the imported geometry "
        message += "to avoid physical inconsistency in model results."
        message += f"\n\nLine length: {round(line_length, 6)} [m]"
        
        PrintMessageInput([window_title_2, title, message])

    def merge_near_points(self, point_coords, tolerance=5e-3):

        points = np.array(list(self.points_coords.keys()))
        coords = np.array(list(self.points_coords.values()))
        dist = np.linalg.norm((coords - point_coords), axis=1)

        mask = dist <  tolerance
        if True in mask:

            points_to_merge = points[mask]
            for point in points_to_merge:
                self.points_coords[point] = point_coords
                if point not in self.merged_points:
                    self.merged_points.append(point)

            self.map_points_according_to_coordinates()
            # print(np.array(list(self.points_coords.values())))

    def print_merged_nodes_message(self):

        title = "Points merging detected"
        message = f"The points {self.merged_points} were merged in geometry processing.\n\n"

        for point in self.merged_points:
            message += f"{point} : {self.points_coords_cache[point]}\n"

        PrintMessageInput([window_title_2, title, message])