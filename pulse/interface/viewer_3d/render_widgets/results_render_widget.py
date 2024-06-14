from dataclasses import dataclass
from pathlib import Path

import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from vtkat.render_widgets import CommonRenderWidget

from pulse.interface.viewer_3d.actors import TubeActor
from pulse.interface.viewer_3d.actors.tube_actor import ColorMode
from pulse.interface.viewer_3d.text_helppers import TreeInfo, format_long_sequence
from pulse import app, ICON_DIR


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
    nodes: bool = False
    entities: bool = False
    elements: bool = False


class ResultsRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        app().main_window.theme_changed.connect(self.set_theme)
        
        # self.interactor_style = BoxSelectionInteractorStyle()
        # self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.open_pulse_logo = None
        self.tubes_actor = None

        self.create_axes()
        self.create_scale_bar()
        self.create_color_bar()
        self.create_logos()
        self.set_theme("light")

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.create_logos()

        project = app().project

        self.tubes_actor = TubeActor(project)

        self.renderer.AddActor(self.tubes_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        # self.update()
    
    def show_empty(self, *args, **kwargs):
        pass

    def show_displacement_field(self, frequency_index):
        pass

    def show_stress_field(self, frequency_index):
        pass

    def show_pressure_field(self, frequency_index):
        pass

    def remove_actors(self):
        self.renderer.RemoveActor(self.tubes_actor)
        self.tubes_actor = None
    
    def set_color_mode_to_empty(self):
        if not self._actor_exists():
            return
        self.tubes_actor.color_mode = ColorMode.empty
        self.tubes_actor.clear_colors()

    def set_color_mode_to_material(self):
        if not self._actor_exists():
            return
        self.tubes_actor.color_mode = ColorMode.material
        self.tubes_actor.clear_colors()

    def set_color_mode_to_fluid(self):
        if not self._actor_exists():
            return
        self.tubes_actor.color_mode = ColorMode.fluid
        self.tubes_actor.clear_colors()

    def _actor_exists(self):
        actors = [
            self.tubes_actor,
        ]
        return all([actor is not None for actor in actors])

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.open_pulse_logo = self.create_logo(ICON_DIR/ 'logos/OpenPulse_logo_gray.png')
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)
