from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import numpy as np
from pathlib import Path

from pulse import UI_DIR
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

class StaticAnalysisInput(QDialog):
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(UI_DIR / "analysis/structural/static_analysis.ui", self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Static Analysis Setup")

        self.project = project
        self.gravity_vector = self.project.preprocessor.gravity_vector
        
        self._reset_variables()
        self._define_qt_variables()
        self._load_current_state()
        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def _reset_variables(self):
        self.complete = False
        self.global_damping = [0, 0, 0, 0]
        self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)

    def _define_qt_variables(self):
        #
        self.checkBox_self_weight_load = self.findChild(QCheckBox, 'checkBox_self_weight_load')
        self.checkBox_internal_pressure_load = self.findChild(QCheckBox, 'checkBox_internal_pressure_load')
        self.checkBox_external_nodal_loads = self.findChild(QCheckBox, 'checkBox_external_nodal_loads')
        self.checkBox_distributed_element = self.findChild(QCheckBox, 'checkBox_distributed_element')
        #
        self.pushButton_run_analysis = self.findChild(QPushButton, 'pushButton_run_analysis')
        self.pushButton_run_analysis.clicked.connect(self.confirm)

    def _load_current_state(self):
        self.checkBox_self_weight_load.setChecked(self.project.weight_load)
        self.checkBox_internal_pressure_load.setChecked(self.project.internal_pressure_load)
        self.checkBox_external_nodal_loads.setChecked(self.project.external_nodal_loads)
        self.checkBox_distributed_element.setChecked(self.project.element_distributed_load)

    def confirm(self):

        self.project.set_structural_damping(self.global_damping)
        self.project.set_frequencies(np.array([0], dtype=float), 0, 0, 0)

        weight_load = self.checkBox_self_weight_load.isChecked()
        internal_pressure_load = self.checkBox_internal_pressure_load.isChecked()
        external_nodal_load = self.checkBox_external_nodal_loads.isChecked()
        distributed_load = self.checkBox_distributed_element.isChecked()
        analysis_setup = [weight_load, internal_pressure_load, external_nodal_load, distributed_load]

        self.project.set_static_analysis_setup(analysis_setup)

        self.complete = True
        self.close()