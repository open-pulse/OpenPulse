from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path
import numpy as np
from pulse import UI_DIR


class CoupledHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/analysis/general/harmonic_analysis_method.ui")
        uic.loadUi(ui_path, self)
        
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()       
        self._create_connections()
        self.exec()

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Structural harmonic analysis")
        self.setWindowIcon(self.icon)

    def _initialize(self):
        self.index = -1

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox = self.findChild(QComboBox, 'comboBox')
        # QLabel
        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_title.setText("  Harmonic Analysis - Coupled  ")
        # QPushButton
        self.pushButton_go_to_analysis_setup = self.findChild(QPushButton, 'pushButton_go_to_analysis_setup')
    
    def _create_connections(self):
        self.pushButton_go_to_analysis_setup.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.check()

    def check(self):
        self.index = self.comboBox.currentIndex()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()