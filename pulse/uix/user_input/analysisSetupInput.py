from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QPushButton
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np

class AnalysisSetupInput(QDialog):
    def __init__(self, project, f_min = 0, f_max = 0, f_step = 0):
        super().__init__()

        self.analysis_ID = project.analysis_ID

        if self.analysis_ID in [1,6]:
            uic.loadUi('pulse/uix/user_input/ui/analysisSetupInput_ModeSuperpositionMethod.ui', self)
        elif self.analysis_ID in [0,3,5]:
            uic.loadUi('pulse/uix/user_input/ui/analysisSetupInput_DirectMethod.ui', self)
        else:
            return

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        title = project.analysis_type_label
        subtitle = project.analysis_method_label
        
        self.complete = False
        self.flag_run = False
        self.frequencies = []

        self.f_min = f_min
        self.f_max = f_max
        self.f_step = f_step

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
        
        if self.f_step != 0:
            self.lineEdit_fmin.setText(str(self.f_min))
            self.lineEdit_fmax.setText(str(self.f_max))
            self.lineEdit_fstep.setText(str(self.f_step))

        if True in [True if damp != 0 else False for damp in self.global_damping]:
            self.lineEdit_av.setText(str(self.global_damping[0]))
            self.lineEdit_bv.setText(str(self.global_damping[1]))
            self.lineEdit_ah.setText(str(self.global_damping[2]))
            self.lineEdit_bh.setText(str(self.global_damping[3]))

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check_run()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def check_exit(self):
        input_fmin = input_fmax = input_fstep = 0
        if self.analysis_ID not in [2,4]:
            #Verify Modes
            if self.analysis_ID == 1:
                if self.lineEdit_modes.text() == "":
                    error("Insert a value (modes)")
                    return
                else:
                    try:
                        self.modes = int(self.lineEdit_modes.text())
                    except Exception:
                        error("Value error (modes)")
                        return

            if self.lineEdit_fmin.text() == "":
                error("Insert a value (freq min)")
                return
            else:
                try:
                    if float(self.lineEdit_fmin.text())>=0:
                        input_fmin = float(self.lineEdit_fmin.text())
                except Exception:
                    error("Value error (freq min)")
                    return

            if self.lineEdit_fmax.text() == "":
                error("Insert a value (freq max)")
                return
            else:
                try:
                    if float(self.lineEdit_fmax.text()) > float(self.lineEdit_fmin.text()) + float(self.lineEdit_fstep.text()):
                        input_fmax = float(self.lineEdit_fmax.text())
                except Exception:
                    error("Value error (freq max)")
                    return

            if self.lineEdit_fstep.text() == "":
                error("Insert a value (freq df)")
                return
            else:
                try:
                    input_fstep = float(self.lineEdit_fstep.text())
                    if float(self.lineEdit_fstep.text())<=0 or float(self.lineEdit_fstep.text())>=float(self.lineEdit_fmax.text()):
                            error(" The value assigned to f_step must be\n greater than 0 and less than f_max! ")
                            return
                except Exception:
                    error("Value error (freq df)")
                    return
                
        alpha_v = beta_v = alpha_h = beta_h = 0
        if self.lineEdit_av.text() != "":
            try:
                alpha_v = float(self.lineEdit_av.text())
            except Exception:
                error("Value error (alpha_v)")
                return

        if self.lineEdit_bv.text() != "":
            try:
                beta_v = float(self.lineEdit_bv.text())
            except Exception:
                error("Value error (beta_v)")
                return

        if self.lineEdit_ah.text() != "":
            try:
                alpha_h = float(self.lineEdit_ah.text())
            except Exception:
                error("Value error (alpha_h)")
                return

        if self.lineEdit_bh.text() != "":
            try:
                beta_h = float(self.lineEdit_bh.text())
            except Exception:
                error("Value error (beta_h)")
                return

        self.global_damping = [alpha_v, beta_v, alpha_h, beta_h]

        self.f_min = input_fmin
        self.f_max = input_fmax
        self.f_step = input_fstep
        self.frequencies = np.arange(input_fmin, input_fmax+input_fstep, input_fstep)
        
        self.complete = True
        self.close()
    
    def check_run(self):
        self.check_exit()
        self.flag_run = True