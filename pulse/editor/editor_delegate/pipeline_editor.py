from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, fields

import numpy as np

from pulse.editor.structures import (
    Bend,
    Elbow,
    Flange,
    IBeam,
    Pipe,
    Point,
    Structure,
)
from pulse.editor import Pipeline


class PipelineEditor:
    def __init__(self, pipeline: Pipeline, origin=(0.0, 0.0, 0.0)):
        self.pipeline = pipeline
        self.pipeline._update_points()

        self.deltas = np.array([0, 0, 0])
        self.anchor = Point(0, 0, 0)
        self.default_initial_diameter = 0.2
        self.default_final_diameter = 0.2

        self.selected_points = set()
        self.selected_structures = set()
        self.staged_structures = list()

    def reset(self):
        # not the same as __init__
        self.pipeline.structures.clear()
        self.deltas = np.array([0, 0, 0])
        self.default_initial_diameter = 0.2
        self.default_final_diameter = 0.2

        self.selected_points.clear()
        self.selected_structures.clear()
        self.staged_structures.clear()

    def set_anchor(self, point):
        self.anchor = point

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def add_structure(self, structure):
        structure.staged = True
        self.pipeline.add_structure(structure)
        self.staged_structures.append(structure)
        self.update()
        return structure

    def remove_structure(self, structure, rejoin=True):
        if not isinstance(structure, Structure):
            return

        if rejoin and isinstance(structure, Bend | Elbow):
            structure.colapse()

        self.pipeline.remove_structure(structure)

    def merge_coincident_points(self):
        found_points = dict()
        points_to_remove = []

        for structure in self.pipeline.structures:
            for point in structure.get_points():
                x, y, z = np.round(point.coords(), 6)

                if (x, y, z) in found_points:
                    new = found_points[x, y, z]
                    structure.replace_point(point, new)
                    points_to_remove.append(point)
                else:
                    found_points[x, y, z] = point

        self.pipeline.remove_points(points_to_remove)

    def remove_point(self, point, rejoin=True):
        if not isinstance(point, Point):
            return

        structures_to_remove = []
        for structure in self.pipeline.structures:
            if point in structure.get_points():
                structures_to_remove.append(structure)

        for structure in structures_to_remove:
            self.remove_structure(structure, rejoin)

    def move_point(self, position):
        if self.anchor not in self.pipeline.control_points:
            return
        self.anchor.set_coords(*position)

    def morph(self, structure, new_type):
        params = self._structure_params(structure)
        new_structure = new_type(**params)

        self.remove_structure(structure)
        self.pipeline.add_structure(new_structure)
        return new_structure

    def commit(self):
        self.update()
        for structure in self.pipeline.structures:
            structure.staged = False
        self.staged_structures.clear()

    def dismiss(self):
        staged_points = []
        for structure in self.staged_structures:
            staged_points.extend(structure.get_points())
            self.remove_structure(structure)
        self.staged_structures.clear()
        self.update()

        point_hashes = set(self.pipeline.points)
        if self.anchor in point_hashes:
            return

        for point in staged_points:
            if point in point_hashes:
                self.anchor = point
                break
        else:
            self.set_anchor(self.pipeline.control_points[-1])

    def change_diameter(self, initial_diameter, final_diameter):
        self.default_initial_diameter = initial_diameter
        self.default_final_diameter = final_diameter

    def get_diameters_at_point(self):
        diameters = []
        for structure in self.pipeline.structures:
            if self.anchor in structure.get_points():
                diameters.extend(structure.get_diameters())
        return diameters

    # STRUCTURES
    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        if self.anchor not in self.pipeline.control_points:
            return

        current_point = self.anchor
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(current_point, next_point)
        new_pipe.set_diameter(self.default_initial_diameter, self.default_final_diameter)

        self.add_structure(new_pipe)
        self.anchor = next_point
        return new_pipe

    def add_i_beam(self, deltas=None, **kwargs):
        if deltas != None:
            self.deltas = deltas

        if self.anchor not in self.pipeline.control_points:
            return

        current_point = self.anchor
        next_point = Point(*(current_point.coords() + self.deltas))
        new_beam = IBeam(current_point, next_point, **kwargs)

        self.add_structure(new_beam)
        self.anchor = next_point
        return new_beam

    def add_bend(self, curvature_radius=0.3):
        start_point = self.anchor
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into a Bend
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if start_point in joint.get_points():
                new_bend = self.morph(joint, Bend)

                if not self.pipeline._connected_points(joint.start):
                    self.anchor = joint.start
                elif not self.pipeline._connected_points(joint.end):
                    self.anchor = joint.end
                else:
                    self.anchor = joint.corner

                return new_bend

        new_bend = Bend(start_point, end_point, corner_point, curvature_radius)
        new_bend.set_diameter(self.default_initial_diameter, self.default_final_diameter)
        self.add_structure(new_bend)
        self.anchor = end_point
        return new_bend

    def add_elbow(self, curvature_radius=0.3):
        start_point = self.anchor
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into an Elbow
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                new_elbow = self.morph(joint, Elbow)

                if not self.pipeline._connected_points(joint.start):
                    self.anchor = joint.start
                elif not self.pipeline._connected_points(joint.end):
                    self.anchor = joint.end
                else:
                    self.anchor = joint.corner

                return new_elbow

        new_elbow = Elbow(start_point, end_point, corner_point, curvature_radius)
        new_elbow.set_diameter(self.default_initial_diameter, self.default_final_diameter)
        self.add_structure(new_elbow)
        self.anchor = end_point
        return new_elbow

    def add_flange(self):
        # If a flange already exists return it
        for flange in self.pipeline.structures:
            if not isinstance(flange, Flange):
                continue
            if flange.position == self.anchor:
                return flange

        # It avoids the placement of a flange in the middle of a bend.
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == self.anchor:
                new_flange = Flange(joint.start, normal=np.array([1, 0, 0]))
                new_flange.set_diameter(self.default_initial_diameter)
                self.add_structure(new_flange)
                return new_flange

        new_flange = Flange(self.anchor, normal=np.array([1, 0, 0]))
        new_flange.set_diameter(self.default_initial_diameter)
        self.add_structure(new_flange)
        return new_flange

    def add_bent_pipe(self, deltas=None, curvature_radius=0.3):
        if deltas != None:
            self.set_deltas(deltas)

        if all(self.deltas == (0, 0, 0)):
            return

        if self.anchor not in self.pipeline.control_points:
            return

        # do not add a bend if the only avaliable point is the origin
        if len(self.pipeline.points) > 1:
            self.add_bend(curvature_radius)

        return self.add_pipe(deltas)

    # SELECTION
    def select_points(self, points, join=False, remove=False):
        points = set(points)

        if not points:
            return

        if join and remove:
            self.selected_points ^= points
        elif join:
            self.selected_points |= points
        elif remove:
            self.selected_points -= points
        else:
            self.selected_points = points

    def select_structures(self, structures, join=False, remove=False):
        structures = set(structures)

        if not structures:
            return

        # clear all the selected flags
        for structure in self.pipeline.structures:
            structure.selected = False

        # handle the selection according to modifiers like ctrl, shift, etc.
        if join and remove:
            self.selected_structures ^= structures
        elif join:
            self.selected_structures |= structures
        elif remove:
            self.selected_structures -= structures
        else:
            self.selected_structures = structures

        # apply the selection flag again for selected structures
        for structure in self.selected_structures:
            structure.selected = True

    def clear_selection(self):
        for structure in self.pipeline.structures:
            structure.selected = False
        self.selected_points.clear()
        self.selected_structures.clear()

    def delete_selection(self):
        for structure in self.selected_structures:
            self.remove_structure(structure, rejoin=True)

        for point in self.selected_points:
            self.remove_point(point, rejoin=False)

        self.clear_selection()

    def update(self):
        pass

    def _structure_params(self, structure):
        """
        Get the params that can create a similar structure.
        It only works if the structure is a dataclass.
        """
        return {field.name: getattr(structure, field.name) for field in fields(structure)}
