import sys
from functools import partial
import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QSplitter, QStackedWidget, QLabel, QToolBar, QComboBox, QFileDialog
from PyQt5 import uic
from pathlib import Path

from pulse import app
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget
from pulse.uix.menu.Menu import Menu
from pulse.uix.input_ui import InputUi
from pulse.uix.opv_ui import OPVUi
from pulse.uix.mesh_toolbar import MeshToolbar


from data.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput
from data.user_input.project.call_double_confirmation_input import CallDoubleConfirmationInput

from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget


UI_DIR = Path('pulse/interface/ui_files/')


class MainWindow(QMainWindow):
    permission_changed = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_DIR / 'main_window.ui', self)

        # i am keeping these atributes here to make
        # the transition easier, but it should be
        # defined only in the app.
        self.config = app().config
        self.project = app().project

    def configure_window(self):
        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()
        self._update_recent_projects()
        self._createMeshToolbar()
    
        self.plot_entities_with_cross_section()
        self.loadRecentProject()

    # public
    def new_project(self):
        if not self.input_widget.new_project(self.config):
            return 
        self._update_recent_projects()
        self.set_window_title(self.project.file._project_name)
        self.update()

    def open_project(self, path=None):
        if not self.input_widget.loadProject(self.config, path):
            return 

        self._update_recent_projects()
        self.set_window_title(self.project.file._project_name)
        self.update()

    def update(self):
        self.geometry_widget.update_plot(reset_camera=True)
        self.mesh_widget.update_plot(reset_camera=True)
        self.opv_widget.updatePlots()

    def use_geometry_workspace(self):
        self.combo_box.setCurrentIndex(0)

    def use_structural_setup_workspace(self):
        self.combo_box.setCurrentIndex(1)

    def use_acoustic_setup_workspace(self):
        self.combo_box.setCurrentIndex(2)

    def use_analisys_setup_workspace(self):
        self.combo_box.setCurrentIndex(3)

    def use_results_workspace(self):
        self.combo_box.setCurrentIndex(4)

    def plot_entities(self):
        self.use_structural_setup_workspace()
        self.opv_widget.changePlotToEntities()

    def plot_entities_with_cross_section(self):
        self.use_structural_setup_workspace()
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def plot_mesh(self):
        self.use_structural_setup_workspace()
        self.opv_widget.changePlotToMesh()

    def plot_raw_geometry(self):
        self.use_structural_setup_workspace()
        self.opv_widget.changePlotToRawGeometry()
    
    def plot_geometry_editor(self):
        self.use_geometry_workspace()

    def set_window_title(self, msg=""):
        title = "OpenPulse"
        if (msg != ""):
            title += " - " + msg
        self.setWindowTitle(title)

    def show_get_started_window(self):
        config = app().config

        if config.openLastProject and config.haveRecentProjects():
            self.open_project(config.getMostRecentProjectDir())
        else:
            if self.input_widget.getStarted(config):
                self._loadProjectMenu()
                self.changeWindowTitle(self.project.file._project_name)
                # self.draw()

    # internal
    def _update_recent_projects(self):
        actions = self.menurecent.actions()
        for action in actions:
            self.menurecent.removeAction(action)

        self.menu_actions = []
        for name, path in reversed(self.config.recentProjects.items()):
            import_action = QAction(str(name) + "\t" + str(path))
            import_action.setStatusTip(str(path))
            import_action.triggered.connect(partial(self.open_project, path))
            self.menurecent.addAction(import_action)
            self.menu_actions.append(import_action)

    def _config_window(self):
        self.showMaximized()
        self.installEventFilter(self)
    
    def _define_qt_variables(self):
        '''
        This function is doing nothing. Every variable was
        already defined in the UI file.

        Despite that, it is nice to list the variables to
        help future maintainers and the code editor with
        type inference.
        '''
        self.setup_widgets_stack: QStackedWidget
        self.render_widgets_stack: QStackedWidget
        self.action_geometry_workspace: QAction
        self.action_structural_setup_workspace: QAction
        self.action_acoustic_setup_workspace: QAction
        self.action_analysis_setup_workspace: QAction
        self.action_results_workspace: QAction
        self.tool_bar: QToolBar
        self.splitter: QSplitter
        self.menurecent: QMenu
        self.menu_project: QMenu
        self.menu_graphic: QMenu
        self.menu_general_settings: QMenu
        self.menu_structural_model: QMenu
        self.menu_acoustic_model: QMenu
        self.menu_model_info: QMenu
        self.menu_analysis: QMenu
        self.menu_results_viewer: QMenu
        self.menu_help: QMenu
        self.action_show_points: QAction
        self.action_show_lines: QAction
        self.action_show_tubes: QAction
        self.action_show_symbols: QAction


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
        actions = [
            self.action_geometry_workspace,
            self.action_structural_setup_workspace,
            self.action_acoustic_setup_workspace,
            self.action_analysis_setup_workspace,
            self.action_results_workspace,
        ]
        self.combo_box = QComboBox()
        for action in actions:
            self.combo_box.addItem(action.text())

        self.combo_box.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(self.combo_box)

    def _create_layout(self):
        editor = app().geometry_toolbox.editor

        self.menu_widget = Menu(self)
        self.opv_widget = OPVUi(self.project, self)
        self.opv_widget.opvAnalysisRenderer._createPlayer()
        self.input_widget = InputUi(self.project, self)

        self.mesh_widget = MeshRenderWidget()
        self.geometry_widget = EditorRenderWidget(editor)
        self.geometry_widget.set_theme("light")
        self.results_widget = QLabel("RESULTS")
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.results_widget)
        self.render_widgets_stack.addWidget(self.opv_widget)

        self.geometry_input_wigdet = OPPGeometryDesignerInput(self.geometry_widget)
        self.mesh_input_wigdet = QLabel("mesh")
        self.results_input_wigdet = QLabel("results")
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.mesh_input_wigdet)
        self.setup_widgets_stack.addWidget(self.results_input_wigdet)
        self.setup_widgets_stack.addWidget(self.menu_widget)

        self.splitter.setSizes([120, 400])
        self.opv_widget.updatePlots()
        self.opv_widget.changePlotToEntitiesWithCrossSection()

    def _update_permissions(self):
        pass
    
    def _update_visualization(self):
        points = self.action_show_points.isChecked()
        lines = self.action_show_lines.isChecked()
        tubes = self.action_show_tubes.isChecked()
        symbols = self.action_show_symbols.isChecked()
        self.opv_widget.update_visualization(points, lines, tubes, symbols)
        self.mesh_widget.update_visualization(points, lines, tubes, symbols)

    # callbacks
    def action_new_project_callback(self):
        self.new_project()

    def action_open_project_callback(self):
        self.open_project()

    def action_geometry_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def action_structural_setup_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.menu_widget)
        self.render_widgets_stack.setCurrentWidget(self.opv_widget)

    def action_acoustic_setup_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.mesh_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)

    def action_analysis_setup_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.results_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.results_widget)  

    def action_results_workspace_callback(self):
        self.setup_widgets_stack.setCurrentWidget(self.results_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.results_widget)  

    def action_save_as_png_callback(self):
        self.savePNG_call()
    
    def action_reset_callback(self):
        self.input_widget.reset_project()
    
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

    def action_set_structural_element_type_callback(self):
        self.input_widget.setStructuralElementType()

    def action_add_connecting_flanges_callback(self):
        self.input_widget.add_flanges()

    def action_set_prescribed_dofs_callback(self):
        self.input_widget.setDOF()

    def action_set_nodal_loads_callback(self):
        self.input_widget.setNodalLoads()

    def action_add_mass_spring_damper_callback(self):
        self.input_widget.addMassSpringDamper()

    def action_set_capped_end_callback(self):
        self.input_widget.setcappedEnd()

    def action_set_stress_stiffening_callback(self):
        self.input_widget.set_stress_stress_stiffening()

    def action_add_elastic_nodal_links_callback(self):
        self.input_widget.add_elastic_nodal_links()

    def action_structural_model_info_callback(self):
        self.input_widget.structural_model_info()

    def action_set_acoustic_element_type_callback(self):
        self.input_widget.set_acoustic_element_type()

    def action_set_acoustic_pressure_callback(self):
        self.input_widget.setAcousticPressure()

    def action_set_volume_velocity_callback(self):
        self.input_widget.setVolumeVelocity()

    def action_set_specific_impedance_callback(self):
        self.input_widget.setSpecificImpedance()

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
        self.input_widget.analysisTypeInput()

    def action_analysis_setup_callback(self):
        self.input_widget.analysisSetup()
    
    def action_run_analysis_callback(self):
        self.input_widget.runAnalysis()

    def action_about_openpulse(self):
        self.input_widget.about_OpenPulse()

    def action_show_points_callback(self, cond):
        self._update_visualization()

    def action_show_lines_callback(self, cond):
        self._update_visualization()

    def action_show_tubes_callback(self, cond):
        self._update_visualization()
    
    def action_show_symbols_callback(self, cond):
        self._update_visualization()

    # DEPRECATED, REMOVE AS SOON AS POSSIBLE
    def getInputWidget(self):
        return self.input_widget

    def getMenuWidget(self):
        return self.menu_widget

    def getOPVWidget(self):
        return self.opv_widget

    def getProject(self):
        return self.project
    
    def changeWindowTitle(self, msg = ""):
        self.set_window_title(msg)

    def draw(self):
        self.update()
        self.opv_widget.updatePlots()
        self.plot_entities_with_cross_section()
        self.opv_widget.setCameraView(5)

    def closeEvent(self, event):
        title = "OpenPulse stop execution requested"
        message = "Do you really want to stop the OpenPulse processing and close the current project setup?"

        buttons_config = {"left_button_label" : "No", 
                          "right_button_label" : "Yes",
                          "right_toolTip" : "The current project setup progress has already been saved in the project files."}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)

        if read._stop:
            event.ignore()
            return

        if read._continue:
            sys.exit()
    
    def _loadProjectMenu(self):
        self._update_recent_projects()

    def loadRecentProject(self):
        if self.config.openLastProject and self.config.haveRecentProjects():
            self.importProject_call(self.config.getMostRecentProjectDir())
        else:
            if self.input_widget.getStarted(self.config):
                self._loadProjectMenu()
                self.changeWindowTitle(self.project.file._project_name)
                self.draw()

    def importProject_call(self, path=None):
        if self.input_widget.loadProject(self.config, path):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.file._project_name)
            self.draw()

    def newProject_call(self):
        if self.input_widget.new_project(self.config):
            self._loadProjectMenu()
            self.changeWindowTitle(self.project.file._project_name)
            self.draw()

    def _createMeshToolbar(self):
        self.mesh_toolbar = MeshToolbar(self)
        self.addToolBar(self.mesh_toolbar)
        self.insertToolBarBreak(self.mesh_toolbar)

    def _updateStatusBar(self):
        pass
    
    def set_enable_menuBar(self, *args, **kwargs):
        pass

    def savePNG_call(self):
        project_path = self.project.file._project_path
        if not os.path.exists(project_path):
            project_path = ""
        path, _type = QFileDialog.getSaveFileName(None, 'Save file', project_path, 'PNG (*.png)')
        if path != "":
            self.getOPVWidget().savePNG(path)