from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
from time import time
import configparser

from pulse.processing.solution import *

class RunAnalyseInput(QDialog):
    def __init__(self, mesh, analyseType, frequencies, modes, damping,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/runAnalyseInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.solution = None
        self.naturalFrequencies = []

        self.mesh = mesh
        self.analyseType = analyseType
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
        if self.analyseType == 0:  #Harmonic Structural Direct
            self.solution = direct_method(self.mesh, self.frequencies, self.damping)
        elif self.analyseType == 1: #Harmonic Structural Modal
            self.solution = modal_superposition(self.mesh, self.frequencies, self.modes, self.damping)
        elif self.analyseType == 2: #Modal Structural
            self.naturalFrequencies, self.solution = modal_analysis(self.mesh, modes = self.modes)
        fim = time()
        text = "Solution finished!\n"
        text += "Time elapsed: {} [s]\n".format(fim-inicio)
        text += "Press ESC to continue..."
        self.label_title.setText(text)