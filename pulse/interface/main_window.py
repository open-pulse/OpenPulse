from time import time
import os
import sys
import qdarktheme
from functools import partial
from pathlib import Path
import logging
from shutil import copy, rmtree
from time import time

from PyQt5.QtWidgets import QAbstractButton, QAction, QComboBox, QDialog, QFileDialog, QMainWindow, QMenu, QMessageBox, QSplitter, QStackedWidget, QToolBar, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QPoint
from PyQt5.QtGui import QColor, QCloseEvent, QCursor
from PyQt5 import uic

from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from opps.io.pcf.pcf_exporter import PCFExporter
from opps.io.pcf.pcf_handler import PCFHandler

from molde.render_widgets import CommonRenderWidget

from pulse import USER_PATH, TEMP_PROJECT_DIR, TEMP_PROJECT_FILE
from pulse import app, UI_DIR, QSS_DIR
from pulse.interface.formatters import icons
from pulse.interface.auxiliar.file_dialog import FileDialog
from pulse.interface.toolbars.mesh_toolbar import MeshToolbar
from pulse.interface.others.status_bar import StatusBar
from pulse.interface.viewer_3d.render_widgets import GeometryRenderWidget, MeshRenderWidget, ResultsRenderWidget
from pulse.interface.user_input.input_ui import InputUi
from pulse.interface.user_input.model.geometry.geometry_designer_widget import GeometryDesignerWidget
from pulse.interface.menu.model_and_analysis_setup_widget import ModelAndAnalysisSetupWidget
from pulse.interface.menu.results_viewer_widget import ResultsViewerWidget
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.render.section_plane_widget import SectionPlaneWidget
from pulse.interface.utils import Workspace, VisualizationFilter, SelectionFilter, ColorMode
from pulse.interface.user_input.project.get_started import GetStartedInput
from pulse.interface.user_input.project.new_project import NewProjectInput
from pulse.interface.user_input.project.reset_project import ResetProjectInput
from pulse.interface.user_input.project.import_geometry import ImportGeometry
from pulse.interface.user_input.project.about_open_pulse import AboutOpenPulseInput
from pulse.interface.user_input.project.save_project_data_selector import SaveProjectDataSelector
from pulse.interface.user_input.project.loading_window import LoadingWindow


class MainWindow(QMainWindow):
    theme_changed = pyqtSignal(str)
    visualization_changed = pyqtSignal()
    selection_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()

        ui_path = UI_DIR / 'main_window.ui'
        uic.loadUi(ui_path, self)

        self.selected_nodes = set()
        self.selected_lines = set()
        self.selected_elements = set()
        
        self.visualization_filter = VisualizationFilter.all_true()
        self.selection_filter = SelectionFilter.all_false()

        self.ui_dir = UI_DIR
        self.config = app().config
        self.project = app().project

        self._initialize()

    def _initialize(self):

        self.dialog = None
        self.pulse_file = None
        self.input_ui = None

        self.model_and_analysis_setup_widget = None
        self.results_viewer_wigdet = None

        self.interface_theme = None
        self.last_index = None
        self.last_render_index = None

        self.project_data_modified = False

        self.cache_indexes = list()

    def _load_stylesheets(self):
        stylesheets = []
        common_dir = QSS_DIR / "common_theme"
        
        if self.interface_theme == "light":
            theme_dir = QSS_DIR / "light_theme"
        elif self.interface_theme == "dark":
            theme_dir = QSS_DIR / "dark_theme"
        else:
            return

        for path in common_dir.rglob("*.qss"):
            stylesheets.append(path.read_text())

        for path in theme_dir.rglob("*.qss"):
            stylesheets.append(path.read_text())

        combined_stylesheet = "\n\n".join(stylesheets)
        self.setStyleSheet(combined_stylesheet)

    def _config_window(self):
        self.showMinimized()
        self.installEventFilter(self)
        self.pulse_icon = icons.get_openpulse_icon()
        self.setWindowIcon(self.pulse_icon)
        # self.setStyleSheet("""QToolTip{color: rgb(100, 100, 100); background-color: rgb(240, 240, 240)}""")

    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        help future maintainers and the code editor with
        type inference.
        '''
        
        # QAction
        self.action_open_project: QAction
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
        self.action_save_project : QAction
        self.action_save_project_as : QAction
        self.action_show_mesh_nodes : QAction
        self.action_show_geometry_points : QAction
        self.action_show_lines : QAction
        self.action_show_tubes : QAction
        self.action_show_symbols : QAction
        self.action_show_transparent : QAction
        self.action_select_elements : QAction
        self.action_plot_geometry_editor : QAction
        self.action_plot_lines : QAction
        self.action_plot_lines_with_cross_section : QAction
        self.action_plot_mesh : QAction
        self.action_export_piping : QAction
        self.action_user_preferences : QAction
        self.action_geometry_editor_help : QAction
        self.action_pulsation_suppression_device_editor : QAction
        self.action_section_plane : QAction

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

        self.selection_changed.connect(self.selection_changed_callback)

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
            self.combo_box_workspaces.addItem(f" {action.text()}")

        self.combo_box_workspaces.currentIndexChanged.connect(self.update_combobox_indexes)
        self.combo_box_workspaces.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(self.combo_box_workspaces)

    def update_combobox_indexes(self, index):
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

        self.model_and_analysis_setup_widget = ModelAndAnalysisSetupWidget()
        self.results_viewer_wigdet = ResultsViewerWidget()
        self.input_ui = InputUi(self)
        self.mesh_widget = MeshRenderWidget()
        self.results_widget = ResultsRenderWidget()
        self.geometry_widget = GeometryRenderWidget()

        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.results_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.currentChanged.connect(self.render_changed_callback)

        self.geometry_input_wigdet = GeometryDesignerWidget(self.geometry_widget, self)
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.model_and_analysis_setup_widget)
        self.setup_widgets_stack.addWidget(self.results_viewer_wigdet)

        self.splitter.setSizes([100, 400])
        self.splitter.widget(0).setMinimumWidth(380)
        self._update_visualization()

        self.model_and_analysis_items = self.model_and_analysis_setup_widget.model_and_analysis_setup_items

    def create_file_dialog(self):
        self.file_dialog = FileDialog()

    def configure_window(self):
        t0 = time()
        # self._load_stylesheets()
        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        app().splash.update_progress(30)
        self._load_section_plane()
        dt = time() - t0
        print(f"Time to process A: {dt} [s]")

        t1 = time()
        self._create_layout()
        self._create_workspaces_toolbar()
        self._create_status_bar()
        self._update_recent_projects()
        self._add_mesh_toolbar()
        app().splash.update_progress(70)
        dt = time() - t1
        print(f"Time to process B: {dt} [s]")

        t2 = time()
        self.plot_lines_with_cross_sections()
        self.use_structural_setup_workspace()
        self.load_user_preferences()
        self.create_temporary_folder()
        app().splash.update_progress(98)
        dt = time() - t2
        print(f"Time to process C: {dt} [s]")

        app().splash.close()
        self.showMaximized()

        app().processEvents()
        self.create_file_dialog()
        dt = time() - t0
        print(f"Time to process D: {dt} [s]")

        if not self.is_temporary_folder_empty():
            self.recovery_dialog()
        else:
            self.load_recent_project()
 
    def create_temporary_folder(self):
        create_new_folder(USER_PATH, "temp_pulse")

    def reset_temporary_folder(self):
        if TEMP_PROJECT_DIR.exists():
            for filename in os.listdir(TEMP_PROJECT_DIR).copy():
                file_path = TEMP_PROJECT_DIR / filename
                if os.path.exists(file_path):
                    if "." in filename:
                        os.remove(file_path)
                    else:
                        rmtree(file_path)

    def is_temporary_folder_empty(self):
        if TEMP_PROJECT_DIR.exists():
            if os.listdir(TEMP_PROJECT_DIR):
                return False
        return True
    
    def recovery_dialog(self):

        caption = "The recovery project data has been detected in the application backup files. "
        caption += "Would you like to try to recover the last project files?"

        obj = QMessageBox.question(   
                                    self, 
                                    "Project recovery", 
                                    caption, 
                                    QMessageBox.Yes | QMessageBox.No
                                  )

        if obj == QMessageBox.Yes:
            self.open_project()
        else:
            self.reset_temporary_folder()
            self.load_recent_project()

    def open_pcf(self):
        '''
        This function is absolutelly disgusting. I will refactor this next week, 
        but for now it will be like this just in order to make the bosses happy =)
        '''
        from opps.model import Pipe, Bend, Flange

        last_path = app().config.get_last_folder_for("pcf folder")
        if last_path is None:
            last_path = str(Path().home())

        file_path, check = self.file_dialog.get_open_file_name(
                                                                "Open PCF File", 
                                                                last_path, 
                                                                filter = "PCF File (*.pcf)"
                                                               )

        if not check:
            return

        pipeline = app().project.pipeline
        pcf_handler = PCFHandler()
        pcf_handler.load(file_path, pipeline)

        for structure in pipeline.structures:
            if isinstance(structure, Pipe | Bend):
                if structure.start_diameter == structure.end_diameter:
                    section_label = 'Pipe'
                    start_thickness = structure.start_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 0, 0]
                else:
                    section_label = 'Reducer'  
                    start_thickness = structure.start_diameter * 0.05
                    end_thickness = structure.end_diameter * 0.05
                    section_parameters = [structure.start_diameter, start_thickness, 0, 0, 
                                          structure.end_diameter, end_thickness, 0, 0, 0, 0]

            elif isinstance(structure, Flange):
                section_label = 'Pipe'
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

        last_path = app().config.get_last_folder_for("exported pcf folder")
        if last_path is None:
            last_path = str(Path().home())

        path, check = self.file_dialog.get_save_file_name( 
                                                            'Export PCF file', 
                                                            last_path, 
                                                            'PCF File (*.pcf)'
                                                         )

        if not check:
            return

        pipeline = app().project.pipeline
        pcf_exporter = PCFExporter()
        pcf_exporter.save(path, pipeline)
        self.update_plots()

    def export_geometry(self):

        last_path = app().config.get_last_folder_for("exported geometry folder")
        if last_path is None:
            last_path = str(Path().home())

        path, check = self.file_dialog.get_save_file_name(
                                                            'Export geometry file', 
                                                            last_path, 
                                                            'Geometry File (*.step)'
                                                          )

        if not check:
            return

        geometry_handler = GeometryHandler()
        geometry_handler.export_cad_file(path)

    # public
    def update_plots(self):
        self.geometry_widget.update_plot(reset_camera=True)
        self.mesh_widget.update_plot(reset_camera=True)
        self.results_widget.update_plot(reset_camera=True)

    def selection_changed_callback(self):
        # TODO: implement something useful
        pass

    def set_selection(self, *, nodes=None, elements=None, lines=None, join=False, remove=False):

        if nodes is None:
            nodes = set()

        if elements is None:
            elements = set()

        if lines is None:
            lines = set()

        if join and remove:
            self.selected_nodes ^= set(nodes)
            self.selected_lines ^= set(lines)
            self.selected_elements ^= set(elements)

        elif join:
            self.selected_nodes |= set(nodes)
            self.selected_lines |= set(lines)
            self.selected_elements |= set(elements)

        elif remove:
            self.selected_nodes -= set(nodes)
            self.selected_lines -= set(lines)
            self.selected_elements -= set(elements)

        else:
            self.selected_nodes = set(nodes)
            self.selected_lines = set(lines)
            self.selected_elements = set(elements)

        self.selection_changed.emit()
    
    def list_selected_nodes(self) -> list[int]:
        return list(self.selected_nodes)

    def list_selected_lines(self) -> list[int]:
        return list(self.selected_lines)

    def list_selected_elements(self) -> list[int]:
        return list(self.selected_elements)

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

    def plot_lines(self):
        self._configure_visualization(points=True, lines=True)

    def plot_lines_with_cross_sections(self):
        self._configure_visualization(
            points=True, lines=True, tubes=True,
            acoustic_symbols=True, structural_symbols=True,
        )

    def plot_mesh(self):
        self._configure_visualization(
            nodes=True, lines=True, tubes=True,
            acoustic_symbols=True, structural_symbols=True,
        )
    
    def plot_geometry_editor(self):
        self.use_geometry_workspace()

    def set_window_title(self, msg=""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title) 

    def get_started(self):
        self.close_dialogs()
        self.model_and_analysis_items.modify_model_setup_items_access(True)
        obj = GetStartedInput()
        return obj.complete

    def initial_project_action(self, finalized):
        # t0 = time()
        self.update_export_geometry_file_access()
        self.model_and_analysis_items.modify_model_setup_items_access(True)
        if finalized:
            self.disable_workspace_selector_and_geometry_editor(False)
            if app().pulse_file.check_pipeline_data():
                self.project.none_project_action = False
                self.model_and_analysis_items.modify_model_setup_items_access(False)
                # dt = time() - t0
                # print(f"initial_project_action: {dt} s")
                return True
            else:
                self.model_and_analysis_items.modify_geometry_item_access(False)
                return True
        else:
            self.project.none_project_action = True
            return False

    def reset_geometry_render(self):
        self.project.pipeline.reset()

    def reset_project(self):
        if not self.project.none_project_action:
            ResetProjectInput()

    def load_recent_project(self):
        # t0 = time()
        self.mesh_toolbar.pushButton_generate_mesh.setDisabled(True)

        if self.config.open_last_project and self.config.haveRecentProjects():
            self.open_project(self.config.getMostRecentProjectDir())

        elif self.get_started():
            self.action_front_view_callback()
            # self._update_recent_projects()

        else:
            self.disable_workspace_selector_and_geometry_editor(True)
        # dt = time() - t0
        # print(f"Elapsed time to load_recent_project: {dt}s")

    # internal
    def _update_recent_projects(self):
        actions = self.menu_recent.actions()
        for action in actions:
            self.menu_recent.removeAction(action)

        self.menu_actions = []
        for name, path in reversed(self.config.recent_projects.items()):
            path = Path(path)
            if not path.exists():
                continue
            import_action = QAction(str(name) + "\t" + str(path))
            import_action.setStatusTip(str(path))
            import_action.triggered.connect(partial(self.open_project, path))
            self.menu_recent.addAction(import_action)
            self.menu_actions.append(import_action)

    def _update_permissions(self):
        pass

    def _configure_visualization(self, *args, **kwargs):
        kwargs.setdefault("color_mode", self.visualization_filter.color_mode)

        self.visualization_filter = VisualizationFilter(*args, **kwargs)
        self.action_show_geometry_points.setChecked(self.visualization_filter.points)
        self.action_show_mesh_nodes.setChecked(self.visualization_filter.nodes)
        self.action_show_lines.setChecked(self.visualization_filter.lines)
        self.action_show_tubes.setChecked(self.visualization_filter.tubes)
        symbols = self.visualization_filter.acoustic_symbols | self.visualization_filter.structural_symbols
        self.action_show_symbols.setChecked(symbols)
        self.visualization_changed.emit()
        self._update_visualization()

    def _update_visualization(self):
        symbols = self.action_show_symbols.isChecked()
        self.visualization_filter.nodes = self.action_show_mesh_nodes.isChecked()
        self.visualization_filter.points = self.action_show_geometry_points.isChecked()
        self.visualization_filter.tubes = self.action_show_tubes.isChecked()
        self.visualization_filter.lines = self.action_show_lines.isChecked()
        self.visualization_filter.transparent = self.action_show_transparent.isChecked()
        self.visualization_filter.acoustic_symbols = symbols
        self.visualization_filter.structural_symbols = symbols
        self.selection_filter.nodes = self.visualization_filter.nodes | self.visualization_filter.points
        self.selection_filter.elements = self.visualization_filter.nodes
        self.selection_filter.lines = not self.selection_filter.elements
        self.visualization_changed.emit()

    def _load_section_plane(self):
        self.section_plane = SectionPlaneWidget()

    # callbacks
    def action_new_project_callback(self):
        self.new_project()

    def action_open_project_callback(self):
        self.open_project_dialog()

    def action_save_project_as_callback(self):
        self.save_project_as_dialog()

    def action_save_project_callback(self):
        self.save_project_dialog()

    def action_import_pcf_callback(self):
        self.open_pcf()

    def action_export_pcf_callback(self):
        self.export_pcf()

    def action_export_geometry_callback(self):
        self.export_geometry()

    def action_geometry_workspace_callback(self):
        self._configure_visualization(
            points=True, tubes=True,
            acoustic_symbols=self.visualization_filter.acoustic_symbols,
            structural_symbols=self.visualization_filter.structural_symbols,
        )
        self.close_dialogs()
        self.mesh_toolbar.setDisabled(True)

        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def action_structural_setup_workspace_callback(self):
        self.mesh_toolbar.setDisabled(False)
        self.model_and_analysis_setup_widget.update_visibility_for_structural_analysis()

        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)

    def action_acoustic_setup_workspace_callback(self):
        self.mesh_widget.update_selection()
        self.mesh_toolbar.setDisabled(False)
        self.model_and_analysis_setup_widget.update_visibility_for_acoustic_analysis()

        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)

    def action_coupled_setup_workspace_callback(self):
        self.model_and_analysis_setup_widget.update_visibility_for_coupled_analysis()
        self.setup_widgets_stack.setCurrentWidget(self.model_and_analysis_setup_widget)
        self.render_widgets_stack.setCurrentWidget(self.results_widget)

    def action_results_workspace_callback(self):
        self.results_widget.update_selection()
        self.results_viewer_wigdet.animation_widget.setVisible(False)
        self.results_viewer_wigdet.update_visibility_items()

        if self.project.is_the_solution_finished():
            self.results_viewer_wigdet.animation_widget.setVisible(False)
            self.setup_widgets_stack.setCurrentWidget(self.results_viewer_wigdet)
            self.render_widgets_stack.setCurrentWidget(self.results_widget)
            self.results_viewer_wigdet.update_visibility_items()
            self._configure_visualization(tubes=True)
        else:
            if self.cache_indexes:
                self.combo_box_workspaces.setCurrentIndex(self.cache_indexes[-2])

    def render_changed_callback(self, new_index):
        if self.last_render_index is None:
            self.last_render_index = new_index
            return

        new_widget = self.render_widgets_stack.widget(new_index)
        if isinstance(new_widget, CommonRenderWidget):
            last_widget = self.render_widgets_stack.widget(self.last_render_index)
            new_widget.copy_camera_from(last_widget)
            # if last_widget is not a valid render the operation will be ignored

        self.last_render_index = new_index

    def action_save_as_png_callback(self):
        self.savePNG_call()
    
    def action_reset_callback(self):
        #TODO: reimplement the project resetting
        return
        self.input_ui.reset_project()

    def action_plot_geometry_editor_callback(self):
        self.action_show_mesh_nodes.setChecked(True)
        self.action_show_lines.setChecked(True)
        self.action_show_tubes.setChecked(True)
        self.action_show_symbols.setChecked(True)
        self.use_geometry_workspace()
    
    def action_user_preferences_callback(self):
        self.input_ui.mesh_setup_visibility()

    def action_geometry_editor_help_callback(self):
        self.input_ui.geometry_editor_help()

    def action_pulsation_suppression_device_editor_callback(self):
        self.input_ui.pulsation_suppression_device_editor()

    def action_plot_lines_callback(self):
        if self.get_current_workspace() not in [Workspace.STRUCTURAL_SETUP, Workspace.ACOUSTIC_SETUP]:
            self.use_structural_setup_workspace()
        self.plot_lines()

    def action_plot_lines_with_cross_section_callback(self):
        if self.get_current_workspace() not in [Workspace.STRUCTURAL_SETUP, Workspace.ACOUSTIC_SETUP]:
            self.use_structural_setup_workspace()
        self.plot_lines_with_cross_sections()

    def action_plot_mesh_callback(self):
        if self.get_current_workspace() not in [Workspace.STRUCTURAL_SETUP, Workspace.ACOUSTIC_SETUP]:
            self.use_structural_setup_workspace()
        self.plot_mesh()

    def action_plot_cross_section_callback(self):
        self.input_ui.plot_cross_section()

    def action_isometric_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_isometric_view()

    def action_top_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_top_view()

    def action_bottom_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_bottom_view()

    def action_left_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_left_view()

    def action_right_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_right_view()

    def action_front_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_front_view()

    def action_back_view_callback(self):
        render_widget = self.render_widgets_stack.currentWidget()
        render_widget.set_back_view()
    
    def action_section_plane_callback(self, condition):
        if condition:
            self.section_plane.show()
        else:
            self.section_plane.keep_section_plane = False
            self.section_plane.close()

    def action_zoom_callback(self):
        self.geometry_widget.renderer.ResetCamera()
        self.mesh_widget.renderer.ResetCamera()
        self.results_widget.renderer.ResetCamera()
        self.geometry_widget.update()
        self.mesh_widget.update()
        self.results_widget.update()

    def action_set_structural_element_type_callback(self):
        self.input_ui.set_structural_element_type()

    def action_add_connecting_flanges_callback(self):
        self.input_ui.add_flanges()

    def action_set_prescribed_dofs_callback(self):
        self.input_ui.set_prescribed_dofs()

    def action_set_nodal_loads_callback(self):
        self.input_ui.set_nodal_loads()

    def action_add_mass_spring_damper_callback(self):
        self.input_ui.add_mass_spring_damper()

    def action_set_capped_end_callback(self):
        self.input_ui.set_capped_end()

    def action_set_stress_stiffening_callback(self):
        self.input_ui.set_stress_stress_stiffening()

    def action_add_elastic_nodal_links_callback(self):
        self.input_ui.add_elastic_nodal_links()

    def action_structural_model_info_callback(self):
        self.input_ui.structural_model_info()

    def action_set_acoustic_element_type_callback(self):
        self.input_ui.set_acoustic_element_type()

    def action_set_acoustic_pressure_callback(self):
        self.input_ui.set_acoustic_pressure()

    def action_set_volume_velocity_callback(self):
        self.input_ui.set_volume_velocity()

    def action_set_specific_impedance_callback(self):
        self.input_ui.set_specific_impedance()

    def action_add_perforated_plate_callback(self):
        self.input_ui.add_perforated_plate()

    def action_set_acoustic_element_length_correction_callback(self):
        self.input_ui.set_acoustic_element_length_correction()

    def action_add_compressor_excitation_callback(self):
        self.input_ui.add_compressor_excitation()

    def action_acoustic_model_info_callback(self):
        self.input_ui.acoustic_model_info()
    
    def action_check_beam_criteria_callback(self):
        self.input_ui.check_beam_criteria()

    def action_select_analysis_type_callback(self):
        self.input_ui.analysis_type_input()

    def action_analysis_setup_callback(self):
        self.input_ui.analysis_setup()
    
    def action_run_analysis_callback(self):
        self.input_ui.run_analysis()

    def action_about_openpulse_callback(self):
        AboutOpenPulseInput()

    def action_show_mesh_nodes_callback(self, cond):
        self.action_show_geometry_points.blockSignals(True)
        status = self.action_show_geometry_points.isChecked()
        self.action_show_geometry_points.setChecked(status and not cond)
        self.action_show_geometry_points.blockSignals(False)
        self._update_visualization()
    
    def action_show_geometry_points_callback(self, cond):
        self.action_show_mesh_nodes.blockSignals(True)
        status = self.action_show_mesh_nodes.isChecked()
        self.action_show_mesh_nodes.setChecked(status and not cond)
        self.action_show_mesh_nodes.blockSignals(False)
        self._update_visualization()

    def action_show_lines_callback(self, cond):
        self._update_visualization()

    def action_show_tubes_callback(self, cond):
        self._update_visualization()

    def action_show_symbols_callback(self, cond):
        self._update_visualization()
    
    def action_show_transparent_callback(self, cond):
        self._update_visualization()
    
    def action_select_elements_callback(self, cond):
        self._update_visualization()

    def action_plot_default_color_callback(self):
        self.set_color_mode(ColorMode.EMPTY)

    def action_plot_material_callback(self):
        self.set_color_mode(ColorMode.MATERIAL)

    def action_plot_fluid_callback(self):
        self.set_color_mode(ColorMode.FLUID)

    def get_color_mode(self):
        return self.visualization_filter.color_mode
    
    def set_color_mode(self, color_mode):
        self.visualization_filter.color_mode = color_mode
        self.visualization_changed.emit()

    def update_export_geometry_file_access(self):
        import_type = app().project.model.mesh.import_type
        if import_type == 0:
            self.action_export_geometry.setDisabled(True)
        elif import_type == 1:
            self.action_export_geometry.setDisabled(False)

    def action_import_geometry_callback(self):
        obj = ImportGeometry()
        self.initial_project_action(obj.complete)

    def _add_mesh_toolbar(self):
        self.mesh_toolbar = MeshToolbar()
        self.addToolBar(self.mesh_toolbar)
        self.insertToolBarBreak(self.mesh_toolbar)

    def _enable_menus_at_start(self):
        pass

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
        self.update_theme = True

    def action_set_dark_theme_callback(self):
        self.set_theme("dark")

    def action_set_light_theme_callback(self):
        self.set_theme("light")
    
    def set_theme(self, theme):
        if theme not in ["light", "dark"]:
            return
    
        self.update_themes_in_file(theme)
        if self.interface_theme == theme:
            return
        
        self.custom_colors = {}
        if theme == "dark":
            self.custom_colors["[dark]"] = {"toolbar.background": "#202124"}
            icon_color = QColor("#5f9af4")

        elif theme == "light":
            icon_color = QColor("#1a73e8")
    
        self.interface_theme = theme
        qdarktheme.setup_theme(theme, custom_colors=self.custom_colors)
        self.theme_changed.emit(theme)
        
        self.action_set_light_theme.setDisabled(theme == "light")
        self.action_set_dark_theme.setDisabled(theme == "dark")
        self._load_stylesheets()

        # paint the icons of every children widget
        widgets = self.findChildren((QAbstractButton, QAction))
        icons.change_icon_color_for_widgets(widgets, icon_color)

        # TODO: Connect this via signaling
        self.geometry_widget.set_theme(theme)

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
            # self.opv_widget.set_user_interface_preferences(self.user_preferences)

    def savePNG_call(self):

        last_path = app().config.get_last_folder_for("exported image folder")
        if last_path is None:
            last_path = str(Path().home())

        path, check = self.file_dialog.get_save_file_name(
                                                            'Save Captured Image', 
                                                            last_path, 
                                                            'PNG File (*.png)'
                                                          )

        if not check:
            return

        # TODO: reimplement this
        # self.opv_widget().savePNG(path)

    def positioning_cursor_on_widget(self, widget):
        width, height = widget.width(), widget.height()
        final_pos = widget.mapToGlobal(QPoint(int(width/2), int(height/2)))
        QCursor.setPos(final_pos)
    
    def new_project(self):
        self.reset_geometry_render()
        obj = NewProjectInput()
        self.initial_project_action(obj.complete)
        return obj.complete

    # def new_project(self):
    #     # TODO: remove repeated
    #     if not self.input_ui.new_project():
    #         return 
    #     self._update_recent_projects()
    #     self.set_window_title(self.file._project_name)
    #     self.use_structural_setup_workspace()
    #     self.update_plots()

    def open_project(self, project_path: str | Path | None = None):
        def tmp():
            self.reset_geometry_render()

            if project_path is not None:
                app().config.add_recent_file(project_path)
                app().config.write_last_folder_path_in_file("project folder", project_path)
                copy(project_path, TEMP_PROJECT_FILE)
                self.update_window_title(project_path)

            self.project.load_project()
            self.mesh_toolbar.update_mesh_attributes()

            if project_path is not None:
                path = Path(project_path)
                self.project.name = path.stem
                self.project.save_path = path

            self.initial_project_action(True)
            self._update_recent_projects()
            self.update_plots()
            self.action_front_view_callback()
        
        LoadingWindow(tmp).run()

    # def open_project(self, path=None):
    #     # TODO: remove repeated
    #     def tmp():
    #         logging.info("Loading project [1/3]")
    #         if not self.input_ui.load_project(path):
    #             return False

    #         logging.info("Update recent projects [2/3]")
    #         self._update_recent_projects()

    #         logging.info("Configuring visualization [3/3]")
    #         self.set_window_title(self.file._project_name)
    #         self.update_plots()
    #         self.action_front_view_callback()
    #         return True

    #     LoadingWindow(tmp).run()

    def open_project_dialog(self):

        last_path = app().config.get_last_folder_for("project folder")
        if last_path is None:
            last_path = str(Path().home())

        project_path, check = self.file_dialog.get_open_file_name(
                                                                    "Open Project", 
                                                                    last_path, 
                                                                    filter = "Pulse File (*.pulse)"
                                                                  )

        if not check:
            return True

        self.open_project(project_path)

    def save_project_dialog(self):
        if self.project.save_path is None:
            return self.save_project_as_dialog()
        else:
            self.save_project_as(self.project.save_path)
            return True

    def save_project_as_dialog(self):

        obj = SaveProjectDataSelector()
        if obj.complete:

            last_path = app().config.get_last_folder_for("project folder")
            if last_path is None:
                last_path = str(Path.home())

            file_path, check = self.file_dialog.get_save_file_name(
                                                                    "Save As",
                                                                    last_path,
                                                                    filter = "Pulse File (*.pulse)",
                                                                  )

            if not check:
                return

            if obj.ignore_results_data:
                pass
                # self.ulse_file.remove_results_data_from_project_file()
            
            if obj.ignore_mesh_data:
                pass
                # self.pulse_file.remove_mesh_data_from_project_file()

            self.save_project_as(file_path)

        return obj.complete

    def save_project_as(self, path):
        path = Path(path)
        self.project.name = path.stem
        self.project.save_path = path
        app().pulse_file.write_thumbnail()
        app().config.add_recent_file(path)
        app().config.write_last_folder_path_in_file("project folder", path)
        # self.project_menu.update_recents_menu()
        copy(TEMP_PROJECT_FILE, path)
        self.update_window_title(path)
        self.project_data_modified = False

    def update_window_title(self, project_path : str | Path):
        if isinstance(project_path, str):
            project_path = Path(project_path)
        project_name = project_path.stem
        self.setWindowTitle(f"{project_name}")

    def set_input_widget(self, dialog):
        self.dialog = dialog

    def close_dialogs(self):
        if isinstance(self.dialog, (QDialog, QWidget)):
            self.dialog.close()
            self.set_input_widget(None)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ShortcutOverride:
            if event.key() == Qt.Key_E:
                self.combo_box_workspaces.setCurrentIndex(0)
            elif event.key() == Qt.Key_S:
                self.combo_box_workspaces.setCurrentIndex(1)
            elif event.key() == Qt.Key_A:
                self.combo_box_workspaces.setCurrentIndex(2)
            elif event.key() == Qt.Key_R:
                self.combo_box_workspaces.setCurrentIndex(3)
            elif event.key() == Qt.Key_F5:
                self.update_plots()
        return super(MainWindow, self).eventFilter(obj, event)

    def closeEvent(self, event: QCloseEvent | None) -> None:
        self.close_app()
        event.ignore()

    def close_app(self):
        self.close_dialogs()

        condition_1 = self.project.save_path is None
        condition_2 = os.path.exists(TEMP_PROJECT_FILE)
        condition_3 = self.project_data_modified
        condition = (condition_1 and condition_2) or condition_3

        if condition:
            close = QMessageBox.question(   
                                            self, 
                                            "QUIT", 
                                            "Would you like to save the project data before exit?", 
                                            QMessageBox.Cancel | QMessageBox.Discard | QMessageBox.Save
                                        )

            if close == QMessageBox.Cancel:
                return

            elif close == QMessageBox.Save:
                if not self.save_project_dialog():
                    return

        else:
            close = QMessageBox.question(
                                            self, 
                                            "QUIT", 
                                            "Would you like to close the application?", 
                                            QMessageBox.Yes | QMessageBox.No
                                        )

            if close == QMessageBox.No:
                return

        # self.user_config.save()
        self.reset_temporary_folder()
        self.mesh_widget.render_interactor.Finalize()
        self.results_widget.render_interactor.Finalize()
        sys.exit()

    def _create_status_bar(self):
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)

    def update_status_bar_info(self):
        self.status_bar.update_mesh_information()
        self.status_bar.update_geometry_information()

def create_new_folder(path : Path, folder_name : str) -> Path:
    folder_path = path / folder_name
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    return folder_path