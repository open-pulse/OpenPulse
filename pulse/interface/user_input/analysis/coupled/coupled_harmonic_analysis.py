from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR


class CoupledHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/general/harmonic_analysis_method.ui"
        uic.loadUi(ui_path, self)
        
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()       
        self._create_connections()
        self.exec()
        
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Structural harmonic analysis")

    def _initialize(self):
        self.index = -1

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_method : QComboBox
        # QLabel
        self.label_method : QLabel
        self.label_method.setText("Harmonic Analysis - Coupled")
        # QPushButton
        self.pushButton_go_to_analysis_setup : QPushButton
    
    def _create_connections(self):
        self.pushButton_go_to_analysis_setup.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.check()

    def check(self):
        self.index = self.comboBox_method.currentIndex()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()