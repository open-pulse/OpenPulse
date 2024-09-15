from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.analysis.structural.static_analysis_input import StaticAnalysisInput
from pulse.interface.user_input.project.print_message import PrintMessageInput

import numpy as np

window_title = "Error"

class AnalysisSetupInput(QDialog):
    def __init__(self):
        super().__init__()

        """
        |--------------------------------------------------------------------|
        |                    Analysis ID codification                        |
        |--------------------------------------------------------------------|
        |    0 - Structural - Harmonic analysis through direct method        |
        |    1 - Structural - Harmonic analysis through mode superposition   |
        |    2 - Structural - Modal analysis                                 |
        |    3 - Acoustic - Harmonic analysis through direct method          |
        |    4 - Acoustic - Modal analysis (convetional FE 1D)               |
        |    5 - Coupled - Harmonic analysis through direct method           |
        |    6 - Coupled - Harmonic analysis through mode superposition      |
        |    7 - Structural - Static analysis (under development)            |
        |--------------------------------------------------------------------|
        """
        self.analysis_id = app().project.analysis_id

        if self.analysis_id in [1, 6]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_mode_superposition_method.ui"
        elif self.analysis_id in [0, 5]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_direct_method.ui"
        elif self.analysis_id in [3]:
            ui_path = UI_DIR / "analysis/acoustic/harmonic_analysis_direct_method.ui"
        # elif self.analysis_id == 7:
        #     read = StaticAnalysisInput()
        #     self.complete = self.flag_run = read.complete
        #     return
        else:
            return

        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self.project = app().project
        self.model = app().project.model

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        self.update_frequency_setup_input_texts()
        self.update_damping_input_texts()
        self.exec()

    def _initialize(self):
        self.complete = False
        self.flag_run = False
        self.frequencies = list()
        self.modes = 0

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Analysis setup")

    def _define_qt_variables(self):
        # QLabel
        self.label_title : QLabel
        self.label_subtitle : QLabel
        self.label_title.setText(app().project.analysis_type_label)
        self.label_subtitle.setText(app().project.analysis_method_label)
        
        # QLineEdit

        if self.analysis_id == 1:
            self.lineEdit_modes : QLineEdit
    
        self.lineEdit_av : QLineEdit
        self.lineEdit_bv : QLineEdit
        self.lineEdit_ah : QLineEdit
        self.lineEdit_bh : QLineEdit
        self.lineEdit_fmin : QLineEdit
        self.lineEdit_fmax : QLineEdit
        self.lineEdit_fstep : QLineEdit
        
        # QPushButton
        self.enter_setup_button : QPushButton
        self.run_analysis_button : QPushButton

        # QTabWidget
        self.tabWidget : QTabWidget
        self.currentTab = self.tabWidget.currentIndex()

    def _create_connections(self):
        #
        self.enter_setup_button.clicked.connect(self.enter_setup_callback)
        self.run_analysis_button.clicked.connect(self.check_run)
        #
        self.tabWidget.currentChanged.connect(self.tabEvent)

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def update_damping_input_texts(self):
        if self.analysis_id not in [2, 3, 4]:
            if self.model.global_damping != [0, 0, 0, 0]:
                self.lineEdit_av.setText(str(self.model.global_damping[0]))
                self.lineEdit_bv.setText(str(self.model.global_damping[1]))
                self.lineEdit_ah.setText(str(self.model.global_damping[2]))
                self.lineEdit_bh.setText(str(self.model.global_damping[3]))

    def update_frequency_setup_input_texts(self):

        if (self.model.f_min, self.model.f_max, self.model.f_step).count(None):
            f_min = 0
            f_max = 200
            f_step = 1

        else:
            f_min = self.model.f_min
            f_max = self.model.f_max
            f_step = self.model.f_step

        if f_step != 0:

            self.lineEdit_fmin.setText(str(f_min))
            self.lineEdit_fmax.setText(str(f_max))
            self.lineEdit_fstep.setText(str(f_step))

            if app().project.model.properties.check_if_there_are_tables_at_the_model():
                self.lineEdit_fmin.setDisabled(True)
                self.lineEdit_fmax.setDisabled(True)
                self.lineEdit_fstep.setDisabled(True)

    def enter_setup_callback(self):

        analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()
        
        analysis_setup["analysis_id"] = self.analysis_id

        f_min = f_max = f_step = 0.

        if self.analysis_id not in [2, 4]:

            if self.analysis_id in [1, 6]:
                number_of_modes = self.check_inputs(self.lineEdit_modes, "'number of modes'")
                if self.stop:
                    self.lineEdit_modes.setFocus()
                    return True

            f_min = self.check_inputs(self.lineEdit_fmin, "'minimum frequency'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_fmin.setFocus()
                return True

            f_max = self.check_inputs(self.lineEdit_fmax, "'maximum frequency'", _float=True)
            if self.stop:
                self.lineEdit_fmax.setFocus()
                return True

            f_step = self.check_inputs(self.lineEdit_fstep, "'frequency resolution (df)'", _float=True)
            if self.stop:
                self.lineEdit_fstep.setFocus()
                return True

            if f_max < f_min + f_step:
                title = "Invalid frequency setup"
                message = "The maximum frequency (fmax) must be greater than \n"
                message += "the sum between minimum frequency (fmin) and \n"
                message += "frequency resolution (df)."
                PrintMessageInput([window_title, title, message])
                return True
            
            analysis_setup["f_min"] = f_min
            analysis_setup["f_max"] = f_max
            analysis_setup["f_step"] = f_step

        alpha_v = beta_v = alpha_h = beta_h = 0.0
        
        if self.analysis_id in [0, 1, 5, 6]:    

            alpha_v = self.check_inputs(self.lineEdit_av, "'proportional viscous damping (alpha_v)'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_av.setFocus()
                return True

            beta_v = self.check_inputs(self.lineEdit_bv, "'proportional viscous damping (beta_v)'", zero_included=True,  _float=True)
            if self.stop:
                self.lineEdit_bv.setFocus()
                return True

            alpha_h = self.check_inputs(self.lineEdit_ah, "'proportional hysteretic damping (alpha_h)'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_ah.setFocus()
                return True

            beta_h = self.check_inputs(self.lineEdit_bh, "'proportional hysteretic damping (beta_h)'", zero_included=True,  _float=True)
            if self.stop:
                self.lineEdit_bh.setFocus()
                return True

        global_damping = [alpha_v, beta_v, alpha_h, beta_h]
        analysis_setup["global_damping"] = global_damping
        self.model.set_global_damping(analysis_setup)

        if app().project.model.properties.check_if_there_are_tables_at_the_model():
            self.frequencies = self.model.frequencies
        else:
            self.model.set_frequency_setup(analysis_setup)

        if self.analysis_id in [1, 6]:
            analysis_setup["modes"] = number_of_modes

        app().pulse_file.write_analysis_setup_in_file(analysis_setup)
        app().main_window.analysis_toolbar.pushButton_run_analysis.setEnabled(True)

        self.complete = True
        self.close()

        return False

    def check_inputs(self, lineEdit, label, only_positive=True, zero_included=False, _float=False):
        self.stop = False
        message = ""
        title = "Invalid input to the analysis setup"
        if lineEdit.text() != "":
            try:

                if _float:
                    out = float(lineEdit.text())
                else:
                    out = int(lineEdit.text())

                if only_positive:
                    if zero_included:
                        if out < 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is allowed."
                    else:
                        if out <= 0:
                            message = f"Insert a positive value to the {label}."
                            message += "\n\nNote: zero value is not allowed."

            except Exception as _err:
                message = "Dear user, you have typed and invalid value at the \n"
                message += f"{label} input field.\n\n"
                message += str(_err)

        else:

            if zero_included:
                return float(0)
            else: 
                message = f"Insert some value at the {label} input field."
        
        if message != "":
            PrintMessageInput([window_title, title, message])                   
            self.stop = True
            return None
        return out

    def check_run(self):
        if self.enter_setup_callback():
            return
        self.flag_run = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()