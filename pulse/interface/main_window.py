import sys
from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction, QSplitter, QStackedWidget, QLabel, QToolBar, QComboBox, QSizePolicy
from PyQt5 import uic
from pathlib import Path

from pulse import app
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget
from pulse.uix.menu.Menu import Menu
from pulse.uix.input_ui import InputUi
from pulse.uix.opv_ui import OPVUi
from pulse.uix.mesh_toolbar import MeshToolbar


from data.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

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

    def load_project(self, path=None):
        if not self.input_widget.loadProject(self.config, path):
            return 

        self._update_recent_projects()
        self.set_window_title(self.project.file._project_name)
        self.update()

    def update(self):
        self.geometry_widget.update_plot(reset_camera=True)
        self.mesh_widget.update_plot(reset_camera=True)

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
            self.load_project(config.getMostRecentProjectDir())
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
            import_action.triggered.connect(partial(self.load_project, path))
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
        future maintainers and to help the code editor with
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

    # callbacks
    def action_new_project_callback(self):
        self.new_project()

    def action_load_project_callback(self):
        self.load_project()

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
