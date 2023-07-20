from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path
import numpy as np

class AcousticHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(Path('data/user_input/ui/analysis_/acoustic_/analysis_setup_input_harmonic_analysis_direct_method.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.index = 0
        self.complete = False
        
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.button_clicked)

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()

    def check(self):
        self.complete = True
        self.close()

    def button_clicked(self):
        self.check()