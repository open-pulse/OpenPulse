from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.utils import check_inputs

import configparser
import numpy as np

class PulsationAttenuatorDeviceInput(QDialog):
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
        ConfigWidgetAppearance(self)
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
        self.file = self.project.file

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
        self.pushButton_cancel : QPushButton
        self.pushButton_confirm : QPushButton

        # QSpinBox
        self.spinBox_input_pipe_angle : QDoubleSpinBox
        self.spinBox_output_pipe_angle : QDoubleSpinBox

    def _create_connections(self):

        self.comboBox_number_volumes.currentIndexChanged.connect(self.number_volumes_callback)

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.confirm_button_pressed)

    def _config_widgets(self):
        pass

    def number_volumes_callback(self):
        if self.comboBox_number_volumes.currentIndex() == 0:
            self.comboBox_filter_setup.setDisabled(True)
            self.lineEdit_chamber_separation.setText("")
            self.lineEdit_chamber_separation.setDisabled(True)
        else:
            self.comboBox_filter_setup.setDisabled(False)
            self.lineEdit_chamber_separation.setDisabled(False)

    def check_all_inputs(self):

        self.attenuator_data = dict()

        if self.comboBox_main_axis.currentIndex() == 0:
            self.attenuator_data["main axis"] = "along x-axis"
        elif self.comboBox_main_axis.currentIndex() == 1:
            self.attenuator_data["main axis"] = "along y-axis"
        elif self.comboBox_main_axis.currentIndex() == 2:
            self.attenuator_data["main axis"] = "along z-axis"

        if self.comboBox_connection_type.currentIndex() == 0:
            self.attenuator_data["connection type"] = "discharge"
        elif self.comboBox_connection_type.currentIndex() == 1:
            self.attenuator_data["connection type"] = "sucction"

        if self.comboBox_number_volumes.currentIndex() == 0:
            self.attenuator_data["number of volumes"] = "single volume"
        elif self.comboBox_number_volumes.currentIndex() == 1:
            self.attenuator_data["number of volumes"] = "dual volume"

        if self.comboBox_filter_setup.isEnabled():
            if self.comboBox_filter_setup.currentIndex() == 0:
                self.attenuator_data["filter setup"] = "choke-volumes"
            elif self.comboBox_filter_setup.currentIndex() == 1:
                self.attenuator_data["filter setup"] = "plate-volumes"

        if self.comboBox_input_pipe_layout.currentIndex() == 0:
            self.attenuator_data["input pipe layout"] = "axial"
        elif self.comboBox_input_pipe_layout.currentIndex() == 1:
            self.attenuator_data["input pipe layout"] = "radial"

        if self.comboBox_output_pipe_layout.currentIndex() == 0:
            self.attenuator_data["output pipe layout"] = "axial"
        elif self.comboBox_output_pipe_layout.currentIndex() == 1:
            self.attenuator_data["output pipe layout"] = "radial"

        value = check_inputs(self.lineEdit_input_chamber_length, "'input chamber length'")
        if value is None:
            self.lineEdit_input_chamber_length.setFocus()
            return True
        self.attenuator_data["input chamber length"] = value

        value = check_inputs(self.lineEdit_input_chamber_diameter, "'input chamber diameter'")
        if value is None:
            self.lineEdit_input_chamber_diameter.setFocus()
            return True
        self.attenuator_data["input chamber diameter"] = value

        value = check_inputs(self.lineEdit_output_chamber_length, "'output chamber length'")
        if value is None:
            self.lineEdit_output_chamber_length.setFocus()
            return True
        self.attenuator_data["output chamber length"] = value

        value = check_inputs(self.lineEdit_output_chamber_diameter, "'output chamber diameter'")
        if value is None:
            self.lineEdit_output_chamber_diameter.setFocus()
            return True
        self.attenuator_data["output chamber diameter"] = value

        value = check_inputs(self.lineEdit_chamber_separation, "'chamber separation'")
        if value is None:
            self.lineEdit_chamber_separation.setFocus()
            return True
        self.attenuator_data["chamber separation"] = value
        
        value = check_inputs(self.lineEdit_input_pipe_length, "'input pipe length'")
        if value is None:
            self.lineEdit_input_pipe_length.setFocus()
            return True
        self.attenuator_data["input pipe length"] = value
        
        value = check_inputs(self.lineEdit_output_pipe_length, "'output pipe length'")
        if value is None:
            self.lineEdit_output_pipe_length.setFocus()
            return True
        self.attenuator_data["output pipe length"] = value
        
        value = check_inputs(self.lineEdit_input_pipe_distance, "'input pipe distance'")
        if value is None:
            self.lineEdit_input_pipe_distance.setFocus()
            return True
        self.attenuator_data["input pipe distance"] = value
        
        value = check_inputs(self.lineEdit_output_pipe_distance, "'input pipe distance'")
        if value is None:
            self.lineEdit_output_pipe_distance.setFocus()
            return True
        self.attenuator_data["input pipe distance"] = value

        self.attenuator_data["input pipe angle"] = self.spinBox_input_pipe_angle.value()
        self.attenuator_data["output pipe angle"] = self.spinBox_output_pipe_angle.value()

    def confirm_button_pressed(self):

        if self.check_all_inputs():
            self.attenuator_data = dict()
            return

        tag = self.get_device_tag()
        self.project.PAD.add_pulsation_attenuator_device(tag, self.attenuator_data)

        self.close()

    def get_device_tag(self):
        index = 1
        _run = True
        while _run:
            if index in self.project.PAD.pulsation_attenuator_device.keys():
                index += 1
            else:
                _run = False
        return index

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()