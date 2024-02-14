from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np
from pathlib import Path

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from math import pi

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class StructuralModalAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/analysis/structural/modal_analysis.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.lineEdit_number_modes = self.findChild(QLineEdit, 'lineEdit_number_modes')
        self.lineEdit_input_sigma_factor = self.findChild(QLineEdit, 'lineEdit_input_sigma_factor')

        self.modes = int(self.lineEdit_number_modes.text())
        self.sigma_factor = float(self.lineEdit_input_sigma_factor.text())
        self.sigma_factor = (2*pi*self.sigma_factor)**2

        self.pushButton = self.findChild(QPushButton, 'pushButton')
        self.pushButton.clicked.connect(self.confirm)
        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.confirm)

        self.complete = False
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def check(self):
        if self.lineEdit_number_modes.text() == "":
            title = "INVALID INPUT VALUE"
            message = "Invalid a value to the number of modes."
            self.text_data = [title, message, window_title1]
            return True
        else:
            try:
                self.modes = int(self.lineEdit_number_modes.text())
            except Exception:
                title = "INVALID INPUT VALUE"
                message = "Invalid input value for number of modes."
                self.text_data = [title, message, window_title1]
                return True
            try:
                self.sigma_factor = (2*pi*float(self.lineEdit_input_sigma_factor.text()))**2
            except Exception:
                title = "INVALID INPUT VALUE"
                message = "Invalid input value for sigma factor."
                self.text_data = [title, message, window_title1]
                return True
        return False
    
    def confirm(self):
        if self.check():
            PrintMessageInput(self.text_data)
            return
        self.complete = True
        self.close()

    def button_clicked(self):
        self.check()