from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

import numpy as np

class PulsationAttenuatorDeviceInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/editor/pulsation_attenuator_device_input.ui"
        uic.loadUi(ui_path, self)

        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.preprocessor = self.project.preprocessor

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_main_axis : QComboBox
        self.comboBox_connection_type : QComboBox
        self.comboBox_number_volumes : QComboBox
        self.comboBox_filter_setup : QComboBox
        self.comboBox_input_pipe_layout : QComboBox
        self.comboBox_output_pipe_layout : QComboBox
        self.comboBox_tunned_filter : QComboBox

        # QLineEdit
        self.lineEdit_input_chamber_length : QLineEdit
        self.lineEdit_input_chamber_diameter : QLineEdit
        self.lineEdit_output_chamber_length : QLineEdit
        self.lineEdit_output_chamber_diameter : QLineEdit
        self.lineEdit_chamber_separation : QLineEdit
        self.lineEdit_input_pipe_length : QLineEdit
        self.lineEdit_output_pipe_length : QLineEdit
        self.lineEdit_input_pipe_distance : QLineEdit
        self.lineEdit_output_pipe_distance : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton

        # QSpinBox
        self.spinBox_input_pipe_angle : QDoubleSpinBox
        self.spinBox_input_pipe_angle : QDoubleSpinBox

    def _create_connections(self):
        pass

    def _config_widgets(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
