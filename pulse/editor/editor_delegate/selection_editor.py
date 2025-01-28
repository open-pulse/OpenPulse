import numpy as np
from ordered_set import OrderedSet

from pulse.editor.structures import Point

from .editor import Editor


class SelectionEditor(Editor):
    def select_last_point(self):
        if self.pipeline.points:
            *_, point = self.pipeline.points
        else:
            point = Point(0, 0, 0)
            self.pipeline.staged_points.append(point)

        self.pipeline.select_points([point])

    def select_last_structure(self):
        if not self.pipeline.structures:
            return

        *_, structure = self.pipeline.structures
        self.pipeline.select_structures([structure])

    def select_points(self, points, join=False, remove=False):
        points = OrderedSet(points)

        if not points:
            return

        current_selection = OrderedSet(self.pipeline.selected_points)

        if join and remove:
            current_selection ^= points
        elif join:
            current_selection |= points
        elif remove:
            current_selection -= points
        else:
            current_selection = points

        self.pipeline.selected_points = list(current_selection)

    def select_structures(self, structures, join=False, remove=False):
        structures = OrderedSet(structures)

        if not structures:
            return

        current_selection = OrderedSet(self.pipeline.selected_structures)

        # clear all the selected flags
        for structure in self.pipeline.structures:
            structure.selected = False

        # handle the selection according to modifiers like ctrl, shift, etc.
        if join and remove:
            current_selection ^= structures
        elif join:
            current_selection |= structures
        elif remove:
            current_selection -= structures
        else:
            current_selection = structures

        # apply the selection flag again for selected structures
        for structure in current_selection:
            structure.selected = True

        self.pipeline.selected_structures = list(current_selection)

    def clear_selection(self):
        self.clear_structure_selection()
        self.clear_point_selection()

    def clear_point_selection(self):
        self.pipeline.selected_points.clear()

    def clear_structure_selection(self):
        for structure in self.pipeline.structures:
            structure.selected = False
        self.pipeline.selected_structures.clear()
