from dataclasses import dataclass
from vtkat.render_widgets import CommonRenderWidget
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker

from pulse.interface.viewer_3d.actors import NodesActor, ElementLinesActor, TubeActor
from pulse import app


@dataclass
class PlotFilter:
    nodes: bool = False
    lines: bool = False
    tubes: bool = False
    transparent: bool = False
    acoustic_symbols: bool = False
    structural_symbols: bool = False
    raw_lines: bool = False


@dataclass
class SelectionFilter:
    nodes: bool    = False
    entities: bool = False
    elements: bool = False


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        
        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None

        self.create_axes()
        self.create_scale_bar()
        self.set_theme("light")

    def update_plot(self, reset_camera=True):
        self.remove_actors()
        project = app().project

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActor(project)

        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.tubes_actor)

        if reset_camera:
            self.renderer.ResetCamera()
    
    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.tubes_actor)

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x, y):
        self.tubes_actor.clear_colors()
        picker = CellAreaPicker()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            picker.pick(x, y, 0, self.renderer)

        picked = picker.get_picked()
        if self.tubes_actor in picked:
            cells = picked[self.tubes_actor]
            elements = {self.tubes_actor.get_cell_element(i) for i in cells}
            entities = {self.tubes_actor.get_cell_entity(i) for i in cells}
            self.tubes_actor.set_color((255, 0, 0), elements=elements, entities=entities)
