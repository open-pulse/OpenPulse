from PyQt5.QtWidgets import QDialog, QComboBox, QLabel, QLineEdit, QPushButton, QTabWidget, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
from pulse.tools.utils import get_new_path

import os

window_title_1 = "Error"
window_title_2 = "Warning"

class SetFluidCompositionInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/acoustic/set_fluid_composition_input.ui"
        uic.loadUi(ui_path, self)

        self.selected_fluid_to_edit = kwargs.get("selected_fluid_to_edit", None)
        self.compressor_info = kwargs.get("compressor_info", dict())
        
        self.project = app().project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()

        if self.compressor_info:
            self.check_compressor_inputs()

        self.update_remainig_composition()
        if self.default_library_gases():
            return

        self.load_default_gases_info()
        self.update_selected_fluid()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("OpenPulse")

    def _initialize(self):

        self.save_path = ""
        self.export_file_path = ""
        self.userPath = os.path.expanduser('~')
        self.fluid_path = self.project.get_fluid_list_path()

        # self.isentropic_label = "ISENK"   # isentropic exponent (real gas)
        self.isentropic_label = "CP/CV"     # isentropic expansion coefficient (ideal gas)

        self.map_properties = { "D" : "fluid density",
                                "CP" : "specific heat Cp",
                                "CV" : "specific heat Cv",
                                self.isentropic_label : "isentropic exponent",
                                "W" : "speed of sound",
                                "VIS" : "dynamic viscosity",
                                "TCX" : "thermal conductivity",
                                "PRANDTL" : "Prandtl number",
                                "TD" : "thermal diffusivity",
                                "KV" : "kinematic viscosity",
                                "M" : "molar mass" }

        self.selected_fluid = ""
        self.str_composition_value = ""
        self.unit_temperature = "K"
        self.unit_pressure = "Pa"
        self.composition_value = 0
        self.remaining_composition = 1
        self.list_fluids = []
        self.fluid_to_composition = {}
        self.fluid_states = {}
        self.all_fluid_state_properties = {}
        self.errors_by_fluid_state = {}
        self.complete = False
        self.state_index = None

    def _define_qt_variables(self):

        # QComboBox
        self.comboBox_temperature_units : QComboBox
        self.comboBox_pressure_units : QComboBox
        self.comboBox_temperature_units_test : QComboBox
        self.comboBox_pressure_units_test : QComboBox

        # QLabel
        self.label_selected_fluid : QLabel
        self.label_title_remaining_fraction : QLabel
        self.label_remaining_composition : QLabel
        self.label_fluid_temperature : QLabel
        self.label_fluid_pressure : QLabel
        self.label_temperature_unit : QLabel
        self.label_pressure_unit : QLabel
        self.label_fluid_density : QLabel
        self.label_fluid_specific_heat_Cp : QLabel
        self.label_fluid_specific_heat_Cv : QLabel
        self.label_fluid_isentropic_coefficient : QLabel
        self.label_fluid_speed_of_sound : QLabel
        self.label_fluid_dynamic_viscosity : QLabel
        self.label_fluid_thermal_conductivity : QLabel
        self.label_discharge : QLabel
        self.label_suction : QLabel

        # QLineEdit
        self.lineEdit_composition : QLineEdit
        self.lineEdit_fluid_name : QLineEdit
        self.label_fluid_state_index : QLabel
        self.lineEdit_temperature : QLineEdit
        self.lineEdit_pressure : QLineEdit
        self.lineEdit_pressure_disch : QLineEdit
        self.lineEdit_temperature_disch : QLineEdit
        self.lineEdit_temperature_test : QLineEdit
        self.lineEdit_pressure_test : QLineEdit

        # QPushButton
        self.pushButton_confirm : QPushButton
        self.pushButton_reset_fluid : QPushButton
        self.pushButton_add_gas : QPushButton
        self.pushButton_remove_gas : QPushButton
        self.pushButton_add_fluid_state : QPushButton
        self.pushButton_remove_fluid_state : QPushButton
        self.pushButton_get_fluid_properties_info : QPushButton

        # QTabWidget
        self.tabWidget_main : QTabWidget

        # QTreeWidget
        self.treeWidget_reference_gases : QTreeWidget
        self.treeWidget_new_gas : QTreeWidget
        self.treeWidget_fluid_states : QTreeWidget

    def _create_connections(self):
        #
        self.comboBox_temperature_units_test.currentIndexChanged.connect(self.update_state_treeWidget_info)
        self.comboBox_pressure_units_test.currentIndexChanged.connect(self.update_state_treeWidget_info)
        #
        self.pushButton_add_gas.clicked.connect(self.add_selected_gas)
        self.pushButton_add_fluid_state.clicked.connect(self.add_fluid_state)
        self.pushButton_confirm.clicked.connect(self.get_fluid_properties)
        self.pushButton_remove_fluid_state.clicked.connect(self.remove_fluid_state)
        self.pushButton_remove_gas.clicked.connect(self.remove_selected_gas)
        self.pushButton_reset_fluid.clicked.connect(self.reset_fluid)
        # self.pushButton_use_remaining_molar_fraction.clicked.connect(self.use_remaining_molar_fraction)
        #
        self.tabWidget_main.currentChanged.connect(self.update_state_treeWidget_info)
        self.treeWidget_new_gas.itemDoubleClicked.connect(self.on_double_click_item_new_gas)
        self.treeWidget_fluid_states.itemClicked.connect(self.on_click_item_fluid_state)
        self.treeWidget_fluid_states.itemDoubleClicked.connect(self.on_doubleclick_item_fluid_state)
        self.treeWidget_new_gas.itemClicked.connect(self.on_click_item_new_gas)
        self.treeWidget_reference_gases.itemClicked.connect(self.on_click_item_reference_gases)

    def _config_widgets(self):
        self.label_discharge.setVisible(False)
        self.label_suction.setVisible(False)
        #
        self.lineEdit_pressure_disch.setVisible(False)
        self.lineEdit_temperature_disch.setVisible(False)
        #
        self.treeWidget_new_gas.setColumnWidth(0, 376)
        self.treeWidget_fluid_states.setColumnWidth(0, 60)
        self.treeWidget_fluid_states.setColumnWidth(1, 120)
        self.treeWidget_fluid_states.setColumnWidth(2, 120)

    def _call_help(self):
        title = "Thermodynamic states checking"
        message = "The pretest analysis checks if all fluid states lead to valid fluid properties. "
        message += "If the calculated fluid properties are physically consistent, the new fluid can "
        message += "be added to the fluid library, otherwise, it cannot."
        PrintMessageInput([window_title_2, title, message])

    def check_compressor_inputs(self):

        self.comboBox_temperature_units.setDisabled(True)
        self.comboBox_pressure_units.setDisabled(True)
        self.label_discharge.setVisible(True)
        self.label_suction.setVisible(True)
        self.lineEdit_pressure_disch.setVisible(True)
        self.lineEdit_temperature_disch.setVisible(True)
        self.lineEdit_temperature.setDisabled(True)
        self.lineEdit_temperature_disch.setDisabled(True)
        self.lineEdit_pressure.setDisabled(True)
        self.lineEdit_pressure_disch.setDisabled(True)
        self.tabWidget_main.setTabVisible(1, False)
    
        self.connection_type_comp = self.compressor_info['connection type']
        self.connection_label = "discharge" if self.connection_type_comp else "suction"
        
        self.T_suction = self.compressor_info[f'temperature (suction)']
        self.P_suction = self.compressor_info[f'pressure (suction)']
        self.p_ratio =  self.compressor_info['pressure ratio']
        self.P_discharge = self.p_ratio*self.P_suction

        if self.connection_label == "suction":
            self.lineEdit_pressure_disch.setVisible(False)
            self.lineEdit_temperature_disch.setVisible(False)
            self.label_discharge.setVisible(False)
    
        self.lineEdit_temperature.setText(str(round(self.T_suction, 4)))
        self.lineEdit_pressure.setText(str(round(self.P_suction, 2)))
        self.lineEdit_pressure_disch.setText(str(round(self.P_discharge, 2)))
        self.lineEdit_temperature_disch.setText("---")
        self.lineEdit_temperature_disch.setToolTip("The temperature at discharge will be calculated after the fluid definition.")
        

    def update_selected_fluid(self):
        if self.selected_fluid_to_edit:
            [fluid_name, temperature, pressure, key_mixture, molar_fractions] = self.selected_fluid_to_edit
            fluid_file_names = key_mixture.split(";")
            self.lineEdit_fluid_name.setText(fluid_name)
            self.lineEdit_temperature.setText(str(temperature))
            self.lineEdit_pressure.setText(str(pressure))

            for index, fluid_file_name in enumerate(fluid_file_names):
                final_name = self.fluid_file_to_final_name[fluid_file_name]
                str_molar_fraction = str(round(molar_fractions[index]*100, 5))
                self.fluid_to_composition[final_name] = [str_molar_fraction, molar_fractions[index], fluid_file_name]

            self.load_new_gas_composition_info()
            self.update_remainig_composition()

    def use_remaining_molar_fraction(self):
        self.lineEdit_composition.setText(str(self.remaining_composition))

    def add_selected_gas(self):
        if self.label_selected_fluid.text() != "":
            if self.check_composition_input():
                return
            self.load_new_gas_composition_info()
            self.update_remainig_composition()  
        else:
            title = "None 'Fluid' selected"
            message = "Dear user, it is necessary to select a fluid in the list to proceed"
            PrintMessageInput([window_title_1, title, message])   
    
    def update_remainig_composition(self):
        self.remaining_composition = 1
        for [_, composition_value, _] in self.fluid_to_composition.values():
            self.remaining_composition -= composition_value

        if round(abs(self.remaining_composition),5) > 0:
            self.label_remaining_composition.setVisible(True)
            self.label_title_remaining_fraction.setVisible(True)
            _remain = round(self.remaining_composition*100, 5)
            self.label_remaining_composition.setText(str(_remain))
        else:
            self.label_remaining_composition.setText("")
            self.label_remaining_composition.setVisible(False)
            self.label_title_remaining_fraction.setVisible(False)
            if self.compressor_info:
                temperature_K = self.T_suction
                pressure_Pa = self.P_suction
                self.get_specific_fluid_property(   self.isentropic_label,
                                                    temperature_K,
                                                    pressure_Pa   )

    def get_specific_fluid_property(self, key_prop, temperature_K, pressure_Pa):
        
        units = self.RefProp.GETENUMdll(0, "MASS BASE SI").iEnum

        fluids_string = ""
        molar_fractions = []
        for _, _fraction, file_name in self.fluid_to_composition.values():
            fluids_string += file_name + ";"
            molar_fractions.append(_fraction)
        fluids_string = fluids_string[:-1]

        read = self.RefProp.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
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


    def create_font(self, size):
        self.font = QFont()
        self.font.setPointSize(size)
        self.font.setItalic(False)
        # self.font.setBold(True)
        # self.font.setWeight(75)

    def remove_selected_gas(self):
        if self.label_selected_fluid.text() != "":
            _fluid = self.label_selected_fluid.text()
            if _fluid in self.fluid_to_composition.keys():
                self.fluid_to_composition.pop(_fluid)
                self.load_new_gas_composition_info()
                self.update_remainig_composition() 

    def reset_fluid(self):
            title = f"Resetting of the current 'Fluid Composition'"
            message = "Do you really want to reset the current Fluid Composition?\n\n"
            
            message += "\n\nPress the Continue button to proceed with the resetting or press Cancel or "
            message += "\nClose buttons to abort the current operation."
            buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Continue"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)


            if read._stop:
                return

            self.fluid_to_composition.clear()
            self.load_new_gas_composition_info()
            self.update_remainig_composition()

    def load_default_gases_info(self):
        self.treeWidget_reference_gases.clear()
        self.treeWidget_reference_gases.setGeometry(10, 142, 376, 400)
        self.treeWidget_reference_gases.headerItem().setText(0, "Default fluid library")
        for gas in self.list_gases.keys():
            new = QTreeWidgetItem([gas])
            new.setTextAlignment(0, Qt.AlignCenter)
            self.treeWidget_reference_gases.addTopLevelItem(new)
        
    def load_new_gas_composition_info(self):
        # if self.selected_fluid != "":
        self.treeWidget_new_gas.clear()
        self.treeWidget_new_gas.setGeometry(576, 142, 509, 400)
        self.treeWidget_new_gas.headerItem().setText(0, "Fluid")
        self.treeWidget_new_gas.headerItem().setText(1, "Composition [%]")
        for fluid, [str_composition, _, _] in self.fluid_to_composition.items():
            new = QTreeWidgetItem([fluid, str_composition])
            new.setTextAlignment(0, Qt.AlignCenter)
            new.setTextAlignment(1, Qt.AlignCenter)
            self.treeWidget_new_gas.addTopLevelItem(new)
        self.label_selected_fluid.setText("")
        self.lineEdit_composition.setText("")

    def check_composition_input(self):
        self.str_composition_value = self.lineEdit_composition.text()
        if self.str_composition_value != "":
            title = "Invalid input value to the fluid Composition"
            message = ""
            value = None
            try:
                value = float(self.str_composition_value)
            except Exception as log_error:
                message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
                message += "\nPlease, check the typed value to proceed with the fluid setup.\n\n"
                message += str(log_error)
            
            if value is not None:             
                if value>100 or value<0:
                    message = "Dear user, you have typed an invalid entry at the fluid Composition input. "
                    message += "The value must be a positive value less or equals to 100."
                    message += "\nPlease, check the typed value to proceed with the fluid setup."

            if round(value/100, 5) >  round(self.remaining_composition, 5):
                _remain = round(self.remaining_composition*100, 5)
                message = "Dear user, you have typed an invalid entry at the Fluid Composition input. "
                message += f"The value must be a positive value less or equals to {_remain}%."
                message += "\nPlease, check the typed value to proceed with the fluid setup."

            if message == "":
                
                self.composition_value = value/100
                fluid_file_name, _, _ = self.list_gases[self.selected_fluid]
                self.fluid_to_composition[self.selected_fluid] = [  self.str_composition_value, 
                                                                    self.composition_value, 
                                                                    fluid_file_name  ]
                if self.composition_value == 0:
                    if self.selected_fluid in self.fluid_to_composition.keys():
                        self.fluid_to_composition.pop(self.selected_fluid)       
                return False
            else:
                PrintMessageInput([window_title_1, title, message])
                return True
        else:
            title = "Empty entry at molar fraction input field"
            message = "An Empty entry has been detected at molar fraction input field. "
            message += "You should to inform a valid positive float number less than 1 to proceed."
            PrintMessageInput([window_title_1, title, message])
            return True

    def update_label_selected_fluid_font(self):
        if len(self.selected_fluid) < 20:
            fontsize = 12
        elif len(self.selected_fluid) < 40:
            fontsize = 11
        elif len(self.selected_fluid) < 60:
            fontsize = 10
        elif len(self.selected_fluid) < 70:
            fontsize = 9
        else:
            fontsize = 8
        self.create_font(fontsize)
        self.label_selected_fluid.setFont(self.font)

    def on_click_item_reference_gases(self, item):
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(self.selected_fluid)
        self.update_label_selected_fluid_font()
    
    def on_double_click_item_new_gas(self, item):
        return

    def on_click_item_new_gas(self, item):
        self.selected_fluid = item.text(0)
        self.label_selected_fluid.setText(item.text(0))
        self.lineEdit_composition.setText(item.text(1))
        self.update_label_selected_fluid_font()
        
    def get_fluid_properties(self):
        message = ""
        self.fluid_setup = []
        self.errors = {}
        if round(self.remaining_composition, 5) == 0:
            if self.lineEdit_fluid_name.text() != "":
                self.fluid_properties = {}
                units = self.RefProp.GETENUMdll(0, "MASS BASE SI").iEnum

                fluids_string = ""
                molar_fractions = []
                for _, _fraction, file_name in self.fluid_to_composition.values():
                    fluids_string += file_name + ";"
                    molar_fractions.append(_fraction)
                fluids_string = fluids_string[:-1]

                self.unit_temperature_update(self.comboBox_temperature_units)
                self.unit_pressure_update(self.comboBox_pressure_units)
                values = self.check_input_values_with_units(self.lineEdit_temperature, 
                                                            self.lineEdit_pressure)

                if values is None:
                    return
                else:
                    [temperature_K, pressure_Pa] = values
                    self.fluid_properties["temperature"] = temperature_K
                    self.fluid_properties["pressure"] = pressure_Pa

                self.fluid_properties["fluid name"] = self.lineEdit_fluid_name.text()
                
                if self.compressor_info:

                    for key_prop in ["D", "CV", "CP", self.isentropic_label, "W", "VIS", "TCX", "M"]:#, "PRANDTL", "TD", "KV"]:

                        read = self.RefProp.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                        temperature_K, pressure_Pa, molar_fractions )

                        if read.herr:
                            self.errors[self.map_properties[key_prop]] = read.herr
                        
                        if key_prop == "M":
                            self.fluid_properties[self.map_properties[key_prop]] = 1000*read.Output[0]   
                        else:
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]
                            if key_prop == self.isentropic_label:
                                self.k = read.Output[0] 
                    
                    self.T_discharge = (self.T_suction)*(self.p_ratio**((self.k-1)/self.k))
                    self.lineEdit_temperature_disch.setText(str(round(self.T_discharge,4)))
                    temperature_K = self.T_discharge
                    pressure_Pa = self.P_discharge

                    if self.connection_label == "discharge":
                        count = 0
                        criteria = 100
                        cache_temperatures = [temperature_K]
                        while criteria > 0.001 and count <= 100:

                            for key_prop in ["D", "CV", "CP", self.isentropic_label, "W", "VIS", "TCX", "M"]:#, "PRANDTL", "TD", "KV"]:
                                read = self.RefProp.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                                temperature_K, pressure_Pa, molar_fractions )

                                if read.herr:
                                    self.errors[self.map_properties[key_prop]] = read.herr
                                
                                if key_prop == "M":
                                    self.fluid_properties[self.map_properties[key_prop]] = 1000*read.Output[0]   
                                else:
                                    self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]

                                if key_prop == self.isentropic_label:
                                    k_iter = read.Output[0]
                            
                            count += 1
                            temperature_K_iter = self.T_suction*(self.p_ratio**((k_iter-1)/k_iter))
                            cache_temperatures.append(temperature_K_iter)
                            criteria = abs(cache_temperatures[-1]-cache_temperatures[-2])/((cache_temperatures[-1]+cache_temperatures[-2])/2)
                            temperature_K = temperature_K_iter
                            self.fluid_properties["temperature"] = temperature_K
                            # print(count, k_iter, cache_temperatures[-1], cache_temperatures[-2], criteria)
                        
                        self.fluid_properties["pressure"] = pressure_Pa

                else:

                    for key_prop in ["D", "CV", "CP", self.isentropic_label, "W", "VIS", "TCX", "M"]:#, "PRANDTL", "TD", "KV"]:
                        read = self.RefProp.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                        temperature_K, pressure_Pa, molar_fractions )

                        if read.herr:
                            self.errors[self.map_properties[key_prop]] = read.herr
                        
                        if key_prop == "M":
                            self.fluid_properties[self.map_properties[key_prop]] = 1000*read.Output[0]    
                        else:
                            self.fluid_properties[self.map_properties[key_prop]] = read.Output[0]

                self.fluid_properties["impedance"] = round(self.fluid_properties["fluid density"]*self.fluid_properties["speed of sound"],6)
                self.fluid_setup = [fluids_string, molar_fractions]
                
                if self.process_errors():
                    return

                self.complete = True
                self.close()
                # self.actions_to_finalize()
            else:
                title = "Additional input required"
                message = "Define a fluid name at specific input field to proceed."
                self.lineEdit_fluid_name.setFocus()
        else:
            title = "Fluid composition not finished"
            message = "Dear user, you should to complete the fluid mixture composition to proceed. "
            message += "The sum of all fluids molar fractions must be equals to 1. It is recommended "
            message += "to check the inserted molar fractions until this requirement is met."
        if message != "":
            PrintMessageInput([window_title_1, title, message])

    def process_errors(self):
        if len(self.errors) != 0:
            title = "REFPROP: Error while processing fluid properties"
            message = "The following errors were found while processing the fluid properties.\n\n"
            for key, _error in self.errors.items():
                message += f"{str(key)}: {str(_error)}\n\n"
            message += "It is recommended to check the fluid composition and state properties to proceed."
            PrintMessageInput([window_title_1, title, message])
            return True

    def get_fluid_state_index(self):
        index = len(self.fluid_states) + 1
        if str(index) in self.fluid_states.keys():
            index = 1
            while str(index) in self.fluid_states.keys():
                index += 1
        self.state_index = str(index)

    def actions_to_finalize(self):
        if self.compressor_info:
            if self.compressor_info["connection type"] == 1:
                title = "Fluid properties convergence"
                message = "The following fluid properties were obtained after completing the iterative updating process:"
                message += f"\n\nTemperature (discharge) = {round(self.fluid_properties['temperature'],4)} [K]"
                message += f"\nIsentropic exponent = {round(self.fluid_properties['isentropic exponent'],6)} [-]"
                message += "\n\nReference fluid properties:"
                message += f"\n\nTemperature (suction) = {self.compressor_info['temperature (suction)']} [K]"
                message += f"\nPressure (suction) = {self.compressor_info['pressure (suction)']} [Pa]"
                message += f"\nPressure (discharge) = {round(self.compressor_info['pressure (discharge)'],4)} [Pa]"
                message += f"\nMolar mass = {round(self.fluid_properties['molar mass'],6)} [kg/mol]"   
                PrintMessageInput([window_title_2, title, message])

    def add_fluid_state(self):
        self.get_fluid_state_index()
        self.unit_temperature_update(self.comboBox_temperature_units_test)
        self.unit_pressure_update(self.comboBox_pressure_units_test)
        values = self.check_input_values_with_units(self.lineEdit_temperature_test, self.lineEdit_pressure_test)
        if values is None:
            return
        else:
            if values not in self.fluid_states.values():
                self.fluid_states[self.state_index] = values
        self.run_pretest_analysis()

    def check_temperature_value(self, lineEdit_temperature):
        temperature = None
        str_value = lineEdit_temperature.text()
        if str_value != "":
            try:
                temperature = float(str_value)
            except Exception as log_error:
                title = "Invalid entry to the temperature"
                message = "Dear user, you have typed an invalid value at the temperature input field."
                message += "You should to inform a valid float number to proceed."
                PrintMessageInput([window_title_1, title, message])
        else:
            title = "Empty temperature input field"
            message = "Dear user, the temperature input field is empty. Please, inform a valid float number to proceed."
            PrintMessageInput([window_title_1, title, message])
            lineEdit_temperature.setFocus()
        return temperature

    def check_pressure_value(self, lineEdit_pressure):
        pressure = None
        str_value = lineEdit_pressure.text()
        if str_value != "":
            try:
                pressure = float(str_value)
            except Exception as log_error:
                title = "Invalid entry to the pressure"
                message = "Dear user, you have typed an invalid value at the pressure input field."
                message += "You should to inform a valid float number to proceed."
                PrintMessageInput([window_title_1, title, message])
        else:
            title = "Empty pressure input field"
            message = "Dear user, the pressure input field is empty. Please, inform a valid float number to proceed."
            PrintMessageInput([window_title_1, title, message])
            lineEdit_pressure.setFocus()        
        return pressure

    def remove_fluid_state(self):
        if self.state_index in self.fluid_states.keys():
            self.fluid_states.pop(self.state_index)
            self.update_state_treeWidget_info()

    def unit_temperature_update(self, comboBox_temperature_units):
        temperature_unit_labels = ["K", "°C", "°F"]
        index_temperature = comboBox_temperature_units.currentIndex()
        self.unit_temperature = temperature_unit_labels[index_temperature]

    def unit_pressure_update(self, comboBox_pressure_units):
        self.unit_pressure = comboBox_pressure_units.currentText()
        self.unit_pressure = self.unit_pressure.replace(" ", "")

    def check_input_values_with_units(self, lineEdit_temperature, lineEdit_pressure):

        _temperature_value = self.check_temperature_value(lineEdit_temperature)
        if _temperature_value is None:
            return None

        if self.unit_temperature == "°C" :
            _temperature_value += 273.15
        elif self.unit_temperature == "°F" :
            _temperature_value = (_temperature_value-32)*(5/9) + 273.15
        
        if _temperature_value < 0:
            title = "Invalid entry to the temperature"
            message = "The typed value at temperature input field reaches a negative value in Kelvin scale."
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([window_title_1, title, message])
            return None

        _pressure_value = self.check_pressure_value(lineEdit_pressure)
        if _pressure_value is None:
            return None

        if self.unit_pressure == "kPa":
            _pressure_value *= 1e3
        elif self.unit_pressure == "atm":
            _pressure_value *= 101325
        elif self.unit_pressure == "bar":
            _pressure_value *= 1e5
        elif self.unit_pressure == "kgf/cm²":
            _pressure_value *= 9.80665e4
        elif self.unit_pressure == "psi":
            _pressure_value *= 6894.75729
        elif self.unit_pressure == "ksi":
            _pressure_value *= 6.89475729e6

        if _pressure_value < 0:
            title = "Invalid entry to the pressure"
            message = "The typed value at pressure input field reaches a negative value in Pascal scale. "
            message += "It is necessary to enter a value that maintains the physicall coherence and consistence "
            message += "to proceed with the fluid setup."
            PrintMessageInput([window_title_1, title, message])
            return None

        return [round(_temperature_value, 5), round(_pressure_value, 5)]

    def update_fluid_state_header(self):
        self.unit_temperature_update(self.comboBox_temperature_units_test)
        self.unit_pressure_update(self.comboBox_pressure_units_test)
        self.treeWidget_fluid_states.headerItem().setText(0, f"Index")
        self.treeWidget_fluid_states.headerItem().setText(1, f"Temperature [{self.unit_temperature}]")
        self.treeWidget_fluid_states.headerItem().setText(2, f"Pressure [{self.unit_pressure}]")
        self.treeWidget_fluid_states.headerItem().setText(3, "Set of properties")
        for i in range(4):
            self.treeWidget_fluid_states.headerItem().setTextAlignment(i, Qt.AlignCenter)

    def update_state_treeWidget_info(self):
        if self.tabWidget_main.currentIndex() == 1:
            self.update_fluid_state_header()
            self.treeWidget_fluid_states.clear()
            for index, [temperature, pressure] in self.fluid_states.items():
                
                if self.unit_temperature == "°C":
                    temperature -= 273.15
                elif self.unit_temperature == "°F":
                    temperature = (temperature - 273.15)*(9/5) + 32

                if self.unit_pressure == "kPa":
                    pressure /= 1e3
                elif self.unit_pressure == "atm":
                    pressure /= 101325
                elif self.unit_pressure == "bar":
                    pressure /= 1e5
                elif self.unit_pressure == "kgf/cm²":
                    pressure /= 9.80665e4
                elif self.unit_pressure == "psi":
                    pressure /= 6894.75729
                elif self.unit_pressure == "ksi":
                    pressure /= 6.89475729e6
                
                if self.errors_by_fluid_state:
                    if self.errors_by_fluid_state[index] != 0:
                        status = "invalid"
                    else:
                        status = "valid"  
                else:
                    status = "--" 

                new = QTreeWidgetItem([index, str(round(temperature, 6)), str(round(pressure,6)), status])
                for i in range(5):
                    new.setTextAlignment(i, Qt.AlignCenter)
                self.treeWidget_fluid_states.addTopLevelItem(new)

            self.state_index = None
            self.lineEdit_temperature.setText("")
            self.lineEdit_pressure.setText("")
            self.label_fluid_state_index.setText("")
            self.pushButton_reset_fluid.setVisible(False)
            self.pushButton_confirm.setVisible(False)
            self.reset_fluid_properties_labels()
        else:
            self.pushButton_reset_fluid.setVisible(True) 
            self.pushButton_confirm.setVisible(True)

    def on_click_item_fluid_state(self, item):
        str_index = item.text(0)
        if str_index != "":
            self.label_fluid_state_index.setText(str_index)
            self.state_index = str_index
            self.fluid_temperature = item.text(1)
            self.fluid_pressure = item.text(2)

    def on_doubleclick_item_fluid_state(self, item):
        self.on_click_item_fluid_state(item)
        self.get_fluid_properties_by_state()

    def run_pretest_analysis(self):
        self.errors_by_fluid_state = {}
        self.all_fluid_state_properties = {}
        for index, [temperature_K, pressure_Pa] in self.fluid_states.items():
            # message = ""
            if round(self.remaining_composition, 5) == 0:
                # self.fluid_properties = {}
                units = self.RefProp.GETENUMdll(0, "MASS BASE SI").iEnum

                fluids_string = ""
                molar_fractions = []
                for _, _fraction, file_name in self.fluid_to_composition.values():
                    fluids_string += file_name + ";"
                    molar_fractions.append(_fraction)
                fluids_string = fluids_string[:-1]
                
                fluid_properties_by_state = {}
                for key_prop in ["D", "CV", "CP", self.isentropic_label, "W", "VIS", "TCX"]:#, "PRANDTL", "TD", "KV"]:
                    read = self.RefProp.REFPROPdll( fluids_string, "TP", key_prop, units, 0, 0, 
                                                    temperature_K, pressure_Pa, molar_fractions )
                    if index in self.errors_by_fluid_state.keys():
                        if read.herr:
                            self.errors_by_fluid_state[index] += 1
                    else:
                        self.errors_by_fluid_state[index] = 0
                    fluid_properties_by_state[self.map_properties[key_prop]] = read.Output[0]

                self.all_fluid_state_properties[index] = fluid_properties_by_state  
  
        self.update_state_treeWidget_info()

    def get_fluid_properties_by_state(self):
        if self.all_fluid_state_properties:
            fluid_state_properties = self.all_fluid_state_properties[self.state_index]
            self.label_fluid_temperature.setText(str(self.fluid_temperature))
            self.label_temperature_unit.setText(f"[{self.unit_temperature}]")
            self.label_pressure_unit.setText(f"[{self.unit_pressure}]")
            self.label_fluid_pressure.setText(str(self.fluid_pressure))
            self.label_fluid_density.setText(str(round(fluid_state_properties["fluid density"],6)))
            self.label_fluid_specific_heat_Cp.setText(str(round(fluid_state_properties["specific heat Cp"],6)))
            self.label_fluid_specific_heat_Cv.setText(str(round(fluid_state_properties["specific heat Cv"],6)))
            self.label_fluid_isentropic_coefficient.setText(str(round(fluid_state_properties["isentropic exponent"],6)))
            self.label_fluid_speed_of_sound.setText(str(round(fluid_state_properties["speed of sound"],6)))
            self.label_fluid_dynamic_viscosity.setText(str(round(fluid_state_properties["dynamic viscosity"],10)))
            self.label_fluid_thermal_conductivity.setText(str(round(fluid_state_properties["thermal conductivity"],6)))
    
    def reset_fluid_properties_labels(self):
        self.label_fluid_temperature.setText("")
        self.label_fluid_pressure.setText("")
        self.label_fluid_density.setText("")
        self.label_fluid_specific_heat_Cp.setText("")
        self.label_fluid_specific_heat_Cv.setText("")
        self.label_fluid_isentropic_coefficient.setText("")
        self.label_fluid_speed_of_sound.setText("")
        self.label_fluid_dynamic_viscosity.setText("")
        self.label_fluid_thermal_conductivity.setText("")

    def default_library_gases(self):
        try:
            
            from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary
            
            self.list_gases = {}
            self.fluid_file_to_final_name = {}
            refProp_path = os.environ['RPPREFIX']

            if os.path.exists(refProp_path):
                
                self.RefProp = REFPROPFunctionLibrary(refProp_path)
                self.RefProp.SETPATHdll(refProp_path)
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
                        self.list_gases[final_name] = [fluid_file, short_name, full_name]
                        self.fluid_file_to_final_name[fluid_file] = final_name
            else:
                title = "REFPROP installation not detected"
                message = "Dear user, REFPROP application files were not found in the computer's default paths. "
                message += "Please, install the REFPROP on your computer to enable the set-up of the fluids mixture."
                PrintMessageInput([window_title_1, title, message])
                return True

        except Exception as log_error:
            title = "Error while loading REFPROP"
            message = "An error has been reached while trying to load REFPROP data. If the REFPROP module has already been "
            message += "installed we recommend running the 'pip install ctREFPROP' command at the terminal to install the "
            message += "necessary libraries."
            message += f"\n\n{str(log_error)}"
            PrintMessageInput([window_title_1, title, message])
            return True
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.get_fluid_properties()
        elif event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.remove_selected_gas()
        elif event.key() == Qt.Key_Escape:
            self.close()