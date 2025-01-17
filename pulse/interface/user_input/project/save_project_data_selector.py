# fmt: off

from PySide6.QtWidgets import QCheckBox, QDialog, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import app, UI_DIR, TEMP_PROJECT_FILE

from molde import load_ui

import os

window_title_1 = "Error"
window_title_2 = "Warning"


class SaveProjectDataSelector(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/save_project_data_selector.ui"
        load_ui(ui_path, self)

        main_window = app().main_window
        main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()

        self.get_required_memory()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True
        self.complete = False

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_mesh_data : QCheckBox
        self.checkBox_solution_data : QCheckBox

        # QLineEdit
        self.lineEdit_required_memory : QLineEdit
        self.lineEdit_required_memory.setDisabled(True)

        # QPushButton
        self.pushButton_proceed : QPushButton

    def _create_connections(self):
        self.checkBox_mesh_data.stateChanged.connect(self.remove_solution_data)
        self.pushButton_proceed.clicked.connect(self.proceed_callback)

    def get_required_memory(self):
        path = TEMP_PROJECT_FILE
        size_of_file = os.path.getsize(path) / 1e6
        self.lineEdit_required_memory.setText(str(round(size_of_file, 4)))

    def remove_solution_data(self):
        if self.checkBox_mesh_data.isChecked():
            self.checkBox_solution_data.setDisabled(False)
        else:
            self.checkBox_solution_data.setChecked(False)
            self.checkBox_solution_data.setDisabled(True)

    def proceed_callback(self):

        self.ignore_results_data = False
        if not self.checkBox_solution_data.isChecked():
            self.ignore_results_data = True
        
        self.ignore_mesh_data = False
        if not self.checkBox_mesh_data.isChecked():
            self.ignore_mesh_data = True

        self.complete = True
        self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)

# fmt: on