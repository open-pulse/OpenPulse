from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QTabWidget, QPushButton
from os.path import basename
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.uix.user_input.analyseHarmonicInput import AnalyseHarmonicInput
from pulse.uix.user_input.analyseModalInput import AnalyseModalInput

class AnalyseTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analyseTypeInput.ui', self)

        self.typeID = None
        self.type = None
        self.method = None
        self.modes = 0
        #Type 0 == Harmonic Structural Direct
        #Type 1 == Harmonic Structural Modal
        #Type 2 == Modal Structural

        self.pushButton_harmonic_structural = self.findChild(QPushButton, 'pushButton_harmonic_structural')
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)

        self.pushButton_modal_structural = self.findChild(QPushButton, 'pushButton_modal_structural')
        self.pushButton_modal_structural.clicked.connect(self.modal_structural)

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
        self.typeID = select.index
        self.type = "Harmonic Analysis - Structural"
        if self.typeID == 0:
            self.method = "Direct"
        else:
            self.method = "Mode Superposition"
        self.close()

    def modal_structural(self):
        modal = AnalyseModalInput()
        if modal.modes is None:
            return
        self.modes = modal.modes
        self.typeID = 2
        self.type = "Modal Analysis - Structural"
        self.close()