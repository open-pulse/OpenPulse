
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidgetItem,
    QTreeWidgetItem,
)

from pulse import app
from pulse.interface.ui_generated.model.setup.fluid.set_fluid_composition_input_ui import (
    SetFluidCompositionInput_UI,
)
from pulse.interface.user_input.model.setup.fluid.load_fluid_composition_input import (
    LoadFluidCompositionInput,
)
from pulse.interface.user_input.model.setup.fluid.refprop_interface import (
    RefpropInterface,
)
from pulse.interface.user_input.numeric_checks.unit_utilities import (
    PressureUnits,
    TemperatureUnits,
    convert_pressure_unit,
    convert_temperature_unit,
    pressure_units_labels,
    temperature_units_labels,
)
from pulse.interface.user_input.numeric_checks.validators import StrictDoubleValidator
from pulse.interface.user_input.project.get_user_confirmation_input import (
    GetUserConfirmationInput,
)
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.properties.fluid import Fluid

error_title = "Error"
warning_title = "Warning"


class SetFluidCompositionInput(SetFluidCompositionInput_UI):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.state_properties = kwargs.get("state_properties", dict())
        self.fluid_to_edit = kwargs.get("fluid_to_edit")

        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._config_widgets()
        self._create_connections()

        if self.state_properties: 
            self.check_state_properties(self.state_properties)

        self.update_remainig_composition()
        if self.initialize_refprop_interface():
            return

        self.update_selected_fluid(fluid_to_edit = self.fluid_to_edit)

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.fluid_to_row = dict()
        self.fluid_to_composition = dict()
        self.remaining_molar_fraction = 1

        self.errors = dict()
        self.warnings = dict()
        self.fluid_data = dict()
        self.fluid_properties = dict()
        self.refprop_fluids_data = dict()

        self.selected_row = None
        self.cache_number_of_fluids = None

        self.complete = False
        self.check_ideal_gas = True
        self.keep_window_open = True

        self.selected_fluid = ""
        self.composition_file_path = ""

    def _config_widgets(self):
        #
        self.label_thermostate_right.setVisible(False)
        self.label_thermostate_left.setVisible(False)
        self.label_spacing.setVisible(False)
        #
        self.lineEdit_pressure_right.setVisible(False)
        self.lineEdit_temperature_right.setVisible(False)
        #
        self._load_units_labels()
        self.configure_dynamic_validators()

    def _load_units_labels(self):
        # clear data from unit combo boxes
        self.comboBox_pressure_units.clear()
        self.comboBox_temperature_units.clear()

        # add temperature and pressure labels into unit combo boxes
        self.comboBox_pressure_units.addItems(pressure_units_labels)
        self.comboBox_temperature_units.addItems(temperature_units_labels)

        # set default units
        self.comboBox_pressure_units.setCurrentText("Pa (a)")
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
        self.lineEdit_pressure_left.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_pressure_right.setValidator(StrictDoubleValidator(p_min, p_max, 6))
        self.lineEdit_temperature_left.setValidator(StrictDoubleValidator(t_min, t_max, 6))
        self.lineEdit_temperature_right.setValidator(StrictDoubleValidator(t_min, t_max, 6))

    def initialize_refprop_interface(self):
        self.refprop_interface = RefpropInterface()
        if self.refprop_interface.initialize_REFPROP():
            return True

        self.refprop = self.refprop_interface.refprop
        self.load_default_gases_info(self.refprop_interface.refprop_fluids)

        version = self.refprop_interface.get_REFPROP_version()
        self.setWindowTitle(f"OpenPulse (REFPROP v{version})")

    def _create_connections(self):
        #
        self.comboBox_pressure_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        self.comboBox_temperature_units.currentIndexChanged.connect(self.configure_dynamic_validators)
        self.comboBox_distribution_type.currentIndexChanged.connect(self.distribution_type_changed_callback)
        #
        self.spinBox_number_of_fluids.valueChanged.connect(self.number_of_fluids_changed_callback)
        #
        self.pushButton_add_gas.clicked.connect(self.add_selected_fluid_button_callback)
        self.pushButton_confirm.clicked.connect(self.get_fluid_data)
        self.pushButton_exit.clicked.connect(self.close)
        self.pushButton_load_composition.clicked.connect(self.load_fluid_composition_callback)
        self.pushButton_remove_gas.clicked.connect(self.remove_selected_gas)
        self.pushButton_reset_fluid.clicked.connect(self.reset_fluid)
        self.pushButton_fluid_configuration_mode.clicked.connect(self.fluids_configuration_mode_callback)
        #
        self.tableWidget_new_fluid.cellClicked.connect(self.cell_clicked_on_composition_table)
        self.tableWidget_new_fluid.itemChanged.connect(self.item_changed_callback)
        #
        self.treeWidget_refprop_fluids.itemClicked.connect(self.on_click_item_refprop_fluids)
        self.treeWidget_refprop_fluids.itemDoubleClicked.connect(self.on_double_click_item_refprop_fluids)
        #
        self.distribution_type_changed_callback()
        self.fluids_configuration_mode_callback()

    def distribution_type_changed_callback(self):
        distribution_type = self.comboBox_distribution_type.currentText()
        if distribution_type == "Linear":
            self.label_decay_factor.setDisabled(True)
            self.doubleSpinBox_decay_factor.setValue(0.5000)
            self.doubleSpinBox_decay_factor.setDisabled(True)

        else:
            self.label_decay_factor.setEnabled(True)
            self.doubleSpinBox_decay_factor.setValue(0.6000)
            self.doubleSpinBox_decay_factor.setEnabled(True)

    def number_of_fluids_changed_callback(self):
        self.cache_number_of_fluids = self.spinBox_number_of_fluids.value()

    def fluids_configuration_mode_callback(self):

        if self.state_properties:
            self.frame_multiple_fluids.setVisible(False)
            self.pushButton_fluid_configuration_mode.setDisabled(True)
            return

        self.spinBox_number_of_fluids.blockSignals(True)
        multiple_fluids_mode = not self.pushButton_fluid_configuration_mode.text() == "Single fluid mode"

        self.label_thermostate_left.setVisible(multiple_fluids_mode)
        self.label_thermostate_right.setVisible(multiple_fluids_mode)
        self.lineEdit_pressure_right.setVisible(multiple_fluids_mode)
        self.lineEdit_temperature_right.setVisible(multiple_fluids_mode)

        if multiple_fluids_mode:
            self.label_thermostate_left.setText("Start")
            self.label_thermostate_right.setText("End")
            self.spinBox_number_of_fluids.setMinimum(2)
            if isinstance(self.cache_number_of_fluids, int):
                self.spinBox_number_of_fluids.setValue(self.cache_number_of_fluids)

            self.frame_multiple_fluids.setVisible(True)
            self.pushButton_fluid_configuration_mode.setText("Single fluid mode")
            
            main_title = "Mulit-fluid configuration mode"
            tool_tip = "Switch to simple fluid configuration mode"

        else:
            self.spinBox_number_of_fluids.setMinimum(1)
            self.spinBox_number_of_fluids.setValue(1)
            self.frame_multiple_fluids.setVisible(False)
            self.pushButton_fluid_configuration_mode.setText("Multi-fluid mode")
            self.comboBox_distribution_type.setCurrentText("Linear")

            main_title = "Single fluid configuration mode"
            tool_tip = "Switch to multi-fluid configuration mode"

        self.label_title.setText(main_title)
        self.pushButton_fluid_configuration_mode.setToolTip(tool_tip)
        self.spinBox_number_of_fluids.blockSignals(False)

    def check_state_properties(self, state_properties: dict):

        # update the editable state of the state properties
        editable_state = state_properties.get("editable_state", False)

        self.comboBox_temperature_units.setEnabled(editable_state)
        self.comboBox_pressure_units.setEnabled(editable_state)

        self.lineEdit_pressure_left.setEnabled(editable_state)
        self.lineEdit_temperature_left.setEnabled(editable_state)
        self.lineEdit_pressure_right.setEnabled(editable_state)
        self.lineEdit_temperature_right.setEnabled(editable_state)

        self.reciprocating_machine = state_properties.get("source")
        self.check_ideal_gas = state_properties.get("check_ideal_gas", True)

        pressure_unit = state_properties.get("pressure_unit", "kgf/cm² (a)")
        temperature_unit = state_properties.get("temperature_unit", "°C")

        self.comboBox_pressure_units.setCurrentText(pressure_unit)
        self.comboBox_temperature_units.setCurrentText(temperature_unit)

        if self.reciprocating_machine is None:
            pressure = state_properties.get("pressure")
            temperature = state_properties.get("temperature")

            if isinstance(temperature, (int | float)):
                self.lineEdit_temperature_left.setText(f"{temperature : .6f}")

            if isinstance(pressure, (int | float)):
                self.lineEdit_pressure_left.setText(f"{pressure : .8e}")

        else:
            self.connection_type = state_properties['connection_type']
            T_suction = state_properties['suction_temperature']
            P_suction = state_properties['suction_pressure']

            connected_at_discharge = self.connection_type == "discharge"

            self.label_thermostate_left.setVisible(connected_at_discharge)
            self.label_thermostate_right.setVisible(connected_at_discharge)
            self.label_spacing.setVisible(connected_at_discharge)

            self.lineEdit_pressure_right.setVisible(connected_at_discharge)
            self.lineEdit_temperature_right.setVisible(connected_at_discharge)

            if 'suction_pressure' in state_properties.keys():
                self.lineEdit_temperature_left.setText(f"{T_suction : .6f}")
                self.lineEdit_pressure_left.setText(f"{P_suction : .8e}")

            if 'pressure_ratio' in state_properties.keys():
                self.p_ratio =  state_properties['pressure_ratio']
                P_discharge = self.p_ratio * P_suction

            elif 'discharge_pressure' in state_properties.keys():
                P_discharge = state_properties['discharge_pressure']

            self.lineEdit_pressure_right.setText(f"{P_discharge : .8e}")

            if 'discharge_temperature' in state_properties.keys():
                T_discharge = state_properties['discharge_temperature']
                self.lineEdit_temperature_right.setText(f"{T_discharge : .6f}")

            else:

                tool_tip = "The temperature at discharge will be "
                tool_tip += "calculated after the fluid definition."

                self.lineEdit_temperature_right.setText("---")
                self.lineEdit_temperature_right.setToolTip(tool_tip)

    def update_selected_fluid(self, fluid_to_edit: None | Fluid = None ):

        if not isinstance(fluid_to_edit, Fluid):
            return

        fluid_name = fluid_to_edit.name
        pressure = fluid_to_edit.pressure
        temperature = fluid_to_edit.temperature
        key_mixture = fluid_to_edit.key_mixture
        molar_fractions = fluid_to_edit.molar_fractions

        fluid_file_names = key_mixture.split(";")
        self.lineEdit_fluid_name.setText(fluid_name)
        self.lineEdit_pressure_left.setText(f"{pressure : .8e}")
        self.lineEdit_temperature_left.setText(f"{temperature : .6f}")

        self.comboBox_temperature_units.setCurrentIndex(TemperatureUnits.KELVIN)
        self.comboBox_pressure_units.setCurrentIndex(PressureUnits.Pa_a)

        for index, fluid_file_name in enumerate(fluid_file_names):
            final_name = self.refprop_interface.fluid_file_to_final_name[fluid_file_name]
            molar_fraction = round(100 * molar_fractions[index], 6)

            self.fluid_to_composition[final_name] = [
            str(molar_fraction), 
            molar_fractions[index], 
            fluid_file_name
            ]

        self.load_fluid_composition_info()
        self.update_remainig_composition()

    def add_selected_fluid_button_callback(self):
        self.add_selected_fluid_to_composition_table(self.selected_fluid)

    def add_selected_fluid(self, fluid_name: str, molar_fraction: float):

        fluid_file_name, _, _ = self.refprop_fluids[fluid_name]

        if isinstance(molar_fraction, float):
            self.fluid_to_composition[fluid_name] = [  
                str(molar_fraction), 
                molar_fraction / 100, 
                fluid_file_name
                ]

            if molar_fraction == 0:
                if fluid_name in self.fluid_to_composition.keys():
                    self.fluid_to_composition.pop(fluid_name)

        elif molar_fraction == "":
            self.fluid_to_composition[fluid_name] = list()

        self.update_remainig_composition()

    def update_remainig_composition(self):

        self.remaining_molar_fraction = 1
        for composition_data in self.fluid_to_composition.values():
            if len(composition_data) == 3:
                composition_value = composition_data[1]
                self.remaining_molar_fraction -= composition_value

        _remain = round(100 * self.remaining_molar_fraction, 6)
        if _remain == 0:
            _remain = 0.00

        self.remaining_composition_highlight(_remain)
        if not self.state_properties:
            return

        if self.state_properties.get("source") != "reciprocating_compressor":
            return

        if self.state_properties.get("connection_type") == "suction":
            return

        if round(abs(self.remaining_molar_fraction), 6) == 0:
            self.compute_reciprocating_compressor_state_properties()

    def remaining_composition_highlight(self, value: float):
        if value >= 0:
            style_sheet =   """  
                QLabel{border-radius: 4px; border-color: rgb(100, 100, 100); 
                    border-style: solid; border-width: 1px; color: rgb(100, 100, 100); 
                    background-color: rgb(255, 255, 255)}
                """

        else:
            style_sheet =   """  
                QLabel{border-radius: 4px; border-color: rgb(250, 10, 10); 
                    border-style: solid; border-width: 2px; color: rgb(250, 10, 10); 
                    background-color: rgb(255, 255, 255)}
                """

        self.label_remaining_composition.setStyleSheet(style_sheet)
        self.label_remaining_composition.setText(str(value))

    def update_discharge_temperature_line_edit(self, T_discharge_K: float):
        temp_unit = self.comboBox_temperature_units.currentText()
        T_disch = convert_temperature_unit(T_discharge_K, "K", temp_unit)
        self.lineEdit_temperature_right.setText(f"{T_disch : .6f}")

    def compute_reciprocating_compressor_state_properties(self):

        composition_data = self.get_fluid_composition_data()
        if composition_data is None:
            return
        else:
            key_mixture, molar_fractions = composition_data

        values = self.get_temperature_and_pressure_SI_units()
        if values is None:
            return

        [T_suction_K, P_suction_Pa] = values

        k_suction, errors, warnings = self.refprop_interface.get_specific_fluid_property( 
            key_mixture = key_mixture,
            molar_fractions = molar_fractions,
            property_key = self.refprop_interface.isentropic_label,
            temperature_K = T_suction_K,
            pressure_Pa = P_suction_Pa,
            )

        if errors:
            return

        # evaluate the temperature at the discharge
        T_discharge_K = T_suction_K * (self.p_ratio**((k_suction - 1) / k_suction))

        # update the discharge temperature QLineEdit
        self.update_discharge_temperature_line_edit(T_discharge_K)

    def remove_selected_gas(self):

        if isinstance(self.selected_row, int):

            item = self.tableWidget_new_fluid.item(self.selected_row, 0)

            if item is None:
                return

            selected_fluid = item.text()
            self.tableWidget_new_fluid.removeRow(self.selected_row)

            if selected_fluid in self.fluid_to_composition.keys():
                self.fluid_to_composition.pop(selected_fluid)
                self.update_remainig_composition()

    def reset_fluid(self):

        self.hide()

        title = "Fluid composition reset"
        message = "Would you like to reset the current fluid composition?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        self.fluid_to_composition.clear()
        self.load_fluid_composition_info()
        self.update_remainig_composition()

    def load_default_gases_info(self, refprop_fluids: dict):

        self.config_table_data()
        self.refprop_fluids = refprop_fluids
        self.treeWidget_refprop_fluids.clear()
        self.treeWidget_refprop_fluids.headerItem().setText(0, "Default fluid library")

        for fluid in self.refprop_fluids.keys():
            new = QTreeWidgetItem([fluid])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_refprop_fluids.addTopLevelItem(new)

    def config_table_data(self):

        header = ['Fluid name', 'Molar fraction [%]']
        
        self.tableWidget_new_fluid.setColumnCount(len(header))
        self.tableWidget_new_fluid.setHorizontalHeaderLabels(header)
        self.tableWidget_new_fluid.setSelectionBehavior(QAbstractItemView.SelectionBehavior(1))
        self.tableWidget_new_fluid.resizeColumnsToContents()

        self.tableWidget_new_fluid.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode(0))
        self.tableWidget_new_fluid.horizontalHeader().setStretchLastSection(True)

        for j, width in enumerate([220, 120]):
            self.tableWidget_new_fluid.horizontalHeader().resizeSection(j, width)
            self.tableWidget_new_fluid.horizontalHeaderItem(j).setTextAlignment(Qt.AlignCenter)

    def load_fluid_composition_info(self):

        self.tableWidget_new_fluid.blockSignals(True)
        self.tableWidget_new_fluid.clearContents()
        self.tableWidget_new_fluid.setRowCount(len(self.fluid_to_composition))
        self.tableWidget_new_fluid.setColumnCount(2)

        for row, (fluid, composition_data) in enumerate(self.fluid_to_composition.items()):

            self.tableWidget_new_fluid.setItem(row, 0, QTableWidgetItem(fluid))
            self.tableWidget_new_fluid.item(row, 0).setTextAlignment(Qt.AlignCenter)

            if len(composition_data) == 3:
                molar_fraction = round(100*composition_data[1], 7)
                self.add_molar_fraction_to_cell(row, molar_fraction = str(molar_fraction))

        self.label_selected_fluid.clear()
        self.tableWidget_new_fluid.blockSignals(False)

    def check_composition_input(self, fluid_name, composition):

        if isinstance(composition, float):

            fluid_file_name, _, _ = self.refprop_fluids[fluid_name]
            self.fluid_to_composition[fluid_name] = [  
                str(composition), 
                composition / 100, 
                fluid_file_name,
                ]

            if composition == 0:
                if fluid_name in self.fluid_to_composition.keys():
                    self.fluid_to_composition.pop(fluid_name)

            return False

    def on_click_item_refprop_fluids(self, item):
        self.selected_item = item
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(self.selected_fluid)

    def on_double_click_item_refprop_fluids(self, item):
        self.on_click_item_refprop_fluids(item)
        self.add_selected_fluid_to_composition_table(item.text(0))

    def add_selected_fluid_to_composition_table(self, selected_fluid):

        self.tableWidget_new_fluid.blockSignals(True)

        if selected_fluid == "":
            self.tableWidget_new_fluid.blockSignals(False)
            return

        if selected_fluid in self.fluid_to_composition.keys():
            self.tableWidget_new_fluid.blockSignals(False)
            return
        else:
            rows = self.tableWidget_new_fluid.rowCount()
            self.fluid_to_row[selected_fluid] = rows
            self.fluid_to_composition[selected_fluid] = list()

        self.tableWidget_new_fluid.setColumnCount(2)
        self.tableWidget_new_fluid.insertRow(rows)

        new_item = QTableWidgetItem(selected_fluid)
        new_item.setTextAlignment(Qt.AlignCenter)
        new_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tableWidget_new_fluid.setItem(rows, 0, new_item)

        if self.add_molar_fraction_to_cell(rows):
            self.tableWidget_new_fluid.blockSignals(False)
            return

        molar_fraction = self.tableWidget_new_fluid.item(rows, 1).text()
        self.add_selected_fluid(self.selected_fluid, float(molar_fraction))

        self.tableWidget_new_fluid.blockSignals(False)

    def add_molar_fraction_to_cell(self, row, molar_fraction: str | None = None):

        if molar_fraction is None:
            self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem())
            self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)
            return True

        try:

            molar_fraction = molar_fraction.replace(",", ".")
            self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem(molar_fraction))
            self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)

        except Exception:
            return True

    def check_remaining_molar_fraction(self):

        message = ""
        if round(self.remaining_molar_fraction, 6):
            self.hide()
            remaining_molar_fraction = round(100*self.remaining_molar_fraction, 6)
            title = "Fluid composition not invalid"
            message += "The sum of all molar fractions must be equal to the unity. It is recommended "
            message += "to adjust the fluid composition until this requirement is met.\n\n"
            message += f"Remaining molar fraction: {remaining_molar_fraction} %"
            PrintMessageInput([error_title, title, message])
            return True
        
        return False
        
    def check_fluid_name(self):

        if self.lineEdit_fluid_name.text() == "":
            self.hide()
            title = "Additional input required"
            message = "Define a fluid name at specific input field to proceed."
            self.lineEdit_fluid_name.setFocus()
            PrintMessageInput([error_title, title, message])
            return True
        
        return False

    def get_fluid_composition_data(self):
        key_mixture = ""
        molar_fractions = list()
        for composition_data in self.fluid_to_composition.values():
            if len(composition_data) != 3:
                continue

            _, _fraction, file_name = composition_data
            key_mixture += file_name + ";"
            molar_fractions.append(_fraction)

        if key_mixture == "":
            return None

        key_mixture = key_mixture[:-1]

        return (key_mixture, molar_fractions)

    def process_fluid_data_for_general_purposes(self, **kwargs):

        self.ideal_gas_warning = False
        self.compressibility_factor = -1

        key_mixture = kwargs.get("key_mixture", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        temperature_K = kwargs.get("temperature_K")
        pressure_Pa = kwargs.get("pressure_Pa")

        for key_prop, prop_label in self.refprop_interface.map_properties.items():
            if key_prop in ["PRANDTL", "TD", "KV"]:
                continue 

            fluid_property, errors, warnings = self.refprop_interface.get_specific_fluid_property(
                key_mixture = key_mixture,
                molar_fractions = molar_fractions,
                property_key = key_prop,
                temperature_K = temperature_K,
                pressure_Pa = pressure_Pa,
                )

            if errors:
                self.errors[prop_label] = errors
            
            if warnings:
                self.warnings[prop_label] = warnings

            if key_prop == "Z":
                Z = fluid_property
                if Z < 0.9 or Z > 1.1:
                    self.ideal_gas_warning = True
                    self.compressibility_factor = Z

            self.fluid_properties[prop_label] = fluid_property

    def process_fluid_data_for_reciprocating_compressors(self, **kwargs):

        self.ideal_gas_warning = False
        self.compressibility_factor = -1

        key_mixture = kwargs.get("key_mixture", "")
        molar_fractions = kwargs.get("molar_fractions", list())
        T_suction_K = kwargs.get("temperature_K")
        P_suction_Pa = kwargs.get("pressure_Pa")

        for key_prop, prop_label in self.refprop_interface.map_properties.items():
            if key_prop in ["PRANDTL", "TD", "KV"]:
                continue

            fluid_property, errors, warnings = self.refprop_interface.get_specific_fluid_property(
                key_mixture = key_mixture,
                molar_fractions = molar_fractions,
                property_key = key_prop,
                temperature_K = T_suction_K,
                pressure_Pa = P_suction_Pa,
                )

            if errors:
                self.errors[prop_label] = errors
            
            if warnings:
                self.warnings[prop_label] = warnings

            self.fluid_properties[prop_label] = fluid_property
            if key_prop != "M":
                if key_prop == self.refprop_interface.isentropic_label:
                    self.k = fluid_property

        # evaluate the temperature at the discharge
        T_discharge_K = T_suction_K * (self.p_ratio**((self.k - 1) / self.k))

        # update the discharge temperature QLineEdit
        self.update_discharge_temperature_line_edit(T_discharge_K)

        if self.connection_type == "suction":
            self.fluid_properties["temperature"] = T_suction_K
            self.fluid_properties["pressure"] = P_suction_Pa
            return

        # It is well known that the isentropic exponent depends on the temperature, 
        # k = k(T), meaning there is a non-linear relationship to be resolved. 
        # Therefore, the temperature T_disch of the first iteration is computed using 
        # the isentropic exponent evaluated for the suction thermodynamic state. 
        # The newly computed temperature T_disch is used to update the isentropic
        # exponent, and a new temperature is computed within a while loop until 
        # the predefined criterion is satisfied.

        P_disch_Pa = self.p_ratio * P_suction_Pa
        temp_cache = [T_discharge_K]

        count = 0
        max_iter = 100
        criteria = 1e4

        while criteria > 0.001 and count <= max_iter:

            for key_prop, prop_label in self.refprop_interface.map_properties.items():
                if key_prop in ["PRANDTL", "TD", "KV"]:
                    continue    

                fluid_property, errors, warnings = self.refprop_interface.get_specific_fluid_property(
                    key_mixture = key_mixture,
                    molar_fractions = molar_fractions,
                    property_key = key_prop,
                    temperature_K = T_discharge_K,
                    pressure_Pa = P_disch_Pa,
                    )

                if errors:
                    self.errors[prop_label] = errors

                if warnings:
                    self.warnings[prop_label] = warnings

                self.fluid_properties[prop_label] = fluid_property  
                if key_prop == self.refprop_interface.isentropic_label:
                    k_iter = fluid_property

                if key_prop == "Z":
                    Z = fluid_property
                    if Z < 0.9 or Z > 1.1:
                        self.ideal_gas_warning = True
                        self.compressibility_factor = Z

            count += 1
            T_discharge_K = T_suction_K * (self.p_ratio**((k_iter-1)/k_iter))

            # cache computed temperature discharge value
            temp_cache.append(T_discharge_K)

            num = abs(temp_cache[-1] - temp_cache[-2])
            den = (temp_cache[-1] + temp_cache[-2]) / 2
            criteria = num / den

            self.fluid_properties["temperature"] = T_discharge_K
            # print(count, k_iter, cache_temperatures[-1], cache_temperatures[-2], criteria)

        self.fluid_properties["pressure"] = P_disch_Pa

        # update the discharge temperature QLineEdit
        self.update_discharge_temperature_line_edit(T_discharge_K)

    def get_fluid_data(self):

        self.fluid_data.clear()
        self.refprop_fluids_data.clear()

        if self.check_fluid_name():
            return
        
        fluid_name = self.lineEdit_fluid_name.text()
        if self.check_remaining_molar_fraction():
            return

        composition_data = self.get_fluid_composition_data()
        if composition_data is None:
            return
        else:
            key_mixture, molar_fractions = composition_data

        if self.spinBox_number_of_fluids.value() == 1:

            self.fluid_properties.clear()
            self.fluid_properties["name"] = fluid_name

            values = self.get_temperature_and_pressure_SI_units()
            if values is None:
                return

            [temperature_K, pressure_Pa] = values
            self.fluid_properties["temperature"] = temperature_K
            self.fluid_properties["pressure"] = pressure_Pa

            if self.state_properties.get("source") == "reciprocating_compressor":
                self.process_fluid_data_for_reciprocating_compressors(
                    key_mixture = key_mixture,
                    molar_fractions = molar_fractions,
                    temperature_K = temperature_K,
                    pressure_Pa = pressure_Pa,
                    )

            else:
                self.process_fluid_data_for_general_purposes(
                    key_mixture = key_mixture,
                    molar_fractions = molar_fractions,
                    temperature_K = temperature_K,
                    pressure_Pa = pressure_Pa,
                    )

            self.fluid_properties["key_mixture"] = key_mixture
            self.fluid_properties["molar_fractions"] = molar_fractions

            if isinstance(self.fluid_to_edit, Fluid):
                self.fluid_properties["identifier"] = self.fluid_to_edit.identifier
                self.fluid_properties["color"] = self.fluid_to_edit.color

            self.refprop_fluids_data["thermodynamic_states"] = "single_state"
            self.refprop_fluids_data["properties"] = self.fluid_properties

        else:

            distribution_type = self.comboBox_distribution_type.currentText().lower().replace(" ", "_")
            decay_factor = self.doubleSpinBox_decay_factor.value()
            number_of_fluids = self.spinBox_number_of_fluids.value()
            color_scale = self.comboBox_color_scale.currentText().lower()

            values = self.get_temperature_and_pressure_SI_units(thermostate_side="left")
            if values is None:
                return

            [T_start, P_start] = values
            
            values = self.get_temperature_and_pressure_SI_units(thermostate_side="right")
            if values is None:
                return

            [T_end, P_end] = values

            if round(T_start - T_end, 6) == 0 and round(P_start - P_end, 6) == 0:
                self.hide()
                title = "Invalid thermodynamic states"
                message = "The initial and final thermodynamic states are identical. "
                message += "You must to specify different states to obtain valid"
                message += "property distribuitions."
                PrintMessageInput([error_title, title, message])
                app().main_window.set_input_widget(self)
                return

            state_properties = self.refprop_interface.get_state_properties(
                temperatures_K = [T_start, T_end],
                pressures_Pa = [P_start, P_end],
                number_of_fluids = number_of_fluids,
                distribution_type = distribution_type,
                decay_factor = decay_factor,
                color_scale = color_scale,
                )

            multistage_fluid_properties = self.refprop_interface.compute_fluid_properties_for_multiple_state_properties(
                fluid_name = fluid_name,
                key_mixture = key_mixture,
                molar_fractions = molar_fractions,
                state_properties = state_properties,
                )

            if multistage_fluid_properties is None:
                return

            for _fluid_properties in multistage_fluid_properties.values():
                Z = _fluid_properties.get("compressibility_factor")
                if Z < 0.9 or Z > 1.1:
                    self.compressibility_factor = Z
                    self.ideal_gas_warning = True
                    break

            self.refprop_fluids_data["thermodynamic_states"] = "multiple_states"
            self.refprop_fluids_data["properties"] = multistage_fluid_properties

        self.process_refprop_warning_and_errors()

        if self.ideal_gas_check():
            return

        self.complete = True
        self.close()

    def ideal_gas_check(self):
        if self.ideal_gas_warning and self.check_ideal_gas:

            self.hide()

            Z = self.compressibility_factor
            title = "Deviation from ideal gas behavior"
            message = f"The gas compressibility factor Z = {round(Z, 6)} exceeds the internal criteria of +/- 10% "
            message += "for ideal gases. The real gases could be treated as ideal if the compressibility "
            message += " factor tends to the unit."

            message += "\n\nPress Yes to ignore this warning and get fluid properties or No to cancel."

            buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
            read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

            if app().main_window.force_close:
                self.close()
                return True

            if read._cancel:
                self.complete = False                        
                app().main_window.set_input_widget(self)
                return True

    def get_temperature_and_pressure_SI_units(self, thermostate_side: str="left"):

        # overwrite the thermostate_side if there's a reciprocating pump connected at the discharge
        if self.state_properties.get("source") == "reciprocating_pump":
            if self.state_properties.get("connection_type") == "discharge":
                thermostate_side = "right"

        if thermostate_side == "left":
            str_temperature = self.lineEdit_temperature_left.text()
            str_pressure = self.lineEdit_pressure_left.text()
        else:
            str_temperature = self.lineEdit_temperature_right.text()
            str_pressure = self.lineEdit_pressure_right.text()

        if not str_temperature.isnumeric():
            return None

        if not str_pressure.isnumeric():
            return None
        
        input_temperature = float(str_temperature)
        input_pressure = float(str_pressure)
       
        temp_unit = self.comboBox_temperature_units.currentText()
        temperature_K = convert_temperature_unit(input_temperature, temp_unit,  "K")

        press_unit = self.comboBox_pressure_units.currentText()
        pressure_Pa = convert_pressure_unit(input_pressure, press_unit,  "Pa")

        if temperature_K < 0:
            title = "Invalid entry to the temperature"
            message = "The typed value at temperature input field reaches a negative value in Kelvin scale."
            message += "It is necessary to enter a value that maintains the physical coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([error_title, title, message])
            return None

        if pressure_Pa < 0:
            title = "Invalid entry to the pressure"
            message = "The typed value at pressure input field reaches a negative value in Pascal scale. "
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([error_title, title, message])
            return None

        return [round(temperature_K, 8), round(pressure_Pa, 8)]

    def process_refprop_warning_and_errors(self):
        if not (self.errors or self.warnings):
            return

        self.hide()
        further_details = ""

        if self.errors:
            for key, _error in self.errors.items():
                further_details += f"{str(key)}: {str(_error)}\n\n"
            
            title = "Error generated while processing fluid properties"
            message = "The following errors were found in while processing the fluid properties.\n\n"
            message += further_details
            message += "It is recommended to check the fluid composition and state properties to proceed."
            PrintMessageInput([error_title, title, message])

        else:
            for key, _warning in self.warnings.items():
                further_details += f"{str(key)}: {str(_warning)}\n\n"

            title = "Warning generated while processing fluid properties"
            message = "The following warnings were generated while processing the fluid properties.\n\n"
            message += further_details
            message += "It is recommended to check the fluid properties related to the warnings."
            message += "\n\nThis warning is shown only once."
            PrintMessageInput([warning_title, title, message])

    def actions_to_finalize(self):
        if not self.state_properties:
            return

        if self.state_properties["connection type"] == 1:
            title = "Fluid properties convergence"
            message = "The following fluid properties were obtained after completing the iterative updating process:"
            message += f"\n\nTemperature (discharge) = {round(self.fluid_data['temperature'], 4)} [K]"
            message += f"\nIsentropic exponent = {round(self.fluid_data['isentropic_exponent'], 6)} [-]"
            message += "\n\nReference fluid properties:"
            message += f"\n\nTemperature (suction) = {self.state_properties['temperature (suction)']} [K]"
            message += f"\nPressure (suction) = {self.state_properties['pressure (suction)']} [Pa]"
            message += f"\nPressure (discharge) = {round(self.state_properties['pressure (discharge)'], 4)} [Pa]"
            message += f"\nMolar mass = {round(self.fluid_data['molar_mass'],6)} [kg/mol]"   
            PrintMessageInput([warning_title, title, message])

    def cell_clicked_on_composition_table(self, row, col):
        self.selected_row = row

    def item_changed_callback(self, item):

        self.tableWidget_new_fluid.blockSignals(True)

        if item.column() == 0:
            row = item.row()
            selected_fluid = item.text()

            if selected_fluid in self.refprop_fluids.keys():
                if selected_fluid in self.fluid_to_composition.keys():
                    self.tableWidget_new_fluid.removeRow(row)
                    self.tableWidget_new_fluid.blockSignals(False)
                    return

                fluid_to_row = self.fluid_to_row.copy()
                for key, value in fluid_to_row.items():
                    if row == value:
                        if key != selected_fluid:

                            self.fluid_to_row.pop(key)
                            if key in self.fluid_to_composition.keys():
                                self.fluid_to_composition.pop(key)
                            
                            self.tableWidget_new_fluid.removeRow(row)
                            self.update_remainig_composition()
                            self.tableWidget_new_fluid.blockSignals(False)
                            return

            else:

                if self.selected_fluid in self.refprop_fluids.keys():
                    if self.selected_fluid in self.fluid_to_composition.keys():
                        self.fluid_to_composition.pop(self.selected_fluid)
                        self.update_remainig_composition()

                self.tableWidget_new_fluid.removeRow(row)
                self.tableWidget_new_fluid.blockSignals(False)
                return

            self.fluid_to_row[selected_fluid] = row
            if self.add_molar_fraction_to_cell(row):
                self.tableWidget_new_fluid.blockSignals(False)
                return

            molar_fraction = self.tableWidget_new_fluid.item(item.row(), 1).text()
            if molar_fraction != "":
                molar_fraction = float(molar_fraction)

            self.add_selected_fluid(selected_fluid, molar_fraction)

        else:

            if self.item_is_invalid_number(item):
                self.tableWidget_new_fluid.blockSignals(False)
                return
 
            self.go_to_next_cell(item)
            selected_fluid = self.tableWidget_new_fluid.item(item.row(), 0).text()
            molar_fraction = self.tableWidget_new_fluid.item(item.row(), 1).text()

            if molar_fraction != "":
                molar_fraction = float(molar_fraction)

            self.add_selected_fluid(selected_fluid, molar_fraction)

        self.tableWidget_new_fluid.blockSignals(False)

    def go_to_next_cell(self, item):
        
        row = item.row()
        column = item.column()
        if column == 0:
            return

        if row <= self.tableWidget_new_fluid.rowCount() - 1:
            next_item = self.tableWidget_new_fluid.item(row + 1, column)
            if next_item is None:
                return
            
            if next_item.text() == "":
                self.tableWidget_new_fluid.setCurrentItem(next_item)
                self.tableWidget_new_fluid.editItem(next_item)

    def item_is_invalid_number(self, item):

        if item is None:
            return True
        
        if item.text() == "":
            return False

        if item.column() == 0:
            return True
        
        str_value = item.text().replace(",", ".")
        item.setText(str_value)

        try:
            value = float(str_value)

        except Exception as error_log:
            window_title = "Error"
            title = "Invalid real number"
            message = "The value typed for molar composition must be a non-zero positive number.\n\n"
            message += f"Details: {error_log}"
            PrintMessageInput([window_title, title, message])
            item.clear()
            return True
        
        message = ""

        if value > 100 or value < 0:
            message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
            message += "The value should be a positive value less or equals to 100."

        if message != "":
            self.hide()
            window_title = "Error"
            title = "Invalid molar fraction"
            PrintMessageInput([window_title, title, message])
            item.clear()
            return True
        
        return False

    def load_fluid_composition_callback(self):

        self.hide()
        self.label_selected_fluid.clear()

        self.fluid_data = dict()
        self.fluid_to_composition = dict()

        read = LoadFluidCompositionInput(file_path = self.composition_file_path)

        if read.complete:

            self.composition_file_path = read.file_path
            composition_data = read.fluid_composition_data

            comp = 0
            for (i, label, refprop_fluid_name, molar_fraction) in composition_data:

                self.fluid_data[i] = [label, refprop_fluid_name, molar_fraction]

                if refprop_fluid_name not in self.refprop_fluids.keys():
                    pass

                if refprop_fluid_name in self.refprop_fluids.keys():
                    if molar_fraction:

                        [fluid_file, _, _] = self.refprop_fluids[refprop_fluid_name]
                        self.fluid_to_composition[refprop_fluid_name] = [str(molar_fraction), molar_fraction, fluid_file]
                        comp += molar_fraction

            self.load_fluid_composition_info()
            self.update_remainig_composition()

        app().main_window.set_input_widget(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.get_fluid_data()
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.remove_selected_gas()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False