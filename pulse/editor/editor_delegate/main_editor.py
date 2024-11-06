import numpy as np
from typing import TypeVar

from pulse.editor.structures import (
    Bend,
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Flange,
    IBeam,
    Pipe,
    Point,
    RectangularBeam,
    Reducer,
    Structure,
    TBeam,
    Valve,
    LinearStructure,
    Fillet,
    Arc,
)

from .editor import Editor


t_structure = TypeVar("t_structure", bound=type[Structure])


class MainEditor(Editor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.next_border = list()
    
    def add_structure_deltas(self, structure_type: t_structure, deltas: tuple[float, float, float], **kwargs) -> list[t_structure]:
        if not issubclass(structure_type, Structure):
            return

        if issubclass(structure_type, Pipe):
            return self.add_bent_pipe(deltas, **kwargs)
        
        elif issubclass(structure_type, Bend):
            return self.add_bend(**kwargs)
        
        elif issubclass(structure_type, LinearStructure):
            return self._add_generic_linear_structure(structure_type, deltas, **kwargs)
        
        elif issubclass(structure_type, Arc):
            return self._add_generic_arc(structure_type, deltas, **kwargs)

    def add_pipe(self, deltas, **kwargs) -> list[Pipe]:
        return self._add_generic_linear_structure(Pipe, deltas, **kwargs)

    def add_bend(self, curvature_radius: float, allow_dangling=False, **kwargs) -> list[Bend]:
        bends = list()

        if curvature_radius <= 0:
            return bends

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        for point in self.pipeline.selected_points:
            vec_a, vec_b, dangling = self._get_bend_vectors(point)
            if dangling and not allow_dangling:
                continue

            angle_between_pipes = np.arccos(np.dot(vec_a, vec_b))
            if angle_between_pipes == 0:
                continue

            if angle_between_pipes == np.pi:  # 180º
                continue

            bend_exists = False
            for bend in self.pipeline.structures_of_type(Bend):
                if point in bend.get_points():
                    bend_exists = True
                    break

            # Do not put a bend over another
            if bend_exists:
                continue

            start = point
            corner = point.copy()
            end = point.copy()

            # detatch the connection between pipes (if it exists)
            # to add the bend in between them
            detatched = self.pipeline.detatch_point(point)
            if len(detatched) >= 1:
                end = detatched[0]

            bend = Bend(start, end, corner, curvature_radius, **kwargs)
            bend.normalize_values_vector(vec_a, vec_b)
            self.pipeline.add_structure(bend)
            bends.append(bend)

        return bends

    def add_flange(self, deltas, **kwargs) -> list[Flange]:
        return self._add_generic_linear_structure(Flange, deltas, **kwargs)

    def add_bent_pipe(self, deltas, curvature_radius: float, **kwargs) -> list[Pipe | Bend]:
        pipes = self.add_pipe(deltas, **kwargs)
        bends = self.add_bend(curvature_radius, **kwargs)

        # force the last point added to be a pipe point instead of a bend point
        if pipes:
            *_, last_pipe = pipes
            self.pipeline.staged_points.remove(last_pipe.end)
            self.pipeline.add_point(last_pipe.end)

        return bends + pipes

    def add_expansion_joint(self, deltas, **kwargs) -> list[ExpansionJoint]:
        return self._add_generic_linear_structure(ExpansionJoint, deltas, **kwargs)

    def add_valve(self, deltas, **kwargs) -> list[Valve]:
        return self._add_generic_linear_structure(Valve, deltas, **kwargs)

    def add_reducer_eccentric(self, deltas, **kwargs) -> list[Reducer]:
        return self._add_generic_linear_structure(Reducer, deltas, **kwargs)

    def add_circular_beam(self, deltas, **kwargs) -> list[CircularBeam]:
        return self._add_generic_linear_structure(CircularBeam, deltas, **kwargs)

    def add_rectangular_beam(self, deltas, **kwargs) -> list[RectangularBeam]:
        return self._add_generic_linear_structure(RectangularBeam, deltas, **kwargs)

    def add_i_beam(self, deltas, **kwargs) -> list[IBeam]:
        return self._add_generic_linear_structure(IBeam, deltas, **kwargs)

    def add_c_beam(self, deltas, **kwargs) -> list[CBeam]:
        return self._add_generic_linear_structure(CBeam, deltas, **kwargs)

    def add_t_beam(self, deltas, **kwargs) -> list[TBeam]:
        return self._add_generic_linear_structure(TBeam, deltas, **kwargs)

    def recalculate_curvatures(self):
        # collapse all curvatures that are in between pipes
        for bend in self.pipeline.structures_of_type(Bend):
            a_vectors = self.get_point_tangency(bend.start)
            b_vectors = self.get_point_tangency(bend.end)

            if (not a_vectors) or (not b_vectors):
                continue

            if not bend.auto:
                continue

            bend.colapse()

        for bend in self.pipeline.structures_of_type(Bend):
            if not bend.auto:
                continue

            a_vectors = self.get_point_tangency(bend.start)
            b_vectors = self.get_point_tangency(bend.end)

            if (not a_vectors) or (not b_vectors):
                continue

            vec_a, vec_b = a_vectors[0], b_vectors[0]
            angle_between_pipes = np.arccos(np.dot(vec_a, vec_b))

            if angle_between_pipes == 0:
                continue

            if angle_between_pipes == np.pi:  # 180º
                continue

            bend.normalize_values_vector(vec_a, vec_b)

        # Removing collapsed bends feels weird for users.
        # If you still want this for some reason discomment
        # the following line:
        # self.remove_collapsed_bends()

    def add_isolated_point(self, coords: tuple[float, float, float], **kwargs):
        point = Point(*coords, **kwargs)
        self.pipeline.add_point(point)
        self.next_border.append(point)
        return point

    def remove_collapsed_bends(self):
        to_remove = []
        for bend in self.pipeline.structures_of_type(Bend):
            if bend.is_colapsed():
                to_remove.append(bend)
        self.pipeline.remove_structures(to_remove)
        return to_remove

    def get_point_tangency(self, point: Point) -> list[np.ndarray]:
        directions = list()

        for structure in self.pipeline.structures_of_type(LinearStructure):
            if id(structure.start) == id(point):
                vector = point.coords() - structure.end.coords()
                size = np.linalg.norm(vector)
            elif id(structure.end) == id(point):
                vector = point.coords() - structure.start.coords()
                size = np.linalg.norm(vector)
            else:
                continue

            if size:
                directions.append(vector / size)

        for structure in self.pipeline.structures_of_type(Fillet):
            if structure.is_colapsed():
                continue
            
            if id(structure.start) == id(point):
                vector = structure.end.coords() - structure.corner.coords()
                size = np.linalg.norm(vector)
            elif id(structure.end) == id(point):
                vector = structure.start.coords() - point.coords()
                size = np.linalg.norm(vector)
            else:
                continue

            if size:
                directions.append(vector / size)            

        return directions

    def _add_generic_arc(
            self, 
            structure_type: type[Arc], 
            deltas: tuple[float, float, float], 
            **kwargs
    ):
        if not np.array(deltas).any():  # all zeros
            return []

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        structures = list()
        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)

            tangencies = self.get_point_tangency(point)
            tangency = tangencies[0] if tangencies else np.array([1, 0, 0])
            structure = structure_type.from_tangency(point, next_point, tangency, **kwargs)
            
            self.pipeline.add_structure(structure)
            structures.append(structure)
        
        return structures

    def _add_generic_linear_structure(
        self, 
        structure_type: type[LinearStructure], 
        deltas: tuple[float, float, float], 
        **kwargs
    ):
        if not np.array(deltas).any():  # all zeros
            return []

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        structures = list()
        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            structure = structure_type(point, next_point, **kwargs)
            self.pipeline.add_structure(structure)
            structures.append(structure)
        self.pipeline.main_editor._colapse_overloaded_bends()
        return structures

    def _colapse_overloaded_bends(self):
        """
        If a bend, that should connect only two pipes, has a third connection
        or more, this function will colapse it.
        Then, during the commit, these colapsed bends can be safelly removed.
        """

        for point in self.pipeline.selected_points:
            for bend in self.pipeline.structures_of_type(Bend):
                if not bend.auto:
                    continue

                if id(bend.corner) != id(point):
                    continue

                bend.colapse()

    def _get_bend_vectors(self, point: Point):
        directions = self.get_point_tangency(point)

        if len(directions) == 0:
            vec_a = np.array([-1, 0, 0])
            vec_b = np.array([0, 1, 0])
            dangling = True

        elif len(directions) == 1:
            vec_a = directions[0]
            if not np.allclose(vec_a, [0, 0, 1]):
                vec_b = np.cross(vec_a, [0, 0, 1])
            else:
                vec_b = np.cross(vec_a, [1, 0, 0])
            dangling = True

        else:
            vec_a, vec_b, *_ = directions
            dangling = False

        return vec_a, vec_b, dangling
