from dataclasses import dataclass
from pathlib import Path
from enum import Enum, auto
import numpy as np

from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from vtkat.render_widgets import AnimatedRenderWidget

from ._mesh_picker import MeshPicker
from pulse.interface.viewer_3d.actors import TubeActorGPU, NodesActor, ElementLinesActor, CuttingPlaneActor
from pulse.interface.viewer_3d.coloring.color_table import ColorTable
from pulse.interface.viewer_3d.text_helppers import TreeInfo, format_long_sequence
from pulse.interface.utils import rotation_matrices
from pulse.postprocessing.plot_structural_data import (
    get_structural_response,
    get_stresses_to_plot,
    get_min_max_stresses_values,
    get_min_max_resultant_displacements,
)
from pulse.postprocessing.plot_acoustic_data import (
    get_max_min_values_of_pressures,
    get_acoustic_response,
)
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

class AnalysisMode(Enum):
    EMPTY = auto()
    STRESS = auto()
    PRESURE = auto()
    DISPLACEMENT = auto()


class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        app().main_window.theme_changed.connect(self.set_theme)
        app().main_window.visualization_changed.connect(self.visualization_changed_callback)

        self.renderer.SetUseDepthPeeling(True)  # dont't remove, transparency depends on it

        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)
        self.mesh_picker = MeshPicker(self)

        self.open_pulse_logo = None
        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.plane_actor = None

        self.current_frequency_index = 0
        self.current_phase_step = 0
        self._result_min = 0
        self._result_max = 0
        self.u_def = []

        self.cutting_plane_active = False
        self.transparency = 0
        self.plane_origin = (0, 0, 0)
        self.plane_normal = (1, 0, 0)
        self.config_tube_args = (0, 0, 0, 0, 0, 0)

        self.analysis_mode = AnalysisMode.EMPTY
        self.colormap = "viridis"

        self.create_axes()
        self.create_scale_bar()
        self.create_color_bar()
        self.create_logos()
        self.set_theme("light")
        self.create_camera_light(0.1, 0.1)

    def create_logos(self, theme="light"):
        self.renderer.RemoveViewProp(self.open_pulse_logo)
        self.open_pulse_logo = self.create_logo(ICON_DIR/ 'logos/OpenPulse_logo_gray.png')
        self.open_pulse_logo.SetPosition(0.845, 0.89)
        self.open_pulse_logo.SetPosition2(0.15, 0.15)

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.mesh_picker.update_bounds()
        project = app().project

        try:
            # update the data according to the current analysis
            deformed = False
            if self.analysis_mode == AnalysisMode.DISPLACEMENT:
                deformed = True
                color_table = self._compute_displacement_field(self.current_frequency_index, self.current_phase_step)

            elif self.analysis_mode == AnalysisMode.STRESS:
                color_table = self._compute_stress_field(self.current_frequency_index, self.current_phase_step)

            elif self.analysis_mode == AnalysisMode.PRESURE:
                color_table = self._compute_pressure_field(self.current_frequency_index, self.current_phase_step)

            else:
                # Empty color table
                color_table = ColorTable(project, [], [0, 0], self.colormap)

        except Exception as e:
            return 

        self.nodes_actor = NodesActor(project)
        self.lines_actor = ElementLinesActor(project)
        self.tubes_actor = TubeActorGPU(project, show_deformed=deformed)
        self.plane_actor = CuttingPlaneActor(size=self._get_plane_size())
        self.plane_actor.VisibilityOff()

        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.tubes_actor)
        self.renderer.AddActor(self.plane_actor)

        self.colorbar_actor.SetLookupTable(color_table)
        self.tubes_actor.set_color_table(color_table)

        if self.cutting_plane_active:
            self.configure_cutting_plane(*self.config_tube_args)
            self.apply_cutting_plane()
        self.set_tube_actors_transparency(self.transparency)

        if reset_camera:
            self.renderer.ResetCamera()
        self.visualization_changed_callback()

    def set_colormap(self, colormap):
        self.colormap = colormap
        self.update_plot()

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

    def slider_callback(self, phase_deg):        
        self.current_phase_step = phase_deg * (2 * np.pi / 360)
        self.update_plot()

    def show_empty(self, *args, **kwargs):
        pass

    def show_displacement_field(self, frequency_index):
        solution = app().main_window.project.get_structural_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.DISPLACEMENT

        self._reset_min_max_values()
        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

        self.update_plot()

    def show_stress_field(self, frequency_index):
        solution = app().main_window.project.get_structural_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.STRESS

        self._reset_min_max_values()
        self.stress_min, self.stress_max = get_min_max_stresses_values()
        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

        self.update_plot()

    def show_pressure_field(self, frequency_index):
        solution = app().main_window.project.get_acoustic_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.PRESURE

        self._reset_min_max_values()
        tmp = get_max_min_values_of_pressures(solution, frequency_index)
        self.pressure_min, self.pressure_max = tmp

        self.update_plot()

    def set_tube_actors_transparency(self, transparency):
        self.transparency = transparency
        opacity = 1 - transparency
        self.tubes_actor.GetProperty().SetOpacity(opacity)
        self.update()

    def configure_cutting_plane(self, x, y, z, rx, ry, rz):
        self.tubes_actor.disable_cut()
        self.config_tube_args = x, y, z, rx, ry, rz

        self.plane_origin = self._calculate_relative_position([x, y, z])
        self.plane_normal = self._calculate_normal_vector([rx, ry, rz])
        self.plane_actor.SetPosition(self.plane_origin)
        self.plane_actor.SetOrientation(rx, ry, rz)
        self.plane_actor.GetProperty().SetOpacity(0.9)
        self.plane_actor.VisibilityOn()
        self.update()

    def apply_cutting_plane(self):
        if self.plane_origin is None:
            return

        if self.plane_normal is None:
            return

        self.cutting_plane_active = True
        self.tubes_actor.apply_cut(self.plane_origin, self.plane_normal)
        self.plane_actor.GetProperty().SetOpacity(0.2)
        self.plane_actor.VisibilityOn()
        self.update()
    
    def dismiss_cutting_plane(self):
        if not self._actor_exists():
            return
        
        self.cutting_plane_active = False
        self.tubes_actor.disable_cut()
        self.plane_actor.VisibilityOff()
        self.update()

    def remove_actors(self):
        self.renderer.RemoveActor(self.nodes_actor)
        self.renderer.RemoveActor(self.lines_actor)
        self.renderer.RemoveActor(self.tubes_actor)
        self.renderer.RemoveActor(self.plane_actor)
        self.nodes_actor = None
        self.lines_actor = None
        self.tubes_actor = None
        self.plane_actor = None

    def _actor_exists(self):
        actors = [
            self.nodes_actor,
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
            phase_step = phase_step,
            r_max = self.r_xyz_abs
        )

        color_table = ColorTable(
            project,
            u_def,
            (self.result_disp_min, self.result_disp_max),
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
            phase_step = phase_step,
            r_max = self.r_xyz_abs
        )

        stresses_data, self.min_max_stresses_values_current = get_stresses_to_plot(
            phase_step=phase_step
        )

        color_table = ColorTable(
            project,
            stresses_data,
            (self.stress_min, self.stress_max),
            self.colormap,
            stress_field_plot=True,   
        )
        return color_table


    def _compute_pressure_field(self, frequency_index, phase_step):
        project = app().project
        preprocessor = project.preprocessor
        solution = project.get_acoustic_solution()

        *_, pressure_field_data, self.min_max_pressures_values_current = get_acoustic_response(
            preprocessor,
            solution,
            frequency_index, 
            phase_step=phase_step
        )

        color_table = ColorTable(
            project,
            pressure_field_data,
            (self.pressure_min, self.pressure_max),
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

    def _get_plane_size(self):
        x0, x1, y0, y1, z0, z1 = self.tubes_actor.GetBounds()
        size = np.max(np.abs([x1-x0, y1-y0, z1-z0]))
        return size

    def _calculate_relative_position(self, position):
        def lerp(a, b, t):
           return a + (b - a) * t

        if not self._actor_exists():
            return       
        
        bounds = self.tubes_actor.GetBounds()
        x = lerp(bounds[0], bounds[1], position[0] / 100)
        y = lerp(bounds[2], bounds[3], position[1] / 100)
        z = lerp(bounds[4], bounds[5], position[2] / 100)
        return np.array([x, y, z])
    
    def _calculate_normal_vector(self, orientation):
        orientation = np.array(orientation) * np.pi / 180
        rx, ry, rz = rotation_matrices(*orientation)

        normal = rz @ rx @ ry @ np.array([1, 0, 0, 1])
        return -normal[:3]
