import gmsh
import math
import numpy as np
import configparser
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model import Point
from opps.model.pipeline_editor import PipelineEditor
from OpenPulse.pulse.interface.handler.geometry_handler import GeometryHandler



class StepHandler:
    def __init__(self):
        pass

    def save(self, path, editor):
        gmsh.initialize("", False)
        for structure in editor.pipeline.structures: 

            if isinstance(structure, Pipe):
                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(structure, Bend):
                if (structure.start.coords() == structure.end.coords()).all():
                    continue
                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())
                center_point = gmsh.model.occ.add_point(*structure.center.coords())

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))

    def normalize(vector):
        return vector / np.linalg.norm(vector)

    
    def open(self, path, editor):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(str(path))

        structures = [] 
        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)
        
        points_coords = []
        for point in points: 
            coords = gmsh.model.getValue(*point, [])
            points_coords.append((point[1], (coords)))

        associated_points = []
        for line in lines:
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][0])
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][1])

        center_points = []
        for point in points:
            if point[1] not in associated_points:
                center_points.append(point[1])

        for line in lines: 
            start_point = gmsh.model.get_adjacencies(*line)[1][0]
            end_point = gmsh.model.get_adjacencies(*line)[1][1]
            line_type = gmsh.model.get_type(*line)

            start_coords = (points_coords[start_point -1][1])
            end_coords = (points_coords[end_point -1][1])

            start = Point(*start_coords)
            end = Point(*end_coords)

            if line_type == 'Line':
                pipe = Pipe(start, end)

            elif line_type == 'Circle':
                for point in center_points:
                    start_radius = math.dist(start_coords, points_coords[point-1][1]) # the second argument is the coords of the tested center point
                    end_radius = math.dist(end_coords, points_coords[point-1][1])
                    
                    if abs(start_radius - end_radius) <= 1e-10:
                        start_radius_center = start_radius
                        end_radius_center = end_radius
                        center_point = point

                center_coords = np.array(points_coords[center_point - 1][1])
                start_coords = np.array(start_coords)
                end_coords = np.array(end_coords)

                a_vector = start_coords - center_coords
                b_vector = end_coords - center_coords
                a_vector_normalized = a_vector / np.linalg.norm(a_vector)
                b_vector_normalized = b_vector / np.linalg.norm(b_vector)
                c_vector = a_vector_normalized + b_vector_normalized
                c_vector_normalized = c_vector / np.linalg.norm(c_vector)

                radius = (start_radius_center + end_radius_center) / 2
                corner_distance = (radius**2)*np.sqrt(2 / (np.dot(a_vector, b_vector) + radius**2))
                corner_coords = center_coords + c_vector_normalized * corner_distance

                corner = Point(*corner_coords)
                pipe = Bend(start, end, corner, radius)

            structures.append(pipe)

        editor.pipeline.structures = structures
        editor.merge_coincident_points()

    def write_dat_file(self, path):
        gmsh.initialize()
        # path = "C:\\meus_arquivos\\ufsc\\LVA\\geometry_files\\teste25.step"
        gmsh.open(path)

        gmsh.model.occ.removeAllDuplicates()
        gmsh.model.occ.synchronize()

        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)

        lines_tags = []
        for line in lines:
            lines_tags.append(line[1])

        points_tags_and_coords = dict()
        for point in points: 
            coords = gmsh.model.getValue(*point, [])
            points_tags_and_coords[point[1]] = list(coords)

        config = configparser.ConfigParser()
        for line in lines_tags: 
            start_point = gmsh.model.get_adjacencies(1, line)[1][0]
            end_point = gmsh.model.get_adjacencies(1, line)[1][1]
            line_type = gmsh.model.get_type(1, line)

            start_point_coords = points_tags_and_coords[start_point]
            end_point_coords = points_tags_and_coords[end_point]

            config[str(line)] = {}
            config[str(line)]['start point'] = str(list(np.round(start_point_coords, 8)))
            config[str(line)]['end point'] = str(list(np.round(end_point_coords, 8)))

            # if line_type == "Circle":
            #     # get_corner_point_coords(self, start_point, end_point)

        with open("entity.dat", 'w') as config_file:
                config.write(config_file)
