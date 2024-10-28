from itertools import chain, pairwise
from typing import Generator, TypeVar

import numpy as np
import yaml

from pulse.editor.editor_delegate import (
    ConnectionEditor,
    DivideEditor,
    MainEditor,
    PointsEditor,
    ReplaceEditor,
    SelectionEditor,
)

from pulse.editor.structures import (
    Beam,
    Bend,
    Elbow,
    Flange,
    Pipe,
    Point,
    Structure,
    TBeam
)

# only to help the editor, ignore it
generic_type = TypeVar("generic_type")


class Pipeline:
    def __init__(self):
        self.points: list[Point] = list()
        self.structures: list[Structure] = list()

        self.staged_points: list[Point] = list()
        self.staged_structures: list[Structure] = list()

        self.selected_points: list[Point] = list()
        self.selected_structures: list[Structure] = list()

        # Instead of placing incountable lines of code here,
        # most of the functions are a facade, and their actual
        # implementation is handled by one of the following editors.
        self.main_editor = MainEditor(self)
        self.points_editor = PointsEditor(self)
        self.selection_editor = SelectionEditor(self)
        self.connection_editor = ConnectionEditor(self)
        self.replace_editor = ReplaceEditor(self)
        self.divide_editor = DivideEditor(self)

    def reset(self):
        self.points.clear()
        self.structures.clear()
        self.staged_points.clear()
        self.staged_structures.clear()
        self.selected_points.clear()
        self.selected_structures.clear()
        self.points.append(Point(0, 0, 0))

    def load_file(self, path):
        with open(path, "r") as file:
            data = yaml.safe_load(file)

        if data is not None:
            self.points = data["points"]
            self.structures = data["structures"]

    def save_file(self, path):
        with open(path, "w") as file:
            yaml.safe_dump(self.as_dict(), file, sort_keys=False)

    def all_points(self):
        return chain(self.points, self.staged_points)

    def all_structures(self):
        return chain(self.structures, self.staged_structures)

    def structures_of_type(
        self, structure_type: generic_type
    ) -> Generator[generic_type, None, None]:
        for structure in self.all_structures():
            if isinstance(structure, structure_type):
                yield structure

    # Essential functions
    def commit(self):
        self.main_editor.remove_collapsed_bends()

        for structure in self.staged_structures:
            structure.staged = False

        self.points.extend(self.staged_points)
        self.structures.extend(self.staged_structures)

        # select the points to continue the creation
        self.select_points(self.main_editor.next_border)
        self.main_editor.next_border.clear()

        self.staged_points.clear()
        self.staged_structures.clear()
        self.main_editor.next_border.clear()

    def dismiss(self):
        for structure in self.staged_structures:
            if isinstance(structure, Bend):
                structure.colapse()

        self.staged_points.clear()
        self.staged_structures.clear()
        self.main_editor.next_border.clear()
        self.main_editor.next_border.clear()

        self.main_editor.recalculate_curvatures()

    def add_point(self, point: Point):
        self.staged_points.append(point)

    def add_structure(self, structure: Structure):
        structure.staged = True
        self.staged_structures.append(structure)
        self.add_points(structure.get_points())

    def remove_point(self, point: Point, rejoin=True):
        if not isinstance(point, Point):
            return

        for i in self.get_point_indexes(point):
            self.points.pop(i)

        structures_to_remove = []
        for structure in self.structures:
            if point in structure.get_points():
                structures_to_remove.append(structure)

        for structure in structures_to_remove:
            self.remove_structure(structure, rejoin)

    def remove_structure(self, structure: Structure, rejoin=True):
        if not isinstance(structure, Structure):
            return

        if rejoin and isinstance(structure, Bend | Elbow):
            structure.colapse()

        for i in self.get_structure_indexes(structure):
            self.structures.pop(i)

        if rejoin and isinstance(structure, Bend | Elbow):
            self.attatch_point(structure.corner)

    def delete_selection(self):
        for structure in self.selected_structures:
            self.remove_structure(structure, rejoin=True)

        for point in self.selected_points:
            self.remove_point(point, rejoin=False)

        self.clear_selection()

    # Essential functions plural
    def add_points(self, points: list[Point]):
        for point in points:
            self.add_point(point)

    def add_structures(self, structures: list[Structure]):
        for structure in structures:
            self.add_structure(structure)

    def remove_points(self, points: list[Point]):
        for point in points:
            self.remove_point(point)

    def remove_structures(self, structures: list[Structure]):
        for structure in structures:
            self.remove_structure(structure)

    def get_point_indexes(self, point: Point):
        indexes = []
        for i, s in enumerate(self.points):
            if id(s) == id(point):
                indexes.append(i)
        indexes.reverse()
        return indexes

    def get_structure_indexes(self, structure: Structure):
        indexes = []
        for i, s in enumerate(self.structures):
            if id(s) == id(structure):
                indexes.append(i)
        indexes.reverse()
        return indexes

    # Main Editor
    def add_structure_deltas(self, structure_type, deltas, **kwargs):
        return self.main_editor.add_structure_deltas(structure_type, deltas, **kwargs)

    def add_pipe(self, deltas, **kwargs):
        return self.main_editor.add_pipe(deltas, **kwargs)

    def add_bend(self, curvature_radius, **kwargs):
        return self.main_editor.add_bend(curvature_radius, **kwargs)

    def add_flange(self, deltas, **kwargs):
        return self.main_editor.add_flange(deltas, **kwargs)

    def add_bent_pipe(self, deltas, curvature_radius, **kwargs):
        return self.main_editor.add_bent_pipe(deltas, curvature_radius, **kwargs)

    def add_expansion_joint(self, deltas, **kwargs):
        return self.main_editor.add_expansion_joint(deltas, **kwargs)

    def add_valve(self, deltas, **kwargs):
        return self.main_editor.add_valve(deltas, **kwargs)

    def add_reducer_eccentric(self, deltas, **kwargs):
        return self.main_editor.add_reducer_eccentric(deltas, **kwargs)

    def add_circular_beam(self, deltas, **kwargs):
        return self.main_editor.add_circular_beam(deltas, **kwargs)

    def add_rectangular_beam(self, deltas, **kwargs):
        return self.main_editor.add_rectangular_beam(deltas, **kwargs)

    def add_c_beam(self, deltas, **kwargs):
        return self.main_editor.add_c_beam(deltas, **kwargs)

    def add_t_beam(self, deltas, **kwargs):
        return self.main_editor.add_t_beam(deltas, **kwargs)

    def add_i_beam(self, deltas, **kwargs):
        return self.main_editor.add_i_beam(deltas, **kwargs)

    def add_isolated_point(self, coords, **kwargs):
        return self.main_editor.add_isolated_point(coords, **kwargs)

    def recalculate_curvatures(self):
        self.main_editor.recalculate_curvatures()

    # Connection Editor
    def connect_structures(self, structure_type: type[Structure], **kwargs):
        return self.connection_editor.connect_structure(structure_type, **kwargs)

    def connect_pipes(self, **kwargs):
        return self.connection_editor.connect_pipes(**kwargs)

    def connect_bent_pipes(self, curvature_radius, **kwargs):
        return self.connection_editor.connect_bent_pipes(curvature_radius, **kwargs)

    def connect_flanges(self, **kwargs):
        return self.connection_editor.connect_flanges(**kwargs)

    def connect_expansion_joints(self, **kwargs):
        return self.connection_editor.connect_expansion_joints(**kwargs)

    def connect_valves(self, **kwargs):
        return self.connection_editor.connect_valves(**kwargs)

    def connect_reducer_eccentrics(self, **kwargs):
        return self.connection_editor.connect_reducer_eccentrics(**kwargs)

    def connect_circular_beams(self, **kwargs):
        return self.connection_editor.connect_circular_beams(**kwargs)

    def connect_rectangular_beams(self, **kwargs):
        return self.connection_editor.connect_rectangular_beams(**kwargs)

    def connect_i_beams(self, **kwargs):
        return self.connection_editor.connect_i_beams(**kwargs)

    def connect_c_beams(self, **kwargs):
        return self.connection_editor.connect_c_beams(**kwargs)

    def connect_t_beams(self, **kwargs):
        return self.connection_editor.connect_t_beams(**kwargs)

    # Replace Editor
    def replace_selection_by(self, structure_type: type[Structure], **kwargs):
        return self.replace_editor.replace_selection_by(structure_type, **kwargs) 

    def replace_by_pipe(self, **kwargs):
        return self.replace_editor.replace_selection_by(Pipe, **kwargs)
    
    # def replace_by_bent_pipes(self, curvature_radius, **kwargs):
    #     return self.replace_editor.replace_by_bent_pipes(curvature_radius, **kwargs)

    def replace_by_flanges(self, **kwargs):
        return self.replace_editor.replace_by_flanges(**kwargs)

    def replace_by_expansion_joints(self, **kwargs):
        return self.replace_editor.replace_by_expansion_joints(**kwargs)

    def replace_by_valves(self, **kwargs):
        return self.replace_editor.replace_by_valves(**kwargs)

    def replace_by_reducer_eccentrics(self, **kwargs):
        return self.replace_editor.replace_by_reducer_eccentrics(**kwargs)

    def replace_by_circular_beams(self, **kwargs):
        return self.replace_editor.replace_by_circular_beams(**kwargs)

    def replace_by_rectangular_beams(self, **kwargs):
        return self.replace_editor.replace_by_rectangular_beams(**kwargs)

    def replace_by_i_beams(self, **kwargs):
        return self.replace_editor.replace_by_i_beams(**kwargs)

    def replace_by_c_beams(self, **kwargs):
        return self.replace_editor.replace_by_c_beams(**kwargs)

    def replace_by_t_beams(self, **kwargs):
        return self.replace_editor.replace_selection_by(TBeam, **kwargs)

    # Points Editor
    def attatch_point(self, point: Point):
        self.points_editor.attatch_point(point)

    def detatch_point(self, point: Point):
        return self.points_editor.dettatch_point(point)

    def join_points(self, points: list[Point]):
        self.points_editor.join_points(points)

    def move_point(self, point, new_position):
        self.points_editor.move_point(point, new_position)

    def merge_coincident_points(self):
        self.points_editor.merge_coincident_points()

    # Selection Editor
    def select_points(self, points, join=False, remove=False):
        self.selection_editor.select_points(points, join, remove)

    def select_structures(self, structures, join=False, remove=False):
        self.selection_editor.select_structures(structures, join, remove)

    def select_last_point(self):
        self.selection_editor.select_last_point()

    def select_last_structure(self):
        self.selection_editor.select_last_structure()

    def clear_selection(self):
        self.selection_editor.clear_selection()

    def clear_point_selection(self):
        self.selection_editor.clear_point_selection()

    def clear_structure_selection(self):
        self.selection_editor.clear_structure_selection()

    # Divide editor
    def divide_structures(self, t=0.5):
        self.divide_editor.divide_structures(t)

    def divide_structures_evenly(self, divisions=1):
        self.divide_editor.divide_structures_evenly(divisions)

    def preview_divide_structures(self, t=0.5):
        self.divide_editor.preview_divide_structures(t)

    def preview_divide_structures_evenly(self, divisions=1):
        self.divide_editor.preview_divide_structures_evenly(divisions)

    # Common
    def as_dict(self) -> dict:
        return {"structures": self.structures, "points": self.points}

    def as_vtk(self):
        from pulse.interface.viewer_3d.actors import (
            PipelineActor,
        )

        return PipelineActor(self)

    def __hash__(self) -> int:
        return id(self)
