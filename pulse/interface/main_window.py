from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QSplitter, QStackedWidget, QLabel, QToolBar, QComboBox, QSizePolicy
from PyQt5 import uic
from pathlib import Path

from pulse import app
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget
from data.user_input.model.geometry.geometry_designer import OPPGeometryDesignerInput

from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget


UI_DIR = Path('pulse/interface/ui_files/')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_DIR / 'main_window.ui', self)

        self._config_window()
        self._define_qt_variables()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()

        self.use_geometry_workspace()

    # public
    def use_geometry_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.geometry_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def use_mesh_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.mesh_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)

    def use_results_workspace(self):
        self.setup_widgets_stack.setCurrentWidget(self.results_input_wigdet)
        self.render_widgets_stack.setCurrentWidget(self.results_widget)  

    # internal
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
        self.action_mesh_workspace: QAction
        self.action_results_workspace: QAction
        self.tool_bar: QToolBar
        self.splitter: QSplitter

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
            self.action_mesh_workspace,
            self.action_results_workspace
        ]
        combo_box = QComboBox()
        for action in actions:
            action: QAction 
            combo_box.addItem(action.text())
        combo_box.currentIndexChanged.connect(lambda x: actions[x].trigger())
        self.tool_bar.addWidget(combo_box)

    def _create_layout(self):
        editor = app().geometry_toolbox.editor

        self.mesh_widget = MeshRenderWidget()
        self.geometry_widget = EditorRenderWidget(editor)
        self.results_widget = QLabel("RESULTS")
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)
        self.render_widgets_stack.addWidget(self.results_widget)

        self.geometry_input_wigdet = OPPGeometryDesignerInput(self.geometry_widget)
        self.mesh_input_wigdet = QLabel("mesh")
        self.results_input_wigdet = QLabel("results")
        self.setup_widgets_stack.addWidget(self.geometry_input_wigdet)
        self.setup_widgets_stack.addWidget(self.mesh_input_wigdet)
        self.setup_widgets_stack.addWidget(self.results_input_wigdet)

        self.splitter.setSizes([100, 400])

    # callbacks
    def action_geometry_workspace_callback(self):
        self.use_geometry_workspace()

    def action_mesh_workspace_callback(self):
        self.use_mesh_workspace()

    def action_results_workspace_callback(self):
        self.use_results_workspace()
