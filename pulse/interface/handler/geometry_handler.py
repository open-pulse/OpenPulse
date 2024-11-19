# fmt: off
from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

from pulse.editor.structures import (
    Pipe,
    Bend,
    Point,
    Flange,
    Valve,
    Beam,
    Reducer,
    RectangularBeam,
    CircularBeam,
    IBeam,
    TBeam,
    CBeam,
    ExpansionJoint,
    SimpleCurve,
)

import gmsh
import numpy as np

# from math import dist
from collections import defaultdict


window_title_1 = "Error"
window_title_2 = "Warning"


def get_data(data):
    return list(np.array(np.round(data, 8), dtype=float))

def normalize(vector):
    return vector / np.linalg.norm(vector)

class GeometryHandler:
    def __init__(self):
        self.project = app().project
        self._initialize()

    def _initialize(self):
        self.length_unit = "meter"
        self.merged_points = list()
        self.points_coords = dict()
        self.points_coords_cache = dict()
        self.lines_mapping = dict()
        self.curve_length = dict()
        self.valve_internal_lines = dict()
        # self.valve_points_to_ignore = dict()
        self.pipeline = self.project.pipeline

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def set_length_unit(self, unit):
        if unit in ["meter", "millimeter", "inch"]:
            self.length_unit = unit

    def create_geometry(self, gmsh_GUI=False):

        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal",0)
        gmsh.option.setNumber("General.Verbosity", 0)

        for structure in self.pipeline.structures:

            if isinstance(structure, (Pipe, Beam, Reducer, Flange, ExpansionJoint)):

                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()

                if self.length_unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)

                elif self.length_unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)

                else:
                    start_coords = _start_coords
                    end_coords = _end_coords

                start_point = gmsh.model.occ.addPoint(*start_coords)
                end_point = gmsh.model.occ.addPoint(*end_coords)
                line_tag = gmsh.model.occ.addLine(start_point, end_point)

                self.lines_mapping[line_tag] = structure.tag
                self.curve_length[structure.tag] = np.linalg.norm(end_coords-start_coords)

            elif isinstance(structure, Valve):

                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()

                if self.length_unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)

                elif self.length_unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)

                else:
                    start_coords = _start_coords
                    end_coords = _end_coords

                valve_info = structure.extra_info["valve_info"]
                valve_points = self.process_valve_points(start_coords, end_coords, valve_info)

                lc = 0
                if "external_points" in valve_points.keys():
                    (coords_A, coords_B) = valve_points["external_points"]
                    point_A = gmsh.model.occ.addPoint(*coords_A, meshSize=lc)
                    point_B = gmsh.model.occ.addPoint(*coords_B, meshSize=lc)
                    self.curve_length[structure.tag] = np.linalg.norm(coords_B - coords_A)

                if "flange_points" in valve_points.keys():
                    (coords_C, coords_D) = valve_points["flange_points"]
                    point_C = gmsh.model.occ.addPoint(*coords_C, meshSize=lc)
                    point_D = gmsh.model.occ.addPoint(*coords_D, meshSize=lc)

                if "internal_points" in valve_points.keys():
                    (coords_E, coords_F) = valve_points["internal_points"]
                    point_E = gmsh.model.occ.addPoint(*coords_E, meshSize=lc)
                    point_F = gmsh.model.occ.addPoint(*coords_F, meshSize=lc)

                # line_tag = gmsh.model.occ.addLine(point_A, point_B)
                # self.lines_mapping[line_tag] = structure.tag

                lines = list()
                if "flange_points" in valve_points.keys():
                    if "internal_points" in valve_points.keys():
                        lines.append(gmsh.model.occ.addLine(point_A, point_C))
                        lines.append(gmsh.model.occ.addLine(point_C, point_E))
                        lines.append(gmsh.model.occ.addLine(point_E, point_F))
                        lines.append(gmsh.model.occ.addLine(point_F, point_D))
                        lines.append(gmsh.model.occ.addLine(point_D, point_B))

                        if "blocking_length" in valve_info.keys():
                            self.valve_internal_lines[lines[2]] = structure.tag
                        # self.valve_points_to_ignore[structure.tag] = (point_C, point_D, point_E, point_F)

                    else:
                        lines.append(gmsh.model.occ.addLine(point_A, point_C))
                        lines.append(gmsh.model.occ.addLine(point_C, point_D))
                        lines.append(gmsh.model.occ.addLine(point_D, point_B))
                        # self.valve_points_to_ignore[structure.tag] = (point_C, point_D)

                elif "internal_points" in valve_points.keys():
                    lines.append(gmsh.model.occ.addLine(point_A, point_E))
                    lines.append(gmsh.model.occ.addLine(point_E, point_F))
                    lines.append(gmsh.model.occ.addLine(point_F, point_B))

                    if "blocking_length" in valve_info.keys():
                        self.valve_internal_lines[lines[1]] = structure.tag
                    # self.valve_points_to_ignore[structure.tag] = (point_E, point_F)

                else:
                    lines.append(gmsh.model.occ.addLine(point_A, point_B))

                for line_tag in lines:
                    self.lines_mapping[line_tag] = structure.tag

            elif isinstance(structure, SimpleCurve):

                if structure.is_colapsed():
                    continue

                _start_coords = structure.start.coords()
                _end_coords = structure.end.coords()
                _center_coords = structure.center_coords

                # TODO: remove OPPS internal calculation as soos as possible
                # _center_coords2 = structure.center.coords()

                # print(f"Center coordinates (external): {_center_coords} [m]")
                # print(f"Center coordinates (internal): {_center_coords2} [m]")

                if self.length_unit == "meter":
                    start_coords = m_to_mm(_start_coords)
                    end_coords = m_to_mm(_end_coords)
                    center_coords = m_to_mm(_center_coords)
                
                elif self.length_unit == "inch":
                    start_coords = in_to_mm(_start_coords)
                    end_coords = in_to_mm(_end_coords)
                    center_coords = in_to_mm(_center_coords)

                else:
                    start_coords = _start_coords
                    end_coords = _end_coords
                    center_coords = _center_coords

                start_radius = np.linalg.norm(start_coords-center_coords)
                end_radius = np.linalg.norm(end_coords-center_coords)

                if abs(start_radius-end_radius) > 1e-12:

                    center_coords, shift_value = self.get_corrected_arc_center_coordinates(start_coords, 
                                                                                           end_coords, 
                                                                                           center_coords)

                    print("The arc center point was shifted by {:.6e} [mm]".format(shift_value))

                start_point = gmsh.model.occ.addPoint(*start_coords)
                end_point = gmsh.model.occ.addPoint(*end_coords)
                center_point = gmsh.model.occ.addPoint(*center_coords)

                line_tag = gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

                self.lines_mapping[line_tag] = structure.tag
                self.curve_length[structure.tag] = get_arc_length(start_coords, end_coords, center_coords)

        gmsh.model.occ.synchronize()

        if gmsh_GUI:
            import sys
            if '-nopopup' not in sys.argv:
                gmsh.option.setNumber('General.FltkColorScheme', 1)
                gmsh.fltk.run()
    
    def get_corrected_arc_center_coordinates(self, start_coords: np.ndarray, end_coords: np.ndarray, center_coords: np.ndarray):
        """ 
            This method returns precise arc center coordinates to avoid floating
            precision errors while decoding geometry data from imported CAD files.
        """
        middle_coords = (start_coords + end_coords) / 2
        normal_vector = np.cross(end_coords - start_coords, center_coords - start_coords)
        bisector_direction = np.cross(normal_vector, end_coords - start_coords)
        # bisector_direction = np.cross(end - start, normal_vector)

        u = center_coords - middle_coords
        v = bisector_direction
        projection_uv = (np.dot(u, v) / (np.linalg.norm(v)**2)) * v

        corrected_center_coords = middle_coords + projection_uv
        correction_length = np.linalg.norm(corrected_center_coords - center_coords)

        return corrected_center_coords, correction_length

    def process_valve_points(self, start_coords: np.ndarray, end_coords: np.ndarray, valve_info: dict) -> dict:
        """
        """

        valve_points = dict()

        A = start_coords
        B = end_coords
        AB = B - A

        L = np.linalg.norm(AB)
        n = AB / L

        valve_points["external_points"] = (A, B)

        if "flange_length" in valve_info.keys():
            flange_length = 1e3 * valve_info["flange_length"]
            C = A + n * flange_length
            D = A + n * (L - flange_length)
            valve_points["flange_points"] = (C, D)

        if "orifice_plate_thickness" in valve_info.keys():
            internal_length = 1e3 * valve_info["orifice_plate_thickness"]
            E = A + n * (L - internal_length) / 2
            F = A + n * (L + internal_length) / 2
            valve_points["internal_points"] = (E, F)

        elif "blocking_length" in valve_info.keys():
            internal_length = 1e3 * valve_info["blocking_length"]
            E = A + n * (L - internal_length) / 2
            F = A + n * (L + internal_length) / 2
            valve_points["internal_points"] = (E, F)

        return valve_points

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

        structures = list()
        self.pipeline.reset()

        lines_data = app().pulse_file.read_line_properties_from_file()

        if isinstance(lines_data, dict):
            for _line_id, data in lines_data.items():

                data : dict
                line_id = int(_line_id)

                structural_element_type = data.get("structural_element_type", None)
                structure = None

                if structural_element_type in ["pipe_1", None]:
                    structure = self._process_pipe(line_id, data)

                elif structural_element_type == "beam_1":
                    structure = self._process_beam(line_id, data)

                elif structural_element_type == "valve":
                    structure = self._process_valve(line_id, data)

                elif structural_element_type == "expansion_joint":
                    structure = self._process_expansion_joint(line_id, data)

                if "material_id" in data.keys():
                    structure.extra_info["material_info"] = data['material_id']

                if structure is not None:
                    structures.append(structure)

        self.pipeline.structures.clear()
        if len(structures):
            self.pipeline.add_structures(structures)
            self.pipeline.commit()
            self.pipeline.merge_coincident_points()
            app().main_window.update_plots()

    def _process_pipe(self, line_id: int, data: dict):

        if "section_parameters" in data.keys():
            section_parameters = data["section_parameters"]
        else:
            section_parameters = [0.01, 0.001, 0, 0, 0 ,0]

        if "section_type_label" in data.keys():
            section_type_label = data["section_type_label"]
        else:
            section_type_label = "Pipe"

        if len(section_parameters) == 6:

            if data["structure_name"] == "pipe":
                start = Point(*data['start_coords'])
                end = Point(*data['end_coords'])
                structure = Pipe(
                                 start, 
                                 end, 
                                 diameter = section_parameters[0],
                                 thickness = section_parameters[1],
                                )

            elif data["structure_name"] == "bend":

                start = Point(*data['start_coords'])
                end = Point(*data['end_coords'])
                corner = Point(*data['corner_coords'])
                curvature_radius = data['curvature_radius']
                center_coords = data.get('center_coords')

                structure = Bend(
                                 start, 
                                 end, 
                                 corner, 
                                 curvature_radius,
                                 center_coords = center_coords, 
                                 diameter = section_parameters[0],
                                 thickness = section_parameters[1]
                                )

                if center_coords is None:
                    structure.center_coords = structure.center.coords()

            elif data["structure_name"] == "flange":
                start = Point(*data['start_coords'])
                end = Point(*data['end_coords'])
                structure = Flange(
                                   start, 
                                   end, 
                                   diameter = section_parameters[0],
                                   thickness = section_parameters[1],
                                   )

        elif len(section_parameters) == 10:

            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = Reducer(
                                start, 
                                end, 
                                initial_diameter = section_parameters[0],
                                final_diameter = section_parameters[4],
                                thickness = section_parameters[1],
                                initial_offset_y = section_parameters[2],
                                initial_offset_z = section_parameters[3],
                                final_offset_y = section_parameters[6],
                                final_offset_z = section_parameters[7],
                                )

        else:
            return

        structure.tag = line_id

        section_info = {
                        "section_type_label" : section_type_label,
                        "section_parameters" : section_parameters
                       }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "pipe_1"
        
        if "psd_name" in data.keys():
            structure.extra_info["psd_name"] = data["psd_name"]

        return structure

    def _process_beam(self, line_id: int, data: dict):

        if "section_parameters" not in data.keys():
            return

        section_type_label = data.get("section_type_label", None)
        section_parameters = data["section_parameters"]

        if section_type_label == "Rectangular section":
            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = RectangularBeam(
                                        start, 
                                        end,
                                        width = section_parameters[0],
                                        height = section_parameters[1],
                                        thickness_width = (section_parameters[0] - section_parameters[2]) / 2,
                                        thickness_height = (section_parameters[0] - section_parameters[3]) / 2,
                                        )
        
        elif section_type_label == "Circular section":
            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = CircularBeam(
                                     start, 
                                     end, 
                                     diameter = section_parameters[0],
                                     thickness = section_parameters[1],
                                    )

        elif section_type_label == "C-section":
            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = CBeam(
                              start, 
                              end, 
                              height = section_parameters[0],
                              width_1 = section_parameters[1],
                              width_2 = section_parameters[3],
                              thickness_1 = section_parameters[2],
                              thickness_2 = section_parameters[4],
                              thickness_3 = section_parameters[5],
                              )
    
        elif section_type_label == "I-section":
            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = IBeam(
                              start, 
                              end, 
                              height = section_parameters[0],
                              width_1 = section_parameters[1],
                              width_2 = section_parameters[3],
                              thickness_1 = section_parameters[2],
                              thickness_2 = section_parameters[4],
                              thickness_3 = section_parameters[5],
                              )
                        
        elif section_type_label == "T-section":
            start = Point(*data['start_coords'])
            end = Point(*data['end_coords'])
            structure = TBeam(
                              start, 
                              end, 
                              height = section_parameters[0],
                              width = section_parameters[1],
                              thickness_1 = section_parameters[2],
                              thickness_2 = section_parameters[3],
                              )

        else:
            return

        structure.tag = line_id

        section_properties = data["section_properties"]
        section_info = {
                        "section_type_label" : section_type_label,
                        "section_parameters" : section_parameters,
                        "section_properties" : section_properties
                        }

        structure.extra_info["cross_section_info"] = section_info
        structure.extra_info["structural_element_type"] = "beam_1"

        return structure

    def _process_valve(self, line_id: int, data: dict):

        start = Point(*data['start_coords'])
        end = Point(*data['end_coords'])

        valve_info = data["valve_info"]
        d_out, t, *_ = valve_info["body_section_parameters"]
        flange_outer_diameter, *_ = valve_info["flange_section_parameters"]
        flange_length = valve_info["flange_length"]

        structure = Valve(
            start, 
            end,
            diameter = d_out,
            thickness = t,
            flange_outer_diameter = flange_outer_diameter,
            flange_length = flange_length,                          
        )

        structure.tag = line_id

        section_info = {"section_type_label" : "Valve"}
        structure.extra_info["cross_section_info"] = section_info

        structure.extra_info["valve_info"] = valve_info
        structure.extra_info["structural_element_type"] = "valve"

        return structure

    def _process_expansion_joint(self, line_id: int, data: dict):

        start = Point(*data['start_coords'])
        end = Point(*data['end_coords'])

        expansion_joint_info = data["expansion_joint_info"]
        diameter  = expansion_joint_info["effective_diameter"]

        structure = ExpansionJoint(
                                   start, 
                                   end,
                                   diameter = diameter,
                                   thickness = 0.05*diameter
                                   )

        structure.tag = line_id

        section_info = {"section_type_label" : "Expansion joint"}
        structure.extra_info["cross_section_info"] = section_info

        structure.extra_info["expansion_joint_info"] = expansion_joint_info
        structure.extra_info["structural_element_type"] = "expansion_joint"

        return structure

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

        if self.length_unit == "meter":
            self.conv_unit = mm_to_m
        elif self.length_unit == "millimeter":
            self.conv_unit = um_to_m
        else:
            self.conv_unit = in_to_mm

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

        element_size = app().project.preprocessor.mesh.element_size
        if self.length_unit == "millimeter":
            element_size = mm_to_m(element_size)

        if self.length_unit == "inch":
            element_size = in_to_m(element_size)

        if self.length_unit !=  "meter":
            app().pulse_file.modify_project_attributes(length_unit = "meter", element_size = element_size)
            app().main_window.mesh_toolbar.update_mesh_attributes()

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
                PrintMessageInput([window_title_1, title, message])
                
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
                PrintMessageInput([window_title_1, title, message])
                
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

    def print_merged_nodes_message(self):

        title = "Points merging detected"
        message = f"The points {self.merged_points} were merged in geometry processing.\n\n"

        for point in self.merged_points:
            message += f"{point} : {self.points_coords_cache[point]}\n"

        PrintMessageInput([window_title_2, title, message])

    def get_structures_tags(self):
        tags = list()
        for structure in self.pipeline.structures:
            if structure.tag != -1:
                tags.append(structure.tag)
        return tags

    def export_model_data_file(self):

        structures_data = dict()
        section_info = dict()

        element_type_info = defaultdict(list)
        material_info = defaultdict(list)

        psd_info = dict()
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

            if "material_info" in structure.extra_info.keys():
                material_id = structure.extra_info["material_info"]
                material_info[material_id].append(tag)

            if "structural_element_type" in structure.extra_info.keys():
                if structure.extra_info["structural_element_type"] is not None:
                    structural_element_type = structure.extra_info["structural_element_type"]
                    element_type_info[structural_element_type].append(tag)

            if "expansion_joint_info" in structure.extra_info.keys():
                expansion_joint_info[tag] = structure.extra_info["expansion_joint_info"]

            if "valve_info" in structure.extra_info.keys():
                valve_info[tag] = structure.extra_info["valve_info"]

            if "psd_name" in structure.extra_info.keys():
                psd_info[tag] = structure.extra_info["psd_name"]

            tag += 1

        if structures_data:

            # self.remove_lines(structures_data)
            for line_id, structure_data in structures_data.items():
                structure_data: dict
                for key, values in structure_data.items():
                    app().project.model.properties._set_line_property(key, values, line_ids=line_id)

            for line_id, cross_data in section_info.items():
                app().project.model.properties._set_multiple_line_properties(cross_data, line_ids=line_id)

            for element_type, line_ids in element_type_info.items():
                app().project.model.properties._set_line_property("structural_element_type", element_type, line_ids=line_ids)

            for material_id, line_ids in material_info.items():
                app().project.model.properties._set_line_property("material_id", material_id, line_ids=line_ids)

            for line_id, ej_data in expansion_joint_info.items():
                app().project.model.properties._set_line_property("expansion_joint_info", ej_data, line_ids=line_id)

            for line_id, valve_data in valve_info.items():
                app().project.model.properties._set_line_property("valve_info", valve_data, line_ids=line_id)

            for line_id, psd_label in psd_info.items():
                app().project.model.properties._set_line_property("psd_name", psd_label, line_ids=line_id)

            app().pulse_file.write_line_properties_in_file()
            app().pulse_file.modify_project_attributes(import_type = 1)

    def get_pipeline_data(self, structure):

        data = dict()
        # data["structure name"] = structure.name

        if isinstance(structure, Bend):
            data["structure_name"] = self.get_structure_name(structure)
            data["start_coords"] = get_data(structure.start.coords())
            data["end_coords"] = get_data(structure.end.coords())
            # print("-> ", structure.center_coords)

            if structure.center_coords is None:
                data["center_coords"] = get_data(structure.center.coords())
            else:
                data["center_coords"] = get_data(structure.center_coords)

            data["corner_coords"] = get_data(structure.corner.coords())
            data["curvature_radius"] = np.round(structure.curvature_radius, 8)

        elif isinstance(structure, Pipe | Beam | Reducer | Flange | Valve | ExpansionJoint):
            data["structure_name"] = self.get_structure_name(structure)
            data["start_coords"] = get_data(structure.start.coords())
            data["end_coords"] = get_data(structure.end.coords())

        return data

    def get_structure_name(self, structure):

        # temporary solution, replace for structure.name

        if isinstance(structure, Pipe):
            return "pipe"
        elif isinstance(structure, Bend):
            return "bend"
        elif isinstance(structure, Flange):
            return "flange"
        elif isinstance(structure, Reducer):
            return "reducer"
        elif isinstance(structure, ExpansionJoint):
            return "expansion joint"
        elif isinstance(structure, Valve):
            return "valve"
        else:
            return "undefined"

    def get_dummy_pipe_section_info(self):
        section_info = dict()
        section_info["section_type_label"] = "Pipe"
        section_info["section_parameters"] = [0.01, 0.001, 0, 0, 0 ,0]
        return section_info

    # def remove_lines(self, structures_data: dict):
    #     """ This method removes the lines properties associated with the
    #         removed structures.
    #     """
    #     lines_to_remove = list()
    #     for line_id in app().project.model.properties.line_properties.keys():
    #         if line_id not in structures_data.keys():
    #             lines_to_remove.append(line_id)
        
    #     for line_id in lines_to_remove:
    #         app().project.model.properties._remove_line(line_id)

def get_arc_length(coords_A, coords_B, coords_C):

    u = coords_A - coords_C
    v = coords_B - coords_C

    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_alpha = np.dot(u, v) / (norm_u * norm_v)

    average_radius = (norm_u + norm_v) / 2
    arc_length = np.arccos(cos_alpha) * average_radius

    return arc_length

# fmt: on
