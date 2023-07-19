from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path
import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

window_title = "ERROR"

class AnalysisSetupInput(QDialog):
    def __init__(self, project):
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
        |--------------------------------------------------------------------|
        """

        self.project = project
        self.analysis_ID = project.analysis_ID

        if self.analysis_ID in [1,6]:
            ui_path = Path('data/user_input/ui/Analysis/Structural/analysisSetupInput_HarmonicAnalysisModeSuperpositionMethod.ui')
        elif self.analysis_ID in [0,5]:
            ui_path = Path('data/user_input/ui/Analysis/Structural/analysisSetupInput_HarmonicAnalysisDirectMethod.ui')
        elif self.analysis_ID in [3]:
            ui_path = Path('data/user_input/ui/Analysis/Acoustic/analysisSetupInput_HarmonicAnalysisDirectMethod.ui')
        else:
            return
        uic.loadUi(ui_path, self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        title = project.analysis_type_label
        subtitle = project.analysis_method_label
        
        self.complete = False
        self.flag_run = False
        self.frequencies = []

        self.f_min = project.f_min
        self.f_max = project.f_max
        self.f_step = project.f_step

        self.global_damping = project.global_damping
        self.modes = 0

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_subtitle = self.findChild(QLabel, 'label_subtitle')

        if self.analysis_ID == 1:
            self.lineEdit_modes = self.findChild(QLineEdit, 'lineEdit_modes')

        self.lineEdit_av = self.findChild(QLineEdit, 'lineEdit_av')
        self.lineEdit_bv = self.findChild(QLineEdit, 'lineEdit_bv')
        self.lineEdit_ah = self.findChild(QLineEdit, 'lineEdit_ah')
        self.lineEdit_bh = self.findChild(QLineEdit, 'lineEdit_bh')
        
        self.lineEdit_fmin = self.findChild(QLineEdit, 'lineEdit_min')
        self.lineEdit_fmax = self.findChild(QLineEdit, 'lineEdit_max')
        self.lineEdit_fstep = self.findChild(QLineEdit, 'lineEdit_step')

        self.pushButton_confirm_close = self.findChild(QPushButton, 'pushButton_confirm_close')
        self.pushButton_confirm_close.clicked.connect(self.check_exit)
        self.pushButton_confirm_run_analysis = self.findChild(QPushButton, 'pushButton_confirm_run_analysis')
        self.pushButton_confirm_run_analysis.clicked.connect(self.check_run)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)
        self.currentTab = self.tabWidget.currentIndex()
        
        self.label_title.setText(title)
        self.label_subtitle.setText(subtitle)

        self.update_frequency_setup_input_texts()
        self.update_damping_input_texts()
        
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()

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
        if self.analysis_ID not in [2,4]:
            
            if self.analysis_ID == 1:
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
                PrintMessageInput([title, message, window_title])
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
            PrintMessageInput([title, message, window_title])                   
            self.stop = True
            return None
        return out

    def check_run(self):
        if self.check_exit():
            return
        self.flag_run = True
        