import gmsh
import math
import numpy as np
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model import Point
from opps.model.pipeline_editor import PipelineEditor


class StepHandler:
    def __init__(self):
        pass

    def save(self, path, editor):
        gmsh.initialize("", False)
        for structure in editor.pipeline.structures: 

            if isinstance(structure, Pipe):
                start_coords = gmsh.model.occ.add_point(*structure.start.coords())
                end_coords = gmsh.model.occ.add_point(*structure.end.coords())

                gmsh.model.occ.add_line(start_coords, end_coords)

            elif isinstance(structure, Bend):
                if (structure.start.coords() == structure.end.coords()).all():
                    continue
                start_coords = gmsh.model.occ.add_point(*structure.start.coords())
                end_coords = gmsh.model.occ.add_point(*structure.end.coords())
                center_point = gmsh.model.occ.add_point(*structure.center.coords())

                gmsh.model.occ.add_circle_arc(start_coords, center_point, end_coords)

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
            start_coords = gmsh.model.get_adjacencies(*line)[1][0]
            end_coords = gmsh.model.get_adjacencies(*line)[1][1]
            line_type = gmsh.model.get_type(*line)

            start_coords = (points_coords[start_coords -1][1])
            end_coords = (points_coords[end_coords -1][1])

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