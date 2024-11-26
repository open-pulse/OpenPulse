from enum import Enum, auto
import logging
import numpy as np
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.render_widgets import AnimatedRenderWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from vtkmodules.vtkCommonDataModel import vtkPolyData

from pulse import ICON_DIR, app
from pulse.interface.utils import rotation_matrices
from pulse.interface.viewer_3d.actors import (
    SectionPlaneActor,
    ElementLinesActor,
    NodesActor,
    PointsActor,
    TubeActorResults,
)
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.viewer_3d.coloring.color_table import ColorTable
from pulse.postprocessing.plot_acoustic_data import (
    get_acoustic_response,
    get_max_min_values_of_pressures,
)
from pulse.postprocessing.plot_structural_data import (
    get_min_max_resultant_displacements,
    get_min_max_stresses_values,
    get_stresses_to_plot,
    get_structural_response,
)

from ._mesh_picker import MeshPicker
from ._model_info_text import (
    analysis_info_text,
    elements_info_text,
    lines_info_text,
    nodes_info_text,
    min_max_stresses_info_text,
)


class AnalysisMode(Enum):
    EMPTY = auto()
    STRESS = auto()
    PRESURE = auto()
    DISPLACEMENT = auto()


class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # dont't remove, transparency depends on it
        self.renderer.SetUseDepthPeeling(
            True
        )

        self.set_interactor_style(BoxSelectionInteractorStyle())
        self.mesh_picker = MeshPicker(self)

        self.open_pulse_logo = None
        self.nodes_actor = None
        self.points_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.plane_actor = None

        self.current_frequency_index = 0
        self.current_phase_step = 0
        self._result_min = 0
        self._result_max = 0

        self._animation_color_map = None
        self._animation_current_frequency = None
        self._animation_cached_data = dict()

        self.transparency = 0
        self.mouse_click = (0, 0)

        self.analysis_mode = AnalysisMode.EMPTY
        self.colormap = app().config2.user_preferences.color_map
        self.create_axes()
        self.create_scale_bar()
        self.create_logos()
        self.create_color_bar()
        self.update_renderer_font_size()
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

        try:

            # Default behavior
            self.colorbar_actor.VisibilityOn()
            deformed = False
    
            unit_label = ""
            analysis_id = project.analysis_id

            # update the data according to the current analysis
            if self.analysis_mode == AnalysisMode.DISPLACEMENT:

                if analysis_id in [0, 1, 5, 6, 7]:
                    unit_label = "Unit: [m]"
                elif analysis_id in [2]:
                    unit_label = "Unit: [--]"

                deformed = True
                color_table = self._compute_displacement_field(
                    self.current_frequency_index, self.current_phase_step
                )

            elif self.analysis_mode == AnalysisMode.STRESS:

                if analysis_id in [0, 1, 5, 6, 7]:
                    unit_label = "Unit: [Pa]"

                deformed = True
                color_table = self._compute_stress_field(
                    self.current_frequency_index, self.current_phase_step
                )

            elif self.analysis_mode == AnalysisMode.PRESURE:

                if analysis_id in [3, 5, 6]:
                    unit_label = "Unit: [Pa]"
                elif analysis_id in [4]:
                    unit_label = "Unit: [--]"

                color_table = self._compute_pressure_field(
                    self.current_frequency_index, self.current_phase_step
                )

            else:
                # Empty color table
                color_table = ColorTable([], [0, 0], self.colormap)
                self.colorbar_actor.VisibilityOff()

        except Exception as error_log:
            print(str(error_log))
            return

        acoustic_plot = (self.analysis_mode == AnalysisMode.PRESURE)

        self.lines_actor = ElementLinesActor(show_deformed=deformed)
        self.nodes_actor = NodesActor(show_deformed=deformed)
        self.points_actor = PointsActor(show_deformed=deformed)
        self.tubes_actor = TubeActorResults(show_deformed=deformed, acoustic_plot=acoustic_plot)
        self.plane_actor = SectionPlaneActor(self.tubes_actor.GetBounds())
        self.plane_actor.VisibilityOff()

        self.add_actors(
            self.lines_actor,
            self.nodes_actor,
            self.points_actor,
            self.tubes_actor,
            self.plane_actor,
        )

        self.colorbar_actor.SetTitle(unit_label)
        self.colorbar_actor.SetLookupTable(color_table)
        self.tubes_actor.set_color_table(color_table)

        self.visualization_changed_callback(update=False)
        self.update_section_plane()

        if reset_camera:
            self.renderer.ResetCamera()

        self.update_info_text()
        self.update_theme()
        self.update()

        # It needs to appear after the update to work propperly
        self.set_tube_actors_transparency(self.transparency)

    def set_colormap(self, colormap):
        app().config2.user_preferences.color_map = colormap
        self.colormap = colormap
        self.update_plot()

        app().config2.update_config_file()

    def cache_animation_frames(self):
        self._animation_current_frequency = self.current_frequency_index
        self._animation_color_map = self.colormap

        with self.update_lock:
            for frame in range(self._animation_total_frames):
                logging.info(f"Caching animation frames [{frame}/{self._animation_total_frames}]")
                d_theta = 2 * np.pi / self._animation_total_frames
                phase_step = frame * d_theta
                self.current_phase_step = phase_step

                self.update_plot()
                cached = vtkPolyData()
                cached.DeepCopy(self.tubes_actor.GetMapper().GetInput())
                self._animation_cached_data[frame] = cached
        self._animation_current_cycle = 0

    def stop_animation(self):
        # Do the things defined in the mother class 
        super().stop_animation()
        # Change the animation button to paused
        app().main_window.animation_toolbar.pause_animation()

    def clear_cache(self):
        self._animation_cached_data.clear()

    def update_animation(self, frame: int):
        if self.analysis_mode == AnalysisMode.EMPTY:
            self.stop_animation()
            return

        conditions_to_clear_cache = [
            self._animation_current_frequency != self.current_frequency_index,
            self._animation_color_map != self.colormap,
        ]

        if any(conditions_to_clear_cache):
            self.clear_cache()

        if not self._animation_cached_data:
            LoadingWindow(self.cache_animation_frames).run()

        if frame in self._animation_cached_data:
            logging.info(f"Rendering animation frame [{frame}/{self._animation_total_frames}]")
            cached = self._animation_cached_data[frame]
            self.tubes_actor.GetMapper().SetInputData(cached)
            self.update()
        else:
            # It will only enter here if something wrong happened
            # in the function that caches the frames
            logging.warn(f"Cache miss on update_animation function for frame {frame}")
            d_theta = 2 * np.pi / self._animation_total_frames
            phase_step = frame * d_theta
            self.current_phase_step = phase_step

            self.update_plot()
            cached = vtkPolyData()
            cached.DeepCopy(self.tubes_actor.GetMapper().GetInput())
            self._animation_cached_data[frame] = cached

    def visualization_changed_callback(self, update=True):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
        self.points_actor.SetVisibility(visualization.points)
        self.nodes_actor.SetVisibility(visualization.nodes)
        self.lines_actor.SetVisibility(visualization.lines)
        self.tubes_actor.SetVisibility(visualization.tubes)
        opacity = 0.9 if visualization.transparent else 1
        self.tubes_actor.GetProperty().SetOpacity(opacity)
        if update:
            self.update()

    def slider_callback(self, phase_deg):
        self.current_phase_step = phase_deg * (2 * np.pi / 360)
        self.update_plot()

    def show_empty(self, *args, **kwargs):
        self.analysis_mode = AnalysisMode.EMPTY
        self.current_frequency_index = 0
        self.current_phase_step = 0
        self.clear_cache()
        self.update_plot()

    def show_displacement_field(self, frequency_index):

        solution = app().project.get_structural_solution()
        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.DISPLACEMENT

        self._reset_min_max_values()
        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

        self.clear_cache()
        self.update_plot()

    def show_stress_field(self, frequency_index):
        solution = app().project.get_structural_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.STRESS

        self._reset_min_max_values()
        self.stress_min, self.stress_max = get_min_max_stresses_values()
        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

        self.clear_cache()
        self.update_plot()

    def show_pressure_field(self, frequency_index):
        solution = app().project.get_acoustic_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.PRESURE

        self._reset_min_max_values()
        tmp = get_max_min_values_of_pressures(solution, frequency_index)
        self.pressure_min, self.pressure_max = tmp

        self.clear_cache()
        self.update_plot()

    def set_tube_actors_transparency(self, transparency):
        self.transparency = transparency
        opacity = 1 - transparency
        self.tubes_actor.GetProperty().SetOpacity(opacity)
        self.update()

    def set_theme(self, *args, **kwargs):
        """ It's necessary because if this function doesn't exist
            CommomRenderWidget will call it's own set_theme function in
            it's constructor """

        self.update_theme()

    def update_theme(self):
        user_preferences = app().main_window.config2.user_preferences
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
        if app().main_window.config2.user_preferences.interface_theme == "light":
            path = ICON_DIR / "logos/OpenPulse_logo_gray.png"
        else:
            path = ICON_DIR / "logos/OpenPulse_logo_white.png"

        if hasattr(self, "open_pulse_logo"):
            self.renderer.RemoveViewProp(self.open_pulse_logo)

        self.open_pulse_logo = self.create_logo(path)
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def update_renderer_font_size(self):
        user_preferences = app().main_window.config2.user_preferences
        font_size_px = int(user_preferences.renderer_font_size * 4/3)

        info_text_property = self.text_actor.GetTextProperty()
        info_text_property.SetFontSize(font_size_px)

        scale_bar_title_property = self.scale_bar_actor.GetLegendTitleProperty()
        scale_bar_label_property = self.scale_bar_actor.GetLegendLabelProperty()
        scale_bar_title_property.SetFontSize(font_size_px)
        scale_bar_label_property.SetFontSize(font_size_px)
    
    def enable_open_pulse_logo(self):
        self.open_pulse_logo.VisibilityOn()

    def disable_open_pulse_logo(self):
        self.open_pulse_logo.VisibilityOff()
    
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
        visualization_filter = app().main_window.visualization_filter
        selection_filter = app().main_window.selection_filter

        picked_nodes = set()
        picked_elements = set()
        picked_lines = set()

        if mouse_moved:
            if selection_filter.nodes:
                picked_nodes = self.mesh_picker.area_pick_nodes(x0, y0, x1, y1)

            if selection_filter.elements and visualization_filter.lines:
                picked_elements = self.mesh_picker.area_pick_elements(x0, y0, x1, y1)

            if selection_filter.lines and visualization_filter.lines:
                picked_lines = self.mesh_picker.area_pick_lines(x0, y0, x1, y1)

        else:
            if selection_filter.nodes:
                picked_nodes = set([self.mesh_picker.pick_node(x1, y1)])
                picked_nodes.difference_update([-1])

            if selection_filter.elements and visualization_filter.lines:
                picked_elements = set([self.mesh_picker.pick_element(x1, y1)])
                picked_elements.difference_update([-1])

            if selection_filter.lines and visualization_filter.lines:
                picked_lines = set([self.mesh_picker.pick_entity(x1, y1)])
                picked_lines.difference_update([-1])

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

        nodes = app().main_window.selected_nodes
        lines = app().main_window.selected_lines
        elements = app().main_window.selected_elements

        self.points_actor.set_color((255, 50, 50), nodes)
        self.nodes_actor.set_color((255, 50, 50), nodes)
        self.lines_actor.set_color((200, 0, 0), elements, lines)

        self.update_info_text()
        self.update()

    def update_info_text(self):
        if self.analysis_mode == AnalysisMode.EMPTY:
            self.set_info_text("")
            return

        info_text = ""
        info_text += analysis_info_text(self.current_frequency_index)
        info_text += nodes_info_text()
        info_text += elements_info_text()
        info_text += lines_info_text()

        if self.analysis_mode == AnalysisMode.STRESS:
            info_text += min_max_stresses_info_text()

        self.set_info_text(info_text)

    def remove_actors(self):
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.points_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.nodes_actor = None
        self.points_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.plane_actor = None

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
            self.points_actor,
            self.lines_actor,
            self.tubes_actor,
            self.plane_actor,
        ]
        return all([actor is not None for actor in actors])

    def _compute_displacement_field(self, frequency_index, phase_step):

        project = app().project
        preprocessor = project.preprocessor
        solution = project.get_structural_solution()

        # It is probably a bit unclear, but this function have some colateral
        # effects. It interprets the structural analysis and puts the meaningfull
        # data inside the correspondent nodes.
        # The return values are just extra information.
        _, _, u_def, self._magnification_factor = get_structural_response(
            preprocessor,
            solution,
            frequency_index,
            phase_step=phase_step,
            r_max=self.r_xyz_abs,
        )

        min_max_values = (self.result_disp_min, self.result_disp_max)
        color_table = ColorTable(
                                 u_def,
                                 min_max_values,
                                 self.colormap,
                                 )

        return color_table

    def _compute_stress_field(self, frequency_index, phase_step):
        project = app().project
        preprocessor = project.preprocessor
        solution = project.get_structural_solution()

        *_, self._magnification_factor = get_structural_response(
            preprocessor,
            solution,
            frequency_index,
            phase_step=phase_step,
            r_max=self.r_xyz_abs,
        )

        stresses_data, self.min_max_stresses_values_current = get_stresses_to_plot(
            phase_step=phase_step
        )

        min_max_values = (self.stress_min, self.stress_max)
        color_table = ColorTable(
                                 stresses_data,
                                 min_max_values,
                                 self.colormap,
                                 stress_field_plot = True,
                                 )

        return color_table

    def _compute_pressure_field(self, frequency_index, phase_step):

        project = app().project
        preprocessor = project.model.preprocessor
        solution = project.get_acoustic_solution()

        *_, pressure_field_data, self.min_max_pressures_values_current = (
            get_acoustic_response(
                preprocessor, solution, frequency_index, phase_step=phase_step
            )
        )

        min_max_values = (self.pressure_min, self.pressure_max)
        color_table = ColorTable(
                                 pressure_field_data,
                                 min_max_values,
                                 self.colormap,
                                 pressure_field_plot=True,
                                )

        return color_table

    def _reset_min_max_values(self):
        self.count_cycles = 0
        self.r_xyz_abs = None
        self.result_disp_min = None
        self.result_disp_max = None
        self.stress_min = None
        self.stress_max = None
        self.pressure_min = None
        self.pressure_max = None
        self.min_max_stresses_values_current = None
        self.min_max_pressures_values_current = None
        self.plot_state = [False, False, False]


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
