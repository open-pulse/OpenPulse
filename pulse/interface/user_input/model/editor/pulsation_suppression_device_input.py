from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.editor.single_volume_psd import SingleVolumePSD
from pulse.editor.dual_volume_psd import DualVolumePSD

from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.utils import check_inputs

import numpy as np


window_title_1 = "Error"
window_title_2 = "Warning"

class PulsationSuppressionDeviceInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ui_path = UI_DIR / "model/editor/pulsation_suppression_device_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.project = app().project

        self.preprocessor = app().project.model.preprocessor
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        self.load_psd_info()
        self.selection_callback()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.keep_window_open = True

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_main_axis : QComboBox
        self.comboBox_connection_pipe : QComboBox
        self.comboBox_number_volumes : QComboBox
        self.comboBox_volumes_connection : QComboBox
        self.comboBox_pipe1_connection : QComboBox
        self.comboBox_pipe2_connection : QComboBox
        self.comboBox_tuned_filter : QComboBox

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
        self.label_volume1 : QLabel
        self.label_volume2 : QLabel

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
        self.lineEdit_selection : QLineEdit

        # QPushButton
        self.pushButton_cancel : QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_remove : QPushButton
        self.pushButton_reset : QPushButton

        # QSpinBox
        self.spinBox_pipe1_rotation_angle : QDoubleSpinBox
        self.spinBox_pipe2_rotation_angle : QDoubleSpinBox
        self.spinBox_volumes_spacing : QDoubleSpinBox

        # QTavbWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_psd_info : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_main_axis.currentIndexChanged.connect(self.update_the_rotation_angle)
        self.comboBox_number_volumes.currentIndexChanged.connect(self.number_volumes_callback)
        self.comboBox_pipe1_connection.currentIndexChanged.connect(self.pipe_connection_callback)
        self.comboBox_pipe2_connection.currentIndexChanged.connect(self.pipe_connection_callback)
        self.comboBox_volumes_connection.currentIndexChanged.connect(self.volumes_connection_callback)
        self.comboBox_tuned_filter.currentIndexChanged.connect(self.tuned_filter_callback)
        #
        self.lineEdit_volume1_length.textChanged.connect(self.update_tuned_filter_callback)
        self.lineEdit_volume1_length.textChanged.connect(self.update_tuned_filter_callback)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.confirm_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        #
        self.treeWidget_psd_info.itemClicked.connect(self.on_click_item)
        self.treeWidget_psd_info.itemDoubleClicked.connect(self.on_double_click_item)
        #
        self.update_the_rotation_angle()
        self.number_volumes_callback()
        self.update_tuned_filter_callback()
        #
        app().main_window.selection_changed.connect(self.selection_callback)

    def selection_callback(self):
        selected_nodes = app().main_window.list_selected_nodes()
        if len(selected_nodes) == 1:
            node = self.preprocessor.nodes[selected_nodes[0]]
            self.lineEdit_connecting_coord_x.setText(str(round(node.x, 6)))
            self.lineEdit_connecting_coord_y.setText(str(round(node.y, 6)))
            self.lineEdit_connecting_coord_z.setText(str(round(node.z, 6)))

    def _config_widgets(self):
        #
        self.lineEdit_device_label.setFocus()
        self.lineEdit_selection.setDisabled(True)
        self.pushButton_remove.setDisabled(True)
        #
        self.config_treeWidget()        

    def config_treeWidget(self):
        widths = [120, 140, 140, 140]
        header_labels = ["PSD label", "Connection type", "Connection point", "Lines"]
        for col, label in enumerate(header_labels):
            self.treeWidget_psd_info.headerItem().setText(col, label)
            self.treeWidget_psd_info.headerItem().setTextAlignment(col, Qt.AlignCenter)
            self.treeWidget_psd_info.setColumnWidth(col, widths[col])

    def pipe_connection_callback(self):

        index_1 = self.comboBox_pipe1_connection.currentIndex()
        index_2 = self.comboBox_pipe2_connection.currentIndex()
        
        self.label_rotation_angle_pipe1.setDisabled(bool(index_1))
        self.label_rotation_angle_pipe2.setDisabled(bool(index_2))
        self.label_rotation_angle_pipe1_unit.setDisabled(bool(index_1))
        self.label_rotation_angle_pipe2_unit.setDisabled(bool(index_2))

        self.spinBox_pipe1_rotation_angle.setDisabled(bool(index_1))
        self.spinBox_pipe2_rotation_angle.setDisabled(bool(index_2))

        self.lineEdit_pipe1_distance.setDisabled(bool(index_1))
        self.lineEdit_pipe2_distance.setDisabled(bool(index_2))

        if bool(index_1):
            self.lineEdit_pipe1_distance.setText("")

        if bool(index_2):
            self.lineEdit_pipe2_distance.setText("")

    def number_volumes_callback(self):

        index = self.comboBox_number_volumes.currentIndex()
        self.comboBox_volumes_connection.setDisabled(bool(index))

        self.label_volumes_connection.setDisabled(bool(index))
        self.label_volumes_spacing.setDisabled(bool(index))
        self.label_volumes_spacing_unit.setDisabled(bool(index))

        self.label_pipe3.setDisabled(bool(index))
        self.lineEdit_pipe3_length.setDisabled(bool(index))
        self.lineEdit_pipe3_diameter.setDisabled(bool(index))
        self.lineEdit_pipe3_wall_thickness.setDisabled(bool(index))
        self.lineEdit_pipe3_distance.setDisabled(bool(index))
        self.spinBox_volumes_spacing.setDisabled(bool(index))

        self.label_volume2.setDisabled(bool(index))
        self.lineEdit_volume2_length.setDisabled(bool(index))
        self.lineEdit_volume2_diameter.setDisabled(bool(index))
        self.lineEdit_volume2_wall_thickness.setDisabled(bool(index))

        if index:
            # self.spinBox_volumes_spacing.setValue(0.025)
            self.comboBox_volumes_connection.setCurrentIndex(3)
        else:
            self.spinBox_volumes_spacing.setFocus()
            self.comboBox_volumes_connection.setCurrentIndex(0)

        self.update_tuned_filter_callback()

    def volumes_connection_callback(self):
        index = self.comboBox_volumes_connection.currentIndex()
        if index == 2:
            self.lineEdit_pipe3_distance.setText("")
            self.lineEdit_pipe3_distance.setDisabled(True)
        else:
            if self.comboBox_number_volumes.currentIndex() == 0:
                self.lineEdit_pipe3_distance.setEnabled(True)

    def tuned_filter_callback(self):

        index = self.comboBox_tuned_filter.currentIndex()

        if index == 1:
            self.comboBox_pipe1_connection.setCurrentIndex(0)
            self.comboBox_pipe2_connection.setCurrentIndex(0)

        self.comboBox_pipe1_connection.setDisabled(bool(index))
        self.comboBox_pipe2_connection.setDisabled(bool(index))

        self.lineEdit_pipe1_distance.setDisabled(bool(index))
        self.lineEdit_pipe2_distance.setDisabled(bool(index))
        self.lineEdit_pipe3_distance.setDisabled(bool(index))
        self.lineEdit_pipe3_length.setDisabled(bool(index))

        self.update_tuned_filter_callback()

    def update_tuned_filter_callback(self):

        if self.comboBox_tuned_filter.currentIndex() == 1:

            volume_spacing = self.spinBox_volumes_spacing.value()

            if self.lineEdit_volume1_length.text() != "":
                volume1_length = check_inputs(self.lineEdit_volume1_length, "'volume #1 length'")
                if volume1_length is None:
                    self.lineEdit_volume1_length.setFocus()
                    return True

            if self.lineEdit_volume2_length.text() != "": 
                volume2_length = check_inputs(self.lineEdit_volume2_length, "'volume #2 length'")
                if volume2_length is None:
                    self.lineEdit_volume2_length.setFocus()
                    return True

            if self.comboBox_number_volumes.currentIndex() == 1:

                self.lineEdit_pipe1_distance.setText(f"{round(volume1_length*(1/4), 6)}")
                self.lineEdit_pipe2_distance.setText(f"{round(volume1_length*(3/4), 6)}")

            else:

                pipe2_distance = volume1_length + volume_spacing + volume2_length / 2
                pipe3_length = volume1_length + volume_spacing + volume2_length / 4

                self.lineEdit_pipe1_distance.setText(f"{round(volume1_length*(1/2), 6)}")
                self.lineEdit_pipe3_distance.setText(f"{round(volume1_length*(3/4), 6)}")

                self.lineEdit_pipe2_distance.setText(f"{round(pipe2_distance, 6)}")
                self.lineEdit_pipe3_length.setText(f"{round(pipe3_length, 6)}")

                self.lineEdit_pipe3_distance.setDisabled(True)
                self.lineEdit_pipe3_length.setDisabled(True)

    def tab_event_callback(self):
        self.pushButton_remove.setDisabled(True)
        if self.tabWidget_main.currentIndex() == 0:
            self.pushButton_cancel.setDisabled(False)
            self.pushButton_confirm.setDisabled(False)
        else:
            self.pushButton_cancel.setDisabled(True)
            self.pushButton_confirm.setDisabled(True)

    def on_click_item(self, item):
        self.lineEdit_selection.setText(item.text(0))
        self.pushButton_remove.setDisabled(False)
        if item.text(0) in self.psds_lines.keys():
            device_lines = self.psds_lines[item.text(0)]
            app().main_window.set_selection(lines = device_lines)

    def on_double_click_item(self, item):
        self.on_click_item(item)
        # TODO: get detailed information about selected PSD

    def update_the_rotation_angle(self):
        index = self.comboBox_main_axis.currentIndex()
        if index == 0:
            self.lineEdit_rotation_plane.setText("YZ-plane")
        elif index == 1:
            self.lineEdit_rotation_plane.setText("XZ-plane")
        elif index == 2:
            self.lineEdit_rotation_plane.setText("XY-plane")

    def check_psd_label(self):

        psd_label = self.lineEdit_device_label.text()
        if psd_label == "":
            self.lineEdit_device_label.setFocus()
            title = "Empty field detected"
            message = "Enter a device label to proceed."
            PrintMessageInput([window_title_2, title, message])
            return True, None
        
        elif psd_label in self.psds_data.keys():
            self.lineEdit_device_label.setFocus()
            
            title = "Invalid input"
            message = "The typed 'device label' has already been applied to other PSD. "
            message += "You should enter a different label to proceed with the PSD configuration."
            PrintMessageInput([window_title_2, title, message])
            return True, None
        
        return False, psd_label

    def check_connecting_coords(self):

        coord_x = check_inputs(self.lineEdit_connecting_coord_x, "'connecting coord. x'", only_positive=False)
        if coord_x is None:
            self.lineEdit_connecting_coord_x.setFocus()
            return True

        coord_y = check_inputs(self.lineEdit_connecting_coord_y, "'connecting coord. y'", only_positive=False)
        if coord_y is None:
            self.lineEdit_connecting_coord_y.setFocus()
            return True
        
        coord_z = check_inputs(self.lineEdit_connecting_coord_z, "'connecting coord. z'", only_positive=False)
        if coord_z is None:
            self.lineEdit_connecting_coord_z.setFocus()
            return True
        
        self._psd_data["connecting coords"] = [round(coord_x, 6), round(coord_y, 6), round(coord_z, 6)]

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

        self._psd_data["volume #1 parameters"] = [diameter, wall_thickness, length]

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

        self._psd_data["volume #2 parameters"] = [diameter, wall_thickness, length]

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

        if self.comboBox_pipe1_connection.currentIndex() == 0:

            distance = check_inputs(self.lineEdit_pipe1_distance, "'pipe #1 distance'")
            if distance is None:
                self.lineEdit_pipe1_distance.setFocus()
                return True

            rot_angle = self.spinBox_pipe1_rotation_angle.value()
            values = [diameter, wall_thickness, length, distance, rot_angle]

        else:
            values = [diameter, wall_thickness, length]

        self._psd_data["pipe #1 parameters"] = values

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

        if self.comboBox_pipe2_connection.currentIndex() == 0:
            
            distance = check_inputs(self.lineEdit_pipe2_distance, "'pipe #2 distance'")
            if distance is None:
                self.lineEdit_pipe2_distance.setFocus()
                return True

            rot_angle = self.spinBox_pipe2_rotation_angle.value()
            values = [diameter, wall_thickness, length, distance, rot_angle]

        else:
            values = [diameter, wall_thickness, length]

        self._psd_data["pipe #2 parameters"] = values

    def check_pipe3_info(self):
        
        diameter = check_inputs(self.lineEdit_pipe3_diameter, "'pipe #3 diameter'")
        if diameter is None:
            self.lineEdit_pipe3_diameter.setFocus()
            return True

        wall_thickness = check_inputs(self.lineEdit_pipe3_wall_thickness, "'pipe #3 wall_thickness'")
        if wall_thickness is None:
            self.lineEdit_pipe3_wall_thickness.setFocus()
            return True
            
        index = self.comboBox_volumes_connection.currentIndex()
        if index in [1, 2]:
            vol_diameter, *args = self._psd_data["volume #1 parameters"]           

        if index in [0 ,1]:

            length = check_inputs(self.lineEdit_pipe3_length, "'pipe #3 length'")
            if length is None:
                self.lineEdit_pipe3_length.setFocus()
                return True

            distance = check_inputs(self.lineEdit_pipe3_distance, "'pipe #3 distance'")
            if distance is None:
                self.lineEdit_pipe3_distance.setFocus()
                return True

        if index in [0, 1]:
            parameters = [diameter, wall_thickness, length, distance]
            self._psd_data["pipe #3 parameters"] = parameters  

        if index in [1, 2]:
            _length = self._psd_data["volumes spacing"]
            _wall_thickness = round((vol_diameter - diameter) / 2 + wall_thickness, 6)
            _parameters = [vol_diameter, _wall_thickness, _length]

            self._psd_data["pipe #4 parameters"] = _parameters

    def check_psd_inputs(self):

        self._psd_data = dict()

        main_axis = self.comboBox_main_axis.currentText()[1:]
        self._psd_data["main axis"] = main_axis

        if self.comboBox_connection_pipe.currentIndex() == 0:
            self._psd_data["connection pipe"] = "pipe #1"
        else:
            self._psd_data["connection pipe"] = "pipe #2"

        if self.check_connecting_coords():
            return True

        if self.check_volume1_info():
            return True

        if self.comboBox_number_volumes.currentIndex() == 0:
    
            if self.check_volume2_info():
                return True
            
            if self.check_pipe1_info():
                return True

            if self.check_pipe2_info():
                return True

            self._psd_data["volumes spacing"] = self.spinBox_volumes_spacing.value()

            if self.check_pipe3_info():
                return True
            
            if self.check_geometric_criteria_for_double_volume_psd():
                return True

            index_vol_connect = self.comboBox_volumes_connection.currentIndex()

            if index_vol_connect == 0:
                self._psd_data["volumes connection"] = "pipe"

            elif index_vol_connect == 1:
                self._psd_data["volumes connection"] = "pipe-plate"

            elif index_vol_connect == 2:
                self._psd_data["volumes connection"] = "perf. plate"

        else:

            if self.check_pipe1_info():
                return True

            if self.check_pipe2_info():
                return True

            if self.check_geometric_criteria_for_single_volume_psd():
                return True

    def check_geometric_criteria_for_single_volume_psd(self):

        volume1_length = self._psd_data["volume #1 parameters"][2]

        if len(self._psd_data["pipe #1 parameters"]) == 5:

            pipe1_diameter = self._psd_data["pipe #1 parameters"][0]
            pipe1_distance = self._psd_data["pipe #1 parameters"][3]

            if pipe1_distance <= pipe1_diameter / 2:
                title = "Invalid pipe #1 distance"
                message = "The 'pipe #1 distance' must be greater than half of the 'pipe #1 diameter'"
                PrintMessageInput([window_title_2, title, message])
                return True

            if len(self._psd_data["pipe #2 parameters"]) == 3: # i.e. pipe #2 is axial
                if pipe1_distance >= volume1_length - pipe1_diameter / 2:
                    title = "Invalid pipe #1 distance"
                    message = "For the radial-axial psd configuration, the 'pipe #1 distance' should be less "
                    message += "than the 'volume #1 length'minus the half of the 'pipe #1 diameter'."
                    PrintMessageInput([window_title_2, title, message])
                    return True
                
        if len(self._psd_data["pipe #2 parameters"]) == 5:

            pipe2_diameter = self._psd_data["pipe #2 parameters"][1]
            pipe2_distance = self._psd_data["pipe #2 parameters"][3]

            if pipe2_distance >= volume1_length - pipe2_diameter / 2:
                title = "Invalid pipe #2 distance"
                message = "The 'pipe #2 distance' should be less than the 'volume #1 length' "
                message += "minus the half of the 'pipe #2 diameter'."
                PrintMessageInput([window_title_2, title, message])
                return True

            if len(self._psd_data["pipe #1 parameters"]) == 5:

                pipe1_distance = self._psd_data["pipe #1 parameters"][3]

                if pipe1_distance >= pipe2_distance:
                    title = "Invalid pipe #1 distance"
                    message = "The 'pipe #1 distance' should be less than the 'pipe #2 distance'."
                    PrintMessageInput([window_title_2, title, message])
                    return True
            
            if len(self._psd_data["pipe #1 parameters"]) == 3:
                if pipe2_distance <= pipe2_diameter:
                    title = "Invalid pipe #2 length"
                    message = "For the axial-radial configuration, the 'pipe #2 distance' must be greater than half of the 'pipe #2 diameter'"
                    PrintMessageInput([window_title_2, title, message])
                    return True
                
    def check_geometric_criteria_for_double_volume_psd(self):
        
        volumes_spacing = self._psd_data["volumes spacing"]
        volume1_length = self._psd_data["volume #1 parameters"][2]
        volume2_length = self._psd_data["volume #2 parameters"][2]
        pipe3_length = self._psd_data["pipe #3 parameters"][2]
        pipe3_distance = self._psd_data["pipe #3 parameters"][3]
        

        if len(self._psd_data["pipe #1 parameters"]) == 5: # i.e. pipe #1 is radial
            pipe1_distance = self._psd_data["pipe #1 parameters"][3]
            pipe1_diameter = self._psd_data["pipe #1 parameters"][0]

            if pipe1_distance >= volume1_length - pipe1_diameter / 2: # i.e. pipe #1 distance must be 
                title = "Invalid pipe #1 distance"
                message = "The 'pipe #1 distance' must be less than the 'volume #1 length' "
                message += "minus the half of the 'pipe #1 diameter'"
                PrintMessageInput([window_title_2, title, message])
                return True
            
            if pipe1_distance <= pipe1_diameter / 2:
                title = "Invalid pipe #1 distance"
                message = "The 'pipe #1 distance' must be greater than half of the 'pipe #1 diameter'"
                PrintMessageInput([window_title_2, title, message])
                return True

        
        if len(self._psd_data["pipe #2 parameters"]) == 5: # i.e. pipe #2 is radial
            pipe2_distance = self._psd_data["pipe #2 parameters"][3]
            pipe2_diameter = self._psd_data["pipe #2 parameters"][0]

            if pipe2_distance >= volume1_length + volumes_spacing + volume2_length - pipe2_diameter / 2 : # i.e. pipe #2 distance must be less than "volume #2 distance + length"
                title = "Invalid pipe #2 distance"
                message = "The 'pipe #2 distance' must be less than the 'volume #1 length' "
                message += "+ 'volumes spacing' + 'volume #2 length' "
                message += "minus the half of the 'pipe #2 diameter'"
                PrintMessageInput([window_title_2, title, message])
                return True
            
            if pipe2_distance - pipe2_diameter / 2 <= volume1_length + volumes_spacing: 
                title = "Invalid pipe #2 distance"
                message = "The 'pipe #2 distance' minus the 'pipe #2 diameter / 2' must be greater than the volume #1 length plus "
                message += "the 'volumes spacing'"
                PrintMessageInput([window_title_2, title, message])
                return True

        # TODO: check if the cases where these are equal to each other and see if they are valid
        if pipe3_distance > volume1_length:
            title = "Invalid pipe #3 length"
            message = "The 'pipe #3 distance' must be less than the 'volume #1 length'"
            PrintMessageInput([window_title_2, title, message])
            return True
        
        if pipe3_length < volumes_spacing:
            title = "Invalid pipe #3 length"
            message = "The 'pipe #3 length' must be greater than or equal to the 'volumes spacing'"
            PrintMessageInput([window_title_2, title, message])
            return True            
        
        if pipe3_distance + pipe3_length < volume1_length + volumes_spacing:
            title = "Invalid combination of pipe #3 length and distance"
            message = "The pipe #3 length plus the pipe #3 distance must be less "
            message += "than the volume #1 length plus the volumes spacing"
            PrintMessageInput([window_title_2, title, message])
            return True

    def get_values(self, values: np.ndarray):
        return list(np.array(np.round(values, 6), dtype=float))

    def confirm_callback(self):

        stop, psd_label = self.check_psd_label()
        if stop:
            return

        if self.check_psd_inputs():
            self._psd_data.clear()
            return

        aux = self.psds_data.copy()
        for key, data in aux.items():
            if data == self._psd_data:
                self.psds_data.pop(key)
                break
        
        self.psds_data[psd_label] = self._psd_data

        if "volume #2 parameters" in self._psd_data.keys():
            device = DualVolumePSD(self._psd_data)
        else:
            device = SingleVolumePSD(self._psd_data)

        self.build_device(psd_label, device)
        self.actions_to_finalize()

        # remember, you should to generate the mesh
        self.write_psd_nodal_properties_in_file()
        self.set_element_length_corrections(psd_label, device)

        app().main_window.update_plots()
        self.close()

    def build_device(self, psd_label: str, device: (SingleVolumePSD | DualVolumePSD)):

        lines_data = app().pulse_file.read_line_properties_from_file()
        if lines_data is None:
            lines_data = dict()

        line_tags = list(lines_data.keys())
        if line_tags:
            shifted_line = max(line_tags) + 1
        else:
            shifted_line = 1

        device.process_segment_data()

        counter = 0
        for i in range(len(device.segment_data)):

            start_coords, end_coords, section_data, segment_label = device.segment_data[i]

            if isinstance(section_data, list):

                aux = { 
                        "structure_name" : "pipe",
                        "start_coords" : self.get_values(start_coords),
                        "end_coords" : self.get_values(end_coords),
                        "section_type_label" : "Pipe",
                        "section_parameters" : section_data,
                        "structural_element_type" : "pipe_1",
                        "psd_label" : psd_label,
                        "psd_segment" : segment_label
                       }

                tag = int(shifted_line + i)

                self.properties._set_multiple_line_properties(aux, tag)

            else:

                coords = list()
                coords.extend(self.get_values(start_coords))
                coords.extend(self.get_values(end_coords))

                link = { 
                        "psd_label" : psd_label,
                        "coords" : coords,
                        "link_type" : section_data
                        }

                counter += 1
                self.psds_data[psd_label][f"Link-{counter}"] = link

        app().pulse_file.write_line_properties_in_file()
        self.write_psd_element_properties_in_file(psd_label, device)

    def write_psd_nodal_properties_in_file(self):
            
        for psd_label, psd_data in self.psds_data.items():
            for key, data in psd_data.items():

                if "Link-" in key:
                    link_type = data["link_type"]

                    coords = data["coords"]
                    node_id1 = self.preprocessor.get_node_id_by_coordinates(coords[:3])
                    node_id2 = self.preprocessor.get_node_id_by_coordinates(coords[3:])
                    node_ids = [node_id1, node_id2]

                    if link_type == "acoustic_link":
                        self.properties._set_nodal_property("psd_acoustic_link", data, node_ids)

                    if link_type == "structural_link":
                        self.properties._set_nodal_property("psd_structural_links", data, node_ids)

        app().pulse_file.write_nodal_properties_in_file()

    def write_psd_element_properties_in_file(self, psd_label: str, device: (SingleVolumePSD | DualVolumePSD)):

        # psd_data = app().pulse_file.read_psd_data_from_file()
        if self.psds_data is None:
            return

        index = 0
        if psd_label in self.psds_data.keys():
            for (_coords, _connection_type) in device.branch_data:
                index += 1
                coords = self.get_values(_coords)
                key = f"element_length_correction - {index}"
                self.psds_data[psd_label][key] = {   
                                                    "connection_coords" : coords,
                                                    "connection_type" : _connection_type 
                                                  }

        app().pulse_file.write_psd_data_in_file(self.psds_data)

    def remove_psd_related_line_properties(self, psd_labels: str | list):

        if isinstance(psd_labels, str):
            psd_labels = [psd_labels]

        lines_data = app().pulse_file.read_line_properties_from_file()
        if lines_data is None:
            return

        remove_gaps = False
        for line_id, data in lines_data.items():
            if "psd_label" in data.keys():
                if data["psd_label"] in psd_labels:
                    for property in data.keys():
                        self.properties._remove_line_property(property, line_id)
                    remove_gaps = True

        app().pulse_file.write_line_properties_in_file()

        if remove_gaps:
            app().pulse_file.remove_line_gaps_from_line_properties_file()

    def remove_psd_related_nodal_properties(self, psd_labels: str | list):

        if isinstance(psd_labels, str):
            psd_labels = [psd_labels]

        aux = self.properties.nodal_properties.copy()
        for (property, *args), data in aux.items():
            if "psd_label" in data.keys():
                if data["psd_label"] in psd_labels:
                    self.properties._remove_nodal_property(property, args)

        app().pulse_file.write_line_properties_in_file()

    def remove_selected_psd(self, psd_label: str):

        if psd_label in self.psds_data.keys():
            self.psds_data.pop(psd_label)

        self.remove_psd_related_line_properties(psd_label)
        self.remove_psd_related_nodal_properties(psd_label)
        self.remove_psd_related_element_properties(psd_label)

        self.actions_to_finalize()
        app().main_window.update_plots()

    # def update_length_correction_after_psd_removal(self):

    #     psds_data = app().pulse_file.read_psd_data_from_file()
    #     if psds_data is None:
    #         return

    #     for device_label, psd_data in psds_data.items():

    #         elc_data = list()
    #         for key, data in psd_data.items():
    #             if "element_length_correction -" in key:
    #                 elc_coords = data["connection_coords"]
    #                 elc_type = data["connection_type"]
    #                 elc_data.append((elc_coords, elc_type))

    #         if elc_data:
    #             self.set_element_length_corrections(device_label, elc_data)

    def set_element_length_corrections(self, psd_label: str, device: (SingleVolumePSD | DualVolumePSD)):

        for (coords, connection_type) in device.branch_data:

            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
            elements = self.preprocessor.neighboor_elements_of_node(node_id)
            element_ids = [element.index for element in elements]

            if connection_type == "radial":
                _type = 1

            else:
                _type = 0

            data = {
                    "correction_type" : _type,
                    "psd_label" : psd_label
                    }

            self.preprocessor.set_element_length_correction_by_element(element_ids, data)
            self.properties._set_element_property("element_length_correction", data, element_ids)
            app().pulse_file.write_element_properties_in_file()

    def remove_psd_related_element_properties(self, psd_label: str):

        element_ids = list()
        for (_property, element_id), data in self.properties.element_properties.items():
            if _property == "element_length_correction":
                data: dict
                if "psd_label" in data.keys():
                    if psd_label == "_remove_all_":
                        element_ids.append(element_id)
                    elif psd_label == data["psd_label"]:
                        element_ids.append(element_id)
        
        self.preprocessor.set_element_length_correction_by_element(element_ids, None)
        self.properties._remove_element_property("element_length_correction", element_ids) 
        app().pulse_file.write_element_properties_in_file()
        # self.update_length_correction_after_psd_removal()

    def remove_callback(self):

        if self.lineEdit_selection.text() != "":

            device_label = self.lineEdit_selection.text()
            self.remove_selected_psd(device_label)
            self.load_psd_info()

            app().main_window.update_plots()

    def reset_callback(self):

        self.hide()

        title = "Resetting of the Pulsation Suppression Devices"
        message = "Would you to remove the all Pulsation Suppression Devices from model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Proceed"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            self.psds_data.clear()

            psds_labels = list(self.psds_data.keys())

            self.remove_psd_related_line_properties(psds_labels)
            self.remove_psd_related_nodal_properties(psds_labels)
            self.remove_psd_related_element_properties("_remove_all_")

            self.actions_to_finalize()
            app().main_window.update_plots()

    def load_psd_info(self):

        self.treeWidget_psd_info.clear()
        self.psds_lines = app().loader.get_psd_related_lines()
        self.psds_data = app().pulse_file.read_psd_data_from_file()
        if self.psds_data is None:
            self.psds_data = dict()

        for key, psd_data in self.psds_data.items():
            coords = psd_data["connecting coords"]
            connection = psd_data["connection pipe"]
            psd_lines = self.psds_lines[key]
            new = QTreeWidgetItem([key, connection, str(coords), str(psd_lines)])
            for col in range(4):
                new.setTextAlignment(col, Qt.AlignCenter)
            self.treeWidget_psd_info.addTopLevelItem(new)

        if self.psds_data:
            if self.psds_data:
                self.tabWidget_main.setTabVisible(1, True)
            else:
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(1, False)

    def get_device_tag(self):
        index = 1
        _run = True
        while _run:
            if index in self.psds_data.keys():
                index += 1
            else:
                _run = False
        return index

    def actions_to_finalize(self):
        app().pulse_file.write_psd_data_in_file(self.psds_data)
        app().loader.load_project_data()
        app().project.initial_load_project_actions()
        app().loader.load_mesh_dependent_properties()
        app().main_window.initial_project_action(True)
        self.load_psd_info()
        # app().main_window.use_structural_setup_workspace()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_callback()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)