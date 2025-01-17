from PySide6.QtWidgets import QDialog, QComboBox, QFileDialog, QLabel, QLineEdit, QPushButton, QTableWidget, QTabWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.auxiliar.file_dialog import FileDialog
from pulse.interface.user_input.model.setup.fluid.load_fluid_composition_input import LoadFluidCompositionInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.utils.common_utils import get_new_path

from molde import load_ui

import os
from pathlib import Path

window_title_1 = "Error"
window_title_2 = "Warning"

class SetFluidCompositionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/fluid/set_fluid_composition_input.ui"
        load_ui(ui_path, self)

        self.state_properties = kwargs.get("state_properties", dict())
        self.selected_fluid_to_edit = kwargs.get("selected_fluid_to_edit", None)

        self.project = app().project
        app().main_window.set_input_widget(self)

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        if self.state_properties:
            self.check_state_properties(self.state_properties)

        self.update_remainig_composition()
        if self.default_library_gases():
            return

        self.load_default_gases_info()
        self.update_selected_fluid()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.selected_row = None
        self.reciprocating_machine = None

        self.keep_window_open = True
        self.check_ideal_gas = True
        self.temp_file_path = ""

        # self.isentropic_label = "ISENK"   # isentropic exponent (real gas)
        self.isentropic_label = "CP/CV"     # isentropic expansion coefficient (ideal gas)

        self.map_properties = { 
                                "D" : "density",
                                "CP" : "specific_heat_Cp",
                                "CV" : "specific_heat_Cv",
                                self.isentropic_label : "isentropic_exponent",
                                "W" : "speed_of_sound",
                                "VIS" : "dynamic_viscosity",
                                "TCX" : "thermal_conductivity",
                                "PRANDTL" : "Prandtl_number",
                                "TD" : "thermal_diffusivity",
                                "KV" : "kinematic_viscosity",
                                "M" : "molar_mass",
                                "BS" : "adiabatic_bulk_modulus",
                                "KKT" : "isothermal_bulk_modulus",
                                "Z" : "compressibility_factor",
                                "ANC-TP" : "vapor_pressure",
                                "QMASS" : "quality_mass",
                                "QMOLE" : "quality_mole",
                               }

        self.selected_fluid = ""
        self.unit_temperature = "K"
        self.unit_pressure = "Pa"

        self.complete = False
        self.remaining_molar_fraction = 1
        self.fluid_to_composition = dict()
        self.fluid_to_row = dict()

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_temperature_units : QComboBox
        self.comboBox_pressure_units : QComboBox

        # QLabel
        self.label_selected_fluid : QLabel
        self.label_title_remaining_fraction : QLabel
        self.label_remaining_composition : QLabel
        self.label_discharge : QLabel
        self.label_suction : QLabel
        self.label_spacing : QLabel

        # QLineEdit
        self.lineEdit_fluid_name : QLineEdit
        self.lineEdit_temperature : QLineEdit
        self.lineEdit_pressure : QLineEdit
        self.lineEdit_pressure_disch : QLineEdit
        self.lineEdit_temperature_disch : QLineEdit
        self.lineEdit_temperature_test : QLineEdit
        self.lineEdit_pressure_test : QLineEdit

        # QPushButton
        self.pushButton_add_gas : QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_get_fluid_properties_info : QPushButton
        self.pushButton_load_composition : QPushButton
        self.pushButton_remove_gas : QPushButton
        self.pushButton_reset_fluid : QPushButton

        # QTableWidget
        self.tableWidget_new_fluid : QTableWidget

        # QTreeWidget
        self.treeWidget_reference_gases : QTreeWidget

    def _create_connections(self):
        #
        self.pushButton_add_gas.clicked.connect(self.add_selected_fluid_button_callback)
        self.pushButton_confirm.clicked.connect(self.get_fluid_properties)
        self.pushButton_load_composition.clicked.connect(self.load_fluid_composition_callback)
        self.pushButton_remove_gas.clicked.connect(self.remove_selected_gas)
        self.pushButton_reset_fluid.clicked.connect(self.reset_fluid)
        #
        self.tableWidget_new_fluid.cellClicked.connect(self.cell_clicked_on_composition_table)
        self.tableWidget_new_fluid.itemChanged.connect(self.item_changed_callback)
        #
        self.treeWidget_reference_gases.itemClicked.connect(self.on_click_item_refprop_fluids)
        self.treeWidget_reference_gases.itemDoubleClicked.connect(self.on_double_click_item_refprop_fluids)

    def _config_widgets(self):

        self.label_discharge.setVisible(False)
        self.label_suction.setVisible(False)
        self.label_spacing.setVisible(False)
        #
        self.lineEdit_pressure_disch.setVisible(False)
        self.lineEdit_temperature_disch.setVisible(False)

    def check_state_properties(self, state_properties: dict):

        self.comboBox_temperature_units.setDisabled(True)
        self.comboBox_pressure_units.setDisabled(True)
        self.comboBox_temperature_units.setCurrentIndex(0)

        self.reciprocating_machine = state_properties.get("source", None)
        self.check_ideal_gas = state_properties.get("check_ideal_gas", True)

        if self.reciprocating_machine is None:

            pressure = state_properties.get("pressure", None)
            temperature = state_properties.get("temperature", None)

            if isinstance(temperature, (int | float)):
                self.lineEdit_temperature.setText(str(round(temperature, 4)))

            if isinstance(pressure, (int | float)):
                self.lineEdit_pressure.setText(f"{pressure : .8e}")

        else:

            self.label_discharge.setVisible(True)
            self.label_suction.setVisible(True)
            self.label_spacing.setVisible(True)

            self.lineEdit_temperature.setDisabled(True)
            self.lineEdit_pressure.setDisabled(True)

            self.lineEdit_pressure_disch.setVisible(True)
            self.lineEdit_pressure_disch.setDisabled(True)

            self.lineEdit_temperature_disch.setVisible(True)
            self.lineEdit_temperature_disch.setDisabled(True)

            self.connection_type = state_properties['connection_type']
            self.T_suction = state_properties[f'temperature_at_suction']
            self.P_suction = state_properties[f'suction_pressure']

            if self.connection_type == "suction":
                self.lineEdit_pressure_disch.setVisible(False)
                self.lineEdit_temperature_disch.setVisible(False)
                self.label_discharge.setVisible(False)

            if 'suction_pressure' in state_properties.keys():
                self.lineEdit_temperature.setText(f"{self.T_suction : .4f}")
                self.lineEdit_pressure.setText(f"{self.P_suction : .8e}")

            if 'pressure_ratio' in state_properties.keys():
                self.p_ratio =  state_properties['pressure_ratio']
                self.P_discharge = self.p_ratio * self.P_suction

            elif 'discharge_pressure' in state_properties.keys():
                self.P_discharge = state_properties['discharge_pressure']

            self.lineEdit_pressure_disch.setText(f"{self.P_discharge : .8e}")

            if 'temperature_at_discharge' in state_properties.keys():
                self.T_discharge = state_properties[f'temperature_at_discharge']
                self.lineEdit_temperature_disch.setText(f"{self.T_discharge : .4f}")

            else:

                tool_tip = "The temperature at discharge will be "
                tool_tip += "calculated after the fluid definition."

                self.lineEdit_temperature_disch.setText("---")
                self.lineEdit_temperature_disch.setToolTip(tool_tip)

    def update_selected_fluid(self):

        if self.selected_fluid_to_edit:

            [fluid_name, temperature, pressure, key_mixture, molar_fractions] = self.selected_fluid_to_edit

            fluid_file_names = key_mixture.split(";")
            self.lineEdit_fluid_name.setText(fluid_name)
            self.lineEdit_temperature.setText(str(temperature))
            self.lineEdit_pressure.setText(str(pressure))
            self.comboBox_temperature_units.setCurrentIndex(0)

            for index, fluid_file_name in enumerate(fluid_file_names):
                final_name = self.fluid_file_to_final_name[fluid_file_name]
                str_molar_fraction = str(round(molar_fractions[index]*100, 6))
                self.fluid_to_composition[final_name] = [str_molar_fraction, 
                                                         molar_fractions[index], 
                                                         fluid_file_name]

            self.load_fluid_composition_info()
            self.update_remainig_composition()

    def add_selected_fluid_button_callback(self):
        self.add_selected_fluid_to_composition_table(self.selected_fluid)

    def add_selected_gas(self, fluid_name, molar_fraction):

        fluid_file_name, _, _ = self.refprop_fluids[fluid_name]

        if isinstance(molar_fraction, float):

            self.fluid_to_composition[fluid_name] = [  str(molar_fraction), 
                                                        molar_fraction / 100, 
                                                        fluid_file_name  ]

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

        _remain = round(self.remaining_molar_fraction*100, 6)
        if _remain == 0:
            _remain = 0.00

        self.remaining_composition_highlight(_remain)
        self.label_remaining_composition.setText(str(_remain))

        if round(abs(self.remaining_molar_fraction), 6) == 0:
            if self.reciprocating_machine == "reciprocating_compressor":
                temperature_K = self.T_suction
                pressure_Pa = self.P_suction
                self.get_specific_fluid_property(   
                                                 self.isentropic_label,
                                                 temperature_K,
                                                 pressure_Pa   
                                                 )

    def remaining_composition_highlight(self, value):
        if value >= 0:
            style_sheet =   """  QLabel{border-radius: 4px; border-color: rgb(100, 100, 100); border-style: solid; border-width: 1px}
                            """
        else:
            style_sheet =   """  QLabel{border-radius: 4px; border-color: rgb(250, 10, 10); border-style: solid; border-width: 2px; color: rgb(250, 10, 10)}
                            """
        self.label_remaining_composition.setStyleSheet(style_sheet)

    def get_specific_fluid_property(self, key_prop: str, temperature_K: int | float, pressure_Pa: int | float):
        
        units = self.refprop.GETENUMdll(0, "MASS BASE SI").iEnum

        fluids_string = ""
        molar_fractions = list()

        for _, _fraction, file_name in self.fluid_to_composition.values():
            fluids_string += file_name + ";"
            molar_fractions.append(_fraction)
        fluids_string = fluids_string[:-1]

        read = self.refprop.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                        temperature_K, pressure_Pa, molar_fractions )

        if read.herr:
            return

        if key_prop == "M":
            fluid_property = 1000*read.Output[0]   
        else:
            fluid_property = read.Output[0]

        if key_prop == self.isentropic_label:
            _k = fluid_property 
            self.T_discharge = (self.T_suction)*(self.p_ratio**((_k-1)/_k))
            self.lineEdit_temperature_disch.setText(str(round(self.T_discharge, 4)))
        
        return fluid_property

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

        title = f"Resetting of the fluid composition"
        message = "Would you like to reset the current fluid composition?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        self.fluid_to_composition.clear()
        self.load_fluid_composition_info()
        self.update_remainig_composition()

    def load_default_gases_info(self):
        self.config_table_data()
        self.treeWidget_reference_gases.clear()
        self.treeWidget_reference_gases.headerItem().setText(0, "Default fluid library")
        for gas in self.refprop_fluids.keys():
            new = QTreeWidgetItem([gas])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_reference_gases.addTopLevelItem(new)

    def config_table_data(self):

        header = ['Fluid name', 'Molar fraction [%]']
        
        self.tableWidget_new_fluid.setColumnCount(len(header))
        self.tableWidget_new_fluid.setHorizontalHeaderLabels(header)
        self.tableWidget_new_fluid.setSelectionBehavior(1)
        self.tableWidget_new_fluid.resizeColumnsToContents()

        self.tableWidget_new_fluid.horizontalHeader().setSectionResizeMode(0)
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

        self.label_selected_fluid.setText("")
        self.tableWidget_new_fluid.blockSignals(False)

    def check_composition_input(self, fluid_name, composition):

        if isinstance(composition, float):

            fluid_file_name, _, _ = self.refprop_fluids[fluid_name]
            self.fluid_to_composition[fluid_name] = [  str(composition), 
                                                        composition / 100, 
                                                        fluid_file_name  ]

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

        self.tableWidget_new_fluid.setItem(rows, 0, QTableWidgetItem(selected_fluid))
        self.tableWidget_new_fluid.item(rows, 0).setTextAlignment(Qt.AlignCenter)

        if self.add_molar_fraction_to_cell(rows):
            self.tableWidget_new_fluid.blockSignals(False)
            return

        molar_fraction = self.tableWidget_new_fluid.item(rows, 1).text()
        self.add_selected_gas(self.selected_fluid, float(molar_fraction))

        self.tableWidget_new_fluid.blockSignals(False)

    def add_molar_fraction_to_cell(self, row, molar_fraction=None):

        if molar_fraction is None:
            self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem())
            self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)
            return True

        try:

            if isinstance(molar_fraction, str):
                molar_fraction = molar_fraction.replace(",", ".")
                self.tableWidget_new_fluid.setItem(row, 1, QTableWidgetItem(molar_fraction))
                self.tableWidget_new_fluid.item(row, 1).setTextAlignment(Qt.AlignCenter)

        except:
            self.tableWidget_new_fluid.item(row, 1).setSelected(True)
            return True

    def get_fluid_properties(self):

        message = ""
        self.errors = dict()
        self.fluid_setup = list()
        self.ideal_gas_warning = False

        if round(self.remaining_molar_fraction, 6) == 0:
            if self.lineEdit_fluid_name.text() != "":

                self.fluid_properties = dict()
                units = self.refprop.GETENUMdll(0, "MASS BASE SI").iEnum

                fluids_string = ""
                molar_fractions = list()

                for composition_data in self.fluid_to_composition.values():

                    if len(composition_data) != 3:
                        continue

                    _, _fraction, file_name = composition_data

                    fluids_string += file_name + ";"
                    molar_fractions.append(_fraction)

                if fluids_string == "":
                    return

                fluids_string = fluids_string[:-1]

                values = self.get_temperature_and_pressure_SI_units()

                if values is None:
                    return

                [temperature_K, pressure_Pa] = values
                self.fluid_properties["temperature"] = temperature_K
                self.fluid_properties["pressure"] = pressure_Pa
                self.fluid_properties["name"] = self.lineEdit_fluid_name.text()

                if self.reciprocating_machine == "reciprocating_compressor":

                    for key_prop in self.map_properties.keys():

                        if key_prop in ["PRANDTL", "TD", "KV", "QMASS", "QMOLE"]:
                            continue

                        read = self.refprop.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                        temperature_K, pressure_Pa, molar_fractions )

                        if read.herr:
                            if key_prop ==  "ANC-TP":
                                continue
                            else:
                                self.errors[self.map_properties[key_prop]] = read.herr

                        if key_prop == "M":
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0] * 1e3

                        else:
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]
                            if key_prop == self.isentropic_label:
                                self.k = read.Output[0] 

                    self.T_discharge = (self.T_suction)*(self.p_ratio**((self.k-1)/self.k))
                    self.lineEdit_temperature_disch.setText(str(round(self.T_discharge, 4)))
                    temperature_K = self.T_discharge
                    pressure_Pa = self.P_discharge

                    if self.connection_type == "discharge":
                        count = 0
                        criteria = 100
                        cache_temperatures = [temperature_K]
                        while criteria > 0.001 and count <= 100:

                            for key_prop in self.map_properties.keys():

                                if key_prop in ["PRANDTL", "TD", "KV", "QMASS", "QMOLE"]:
                                    continue

                                read = self.refprop.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                                temperature_K, pressure_Pa, molar_fractions )

                                if read.herr:
                                    if key_prop ==  "ANC-TP":
                                        continue
                                    else:
                                        self.errors[self.map_properties[key_prop]] = read.herr

                                if key_prop == "M":
                                    self.fluid_properties[self.map_properties[key_prop]] = read.Output[0] * 1e3

                                else:
                                    self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]

                                if key_prop == self.isentropic_label:
                                    k_iter = read.Output[0]

                            # evaluate the temperature assuming isentropic compression
                            temperature_K_iter = self.T_suction*(self.p_ratio**((k_iter-1)/k_iter))

                            cache_temperatures.append(temperature_K_iter)
                            criteria = abs(cache_temperatures[-1]-cache_temperatures[-2])/((cache_temperatures[-1]+cache_temperatures[-2])/2)

                            temperature_K = temperature_K_iter
                            self.fluid_properties["temperature"] = temperature_K

                            count += 1
                            # print(count, k_iter, cache_temperatures[-1], cache_temperatures[-2], criteria)

                        self.fluid_properties["pressure"] = pressure_Pa

                else:

                    for key_prop in self.map_properties.keys():

                        if key_prop in ["PRANDTL", "TD", "KV", "QMASS", "QMOLE"]:
                            continue

                        read = self.refprop.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                        temperature_K, pressure_Pa, molar_fractions )

                        if read.herr:
                            if key_prop ==  "ANC-TP":
                                continue
                            else:
                                self.errors[self.map_properties[key_prop]] = read.herr

                        if key_prop == "M":
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0] * 1e3

                        else:
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]

                        if key_prop == "Z":
                            Z = read.Output[0]
                            if Z < 0.9 or Z > 1.1:
                                self.ideal_gas_warning = True

                fluid_density = self.fluid_properties["density"]
                speed_of_sound = self.fluid_properties["speed_of_sound"]
                acoustic_impedance = fluid_density*speed_of_sound

                self.fluid_properties["impedance"] = round(acoustic_impedance, 6)
                self.fluid_setup = [fluids_string, molar_fractions]

                self.process_errors()
                # if self.process_errors():
                #     return

                if self.ideal_gas_warning and self.check_ideal_gas:

                    self.hide()

                    title = "Deviation from ideal gas behavior"
                    message = f"The gas compressibility factor Z = {round(Z, 6)} exceeds the internal criteria of +/- 10% "
                    message += "for ideal gases. The real gases could be treated as ideal if the compressibility "
                    message += " factor tends to the unit."

                    message += "\n\nPress Yes to ignore this warning and get fluid properties or No to cancel."

                    buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
                    read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

                    if app().main_window.force_close:
                        self.close()
                        return

                    if read._cancel:
                        self.complete = False                        
                        app().main_window.set_input_widget(self)
                        return

                    # if read._continue:
                    #     self.complete = True

                self.complete = True
                self.close()
                return

            else:

                title = "Additional input required"
                message = "Define a fluid name at specific input field to proceed."
                self.lineEdit_fluid_name.setFocus()

        else:

            title = "Fluid composition not invalid"
            remaining_molar_fraction = round(100*self.remaining_molar_fraction, 6)
            message += "The sum of all molar fractions must be equals to the unity. It is recommended "
            message += "to adjust the fluid composition until this requirement is met.\n\n"
            message += f"Remaining molar fraction: {remaining_molar_fraction} %"

        if message != "":
            self.hide()
            PrintMessageInput([window_title_1, title, message])

    def process_errors(self):
        if len(self.errors) != 0:
            title = "Error while processing fluid properties"
            message = "The following errors were found in while processing the fluid properties.\n\n"
            for key, _error in self.errors.items():
                message += f"{str(key)}: {str(_error)}\n\n"
            message += "It is recommended to check the fluid composition and state properties to proceed."
            PrintMessageInput([window_title_1, title, message])
            return True

    def actions_to_finalize(self):
        if self.state_properties:
            if self.state_properties["connection_type"] == 1:
                title = "Fluid properties convergence"
                message = "The following fluid properties were obtained after completing the iterative updating process:"
                message += f"\n\nTemperature (discharge) = {round(self.fluid_properties['temperature'],4)} [K]"
                message += f"\nIsentropic exponent = {round(self.fluid_properties['isentropic_exponent'],6)} [-]"
                message += "\n\nReference fluid properties:"
                message += f"\n\nTemperature (suction) = {self.state_properties['temperature_at_suction']} [K]"
                message += f"\nPressure (suction) = {self.state_properties['pressure_suction']} [Pa]"
                message += f"\nPressure (discharge) = {round(self.state_properties['pressure_discharge'],4)} [Pa]"
                message += f"\nMolar mass = {round(self.fluid_properties['molar_mass'],6)} [kg/mol]"   
                PrintMessageInput([window_title_2, title, message])

    def check_input_value(self, str_value: str, label: str):

        value = None

        if str_value != "":

            try:
                str_value = str_value.replace(",", ".")
                value = float(str_value)

            except Exception as error_log:
                title = f"Invalid entry to the {label}"
                message = f"Dear user, you have typed an invalid value at the {label} input field."
                message += "You should to inform a valid float number to proceed.\n\n"
                message += f"Details: {str(error_log)}"
                PrintMessageInput([window_title_1, title, message])
                return None

        else:
            title = "Empty field detected"
            message = f"The {label} input field is empty. Please, inform a valid float number to proceed."
            PrintMessageInput([window_title_1, title, message])
            return None       

        return value

    def get_temperature_and_pressure_SI_units(self):
        
        if self.reciprocating_machine == "reciprocating_pump":
            if self.state_properties["connection_type"] == "suction":
                temperature_K = self.state_properties["temperature_at_suction"]
                pressure_Pa = self.state_properties["suction_pressure"]

            else:
                temperature_K = self.state_properties["temperature_at_discharge"]
                pressure_Pa = self.state_properties["discharge_pressure"]

            return [temperature_K, pressure_Pa]

        str_temperature = self.lineEdit_temperature.text()
        str_pressure = self.lineEdit_pressure.text()

        _temperature_value = self.check_input_value(str_temperature, "'temperature'")
        if _temperature_value is None:
            return None

        tu_index = self.comboBox_temperature_units.currentIndex()
        if tu_index == 1:
            _temperature_value += 273.15

        elif tu_index == 2:
            _temperature_value = (_temperature_value - 32) * (5 / 9) + 273.15

        if _temperature_value < 0:
            title = "Invalid entry to the temperature"
            message = "The typed value at temperature input field reaches a negative value in Kelvin scale."
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([window_title_1, title, message])
            return None

        _pressure_value = self.check_input_value(str_pressure, "'pressure'")
        if _pressure_value is None:
            return None

        pressure_unit = self.comboBox_pressure_units.currentText()
        if "kPa" in pressure_unit:
            _pressure_value *= 1e3

        elif "atm" in pressure_unit:
            _pressure_value *= 101325

        elif "bar" in pressure_unit:
            _pressure_value *= 1e5

        elif "kgf/cm²" in pressure_unit:
            _pressure_value *= 9.80665e4

        elif "psi" in pressure_unit:
            _pressure_value *= 6.89475729e3

        elif "ksi" in pressure_unit:
            _pressure_value *= 6.89475729e6

        if "(g)" in pressure_unit:
            _pressure_value += 101325

        if _pressure_value < 0:
            title = "Invalid entry to the pressure"
            message = "The typed value at pressure input field reaches a negative value in Pascal scale. "
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([window_title_1, title, message])
            return None

        return [round(_temperature_value, 6), round(_pressure_value, 6)]

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

            self.add_selected_gas(selected_fluid, molar_fraction)

        else:

            if self.item_is_invalid_number(item):
                self.tableWidget_new_fluid.blockSignals(False)
                return
 
            self.go_to_next_cell(item)

            selected_fluid = self.tableWidget_new_fluid.item(item.row(), 0).text()
            molar_fraction = self.tableWidget_new_fluid.item(item.row(), 1).text()

            if molar_fraction != "":
                molar_fraction = float(molar_fraction)
            self.add_selected_gas(selected_fluid, molar_fraction)

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
            item.setText("")
            return True
        
        message = ""

        if value > 100 or value < 0:
            message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
            message += "The value should be a positive value less or equals to 100."

        if message != "":
            window_title = "Error"
            title = "Invalid molar fraction"
            PrintMessageInput([window_title, title, message])
            item.setText("")
            return True
        
        return False

    def get_refprop_path(self):

        refProp_path = None
        try:
            refProp_path = os.environ['RPPREFIX']
        except:
            pass

        if refProp_path is None:
            try:
                refProp_path = app().config.get_refprop_path_from_file()
            except:
                pass

        if refProp_path is None:

            caption = 'Search for the REFPROP folder'
            initial_path = str(Path().home())

            folder_path = app().main_window.file_dialog.get_existing_directory(caption, initial_path)
            
            if folder_path == "":
                return None

            if os.path.exists(folder_path):

                if os.path.basename(folder_path) in ["REFPROP", "Refprop", "refprop"]:
                    app().config.write_refprop_path_in_file(folder_path)
                    refProp_path = folder_path

                else:
                    title = "Invalid folder selected"
                    message = f"The selected folder path {folder_path} does not match with the REFPROP installation folder. "
                    message += "As suggestion, try to find the default installation folder in 'C:/Program Files (x86)/REFPROP'. "
                    message += "You should select the valid REFPROP installation folder to proceed."
                    PrintMessageInput([window_title_1, title, message])

        return refProp_path

    def check_refprop_version(self):
        version = self.refprop.RPVersion()
        if version[:3] != "10.":
            title = "Invalid REFPROP version"
            message = "The installed REFPROP version is incompatible with the OpenPulse requirements. It is recommended "
            message += "to install a newer REFPROP version to maintain the compatibility with the application.\n\n"
            message += f"Current version: {version}\n"
            message +=  "Required version: >= 10.0"
            PrintMessageInput([window_title_2, title, message])
            return True
        self.setWindowTitle(f"OpenPulse (REFPROP v{version})")

    def default_library_gases(self):
        try:
            
            from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary
            
            self.refprop_fluids = dict()
            self.fluid_file_to_final_name = dict()

            refProp_path = self.get_refprop_path()

            if refProp_path is None:
                return True

            if os.path.exists(refProp_path):
                
                self.refprop = REFPROPFunctionLibrary(refProp_path)
                if self.check_refprop_version():
                    return True

                self.refprop.SETPATHdll(refProp_path)
                refProp_fluids_path = get_new_path(refProp_path, "FLUIDS")
                list_files = os.listdir(refProp_fluids_path)
                
                for fluid_file in list_files:
                    if ".BNC" not in fluid_file:
                        filepath = get_new_path(refProp_fluids_path, fluid_file)
                        
                        f = open(filepath, 'r')
                        line_0 = f.readline()
                        line_1 = f.readline()
                        line_2 = f.readline()

                        f.close()
                        short_name = line_0.split("!")[0]
                        full_name = line_2.split("!")[0]
                
                        letter = " "
                        while letter == " ":
                            short_name = short_name[:-1]
                            letter = short_name[-1]
                            
                        letter = " "
                        while letter == " ":
                            full_name = full_name[:-1]
                            letter = full_name[-1]

                        final_name = short_name if short_name == full_name else f"{short_name} ({full_name})"
                        self.refprop_fluids[final_name] = [fluid_file, short_name, full_name]
                        self.fluid_file_to_final_name[fluid_file] = final_name

            else:
                title = "REFPROP installation not detected"
                message = "Dear user, the REFPROP application files were not found in the computer's default paths. "
                message += "Please, install the REFPROP on your computer to enable the set-up of the fluids mixture."
                PrintMessageInput([window_title_1, title, message])
                return True

        except Exception as error_log:
            title = "Error while loading REFPROP"
            message = "An error has been reached while trying to load REFPROP data. If the REFPROP module has already been "
            message += "installed we recommend running the 'pip install ctREFPROP' command at the terminal to install the "
            message += "necessary libraries.\n\n"
            message += f"Details: {str(error_log)}"
            PrintMessageInput([window_title_1, title, message])
            return True

    def load_fluid_composition_callback(self):

        self.hide()
        self.label_selected_fluid.setText("")

        self.fluid_data = dict()
        self.fluid_to_composition = dict()
        read = LoadFluidCompositionInput(file_path = self.temp_file_path)

        if read.complete:

            self.temp_file_path = read.file_path
            composition_data = read.fluid_composition_data

            comp = 0
            for (i, label, refprop_fluid_name, molar_fraction) in composition_data:

                self.fluid_data[i] = [label, refprop_fluid_name, molar_fraction]

                if not refprop_fluid_name in self.refprop_fluids.keys():
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
            self.get_fluid_properties()
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.remove_selected_gas()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False