from PyQt5.QtWidgets import QAction, QComboBox, QFileDialog, QLabel, QMainWindow, QMenu, QMessageBox, QSplitter, QStackedWidget, QToolBar
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QPoint
from PyQt5.QtGui import QColor, QCursor
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.toolbars.mesh_toolbar import MeshToolbar
from pulse.interface.viewer_3d.opv_ui import OPVUi
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget
from pulse.interface.user_input.input_ui import InputUi
from pulse.interface.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput
from pulse.interface.menu.model_and_analysis_setup_widget import ModelAndAnalysisSetupWidget
from pulse.interface.menu.results_viewer_widget import ResultsViewerWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.render.clip_plane_widget import ClipPlaneWidget

from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from opps.io.pcf.pcf_exporter import PCFExporter
from opps.io.pcf.pcf_handler import PCFHandler

import os
import sys
import qdarktheme
from functools import partial
from pathlib import Path

from enum import IntEnum


class Workspace(IntEnum):
    GEOMETRY = 0 
    STRUCTURAL_SETUP = 1
    ACOUSTIC_SETUP = 2
    RESULTS = 3


class MainWindow(QMainWindow):
    permission_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        ui_path = UI_DIR / 'main_window.ui'
        uic.loadUi(ui_path, self)

        self.ui_dir = UI_DIR
        self.config = app().config
        self.project = app().project
        self.file = app().project.file
        self.reset()

    def reset(self):
        self.interface_theme = None
        self.model_and_analysis_setup_widget = None
        self.results_viewer_wigdet = None
        self.opv_widget = None
        self.input_widget = None
        self.cache_indexes = list()
        self.last_index = None

    def _load_icons(self):
        self.pulse_icon = get_openpulse_icon()

    def _config_window(self):
        self.showMaximized()
        self.installEventFilter(self)
        self.setWindowIcon(self.pulse_icon)
        self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        help future maintainers and the code editor with
        type inference.
        '''
        
        # QAction
        self.action_geometry_workspace : QAction
        self.action_structural_setup_workspace : QAction
        self.action_acoustic_setup_workspace : QAction
        self.action_analysis_setup_workspace : QAction
        self.action_results_workspace : QAction
        self.action_export_geometry : QAction
        self.action_import_geometry : QAction
        self.action_export_pcf : QAction
        self.action_import_pcf : QAction
        self.action_set_dark_theme : QAction
        self.action_set_light_theme : QAction
        self.action_save_project_as : QAction
        self.action_show_points : QAction
        self.action_show_lines : QAction
        self.action_show_tubes : QAction
        self.action_show_symbols : QAction
        self.action_plot_geometry_editor : QAction
        self.action_plot_lines : QAction
        self.action_plot_lines_with_cross_section : QAction
        self.action_plot_mesh : QAction
        self.action_export_piping : QAction
        self.action_user_preferences : QAction
        self.action_geometry_editor_help : QAction
        self.action_pulsation_attenuator_device_editor : QAction

        # QMenu
        self.menu_recent : QMenu
        self.menu_project : QMenu
        self.menu_plots : QMenu
        self.menu_settings : QMenu
        self.menu_model_info : QMenu
        self.menu_help : QMenu

        # QSplitter
        self.splitter : QSplitter

        # QStackedWidget
        self.setup_widgets_stack : QStackedWidget
        self.render_widgets_stack : QStackedWidget

        # QToolBar
        self.tool_bar : QToolBar

    def _connect_actions(self):
        '''
        Instead of connecting every action manually, one by one,
        this function loops through every action and connects it
        to a function ending with "_callback".

        For example an action named "action_new" will be connected to 
        the function named "action_new_callback" if it exists.
        '''
        for action in self.findChildren(QAction):
            function_name = action.objectName() + "_callback"
            function_exists = hasattr(self, function_name)
            if not function_exists:
                continue

            function = getattr(self, function_name)
            if callable(function):
                action.triggered.connect(function)

    def _create_workspaces_toolbar(self):
        actions = {
            Workspace.GEOMETRY: self.action_geometry_workspace,
            Workspace.STRUCTURAL_SETUP: self.action_structural_setup_workspace,
            Workspace.ACOUSTIC_SETUP: self.action_acoustic_setup_workspace,
            Workspace.RESULTS: self.action_results_workspace,
        }

        self.combo_box_workspaces = QComboBox()
        self.combo_box_workspaces.setMinimumSize(170, 26)

        # iterating sorted items make the icons appear in the same 
        # order as defined in the Workspace enumerator
        for _, action in sorted(actions.items()):
            self.combo_box_workspaces.addItem(action.text())

        self.combo_box_workspaces.currentIndexChanged.connect(self.update_combobox_indexes)
        self.combo_box_workspaces.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(self.combo_box_workspaces)

    def update_combobox_indexes(self):
        index = self.combo_box_workspaces.currentIndex()
        self.cache_indexes.append(index)

    def disable_workspace_selector_and_geometry_editor(self, _bool):
        #TODO: improve as soon as possible
        self.combo_box_workspaces.setDisabled(_bool)
        self.action_plot_geometry_editor.setDisabled(_bool)
        self.action_export_geometry.setDisabled(_bool)
        self.action_export_pcf.setDisabled(_bool)
        self.action_import_geometry.setDisabled(_bool)
        self.action_import_pcf.setDisabled(_bool)

    def _create_layout(self):

        self.opv_widget = OPVUi(self.project, self)
        self.model_and_analysis_setup_widget = ModelAndAnalysisSetupWidget(self)
        self.results_viewer_wigdet = ResultsViewerWidget()
        self.opv_widget.opvAnalysisRenderer._createPlayer()
        self.input_widget = InputUi(self)

        editor = app().geometry_toolbox.editor
        self.mesh_widget = MeshRenderWidget()
        self.geometry_widget = EditorRenderWidget(editor)
        self.geometry_widget.set_theme("light")

        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.opv_widget)

        self.geometry_input_wigdet = OPPGeometryDesignerInput(self.geometry_widget)
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.model_and_analysis_setup_widget)
        self.setup_widgets_stack.addWidget(self.results_viewer_wigdet)

        self.splitter.setSizes([100, 400])
        self.splitter.widget(0).setMinimumWidth(380)
        self.opv_widget.updatePlots()
        self.opv_widget.plot_entities_with_cross_section()

    def configure_window(self):

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()
        self._update_recent_projects()
        self._add_mesh_toolbar()

        self.plot_entities()
        self.use_structural_setup_workspace()
        self.load_user_preferences()
        self.load_recent_project()
 
    # public
    def new_project(self):
        if not self.input_widget.new_project():
            return 
        self._update_recent_projects()
        self.set_window_title(self.file._project_name)
        self.use_structural_setup_workspace()
        app().update()

    def open_project(self, path=None):
        if not self.input_widget.load_project(path):
            return

        self._update_recent_projects()
        self.set_window_title(self.file._project_name)
        app().update()
        self.action_front_view_callback()
    
    def open_pcf(self):
        '''
        This function is absolutelly disgusting. I will refactor this next week, 
        but for now it will be like this just in order to make the bosses happy =)
        '''
        from opps.model import Pipe, Bend, Flange

        path, ok = QFileDialog.getOpenFileName(self, 'Load PCF', '', 'PCF (*.pcf)')
        if not ok:
            return

        app().geometry_toolbox.open(path)
        pipeline = app().geometry_toolbox.pipeline

        for structure in pipeline.structures:
            if isinstance(structure, Pipe | Bend):
                if structure.start_diameter == structure.end_diameter:
                    section_label = 'Pipe section'
                    start_thickness = structure.start_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 0, 0]
                else:
                    section_label = 'Pipe section'  
                    start_thickness = structure.start_diameter * 0.05
                    end_thickness = structure.end_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 
                                          structure.end_diameter, end_thickness, 0, 0, 0, 0]

            elif isinstance(structure, Flange):
                section_label = 'Pipe section'
                thickness = structure.diameter * 0.05
                section_parameters = [structure.diameter, thickness, 0, 0, 0, 0]

            cross_section_info = {
                'section_type_label': section_label, 
                'section_parameters': section_parameters
            }

            # There are no beams in pcf files, therefore it is pipe_1
            structure.extra_info["structural_element_type"] = "pipe_1"
            structure.extra_info["cross_section_info"] = cross_section_info

        self.geometry_input_wigdet.process_geometry_callback()

    def export_pcf(self):
        init_path = os.path.expanduser("~")
        path, ok = QFileDialog.getSaveFileName(self, 
                                               'Export PCF file', 
                                               init_path, 
                                               'PCF (*.pcf)')
        if not ok:
            return

        pipeline = app().geometry_toolbox.pipeline
        pcf_exporter = PCFExporter()
        pcf_exporter.save(path, pipeline)
        self.update()

    def export_geometry(self):
        init_path = os.path.expanduser("~")
        path, ok = QFileDialog.getSaveFileName(self, 
                                               'Export geometry file', 
                                               init_path, 
                                               'STEP (*.step)')
        if not ok:
            return

        geometry_handler = GeometryHandler()
        geometry_handler.export_cad_file(path)

    def update(self):
        self.geometry_widget.update_plot(reset_camera=True)
        self.mesh_widget.update_plot(reset_camera=True)
        self.opv_widget.updatePlots()

    def get_current_workspace(self):
        return self.combo_box_workspaces.currentIndex()

    def use_geometry_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(Workspace.GEOMETRY)

    def use_structural_setup_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(Workspace.STRUCTURAL_SETUP)

    def use_acoustic_setup_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(Workspace.ACOUSTIC_SETUP)

    def use_results_workspace(self):
        self.combo_box_workspaces.setCurrentIndex(Workspace.RESULTS)

    def plot_entities(self):
        # Configure the mesh plot as a combination of the interface buttons
        self.action_show_points.setChecked(False)
        self.action_show_lines.setChecked(True)
        self.action_show_tubes.setChecked(False)
        self.action_show_symbols.setChecked(False)
        self._update_visualization()

    def plot_entities_with_cross_section(self):
        # Configure the mesh plot as a combination of the interface buttons
        self.action_show_points.setChecked(False)
        self.action_show_lines.setChecked(False)
        self.action_show_tubes.setChecked(True)
        self.action_show_symbols.setChecked(False)
        self._update_visualization()

    def plot_mesh(self):
        # Configure the mesh plot as a combination of the interface buttons
        self.action_show_points.setChecked(True)
        self.action_show_lines.setChecked(True)
        self.action_show_tubes.setChecked(True)
        self.action_show_symbols.setChecked(True)
        self._update_visualization()

    def update_plot_mesh(self):

        key = list()
        key.append(self.action_show_points.isChecked())
        key.append(self.action_show_lines.isChecked())
        key.append(self.action_show_tubes.isChecked())
        key.append(self.action_show_symbols.isChecked())

        if key != [True, True, True, True]:
            self.plot_mesh()

    def update_plot_entities(self):

        key = list()
        key.append(self.action_show_points.isChecked())
        key.append(self.action_show_lines.isChecked())
        key.append(self.action_show_tubes.isChecked())
        key.append(self.action_show_symbols.isChecked())

        if key != [False, True, False, False]:
            self.plot_entities()  

    def update_plot_entities_with_cross_section(self):

        key = list()
        key.append(self.action_show_points.isChecked())
        key.append(self.action_show_lines.isChecked())
        key.append(self.action_show_tubes.isChecked())
        key.append(self.action_show_symbols.isChecked())

        if key != [False, False, True, False]:
            self.plot_entities_with_cross_section()

    def plot_raw_geometry(self):
        # self.use_structural_setup_workspace()
        self.action_show_points.setChecked()
    
    def plot_geometry_editor(self):
        self.use_geometry_workspace()

    def set_window_title(self, msg=""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def load_recent_project(self):
        if self.config.open_last_project and self.config.haveRecentProjects():
            self.import_project_call(self.config.getMostRecentProjectDir())
        elif self.input_widget.get_started():
            self.update()  # update the renders before change the view
            self.action_front_view_callback()
            self._update_recent_projects()
            self.set_window_title(self.file.project_name)
        else:
            self.disable_workspace_selector_and_geometry_editor(True)

    # internal
    def _update_recent_projects(self):
        actions = self.menu_recent.actions()
        for action in actions:
            self.menu_recent.removeAction(action)

        self.menu_actions = []
        for name, path in reversed(self.config.recent_projects.items()):
            import_action = QAction(str(name) + "\t" + str(path))
            import_action.setStatusTip(str(path))
            import_action.triggered.connect(partial(self.open_project, path))
            self.menu_recent.addAction(import_action)
            self.menu_actions.append(import_action)

    def change_window_title(self, msg = ""):
        self.set_window_title(msg)

    def _update_permissions(self):
        pass

    def _update_visualization(self):
        points = self.action_show_points.isChecked()
        lines = self.action_show_lines.isChecked()
        tubes = self.action_show_tubes.isChecked()
        symbols = self.action_show_symbols.isChecked()
        self.opv_widget.update_visualization(points, lines, tubes, symbols)
        # self.mesh_widget.update_visualization(points, lines, tubes, symbols)

    # callbacks
    def action_new_project_callback(self):
        self.new_project()

    def action_open_project_callback(self):
        self.open_project()

    def action_save_project_as_callback(self):
        self.input_widget.save_project_as()

    def action_import_pcf_callback(self):
        self.open_pcf()

    def action_export_pcf_callback(self):
        self.export_pcf()

    def action_export_geometry_callback(self):
        self.export_geometry()

    def action_geometry_workspace_callback(self):
        self.close_opened_windows()
        self.mesh_toolbar.setDisabled(True)
        self.geometry_input_wigdet._disable_finalize_button(True)
        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)
        self.geometry_input_wigdet.add_widget.load_defined_unit()

    def action_structural_setup_workspace_callback(self):
        self.mesh_toolbar.setDisabled(False)
        self.model_and_analysis_setup_widget.update_visibility_for_structural_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)
        # update the internal renderer to the setup mode
        self.opv_widget.setRenderer(self.opv_widget.opvRenderer)

    def action_acoustic_setup_workspace_callback(self):
        self.mesh_toolbar.setDisabled(False)
        self.model_and_analysis_setup_widget.update_visibility_for_acoustic_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)
        # update the internal renderer to the setup mode
        self.opv_widget.setRenderer(self.opv_widget.opvRenderer)

    def action_coupled_setup_workspace_callback(self):
        self.model_and_analysis_setup_widget.update_visibility_for_coupled_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)

    def action_results_workspace_callback(self):
        if self.project.is_the_solution_finished():
            self.results_viewer_wigdet.animation_widget.setVisible(False)
            self.setup_widgets_stack.setCurrentWidget(self.results_viewer_wigdet)
            self.render_widgets_stack.setCurrentWidget(self.opv_widget)
            self.results_viewer_wigdet.udate_visibility_items()
        else:
            if self.cache_indexes:
                self.combo_box_workspaces.setCurrentIndex(self.cache_indexes[-2])

    def action_save_as_png_callback(self):
        self.savePNG_call()
    
    def action_reset_callback(self):
        self.input_widget.reset_project()

    def action_plot_geometry_editor_callback(self):
        self.action_show_points.setChecked(True)
        self.action_show_lines.setChecked(True)
        self.action_show_tubes.setChecked(True)
        self.action_show_symbols.setChecked(True)
        self.use_geometry_workspace()
    
    def action_user_preferences_callback(self):
        self.input_widget.mesh_setup_visibility()

    def action_geometry_editor_help_callback(self):
        self.input_widget.geometry_editor_help()

    def action_pulsation_attenuator_device_editor_callback(self):
        self.input_widget.pulsation_attenuator_device_editor()

    def action_plot_lines_callback(self):
        self.use_structural_setup_workspace()
        self.plot_entities()

    def action_plot_lines_with_cross_section_callback(self):
        self.use_structural_setup_workspace()
        self.plot_entities_with_cross_section()

    def action_plot_mesh_callback(self):
        self.use_structural_setup_workspace()
        self.plot_mesh()

    def action_plot_cross_section_callback(self):
        self.input_widget.plot_cross_section()

    def action_isometric_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(0)
            return
        render_widget.set_isometric_view()

    def action_top_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(1)
            return
        render_widget.set_top_view()

    def action_bottom_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(2)
            return
        render_widget.set_bottom_view()

    def action_left_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(3)
            return
        render_widget.set_left_view()

    def action_right_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(4)
            return
        render_widget.set_right_view()

    def action_front_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(5)
            return
        render_widget.set_front_view()

    def action_back_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        if render_widget == self.opv_widget:
            render_widget.setCameraView(6)
            return
        render_widget.set_back_view()
    
    def action_clip_plane_callback(self):
        self.clip_plane = ClipPlaneWidget()

    def action_set_structural_element_type_callback(self):
        self.input_widget.set_structural_element_type()

    def action_add_connecting_flanges_callback(self):
        self.input_widget.add_flanges()

    def action_set_prescribed_dofs_callback(self):
        self.input_widget.set_prescribed_dofs()

    def action_set_nodal_loads_callback(self):
        self.input_widget.set_nodal_loads()

    def action_add_mass_spring_damper_callback(self):
        self.input_widget.add_mass_spring_damper()

    def action_set_capped_end_callback(self):
        self.input_widget.set_capped_end()

    def action_set_stress_stiffening_callback(self):
        self.input_widget.set_stress_stress_stiffening()

    def action_add_elastic_nodal_links_callback(self):
        self.input_widget.add_elastic_nodal_links()

    def action_structural_model_info_callback(self):
        self.input_widget.structural_model_info()

    def action_set_acoustic_element_type_callback(self):
        self.input_widget.set_acoustic_element_type()

    def action_set_acoustic_pressure_callback(self):
        self.input_widget.set_acoustic_pressure()

    def action_set_volume_velocity_callback(self):
        self.input_widget.set_volume_velocity()

    def action_set_specific_impedance_callback(self):
        self.input_widget.set_specific_impedance()

    def action_add_perforated_plate_callback(self):
        self.input_widget.add_perforated_plate()

    def action_set_acoustic_element_length_correction_callback(self):
        self.input_widget.set_acoustic_element_length_correction()

    def action_add_compressor_excitation_callback(self):
        self.input_widget.add_compressor_excitation()

    def action_acoustic_model_info_callback(self):
        self.input_widget.acoustic_model_info()
    
    def action_check_beam_criteria_callback(self):
        self.input_widget.check_beam_criteria()

    def action_select_analysis_type_callback(self):
        self.input_widget.analysis_type_input()

    def action_analysis_setup_callback(self):
        self.input_widget.analysis_setup()
    
    def action_run_analysis_callback(self):
        self.input_widget.run_analysis()

    def action_about_openpulse_callback(self):
        self.input_widget.about_OpenPulse()

    def action_show_points_callback(self, cond):
        self._update_visualization()

    def action_show_lines_callback(self, cond):
        self._update_visualization()

    def action_show_tubes_callback(self, cond):
        self._update_visualization()

    def action_show_symbols_callback(self, cond):
        self._update_visualization()

    def update_export_geometry_file_access(self):
        import_type = self.file.get_import_type()
        if import_type == 0:
            self.action_export_geometry.setDisabled(True)
        elif import_type == 1:
            self.action_export_geometry.setDisabled(False)

    def action_import_geometry_callback(self):
        self.input_widget.import_geometry()

    def import_project_call(self, path=None):
        if self.input_widget.load_project(path):
            self._update_recent_projects()
            self.change_window_title(self.file.project_name)
            self.update()
            self.opv_widget.updatePlots()
            self.plot_mesh()
            self.action_front_view_callback()

    def _add_mesh_toolbar(self):
        self.mesh_toolbar = MeshToolbar()
        self.addToolBar(self.mesh_toolbar)
        self.insertToolBarBreak(self.mesh_toolbar)

    def _enable_menus_at_start(self):
        pass

    def close_opened_windows(self):
        if self.opv_widget.inputObject is not None:
            self.opv_widget.inputObject.close()
            self.opv_widget.setInputObject(None)

    def load_user_preferences(self):
        self.update_theme = False
        self.user_preferences = self.config.get_user_preferences()
        if "interface theme" in self.user_preferences:
            if self.user_preferences["interface theme"] == "dark":
                self.action_set_dark_theme_callback()
            else:
                self.action_set_light_theme_callback()
        else:
            self.action_set_light_theme_callback()
        self.opv_widget.set_user_interface_preferences(self.user_preferences)
        self.update_theme = True

    def action_set_dark_theme_callback(self):
        self.update_themes_in_file(theme="dark")
        if self.interface_theme in [None, "light"]:
            self.interface_theme = "dark"
            self.custom_colors = { "[dark]": { "toolbar.background": "#202124"} }
            qdarktheme.setup_theme("dark", custom_colors=self.custom_colors)
            self.action_set_light_theme.setDisabled(False)
            self.action_set_dark_theme.setDisabled(True)
            self.geometry_widget.set_theme("dark")
            self.mesh_widget.set_theme("dark")
            self.model_and_analysis_setup_widget.model_and_analysis_setup_items.set_theme("dark")
            self.results_viewer_wigdet.results_viewer_items.set_theme("dark")

    def action_set_light_theme_callback(self):
        self.update_themes_in_file(theme="light")
        if self.interface_theme in [None, "dark"]:
            self.interface_theme = "light"
            qdarktheme.setup_theme("light")
            self.action_set_light_theme.setDisabled(True)
            self.action_set_dark_theme.setDisabled(False)
            self.geometry_widget.set_theme("light")
            self.mesh_widget.set_theme("light")
            self.model_and_analysis_setup_widget.model_and_analysis_setup_items.set_theme("light")
            self.results_viewer_wigdet.results_viewer_items.set_theme("light")

    def update_themes_in_file(self, theme):
        if self.update_theme:
            self.user_preferences = self.config.get_user_preferences()
            self.user_preferences["interface theme"] = theme
            self.user_preferences["background color"] = theme
            if theme == "dark":
                self.user_preferences["bottom font color"] = (255, 255, 255)
            else:
                self.user_preferences["bottom font color"] = (0, 0, 0)
            self.config.write_user_preferences_in_file(self.user_preferences)
            self.opv_widget.set_user_interface_preferences(self.user_preferences)

    def savePNG_call(self):
        project_path = self.file._project_path
        if not os.path.exists(project_path):
            project_path = ""
        path, _ = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.opv_widget().savePNG(path)

    def positioning_cursor_on_widget(self, widget):
        width, height = widget.width(), widget.height()
        final_pos = widget.mapToGlobal(QPoint(int(width/2), int(height/2)))
        QCursor.setPos(final_pos)

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.ShortcutOverride:
    #         if event.key() == Qt.Key_Space:
    #             return
    #             self.opv_widget.opvAnalysisRenderer.tooglePlayPauseAnimation()
    #     return super(MainWindow, self).eventFilter(obj, event)

    def closeEvent(self, event):

        if self.opv_widget.inputObject is not None:
            self.opv_widget.inputObject.close()

        title = "OpenPulse"
        message = "Would you like to exit from the OpenPulse application?"
        close = QMessageBox.question(self, title, message, QMessageBox.No | QMessageBox.Yes)
        if close == QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()

    # def _createStatusBar(self):
    #     self.status_bar = QStatusBar()
    #     self.setStatusBar(self.status_bar)
    #     #
    #     label_font = self._getFont(10, bold=True, italic=False, family_type="Arial")
    #     self.label_geometry_state = QLabel("", self)
    #     self.label_geometry_state.setFont(label_font)
    #     self.status_bar.addPermanentWidget(self.label_geometry_state)
    #     #
    #     self.label_mesh_state = QLabel("", self)
    #     self.label_mesh_state.setFont(label_font)
    #     self.status_bar.addPermanentWidget(self.label_mesh_state)