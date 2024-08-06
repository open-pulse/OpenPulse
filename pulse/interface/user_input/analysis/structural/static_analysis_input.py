from PyQt5.QtWidgets import QDialog, QCheckBox, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL

import numpy as np
from pathlib import Path


class StaticAnalysisInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "/analysis/structural/static_analysis.ui"
        uic.loadUi(ui_path, self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._load_current_state()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Static Analysis Setup")

    def _initialize(self):
        self.complete = False
        self.global_damping = [0, 0, 0, 0]
        self.gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)
        self.gravity_vector = self.project.preprocessor.gravity_vector

    def _define_qt_variables(self):

        # QCheckBox
        self.checkBox_self_weight_load : QCheckBox
        self.checkBox_internal_pressure_load : QCheckBox
        self.checkBox_external_nodal_loads : QCheckBox
        self.checkBox_distributed_element : QCheckBox

        # QPushButton
        self.pushButton_run_analysis : QPushButton
    
    def _create_connections(self):
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
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm()
        elif event.key() == Qt.Key_Escape:
            self.close()