# fmt: off
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from pulse import app, ICON_DIR
from pulse.interface.viewer_3d.actors import SectionPlaneActor, ElementAxesActor, ElementLinesActor, NodesActor, PointsActor, TubeActor

from molde.colors import Color
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import CommonRenderWidget

from pulse import ICON_DIR, app
from pulse.interface.viewer_3d.actors import (
    ElementAxesActor,
    ElementLinesActor,
    NodesActor,
    PointsActor,
    SectionPlaneActor,
    VariableSymbolsActor,
    FixedSymbolsActor,
    TubeActor,
)

from ._mesh_picker import MeshPicker
from ._model_info_text import elements_info_text, lines_info_text, nodes_info_text


class MeshRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.set_interactor_style(BoxSelectionInteractorStyle())
        self.mesh_picker = MeshPicker(self)

        self.remove_all_actors()

        self.selected_nodes = set()
        self.selected_lines = set()
        self.selected_elements = set()

        self.mouse_click = (0, 0)

        self.create_axes()
        self.create_logos()
        self.create_scale_bar()
        self.apply_user_preferences()
        self.create_camera_light(0.1, 0.1)
        self._create_connections()

    def _create_connections(self):
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)

        app().main_window.theme_changed.connect(self.set_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)
        app().main_window.selection_changed.connect(self.update_selection)
        app().main_window.section_plane.value_changed_2.connect(self.update_section_plane)

    def update_plot(self, reset_camera=False):
        self.remove_all_actors()
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

        self.symbols_actor = VariableSymbolsActor(self.renderer)
        self.symbols_actor_fixed = FixedSymbolsActor()

        self.add_actors(
            self.lines_actor,
            self.points_actor,
            self.nodes_actor,
            self.tubes_actor,
            self.element_axes_actor,
            self.plane_actor,
            self.symbols_actor,
            self.symbols_actor_fixed,
        )

        # Prevents uneeded update calls
        with self.update_lock:
            self.visualization_changed_callback()
            self.update_section_plane()

            if reset_camera:
                self.renderer.ResetCamera()

            self.update_info_text()

        self.update_theme()
        self.update()

    def remove_all_actors(self):
        super().remove_all_actors()

        self.nodes_actor = None
        self.points_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.element_axes_actor = None
        self.symbols_actor = None
        self.symbols_actor_fixed = None

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

        self.symbols_actor.SetVisibility(visualization.structural_symbols)
        self.symbols_actor_fixed.SetVisibility(visualization.structural_symbols)

        # To update default, material or fluid visualization
        self.tubes_actor.clear_colors()

        self.update()

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
            self.lines_actor,
            self.tubes_actor,
        ]
        return all([actor is not None for actor in actors])

    def set_theme(self, *args, **kwargs):
        """It's necessary because if this function doesn't exist
        CommomRenderWidget will call it's own set_theme function in
        it's constructor"""

        self.update_theme()

    def update_theme(self):
        user_preferences = app().main_window.config.user_preferences
        bkg_1 = user_preferences.renderer_background_color_1
        bkg_2 = user_preferences.renderer_background_color_2
        font_color = user_preferences.renderer_font_color

        if bkg_1 is None:
            raise ValueError('Missing value "bkg_1"')
        if bkg_2 is None:
            raise ValueError('Missing value "bkg_2"')
        if font_color is None:
            raise ValueError('Missing value "font_color"')

        self.renderer.GradientBackgroundOn()
        self.renderer.SetBackground(bkg_1.to_rgb_f())
        self.renderer.SetBackground2(bkg_2.to_rgb_f())

        if hasattr(self, "text_actor"):
            self.text_actor.GetTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "colorbar_actor"):
            self.colorbar_actor.GetTitleTextProperty().SetColor(font_color.to_rgb_f())
            self.colorbar_actor.GetLabelTextProperty().SetColor(font_color.to_rgb_f())

        if hasattr(self, "scale_bar_actor"):
            self.scale_bar_actor.GetLegendTitleProperty().SetColor(font_color.to_rgb_f())
            self.scale_bar_actor.GetLegendLabelProperty().SetColor(font_color.to_rgb_f())

    def create_logos(self):
        if app().main_window.config.user_preferences.interface_theme == "light":
            path = ICON_DIR / "logos/OpenPulse_logo_gray.png"
        else:
            path = ICON_DIR / "logos/OpenPulse_logo_white.png"

        if hasattr(self, "open_pulse_logo"):
            self.renderer.RemoveViewProp(self.open_pulse_logo)

        self.open_pulse_logo = self.create_logo(path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def apply_user_preferences(self):
        self.update_open_pulse_logo_visibility()
        self.update_scale_bar_visibility()
        self.update_renderer_font_size()

    def update_renderer_font_size(self):
        user_preferences = app().main_window.config.user_preferences
        font_size_px = int(user_preferences.renderer_font_size * 4 / 3)

        info_text_property = self.text_actor.GetTextProperty()
        info_text_property.SetFontSize(font_size_px)

        scale_bar_title_property = self.scale_bar_actor.GetLegendTitleProperty()
        scale_bar_label_property = self.scale_bar_actor.GetLegendLabelProperty()
        scale_bar_title_property.SetFontSize(font_size_px)
        scale_bar_label_property.SetFontSize(font_size_px)

    def update_open_pulse_logo_visibility(self):
        user_preferences = app().config.user_preferences

        if user_preferences.show_open_pulse_logo:
            self.enable_open_pulse_logo()
        else:
            self.disable_open_pulse_logo()

    def enable_open_pulse_logo(self):
        self.open_pulse_logo.VisibilityOn()

    def disable_open_pulse_logo(self):
        self.open_pulse_logo.VisibilityOff()

    def update_scale_bar_visibility(self):
        user_preferences = app().config.user_preferences

        if user_preferences.show_reference_scale_bar:
            self.enable_scale_bar()
        else:
            self.disable_scale_bar()

    def enable_scale_bar(self):
        self.scale_bar_actor.VisibilityOn()

    def disable_scale_bar(self):
        self.scale_bar_actor.VisibilityOff()

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
            join=ctrl_pressed or shift_pressed,
            remove=ctrl_pressed or alt_pressed,
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
