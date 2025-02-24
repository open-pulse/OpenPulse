from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.user_input.model.setup.fluid.set_fluid_input import SetFluidInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from pulse.interface.user_input.model.setup.acoustic.pulsation_damper_calculator_inputs import PulsationDamperCalculatorInputs
from pulse.interface.user_input.plots.general.xy_plot import XYPlot
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from pulse.model.properties.fluid import Fluid
from pulse.model.reciprocating_pump_model import ReciprocatingPumpModel

import numpy as np

window_title_1 = "Error"
window_title_2 = "Warning"

psi_to_Pa = (0.45359237 * 9.80665) / ((0.0254)**2)
kgf_cm2_to_Pa = 9.80665e4
bar_to_Pa = 1e5

class ReciprocatingPumpInputs(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "model/setup/acoustic/reciprocating_pump_inputs.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widget()
        self.selection_callback()
        self.load_reciprocating_pump_excitation_info()

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
        self.comboBox_connection_type: QComboBox
        self.comboBox_cylinder_acting: QComboBox
        self.comboBox_fluid_data_source: QComboBox
        self.comboBox_frequency_resolution: QComboBox
        self.comboBox_pressure_units: QComboBox
        self.comboBox_temperature_units: QComboBox

        # QLabel
        self.label_molar_mass: QLabel
        self.label_molar_mass_unit: QLabel
        self.label_isentropic_exp: QLabel
        self.label_isentropic_exp_unit: QLabel
        self.label_suction_pressure_unit: QLabel
        self.label_discharge_pressure_unit: QLabel
        self.label_suction_temperature_unit: QLabel
        self.label_discharge_temperature_unit: QLabel

        # QLineEdit
        self.lineEdit_selected_node_id: QLineEdit
        self.lineEdit_frequency_resolution: QLineEdit
        self.lineEdit_number_of_revolutions: QLineEdit
        self.lineEdit_bore_diameter: QLineEdit
        self.lineEdit_stroke: QLineEdit
        self.lineEdit_connecting_rod_length: QLineEdit
        self.lineEdit_rod_diameter: QLineEdit
        self.lineEdit_clearance_head_end: QLineEdit
        self.lineEdit_clearance_crank_end: QLineEdit
        self.lineEdit_rotational_speed: QLineEdit
        self.lineEdit_bulk_modulus: QLineEdit
        self.lineEdit_selected_fluid: QLineEdit
        self.lineEdit_suction_pressure: QLineEdit
        self.lineEdit_discharge_pressure: QLineEdit
        self.lineEdit_suction_temperature: QLineEdit
        self.lineEdit_discharge_temperature: QLineEdit
        self.lineEdit_connection_type: QLineEdit
        self.lineEdit_fluctuating_volume: QLineEdit

        # QPushButton
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
        self.pushButton_process_fluctuating_volume: QPushButton
        self.pushButton_process_aquisition_parameters: QPushButton
        self.pushButton_plot_fluctuating_volume: QPushButton
        self.pushButton_pulsation_damper_calculator: QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_confirm: QPushButton
        self.pushButton_remove: QPushButton
        self.pushButton_reset: QPushButton
        self.pushButton_get_fluid: QPushButton
        self.pushButton_reset_entries: QPushButton

        # QSpinBox
        self.spinBox_number_of_points: QSpinBox
        self.spinBox_max_frequency: QSpinBox
        self.spinBox_number_of_cylinders: QSpinBox
        self.spinBox_tdc1_crank_angle: QSpinBox

        # QTabWidget
        self.tabWidget_main: QTabWidget

        # QTreeWidget
        self.treeWidget_nodal_info: QTreeWidget

    def _config_widget(self):
        self.treeWidget_nodal_info.setColumnWidth(0, 100)
        # self.treeWidget_nodal_info.setColumnWidth(1, 140)
        self.treeWidget_nodal_info.headerItem().setTextAlignment(0, Qt.AlignCenter)
        self.treeWidget_nodal_info.headerItem().setTextAlignment(1, Qt.AlignCenter)

    def _create_connections(self):
        #
        self.comboBox_pressure_units.currentIndexChanged.connect(self.pressure_unit_callback)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.temperature_unit_callback)
        self.comboBox_cylinder_acting.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_fluid_data_source.currentIndexChanged.connect(self.fluid_data_source_callback)
        #
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
        self.pushButton_plot_fluctuating_volume.clicked.connect(self.plot_integral_fluctuating_volume)
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        self.pushButton_process_fluctuating_volume.clicked.connect(self.process_fluctuating_volume)
        self.pushButton_pulsation_damper_calculator.clicked.connect(self.pulsation_damper_calculator_callback)
        #
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_confirm.clicked.connect(self.attribute_callback)
        self.pushButton_get_fluid.clicked.connect(self.get_fluid_callback)
        self.pushButton_remove.clicked.connect(self.remove_callback)
        self.pushButton_reset.clicked.connect(self.reset_callback)
        self.pushButton_reset_entries.clicked.connect(self.reset_entries)
        #
        self.spinBox_number_of_points.valueChanged.connect(self.spinBox_event_number_of_points)        
        self.spinBox_max_frequency.valueChanged.connect(self.spinBox_event_max_frequency)
        self.spinBox_number_of_cylinders.valueChanged.connect(self.spinBox_event_number_of_cylinders)
        #
        self.tabWidget_main.currentChanged.connect(self.tab_event_callback)
        self.treeWidget_nodal_info.itemClicked.connect(self.on_click_item)
        #
        app().main_window.selection_changed.connect(self.selection_callback)
        #
        self.update_compressing_cylinders_setup()
        self.spinBox_event_number_of_cylinders()
        self.fluid_data_source_callback()

    def fluid_data_source_callback(self):

        index = self.comboBox_fluid_data_source.currentIndex()

        # RefProp
        if index == 0:
            self.lineEdit_bulk_modulus.setDisabled(True)

        # User-defined
        elif index == 1:
            self.lineEdit_bulk_modulus.setEnabled(True)

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if len(selected_nodes) == 1:

            self.lineEdit_selected_node_id.setText(str(selected_nodes[0]))
            stop, node_id = self.check_node_id(self.lineEdit_selected_node_id)

            if stop:
                self.lineEdit_selected_node_id.setFocus()
                return True

            data = self.properties._get_property("reciprocating_pump_excitation", node_ids=node_id)

            if isinstance(data, dict):
                self.update_pump_inputs(data)

    def tab_event_callback(self):
        # self.lineEdit_selected_surface_id.setText("")
        # self.lineEdit_connection_type.setText("")
        self.pushButton_remove.setDisabled(True)
        return

        if self.tabWidget_compressor.currentIndex() == 2:
            self.pushButton_cancel.setDisabled(True)
            self.pushButton_confirm.setDisabled(True)
        else:
            self.pushButton_cancel.setDisabled(False)
            self.pushButton_confirm.setDisabled(False)

    def pressure_unit_callback(self):
        unit_label = self.comboBox_pressure_units.currentText()
        self.label_suction_pressure_unit.setText(f"[{unit_label}]")
        self.label_discharge_pressure_unit.setText(f"[{unit_label}]")

    def temperature_unit_callback(self):
        unit_label = self.comboBox_temperature_units.currentText().replace(" ", "")
        self.label_suction_temperature_unit.setText(f"[{unit_label}]")
        self.label_discharge_temperature_unit.setText(f"[{unit_label}]")

    def update_compressing_cylinders_setup(self):

        self.lineEdit_rod_diameter.setDisabled(False)
        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.comboBox_cylinder_acting.currentIndex() == 1:
            self.lineEdit_rod_diameter.setText("")
            self.lineEdit_rod_diameter.setDisabled(True)
            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(False)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        elif self.comboBox_cylinder_acting.currentIndex() == 2:
            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(False)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)

    def get_state_properties(self, check_all_entries: bool):

        if self.check_all_parameters(check_all_entries = check_all_entries):
            return None

        if self.comboBox_connection_type.currentIndex() == 0:
            pressure = self.P_suction
            temperature = self.T_suction
        else:
            pressure = self.P_discharge
            temperature = self.T_discharge

        state_properties = {
                            "pressure" : pressure,
                            "temperature" : temperature,
                            "check_ideal_gas" : False
                            }

        return state_properties

    def get_fluid_callback(self):

        state_properties = self.get_state_properties(False)

        if state_properties:
            self.hide()
            self.fluid_dialog = SetFluidInputSimplified(state_properties = state_properties)
            self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
            self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
            self.fluid_dialog.exec_and_keep_window_open()
            app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()

        if isinstance(self.selected_fluid, Fluid):

            self.fluid_dialog.close()
            if self.selected_fluid.name in self.fluid_dialog.fluid_widget.fluid_name_to_refprop_data.keys():
                self.comboBox_fluid_data_source.setCurrentIndex(0)

            self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
            self.lineEdit_bulk_modulus.setText(f"{self.selected_fluid.bulk_modulus : .8e}")

    def change_aquisition_parameters_controls(self, _bool):
        self.pushButton_process_aquisition_parameters.setDisabled(_bool)
        self.spinBox_max_frequency.setDisabled(_bool)
        self.spinBox_number_of_points.setDisabled(_bool)
        self.comboBox_frequency_resolution.setDisabled(_bool)

    def get_aquisition_parameters(self, parameters: dict):

        frequencies = app().project.model.frequencies
        rotational_speed = parameters["rotational_speed"]

        f_min = frequencies[0]
        f_max = frequencies[-1]
        df = frequencies[1] - frequencies[0]

        N_rev = int((1 / df) / (60 / rotational_speed))
        self.N_rev = N_rev

        return f_min, f_max, df, N_rev

    def update_pump_inputs(self, data: dict):

        node_id = self.lineEdit_selected_node_id.text()
        self.lineEdit_selected_node_id.setText(node_id)

        if "connection_type" in data.keys():
            connection_type = data["connection_type"]
            if connection_type == 'suction':
                self.comboBox_connection_type.setCurrentIndex(0)
            elif connection_type == 'discharge':
                self.comboBox_connection_type.setCurrentIndex(1)

        parameters = data["parameters"]
        if "bore_diameter" in parameters.keys():
            self.lineEdit_bore_diameter.setText(str(parameters["bore_diameter"]))

        if "stroke" in parameters.keys():
            self.lineEdit_stroke.setText(str(parameters["stroke"]))

        if "connecting_rod_length" in parameters.keys():
            self.lineEdit_connecting_rod_length.setText(str(parameters["connecting_rod_length"]))

        if "rod_diameter" in parameters.keys():
            self.lineEdit_rod_diameter.setText(str(parameters["rod_diameter"]))

        if "clearance_HE" in parameters.keys():
            self.lineEdit_clearance_head_end.setText(str(parameters["clearance_HE"]))

        if "clearance_CE" in parameters.keys():
            self.lineEdit_clearance_crank_end.setText(str(parameters["clearance_CE"]))

        if "TDC_crank_angle_1" in parameters.keys():
            self.spinBox_tdc1_crank_angle.setValue(int(parameters["TDC_crank_angle_1"]))

        if "rotational_speed" in parameters.keys():
            self.lineEdit_rotational_speed.setText(str(parameters["rotational_speed"]))

        if "bulk_modulus" in parameters.keys():
            bulk_modulus = parameters["bulk_modulus"]
            self.lineEdit_bulk_modulus.setText(f"{bulk_modulus : .8e}")

        if "pressure_at_suction" in parameters.keys():
            self.lineEdit_suction_pressure.setText(str(parameters["pressure_at_suction"]))

        if "pressure_at_discharge" in parameters.keys():
            self.lineEdit_discharge_pressure.setText(str(parameters["pressure_at_discharge"]))

        pressure_units = ["kgf/cm² (a)", "bar (a)", "kPa (a)", "Pa (a)", "kgf/cm² (g)", "bar (g)", "kPa (g)", "Pa (g)"]
        if "pressure_unit" in parameters.keys():
            for i, p_unit in enumerate(pressure_units):
                if p_unit in parameters["pressure_unit"]:
                    self.comboBox_pressure_units.setCurrentIndex(i)

        if "temperature_at_suction" in parameters.keys():
            self.lineEdit_suction_temperature.setText(str(parameters["temperature_at_suction"]))

        if "temperature_at_discharge" in parameters.keys():
            self.lineEdit_discharge_temperature.setText(str(parameters["temperature_at_discharge"]))

        temperature_units = ["°C", "K"]
        if "temperature_unit" in parameters.keys():
            for i, p_unit in enumerate(temperature_units):
                if p_unit in parameters["pressure_unit"]:
                    self.comboBox_temperature_units.setCurrentIndex(i)

        if "acting_label" in parameters.keys():
            acting_key = int(parameters["acting_label"])
            self.comboBox_cylinder_acting.setCurrentIndex(acting_key)

        if "number_of_cylinders" in parameters.keys():
            self.spinBox_number_of_cylinders.setValue(int(parameters["number_of_cylinders"]))

        if "points_per_revolution" in parameters.keys():
            self.spinBox_number_of_points.setValue(int(parameters["points_per_revolution"]))

        _, f_max, f_step, N_rev = self.get_aquisition_parameters(parameters)
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))
        self.lineEdit_frequency_resolution.setText(str(round(f_step, 6)))

        f_steps = [0.1, 0.2, 0.5, 1.0, 2.0]
        if f_step in f_steps:
            index = f_steps.index(f_step)
            self.comboBox_frequency_resolution.setCurrentIndex(index)

    def reset_entries(self):
        #
        self.comboBox_cylinder_acting.setCurrentIndex(0)
        self.comboBox_pressure_units.setCurrentIndex(0)
        self.comboBox_temperature_units.setCurrentIndex(0)
        #
        self.lineEdit_bore_diameter.setText("")
        self.lineEdit_stroke.setText("")
        self.lineEdit_connecting_rod_length.setText("")
        self.lineEdit_rod_diameter.setText("")
        self.lineEdit_clearance_head_end.setText("")
        self.lineEdit_clearance_crank_end.setText("")
        self.lineEdit_rotational_speed.setText("")
        self.lineEdit_bulk_modulus.setText("")
        self.lineEdit_suction_pressure.setText("")
        self.lineEdit_suction_temperature.setText("")
        self.lineEdit_discharge_pressure.setText("")
        self.lineEdit_discharge_temperature.setText("")
        #
        self.spinBox_number_of_cylinders.setValue(1)
        self.spinBox_tdc1_crank_angle.setValue(0)

    def check_node_id(self, lineEdit: QLineEdit):
        
        stop, node_id = self.before_run.check_selected_ids(
                                                            lineEdit.text(), 
                                                            "nodes", 
                                                            single_id=True
                                                           )

        if stop:
            return True, None

        neigh_elements = app().project.model.preprocessor.structural_elements_connected_to_node[node_id]

        if len(neigh_elements) == 1:
            return stop, node_id
        
        else:
            self.hide()
            title = "Invalid node selected"
            message = "The selected node does not correspond to the piping endings. "
            message += "It is necessary to change the selection to proceed with the "
            message += "reciprocating pump excitation attribution."
            PrintMessageInput([window_title_1, title, message])
            lineEdit.setText("")
            return True, None

    def check_input_nodes(self):

        stop, node_id = self.check_node_id(self.lineEdit_selected_node_id)

        if stop:
            self.lineEdit_selected_node_id.setFocus()
            return True

        if self.comboBox_connection_type.currentIndex() == 0:
            self.suction_node_id = node_id
        else:
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

    def check_all_parameters(self, check_all_entries=True):

        self.parameters = dict()

        if self.check_input_parameters(self.lineEdit_bore_diameter, "Bore diameter"):
            self.lineEdit_bore_diameter.setFocus()
            return True
        else:
            self.parameters['bore_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_stroke, "Stroke"):
            self.lineEdit_stroke.setFocus()
            return True
        else:
            self.parameters['stroke'] = self.value

        if self.check_input_parameters(self.lineEdit_connecting_rod_length, "Connecting rod length"):
            self.lineEdit_connecting_rod_length.setFocus()
            return True
        else:
            self.parameters['connecting_rod_length'] = self.value

        if self.comboBox_cylinder_acting.currentIndex() in [0, 2]:
            if self.check_input_parameters(self.lineEdit_rod_diameter, "Rod diameter"):
                self.lineEdit_rod_diameter.setFocus()
                return True
            else:
                self.parameters['rod_diameter'] = self.value

        if self.check_input_parameters(self.lineEdit_clearance_head_end, "Clearance (HE)"):
            self.lineEdit_clearance_head_end.setFocus()
            return True
        else:
            self.parameters['clearance_HE'] = self.value
        
        if self.check_input_parameters(self.lineEdit_clearance_crank_end, "Clearance (CE)"):
            self.lineEdit_clearance_crank_end.setFocus()
            return True
        else:
            self.parameters['clearance_CE'] = self.value

        self.parameters['TDC_crank_angle_1'] = self.spinBox_tdc1_crank_angle.value()

        if self.check_input_parameters(self.lineEdit_rotational_speed, "Rotational speed"):
            self.lineEdit_rotational_speed.setFocus()
            return True
        else:
            self.parameters['rotational_speed'] = self.value

        if check_all_entries:
            if self.check_input_parameters(self.lineEdit_bulk_modulus, "Bulk modulus"):
                self.lineEdit_bulk_modulus.setFocus()
                return True
            else:
                self.parameters['bulk_modulus'] = self.value

        if self.check_input_parameters(self.lineEdit_suction_pressure, "Suction pressure"):
            self.lineEdit_suction_pressure.setFocus()
            return True
        else:
            self.parameters['pressure_at_suction'] = self.value

        if self.check_input_parameters(self.lineEdit_discharge_pressure, "Discharge pressure"):
            self.lineEdit_discharge_pressure.setFocus()
            return True
        else:
            self.parameters['pressure_at_discharge'] = self.value

        # unit_labels = ["kgf/cm² (a)", "bar (a)", "kPa (a)", "Pa (a)", "kgf/cm² (g)", "bar (g)", "kPa (g)", "Pa (g)"]
        unit_label = self.comboBox_pressure_units.currentText()
        self.parameters['pressure_unit'] = unit_label
        if self.check_input_parameters(self.lineEdit_suction_temperature, "Temperature at suction"):
            self.lineEdit_suction_temperature.setFocus()
            return True
        else:
            self.parameters['temperature_at_suction'] = self.value

        if self.check_input_parameters(self.lineEdit_discharge_temperature, "Temperature at dischage"):
            self.lineEdit_discharge_temperature.setFocus()
            return True
        else:
            self.parameters['temperature_at_discharge'] = self.value

        tu_labels = ["°C", "K"]
        tu_index = self.comboBox_temperature_units.currentIndex()
        self.parameters['temperature_unit'] = tu_labels[tu_index]

        self.parameters['number_of_cylinders'] = self.number_of_cylinders
        self.parameters['acting_label'] = self.comboBox_cylinder_acting.currentIndex()

        if check_all_entries:
            self.pump_model = ReciprocatingPumpModel(self.parameters)

        if "kgf/cm²" in unit_label:
            self.P_suction = self.parameters['pressure_at_suction'] * kgf_cm2_to_Pa
            self.P_discharge = self.parameters['pressure_at_discharge'] * kgf_cm2_to_Pa
            
        elif "bar" in unit_label:
            self.P_suction = self.parameters['pressure_at_suction'] * bar_to_Pa
            self.P_discharge = self.parameters['pressure_at_discharge'] * bar_to_Pa

        elif "kPa" in unit_label:
            self.P_suction = self.parameters['pressure_at_suction'] * 1e3
            self.P_discharge = self.parameters['pressure_at_discharge'] * 1e3

        if "(g)" in unit_label:
            self.P_suction += 101325
            self.P_discharge += 101325

        if self.comboBox_temperature_units.currentIndex() == 0:
            self.T_suction = self.parameters['temperature_at_suction'] + 273.15
            self.T_discharge = self.parameters['temperature_at_discharge'] + 273.15

        elif self.comboBox_temperature_units.currentIndex() == 1:
            self.T_suction = self.parameters['temperature_at_suction']
            self.T_discharge = self.parameters['temperature_at_discharge']

        return False

    def process_aquisition_parameters(self):

        index = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.max_frequency = self.spinBox_max_frequency.value()

        T_rev = 60/self.parameters['rotational_speed']
        list_T = [10, 5, 2, 1, 0.5]
        list_df = [0.1, 0.2, 0.5, 1, 2]

        T_selected = list_T[index]
        df_selected = list_df[index]

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
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
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

    def attribute_callback(self):

        if self.check_input_nodes():
            return

        if self.check_all_parameters():
            return

        self.process_aquisition_parameters()

        if self.comboBox_connection_type.currentIndex() == 0:
            flow_label = "in_flow"
            connection_type = "suction"
            node_id = self.suction_node_id

        else:
            flow_label = "out_flow"
            connection_type = "discharge"
            node_id = self.discharge_node_id

        line_id = app().project.model.preprocessor.get_line_from_node_id(node_id)

        recip_pump_info = { 
                            "node_id" : node_id,
                            "line_id" : line_id[0],
                            "connection_type" : connection_type,
                            "temperature_at_suction" : self.T_suction,
                            "suction_pressure" : self.P_suction,
                            "temperature_at_discharge" : self.T_discharge,
                            "discharge_pressure" : self.P_discharge,
                            "bulk_modulus" : self.parameters.get('bulk_modulus', None),
                            "source" : "reciprocating_pump",
                            "check_ideal_gas" : False
                            }

        self.hide()
        read = SetFluidInput(state_properties = recip_pump_info)
        app().main_window.set_input_widget(self)

        if not read.complete:
            return

        else:

            if read.fluid_widget.refprop is not None:
                if read.fluid_widget.refprop.complete:
                    self.parameters["bulk_modulus"] = round(read.fluid_widget.fluid_data_refprop["adiabatic_bulk_modulus"], 6)
                    self.parameters['fluid_properties_source'] = "refprop"
            else:
                self.parameters['fluid_properties_source'] = "user-defined"

            self.parameters['points_per_revolution'] = self.pump_model.number_points
            self.pump_model.bulk_modulus = self.parameters["bulk_modulus"]

            freq, flow_rate = self.pump_model.process_FFT_of_volumetric_flow_rate(self.N_rev, flow_label)

            table_name = f"pump_excitation_{connection_type}_node_{node_id}"

            node = app().project.model.preprocessor.nodes[node_id]
            coords = list(np.round(node.coordinates, 5))

            data = {
                    "coords" : coords,
                    "connection_type" : connection_type,
                    "table_names" : [table_name],
                    "parameters" : self.parameters
                    }

            self.remove_conflicting_excitations(node_id)

            if self.save_table_values(table_name, freq, flow_rate):
                return

            self.properties._set_nodal_property("reciprocating_pump_excitation", data, node_id)
            self.actions_to_finalize()

    def actions_to_finalize(self):
        app().pulse_file.write_nodal_properties_in_file()
        app().pulse_file.write_imported_table_data_in_file()
        app().main_window.set_selection()
        app().main_window.update_plots()
        self.load_reciprocating_pump_excitation_info()
        self.pushButton_cancel.setText("Exit")

    def process_table_file_removal(self, table_names: list):
        for table_name in table_names:
            self.properties.remove_imported_tables("acoustic", table_name)
        # if table_names:
        #     app().pulse_file.write_imported_table_data_in_file()

    def remove_conflicting_excitations(self, node_id: int):
        for label in ["acoustic_pressure", "volume_velocity", "reciprocating_pump_excitation", "reciprocating_compressor_excitation"]:
            table_names = self.properties.get_nodal_related_table_names(label, node_id)
            self.properties._remove_nodal_property(label, node_id)
            self.process_table_file_removal(table_names)

    def remove_table_files_from_nodes(self, node_ids : list):
        table_names = self.properties.get_nodal_related_table_names("reciprocating_pump_excitation", node_ids)
        self.process_table_file_removal(table_names)

    def remove_callback(self):

        if self.lineEdit_selected_node_id.text() == "":   
            title = "Empty node selection"
            message = "You should to select a node from the list "
            message += "to proceed with the removal."
            PrintMessageInput([window_title_2, title, message])
            return
            
        node_id = int(self.lineEdit_selected_node_id.text())

        self.remove_table_files_from_nodes(node_id)

        self.properties._remove_nodal_property("reciprocating_pump_excitation", node_id)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Resetting of the reciprocating pump excitations"
        message = "Would you like to remove all reciprocating pump excitations from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            node_ids = list()

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "reciprocating_pump_excitation":

                    node_id = args[0]
                    node_ids.append(node_id)

            for node_id in node_ids:
                self.remove_table_files_from_nodes(node_id)

            self.properties._reset_nodal_property("reciprocating_pump_excitation")
            self.actions_to_finalize()

    def load_reciprocating_pump_excitation_info(self):

        self.treeWidget_nodal_info.clear()

        for (property, *args), data in self.properties.nodal_properties.items():
            if property == "reciprocating_pump_excitation":
                
                node_id = args[0]
                connection_type = data["connection_type"]

                new = QTreeWidgetItem([str(node_id), connection_type])
                new.setTextAlignment(0, Qt.AlignCenter)
                new.setTextAlignment(1, Qt.AlignCenter)
                self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def on_click_item(self, item):
        self.lineEdit_selected_node_id.setText(item.text(0))
        self.lineEdit_connection_type.setText(item.text(1))
        self.pushButton_remove.setDisabled(False)

    def update_tabs_visibility(self):
        self.lineEdit_selected_node_id.setText("")
        self.lineEdit_connection_type.setText("")
        self.pushButton_remove.setDisabled(True)
        self.tabWidget_main.setTabVisible(3, False)
        for (property, *_) in self.properties.nodal_properties.keys():
            if property == "reciprocating_pump_excitation":
                self.tabWidget_main.setCurrentIndex(0)
                self.tabWidget_main.setTabVisible(3, True)
                return
        self.tabWidget_main.setCurrentIndex(0)

    def pulsation_damper_calculator_callback(self):
        self.hide()
        PulsationDamperCalculatorInputs(
                                        fluctuating_volume = self.process_fluctuating_volume(),
                                        state_properties = self.get_state_properties(True)
                                        )
        app().main_window.set_input_widget(self)

    def process_fluctuating_volume(self):

        if self.check_all_parameters():
            return

        if self.comboBox_connection_type.currentIndex() == 0:
            flow_label = "in_flow"
        else:
            flow_label = "out_flow"

        self.pump_model.number_points = self.spinBox_number_of_points.value()
        fluctuating_volume, _ = self.pump_model.get_pump_fluctuating_volume(flow_label)
        str_fluctuating_volume = f"{fluctuating_volume : 0.8e}"
        self.lineEdit_fluctuating_volume.setText(str_fluctuating_volume)

        return fluctuating_volume

    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_number_of_cylinders(self):
        self.number_of_cylinders = self.spinBox_number_of_cylinders.value()

    def comboBox_event_frequency_resolution(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def initialize_xy_plotter(self):


        legends = [f'Target: {self.target*100}%', "Pressure residues", "Delta pressure residues"]



        # self.xy_plot.show()

    def plot_PV_diagram_head_end(self):

        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N

        self.pump_model.plot_PV_diagram_head_end()

        #TODO: check axes limits
        # volume_HE, pressure_HE, _ = self.pump_model.process_head_end_volumes_and_pressures()

        # if volume_HE is None:
        #     return

        # if self.pump_model.pressure_unit == "kgf/cm²":
        #     pressure_HE /= kgf_cm2_to_Pa
        # else:
        #     pressure_HE /= bar_to_Pa

        # x_label = "Volume [m³]"
        # y_label = f"Pressure [{self.pump_model.pressure_unit}]"
        # title = "P-V diagram (head end)"

        # plots_config = {
        #                 "number_of_plots" : 1,
        #                 "x_label" : x_label,
        #                 "y_label" : y_label,
        #                 "colors" : [(0,0,0), (0,0,1), (1,0,0)],
        #                 "line_styles" : ["--", "-", "-"],
        #                 "markers" : [None, "o", "o"],
        #                 "legends" : ["head end"],
        #                 "title" : title
        #                 }

        # self.xy_plot = XYPlot(plots_config, dialog=self)
        # self.xy_plot.set_plot_data(volume_HE, pressure_HE, 0, "auto")
        # self.xy_plot.show()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_PV_diagram_crank_end()

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_PV_diagram_both_ends()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_pressure_vs_time()
        return

    def plot_volume_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_volume_vs_time()
        return
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_volumetric_flow_rate_at_suction_time()
        return

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_volumetric_flow_rate_at_discharge_time()
        return
    
    def plot_rod_pressure_load_frequency(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_rod_pressure_load_frequency(self.N_rev)
        return

    def plot_rod_pressure_load_time(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_rod_pressure_load_time()
        return
    
    def plot_piston_position_and_velocity_time(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_piston_position_and_velocity(domain="time")

    def plot_piston_position_and_velocity_angle(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_piston_position_and_velocity(domain="angle")

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_volumetric_flow_rate_at_suction_frequency(self.N_rev)
        return

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        self.process_aquisition_parameters()
        self.pump_model.plot_volumetric_flow_rate_at_discharge_frequency(self.N_rev)
        return

    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_head_end_pressure_vs_angle()
        return

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_head_end_volume_vs_angle()
        return

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_crank_end_pressure_vs_angle()
        return

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            return
        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N
        self.pump_model.plot_crank_end_volume_vs_angle()
        return
    
    def plot_integral_fluctuating_volume(self):

        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.pump_model.number_points = N

        if self.comboBox_connection_type.currentIndex() == 0:
            flow_label = "in_flow"
        else:
            flow_label = "out_flow"

        self.pump_model.plot_fluctuating_volume(flow_label)

        return
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Delete:
            self.remove_callback()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)