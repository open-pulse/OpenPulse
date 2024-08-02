from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.analysis.structural.structural_harmonic_analysis import StructuralHarmonicAnalysisInput
from pulse.interface.user_input.analysis.coupled.coupled_harmonic_analysis import CoupledHarmonicAnalysisInput
from pulse.interface.user_input.analysis.structural.structural_modal_analysis import StructuralModalAnalysisInput
from pulse.interface.user_input.analysis.acoustic.acoustic_modal_analysis import AcousticModalAnalysisInput
from pulse.interface.user_input.analysis.structural.static_analysis_input import StaticAnalysisInput

from pathlib import Path


"""
|--------------------------------------------------------------------|
|                    Analysis ID codification                        |
|--------------------------------------------------------------------|
|    0 - Structural - Harmonic analysis through direct method        |
|    1 - Structural - Harmonic analysis through mode superposition   |
|    2 - Structural - Modal analysis                                 |
|    3 - Acoustic - Harmonic analysis through direct method          |
|    4 - Acoustic - Modal analysis (convetional FE 1D)               |
|    5 - Coupled - Harmonic analysis through direct method           |
|    6 - Coupled - Harmonic analysis through mode superposition      |
|    7 - Structural - Static analysis (under development)            |
|--------------------------------------------------------------------|
"""

class AnalysisTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "analysis/general/analysis_type.ui"
        uic.loadUi(ui_path, self)

        main_window = app().main_window

        app().main_window.set_input_widget(self)
        self.project = main_window.project

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):
        self.analysis_ID = None
        self.analysis_type_label = None
        self.method_ID = None
        self.analysis_method_label = None
        self.modes = 0
        self.sigma_factor = 1e-4
        self.complete = False

    def _load_icons(self):
        self.icon = get_openpulse_icon()
        
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("Analysis type")

    def _define_qt_variables(self):
        self.pushButton_harmonic_structural : QPushButton
        self.pushButton_harmonic_acoustic : QPushButton
        self.pushButton_harmonic_coupled : QPushButton
        self.pushButton_modal_structural : QPushButton
        self.pushButton_modal_acoustic : QPushButton
        self.pushButton_static_analysis : QPushButton

    def _create_connections(self):
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)
        self.pushButton_harmonic_acoustic.clicked.connect(self.harmonic_acoustic)
        self.pushButton_harmonic_coupled.clicked.connect(self.harmonic_coupled)
        self.pushButton_modal_structural.clicked.connect(self.modal_structural)
        self.pushButton_modal_acoustic.clicked.connect(self.modal_acoustic)
        self.pushButton_static_analysis.clicked.connect(self.static_analysis)

    def harmonic_structural(self):

        self.close()
        select = StructuralHarmonicAnalysisInput()
        if select.index == -1:
            self.show()
            return

        self.method_ID = select.index
        self.analysis_type_label = "Structural Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 0
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_ID = 1
            self.analysis_method_label = "Mode Superposition Method"
        self.project.set_analysis_type( self.analysis_ID, 
                                        self.analysis_type_label, 
                                        self.analysis_method_label )
        self.complete = True

    def harmonic_acoustic(self):

        self.close()
        self.method_ID = 0
        self.analysis_type_label = "Acoustic Harmonic Analysis"

        if self.method_ID == 0:
            self.analysis_ID = 3
            self.analysis_method_label = "Direct Method"
        else:
            return
    
        self.project.set_analysis_type(self.analysis_ID, 
                                       self.analysis_type_label, 
                                       self.analysis_method_label)
        self.complete = True

    def harmonic_coupled(self):

        self.close()
        coupled = CoupledHarmonicAnalysisInput()
        if coupled.index == -1:
            self.show()
            return

        self.method_ID = coupled.index
        self.analysis_type_label = "Coupled Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 5
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_ID = 6
            self.analysis_method_label = "Mode Superposition Method"
        self.project.set_analysis_type(self.analysis_ID, 
                                       self.analysis_type_label, 
                                       self.analysis_method_label)
        self.complete = True

    def modal_structural(self):

        self.close()
        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            self.show()
            return

        self.analysis_ID = 2
        self.analysis_type_label = "Structural Modal Analysis"
        self.project.set_analysis_type(self.analysis_ID, 
                                       self.analysis_type_label, 
                                       self.analysis_method_label)
        self.project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def modal_acoustic(self):

        self.close()
        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            self.show()
            return

        self.analysis_ID = 4
        self.analysis_type_label = "Acoustic Modal Analysis"
        self.project.set_analysis_type(self.analysis_ID, 
                                       self.analysis_type_label, 
                                       self.analysis_method_label)
        self.project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def static_analysis(self):

        self.close()
        static = StaticAnalysisInput()
        if not static.complete:
            self.show()
            return

        self.analysis_ID = 7
        self.analysis_type_label = "Static Analysis"
        self.complete = static.complete
        self.project.set_analysis_type(self.analysis_ID, 
                                       self.analysis_type_label, 
                                       self.analysis_method_label)
        self.complete = static.complete
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()