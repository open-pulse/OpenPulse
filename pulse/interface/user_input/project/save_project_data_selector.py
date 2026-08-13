from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent

from pulse import TEMP_PROJECT_DIR, app
from pulse.interface.ui_generated.project.save_project_data_selector_ui import (
    SaveProjectDataSelector_UI,
)


class SaveProjectDataSelector(SaveProjectDataSelector_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.lineEdit_required_memory.setDisabled(True)

    def _create_connections(self):
        # QCheckBox
        self.checkBox_mesh_data.stateChanged.connect(self.remove_solution_data)

        # QCheckBox
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_proceed.clicked.connect(self.proceed_callback)

    def get_required_memory(self):
        total_size = sum(f.stat().st_size for f in TEMP_PROJECT_DIR.rglob("*") if f.is_file())
        size_of_file = total_size / 1e6
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.proceed_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)