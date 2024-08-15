from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mesh_render_widget import MeshRenderWidget

from itertools import product

import numpy as np
from molde.pickers import CellAreaPicker
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkExtractSelectedFrustum
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkAreaPicker,
    vtkCellPicker,
    vtkPropPicker,
)

from pulse import app


class MeshPicker:
    """
    A custom class to make mesh selection as fast as possible.
    """

    def __init__(self, mesh_render_widget: "MeshRenderWidget"):
        self.mesh_render_widget = mesh_render_widget

        self.nodes_bounds = dict()
        self.line_bounds = dict()
        self.tube_bounds = dict()

    def update_bounds(self):

        elements = app().project.preprocessor.structural_elements
        nodes = app().project.preprocessor.nodes

        self.nodes_bounds.clear()
        self.line_bounds.clear()
        self.tube_bounds.clear()

        for key, node in nodes.items():
            x, y, z = node.coordinates
            self.nodes_bounds[key] = (x, x, y, y, z, z)

        for key, element in elements.items():
            first_node = element.first_node.coordinates
            last_node = element.last_node.coordinates

            x0 = min(first_node[0], last_node[0])
            y0 = min(first_node[1], last_node[1])
            z0 = min(first_node[2], last_node[2])
            x1 = max(first_node[0], last_node[0])
            y1 = max(first_node[1], last_node[1])
            z1 = max(first_node[2], last_node[2])

            if element.cross_section is None:
                return

            # not sure if it works every time, but is a good approximation
            radius = max(element.cross_section.section_parameters)
            center = element.element_center_coordinates

            line_bounds = (x0, x1, y0, y1, z0, z1)
            self.line_bounds[key] = line_bounds

            # If the cross section is bigger than the element in some dimension
            # increase this dimension by the radius of the cross section
            if abs(x1 - x0) < radius:
                x0 = center[0] - radius / 2
                x1 = center[0] + radius / 2

            if abs(y1 - y0) < radius:
                y0 = center[1] - radius / 2
                y1 = center[1] + radius / 2

            if abs(z1 - z0) < radius:
                z0 = center[2] - radius / 2
                z1 = center[2] + radius / 2

            # The xyz sizes may have changed
            tube_bounds = (x0, x1, y0, y1, z0, z1)
            self.tube_bounds[key] = tube_bounds

    def area_pick_nodes(self, x0, y0, x1, y1) -> set[int]:
        picker = vtkAreaPicker()
        extractor = vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        picked_nodes = {
            key
            for key, bound in self.nodes_bounds.items()
            if extractor.OverallBoundsTest(bound)
        }

        return picked_nodes

    def area_pick_elements(self, x0, y0, x1, y1) -> set[int]:
        picker = vtkAreaPicker()
        extractor = vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        picked_elements = {
            key
            for key, bound in self.line_bounds.items()
            if extractor.OverallBoundsTest(bound)
        }

        # Add an extra pick on the last corner
        element = self.pick_element(x1, y1)
        if element >= 0:
            picked_elements.add(element)

        return picked_elements

    def area_pick_lines(self, x0, y0, x1, y1) -> set[int]:
        picker = vtkAreaPicker()
        extractor = vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        elements_to_line = app().project.model.mesh.elements_to_line
        picked_lines = set()

        for element, bound in self.line_bounds.items():
            entity = elements_to_line[element]

            if entity in picked_lines:
                continue

            if extractor.OverallBoundsTest(bound):
                picked_lines.add(entity)

        return picked_lines

    def pick_node(self, x, y) -> int:
        points_actor = self.mesh_render_widget.points_actor
        node = self._pick_cell_property(x, y, "node_index", points_actor)
        if node >= 0:
            return node

        nodes_actor = self.mesh_render_widget.nodes_actor
        node = self._pick_cell_property(x, y, "node_index", nodes_actor)
        return node

    def pick_element(self, x, y) -> int:
        lines_actor = self.mesh_render_widget.lines_actor
        element = self._pick_cell_property(x, y, "element_index", lines_actor)
        if element >= 0:
            return element

        tubes_actor = self.mesh_render_widget.tubes_actor
        element = self._pick_tube_element(x, y, tubes_actor)
        return element

    def pick_entity(self, x, y) -> int:
        element = self.pick_element(x, y)
        if element < 0:
            return -1

        line_to_elements = app().project.model.mesh.line_to_elements
        for i, entity_elements in line_to_elements.items():
            if element in entity_elements:
                return i

        return -1

    def _pick_tube_element(self, x: float, y: float, target_actor: vtkActor):
        picker = vtkPropPicker()
        elements = app().project.get_structural_elements()

        pickability = self._narrow_pickability_to_actor(target_actor)
        picker.Pick(x, y, 0, self.mesh_render_widget.renderer)
        self._restore_pickability(pickability)

        if picker.GetActor() != target_actor:
            return -1

        point = picker.GetPickPosition()
        closest_id = -1
        closest_dist = None
        # TODO: we dont need bounds here
        for i, bounds in self.tube_bounds.items():
            dist = np.linalg.norm(elements[i].element_center_coordinates - point)
            if (closest_dist is None) or (dist < closest_dist):
                closest_id = i
                closest_dist = dist

        return closest_id

    def _pick_cell_property(
        self, x: float, y: float, property_name: str, target_actor: vtkActor
    ):
        cell_picker = vtkCellPicker()
        cell_picker.SetTolerance(0.0018)

        pickability = self._narrow_pickability_to_actor(target_actor)
        cell_picker.Pick(x, y, 0, self.mesh_render_widget.renderer)
        self._restore_pickability(pickability)

        if target_actor != cell_picker.GetActor():
            return -1

        data: vtkPolyData = target_actor.GetMapper().GetInput()
        if data is None:
            return -1

        property_array = data.GetCellData().GetArray(property_name)
        if property_array is None:
            return -1

        cell = cell_picker.GetCellId()

        return property_array.GetValue(cell)

    def _point_inside_bounds(self, point, bounds) -> bool:
        x, y, z = point
        x0, x1, y0, y1, z0, z1 = bounds
        return all(
            [
                (x0 < x < x1) or (x0 > x > x1),  # inside x
                (y0 < y < y1) or (y0 > y > y1),  # inside y
                (z0 < z < z1) or (z0 > z > z1),  # inside z
            ]
        )

    def _verts_from_bounds(self, bounds):
        x0, x1, y0, y1, z0, z1 = bounds
        return product((x0, x1), (y0, y1), (z0, z1))

    def _distance_point_bounds(self, point, bounds) -> float:
        point = np.array(point)
        distance_fn = lambda _vertice: np.linalg.norm(point - _vertice)
        vertices = self._verts_from_bounds(bounds)
        return min(vertices, key=distance_fn)

    def _narrow_pickability_to_actor(self, target_actor: vtkActor):
        actor: vtkActor
        pickability = dict()
        for actor in self.mesh_render_widget.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            actor.SetPickable(actor == target_actor)
        return pickability

    def _restore_pickability(self, pickability: dict):
        actor: vtkActor
        for actor in self.mesh_render_widget.renderer.GetActors():
            actor.SetPickable(pickability[actor])
