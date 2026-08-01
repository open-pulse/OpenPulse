
from PySide6.QtCore import Qt

from pulse import app
from pulse.interface import error_title
from pulse.interface.ui_generated.analysis.structural.modal_analysis_ui import (
    ModalAnalysis_UI,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model import AnalysisID


class ModalAnalysisInput(ModalAnalysis_UI):
    def __init__(self, analysis_id: AnalysisID, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.close_dialogs()
        app().main_window.set_input_widget(self)

        self.analysis_id = analysis_id

        self._initialize()
        self._config_window()
        self._update_modal_analysis_title()
        self._create_connections()
        self._load_analysis_setup()
        self.exec()

    def _initialize(self):
        self.number_of_modes = None
        self.setup_defined = False
        self.proceed_solution = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _update_modal_analysis_title(self):
        if self.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            self.label_title.setText("Acoustic modal analysis setup")

        elif self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.label_title.setText("Structural modal analysis setup")

    def _create_connections(self):
        self.pushButton_run_analysis.clicked.connect(self.run_analysis_callback)
        self.pushButton_enter_setup.clicked.connect(self.enter_setup_callback)

    def _load_analysis_setup(self):

        analysis_setup = app().project.file.read_analysis_setup_from_file()
        if not isinstance(analysis_setup, dict):
            return

        if AnalysisID.is_modal(analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)):
            number_of_modes = analysis_setup.get("number_of_modes")
            sigma = analysis_setup.get("sigma_factor")
            self.lineEdit_number_modes.setText(str(number_of_modes))
            self.lineEdit_sigma_factor.setText(str(sigma))

    def check_analysis_inputs(self):

        title = "Invalid input value"

        if self.lineEdit_number_modes.text() == "":
            message = "Invalid a value to the number of modes."
            PrintMessageInput([error_title, title, message])
            return True

        else:

            try:
                self.number_of_modes = int(self.lineEdit_number_modes.text())
            except Exception:
                message = "Invalid input value for number of modes."
                PrintMessageInput([error_title, title, message])
                return True

            try:
                self.sigma_factor = float(self.lineEdit_sigma_factor.text())
            except Exception:
                message = "Invalid input value for sigma factor."
                PrintMessageInput([error_title, title, message])
                return True

        return False

    def enter_setup_callback(self):

        if self.check_analysis_inputs():
            return True
        
        analysis_id = app().main_window.analysis_toolbar.get_current_analysis_id()
        analysis_domain = app().main_window.analysis_toolbar.combo_box_physical_domain.currentText().lower()

        analysis_setup = {
            "analysis_id": analysis_id,
            "analysis_type" : "modal",
            "analysis_domain" : analysis_domain,
            "number_of_modes": self.number_of_modes,
            "sigma_factor": self.sigma_factor,
        }

        app().project.model.reset_analysis_setup()
        app().project.model.set_analysis_setup(analysis_setup)

        self.setup_defined = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def confirm(self):
        self.proceed_solution = True
        app().main_window.analysis_toolbar.enable_pushbutons.emit()
        self.close()

    def run_analysis_callback(self):
        if self.enter_setup_callback():
            return

        self.confirm()

    def button_clicked(self):
        self.check_analysis_inputs()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.run_analysis_callback()

        elif event.key() == Qt.Key_Escape:
            self.close()