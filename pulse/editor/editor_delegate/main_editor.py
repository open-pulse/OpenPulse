from typing import TypeVar

import numpy as np

from pulse.editor.structures import (
    Arc,
    Bend,
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Fillet,
    Flange,
    IBeam,
    LinearStructure,
    Pipe,
    Point,
    RectangularBeam,
    Reducer,
    Structure,
    TBeam,
    Valve,
)
from pulse.editor.structures.coupling_element import CouplingElement
from pulse.interface import error_title
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.utils.math_utils import normalize

from .editor import Editor

t_structure = TypeVar("t_structure", bound=type[Structure])


class MainEditor(Editor):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.next_border = list()

        # False attaches branches directly to the junction point,
        # without the CouplingElement correction.
        self.correct_t_junction = True

    def add_structure_deltas(
        self,
        structure_type: t_structure,
        deltas: tuple[float, float, float],
        correct_t_junction: bool = True,
        **kwargs,
    ) -> list[t_structure]:

        self.correct_t_junction = correct_t_junction

        if not issubclass(structure_type, Structure):
            return list()

        if deltas == (0, 0, 0):
            return list()

        if issubclass(structure_type, Pipe):
            if self.is_bend_allowed(self.pipeline.selected_points):
                return self.add_bent_pipe(deltas, **kwargs)
            else:
                return self.add_pipe(deltas, **kwargs)

        elif issubclass(structure_type, Bend):
            return self.add_bend(**kwargs)

        elif issubclass(structure_type, LinearStructure):
            return self._add_generic_linear_structure(structure_type, deltas, **kwargs)

        elif issubclass(structure_type, Arc):
            return self._add_generic_arc(structure_type, deltas, **kwargs)

    def add_structure_length(
        self,
        structure_type: t_structure,
        length: float,
        **kwargs,
    ) -> list[t_structure]:

        structures = list()
        for point in self.pipeline.selected_points:
            tangent_vectors = self.get_point_tangency(point)

            if len(tangent_vectors) != 1:
                continue

            if length == 0:
                continue

            vector = tangent_vectors[0]
            deltas = vector * length

            structure = self._add_generic_linear_structure_to_point(
                structure_type,
                deltas,
                point,
                **kwargs,
            )
            structures.append(structure)

        return structures

    def add_pipe(self, deltas, **kwargs) -> list[Pipe]:
        return self._add_generic_linear_structure(Pipe, deltas, **kwargs)

    def add_bend(self, curvature_radius: float, allow_dangling=False, **kwargs) -> list[Bend]:
        bends = list()

        if curvature_radius <= 0:
            return bends

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        for point in self.pipeline.selected_points:
            for structure in self.pipeline.get_structures_of_point(point):
                if "psd_label" in structure.extra_info or "pulsation_damper_label" in structure.extra_info:
                    return bends

            # do not allow adding Bends in more than two connections
            if len(self.get_point_tangency(point)) > 2:
                continue

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

        for structure in self.pipeline.structures_of_type(Arc):
            center = structure.center
            if center is None:
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
                continue

            if id(structure.start) == id(point):
                u = normalize(structure.start.coords() - structure.center.coords())
            elif id(structure.end) == id(point):
                u = normalize(structure.end.coords() - structure.center.coords())
            else:
                continue

            v = normalize(structure.mid.coords() - structure.center.coords())
            n = np.cross(v, u)
            tangency = np.cross(n, u)
            size = np.linalg.norm(tangency)
            if size:
                directions.append(tangency / size)

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

    def can_add_structure_length(self) -> bool:
        for point in self.pipeline.selected_points:
            if self.is_endpoint(point):
                return True
        return False

    def is_endpoint(self, point: Point) -> bool:
        connections = 0

        for structure in self.pipeline.structures:
            if not isinstance(structure, Fillet | LinearStructure | Arc):
                continue

            if (point == structure.start) or (point == structure.end):
                connections += 1

        return connections == 1

    def _is_junction(self, point: Point) -> bool:
        """
        A junction is a point where two or more linear structures meet. Only
        those need the coupling element correction.
        """
        connections = 0

        for structure in self.pipeline.structures:
            if not isinstance(structure,LinearStructure):
                continue

            if (point == structure.start) or (point == structure.end):
                connections += 1

        return connections >= 2

    def _add_generic_arc(self, structure_type: type[Arc], deltas: tuple[float, float, float], **kwargs):
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
        **kwargs,
    ):
        if not np.array(deltas).any():  # all zeros
            return list()

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        structures = list()
        for point in self.pipeline.selected_points:
            if self._is_junction(point) and self.correct_t_junction:
                new_structures = self._add_corrected_t_junction(structure_type, deltas, point, **kwargs)
            else:
                new_structures = [
                    self._add_generic_linear_structure_to_point(structure_type, deltas, point, **kwargs)
                ]

            structures.extend(new_structures)

        self.pipeline.main_editor._colapse_overloaded_bends()
        return structures

    def _add_generic_linear_structure_to_point(self, structure_type: type[LinearStructure], deltas: tuple[float, float, float], point: Point, **kwargs):

        next_point = Point(*(point.coords() + deltas))
        self.next_border.append(next_point)
        structure = structure_type(point, next_point, **kwargs)
        self.pipeline.add_structure(structure)
        return structure

    def _add_corrected_t_junction(self, structure_type: type[LinearStructure], deltas: tuple[float, float, float], point: Point, **kwargs):
        """
        Creates a T-junction: a CouplingElement of length D/2 that shifts the
        branch start away from the main pipe axis, plus the branch itself.
        """
        pipe_before, pipe_after = self._get_junction_pipes(point)

        if pipe_before is None or pipe_after is None:
            title = "Invalid T-junction"
            message = "One of the pipes of the junction is 'None'."
            PrintMessageInput([error_title, title, message])
            return list()

        if not self._has_matching_diameters(pipe_before, pipe_after):
            title = "Mismatched diameters at the T-junction"
            message = "The pipes joined at this point have diameters "
            message += f"{pipe_before.diameter} and {pipe_after.diameter}. "
            message += "Both must match to create a branch."
            PrintMessageInput([error_title, title, message])
            return list()


        diameter = pipe_before.diameter
        branch_direction = normalize(np.array(deltas, dtype=float))

        coupling_element_length = diameter / 2
        coupling_element_start = point
        coupling_element_end = Point(*(point.coords() + branch_direction * coupling_element_length))

        coupling_element = CouplingElement(coupling_element_start, coupling_element_end, extra_info=self._coupling_extra_info(pipe_before))
        self.pipeline.add_structure(coupling_element)

        branch_deltas = tuple(np.array(deltas, dtype=float) - np.array(coupling_element_end - coupling_element_start))
        branch = self._add_generic_linear_structure_to_point(structure_type, branch_deltas, coupling_element_end, **kwargs)

        return [coupling_element, branch]


    def _get_junction_pipes(self, point: Point) -> tuple[Pipe | None, Pipe | None]:
        """
        Finds the two pipes joined at `point`: the one that ends there and the one
        that starts there.

        Returns
        -------
        tuple
            (pipe_before, pipe_after). Either entry is None when no pipe matches.
        """
        pipe_before = None
        pipe_after = None

        for structure in self.pipeline.structures_of_type(Pipe):
            if point not in structure.get_points():
                continue

            if point == structure.end:
                pipe_before = structure

            elif point == structure.start:
                pipe_after = structure

        return pipe_before, pipe_after

    def _has_matching_diameters(self, pipe_before: Pipe, pipe_after: Pipe) -> bool:
        return np.isclose(pipe_before.diameter, pipe_after.diameter)

    def _coupling_extra_info(self, parent_pipe: Pipe) -> dict:
        return dict(
            structural_element_type="coupling_element",
            material_id=parent_pipe.extra_info.get("material_id"),
        )

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
