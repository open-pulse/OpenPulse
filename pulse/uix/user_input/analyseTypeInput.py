from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.uix.user_input.analyseHarmonicInput import AnalyseHarmonicInput

class AnalyseTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analyseTypeInput.ui', self)

        self.type = None
        #Type 0 == Harmonic Structural Direct
        #Type 1 == Harmonic Structural Modal

        self.pushButton_harmonic_structural = self.findChild(QPushButton, 'pushButton_harmonic_structural')
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)

        self.exec_()

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def harmonic_structural(self):
        select = AnalyseHarmonicInput()
        self.type = select.index
        self.close()