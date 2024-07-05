from dataclasses import dataclass
from enum import Enum, auto
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

import vtk
from molde.interactor_styles import BoxSelectionInteractorStyle
from molde.pickers import CellAreaPicker, CellPropertyAreaPicker
from molde.render_widgets import AnimatedRenderWidget
from molde.utils import TreeInfo, format_long_sequence

from ._mesh_picker import MeshPicker
from pulse.interface.viewer_3d.actors import TubeActorGPU, NodesActor, ElementLinesActor, CuttingPlaneActor
from pulse.interface.viewer_3d.coloring.color_table import ColorTable
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


class AnalysisMode(Enum):
    EMPTY = auto()
    STRESS = auto()
    PRESURE = auto()
    DISPLACEMENT = auto()


class ResultsRenderWidget(AnimatedRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mouse_click = (0, 0)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)

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

        self._animation_current_frequency = None
        self._animation_cached_data = dict()

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

        self.lines_actor = ElementLinesActor(project, show_deformed=deformed)
        self.nodes_actor = NodesActor(project, show_deformed=deformed)
        self.tubes_actor = TubeActorGPU(project, show_deformed=deformed)
        self.plane_actor = CuttingPlaneActor(size=self._get_plane_size())
        self.plane_actor.VisibilityOff()

        self.renderer.AddActor(self.lines_actor)
        self.renderer.AddActor(self.nodes_actor)
        self.renderer.AddActor(self.tubes_actor)
        self.renderer.AddActor(self.plane_actor)

        self.colorbar_actor.SetLookupTable(color_table)
        self.tubes_actor.set_color_table(color_table)

        self.visualization_changed_callback(update=False)
        if self.cutting_plane_active:
            self.configure_cutting_plane(*self.config_tube_args)
            self.apply_cutting_plane()
        self.set_tube_actors_transparency(self.transparency)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update_info_text()
        self.update()

    def set_colormap(self, colormap):
        self.colormap = colormap
        self.update_plot()

    def update_animation(self, frame: int):
        if self._animation_current_frequency != self.current_frequency_index:
            self._animation_cached_data.clear()
            self._animation_current_frequency = self.current_frequency_index

        d_theta = 2 * np.pi / self._animation_total_frames
        phase_step = frame * d_theta
        self.current_phase_step = phase_step

        if frame in self._animation_cached_data:
            cached = self._animation_cached_data[frame]
            self.tubes_actor.GetMapper().SetInputData(cached)
            self.update()
        else:
            self.update_plot()
            cached = vtk.vtkPolyData()
            cached.DeepCopy(self.tubes_actor.GetMapper().GetInput())
            self._animation_cached_data[frame] = cached

    def visualization_changed_callback(self, update=True):
        if not self._actor_exists():
            return

        visualization = app().main_window.visualization_filter
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
        pass

    def show_displacement_field(self, frequency_index):
        solution = app().project.get_structural_solution()

        self.current_frequency_index = frequency_index
        self.current_phase_step = 0
        self.analysis_mode = AnalysisMode.DISPLACEMENT

        self._reset_min_max_values()
        tmp = get_min_max_resultant_displacements(solution, frequency_index)
        _, self.result_disp_min, self.result_disp_max, self.r_xyz_abs = tmp

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

        self.update_plot()

    def show_pressure_field(self, frequency_index):
        solution = app().project.get_acoustic_solution()

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
        picked_entities = set()

        if mouse_moved:
            if selection_filter.nodes:
                picked_nodes = self.mesh_picker.area_pick_nodes(x0, y0, x1, y1)

            if selection_filter.elements and visualization_filter.lines:
                picked_elements = self.mesh_picker.area_pick_elements(x0, y0, x1, y1)
    
            if selection_filter.entities and visualization_filter.lines:
                picked_entities = self.mesh_picker.area_pick_entities(x0, y0, x1, y1)

        else:
            if selection_filter.nodes:
                picked_nodes = set([self.mesh_picker.pick_node(x1, y1)])
                picked_nodes.difference_update([-1])

            if selection_filter.elements and visualization_filter.lines:
                picked_elements = set([self.mesh_picker.pick_element(x1, y1)])
                picked_elements.difference_update([-1])
    
            if selection_filter.entities and visualization_filter.lines:
                picked_entities = set([self.mesh_picker.pick_entity(x1, y1)])
                picked_entities.difference_update([-1])

        # give priority to node selection
        if picked_nodes and not mouse_moved:
            picked_entities.clear()
            picked_elements.clear()

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        app().main_window.set_selection(
            nodes=picked_nodes,
            entities=picked_entities,
            elements=picked_elements,
            join=ctrl_pressed | shift_pressed,
            remove=alt_pressed,   
        )

        self.update_selection()

    def update_selection(self):
        self.nodes_actor.clear_colors()
        self.lines_actor.clear_colors()

        nodes = app().main_window.selected_nodes
        entities = app().main_window.selected_entities
        elements = app().main_window.selected_elements

        self.nodes_actor.set_color((255, 50, 50), nodes)
        self.lines_actor.set_color((200, 0, 0), elements, entities)

        self.update_info_text()

    def update_info_text(self):
        info_text = ""
        info_text += self._analysis_info_text()
        info_text += self._nodes_info_text()
        info_text += self._elements_info_text()
        info_text += self._entity_info_text()
        self.set_info_text(info_text)

    def _analysis_info_text(self):
        project = app().project

        tree = TreeInfo(project.analysis_type_label)
        if project.analysis_ID in [2, 4]:
            if project.analysis_type_label == "Structural Modal Analysis":
                frequencies = project.get_structural_natural_frequencies()
            
            if project.analysis_type_label == "Acoustic Modal Analysis":
                frequencies = project.get_acoustic_natural_frequencies()
            
            if frequencies is None:
                return ""

            mode = self.current_frequency_index + 1
            frequency = frequencies[self.current_frequency_index]
            tree.add_item("Mode", mode)
            tree.add_item("Natural Frequency", f"{frequency:.2f}", "Hz")
        else:
            frequencies = project.get_frequencies()
            if frequencies is None:
                return ""

            if project.analysis_method_label is not None:
                tree.add_item("Method", project.analysis_method_label)

            frequency = frequencies[self.current_frequency_index]
            tree.add_item("Frequency", f"{frequency:.2f}", "Hz")

        return str(tree)

    def _nodes_info_text(self):
        nodes = app().main_window.list_selected_nodes()
        info_text = ""
        if len(nodes) > 1:
            info_text += (
                f"{len(nodes)} NODES IN SELECTION\n"
                f"{format_long_sequence(nodes)}\n\n"
            )
        return info_text

    def _elements_info_text(self):
        elements = app().main_window.list_selected_elements()
        info_text = ""
        project = app().project

        if len(elements) == 1:
            _id, *_ = elements
            structural_element = project.get_structural_element(_id)

            first_node = structural_element.first_node
            last_node = structural_element.last_node

            tree = TreeInfo(f"ELEMENT {_id}")
            tree.add_item(
                f"First Node - {first_node.external_index:>5}",
                "({:.3f}, {:.3f}, {:.3f})".format(*first_node.coordinates),
                "m",
            )
            tree.add_item(
                f"Last Node  - {last_node.external_index:>5}",
                "({:.3f}, {:.3f}, {:.3f})".format(*last_node.coordinates),
                "m",
            )
            info_text += str(tree)

        elif len(elements) > 1:
            info_text += (
                f"{len(elements)} ELEMENTS IN SELECTION\n"
                f"{format_long_sequence(elements)}\n\n"
            )
        return info_text

    def _entity_info_text(self):
        entities = app().main_window.list_selected_entities()
        info_text = ""
        project = app().project

        if len(entities) == 1:
            _id, *_ = entities
            entity = project.get_entity(_id)
            info_text += f"LINE {_id}\n\n"

        elif len(entities) > 1:
            info_text += (
                f"{len(entities)} LINES IN SELECTION\n"
                f"{format_long_sequence(entities)}\n\n"
            )

        return info_text

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
