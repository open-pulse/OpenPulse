from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import numpy as np
from pathlib import Path

class StructuralHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui/analysis_/general_/harmonic_analysis_method_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        
        self.index = -1

        self._define_and_connect_qt_variables()       
        self.exec()

    def _define_and_connect_qt_variables(self):
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_title.setText("Harmonic Analysis - Structural")
        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.button_clicked)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()

    def check(self):
        self.index = self.comboBox.currentIndex()
        self.close()

    def button_clicked(self):
        self.check()