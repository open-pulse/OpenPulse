from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QSplitter, QStackedWidget, QLabel, QToolBar, QComboBox
from PyQt5 import uic
from pathlib import Path

from pulse import app
from opps.interface.viewer_3d.render_widgets.editor_render_widget import EditorRenderWidget
from pulse.interface.viewer_3d.render_widgets import MeshRenderWidget


UI_DIR = Path('pulse/interface/ui_files/')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi(UI_DIR / 'main_window.ui', self)

        self._config_window()
        self._connect_actions()
        self._create_layout()
        self._create_workspaces_toolbar()

    def _config_window(self):
        self.showMaximized()
        self.installEventFilter(self)

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

        # All the setup widgets (left side of the screen) are placed here
        self.setup_widgets_stack = QStackedWidget()
        self.setup_widgets_stack.addWidget(QLabel("Hello"))

        # All the render widgets are placed here
        self.render_widgets_stack = QStackedWidget()
        self.render_widgets_stack.addWidget(self.mesh_widget)
        self.render_widgets_stack.addWidget(self.geometry_widget)

        working_area = QSplitter(Qt.Horizontal)
        working_area.addWidget(self.setup_widgets_stack)
        working_area.addWidget(self.render_widgets_stack)
        working_area.setSizes([100,400])
        self.setCentralWidget(working_area)

    def action_geometry_workspace_callback(self):
        self.render_widgets_stack.setCurrentWidget(self.geometry_widget)

    def action_mesh_workspace_callback(self):
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)  

    def action_results_workspace_callback(self):
        self.render_widgets_stack.setCurrentWidget(self.mesh_widget)  
