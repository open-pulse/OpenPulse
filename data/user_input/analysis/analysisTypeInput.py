from PyQt5.QtWidgets import QDialog, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from data.user_input.analysis.structuralHarmonicAnalysisInput import StructuralHarmonicAnalysisInput
from data.user_input.analysis.acousticHarmonicAnalysisInput import AcousticHarmonicAnalysisInput
from data.user_input.analysis.coupledHarmonicAnalysisInput import CoupledHarmonicAnalysisInput
from data.user_input.analysis.structuralModalAnalysisInput import StructuralModalAnalysisInput
from data.user_input.analysis.acousticModalAnalysisInput import AcousticModalAnalysisInput
from data.user_input.analysis.statict_analysis_input import StaticAnalysisInput

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
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        uic.loadUi(Path('data/user_input/ui_files/analysis_/general_/analysis_type_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Analysis type")

        self.project = project

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.exec()


    def _reset_variables(self):
        self.analysis_ID = None
        self.analysis_type_label = None
        self.method_ID = None
        self.analysis_method_label = None
        self.modes = 0
        self.sigma_factor = 1e-4
        self.complete = False


    def _define_qt_variables(self):
        self.pushButton_harmonic_structural = self.findChild(QPushButton, 'pushButton_harmonic_structural')
        self.pushButton_harmonic_acoustic = self.findChild(QPushButton, 'pushButton_harmonic_acoustic')
        self.pushButton_harmonic_coupled = self.findChild(QPushButton, 'pushButton_harmonic_coupled')
        self.pushButton_modal_structural = self.findChild(QPushButton, 'pushButton_modal_structural')
        self.pushButton_modal_acoustic = self.findChild(QPushButton, 'pushButton_modal_acoustic')
        self.pushButton_static_analysis = self.findChild(QPushButton, 'pushButton_static_analysis')


    def _create_connections(self):
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)
        self.pushButton_harmonic_acoustic.clicked.connect(self.harmonic_acoustic)
        self.pushButton_harmonic_coupled.clicked.connect(self.harmonic_coupled)
        self.pushButton_modal_structural.clicked.connect(self.modal_structural)
        self.pushButton_modal_acoustic.clicked.connect(self.modal_acoustic)
        self.pushButton_static_analysis.clicked.connect(self.static_analysis)
            

    def harmonic_structural(self):
        #
        self.close()
        select = StructuralHarmonicAnalysisInput()
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
        #
        self.close()
        self.method_ID = 0
        self.analysis_type_label = "Acoustic Harmonic Analysis"

        if self.method_ID == 0:
            self.analysis_ID = 3
            self.analysis_method_label = "Direct Method"
        else:
            return
    
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.complete = True


    def harmonic_coupled(self):
        #
        self.close()
        coupled = CoupledHarmonicAnalysisInput()
        self.method_ID = coupled.index
        self.analysis_type_label = "Coupled Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 5
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_ID = 6
            self.analysis_method_label = "Mode Superposition Method"
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.complete = coupled.complete


    def modal_structural(self):
        #
        self.close()
        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            return
        self.analysis_ID = 2
        self.analysis_type_label = "Structural Modal Analysis"
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete


    def modal_acoustic(self):
        #
        self.close()
        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            return
        self.analysis_ID = 4
        self.analysis_type_label = "Acoustic Modal Analysis"
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.set_modes_sigma(modal.modes, sigma=modal.sigma_factor)
        self.complete = modal.complete


    def static_analysis(self):
        #
        self.close()
        static = StaticAnalysisInput(self.project)
        self.analysis_ID = 7
        self.analysis_type_label = "Static Analysis"
        self.complete = static.complete
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.complete = static.complete

    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()