from pathlib import Path

import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.pickers import CellAreaPicker, CellPropertyAreaPicker
from molde.render_widgets import CommonRenderWidget

from ._mesh_picker import MeshPicker
from ._model_info_text import nodes_info_text, elements_info_text, entity_info_text

from pulse.interface.viewer_3d.actors import ElementLinesActor, NodesActor, TubeActorGPU
from pulse.interface.viewer_3d.actors.tube_actor import ColorMode
from pulse.interface.viewer_3d.actors.acoustic_symbols_actor import (
    AcousticElementsSymbolsActor,
    AcousticNodesSymbolsActor,
)
from pulse.interface.viewer_3d.actors.structural_symbols_actor import (
    StructuralElementsSymbolsActor,
    StructuralNodesSymbolsActor,
)
from molde.utils import TreeInfo, format_long_sequence
from pulse import app, ICON_DIR
from pulse.interface.utils import PlotFilter, SelectionFilter

class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)

        app().main_window.theme_changed.connect(self.set_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)
        app().main_window.selection_changed.connect(self.update_selection)
        
        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)
        self.mesh_picker = MeshPicker(self)

        self.open_pulse_logo = None
        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

        self.selected_nodes = set()
        self.selected_lines = set()
        self.selected_elements = set()

        self.create_axes()
        self.create_scale_bar()
        self.create_logos()
        self.set_theme("light")
        self.create_camera_light(0.1, 0.1)

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.mesh_picker.update_bounds()
        project = app().project

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActorGPU(project)

        # TODO: Replace these actors for newer ones that
        # are lighter and easier to update
        self._acoustic_nodes_symbols = AcousticNodesSymbolsActor(project)
        self._acoustic_elements_symbols = AcousticElementsSymbolsActor(project)
        self._structural_nodes_symbols = StructuralNodesSymbolsActor(project)
        self._structural_elements_symbols = StructuralElementsSymbolsActor(project)
        self._acoustic_nodes_symbols.build()
        self._acoustic_elements_symbols.build()
        self._structural_nodes_symbols.build()
        self._structural_elements_symbols.build()
        self.acoustic_nodes_symbols_actor = self._acoustic_nodes_symbols.getActor()
        self.acoustic_elements_symbols_actor = self._acoustic_elements_symbols.getActor()
        self.structural_nodes_symbols_actor = self._structural_nodes_symbols.getActor()
        self.structural_elements_symbols_actor = self._structural_elements_symbols.getActor()

        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.tubes_actor)
        self.renderer.AddActor(self.acoustic_nodes_symbols_actor)
        self.renderer.AddActor(self.acoustic_elements_symbols_actor)
        self.renderer.AddActor(self.structural_nodes_symbols_actor)
        self.renderer.AddActor(self.structural_elements_symbols_actor)

        self.visualization_changed_callback()
        if reset_camera:
            self.renderer.ResetCamera()
        self.update_info_text()

    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.acoustic_nodes_symbols_actor)
        self.renderer.RemoveActor(self.acoustic_elements_symbols_actor)
        self.renderer.RemoveActor(self.structural_nodes_symbols_actor)
        self.renderer.RemoveActor(self.structural_elements_symbols_actor)

        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

    def visualization_changed_callback(self):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
        self.nodes_actor.SetVisibility(visualization.nodes)
        self.lines_actor.SetVisibility(visualization.lines)
        self.tubes_actor.SetVisibility(visualization.tubes)
        opacity = 0.9 if visualization.transparent else 1
        self.tubes_actor.GetProperty().SetOpacity(opacity)
        self.update()

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
            self.nodes_actor,
            self.lines_actor,
            self.tubes_actor,
            self.acoustic_nodes_symbols_actor,
            self.acoustic_elements_symbols_actor,
            self.structural_nodes_symbols_actor,
            self.structural_elements_symbols_actor,
        ]
        return all([actor is not None for actor in actors])

    def set_theme(self, theme):
        super().set_theme(theme)

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.open_pulse_logo = self.create_logo(ICON_DIR/ 'logos/OpenPulse_logo_gray.png')
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x1, y1):
        if not self._actor_exists():
            return

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x1 - x0) > 10) or (abs(y1 - y0) > 10)
        selection_filter = app().main_window.selection_filter

        picked_nodes = set()
        picked_elements = set()
        picked_lines = set()


        if mouse_moved:
            if selection_filter.nodes:
                picked_nodes = self.mesh_picker.area_pick_nodes(x0, y0, x1, y1)

            if selection_filter.elements:
                picked_elements = self.mesh_picker.area_pick_elements(x0, y0, x1, y1)

            if selection_filter.lines:
                picked_lines = self.mesh_picker.area_pick_entities(x0, y0, x1, y1)

        else:
            if selection_filter.nodes:
                picked_nodes = set([self.mesh_picker.pick_node(x1, y1)])
                picked_nodes.difference_update([-1])  # remove -1 index

            if selection_filter.elements:
                picked_elements = set([self.mesh_picker.pick_element(x1, y1)])
                picked_elements.difference_update([-1])  # remove -1 index

            if selection_filter.lines:
                picked_lines = set([self.mesh_picker.pick_entity(x1, y1)])
                picked_lines.difference_update([-1])  # remove -1 index

        # give priority to node selection
        if picked_nodes and not mouse_moved:
            picked_lines.clear()
            picked_elements.clear()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        app().main_window.set_selection(
            nodes=picked_nodes,
            lines=picked_lines,
            elements=picked_elements,
            join=ctrl_pressed | shift_pressed,
            remove=alt_pressed,   
        )

    def update_selection(self):
        self.nodes_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.tubes_actor.clear_colors()

        nodes = app().main_window.selected_nodes
        lines = app().main_window.selected_lines
        elements = app().main_window.selected_elements

        self.nodes_actor.set_color((255, 50, 50), nodes)
        self.lines_actor.set_color((200, 0, 0), elements, lines)
        self.tubes_actor.set_color((255, 0, 50), elements, lines)
        self.update_info_text()
        self.update()

    def update_info_text(self):
        info_text = ""
        info_text += nodes_info_text()
        info_text += elements_info_text()
        info_text += entity_info_text()
        self.set_info_text(info_text)
