from dataclasses import dataclass
from vtkat.render_widgets import CommonRenderWidget

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

        self.create_axes()
        self.create_scale_bar()
        self.set_theme("light")

    def update_plot(self, reset_camera=True):
        project = app().main_window.project

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActor(project)

        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.tubes_actor)

        if reset_camera:
            self.renderer.ResetCamera()
