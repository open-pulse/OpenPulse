from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .mesh_render_widget import MeshRenderWidget

import vtk
from pulse import app
from itertools import product


class MeshPicker:
    '''
    A custom class to make mesh selection as fast as possible.
    '''
    def __init__(self, mesh_render_widget: 'MeshRenderWidget'):
        self.mesh_render_widget = mesh_render_widget

        self.nodes_bounds = dict()
        self.elements_bounds = dict()
        self.entities_bounds = dict()
    
    def update_bounds(self):
        elements = app().project.get_structural_elements()
        
        self.elements_bounds.clear()
        for key, element in elements.items():
            first_node = element.first_node.coordinates
            last_node = element.last_node.coordinates

            x0 = min(first_node[0], last_node[0])
            y0 = min(first_node[1], last_node[1])
            z0 = min(first_node[2], last_node[2])
            x1 = max(first_node[0], last_node[0])
            y1 = max(first_node[1], last_node[1])
            z1 = max(first_node[2], last_node[2])

            bounds = (x0,x1,y0,y1,z0,z1)
            self.elements_bounds[key] = bounds

    def area_pick_nodes(self, x0, y0, x1, y1) -> set[int]:
        pass

    def area_pick_elements(self, x0, y0, x1, y1) -> set[int]:
        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        picked_elements = {
            key for key, bound in self.elements_bounds.items()
            if extractor.OverallBoundsTest(bound)
        }
        
        # Add an extra pick on the last corner 
        element = self.pick_element(x1, y1)
        if element >= 0:
            picked_elements.add(element)

        return picked_elements

    def area_pick_entities(self, x0, y0, x1, y1) -> set[int]:
        picker = vtk.vtkAreaPicker()
        extractor = vtk.vtkExtractSelectedFrustum()
        picker.AreaPick(x0, y0, x1, y1, self.mesh_render_widget.renderer)
        extractor.SetFrustum(picker.GetFrustum())

        elements_to_line = app().project.preprocessor.elements_to_line
        picked_entities = set()

        for element, bound in self.elements_bounds.items():
            entity = elements_to_line[element]

            if entity in picked_entities:
                continue
            
            if extractor.OverallBoundsTest(bound):
                picked_entities.add(entity)

        return picked_entities

    def pick_node(self, x, y):
        pass

    def pick_element(self, x, y) -> int:
        lines_actor = self.mesh_render_widget.lines_actor
        element = self._pick_cell_property(x, y, "element_index", lines_actor)
        if element >= 0:
            return element

        tubes_actor = self.mesh_render_widget.tubes_actor
        element = self._pick_cell_property(x, y, "element_index", tubes_actor)
        return element

    def pick_entity(self, x, y) -> int:
        element = self.pick_element(x, y)
        if element < 0:
            return -1

        line_to_elements = app().project.preprocessor.line_to_elements
        for i, entity_elements in line_to_elements.items():
            if element in entity_elements:
                return i

        return -1

    def _pick_cell_property(self, x: float, y: float, property_name: str, target_actor: vtk.vtkActor):
        actor: vtk.vtkActor
        cell_picker = vtk.vtkCellPicker()
        cell_picker.SetTolerance(0.0005)
        pickability = dict()

        # make only the target actor pickable
        for actor in self.mesh_render_widget.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            actor.SetPickable(actor == target_actor)

        cell_picker.Pick(x, y, 0, self.mesh_render_widget.renderer)
        
        if target_actor != cell_picker.GetActor():
            return -1

        data: vtk.vtkPolyData = target_actor.GetMapper().GetInput()
        if data is None:
            return -1

        property_array = data.GetCellData().GetArray(property_name)
        if property_array is None:
            return -1

        cell = cell_picker.GetCellId()
        
        # restore the pickable status for every actor
        for actor in self.mesh_render_widget.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return property_array.GetValue(cell)
