from dataclasses import dataclass
from pathlib import Path
from enum import Enum, auto

from PyQt5.QtWidgets import QApplication
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from vtkat.render_widgets import AnimatedRenderWidget


from pulse.interface.viewer_3d.actors import TubeActorDeformed
from pulse.interface.viewer_3d.coloring.colorTable import ColorTable
from pulse.interface.viewer_3d.text_helppers import TreeInfo, format_long_sequence
from pulse.postprocessing.plot_structural_data import get_structural_response, get_min_max_resultant_displacements
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
        self.result_disp_min = 0
        self.result_disp_max = 0
        self.u_def = []

        self.analysis_mode = AnalysisMode.EMPTY
        self.colormap = "viridis"

        self.create_axes()
        self.create_scale_bar()
        self.create_color_bar()
        self.create_logos()
        self.set_theme("light")

    def update_plot(self, reset_camera=False):
        self.remove_actors()
        self.create_logos()

        project = app().project

        # update the data according to 
        if self.analysis_mode == AnalysisMode.DISPLACEMENT:
            self._compute_displacement_field(self.current_frequency_index, self.current_phase_step)

        self.tubes_actor = TubeActorDeformed(project)

        self.renderer.AddActor(self.tubes_actor)

        color_table = ColorTable(project, self.u_def, [self.result_disp_min, self.result_disp_max], self.colormap)
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

        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

        self.update_plot()

    def show_stress_field(self, frequency_index):
        pass

    def show_pressure_field(self, frequency_index):
        pass

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
        _, _, self.u_def, self._magnification_factor = get_structural_response(
            preprocessor,
            solution,
            frequency_index, 
            phase_step = phase_step,
            r_max = self.r_xyz_abs
        )


        # if self.clipping_plane_active:
        #     self.opvClippableDeformedTubes.build()
        #     self.opvClippableDeformedTubes.setColorTable(colorTable)
        #     self.opvClippableDeformedTubes.apply_cut(self.plane_origin, self.plane_normal)