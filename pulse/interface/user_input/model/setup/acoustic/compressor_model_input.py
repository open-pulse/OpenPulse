from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.fluid.set_fluid_input import SetFluidInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from pulse.model.compressor_model import CompressorModel
# from compressors.reciprocating.model import CompressorModel

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5

class CompressorModelInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/compressor_model_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widget()
        self.selection_callback()
        self.load_compressor_excitation_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.complete = False
        self.keep_window_open = True

        self.aquisition_parameters_processed = False
        self.not_update_event = False

        self.before_run = app().project.get_pre_solution_model_checks()    

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_connection_setup: QComboBox
        self.comboBox_cylinder_acting: QComboBox
        self.comboBox_frequency_resolution: QComboBox
        self.comboBox_stage: QComboBox
        self.comboBox_suction_pressure_units: QComboBox
        self.comboBox_suction_temperature_units: QComboBox

        # QLabel
        self.label_molar_mass: QLabel
        self.label_molar_mass_unit: QLabel
        self.label_isentropic_exp: QLabel
        self.label_isentropic_exp_unit: QLabel

        # QLineEdit
        self.lineEdit_suction_node_id: QLineEdit
        self.lineEdit_discharge_node_id: QLineEdit
        self.lineEdit_frequency_resolution: QLineEdit
        self.lineEdit_number_of_revolutions: QLineEdit
        self.lineEdit_bore_diameter: QLineEdit
        self.lineEdit_stroke: QLineEdit
        self.lineEdit_connecting_rod_length: QLineEdit
        self.lineEdit_rod_diameter: QLineEdit
        self.lineEdit_pressure_ratio: QLineEdit
        self.lineEdit_clearance_head_end: QLineEdit
        self.lineEdit_clearance_crank_end: QLineEdit
        self.lineEdit_rotational_speed: QLineEdit
        self.lineEdit_isentropic_exponent: QLineEdit
        self.lineEdit_molar_mass: QLineEdit
        self.lineEdit_pressure_at_suction: QLineEdit
        self.lineEdit_temperature_at_suction: QLineEdit
        self.lineEdit_selected_id: QLineEdit
        self.lineEdit_connection_type: QLineEdit
        self.current_lineEdit = self.lineEdit_suction_node_id

        # QPushButton
        self.pushButton_invert_selection: QPushButton
        self.pushButton_plot_PV_diagram_head_end: QPushButton
        self.pushButton_plot_PV_diagram_crank_end: QPushButton
        self.pushButton_plot_PV_diagram_both_ends: QPushButton
        self.pushButton_plot_piston_position_and_velocity_time: QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_suction_time: QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time: QPushButton
        self.pushButton_plot_rod_pressure_load_frequency: QPushButton
        self.pushButton_plot_rod_pressure_load_time: QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency: QPushButton
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency: QPushButton
        self.pushButton_plot_pressure_head_end_angle: QPushButton
        self.pushButton_plot_volume_head_end_angle: QPushButton
        self.pushButton_plot_pressure_crank_end_angle: QPushButton
        self.pushButton_plot_volume_crank_end_angle: QPushButton
        self.pushButton_process_aquisition_parameters: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_reset_entries: QPushButton

        # QSpinBox
        self.spinBox_number_of_points: QSpinBox
        self.spinBox_max_frequency: QSpinBox
        self.spinBox_number_of_cylinders: QSpinBox
        self.spinBox_tdc1_crank_angle: QSpinBox
        self.spinBox_tdc2_crank_angle: QSpinBox
        self.spinBox_capacity: QSpinBox

        # QTabWidget
        self.tabWidget_compressor: QTabWidget

        # QTreeWidget
        self.treeWidget_compressor_excitation: QTreeWidget

    def _config_widget(self):
        self.treeWidget_compressor_excitation.setColumnWidth(0, 100)
        # self.treeWidget_compressor_excitation.setColumnWidth(1, 140)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_compressor_excitation.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_connection_setup.currentIndexChanged.connect(self.update_compressor_to_pipeline_connections)
        self.comboBox_cylinder_acting.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_stage.currentIndexChanged.connect(self.comboBox_event_stage)
        #
        self.pushButton_invert_selection.clicked.connect(self.invert_nodes_selection_callback)
        self.pushButton_plot_PV_diagram_head_end.clicked.connect(self.plot_PV_diagram_head_end)
        self.pushButton_plot_PV_diagram_crank_end.clicked.connect(self.plot_PV_diagram_crank_end)
        self.pushButton_plot_PV_diagram_both_ends.clicked.connect(self.plot_PV_diagram_both_ends)
        self.pushButton_plot_volumetric_flow_rate_at_suction_time.clicked.connect(self.plot_volumetric_flow_rate_at_suction_time)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_time.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_time)
        self.pushButton_plot_rod_pressure_load_frequency.clicked.connect(self.plot_rod_pressure_load_frequency)
        self.pushButton_plot_rod_pressure_load_time.clicked.connect(self.plot_rod_pressure_load_time)
        self.pushButton_plot_piston_position_and_velocity_time.clicked.connect(self.plot_piston_position_and_velocity_time)
        self.pushButton_plot_volumetric_flow_rate_at_suction_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_suction_frequency)
        self.pushButton_plot_volumetric_flow_rate_at_discharge_frequency.clicked.connect(self.plot_volumetric_flow_rate_at_discharge_frequency)
        self.pushButton_plot_pressure_head_end_angle.clicked.connect(self.plot_pressure_head_end_angle)
        self.pushButton_plot_volume_head_end_angle.clicked.connect(self.plot_volume_head_end_angle)
        self.pushButton_plot_pressure_crank_end_angle.clicked.connect(self.plot_pressure_crank_end_angle)
        self.pushButton_plot_volume_crank_end_angle.clicked.connect(self.plot_volume_crank_end_angle)
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.compressor_excitation_attribution_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries)
        #
        self.spinBox_number_of_points.valueChanged.connect(self.spinBox_event_number_of_points)        
        self.spinBox_max_frequency.valueChanged.connect(self.spinBox_event_max_frequency)
        self.spinBox_number_of_cylinders.valueChanged.connect(self.spinBox_event_number_of_cylinders)
        #
        self.tabWidget_compressor.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_compressor_excitation.itemClicked.connect(self.on_click_item)
        #
        self.clickable(self.lineEdit_suction_node_id).connect(self.lineEdit_1_clicked)
        self.clickable(self.lineEdit_discharge_node_id).connect(self.lineEdit_2_clicked)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.comboBox_event_stage()
        self.update_compressing_cylinders_setup()
        self.update_compressor_to_pipeline_connections()
        self.spinBox_event_number_of_cylinders()

    def invert_nodes_selection_callback(self):
        if self.comboBox_connection_setup.currentIndex() == 2:
            suction_id = self.lineEdit_suction_node_id.text()
            discharge_id = self.lineEdit_discharge_node_id.text()
            if suction_id != "" and discharge_id != "":
                self.lineEdit_suction_node_id.setText(discharge_id)        
                self.lineEdit_discharge_node_id.setText(suction_id)        

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if len(selected_nodes) == 1:

            index = self.comboBox_connection_setup.currentIndex()

            if index == 1:
                self.lineEdit_discharge_node_id.setText("")
                self.lineEdit_discharge_node_id.setDisabled(True)

            elif index == 2:
                self.lineEdit_suction_node_id.setText("")
                self.lineEdit_suction_node_id.setDisabled(True)

            self.current_lineEdit.setText(str(selected_nodes[0]))
            stop, node_id = self.check_node_id(self.current_lineEdit)

            if stop:
                self.lineEdit_suction_node_id.setFocus()
                return True

            data = self.properties._get_property("compressor_excitation", node_ids=node_id)

            if data is not None:
                compressor_info = data["parameters"]
                compressor_info["frequencies"] = app().project.model.frequencies
                self.update_compressor_inputs(compressor_info)

        else:

            self.current_lineEdit.setFocus()

    def clickable(self, widget):
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def lineEdit_1_clicked(self):
        self.current_lineEdit = self.lineEdit_suction_node_id

    def lineEdit_2_clicked(self):
        self.current_lineEdit = self.lineEdit_discharge_node_id

    def tab_event_callback(self):

        self.lineEdit_selected_id.setText("")
        self.lineEdit_connection_type.setText("")
        self.pushButton_remove.setDisabled(True)

        if self.tabWidget_compressor.currentIndex() == 3:
            self.pushButton_cancel.setDisabled(True)
            self.pushButton_confirm.setDisabled(True)
        else:
            self.pushButton_cancel.setDisabled(False)
            self.pushButton_confirm.setDisabled(False)

    def update_compressing_cylinders_setup(self):

        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.comboBox_cylinder_acting.currentIndex() == 1:
            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        if self.comboBox_cylinder_acting.currentIndex() == 2:
            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)

    def update_compressor_to_pipeline_connections(self):

        self.lineEdit_suction_node_id.setDisabled(False)
        self.lineEdit_discharge_node_id.setDisabled(False)     
        index = self.comboBox_connection_setup.currentIndex()
        node_ids = app().main_window.list_selected_nodes()

        if index == 1:
            self.current_lineEdit = self.lineEdit_suction_node_id
            self.lineEdit_discharge_node_id.setDisabled(True)
            self.lineEdit_discharge_node_id.setText("")
            if len(node_ids) == 1:
                self.lineEdit_suction_node_id.setText(str(node_ids[0]))

        elif index == 2:
            self.current_lineEdit = self.lineEdit_discharge_node_id
            self.lineEdit_suction_node_id.setDisabled(True)
            self.lineEdit_suction_node_id.setText("")
            if len(node_ids) == 1:
                self.lineEdit_discharge_node_id.setText(str(node_ids[0]))

        else:
            self.current_lineEdit = self.lineEdit_suction_node_id
            self.selection_callback()
        
    def change_aquisition_parameters_controls(self, _bool):
        self.pushButton_process_aquisition_parameters.setDisabled(_bool)
        self.spinBox_max_frequency.setDisabled(_bool)
        self.spinBox_number_of_points.setDisabled(_bool)
        self.comboBox_frequency_resolution.setDisabled(_bool)

    def get_aquisition_parameters(self, compressor_info):
        frequencies = compressor_info["frequencies"]
        rotational_speed = compressor_info["rotational_speed"]
        f_min = frequencies[0]
        f_max = frequencies[-1]
        df = frequencies[1]-frequencies[0]
        N_rev = int((1 / df) / (60 / rotational_speed))
        self.N_rev = N_rev
        return f_min, f_max, df, N_rev

    def update_compressor_inputs(self, compressor_info: dict):

        node_id = self.current_lineEdit.text()

        if "connection_type" in compressor_info.keys():

            connection_type = compressor_info["connection_type"]
            
            if connection_type == 'discharge':
                self.comboBox_connection_setup.setCurrentIndex(2)
                self.lineEdit_suction_node_id.setText("")
                self.lineEdit_suction_node_id.setDisabled(True)
                self.lineEdit_discharge_node_id.setText(node_id)
                
            if connection_type == 'suction':
                self.comboBox_connection_setup.setCurrentIndex(1)
                self.lineEdit_discharge_node_id.setText("")
                self.lineEdit_discharge_node_id.setDisabled(True)
                self.lineEdit_suction_node_id.setText(node_id)
            
        if "bore_diameter" in compressor_info.keys():
            self.lineEdit_bore_diameter.setText(str(compressor_info["bore_diameter"]))
        
        if "stroke" in compressor_info.keys():
            self.lineEdit_stroke.setText(str(compressor_info["stroke"]))
        
        if "connecting_rod_length" in compressor_info.keys():
            self.lineEdit_connecting_rod_length.setText(str(compressor_info["connecting_rod_length"]))
        
        if "rod_diameter" in compressor_info.keys():
            self.lineEdit_rod_diameter.setText(str(compressor_info["rod_diameter"]))
        
        if "pressure_ratio" in compressor_info.keys():
            self.lineEdit_pressure_ratio.setText(str(compressor_info["pressure_ratio"]))
        
        if "clearance_HE" in compressor_info.keys():
            self.lineEdit_clearance_head_end.setText(str(compressor_info["clearance_HE"]))
        
        if "clearance_CE" in compressor_info.keys():
            self.lineEdit_clearance_crank_end.setText(str(compressor_info["clearance_CE"]))
        
        if "TDC_crank_angle_1" in compressor_info.keys():
            self.spinBox_tdc1_crank_angle.setValue(int(compressor_info["TDC_crank_angle_1"]))
        
        if "rotational_speed" in compressor_info.keys():
            self.lineEdit_rotational_speed.setText(str(compressor_info["rotational_speed"]))
        
        if "capacity" in compressor_info.keys():
            self.spinBox_capacity.setValue(int(compressor_info["capacity"]))
        
        if "isentropic_exponent" in compressor_info.keys():
            self.lineEdit_isentropic_exponent.setText(str(compressor_info["isentropic_exponent"]))
        
        if "molar_mass" in compressor_info.keys():
            self.lineEdit_molar_mass.setText(str(compressor_info["molar_mass"]))
        
        if "pressure_at_suction" in compressor_info.keys():
            self.lineEdit_pressure_at_suction.setText(str(compressor_info["pressure_at_suction"]))
        
        if compressor_info["pressure_unit"] == "kgf/cm²":
            self.comboBox_suction_pressure_units.setCurrentIndex(0)
        else:
            self.comboBox_suction_pressure_units.setCurrentIndex(1)
        
        if "temperature_at_suction" in compressor_info.keys():
            self.lineEdit_temperature_at_suction.setText(str(compressor_info["temperature_at_suction"]))
        
        if compressor_info["temperature_unit"] == "°C":
            self.comboBox_suction_temperature_units.setCurrentIndex(0)
        else:
            self.comboBox_suction_temperature_units.setCurrentIndex(1)
        
        if "acting_label" in compressor_info.keys():
            acting_key = int(compressor_info["acting_label"])
            self.comboBox_cylinder_acting.setCurrentIndex(acting_key)

        if "number_of_cylinders" in compressor_info.keys():
            if compressor_info["number_of_cylinders"] == 1:
                self.spinBox_number_of_cylinders.setValue(1)
            elif compressor_info["number_of_cylinders"] == 2:
                self.spinBox_number_of_cylinders.setValue(2)
                if "TDC_crank_angle_2" in compressor_info.keys():
                    self.spinBox_tdc2_crank_angle.setValue(int(compressor_info["TDC_crank_angle_2"]))

        if "points_per_revolution" in compressor_info.keys():
            self.spinBox_number_of_points.setValue(int(compressor_info["points_per_revolution"]))

        f_min, f_max, f_step, N_rev = self.get_aquisition_parameters(compressor_info)
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))
        self.lineEdit_frequency_resolution.setText(str(f_step))

        f_steps = [0.1, 0.2, 0.5, 1.0, 2.0]
        if f_step in f_steps:
            index = f_steps.index(f_step)
            self.comboBox_frequency_resolution.setCurrentIndex(index)

    def reset_entries(self):
        self.comboBox_cylinder_acting.setCurrentIndex(0)
        self.comboBox_stage.setCurrentIndex(0)
        self.comboBox_suction_pressure_units.setCurrentIndex(0)
        self.comboBox_suction_temperature_units.setCurrentIndex(0)
        self.lineEdit_bore_diameter.setText("")
        self.lineEdit_stroke.setText("")
        self.lineEdit_connecting_rod_length.setText("")
        self.lineEdit_rod_diameter.setText("")
        self.lineEdit_pressure_ratio.setText("")
        self.lineEdit_clearance_head_end.setText("")
        self.lineEdit_clearance_crank_end.setText("")
        self.lineEdit_rotational_speed.setText("")
        self.lineEdit_isentropic_exponent.setText("")
        self.lineEdit_molar_mass.setText("")
        self.lineEdit_pressure_at_suction.setText("")
        self.lineEdit_temperature_at_suction.setText("")
        self.spinBox_number_of_cylinders.setValue(1)
        self.spinBox_tdc1_crank_angle.setValue(0)
        self.spinBox_tdc2_crank_angle.setValue(0)
        self.spinBox_capacity.setValue(100)

    def check_node_id(self, lineEdit: QLineEdit):
        
        stop, node_id = self.before_run.check_selected_ids(
                                                            lineEdit.text(), 
                                                            "nodes", 
                                                            single_id=True
                                                           )

        if stop:
            return True, None

        neigh_elements = app().project.preprocessor.neighboor_elements_of_node(node_id)
        if len(neigh_elements) == 1:
            return stop, node_id
        
        else:
            self.hide()
            title = "Invalid node selected"
            message = "The selected node does not correspond to the piping endings. "
            message += "It is necessary to change the selection to proceed with the "
            message += "compressor excitation attribution."
            PrintMessageInput([window_title_1, title, message])
            self.current_lineEdit.setText("")
            return True, None

    def check_all_nodes(self):

        index = self.comboBox_connection_setup.currentIndex()

        if index == 0:

            stop, node_id = self.check_node_id(self.lineEdit_suction_node_id)

            if stop:
                self.lineEdit_suction_node_id.setFocus()
                return True

            self.suction_node_id = node_id

            stop, node_id = self.check_node_id(self.lineEdit_discharge_node_id)

            if stop:
                self.lineEdit_discharge_node_id.setFocus()
                return True

            self.discharge_node_id = node_id

            if self.suction_node_id == self.discharge_node_id:
                title = "ERROR IN NODES SELECTION"
                message = "The nodes selected to the suction and discharge must differ. Try to choose another pair of nodes."
                PrintMessageInput([window_title_1, title, message])
                return True

        elif index == 1:

            stop, node_id = self.check_node_id(self.lineEdit_suction_node_id)

            if stop:
                self.lineEdit_suction_node_id.setFocus()
                return True

            self.suction_node_id = node_id

        elif index == 2:

            stop, node_id = self.check_node_id(self.lineEdit_discharge_node_id)

            if stop:
                self.lineEdit_discharge_node_id.setFocus()
                return True

            self.discharge_node_id = node_id

        return False

    def check_input_parameters(self, lineEdit: QLineEdit, label: str, _float=True):

        title = "Input error"
        value_string = lineEdit.text()

        if value_string != "":

            value_string = value_string.replace(",", ".")

            try:

                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string)

                if value < 0:
                    message = f"You cannot input a negative value to the {label}."
                    PrintMessageInput([window_title_1, title, message])
                    return True
                else:
                    self.value = value

            except Exception:
                message = f"You have typed an invalid value to the {label}."
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            message = f"None value has been typed to the {label}."
            PrintMessageInput([window_title_1, title, message])
            return True
        return False

    def check_all_parameters(self):

        self.parameters = dict()

        if self.check_input_parameters(self.lineEdit_bore_diameter, "BORE DIAMETER"):
            self.lineEdit_bore_diameter.setFocus()
            return True
        else:
            self.parameters['bore_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_stroke, "STROKE"):
            self.lineEdit_stroke.setFocus()
            return True
        else:
            self.parameters['stroke'] = self.value

        if self.check_input_parameters(self.lineEdit_connecting_rod_length, "CONNECTING ROD LENGTH"):
            self.lineEdit_connecting_rod_length.setFocus()
            return True
        else:
            self.parameters['connecting_rod_length'] = self.value

        if self.check_input_parameters(self.lineEdit_rod_diameter, "ROD DIAMETER"):
            self.lineEdit_rod_diameter.setFocus()
            return True
        else:
            self.parameters['rod_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_ratio, "PRESSURE RATIO"):
            self.lineEdit_pressure_ratio.setFocus()
            return True
        else:
            self.parameters['pressure_ratio'] = self.value
    
        if self.check_input_parameters(self.lineEdit_clearance_head_end, "CLEARANCE (HE)"):
            self.lineEdit_clearance_head_end.setFocus()
            return True
        else:
            self.parameters['clearance_HE'] = self.value
        
        if self.check_input_parameters(self.lineEdit_clearance_crank_end, "CLEARANCE (CE)"):
            self.lineEdit_clearance_crank_end.setFocus()
            return True
        else:
            self.parameters['clearance_CE'] = self.value

        self.parameters['TDC_crank_angle_1'] = self.spinBox_tdc1_crank_angle.value()

        if self.check_input_parameters(self.lineEdit_rotational_speed, "ROTATIONAL SPEED"):
            self.lineEdit_rotational_speed.setFocus()
            return True
        else:
            self.parameters['rotational_speed'] = self.value

        self.parameters['capacity'] = self.spinBox_capacity.value()

        if self.check_input_parameters(self.lineEdit_molar_mass, "MOLAR MASS"):
            self.lineEdit_molar_mass.setFocus()
            return True
        else:
            self.parameters['molar_mass'] = self.value

        if self.check_input_parameters(self.lineEdit_isentropic_exponent, "ISENTROPIC EXPONENT"):
            self.lineEdit_isentropic_exponent.setFocus()
            return True
        else:
            self.parameters['isentropic_exponent'] = self.value

        if self.check_input_parameters(self.lineEdit_pressure_at_suction, "PRESSURE AT SUCTION"):
            self.lineEdit_pressure_at_suction.setFocus()
            return True
        else:
            self.parameters['pressure_at_suction'] = self.value

        if self.comboBox_suction_pressure_units.currentIndex() == 0:
            self.parameters['pressure_unit'] = "kgf/cm²"
        elif self.comboBox_suction_pressure_units.currentIndex() == 1:
            self.parameters['pressure_unit'] = "bar"

        if self.check_input_parameters(self.lineEdit_temperature_at_suction, "TEMPERATURE AT SUCTION"):
            self.lineEdit_temperature_at_suction.setFocus()
            return True
        else:
            self.parameters['temperature_at_suction'] = self.value

        if self.comboBox_suction_temperature_units.currentIndex() == 0:
            self.parameters['temperature_unit'] = "°C"
        elif self.comboBox_suction_temperature_units.currentIndex() == 1:
            self.parameters['temperature_unit'] = "K"

        self.parameters['compression_stage'] = self.compression_stage_index
        self.parameters['number_of_cylinders'] = self.number_of_cylinders
        self.parameters['acting_label'] = self.comboBox_cylinder_acting.currentIndex()

        if self.number_of_cylinders > 1:
            self.parameters['TDC_crank_angle_2'] = self.spinBox_tdc2_crank_angle.value()
        else:
            self.parameters['TDC_crank_angle_2'] = None

        self.compressor = CompressorModel(self.parameters)
        self.compressor.number_of_cylinders = self.parameters['number_of_cylinders']

        if self.comboBox_suction_pressure_units.currentIndex() == 0:
            self.P_suction = self.parameters['pressure_at_suction']*kgf_cm2_to_Pa
        elif self.comboBox_suction_pressure_units.currentIndex() == 1:
            self.P_suction = self.parameters['pressure_at_suction']*bar_to_Pa

        if self.comboBox_suction_temperature_units.currentIndex() == 0:
            self.T_suction = self.parameters['temperature_at_suction'] + 273.15
        elif self.comboBox_suction_temperature_units.currentIndex() == 1:
            self.T_suction = self.parameters['temperature_at_suction']

        if self.parameters['TDC_crank_angle_2'] is not None:   
            self.compressor.tdc2 = self.parameters['TDC_crank_angle_2']*np.pi/180

        return False
    
    def process_aquisition_parameters(self):

        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.spinBox_max_frequency.value()

        T_rev = 60/self.parameters['rotational_speed']
        list_T = [10, 5, 2, 1, 0.5]
        list_df = [0.1, 0.2, 0.5, 1, 2]

        T_selected = list_T[self.currentIndex]
        df_selected = list_df[self.currentIndex]

        if np.remainder(T_selected, T_rev) == 0:
            T = T_selected
            df = 1/T
        else:
            i = 0
            df = 1/(T_rev)
            while df > df_selected:
                i += 1
                df = 1/(i*T_rev)
        self.N_rev = i

        final_df_label = '{} Hz'.format(round(df, 6))
        self.lineEdit_frequency_resolution.setText(final_df_label)
        self.lineEdit_number_of_revolutions.setText(str(self.N_rev))
        self.aquisition_parameters_processed = True

    def save_table_values(self, table_name: str, frequencies: np.ndarray, complex_values: np.ndarray):

        f_min = frequencies[0]
        f_max = frequencies[-1]
        f_step = frequencies[1] - frequencies[0] 

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):

            title = "Project frequency setup cannot be modified"
            message = f"The following imported table of values has a frequency setup\n"
            message += "different from the others already imported ones. The current\n"
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([window_title_1, title, message])
            return True

        self.update_analysis_setup_in_file(f_min, f_max, f_step)

        real_values = np.real(complex_values)
        imag_values = np.imag(complex_values)

        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_analysis_setup_in_file(self, f_min, f_max, f_step):

        analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()
    
        analysis_setup["f_min"] = f_min
        analysis_setup["f_max"] = f_max
        analysis_setup["f_step"] = f_step
        app().pulse_file.write_analysis_setup_in_file(analysis_setup)

    def compressor_excitation_attribution_callback(self):

        if self.check_all_nodes():
            return

        if self.check_all_parameters():
            return

        self.process_aquisition_parameters()

        index = self.comboBox_connection_setup.currentIndex()
        if index in [0, 1]:

            line_suction_node_id = app().project.model.preprocessor.get_line_from_node_id(self.suction_node_id)
            compressor_info = { "temperature_suction" : self.T_suction,
                                "pressure_suction" : self.P_suction,
                                "line_id" : line_suction_node_id[0],
                                "node_id" : self.suction_node_id,
                                "pressure_ratio" : self.parameters['pressure_ratio'],
                                "connection_type" : "suction" }

            self.hide()
            read = SetFluidInput(compressor_thermodynamic_state = compressor_info)
            if not read.complete:
                return

            else:
                if read.fluid_widget.refprop is not None:
                    if read.fluid_widget.refprop.complete:
                        self.parameters["molar_mass"] = round(read.fluid_widget.fluid_data_refprop["molar_mass"], 6)
                        self.parameters['isentropic_exponent'] = round(read.fluid_widget.fluid_data_refprop["isentropic_exponent"], 6)
                        self.parameters['fluid_properties_source'] = "refprop"
                else:
                    self.parameters['fluid_properties_source'] = "user-defined"

                self.parameters['points_per_revolution'] = self.compressor.number_points
                self.compressor.set_fluid_properties_and_update_state(self.parameters['isentropic_exponent'],
                                                                      self.parameters["molar_mass"])

                # self.T_discharge = self.compressor.T_disc

                freq, in_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'in_flow')

                table_name = f"compressor_excitation_suction_node_{self.suction_node_id}"
                
                node = app().project.model.preprocessor.nodes[self.suction_node_id]
                coords = list(np.round(node.coordinates, 5))

                data = {
                        "coords" : coords,
                        "connection_type" : "suction",
                        "table_names" : [table_name],
                        "parameters" : self.parameters
                        }

                self.remove_conflicting_excitations(self.suction_node_id)

                if self.save_table_values(table_name, freq, in_flow_rate):
                    return

                self.properties._set_nodal_property("compressor_excitation", data, self.suction_node_id)

        if index in [0, 2]:

            line_discharge_node_id = app().project.model.preprocessor.get_line_from_node_id(self.discharge_node_id)
            compressor_info = { "temperature_suction" : self.T_suction,
                                "pressure_suction" : self.P_suction,
                                "line_id" : line_discharge_node_id[0],
                                "node_id" : self.discharge_node_id,
                                "pressure_ratio" : self.parameters['pressure_ratio'],
                                "connection_type" : "discharge" }

            self.hide()
            read = SetFluidInput(compressor_thermodynamic_state = compressor_info)
            if not read.complete:
                return

            else:
                if read.fluid_widget.refprop is not None:
                    if read.fluid_widget.refprop.complete:
                        self.parameters["molar_mass"] = round(read.fluid_widget.fluid_data_refprop["molar_mass"], 6)
                        self.parameters['isentropic_exponent'] = round(read.fluid_widget.fluid_data_refprop["isentropic_exponent"], 6)
                        self.parameters['fluid_properties_source'] = "refprop"
                else:
                    self.parameters['fluid_properties_source'] = "user-defined"
    
                self.parameters['points_per_revolution'] = self.compressor.number_points
                self.compressor.set_fluid_properties_and_update_state(self.parameters['isentropic_exponent'],
                                                                      self.parameters["molar_mass"])

            freq, out_flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'out_flow') 
            
            table_name = f"compressor_excitation_discharge_node_{self.discharge_node_id}"

            node = app().project.model.preprocessor.nodes[self.discharge_node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {
                    "coords" : coords,
                    "connection_type" : "discharge",
                    "table_names" : [table_name],
                    "parameters" : self.parameters
                    }

            self.remove_conflicting_excitations(self.discharge_node_id)

            if self.save_table_values(table_name, freq, out_flow_rate):
                return

            self.properties._set_nodal_property("compressor_excitation", data, self.discharge_node_id)

        app().pulse_file.write_nodal_properties_in_file()
        app().pulse_file.write_imported_table_data_in_file()
        app().main_window.update_plots()
        self.close()

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        if table_names:
            app().pulse_file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, node_id: int):
        for label in ["acoustic_pressure", "volume_velocity", "compressor_excitation"]:
            table_names = self.properties.get_nodal_related_table_names(label, node_id)
            self.properties._remove_nodal_property(label, node_id)
            self.process_table_file_removal(table_names)

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("compressor_excitation", node_ids)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selected_id.text() == "":   
            title = "Empty node selection"
            message = "You should to select a node from the list "
            message += "to proceed with the removal."
            PrintMessageInput([window_title_2, title, message])
            return
            
        node_id = int(self.lineEdit_selected_id.text())

        self.remove_table_files_from_nodes(node_id)

        self.properties._remove_nodal_property("compressor_excitation", node_id)
        app().pulse_file.write_nodal_properties_in_file()

        self.load_compressor_excitation_info()
        app().main_window.update_plots()

    def reset_callback(self):

        self.hide()

        title = "Resetting of compressor excitations"
        message = "Would you like to remove all compressor excitations from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            node_ids = list()

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "compressor_excitation":

                    node_id = args[0]
                    node_ids.append(node_id)

            for node_id in node_ids:
                self.remove_table_files_from_nodes(node_id)

            self.properties._reset_nodal_property("compressor_excitation")
            app().pulse_file.write_nodal_properties_in_file()

            app().main_window.update_plots()
            self.close()

    def load_compressor_excitation_info(self):

        self.treeWidget_compressor_excitation.clear()

        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "compressor_excitation":
                
                node_id = args[0]
                connection_type = data["connection_type"]

                new = QTreeWidgetItem([str(node_id), connection_type])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_compressor_excitation.addTopLevelItem(new)

        self.update_tabs_visibility()

    def on_click_item(self, item):
        self.lineEdit_selected_id.setText(item.text(0))
        self.lineEdit_connection_type.setText(item.text(1))
        self.pushButton_remove.setDisabled(False)

    def update_tabs_visibility(self):
        self.lineEdit_selected_id.setText("")
        self.lineEdit_connection_type.setText("")
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_compressor.setTabVisible(3, False)
        for (property, _) in self.properties.nodal_properties.keys():
            if property == "compressor_excitation":
                self.tabWidget_compressor.setCurrentIndex(0)
                self.tabWidget_compressor.setTabVisible(3, True)
                return
        self.tabWidget_compressor.setCurrentIndex(0)

    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()
    
    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_number_of_cylinders(self):
        self.number_of_cylinders = self.spinBox_number_of_cylinders.value()
        if self.number_of_cylinders == 1:
            self.spinBox_tdc2_crank_angle.setDisabled(True)
        else:
            self.spinBox_tdc2_crank_angle.setDisabled(False)

    def comboBox_event_frequency_resolution(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def comboBox_event_stage(self):
        self.currentIndex_stage = self.comboBox_stage.currentIndex()
        list_stage_labels = ['stage_1', 'stage_2', 'stage_3'] 
        self.compression_stage_label = list_stage_labels[self.currentIndex_stage]
        self.compression_stage_index = self.currentIndex_stage + 1

    def plot_PV_diagram_head_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_head_end()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_crank_end()

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_PV_diagram_both_ends()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_pressure_vs_time()
        return

    def plot_volume_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volume_vs_time()
        return
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_suction_time()
        return

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volumetric_flow_rate_at_discharge_time()
        return
    
    def plot_rod_pressure_load_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_frequency(self.N_rev)
        return

    def plot_rod_pressure_load_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_rod_pressure_load_time()
        return
    
    def plot_piston_position_and_velocity_time(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="time")

    def plot_piston_position_and_velocity_angle(self):
        self.process_aquisition_parameters()
        self.compressor.plot_piston_position_and_velocity(domain="angle")

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_suction_frequency(self.N_rev)
        return

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        self.process_aquisition_parameters()
        self.compressor.plot_volumetric_flow_rate_at_discharge_frequency(self.N_rev)
        return

    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_head_end_pressure_vs_angle()
        return

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_head_end_volume_vs_angle()
        return

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_pressure_vs_angle()
        return

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_crank_end_volume_vs_angle()
        return

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.compressor_excitation_attribution_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)