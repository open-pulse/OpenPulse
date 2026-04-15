from enum import IntEnum

import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QHeaderView, QLineEdit, QTreeWidgetItem

from pulse import app
from pulse.interface.ui_generated.model.setup.acoustic.reciprocating_compressor_inputs_ui import ReciprocatingCompressorInputs_UI
from pulse.interface.user_input.common import update_analysis_setup_in_file
from pulse.interface.user_input.model.setup.fluid.set_fluid_input import SetFluidInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_input_simplified import SetFluidInputSimplified
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    PressureUnits,
    TemperatureUnits,
    convert_temperature_unit,
    convert_pressure_unit,
    pressure_units_labels,
    temperature_units_labels,
)
from pulse.interface.user_input.numeric_checks.validator import StrictDoubleValidator
from pulse.interface.user_input.plots.general.plot_2d_simplified import Plot2DSimplified
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.properties.fluid import Fluid
from pulse.model.reciprocating_compressor_model import CylindersActingMode, ReciprocatingCompressorModel


class TabIndex(IntEnum):
    SETUP = 0
    ADVANCED_OPTIONS = 1
    REMOVE = 2


class ConnectionType(IntEnum):
    SUCTION = 0
    DISCHARGE = 1


error_title = "Error"
warning_title = "Warning"


class ReciprocatingCompressorInputs(ReciprocatingCompressorInputs_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)
        self.properties = app().project.model.properties

        self._config_window()
        self._initialize()
        self._config_widgets()
        self._create_connections()
        self.load_compressor_excitation_info()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):
        self.selected_fluid = None
        self.complete = False
        self.keep_window_open = True
        self.aquisition_parameters_processed = False
        self.plot_2d: Plot2DSimplified = None

        self.before_run = app().project.get_pre_solution_model_checks()    

    def _config_widgets(self):

        self.default_stylesheet = self.lineEdit_selected_node_id.styleSheet()

        # disable the discharge temperature QLineEdit
        self.lineEdit_discharge_temperature.setDisabled(True)

        # configure the QTreeWidget appearance
        self.treeWidget_nodal_info.header().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for i in range(2):
            self.treeWidget_nodal_info.headerItem().setTextAlignment(i, Qt.AlignCenter)

        self._load_units_labels()
        self.configure_dynamic_validators()
        self.configure_static_validators()

    def _load_units_labels(self):
        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()
        self.comboBox_temperature_units.clear()

        # add temperature and pressure labels into unit combo boxes
        self.comboBox_pressure_units.addItems(pressure_units_labels)
        self.comboBox_temperature_units.addItems(temperature_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("kgf/cm² (a)")
        self.comboBox_temperature_units.setCurrentText("°C")

    def configure_dynamic_validators(self):

        # adjust temperature bounds (t_min -> zero absolute)
        t_min = 0
        t_max = 1e4
        if self.comboBox_temperature_units.currentIndex() == TemperatureUnits.CELSIUS:
            t_min = -273.15
        elif self.comboBox_temperature_units.currentIndex() == TemperatureUnits.FARENHEIT:
            t_min = -459.67

        # adjust pressure bounds (p_min -> perfect vacuum)      
        p_min = 0 
        p_max = 1e8

        punit_index = self.comboBox_pressure_units.currentIndex()
        if punit_index == PressureUnits.Pa_g:
            p_min = -101325

        elif punit_index == PressureUnits.kPa_g:
            p_min = -101.325

        elif punit_index == PressureUnits.bar_g:
            p_min = -1.101325
            p_max = 2e3

        elif punit_index == PressureUnits.kgf_cm2_g:
            p_min = -(9.80665*1e4)

        elif punit_index == PressureUnits.psi_g:
            p_min = -(0.45359237*9.80665) / (0.0254**2)

        elif punit_index == PressureUnits.ksi_g:
            p_min = -(0.45359237*9.80665) / (1e3 * (0.0254**2))
            p_max = 1e3

        # configure validator for pressure and temeperature inputs
        self.lineEdit_suction_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_discharge_pressure.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_suction_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))
        self.lineEdit_discharge_temperature.setValidator(StrictDoubleValidator(t_min, t_max, 6))

        press_unit = self.comboBox_pressure_units.currentText()
        self.label_suction_pressure_unit.setText(f"[{press_unit}]")
        self.label_discharge_pressure_unit.setText(f"[{press_unit}]")

        temp_unit = self.comboBox_temperature_units.currentText()
        self.label_suction_temperature_unit.setText(f"[{temp_unit}]")
        self.label_discharge_temperature_unit.setText(f"[{temp_unit}]")

        self.update_state_properties_at_discharge()

    def configure_static_validators(self):

        # configure validator for geometric parameters
        geom_validator = StrictDoubleValidator(1e-6, 1e8, 8)
        self.lineEdit_bore_diameter.setValidator(geom_validator)
        self.lineEdit_stroke.setValidator(geom_validator)
        self.lineEdit_connecting_rod_length.setValidator(geom_validator)
        self.lineEdit_rod_diameter.setValidator(geom_validator)

        # configure validator for pressure ratio and isentropic exponent
        self.lineEdit_pressure_ratio.setValidator(StrictDoubleValidator(1e-8, 10, 8))
        self.lineEdit_isentropic_exponent.setValidator(StrictDoubleValidator(1e-8, 10, 6))

    def _create_connections(self):
        #
        self.comboBox_cylinder_acting.currentIndexChanged.connect(self.update_compressing_cylinders_setup)
        self.comboBox_frequency_resolution.currentIndexChanged.connect(self.comboBox_event_frequency_resolution)
        self.comboBox_pressure_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        #
        self.lineEdit_isentropic_exponent.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_suction_pressure.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_pressure_ratio.textChanged.connect(self.update_state_properties_at_discharge)
        self.lineEdit_suction_temperature.textChanged.connect(self.update_state_properties_at_discharge)
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
        self.pushButton_process_aquisition_parameters.clicked.connect(self.process_aquisition_parameters)
        #
        self.pushButton_exit.clicked.connect(self.close)
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
        self.selection_callback()
        self.update_compressing_cylinders_setup()
        self.spinBox_event_number_of_cylinders()

    def selection_callback(self):

        selected_nodes = app().main_window.list_selected_nodes()

        if len(selected_nodes) != 1:
            return

        self.lineEdit_selected_node_id.setText(str(selected_nodes[0]))
        stop, node_id = self.check_node_id(self.lineEdit_selected_node_id)

        if stop:
            self.lineEdit_selected_node_id.setFocus()
            return True

        data = self.properties._get_property("reciprocating_compressor_excitation", node_ids=node_id)

        if isinstance(data, dict):
            self.update_compressor_inputs(data)

    def tab_event_callback(self):
        tab_config = self.tabWidget_main.currentIndex() != TabIndex.REMOVE
        self.pushButton_confirm.setEnabled(tab_config)
        self.pushButton_remove.setDisabled(True)

    def update_compressing_cylinders_setup(self):

        self.lineEdit_rod_diameter.setDisabled(False)
        self.doubleSpinBox_clearance_head_end.setDisabled(False)
        self.doubleSpinBox_clearance_crank_end.setDisabled(False)

        self.pushButton_plot_PV_diagram_head_end.setDisabled(False)
        self.pushButton_plot_PV_diagram_crank_end.setDisabled(False)
        self.pushButton_plot_pressure_head_end_angle.setDisabled(False)
        self.pushButton_plot_pressure_crank_end_angle.setDisabled(False)
        self.pushButton_plot_volume_head_end_angle.setDisabled(False)
        self.pushButton_plot_volume_crank_end_angle.setDisabled(False)

        if self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.HEAD_END:

            self.lineEdit_rod_diameter.setText("")
            self.lineEdit_rod_diameter.setDisabled(True)

            self.doubleSpinBox_clearance_crank_end.setValue(0.)
            self.doubleSpinBox_clearance_crank_end.setDisabled(True)
            if self.doubleSpinBox_clearance_head_end.value() == 0.:
                self.doubleSpinBox_clearance_head_end.setValue(15.80)

            self.pushButton_plot_PV_diagram_crank_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(False)
            self.pushButton_plot_pressure_crank_end_angle.setDisabled(True)
            self.pushButton_plot_volume_crank_end_angle.setDisabled(True)

        elif self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.CRANK_END:

            if self.lineEdit_rod_diameter.text() == "":
                self.lineEdit_rod_diameter.setText("0.135")

            self.doubleSpinBox_clearance_head_end.setValue(0.)
            self.doubleSpinBox_clearance_head_end.setDisabled(True)
            if self.doubleSpinBox_clearance_crank_end.value() == 0.:
                self.doubleSpinBox_clearance_crank_end.setValue(18.39)

            self.pushButton_plot_PV_diagram_head_end.setDisabled(True)
            self.pushButton_plot_PV_diagram_both_ends.setDisabled(False)
            self.pushButton_plot_pressure_head_end_angle.setDisabled(True)
            self.pushButton_plot_volume_head_end_angle.setDisabled(True)

        elif self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.BOTH_ENDS:

            if self.lineEdit_rod_diameter.text() == "":
                self.lineEdit_rod_diameter.setText("0.135")

            if self.doubleSpinBox_clearance_head_end.value() == 0.:
                self.doubleSpinBox_clearance_head_end.setValue(15.80)

            if self.doubleSpinBox_clearance_crank_end.text() == 0.:
                self.doubleSpinBox_clearance_crank_end.setValue(18.39)

    def get_state_properties(self):

        if self.check_all_parameters():
            return dict()

        state_properties = {
            "source" : "reciprocating_compressor",
            "connection_type" : self.comboBox_connection_type.currentText().lower(),
            "pressure_unit" : self.comboBox_pressure_units.currentText(),
            "temperature_unit" : self.comboBox_temperature_units.currentText(),
            "suction_pressure" : self.parameters.get("suction_pressure"),
            "suction_temperature" : self.parameters.get("suction_temperature"),
            "pressure_ratio" : self.parameters.get("pressure_ratio"),
            "isentropic_exponent" : self.parameters.get("isentropic_exponent"),
            "molar_mass" : self.parameters.get("molar_mass"),
            "check_ideal_gas" : True,
            }

        if self.comboBox_connection_type.currentIndex() == ConnectionType.DISCHARGE:
            T_suction = self.parameters.get("suction_temperature")
            P_suction = self.parameters.get("suction_pressure")
            p_ratio = self.parameters.get('pressure_ratio')
            k = self.parameters.get("isentropic_exponent", 1.4)

            P_discharge = p_ratio * P_suction

            # convert temperature to Kelvin scale
            temp_unit = self.comboBox_temperature_units.currentText()
            T_suction_K = convert_temperature_unit(T_suction, temp_unit, "K")

            # compute the temperature at the discharge
            T_discharge_K = T_suction_K * (p_ratio**((k-1)/k))

            # revert the temperature to its original units
            T_discharge = convert_temperature_unit(T_discharge_K, "K", temp_unit)

            state_properties.update({
                "discharge_pressure" : P_discharge,
                "discharge_temperature" : T_discharge,
            })

        return state_properties

    def get_fluid_callback(self):

        state_properties = self.get_state_properties()
        if not state_properties:
            return

        self.hide()
        self.fluid_dialog = SetFluidInputSimplified(state_properties = state_properties)
        self.fluid_dialog.fluid_widget.pushButton_attribute.setText("Select fluid")
        self.fluid_dialog.pushButton_attribute.clicked.connect(self.get_selected_fluid)
        self.fluid_dialog.exec_and_keep_window_open()
        app().main_window.set_input_widget(self)

    def get_selected_fluid(self):

        self.selected_fluid = self.fluid_dialog.get_selected_fluid()
        if not isinstance(self.selected_fluid, Fluid):
            return

        self.fluid_dialog.close()
        self.lineEdit_selected_fluid.setText(self.selected_fluid.name)
        self.lineEdit_isentropic_exponent.setText(f"{self.selected_fluid.isentropic_exponent : .6f}")
        self.lineEdit_molar_mass.setText(f"{self.selected_fluid.molar_mass : .6f}")

        if self.comboBox_connection_type.currentIndex() == ConnectionType.DISCHARGE:
            temp_unit = self.comboBox_temperature_units.currentText()
            temperature = convert_temperature_unit(self.selected_fluid.temperature, "K", temp_unit)
            self.lineEdit_discharge_temperature.setText(f"{temperature : .6f}")

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

    def update_compressor_inputs(self, data: dict):

        node_id = self.lineEdit_selected_node_id.text()
        self.lineEdit_selected_node_id.setText(node_id)

        if "connection_type" in data.keys():
            connection_type = data.get("connection_type")
            if isinstance(connection_type, str):
                self.comboBox_connection_type.setCurrentText(connection_type.capitalize())

        # compressor model parameters
        parameters = data.get("parameters")
        if not isinstance(parameters, dict):
            return

        if "bore_diameter" in parameters.keys():
            self.lineEdit_bore_diameter.setText(str(parameters["bore_diameter"]))

        if "stroke" in parameters.keys():
            self.lineEdit_stroke.setText(str(parameters["stroke"]))

        if "connecting_rod_length" in parameters.keys():
            self.lineEdit_connecting_rod_length.setText(str(parameters["connecting_rod_length"]))

        if "rod_diameter" in parameters.keys():
            self.lineEdit_rod_diameter.setText(str(parameters["rod_diameter"]))

        if "pressure_ratio" in parameters.keys():
            self.lineEdit_pressure_ratio.setText(str(parameters["pressure_ratio"]))

        if "clearance_HE" in parameters.keys():
            self.doubleSpinBox_clearance_head_end.setValue(parameters["clearance_HE"])

        if "clearance_CE" in parameters.keys():
            self.doubleSpinBox_clearance_crank_end.setValue(parameters["clearance_CE"])

        if "tdc_crank_angle_1" in parameters.keys():
            self.spinBox_tdc_crank_angle_1.setValue(parameters["tdc_crank_angle_1"])

        if "rotational_speed" in parameters.keys():
            self.doubleSpinBox_rotational_speed.setValue(parameters["rotational_speed"])

        if "capacity" in parameters.keys():
            self.spinBox_capacity.setValue(parameters["capacity"])

        if "isentropic_exponent" in parameters.keys():
            self.lineEdit_isentropic_exponent.setText(str(parameters["isentropic_exponent"]))

        if "molar_mass" in parameters.keys():
            self.lineEdit_molar_mass.setText(str(parameters["molar_mass"]))

        if "suction_pressure" in parameters.keys():
            self.lineEdit_suction_pressure.setText(str(parameters["suction_pressure"]))

        if "suction_temperature" in parameters.keys():
            self.lineEdit_suction_temperature.setText(str(parameters["suction_temperature"]))

        if "pressure_unit" in parameters.keys():
            self.comboBox_pressure_units.setCurrentText(parameters["pressure_unit"])

        if "temperature_unit" in parameters.keys():
            self.comboBox_temperature_units.setCurrentText(parameters["temperature_unit"])

        if "acting_mode" in parameters.keys():
            self.comboBox_cylinder_acting.setCurrentIndex(parameters["acting_mode"])

        if "number_of_cylinders" in parameters.keys():
            number_of_cylinders = parameters["number_of_cylinders"]
            self.spinBox_number_of_cylinders.setValue(number_of_cylinders)
            if number_of_cylinders == 2:
                if "tdc_crank_angle_2" in parameters.keys():
                    self.spinBox_tdc_crank_angle_2.setValue(parameters["tdc_crank_angle_2"])

        if "points_per_revolution" in parameters.keys():
            self.spinBox_number_of_points.setValue(int(parameters["points_per_revolution"]))

        f_min, f_max, f_step, N_rev = self.get_aquisition_parameters(parameters)
        self.lineEdit_number_of_revolutions.setText(str(N_rev))
        self.spinBox_max_frequency.setValue(int(f_max))
        self.lineEdit_frequency_resolution.setText(str(f_step))

        f_steps = [0.1, 0.2, 0.5, 1.0, 2.0]
        if f_step in f_steps:
            index = f_steps.index(f_step)
            self.comboBox_frequency_resolution.setCurrentIndex(index)

    def reset_entries(self):

        self.comboBox_cylinder_acting.setCurrentIndex(CylindersActingMode.BOTH_ENDS)
        self.comboBox_stage.setCurrentText("First stage")
        self.comboBox_pressure_units.setCurrentText("kgf/cm² (a)")
        self.comboBox_temperature_units.setCurrentText("°C")

        self.lineEdit_bore_diameter.setText("")
        self.lineEdit_stroke.setText("")
        self.lineEdit_connecting_rod_length.setText("")
        self.lineEdit_rod_diameter.setText("")
        self.lineEdit_pressure_ratio.setText("")
        self.lineEdit_suction_pressure.setText("")
        self.lineEdit_suction_temperature.setText("")
        self.lineEdit_discharge_pressure.setText("")
        self.lineEdit_discharge_temperature.setText("")
        self.lineEdit_isentropic_exponent.setText("")
        self.lineEdit_molar_mass.setText("")

        self.spinBox_number_of_cylinders.setValue(1)
        self.spinBox_tdc_crank_angle_1.setValue(0)
        self.spinBox_tdc_crank_angle_2.setValue(0)
        self.spinBox_capacity.setValue(100)
        self.doubleSpinBox_clearance_head_end.setValue(0)
        self.doubleSpinBox_clearance_crank_end.setValue(0)
        self.doubleSpinBox_rotational_speed.setValue(360.0)

    def check_node_id(self, lineEdit: QLineEdit):
        
        stop, node_id = self.before_run.check_selected_ids(
            lineEdit.text(), 
            "nodes", 
            single_id = True,
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
            message += "compressor excitation attribution."
            PrintMessageInput([error_title, title, message])
            lineEdit.setText("")
            return True, None

    def check_input_nodes(self):

        stop, node_id = self.check_node_id(self.lineEdit_selected_node_id)

        if stop:
            self.lineEdit_selected_node_id.setFocus()
            return True

        if self.comboBox_connection_type.currentIndex() == ConnectionType.SUCTION:
            self.suction_node_id = node_id
        else:
            self.discharge_node_id = node_id

        return False

    def check_all_parameters(self, check_all_entries=True):

        self.parameters = dict()

        line_edits = [
            self.lineEdit_bore_diameter,
            self.lineEdit_stroke,
            self.lineEdit_connecting_rod_length,
            self.lineEdit_rod_diameter,
            self.lineEdit_pressure_ratio,
            self.lineEdit_suction_pressure,
            self.lineEdit_suction_temperature,
        ]

        if check_all_entries:
            line_edits.extend([
                self.lineEdit_isentropic_exponent,
                self.lineEdit_molar_mass,
            ])

        for line_edit in line_edits:
            if line_edit.text() == "":
                if line_edit == self.lineEdit_rod_diameter:
                    if self.comboBox_cylinder_acting.currentIndex() == CylindersActingMode.HEAD_END:
                        continue

                line_edit.setFocus()
                line_edit.setStyleSheet("border: 2px solid red")
                return True

            else:
                _style_sheet = line_edit.styleSheet()
                if _style_sheet != self.default_stylesheet:
                    line_edit.setStyleSheet(self.default_stylesheet)

            key = line_edit.objectName().split("lineEdit_")[1]
            self.parameters[key] = float(line_edit.text())

        self.parameters['acting_mode'] = self.comboBox_cylinder_acting.currentIndex()
        self.parameters['number_of_cylinders'] = self.spinBox_number_of_cylinders.value()
        self.parameters['compression_stage'] = self.comboBox_stage.currentIndex() + 1
        self.parameters['clearance_HE'] = self.doubleSpinBox_clearance_head_end.value()
        self.parameters['clearance_CE'] = self.doubleSpinBox_clearance_crank_end.value()
        self.parameters['tdc_crank_angle_1'] = self.spinBox_tdc_crank_angle_1.value()
        self.parameters['rotational_speed'] = self.doubleSpinBox_rotational_speed.value()
        self.parameters['capacity'] = self.spinBox_capacity.value()
        self.parameters['pressure_unit'] = self.comboBox_pressure_units.currentText()
        self.parameters['temperature_unit'] = self.comboBox_temperature_units.currentText()

        if self.parameters['number_of_cylinders'] > 1:
            self.parameters['tdc_crank_angle_2'] = self.spinBox_tdc_crank_angle_2.value()
        else:
            self.parameters['tdc_crank_angle_2'] = None

        if check_all_entries:
            self.compressor = ReciprocatingCompressorModel(**self.parameters)
            self.compressor.process_remaining_fluid_properties()

        return False

    def process_aquisition_parameters(self):

        self.currentIndex = self.comboBox_frequency_resolution.currentIndex()
        if self.check_all_parameters():
            return True

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.max_frequency = self.spinBox_max_frequency.value()

        T_rev = 60 / self.parameters['rotational_speed']
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

    def save_table_values(self, table_name: str, imported_values: np.ndarray, filter_zero: bool = True):

        if filter_zero:
            mask_filter = imported_values[:, 0] > 0
            _imported_values = imported_values[mask_filter, :]
        else:
            _imported_values = imported_values

        # define the frequencies vector
        frequencies = _imported_values[:, 0]

        if app().project.model.change_analysis_frequency_setup(list(frequencies)):
            self.hide()
            title = "Project frequency setup cannot be modified"
            message = "The following imported table of values has a frequency setup "
            message += "different from the others already imported ones. The current "
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([error_title, title, message])
            return True

        update_analysis_setup_in_file(frequencies)

        # real values vector
        real_values = _imported_values[:, 1]
        
        # imaginary values vector
        imag_values = _imported_values[:, 2]

        # data to be stored
        data = np.array([frequencies, real_values, imag_values], dtype=float).T

        self.properties.add_imported_tables("acoustic", table_name, data)

        return False

    def update_state_properties_at_discharge(self):

        try:
            # fluid properties
            k_isen = float(self.lineEdit_isentropic_exponent.text())
            suction_pressure = float(self.lineEdit_suction_pressure.text())

            # pressure ratio
            pressure_ratio = float(self.lineEdit_pressure_ratio.text())

            # compute the discharge pressure
            discharge_pressure = pressure_ratio * suction_pressure

            # update the discharge pressure text
            self.lineEdit_discharge_pressure.setText(f"{discharge_pressure : .8e}")

        except:
            return

        try:
            # get the temperature unit
            temp_unit = self.comboBox_temperature_units.currentText()

            # convert the suction temperature to the Kelvin scale
            T_suction = float(self.lineEdit_suction_temperature.text())
            T_suction_K = convert_temperature_unit(T_suction, temp_unit, "K") 

            # compute the discharge temperature
            T_discharge_K = T_suction_K * (pressure_ratio**((k_isen - 1) / k_isen))

            # reverts the original units to discharge temperature
            T_discharge = convert_temperature_unit(T_discharge_K, "K", temp_unit)

            # update the discharge temperature text
            self.lineEdit_discharge_temperature.setText(f"{T_discharge : .6f}")

        except:
            return

    def attribute_callback(self):

        if self.check_input_nodes():
            return

        if self.check_all_parameters():
            return

        self.process_aquisition_parameters()

        if self.comboBox_connection_type.currentIndex() == ConnectionType.SUCTION:
            flow_label = "in_flow"
            node_id = self.suction_node_id

        else:
            flow_label = "out_flow"
            node_id = self.discharge_node_id

        connection_type = self.comboBox_connection_type.currentText().lower()
        line_id = app().project.model.preprocessor.get_line_from_node_id(node_id)

        compressor_info = {
            "source" : "reciprocating_compressor",
            "line_id" : line_id[0],
            "node_id" : node_id,
            "connection_type" : connection_type,
            "pressure_unit" : self.comboBox_pressure_units.currentText(),
            "temperature_unit" : self.comboBox_temperature_units.currentText(),
            "suction_pressure" : self.parameters.get("suction_pressure"),
            "suction_temperature" : self.parameters.get("suction_temperature"),
            "isentropic_exponent" : self.parameters.get("isentropic_exponent"),
            "pressure_ratio" : self.parameters.get("pressure_ratio"),
            "check_ideal_gas" : True,
            }
        
        if not isinstance(self.selected_fluid, Fluid):

            self.hide()
            dialog = SetFluidInput(state_properties = compressor_info)
            app().main_window.set_input_widget(self)

            if not dialog.complete:
                return

            self.selected_fluid = dialog.fluid_widget.get_selected_fluid()
            if not isinstance(self.selected_fluid, Fluid):
                return

        self.parameters["molar_mass"] = self.selected_fluid.molar_mass
        self.parameters['isentropic_exponent'] = self.selected_fluid.isentropic_exponent
        self.parameters['points_per_revolution'] = self.compressor.number_points

        self.compressor.update_fluid_properties(
            self.selected_fluid.isentropic_exponent,
            self.selected_fluid.molar_mass,
            )

        freq, flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, flow_label)

        vv_data = np.array([freq, np.real(flow_rate), np.imag(flow_rate)]).T
        table_name = f"compressor_excitation_{connection_type}_node_{node_id}"

        self.remove_properties_from_node(node_id)

        if self.save_table_values(table_name, vv_data):
            return

        node = app().project.model.preprocessor.nodes[node_id]
        coords = list(np.round(node.coordinates, 5))

        data = {
            "coords" : coords,
            "connection_type" : connection_type,
            "table_names" : [table_name],
            "parameters" : self.parameters,
            }

        self.properties._set_nodal_property("reciprocating_compressor_excitation", data, node_id)
        self.actions_to_finalize()

    def actions_to_finalize(self):
        app().project.file.write_nodal_properties_in_file()
        app().project.file.write_imported_table_data_in_file()
        app().main_window.set_selection()
        app().main_window.update_plots()
        self.load_compressor_excitation_info()

    def remove_properties_from_node(self, node_id: int):
        for label in ["acoustic_pressure", "volume_velocity", "reciprocating_compressor_excitation", "reciprocating_pump_excitation"]:
            self.properties._remove_nodal_property(label, node_id)

    def remove_callback(self):

        if self.lineEdit_selected_node_id.text() == "":
            self.hide()
            title = "Invalid selection"
            message = "You should to select an item from the list "
            message += "to proceed with the removal."
            PrintMessageInput([warning_title, title, message])
            return

        node_id = int(self.lineEdit_selected_node_id.text())

        self.properties._remove_nodal_property("reciprocating_compressor_excitation", node_id)
        self.actions_to_finalize()

    def reset_callback(self):

        self.hide()

        title = "Reseting of compressor excitations"
        message = "Would you like to remove all compressor excitations from the acoustic model?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if not read._continue:
            return

        self.properties._reset_nodal_property("reciprocating_compressor_excitation")
        self.actions_to_finalize()

    def load_compressor_excitation_info(self):

        self.treeWidget_nodal_info.clear()
        for (property, *args), data in self.properties.nodal_properties.items():
            if property != "reciprocating_compressor_excitation":
                continue

            if not isinstance(data, dict):
                continue

            node_id = args[0]
            connection_type = data.get("connection_type")

            new = QTreeWidgetItem([str(node_id), connection_type])
            for i in range(2):
                new.setTextAlignment(i, Qt.AlignCenter)

            self.treeWidget_nodal_info.addTopLevelItem(new)

        self.update_tabs_visibility()

    def on_click_item(self, item: QTreeWidgetItem):
        self.lineEdit_selected_node_id.setText(item.text(0))
        self.lineEdit_connection_type.setText(item.text(1))
        self.pushButton_remove.setEnabled(True)

    def update_tabs_visibility(self):
        self.pushButton_remove.setDisabled(True)
        for (property, *_) in self.properties.nodal_properties.keys():
            if property != "reciprocating_compressor_excitation":
                continue

            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            self.tabWidget_main.setTabVisible(TabIndex.REMOVE, True)
            return

        self.lineEdit_connection_type.setText("")
        self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
        self.tabWidget_main.setTabVisible(TabIndex.REMOVE, False)

    def spinBox_event_number_of_points(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_max_frequency(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def spinBox_event_number_of_cylinders(self):
        one_cylinder = self.spinBox_number_of_cylinders.value() == 1
        self.spinBox_tdc_crank_angle_2.setDisabled(one_cylinder)

    def comboBox_event_frequency_resolution(self):
        if self.aquisition_parameters_processed:
            self.process_aquisition_parameters()

    def plot_PV_diagram_head_end(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_HE, pressure_HE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        pressure_unit = self.compressor.pressure_unit
        if volume_HE is None:
            return

        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", pressure_unit)

        self.plot_2d = Plot2DSimplified(
            title="P-V diagram (head-end)",
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{pressure_unit}]"
        )

        self.plot_2d.set_plot_data(volume_HE, pressure_HE)
        self.plot_2d.show()

    def plot_PV_diagram_crank_end(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        
        volume_CE, pressure_CE_Pa, _ = self.compressor.process_crank_end_volumes_and_pressures()
        pressure_unit = self.compressor.pressure_unit
        if volume_CE is None:
            return

        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", pressure_unit)

        self.plot_2d = Plot2DSimplified(
            title="P-V diagram (crank-end)",
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{pressure_unit}]"
        )

        self.plot_2d.set_plot_data(volume_CE, pressure_CE)
        self.plot_2d.show()

    def plot_PV_diagram_both_ends(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_HE, pressure_HE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        volume_CE, pressure_CE_Pa, _ = self.compressor.process_crank_end_volumes_and_pressures()

        pressure_unit = self.compressor.pressure_unit

        if volume_HE is None:
            return
        
        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", pressure_unit)
        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", pressure_unit)

        self.plot_2d = Plot2DSimplified(
            title="P-V RECIPROCATING COMPRESSOR DIAGRAM",
            x_label="Volume [m³]",
            y_left_label=f"Pressure [{pressure_unit}]"
        )

        self.plot_2d.set_plot_data(volume_HE, pressure_HE, label="Head End")
        self.plot_2d.set_plot_data(volume_CE, pressure_CE, label="Crank End", line_style="--", color=(0, 0, 0))
        self.plot_2d.show()

    def plot_pressure_time(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_pressure_vs_time()

    def plot_volume_time(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N
        self.compressor.plot_volume_vs_time()
    
    def plot_volumetric_flow_rate_at_suction_time(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        flow_rate = self.compressor.process_sum_of_volumetric_flow_rate('in_flow')
        if flow_rate is None:
            return

        Trev = 60 / self.compressor.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)

        self.plot_2d = Plot2DSimplified(
        title="Volumetric flow rate at suction",
        x_label="Time [s]",
        y_left_label="Volume [m³/s]"
        )

        self.plot_2d.set_plot_data(time, flow_rate)
        self.plot_2d.show()

    def plot_volumetric_flow_rate_at_discharge_time(self):
        if self.check_all_parameters():
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        flow_rate = self.compressor.process_sum_of_volumetric_flow_rate('out_flow')
        if flow_rate is None:
            return

        Trev = 60 / self.compressor.rpm
        N = len(flow_rate)
        time = np.linspace(0, Trev, N)

        self.plot_2d = Plot2DSimplified(
            title="Volumetric flow rate at discharge",
            x_label="Time [s]",
            y_left_label="Volume [m³/s]"
        )

        self.plot_2d.set_plot_data(time, flow_rate)
        self.plot_2d.show()

    def plot_rod_pressure_load_frequency(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        _, pressure_HE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        _, pressure_CE_Pa, _ = self.compressor.process_crank_end_volumes_and_pressures()

        load_head = pressure_HE_Pa * self.compressor.area_head_end
        load_crank = -pressure_CE_Pa * self.compressor.area_crank_end

        # convert the calculate force in kN
        rod_pressure_load_time = (load_head + load_crank) / 1000

        freq, rod_pressure_load = self.compressor.process_FFT_of_(rod_pressure_load_time, self.N_rev)
        mask = freq <= self.compressor.max_frequency
        freq = freq[mask]
        rod_pressure_load = rod_pressure_load[mask]

        self.plot_2d = Plot2DSimplified(
            title="Rod pressure load",
            x_label="Frequency [Hz]",
            y_left_label="Rod pressure load [kN]"
        )

        self.plot_2d.set_plot_data(freq, rod_pressure_load, absolute_value=True)
        self.plot_2d.show()        

    def plot_rod_pressure_load_time(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return
        
        _, pressure_HE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        _, pressure_CE_Pa, _ = self.compressor.process_crank_end_volumes_and_pressures()

        load_head = pressure_HE_Pa * self.compressor.area_head_end
        load_crank = -pressure_CE_Pa * self.compressor.area_crank_end

        # convert the calculate force in kN
        rod_pressure_load_time = (load_head + load_crank) / 1000

        Trev = 60 / self.compressor.rpm
        N = len(rod_pressure_load_time)
        time = np.linspace(0, Trev, N)

        self.plot_2d = Plot2DSimplified(
            title="Rod pressure load",
            x_label="Time [s]",
            y_left_label="Rod pressure load [kN]"
        )

        self.plot_2d.set_plot_data(time, rod_pressure_load_time, absolute_value=True)
        self.plot_2d.show()
            
    def plot_piston_position_and_velocity_time(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return
    
        _, x = self.compressor.recip_x()
        v = self.compressor.recip_v()
        Trev = 60 / self.compressor.rpm
        N = len(x)

        x_data = np.linspace(0, Trev, N)

        self.plot_2d = Plot2DSimplified(
            title="Piston displacement and velocity during a complete cycle",
            x_label="Time [s]",
            y_left_label="Piston relative displacement [m]",
            y_right_label="Piston velocity [m/s]",
        )

        self.plot_2d.set_plot_data(x_data, x, label="Piston position")
        self.plot_2d.set_plot_data(x_data, v, label="Piston velocity", color=(0, 0, 0), y_label_position="right")
        self.plot_2d.show()

        self.compressor.plot_piston_position_and_velocity(domain="time")

    def plot_piston_position_and_velocity_angle(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        self.compressor.plot_piston_position_and_velocity(domain="angle")

    def plot_volumetric_flow_rate_at_suction_frequency(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        freq, flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'in_flow')
        if flow_rate is None:
            return
        
        self.plot_2d = Plot2DSimplified(
            title="Volumetric flow rate at suction",
            x_label="Frequency [Hz]",
            y_left_label="Volumetric head flow rate [m³/s]"
        )

        self.plot_2d.set_plot_data(freq, flow_rate, absolute_value=True)
        self.plot_2d.show()

    def plot_volumetric_flow_rate_at_discharge_frequency(self):
        if self.process_aquisition_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return
        
        freq, flow_rate = self.compressor.process_FFT_of_volumetric_flow_rate(self.N_rev, 'out_flow')
        if flow_rate is None:
            return
        
        self.plot_2d = Plot2DSimplified(
            title="Volumetric flow rate at discharge",
            x_label="Frequency [Hz]",
            y_left_label="Volumetric crank flow rate [m³/s]"
        )

        self.plot_2d.set_plot_data(freq, flow_rate, absolute_value=True)
        self.plot_2d.show()
        
    def plot_pressure_head_end_angle(self):
        if self.check_all_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        _, pressure_HE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        pressure_unit = self.compressor.pressure_unit

        pressure_HE = convert_pressure_unit(pressure_HE_Pa, "Pa", pressure_unit)
        
        N = len(pressure_HE)
        angle = np.linspace(0, 360, N)

        self.plot_2d = Plot2DSimplified(
            title="Head end pressure vs Angle",
            x_label="Crank angle [degree]",
            y_left_label=f"Pressure [{pressure_unit}]"
        )

        self.plot_2d.set_plot_data(angle, pressure_HE)
        self.plot_2d.show()

    def plot_volume_head_end_angle(self):
        if self.check_all_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_HE, _, _ = self.compressor.process_head_end_volumes_and_pressures()

        N = len(volume_HE)
        angle = np.linspace(0, 360, N)

        self.plot_2d = Plot2DSimplified(
            title="Head end volume vs Angle",
            x_label="Crank angle [degree]",
            y_left_label="Volume [m³]"
        )

        self.plot_2d.set_plot_data(angle, volume_HE)
        self.plot_2d.show()

    def plot_pressure_crank_end_angle(self):
        if self.check_all_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        _, pressure_CE_Pa, _ = self.compressor.process_head_end_volumes_and_pressures()
        pressure_unit = self.compressor.pressure_unit

        pressure_CE = convert_pressure_unit(pressure_CE_Pa, "Pa", pressure_unit)

        N = len(pressure_CE)
        angle = np.linspace(0, 360, N)

        self.plot_2d = Plot2DSimplified(
            title="Crank end pressure vs Angle",
            x_label="Crank angle [degree]",
            y_left_label = f"Pressure [{pressure_unit}]"
        )

        self.plot_2d.set_plot_data(angle, pressure_CE)
        self.plot_2d.show()

    def plot_volume_crank_end_angle(self):
        if self.check_all_parameters():
            self.tabWidget_main.setCurrentIndex(TabIndex.SETUP)
            return

        N = self.spinBox_number_of_points.value()
        self.compressor.number_points = N

        volume_CE, _, _ = self.compressor.process_crank_end_volumes_and_pressures()

        N = len(volume_CE)
        angle = np.linspace(0, 360, N)

        self.plot_2d = Plot2DSimplified(
            title="Crank end volume vs Angle",
            x_label="Crank angle [degree]",
            y_left_label="Volume [m³]"
        )

        self.plot_2d.set_plot_data(angle, volume_CE)
        self.plot_2d.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.attribute_callback()
        elif event.key() == Qt.Key_Enter:
            self.remove_callback()
        if event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)