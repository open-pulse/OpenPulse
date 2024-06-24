from dataclasses import dataclass
from pathlib import Path
from enum import Enum, auto

from PyQt5.QtWidgets import QApplication
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from vtkat.render_widgets import AnimatedRenderWidget


from pulse.interface.viewer_3d.actors import TubeActorGPU
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable
from pulse.interface.viewer_3d.text_helppers import TreeInfo, format_long_sequence
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
        
        # self.interactor_style = BoxSelectionInteractorStyle()
        # self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.open_pulse_logo = None
        self.tubes_actor = None

        self.current_frequency_index = 0
        self.current_phase_step = 0
        self._result_min = 0
        self._result_max = 0
        self.u_def = []

        self.analysis_mode = AnalysisMode.EMPTY
        self.colormap = "viridis"

        self.create_axes()
        self.create_scale_bar()
        self.create_color_bar()
        self.create_logos()
        self.set_theme("light")
        self.create_camera_light(0.1, 0.1)

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.create_logos()

        project = app().project

        # update the data according to the current analysis
        if self.analysis_mode == AnalysisMode.DISPLACEMENT:
            color_table = self._compute_displacement_field(self.current_frequency_index, self.current_phase_step)

        elif self.analysis_mode == AnalysisMode.STRESS:
            color_table = self._compute_stress_field(self.current_frequency_index, self.current_phase_step)

        elif self.analysis_mode == AnalysisMode.PRESURE:
            color_table = self._compute_pressure_field(self.current_frequency_index, self.current_phase_step)

        else:
            # Empty color table
            color_table = ColorTable(project, [], [0, 0], self.colormap)


        self.tubes_actor = TubeActorGPU(project)

        self.renderer.AddActor(self.tubes_actor)

        self.colorbar_actor.SetLookupTable(color_table)
        self.tubes_actor.set_color_table(color_table)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()
    
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

    def remove_actors(self):
        self.renderer.RemoveActor(self.tubes_actor)
        self.tubes_actor = None

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
            stress_field_plot=True,   
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
