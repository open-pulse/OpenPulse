from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.analysis.structural.structural_harmonic_analysis import StructuralHarmonicAnalysisInput
from pulse.interface.user_input.analysis.coupled.coupled_harmonic_analysis import CoupledHarmonicAnalysisInput
from pulse.interface.user_input.analysis.structural.structural_modal_analysis import StructuralModalAnalysisInput
from pulse.interface.user_input.analysis.acoustic.acoustic_modal_analysis import AcousticModalAnalysisInput
from pulse.interface.user_input.analysis.structural.static_analysis_input import StaticAnalysisInput


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

        app().main_window.set_input_widget(self)
        self.project = app().project

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):
        self.method_id = None
        self.analysis_method_label = None
        self.modes = 0
        self.sigma_factor = 1e-4
        self.complete = False

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
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

        self.method_id = select.index
        analysis_type = "Structural Harmonic Analysis"
        if self.method_id == 0:
            analysis_id = 0
            analysis_method = "Direct Method"
        else:
            analysis_id = 1
            analysis_method = "Mode Superposition Method"

        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def harmonic_acoustic(self):

        self.close()
        self.method_id = 0
        analysis_type = "Acoustic Harmonic Analysis"

        if self.method_id == 0:
            analysis_id = 3
            analysis_method = "Direct Method"
        else:
            return
    
        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def harmonic_coupled(self):

        self.close()
        coupled = CoupledHarmonicAnalysisInput()
        if coupled.index == -1:
            self.show()
            return

        self.method_id = coupled.index
        analysis_type = "Coupled Harmonic Analysis"
        if self.method_id == 0:
            analysis_id = 5
            analysis_method = "Direct Method"
        else:
            analysis_id = 6
            analysis_method = "Mode Superposition Method"
        app().project.set_analysis_type(analysis_id, analysis_type, analysis_method)
        self.complete = True

    def modal_structural(self):

        self.close()
        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            self.show()
            return

        analysis_id = 2
        analysis_type = "Structural Modal Analysis"
        app().project.set_analysis_type(analysis_id, analysis_type, None)
        app().project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def modal_acoustic(self):

        self.close()
        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            self.show()
            return

        analysis_id = 4
        analysis_type = "Acoustic Modal Analysis"
        app().project.set_analysis_type(analysis_id, analysis_type, None)
        app().project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete

    def static_analysis(self):

        self.close()
        static = StaticAnalysisInput()
        if not static.complete:
            self.show()
            return

        analysis_id = 7
        analysis_type = "Static Analysis"
        self.complete = static.complete
        app().project.set_analysis_type(analysis_id, analysis_type, None)
        self.complete = static.complete
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()