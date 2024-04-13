from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLabel, QLineEdit, QPushButton, QTreeWidget
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.formatters.config_widget_appearance import ConfigWidgetAppearance
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.utils import check_inputs

import configparser
import numpy as np

class PulsationSuppressionDeviceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/editor/pulsation_suppression_device_input.ui"
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
        self.comboBox_volumes_connection : QComboBox
        self.comboBox_pipe1_connection : QComboBox
        self.comboBox_pipe2_connection : QComboBox
        self.comboBox_tunned_filter : QComboBox

        # QLabel
        self.label_pipe3 : QLabel
        self.label_rotation_plane : QLabel
        self.label_rotation_angle_pipe1 : QLabel
        self.label_rotation_angle_pipe2 : QLabel
        self.label_rotation_angle_pipe1_unit : QLabel
        self.label_rotation_angle_pipe2_unit : QLabel
        self.label_volumes_connection : QLabel
        self.label_volumes_spacing : QLabel
        self.label_volumes_spacing_unit : QLabel

        # QLineEdit
        self.lineEdit_device_label : QLineEdit
        self.lineEdit_connecting_coord_x : QLineEdit
        self.lineEdit_connecting_coord_y : QLineEdit
        self.lineEdit_connecting_coord_z : QLineEdit

        self.lineEdit_volume1_length : QLineEdit
        self.lineEdit_volume2_length : QLineEdit
        self.lineEdit_volume1_diameter : QLineEdit
        self.lineEdit_volume2_diameter : QLineEdit
        self.lineEdit_volume1_wall_thickness : QLineEdit
        self.lineEdit_volume2_wall_thickness : QLineEdit

        self.lineEdit_pipe1_length : QLineEdit
        self.lineEdit_pipe2_length : QLineEdit
        self.lineEdit_pipe3_length : QLineEdit
        self.lineEdit_pipe1_diameter : QLineEdit
        self.lineEdit_pipe2_diameter : QLineEdit
        self.lineEdit_pipe3_diameter : QLineEdit
        self.lineEdit_pipe1_wall_thickness : QLineEdit
        self.lineEdit_pipe2_wall_thickness : QLineEdit
        self.lineEdit_pipe3_wall_thickness : QLineEdit
        self.lineEdit_pipe1_distance : QLineEdit
        self.lineEdit_pipe2_distance : QLineEdit
        self.lineEdit_pipe3_distance : QLineEdit

        self.lineEdit_rotation_plane : QLineEdit
        self.lineEdit_volumes_spacing : QLineEdit

        # QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QSpinBox
        self.spinBox_pipe1_rotation_angle : QDoubleSpinBox
        self.spinBox_pipe2_rotation_angle : QDoubleSpinBox

        # QTreeWidget
        self.treeWidget_psd_info : QTreeWidget

    def _create_connections(self):
        
        self.comboBox_main_axis.currentIndexChanged.connect(self.update_the_rotation_angle)
        self.comboBox_number_volumes.currentIndexChanged.connect(self.number_volumes_callback)
        self.comboBox_pipe1_connection.currentIndexChanged.connect(self.pipe_connection_callback)
        self.comboBox_pipe2_connection.currentIndexChanged.connect(self.pipe_connection_callback)

        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.confirm_button_pressed)

        self.update_the_rotation_angle()

    def _config_widgets(self):
        pass

    def pipe_connection_callback(self):

        index_1 = self.comboBox_pipe1_connection.currentIndex()
        index_2 = self.comboBox_pipe2_connection.currentIndex()
        
        self.label_rotation_angle_pipe1.setDisabled(bool(index_1))
        self.label_rotation_angle_pipe2.setDisabled(bool(index_2))
        self.label_rotation_angle_pipe1_unit.setDisabled(bool(index_1))
        self.label_rotation_angle_pipe2_unit.setDisabled(bool(index_2))

        self.spinBox_pipe1_rotation_angle.setDisabled(bool(index_1))
        self.spinBox_pipe2_rotation_angle.setDisabled(bool(index_2))

    def number_volumes_callback(self):

        index = self.comboBox_number_volumes.currentIndex()
        self.comboBox_volumes_connection.setDisabled(bool(index))

        self.label_pipe3.setDisabled(bool(index))
        self.label_rotation_plane.setDisabled(bool(index))
        self.label_rotation_angle_pipe1.setDisabled(bool(index))
        self.label_rotation_angle_pipe2.setDisabled(bool(index))
        self.label_rotation_angle_pipe1_unit.setDisabled(bool(index))
        self.label_rotation_angle_pipe2_unit.setDisabled(bool(index))
        self.label_volumes_connection.setDisabled(bool(index))
        self.label_volumes_spacing.setDisabled(bool(index))
        self.label_volumes_spacing_unit.setDisabled(bool(index))

        self.lineEdit_pipe3_length.setDisabled(bool(index))
        self.lineEdit_pipe3_diameter.setDisabled(bool(index))
        self.lineEdit_pipe3_wall_thickness.setDisabled(bool(index))
        self.lineEdit_pipe3_distance.setDisabled(bool(index))
        self.lineEdit_volumes_spacing.setDisabled(bool(index))
        self.spinBox_pipe1_rotation_angle.setDisabled(bool(index))
        self.spinBox_pipe2_rotation_angle.setDisabled(bool(index))

        if index:
            self.lineEdit_volumes_spacing.setText("")
            self.comboBox_volumes_connection.setCurrentIndex(3)
        else:
            self.lineEdit_volumes_spacing.setFocus()
            self.comboBox_volumes_connection.setCurrentIndex(0)

    def update_the_rotation_angle(self):
        index = self.comboBox_main_axis.currentIndex()
        if index == 0:
            self.lineEdit_rotation_plane.setText("YZ-plane")
        elif index == 1:
            self.lineEdit_rotation_plane.setText("XZ-plane")
        elif index == 2:
            self.lineEdit_rotation_plane.setText("XY-plane")

    def check_connecting_coords(self):

        coord_x = check_inputs(self.lineEdit_connecting_coord_x, "'connecting coord. x'", zero_included=True)
        if coord_x is None:
            self.lineEdit_connecting_coord_x.setFocus()
            return True

        coord_y = check_inputs(self.lineEdit_connecting_coord_y, "'connecting coord. y'", zero_included=True)
        if coord_y is None:
            self.lineEdit_connecting_coord_y.setFocus()
            return True
        
        coord_z = check_inputs(self.lineEdit_connecting_coord_z, "'connecting coord. z'", zero_included=True)
        if coord_z is None:
            self.lineEdit_connecting_coord_z.setFocus()
            return True
        
        self.suppression_device_data["connecting coords"] = [coord_x, coord_y, coord_z]

    def check_volume1_info(self):

        length = check_inputs(self.lineEdit_volume1_length, "'volume #1 length'")
        if length is None:
            self.lineEdit_volume1_length.setFocus()
            return True

        diameter = check_inputs(self.lineEdit_volume1_diameter, "'volume #1 diameter'")
        if diameter is None:
            self.lineEdit_volume1_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_volume1_wall_thickness, "'volume #1 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_volume1_wall_thickness.setFocus()
            return True

        self.suppression_device_data["volume #1 parameters"] = [length, diameter, wall_thickness]

    def check_volume2_info(self):

        length = check_inputs(self.lineEdit_volume2_length, "'volume #2 length'")
        if length is None:
            self.lineEdit_volume2_length.setFocus()
            return True

        diameter = check_inputs(self.lineEdit_volume2_diameter, "'volume #2 diameter'")
        if diameter is None:
            self.lineEdit_volume2_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_volume2_wall_thickness, "'volume #2 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_volume2_wall_thickness.setFocus()
            return True

        self.suppression_device_data["volume #2 parameters"] = [length, diameter, wall_thickness]

    def check_pipe1_info(self):

        length = check_inputs(self.lineEdit_pipe1_length, "'pipe #1 length'")
        if length is None:
            self.lineEdit_pipe1_length.setFocus()
            return True

        diameter = check_inputs(self.lineEdit_pipe1_diameter, "'pipe #1 diameter'")
        if diameter is None:
            self.lineEdit_pipe1_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_pipe1_wall_thickness, "'pipe #1 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_pipe1_wall_thickness.setFocus()
            return True

        distance = check_inputs(self.lineEdit_pipe1_distance, "'pipe #1 distance'")
        if distance is None:
            self.lineEdit_pipe1_distance.setFocus()
            return True

        if self.comboBox_pipe1_connection.currentIndex() == 0:
            rot_angle = self.spinBox_pipe1_rotation_angle.value()
            values = [length, diameter, wall_thickness, distance, rot_angle]
        else:
            values = [length, diameter, wall_thickness, distance]

        self.suppression_device_data["pipe #1 parameters"] = values

    def check_pipe2_info(self):

        length = check_inputs(self.lineEdit_pipe2_length, "'pipe #2 length'")
        if length is None:
            self.lineEdit_pipe2_length.setFocus()
            return True

        diameter = check_inputs(self.lineEdit_pipe2_diameter, "'pipe #2 diameter'")
        if diameter is None:
            self.lineEdit_pipe2_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_pipe2_wall_thickness, "'pipe #2 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_pipe2_wall_thickness.setFocus()
            return True

        distance = check_inputs(self.lineEdit_pipe2_distance, "'pipe #2 distance'")
        if distance is None:
            self.lineEdit_pipe2_distance.setFocus()
            return True

        if self.comboBox_pipe2_connection.currentIndex() == 0:
            rot_angle = self.spinBox_pipe2_rotation_angle.value()
            values = [length, diameter, wall_thickness, distance, rot_angle]
        else:
            values = [length, diameter, wall_thickness, distance]

        self.suppression_device_data["pipe #2 parameters"] = values

    def check_pipe3_info(self):

        length = check_inputs(self.lineEdit_pipe3_length, "'pipe #3 length'")
        if length is None:
            self.lineEdit_pipe3_length.setFocus()
            return True

        diameter = check_inputs(self.lineEdit_pipe3_diameter, "'pipe #3 diameter'")
        if diameter is None:
            self.lineEdit_pipe3_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_pipe3_wall_thickness, "'pipe #3 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_pipe3_wall_thickness.setFocus()
            return True

        distance = check_inputs(self.lineEdit_pipe3_distance, "'pipe #3 distance'")
        if distance is None:
            self.lineEdit_pipe3_distance.setFocus()
            return True

        self.suppression_device_data["pipe 3# parameters"] = [length, diameter, wall_thickness, distance]

    def check_psd_inputs(self):

        self.suppression_device_data = dict()

        if self.lineEdit_device_label.text() == "":
            self.lineEdit_device_label.setFocus()
            window_title = "Error"
            title = "Empty field detected"
            message = "Enter a device label to proceed."
            PrintMessageInput([window_title, title, message])
            return True
        else:
            self.suppression_device_data["device label"] = self.lineEdit_device_label.text()

        axes = ["along x-axis", "along y-axis", "along z-axis"]
        index = self.comboBox_main_axis.currentIndex()
        self.suppression_device_data["main axis"] = axes[index]

        if self.comboBox_connection_type.currentIndex() == 0:
            self.suppression_device_data["connection type"] = "discharge"
        else:
            self.suppression_device_data["connection type"] = "sucction"

        if self.check_connecting_coords():
            return True

        if self.check_volume1_info():
            return True

        if self.check_volume2_info():
            return True

        if self.check_pipe1_info():
            return True

        if self.check_pipe2_info():
            return True

        if self.comboBox_number_volumes.currentIndex() == 0:

            index_vol_connect = self.comboBox_volumes_connection.currentIndex()
            if index_vol_connect == 0:
                self.suppression_device_data["volumes connection"] = "pipe"
            elif index_vol_connect == 1:
                self.suppression_device_data["volumes connection"] = "pipe-plate"
            elif index_vol_connect == 2:
                self.suppression_device_data["volumes connection"] = "perf. plate"

            value = check_inputs(self.lineEdit_volumes_spacing, "'volumes spacing'")
            if value is None:
                self.lineEdit_volumes_spacing.setFocus()
                return True

            self.suppression_device_data["volumes spacing"] = value

            if index_vol_connect in [0, 2]:
                if self.check_pipe3_info():
                    return True

    def confirm_button_pressed(self):

        if self.check_psd_inputs():
            self.suppression_device_data = dict()
            return

        tag = self.get_device_tag()
        self.project.PSD.add_pulsation_suppression_device(tag, self.suppression_device_data)

        self.close()

    def get_device_tag(self):
        index = 1
        _run = True
        while _run:
            if index in self.project.PSD.pulsation_suppression_device.keys():
                index += 1
            else:
                _run = False
        return index

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()