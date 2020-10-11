from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.uix.user_input.structuralHarmonicAnalysisInput import StructuralHarmonicAnalysisInput
from pulse.uix.user_input.acousticHarmonicAnalysisInput import AcousticHarmonicAnalysisInput
from pulse.uix.user_input.coupledHarmonicAnalysisInput import CoupledHarmonicAnalysisInput
from pulse.uix.user_input.structuralModalAnalysisInput import StructuralModalAnalysisInput
from pulse.uix.user_input.acousticModalAnalysisInput import AcousticModalAnalysisInput

class AnalysisTypeInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/analysisTypeInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.analysis_ID = None
        self.analysis_type_label = None
        self.method_ID = None
        self.analysis_method_label = None

        self.modes = 0
        self.sigma_factor = 1e-4

        #Analysis ID 0 ==> Structural Harmonic Analysis - Direct Method
        #Analysis ID 1 ==> Structural Harmonic Analysis - Mode Superposition Method
        #Analysis ID 2 ==> Structural Modal Analysis 
        #Analysis ID 3 ==> Acoustic Harmonic Analysis - Direct Method
        #Analysis ID 4 ==> Acoustic Modal Analysis
        #Analysis ID 5 ==> Coupled Harmonic Analysis - Direct Method
        #Analysis ID 6 ==> Coupled Harmonic Analysis - Mode Superposition Method

        self.pushButton_harmonic_structural = self.findChild(QPushButton, 'pushButton_harmonic_structural')
        self.pushButton_harmonic_structural.clicked.connect(self.harmonic_structural)

        self.pushButton_harmonic_acoustic = self.findChild(QPushButton, 'pushButton_harmonic_acoustic')
        self.pushButton_harmonic_acoustic.clicked.connect(self.harmonic_acoustic)

        self.pushButton_harmonic_coupled = self.findChild(QPushButton, 'pushButton_harmonic_coupled')
        self.pushButton_harmonic_coupled.clicked.connect(self.harmonic_coupled)

        self.pushButton_modal_structural = self.findChild(QPushButton, 'pushButton_modal_structural')
        self.pushButton_modal_structural.clicked.connect(self.modal_structural)

        self.pushButton_modal_acoustic = self.findChild(QPushButton, 'pushButton_modal_acoustic')
        self.pushButton_modal_acoustic.clicked.connect(self.modal_acoustic)

        self.complete = False
        self.exec_()

    def keyPressEvent(self, event):
        # if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
        #     self.check()
        if event.key() == Qt.Key_Escape:
            self.close()

    def harmonic_structural(self):
        select = StructuralHarmonicAnalysisInput()
        self.method_ID = select.index
        self.analysis_type_label = "Structural Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 0
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_ID = 1
            self.analysis_method_label = "Mode Superposition Method"
        self.close()

    def harmonic_acoustic(self):
        select = AcousticHarmonicAnalysisInput()
        self.method_ID = select.index
        self.analysis_type_label = "Acoustic Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 3
            self.analysis_method_label = "Direct Method"
        else:
            return
        #     self.method_text = "Mode Superposition"
        self.close()

    def harmonic_coupled(self):
        select = CoupledHarmonicAnalysisInput()
        self.method_ID = select.index
        self.analysis_type_label = "Coupled Harmonic Analysis"
        if self.method_ID == 0:
            self.analysis_ID = 5
            self.analysis_method_label = "Direct Method"
        else:
            self.analysis_ID = 6
            self.analysis_method_label = "Mode Superposition Method"
        self.close()

    def modal_structural(self):
        modal = StructuralModalAnalysisInput()
        if modal.modes is None:
            return
        self.modes = modal.modes
        self.sigma_factor = modal.sigma_factor
        self.analysis_ID = 2
        self.analysis_type_label = "Structural Modal Analysis"
        self.complete = modal.complete
        self.close()

    def modal_acoustic(self):
        modal = AcousticModalAnalysisInput()
        if modal.modes is None:
            return
        self.modes = modal.modes
        self.analysis_ID = 4
        self.analysis_type_label = "Acoustic Modal Analysis"
        self.complete = modal.complete
        self.close()