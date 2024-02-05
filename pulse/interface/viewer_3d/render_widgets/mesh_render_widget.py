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

        self.plot_filter = PlotFilter(True, True, True, True, True, True)
        self.selection_filter = SelectionFilter(True, True, True)

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
        # self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.tubes_actor)

    def update_visualization(self, points, lines, tubes, symbols):
        transparent = points or lines or symbols
        self.plot_filter = PlotFilter(
            nodes=points,
            lines=lines,
            tubes=tubes,
            acoustic_symbols=symbols,
            structural_symbols=symbols,
            transparent=transparent,
        )
        
        elements = (lines or tubes) and points
        entities = (lines or tubes) and (not points) 
        self.selection_filter = SelectionFilter(
            nodes=points,
            elements=elements,
            entities=entities,
        )

        if not self._actor_exists():
            return 

        self.nodes_actor.SetVisibility(self.plot_filter.nodes)
        self.lines_actor.SetVisibility(self.plot_filter.lines)
        self.tubes_actor.SetVisibility(self.plot_filter.tubes)
        self.update()

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
            self.lines_actor,
            self.tubes_actor,
        ]
        return all([actor is not None for actor in actors])

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
