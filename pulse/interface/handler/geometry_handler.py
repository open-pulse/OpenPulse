from typing import TYPE_CHECKING

from pulse import app
from pulse.editor import Pipeline
from pulse.editor.structures import (
    ALL_STRUCTURE_TYPES,
    Arc,
    Beam,
    Bend,
    ExpansionJoint,
    Fillet,
    Flange,
    Pipe,
    Point,
    Reducer,
    Structure,
    Valve,
)
from pulse.interface import error_title, warning_title
from pulse.interface.user_input.numeric_checks.unit_utilities import convert_length_unit
from pulse.interface.user_input.project.print_message import PrintMessageInput

if TYPE_CHECKING:
    from pulse.project.project import Project

# from math import dist
from collections import defaultdict

import gmsh
import numpy as np


def get_data(data):
    return list(np.array(np.round(data, 8), dtype=float))

def normalize(vector):
    return vector / np.linalg.norm(vector)

class GeometryHandler:
    def __init__(self, project: 'Project'):

        self._initialize()

        self.project = project
        self.pipeline = project.pipeline

    def _initialize(self):
        self.length_unit = "meter"
        self.merged_points = list()
        self.points_coords = dict()
        self.points_coords_cache = dict()
        self.lines_mapping = dict()
        self.curve_length = dict()
        self.valve_internal_lines = dict()
        # self.valve_points_to_ignore = dict()

    def set_pipeline(self, pipeline: "Pipeline"):
        self.pipeline = pipeline

    def set_length_unit(self, unit):
        if unit in ["meter", "millimeter", "inch"]:
            self.length_unit = unit

    def get_unit_conversion_function(self, input_unit: str, output_unit: str):
        return lambda x : convert_length_unit(x, input_unit, output_unit)

    def save_valve_internal_lines_if_exists(self, structure: Valve, line_tags: list):
        valve_info: dict = structure.extra_info["valve_info"]
        if ("orifice_plate_thickness" in valve_info.keys()) or ("blocking_length" in valve_info.keys()):
            middle_line_tag = line_tags[len(line_tags) // 2]
            self.valve_internal_lines[middle_line_tag] = structure.tag                      

    def create_geometry(self, gmsh_gui=False):
        # TODO this function is currently overriden by the
        # other with the same name. When it is ready we can
        # remove the other one.

        if gmsh.is_initialized():
            gmsh.finalize()
    
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)

        cad = gmsh.model.occ
        conversion_function = self.get_unit_conversion_function(self.length_unit, "mm")

        for structure in self.pipeline.structures:
            line_tags = structure.add_to_gmsh(cad, conversion_function)

            for tag in line_tags:
                self.lines_mapping[tag] = structure.tag

            if line_tags:
                self.curve_length[structure.tag] = conversion_function(structure.arc_length)

            if isinstance(structure, Valve):
                self.save_valve_internal_lines_if_exists(structure, line_tags)

        # cad.remove_all_duplicates()
        cad.synchronize()

        if gmsh_gui:
            gmsh.option.setNumber('General.FltkColorScheme', 1)
            gmsh.fltk.run()

    def fix_data_for_backwards_compatibility(self, data: dict):
        """
        Older files did not have the structure_name property correctly set,
        and the needed information to create the structure was inferred in 
        a confusing way from multiple parameters.
         
        This function fixes some of the cases to keep old files working.
        """

        sections_list = [
            "Pipe", 
            "Rectangular section", 
            "Circular section", 
            "C-section", 
            "I-section", 
            "T-section", 
            "Generic section",
            "Valve",
            "Expansion joint",
            "Reducer"
            ]

        if data.get("section_type_label") in sections_list:
            type_label: str = data["section_type_label"]
            data["section_type_label"] = type_label.lower().replace(" ", "_").replace("-", "_").replace("section", "beam")

        if data.get("structural_element_type") == "pipe_1" and len(data["section_parameters"]) == 10:
            data["structure_name"] = "reducer"

        if data.get("structural_element_type") == "beam_1" and data.get("structure_name") == "undefined":
            data["structure_name"] = type_label

    def create_structure_from_data(self, data: dict) -> Structure:
        """
        This function compares data["structure_name"] the name of every structure availabe. 
        If it matches the structure is created and returned.
        """

        for structure_type in ALL_STRUCTURE_TYPES:
            if structure_type.name() == data.get("structure_name"):
                return structure_type.load_from_data(data)

        return None

    def process_pipeline(self):
        """ This method builds structures based on model_data file data.
        
        Parameters:
        -----------
        structures_data: dictionary
            
            a dictionary containing all required data to build the pipeline structures.

        Returns
        -------
        pipeline: Pipeline type

            pipeline data to...
        """
        self.pipeline.reset()

        lines_data: dict[str, dict] = self.project.file.read_line_properties_from_file()
        if not isinstance(lines_data, dict):
            return

        structures = list()
        for str_line_id, data in lines_data.items():

            self.fix_data_for_backwards_compatibility(data)
            structure = self.create_structure_from_data(data)
            if structure is None:
                continue
        
            structures.append(structure)

            # Adds common properties to the structure
            structure.tag = int(str_line_id)
            if "material_id" in data.keys():
                structure.extra_info["material_id"] = data["material_id"]

            if "fluid_id" in data.keys():
                structure.extra_info["fluid_id"] = data["fluid_id"]

        if not structures:
            return

        self.pipeline.structures.clear()
        self.pipeline.add_structures(structures)
        self.pipeline.commit()
        self.pipeline.merge_coincident_points()
        if app() is not None:
            app().main_window.update_plots()

    def export_cad_file(self, path):
        self.create_geometry()
        gmsh.write(str(path))
        gmsh.finalize()

    def open_cad_file(self, path: str):

        gmsh.initialize('', False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.option.setNumber('Geometry.Tolerance', 1e-6)
        gmsh.open(str(path))

        # TODO: validate this unit conversion using some cad files
        self.conv_unit = self.get_unit_conversion_function("mm", self.length_unit)

        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)

        self.points_coords = dict()
        for point in points:
            coords = gmsh.model.getValue(*point, [])
            self.points_coords[point[1]] = self.conv_unit(coords)
            # self.points_coords[point[1]] = np.round(self.conv_unit(coords), 5)

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

        structures = list()

        for structure_a in self.process_curved_lines(lines):
            structures.append(structure_a)

        for structure_b in self.process_straight_lines(lines):
            structures.append(structure_b)

        self.pipeline.structures.extend(structures)
        self.pipeline.merge_coincident_points()
        self.export_model_data_file()

        _element_size = self.project.model.preprocessor.mesh.element_size
        element_size = convert_length_unit(_element_size, self.length_unit, "m")

        if self.length_unit !=  "meter":
            self.project.file.modify_project_attributes(length_unit = "meter", element_size = element_size)

        if len(self.merged_points):
            self.print_merged_nodes_message()

        gmsh.finalize()

    def process_curved_lines(self, lines):

        curved_structures = list()

        for line in lines:

            try:

                start_point = gmsh.model.get_adjacencies(*line)[1][0]
                end_point = gmsh.model.get_adjacencies(*line)[1][1]
                line_type = gmsh.model.get_type(*line)

                start_coords = self.get_point_coords(start_point)
                end_coords = self.get_point_coords(end_point)

                start = Point(*start_coords)
                end = Point(*end_coords)

                line_length = np.linalg.norm(start_coords - end_coords)
                
                if line_length < 0.001:
                    self.print_warning_for_small_length(line, line_length)

                if line_type == 'Circle':

                    if len(self.get_point_by_coords(start_coords)) < 2:
                        self.merge_near_points(start_coords)
                        start_coords = self.get_point_coords(start_point)

                    if len(self.get_point_by_coords(end_coords)) < 2:
                        self.merge_near_points(end_coords)
                        end_coords = self.get_point_coords(end_point)

                    Ps = gmsh.model.getValue(0, start_point, [])
                    Pe = gmsh.model.getValue(0, end_point, [])

                    t_start = gmsh.model.getParametrization(1, line[1], Ps)
                    t_end = gmsh.model.getParametrization(1, line[1], Pe)
                    t_middle = (t_start + t_end) / 2

                    P1 = gmsh.model.getValue(1, line[1], t_start)
                    P2 = gmsh.model.getValue(1, line[1], t_middle)
                    P3 = gmsh.model.getValue(1, line[1], t_end)
                    P0 = self.get_center_coordinates_from_3p_circle(P1, P2, P3)
                    center_coords = self.conv_unit(P0)

                    corner_coords = self.get_corner_point_coords(start_point, end_point)
                    # center_coords = self.get_center_point_coords(start_point, end_point)

                    if corner_coords is None:
                        message = f"The connecting lines from 'Circle curve' {line} are parallel "
                        message += "and will be ignored in geometry construction."
                        print(message)
                        continue

                    radius = self.get_radius(corner_coords, start_point, end_point)

                    corner = Point(*corner_coords)
                    pipe = Bend(start, end, corner, radius, center_coords=center_coords)

                    curved_structures.append(pipe)

            except Exception as error_log:

                title = "Error while processing curved structures"
                message = str(error_log)
                message += f"\n\nLine: {line}"
                PrintMessageInput([error_title, title, message])
                
                continue
        
        return curved_structures

    def process_straight_lines(self, lines):

        straight_structures = list()

        for line in lines:

            try:

                start_point = gmsh.model.get_adjacencies(*line)[1][0]
                end_point = gmsh.model.get_adjacencies(*line)[1][1]
                line_type = gmsh.model.get_type(*line)

                start_coords = self.get_point_coords(start_point)
                end_coords = self.get_point_coords(end_point)

                line_length = np.linalg.norm(start_coords - end_coords)
                
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
                PrintMessageInput([error_title, title, message])
                
                continue

        return straight_structures

    def get_center_coordinates_from_3p_circle(self, P1: np.ndarray, P2: np.ndarray, P3: np.ndarray):

        v1 = P2 - P1
        v2 = P3 - P1

        v11 = np.dot(v1, v1)
        v22 = np.dot(v2, v2)
        v12 = np.dot(v1, v2)

        b = (1/(2*(v11*v22 - v12**2)))

        k1 = b * v22*(v11 - v12)
        k2 = b * v11*(v22 - v12)

        P0 = P1 + k1*v1 + k2*v2

        return P0

    def map_points_according_to_coordinates(self):
        """ This method maps points according to its nodal coordinates.
        """
        self.points_map  = defaultdict(list)
        for index, coords in self.points_coords.items():
            # key = str(list(coords))
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
        except Exception:
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

        coords_start = self.conv_unit(gmsh.model.getValue(0, start_point, []))
        coords_end = self.conv_unit(gmsh.model.getValue(0, end_point, []))

        _, points_Lstart = self.get_connecting_line_data(coords_start, start_point)
        _, points_Lend = self.get_connecting_line_data(coords_end, end_point)

        X1 = self.conv_unit(gmsh.model.getValue(0, points_Lstart[0], []))
        X2 = self.conv_unit(gmsh.model.getValue(0, points_Lstart[1], []))

        X3 = self.conv_unit(gmsh.model.getValue(0, points_Lend[0], []))
        X4 = self.conv_unit(gmsh.model.getValue(0, points_Lend[1], []))

        a = X2 - X1
        b = X4 - X3
        c = X3 - X1

        cross_ab = np.cross(a, b)
        cross_cb = np.cross(c, b)

        if np.round(np.linalg.norm(cross_ab), 8) != 0:
            s = np.dot(cross_cb, cross_ab)/(((np.linalg.norm(cross_ab)))**2)
            Xc = X1 + a*s
            return np.round(Xc, 10)
        else:
            return None

    def get_center_point_coords(self, start_point, end_point):
        """
            This method returns the arc circle center coordinates.
        """

        coords_start = self.conv_unit(gmsh.model.getValue(0, start_point, []))
        coords_end = self.conv_unit(gmsh.model.getValue(0, end_point, []))

        _, points_Lstart = self.get_connecting_line_data(coords_start, start_point)
        _, points_Lend = self.get_connecting_line_data(coords_end, end_point)

        X1 = self.conv_unit(gmsh.model.getValue(0, points_Lstart[0], []))
        X2 = self.conv_unit(gmsh.model.getValue(0, points_Lstart[1], []))

        X3 = self.conv_unit(gmsh.model.getValue(0, points_Lend[0], []))
        X4 = self.conv_unit(gmsh.model.getValue(0, points_Lend[1], []))

        u = X2 - X1
        v = X4 - X3
        n = np.cross(u, v)
        
        u /= np.linalg.norm(u)
        v /= np.linalg.norm(v)
        n /= np.linalg.norm(n)

        A = np.array([[u[0], u[1], u[2]],
                      [v[0], v[1], v[2]],
                      [n[0], n[1], n[2]]], dtype=float)

        b = np.array([  np.sum(u*coords_start), 
                        np.sum(v*coords_end),
                        np.sum(n*coords_start)], dtype=float)

        center_coordinates = np.linalg.solve(A, b)
        # print(f"Center coordinates (gmsh): {center_coordinates}[m]")
        return center_coordinates

    def get_radius(self, corner_coords, start_point, end_point):
        """
        """
        start_coords = self.conv_unit(gmsh.model.getValue(0, start_point, []))
        end_coords = self.conv_unit(gmsh.model.getValue(0, end_point, []))

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        cos_2x = (np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector))
        cos_x = np.sqrt((1 + cos_2x) / 2)
        corner_distance = norm_a_vector / cos_x

        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)
        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = np.linalg.norm(center_coords - start_coords)
        end_curve_radius = np.linalg.norm(center_coords - end_coords)
        radius = (start_curve_radius + end_curve_radius) / 2

        return np.round(radius, 8)

    def print_warning_for_small_length(self, line, line_length):

        title = "Small line length detected"
        message = f"The line {line} has a small length which may cause problems "
        message += "in model processing. We reccomend to check the imported geometry "
        message += "to avoid physical inconsistency in model results."
        message += f"\n\nLine length: {round(line_length, 6)} [m]"
        
        PrintMessageInput([warning_title, title, message])

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

    def print_merged_nodes_message(self):

        title = "Points merging detected"
        message = f"The points {self.merged_points} were merged in geometry processing.\n\n"

        for point in self.merged_points:
            message += f"{point} : {self.points_coords_cache[point]}\n"

        PrintMessageInput([warning_title, title, message])

    def get_structures_tags(self):
        tags = list()
        for structure in self.pipeline.structures:
            if structure.tag != -1:
                tags.append(structure.tag)
        return tags

    def export_model_data_file(self):

        section_info = dict()
        structures_data = dict()

        fluid_map = defaultdict(list)
        material_map = defaultdict(list)
        element_type_info = defaultdict(list)

        psd_info = dict()
        pulsation_damper_info = dict()
        valve_info = dict()
        expansion_joint_info = dict()

        tags = self.get_structures_tags()

        for structure in self.pipeline.structures:

            if isinstance(structure, Bend) and structure.is_colapsed():               
                continue

            pipeline_data = self.get_pipeline_data(structure)

            if not pipeline_data:
                continue

            tag = structure.tag
            if tag == -1:
                tag = 1
                while tag in tags:
                    tag += 1

            if tag not in tags: 
                tags.append(tag)

            structures_data[tag] = pipeline_data

            if "cross_section_info" in structure.extra_info.keys():
                section_info[tag] = structure.extra_info["cross_section_info"]
            else:
                section_info[tag] = self.get_dummy_pipe_section_info()

            fluid_id = structure.extra_info.get("fluid_id")
            if isinstance(fluid_id, int):
                fluid_map[fluid_id].append(tag)

            material_id = structure.extra_info.get("material_id")
            if isinstance(material_id, int):
                material_map[material_id].append(tag)

            if "structural_element_type" in structure.extra_info.keys():
                if structure.extra_info["structural_element_type"] is not None:
                    structural_element_type = structure.extra_info["structural_element_type"]
                    element_type_info[structural_element_type].append(tag)

            if "expansion_joint_info" in structure.extra_info.keys():
                expansion_joint_info[tag] = structure.extra_info["expansion_joint_info"]

            if "valve_info" in structure.extra_info.keys():
                valve_info[tag] = structure.extra_info["valve_info"]

            if "psd_label" in structure.extra_info.keys():
                psd_info[tag] = structure.extra_info["psd_label"]
            
            if "pulsation_damper_label" in structure.extra_info.keys():
                pulsation_damper_info[tag] = structure.extra_info["pulsation_damper_label"]

            tag += 1

        # reset all model properties before reload the structures data
        self.project.model.properties._reset_variables()

        if not structures_data:
            return
        
        # self.remove_lines(structures_data)
        for line_id, structure_data in structures_data.items():
            structure_data: dict
            for key, values in structure_data.items():
                self.project.model.properties._set_line_property(key, values, line_ids=line_id)

        for line_id, cross_data in section_info.items():
            self.project.model.properties._set_multiple_line_properties(cross_data, line_ids=line_id)

        for element_type, line_ids in element_type_info.items():
            self.project.model.properties._set_line_property("structural_element_type", element_type, line_ids=line_ids)

        for material_id, line_ids in material_map.items():
            self.project.model.properties._set_line_property("material_id", material_id, line_ids=line_ids)

        for fluid_id, line_ids in fluid_map.items():
            self.project.model.properties._set_line_property("fluid_id", fluid_id, line_ids=line_ids)

        for line_id, ej_data in expansion_joint_info.items():
            self.project.model.properties._set_line_property("expansion_joint_info", ej_data, line_ids=line_id)

        for line_id, valve_data in valve_info.items():
            self.project.model.properties._set_line_property("valve_info", valve_data, line_ids=line_id)

        for line_id, psd_label in psd_info.items():
            self.project.model.properties._set_line_property("psd_label", psd_label, line_ids=line_id)
                
        for line_id, damper_label in pulsation_damper_info.items():
            self.project.model.properties._set_line_property("pulsation_damper_label", damper_label, line_ids=line_id)


        self.project.file.write_line_properties_in_file()
        self.project.file.modify_project_attributes(import_type = 1)

    def get_pipeline_data(self, structure):

        data = dict()
        # data["structure name"] = structure.name

        if isinstance(structure, Fillet):
            data["structure_name"] = structure.name()
            data["start_coords"] = get_data(structure.start.coords())
            data["end_coords"] = get_data(structure.end.coords())

            if structure.center_coords is None:
                data["center_coords"] = get_data(structure.center.coords())
            else:
                data["center_coords"] = get_data(structure.center_coords)

            data["corner_coords"] = get_data(structure.corner.coords())
            data["curvature_radius"] = np.round(structure.curvature_radius, 8)

        elif isinstance(structure, Pipe | Beam | Reducer | Flange | Valve | ExpansionJoint):
            data["structure_name"] = structure.name()
            data["start_coords"] = get_data(structure.start.coords())
            data["end_coords"] = get_data(structure.end.coords())
        
        elif isinstance(structure, Arc):
            data["structure_name"] = structure.name()
            data["start_coords"] = get_data(structure.start.coords())
            data["end_coords"] = get_data(structure.end.coords())
            data["mid_coords"] = get_data(structure.mid.coords())

        return data

    def get_dummy_pipe_section_info(self):
        section_info = dict()
        section_info["section_type_label"] = "pipe"
        section_info["section_parameters"] = [0.01, 0.001, 0, 0, 0 ,0]
        return section_info

def get_arc_length(coords_A, coords_B, coords_C):

    u = coords_A - coords_C
    v = coords_B - coords_C

    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_alpha = np.dot(u, v) / (norm_u * norm_v)

    average_radius = (norm_u + norm_v) / 2
    arc_length = np.arccos(cos_alpha) * average_radius

    return arc_length