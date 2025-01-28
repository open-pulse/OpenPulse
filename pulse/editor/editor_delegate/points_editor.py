import numpy as np

from pulse.editor.structures import Bend, Point

from .editor import Editor


class PointsEditor(Editor):
    def attatch_point(self, point: Point):
        replaced_points = []

        for structure in self.pipeline.structures:
            for p in structure.get_points():
                if id(p) == id(point):
                    continue

                if np.allclose(p.coords(), point.coords()):
                    structure.replace_point(p, point)
                    replaced_points.append(p)

        for point in replaced_points:
            for i in self.pipeline.get_point_indexes(point):
                self.pipeline.points.pop(i)

    def dettatch_point(self, point: Point):
        detatched = []
        first_point = True
        for structure in self.pipeline.all_structures():
            if point not in structure.get_points():
                continue

            # we still want to keep the current point in the
            # pipeline so we only replace the next ones.
            if first_point:
                first_point = False
                continue

            new_point = point.copy()
            detatched.append(new_point)
            structure.replace_point(point, new_point)

        self.pipeline.add_points(detatched)
        return detatched

    def move_point(self, point: Point, new_position: tuple[float, float, float]):
        point.set_coords(*new_position)
        self.pipeline.recalculate_curvatures()

    def merge_coincident_points(self):
        found_points = dict()
        for structure in self.pipeline.structures:
            for point in structure.get_points():
                x, y, z = np.round(point.coords(), 6)
                if (x, y, z) in found_points:
                    new = found_points[x, y, z]
                    structure.replace_point(point, new)
                else:
                    found_points[x, y, z] = point

        self.pipeline.points.clear()
        for structure in self.pipeline.structures:
            for point in structure.get_points():
                if point not in self.pipeline.points:
                    self.pipeline.points.append(point)
