from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import  app, UI_DIR

class StructuralHarmonicAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "analysis/general/harmonic_analysis_method.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)

        self._initialize()
        self._config_window()
        self._define_qt_variables()       
        self._create_connections()
        self.exec()
        
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.index = -1

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_method : QComboBox

        # QLabel
        self.label_method : QLabel
        self.label_method.setText("Harmonic Analysis - Structural")

        # QPushButton
        self.pushButton_go_to_analysis_setup : QPushButton
    
    def _create_connections(self):
        self.pushButton_go_to_analysis_setup.clicked.connect(self.analysis_setup_callback)

    def analysis_setup_callback(self):
        self.go_to_analysis_setup()

    def go_to_analysis_setup(self):
        self.index = self.comboBox_method.currentIndex()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.go_to_analysis_setup()
        elif event.key() == Qt.Key_Escape:
            self.index = -1
            self.close()