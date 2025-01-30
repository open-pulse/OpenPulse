from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

from math import pi
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class StructuralModalAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/structural/modal_analysis.ui"
        load_ui(ui_path, self, UI_DIR)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_analysis_setup()
        self.exec()

    def _initialize(self):
        self.modes = None
        self.setup_defined = False
        self.proceed_solution = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_number_modes: QLineEdit
        self.lineEdit_sigma_factor: QLineEdit

        # QPushButton
        self.pushButton_run_analysis: QPushButton
        self.pushButton_enter_setup: QPushButton

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)

    def _load_analysis_setup(self):
        analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        if isinstance(analysis_setup, dict):
            if analysis_setup["analysis_id"] in [2, 4]:
                modes = analysis_setup["modes"]
                sigma = analysis_setup["sigma_factor"]
                self.lineEdit_number_modes.setText(str(modes))
                self.lineEdit_sigma_factor.setText(str(sigma))

    def check_analysis_inputs(self):

        title = "Invalid input value"

        if self.lineEdit_number_modes.text() == "":
            message = "Invalid a value to the number of modes."
            PrintMessageInput([window_title_1, title, message])
            return True

        else:

            try:
                self.modes = int(self.lineEdit_number_modes.text())
            except Exception:
                message = "Invalid input value for number of modes."
                PrintMessageInput([window_title_1, title, message])
                return True

            try:
                self.sigma_factor = float(self.lineEdit_sigma_factor.text())
            except Exception:
                message = "Invalid input value for sigma factor."
                PrintMessageInput([window_title_1, title, message])
                return True

        return False

    def enter_setup_callback(self):

        if self.check_analysis_inputs():
            return True

        analysis_id = 2
        app().project.set_analysis_id(analysis_id)

        analysis_setup = {
                          "analysis_id" : analysis_id,
                          "modes" : self.modes,
                          "sigma_factor" : self.sigma_factor
                          }

        app().pulse_file.write_analysis_setup_in_file(analysis_setup)
        self.setup_defined = True
        self.close()

    def run_analysis(self):

        if self.enter_setup_callback():
            return

        self.proceed_solution = True

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()