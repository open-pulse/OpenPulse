# fmt: off

import numpy as np
from pulse.interface.utils import rotation_matrices

from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget
from molde.colors import Color

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from pulse import ICON_DIR, app
from pulse.interface.viewer_3d.actors import SectionPlaneActor, ElementAxesActor, ElementLinesActor, NodesActor, PointsActor, TubeActor
from pulse.interface.viewer_3d.actors.acoustic_symbols_actor import AcousticElementsSymbolsActor, AcousticNodesSymbolsActor
from pulse.interface.viewer_3d.actors.structural_symbols_actor import StructuralElementsSymbolsActor, StructuralNodesSymbolsActor

from ._mesh_picker import MeshPicker
from ._model_info_text import elements_info_text, lines_info_text, nodes_info_text


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_interactor_style(BoxSelectionInteractorStyle())
        self.mesh_picker = MeshPicker(self)

        self.open_pulse_logo = None
        self.nodes_actor = None
        self.points_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.element_axes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None
        self.plane_actor = None

        self.selected_nodes = set()
        self.selected_lines = set()
        self.selected_elements = set()

        self.mouse_click = (0, 0)

        self.create_axes()
        self.create_scale_bar()
        self.set_theme("light")
        self.create_camera_light(0.1, 0.1)
        self._create_connections()

    def _create_connections(self):
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)

        app().main_window.theme_changed.connect(self.set_theme)
        app().main_window.visualization_changed.connect(
            self.visualization_changed_callback
        )
        app().main_window.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed_2.connect(self.update_section_plane)

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.mesh_picker.update_bounds()
        project = app().project

        if not project.get_structural_elements():
            return

        self.nodes_actor = NodesActor()
        self.lines_actor = ElementLinesActor()
        self.tubes_actor = TubeActor()
        self.points_actor = PointsActor()
        self.element_axes_actor = ElementAxesActor()
        self.element_axes_actor.VisibilityOff()
        self.plane_actor = SectionPlaneActor(self.tubes_actor.GetBounds())
        self.plane_actor.VisibilityOff()

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

        self.add_actors(
            self.lines_actor,
            self.points_actor,
            self.nodes_actor,
            self.tubes_actor,
            self.element_axes_actor,
            self.acoustic_nodes_symbols_actor,
            self.acoustic_elements_symbols_actor,
            self.structural_nodes_symbols_actor,
            self.structural_elements_symbols_actor,
            self.plane_actor
        )

        # Prevents uneeded update calls
        with self.update_lock:
            self.visualization_changed_callback()
            self.update_section_plane()        
        
            if reset_camera:
                self.renderer.ResetCamera()

            self.update_info_text()

        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.element_axes_actor)
        self.renderer.RemoveActor(self.acoustic_nodes_symbols_actor)
        self.renderer.RemoveActor(self.acoustic_elements_symbols_actor)
        self.renderer.RemoveActor(self.structural_nodes_symbols_actor)
        self.renderer.RemoveActor(self.structural_elements_symbols_actor)

        self.nodes_actor = None
        self.points_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.element_axes_actor = None
        self.acoustic_nodes_symbols_actor = None
        self.acoustic_elements_symbols_actor = None
        self.structural_nodes_symbols_actor = None
        self.structural_elements_symbols_actor = None

    def visualization_changed_callback(self):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
        self.points_actor.SetVisibility(visualization.points)
        self.nodes_actor.SetVisibility(visualization.nodes)
        self.lines_actor.SetVisibility(visualization.lines)
        self.tubes_actor.SetVisibility(visualization.tubes)
        opacity = 0.9 if visualization.transparent else 1
        self.tubes_actor.GetProperty().SetOpacity(opacity)

        self.acoustic_nodes_symbols_actor.SetVisibility(visualization.acoustic_symbols)
        self.acoustic_elements_symbols_actor.SetVisibility(visualization.acoustic_symbols)
        self.structural_nodes_symbols_actor.SetVisibility(visualization.structural_symbols)
        self.structural_elements_symbols_actor.SetVisibility(visualization.structural_symbols)

        # To update default, material or fluid visualization
        self.tubes_actor.clear_colors()

        self.update()

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
        self.create_logos(theme)

    def create_logos(self, theme="light"):
        if theme == "light":
            path = ICON_DIR / "logos/OpenPulse_logo_gray.png"
        else:
            path = ICON_DIR / "logos/OpenPulse_logo_white.png"

        if hasattr(self, "open_pulse_logo"):
            self.renderer.RemoveViewProp(self.open_pulse_logo)

        self.open_pulse_logo = self.create_logo(path)
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
        visualization_filter = app().main_window.visualization_filter

        picked_nodes = set()
        picked_elements = set()
        picked_lines = set()

        if mouse_moved:
            if selection_filter.nodes:
                picked_nodes = self.mesh_picker.area_pick_nodes(x0, y0, x1, y1)

            if selection_filter.elements:
                picked_elements = self.mesh_picker.area_pick_elements(x0, y0, x1, y1)

            if selection_filter.lines:
                picked_lines = self.mesh_picker.area_pick_lines(x0, y0, x1, y1)

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

        if visualization_filter.points:
            points_indexes = set(app().project.get_geometry_points().keys())
            picked_nodes.intersection_update(points_indexes)

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
        if not self._actor_exists():
            return

        self.points_actor.clear_colors()
        self.nodes_actor.clear_colors()
        self.lines_actor.clear_colors()
        self.tubes_actor.clear_colors()

        nodes = app().main_window.selected_nodes
        lines = app().main_window.selected_lines
        elements = app().main_window.selected_elements

        self.nodes_actor.set_color((255, 50, 50), nodes)
        self.points_actor.set_color((255, 50, 50), nodes)
        self.lines_actor.set_color((200, 0, 0), elements, lines)
        self.tubes_actor.set_color((255, 0, 50), elements, lines)

        # show element actor
        self.element_axes_actor.VisibilityOff()
        if len(elements) == 1:
            self.element_axes_actor.VisibilityOn()
            element_id, *_ = elements
            element = app().project.get_structural_element(element_id)
            self.element_axes_actor.position_from_element(element)

        self.update_info_text()
        self.update()

    def update_info_text(self):
        info_text = ""
        info_text += nodes_info_text()
        info_text += elements_info_text()
        info_text += lines_info_text()
        self.set_info_text(info_text)

    def update_section_plane(self):
        if not self._actor_exists():
            return

        section_plane = app().main_window.section_plane

        if not section_plane.cutting:
            self._disable_section_plane()
            return

        position = section_plane.get_position()
        rotation = section_plane.get_rotation()
        inverted = section_plane.get_inverted()

        if section_plane.editing:
            self.plane_actor.configure_section_plane(position, rotation)
            self.plane_actor.VisibilityOn()
            self.plane_actor.GetProperty().SetColor(0, 0.333, 0.867)
            self.plane_actor.GetProperty().SetOpacity(0.8)
            self.update()
        else:
            # not a very reliable condition, but it works
            show_plane = not section_plane.keep_section_plane
            self._apply_section_plane(position, rotation, inverted, show_plane)

    def _disable_section_plane(self):
        self.plane_actor.VisibilityOff()
        self.tubes_actor.disable_cut()
        self.update()

    def _apply_section_plane(self, position, rotation, inverted, show_plane=True):
        self.plane_actor.configure_section_plane(position, rotation)
        xyz = self.plane_actor.calculate_xyz_position(position)
        normal = self.plane_actor.calculate_normal_vector(rotation)
        if inverted:
            normal = -normal

        self.tubes_actor.apply_cut(xyz, normal)

        self.plane_actor.SetVisibility(show_plane)
        self.plane_actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.update()

# fmt: on