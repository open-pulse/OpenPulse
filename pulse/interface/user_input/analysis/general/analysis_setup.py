from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
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

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.analysis_ID = self.project.analysis_ID
        self.opv = self.main_window.opv_widget
        app().main_window.input_widget.set_input_widget(self)

        if self.analysis_ID in [1, 6]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_mode_superposition_method.ui"
        elif self.analysis_ID in [0, 5]:
            ui_path = UI_DIR / "analysis/structural/harmonic_analysis_direct_method.ui"
        elif self.analysis_ID in [3]:
            ui_path = UI_DIR / "analysis/acoustic/harmonic_analysis_direct_method.ui"
        elif self.analysis_ID == 7:
            read = StaticAnalysisInput()
            self.complete = self.flag_run = read.complete
            return
        else:
            return

        uic.loadUi(ui_path, self)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()

        self.update_frequency_setup_input_texts()
        self.update_damping_input_texts()
        self.exec()

    def _initialize(self):
        self.complete = False
        self.flag_run = False
        self.frequencies = []
        self.modes = 0
        #
        self.title = self.project.analysis_type_label
        self.subtitle = self.project.analysis_method_label
        self.f_min = self.project.f_min
        self.f_max = self.project.f_max
        self.f_step = self.project.f_step
        self.global_damping = self.project.global_damping

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Analysis setup")

    def _define_qt_variables(self):
        # QLabel
        self.label_title : QLabel
        self.label_subtitle : QLabel
        self.label_title.setText(self.title)
        self.label_subtitle.setText(self.subtitle)
        
        # QLineEdit

        if self.analysis_ID == 1:
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
        self.enter_setup_button.clicked.connect(self.check_exit)
        self.run_analysis_button.clicked.connect(self.check_run)
        self.tabWidget.currentChanged.connect(self.tabEvent)

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def update_damping_input_texts(self):
        if self.analysis_ID not in [2,3,4]:
            if self.global_damping != [0,0,0,0]:
                self.lineEdit_av.setText(str(self.global_damping[0]))
                self.lineEdit_bv.setText(str(self.global_damping[1]))
                self.lineEdit_ah.setText(str(self.global_damping[2]))
                self.lineEdit_bh.setText(str(self.global_damping[3]))

    def update_frequency_setup_input_texts(self):
        if self.f_step != 0:
            self.lineEdit_fmin.setText(str(self.f_min))
            self.lineEdit_fmax.setText(str(self.f_max))
            self.lineEdit_fstep.setText(str(self.f_step))
            if self.project.file.check_if_there_are_tables_at_the_model():
                self.lineEdit_fmin.setDisabled(True)
                self.lineEdit_fmax.setDisabled(True)
                self.lineEdit_fstep.setDisabled(True)

    def check_exit(self):
        input_fmin = input_fmax = input_fstep = 0
        if self.analysis_ID not in [2, 4]:

            if self.analysis_ID in [1, 6]:
                self.modes = self.check_inputs(self.lineEdit_modes, "'number of modes'")
                if self.stop:
                    self.lineEdit_modes.setFocus()
                    return True

            input_fmin = self.check_inputs(self.lineEdit_fmin, "'minimum frequency'", zero_included=True, _float=True)
            if self.stop:
                self.lineEdit_fmin.setFocus()
                return True

            input_fmax = self.check_inputs(self.lineEdit_fmax, "'maximum frequency'", _float=True)
            if self.stop:
                self.lineEdit_fmax.setFocus()
                return True

            input_fstep = self.check_inputs(self.lineEdit_fstep, "'frequency resolution (df)'", _float=True)
            if self.stop:
                self.lineEdit_fstep.setFocus()
                return True

            if input_fmax < input_fmin + input_fstep:
                title = "Invalid frequency setup"
                message = "The maximum frequency (fmax) must be greater than \n"
                message += "the sum between minimum frequency (fmin) and \n"
                message += "frequency resolution (df)."
                PrintMessageInput([window_title, title, message])
                return True

        alpha_v = beta_v = alpha_h = beta_h = 0.0
        
        if self.analysis_ID in [0, 1, 5, 6]:    

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

        self.global_damping = [alpha_v, beta_v, alpha_h, beta_h]
        self.project.set_structural_damping(self.global_damping)

        if self.project.file.check_if_there_are_tables_at_the_model():
            self.frequencies = self.project.frequencies
        else:
            self.frequencies = np.arange(input_fmin, input_fmax+input_fstep, input_fstep)
            self.project.set_frequencies(self.frequencies, input_fmin, input_fmax, input_fstep)
        
        if not self.analysis_ID in [3,4]:
            self.project.set_modes_sigma(self.modes)

        self.project.update_project_analysis_setup_state(True)
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
        if self.check_exit():
            return
        self.flag_run = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()