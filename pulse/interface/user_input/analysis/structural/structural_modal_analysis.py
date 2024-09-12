from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput

from math import pi
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class StructuralModalAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/structural/modal_analysis.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._load_analysis_setup()
        self.exec()

    def _initialize(self):
        self.modes = None
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QLineEdit
        self.lineEdit_number_modes : QLineEdit
        self.lineEdit_sigma_factor : QLineEdit

        # QPushButton
        self.pushButton_run_analysis : QPushButton

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis)

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
            self.text_data = [window_title_1, title, message]
            return True

        else:

            try:
                self.modes = int(self.lineEdit_number_modes.text())
            except Exception:
                message = "Invalid input value for number of modes."
                self.text_data = [window_title_1, title, message]
                return True

            try:
                self.sigma_factor = float(self.lineEdit_sigma_factor.text())
            except Exception:
                message = "Invalid input value for sigma factor."
                self.text_data = [window_title_1, title, message]
                return True
            
        return False
    
    def run_analysis(self):
        if self.check_analysis_inputs():
            PrintMessageInput(self.text_data)
            return
        self.complete = True
        self.close()

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis()
        elif event.key() == Qt.Key_Escape:
            self.close()