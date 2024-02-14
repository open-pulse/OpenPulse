from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
import numpy as np

class CoupledHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/analysis/general/harmonic_analysis_method.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.index = 0
        self.complete = False

        self.comboBox = self.findChild(QComboBox, 'comboBox')
        self.comboBox.currentIndexChanged.connect(self.selectionChange)
        self.index = self.comboBox.currentIndex()

        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_title.setText("  Harmonic Analysis - Coupled  ")

        self.pushButton_2 = self.findChild(QPushButton, 'pushButton_2')
        self.pushButton_2.clicked.connect(self.button_clicked)
        
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()

    def selectionChange(self, index):
        self.index = self.comboBox.currentIndex()

    def check(self):
        self.complete = True
        self.close()

    def button_clicked(self):
        self.check()