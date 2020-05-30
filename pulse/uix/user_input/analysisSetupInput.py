from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
import numpy as np

class AnalysisSetupInput(QDialog):
    def __init__(self, analysis_ID, title, subtitle, f_min = 0, f_max = 0, f_step = 0):
        super().__init__()
        self.analysis_ID = analysis_ID

        if self.analysis_ID in [1,6]:
            uic.loadUi('pulse/uix/user_input/ui/analysisSetupInput_ModeSuperpositionMethod.ui', self)
        elif self.analysis_ID in [0,3,5]:
            uic.loadUi('pulse/uix/user_input/ui/analysisSetupInput_DirectMethod.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.currentTab = 0

        self.complete = False
        self.frequencies = []

        self.min_frequency = f_min
        self.max_frequency = f_max
        self.step_frequency = f_step

        self.damping = [0,0,0,0]
        self.modes = 0

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_subtitle = self.findChild(QLabel, 'label_subtitle')

        if self.analysis_ID == 1:
            self.lineEdit_modes = self.findChild(QLineEdit, 'lineEdit_modes')

        self.lineEdit_av = self.findChild(QLineEdit, 'lineEdit_av')
        self.lineEdit_bv = self.findChild(QLineEdit, 'lineEdit_bv')
        self.lineEdit_ah = self.findChild(QLineEdit, 'lineEdit_ah')
        self.lineEdit_bh = self.findChild(QLineEdit, 'lineEdit_bh')
        
        self.lineEdit_min = self.findChild(QLineEdit, 'lineEdit_min')
        self.lineEdit_max = self.findChild(QLineEdit, 'lineEdit_max')
        self.lineEdit_step = self.findChild(QLineEdit, 'lineEdit_step')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)
        self.currentTab = self.tabWidget.currentIndex()

        self.label_title.setText(title)
        self.label_subtitle.setText(subtitle)
        if self.step_frequency != 0:
            self.lineEdit_min.setText(str(self.min_frequency))
            self.lineEdit_max.setText(str(self.max_frequency))
            self.lineEdit_step.setText(str(self.step_frequency))

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def isInteger(self, value):
        try:
            int(value)
            return True
        except:
            return False

    def check(self):
        _min = _max = _step = 0
        if self.analysis_ID not in [2,4]:
            #Verify Modes
            if self.analysis_ID == 1:
                if self.lineEdit_modes.text() == "":
                    self.error("Insert a value (modes)")
                    return
                else:
                    if self.isInteger(self.lineEdit_modes.text()):
                        self.modes = int(self.lineEdit_modes.text())
                    else:
                        self.error("Value error (modes)")
                        return

            if self.lineEdit_min.text() == "":
                self.error("Insert a value (freq min)")
                return
            else:
                if float(self.lineEdit_min.text())>=0:
                    _min = float(self.lineEdit_min.text())
                else:
                    self.error("Value error (freq min)")
                    return

            if self.lineEdit_max.text() == "":
                self.error("Insert a value (freq max)")
                return
            else:
                if float(self.lineEdit_max.text()) > float(self.lineEdit_min.text()) + float(self.lineEdit_step.text()):
                    _max = float(self.lineEdit_max.text())
                else:
                    self.error("Value error (freq max)")
                    return

            if self.lineEdit_step.text() == "":
                self.error("Insert a value (freq df)")
                return
            else:
                if float(self.lineEdit_step.text())<0 or float(self.lineEdit_step.text())>=float(self.lineEdit_max.text()):
                    self.error("Value error (freq df)")
                    return
                else:
                    _step = float(self.lineEdit_step.text())

        av = bv = ah = bh = 0
        if self.lineEdit_av.text() != "":
            if self.isInteger(self.lineEdit_av.text()):
                av = int(self.lineEdit_av.text())
            else:
                self.error("Value error (av)")
                return

        if self.lineEdit_bv.text() != "":
            if self.isInteger(self.lineEdit_bv.text()):
                bv = int(self.lineEdit_bv.text())
            else:
                self.error("Value error (bv)")
                return

        if self.lineEdit_ah.text() != "":
            if self.isInteger(self.lineEdit_ah.text()):
                ah = int(self.lineEdit_ah.text())
            else:
                self.error("Value error (ah)")
                return

        if self.lineEdit_bh.text() != "":
            if self.isInteger(self.lineEdit_bh.text()):
                bh = int(self.lineEdit_bh.text())
            else:
                self.error("Value error (bh)")
                return

        self.damping = [ah, bh, av, bv]

        self.min_frequency = _min
        self.max_frequency = _max
        self.step_frequency = _step
        self.frequencies = np.arange(_min, _max+_step, _step)
        
        self.complete = True
        self.close()