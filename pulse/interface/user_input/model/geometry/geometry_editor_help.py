from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface.ui_generated.model.geometry.help.geometry_editor_help_ui import GeometryEditorHelp_UI



class GeometryEditorHelp(GeometryEditorHelp_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = app().main_window
        self.project = app().project

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):
        pass

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Quick manual")
        self.setWindowIcon(app().main_window.pulse_icon)

    def _define_qt_variables(self):
        self.pushButton_close : QPushButton
        self.pushButton_tutorial : QPushButton

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_tutorial.clicked.connect(self.show_tutorial)

    def show_tutorial(self):
        pass