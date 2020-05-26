from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
from time import time
import configparser

from pulse.processing.solution_structural import *

class RunAnalyseInput(QDialog):
    def __init__(self, solve, analyseTypeID, analysis_type, frequencies, modes, damping,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/runAnalyseInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.solution = None
        self.naturalFrequencies = []

        self.solve = solve
        self.analyseTypeID = analyseTypeID
        self.analysis_type = analysis_type
        self.frequencies = frequencies
        self.damping = damping
        self.modes = modes

        self.label_title = self.findChild(QLabel, 'label_title')

        self.run()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def run(self):
        inicio = time()
        if self.analyseTypeID == 0:
            if self.analysis_type == "Harmonic Analysis - Structural":
                self.solution = self.solve.direct_method(self.frequencies, self.damping) #Harmonic Structural - Direct Method
            elif self.analysis_type == "Harmonic Analysis - Acoustic":
                self.solution = self.solve.direct_method() #Harmonic Acoustic Direct
        elif self.analyseTypeID == 1: #Harmonic Structural - Mode Superposition
            self.solution = self.solve.mode_superposition(self.frequencies, self.modes, self.damping)
        elif self.analyseTypeID == 2: #Modal Structural
            self.naturalFrequencies, self.solution = self.solve.modal_analysis(modes = self.modes)

        fim = time()
        text = "Solution finished!\n"
        text += "Time elapsed: {} [s]\n".format(fim-inicio)
        text += "Press ESC to continue..."
        self.label_title.setText(text)

        # WARNINGS FROM ANALYSE
        if self.solve.flag_ModeSup_prescribed_NonNull_DOFs:
            self.error(self.solve.warning_ModeSup_prescribedDOFs, title = "WARNING")

        if self.solve.flag_Clump:
            self.error(self.solve.warning_Clump, title = "WARNING")

        if self.solve.flag_Modal_prescribed_NonNull_DOFs:
            self.error(self.solve.warning_Modal_prescribedDOFs, title = "WARNING")