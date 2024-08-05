from PyQt5.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QRadioButton, QTabWidget, QTreeWidget, QTreeWidgetItem, QWidget
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import numpy as np
import configparser

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.preprocessing.fluid import Fluid
from pulse.libraries.default_libraries import default_fluid_library
from pulse.interface.user_input.model.setup.general.color_selector import PickColorInput
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.interface.user_input.model.setup.fluid.set_fluid_composition_input import SetFluidCompositionInput
from pulse.interface.formatters.icons import get_openpulse_icon
from pulse.tools.utils import *

window_title_1 = "Error"
window_title_2 = "Warning"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class FluidInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "model/setup/acoustic/fluid_input.ui"
        uic.loadUi(ui_path, self)
        
        self.compressor_thermodynamic_state = kwargs.get("compressor_thermodynamic_state", dict())
        
        self.project = app().project
        app().main_window.set_input_widget(self)

        self._load_icons()
        self._config_window()

        self._initialize()
        self._define_qt_variable()
        self._create_connections()
        
        self._loading_info_at_start()
        
        if self.compressor_thermodynamic_state:
            self.check_compressor_inputs()

        while self.keep_window_open:
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
        self.before_run = self.project.get_pre_solution_model_checks()
        self.fluid_path = self.project.get_fluid_list_path()
        self.lines_from_model = self.project.preprocessor.lines_from_model

        self.keep_window_open = True

        self.dict_inputs = {}
        self.REFPROP = None
        self.fluid_data_REFPROP = {}
        self.fluid_name_to_REFPROP_data = {}
        self.clicked_item = None
        self.fluid = None
        self.flagAll = False
        self.flagSelection = False
        self.complete = False
        self.refprop_fluid = False
        self.list_ids = []

        self.adding = False
        self.editing = False
        self.force_check = False
        self.temp_fluid_color = ""
        self.fluid_density = 0
        self.speed_of_sound = 0

        self.fluid_data_keys = ["name", 
                                "fluid density", 
                                "speed of sound", 
                                "impedance", 
                                "isentropic exponent", 
                                "thermal conductivity", 
                                "specific heat Cp", 
                                "dynamic viscosity",
                                "temperature",
                                "pressure",
                                "molar mass"]


    def _define_qt_variable(self):
        # QComboBox
        self.comboBox_fluid_id = self.findChild(QComboBox, 'comboBox_fluid_id')    
        self.comboBox_fluid_id_rp = self.findChild(QComboBox, 'comboBox_fluid_id_rp')  
        # QLineEdit
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_fluid_name = self.findChild(QLineEdit, 'lineEdit_selected_fluid_name')
        #
        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')
        self.lineEdit_fluid_density = self.findChild(QLineEdit, 'lineEdit_fluid_density')
        self.lineEdit_speed_of_sound = self.findChild(QLineEdit, 'lineEdit_speed_of_sound')
        self.lineEdit_impedance = self.findChild(QLineEdit, 'lineEdit_impedance')
        self.lineEdit_isentropic_exponent = self.findChild(QLineEdit, 'lineEdit_isentropic_exponent')
        self.lineEdit_thermal_conductivity = self.findChild(QLineEdit, 'lineEdit_thermal_conductivity')
        self.lineEdit_specific_heat_Cp = self.findChild(QLineEdit, 'lineEdit_specific_heat_Cp')
        self.lineEdit_dynamic_viscosity = self.findChild(QLineEdit, 'lineEdit_dynamic_viscosity')
        self.lineEdit_temperature = self.findChild(QLineEdit, 'lineEdit_temperature')
        self.lineEdit_pressure = self.findChild(QLineEdit, 'lineEdit_pressure')
        #
        self.lineEdit_name_rp = self.findChild(QLineEdit, 'lineEdit_name_rp')
        self.lineEdit_id_rp = self.findChild(QLineEdit, 'lineEdit_id_rp')
        self.lineEdit_color_rp = self.findChild(QLineEdit, 'lineEdit_color_rp')
        self.lineEdit_fluid_density_rp = self.findChild(QLineEdit, 'lineEdit_fluid_density_rp')
        self.lineEdit_speed_of_sound_rp = self.findChild(QLineEdit, 'lineEdit_speed_of_sound_rp')
        self.lineEdit_impedance_rp = self.findChild(QLineEdit, 'lineEdit_impedance_rp')
        self.lineEdit_isentropic_exponent_rp = self.findChild(QLineEdit, 'lineEdit_isentropic_exponent_rp')
        self.lineEdit_thermal_conductivity_rp = self.findChild(QLineEdit, 'lineEdit_thermal_conductivity_rp')
        self.lineEdit_specific_heat_Cp_rp = self.findChild(QLineEdit, 'lineEdit_specific_heat_Cp_rp')
        self.lineEdit_dynamic_viscosity_rp = self.findChild(QLineEdit, 'lineEdit_dynamic_viscosity_rp')
        self.lineEdit_temperature_rp = self.findChild(QLineEdit, 'lineEdit_temperature_rp')
        self.lineEdit_pressure_rp = self.findChild(QLineEdit, 'lineEdit_pressure_rp')
        #
        self.lineEdit_name_edit = self.findChild(QLineEdit, 'lineEdit_name_edit')
        self.lineEdit_id_edit = self.findChild(QLineEdit, 'lineEdit_id_edit')
        self.lineEdit_color_edit = self.findChild(QLineEdit, 'lineEdit_color_edit')
        self.lineEdit_fluid_density_edit = self.findChild(QLineEdit, 'lineEdit_fluid_density_edit')
        self.lineEdit_speed_of_sound_edit = self.findChild(QLineEdit, 'lineEdit_speed_of_sound_edit')
        self.lineEdit_impedance_edit = self.findChild(QLineEdit, 'lineEdit_impedance_edit')
        self.lineEdit_isentropic_exponent_edit = self.findChild(QLineEdit, 'lineEdit_isentropic_exponent_edit')
        self.lineEdit_thermal_conductivity_edit = self.findChild(QLineEdit, 'lineEdit_thermal_conductivity_edit')
        self.lineEdit_specific_heat_Cp_edit = self.findChild(QLineEdit, 'lineEdit_specific_heat_Cp_edit')
        self.lineEdit_dynamic_viscosity_edit = self.findChild(QLineEdit, 'lineEdit_dynamic_viscosity_edit')
        self.lineEdit_temperature_edit = self.findChild(QLineEdit, 'lineEdit_temperature_edit')
        self.lineEdit_pressure_edit = self.findChild(QLineEdit, 'lineEdit_pressure_edit')
        #
        self.lineEdit_color.setDisabled(True)
        self.lineEdit_color_rp.setDisabled(True)
        self.lineEdit_color_edit.setDisabled(True)
        # QPushButton
        self.pushButton_pickColor_add_user_defined = self.findChild(QPushButton, 'pushButton_pickColor_add_user_defined')
        self.pushButton_pickColor_add_refprop = self.findChild(QPushButton, 'pushButton_pickColor_add_refprop')
        self.pushButton_pickColor_edit = self.findChild(QPushButton, 'pushButton_pickColor_edit')
        self.pushButton_confirm_add_fluid = self.findChild(QPushButton, 'pushButton_confirm_add_fluid')
        self.pushButton_confirm_add_fluid_rp = self.findChild(QPushButton, 'pushButton_confirm_add_fluid_rp')
        self.pushButton_reset_entries_add_fluid = self.findChild(QPushButton, 'pushButton_reset_entries_add_fluid')
        self.pushButton_call_refprop = self.findChild(QPushButton, 'pushButton_call_refprop')
        self.pushButton_confirm_fluid_edition = self.findChild(QPushButton, 'pushButton_confirm_fluid_edition')
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_edit_fluid_in_refprop = self.findChild(QPushButton, 'pushButton_edit_fluid_in_refprop')
        # self.pushButton_reset_entries_add_fluid_rp = self.findChild(QPushButton, 'pushButton_reset_entries_add_fluid_rp')
        # self.pushButton_reset_entries_add_fluid_rp.clicked.connect(self.reset_add_texts_rp)
        self.pushButton_pickColor_edit.setDisabled(True)
        self.pushButton_confirm_fluid_edition.setDisabled(True)
        # QRadioButton
        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()
        # QTabWidget
        self.tabWidget_fluid = self.findChild(QTabWidget, 'tabWidget_fluid')
        self.tabWidget_add = self.findChild(QTabWidget, 'tabWidget_add')
        self.tabWidget_edit = self.findChild(QTabWidget, 'tabWidget_edit')
        self.tabWidget_add.setTabVisible(2, False)
        self.tabWidget_edit.setTabVisible(1, False)
        self.tabWidget_fluid.setTabVisible(2, False)
        # QTreeWidget
        self.treeWidget_fluids = self.findChild(QTreeWidget, 'treeWidget_fluids')
        widhts = [50, 140, 170, 180, 172, 80]
        for col_index, width in enumerate(widhts):
            self.treeWidget_fluids.setColumnWidth(col_index, width)
        for col_index in [6, 7, 8, 9]:
            self.treeWidget_fluids.hideColumn(col_index)
        # QWidget
        self.tab_user_defined = self.tabWidget_add.findChild(QWidget, 'tab_user_defined')
        self.tab_refprop_button = self.tabWidget_add.findChild(QWidget, 'tab_refprop_button')
        self.tab_refprop_all_entries = self.tabWidget_add.findChild(QWidget, 'tab_refprop_all_entries')        


    def _create_connections(self):
        #
        self.comboBox_fluid_id.currentIndexChanged.connect(self.get_comboBox_index)   
        self.comboBox_fluid_id_rp.currentIndexChanged.connect(self.get_comboBox_index)
        #
        self.lineEdit_fluid_density.editingFinished.connect(self.check_add_input_fluid_density)
        self.lineEdit_speed_of_sound.editingFinished.connect(self.check_add_input_speed_of_sound)
        self.lineEdit_color_edit.editingFinished.connect(self.check_edit_input_fluid_color)
        self.lineEdit_fluid_density_edit.editingFinished.connect(self.check_edit_input_fluid_density)
        self.lineEdit_speed_of_sound_edit.editingFinished.connect(self.check_edit_input_speed_of_sound)
        #
        self.pushButton_call_refprop.clicked.connect(self.call_refprop_interface)
        self.pushButton_pickColor_add_user_defined.clicked.connect(self.pick_color_add_user_defined)
        self.pushButton_pickColor_add_refprop.clicked.connect(self.pick_color_add_refprop)
        self.pushButton_pickColor_edit.clicked.connect(self.pick_color_edit)
        self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)
        self.pushButton_confirm_add_fluid_rp.clicked.connect(self.check_add_fluid_refprop)
        self.pushButton_reset_entries_add_fluid.clicked.connect(self.reset_add_texts)
        self.pushButton_confirm_fluid_edition.clicked.connect(self.check_edit_fluid)
        self.pushButton_confirm.clicked.connect(self.confirm_fluid_attribution)
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        self.pushButton_edit_fluid_in_refprop.clicked.connect(self.edit_REFPROP_fluid)
        #
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        #
        self.treeWidget_fluids.itemClicked.connect(self.on_click_item)
        self.treeWidget_fluids.itemDoubleClicked.connect(self.on_doubleclick_item)
        self.create_lists_of_lineEdits()



    def process_selection(self, selected_lines : list):
        if selected_lines:
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(False)

    def _loading_info_at_start(self):
        self.loadList()
        if app().main_window.list_selected_lines():
            self.write_lines(lines_ids)
            self.radioButton_selected_lines.setChecked(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)
            self.radioButton_all.setChecked(True)

    def edit_REFPROP_fluid(self):
        self.hide()
        self.REFPROP = SetFluidCompositionInput(selected_fluid_to_edit = self.selected_REFPROP_fluid, 
                                                compressor_info = self.compressor_thermodynamic_state)
        app().main_window.set_input_widget(self)
        self.after_getting_fluid_properties_from_REFPROP()

    def call_refprop_interface(self):
        self.hide()
        self.REFPROP = SetFluidCompositionInput(compressor_info = self.compressor_thermodynamic_state)
        # if not self.REFPROP.complete:
        app().main_window.set_input_widget(self)
        # return
        self.after_getting_fluid_properties_from_REFPROP()

    def after_getting_fluid_properties_from_REFPROP(self):
        if self.REFPROP.complete:
            self.tabWidget_add.setTabVisible(1, False)
            self.tabWidget_add.setTabVisible(2, True)
            # self.tabWidget_add.addTab(self.tab_refprop_all_entries, "REFPROP")
            self.tabWidget_add.setCurrentIndex(2)
            self.fluid_data_REFPROP = self.REFPROP.fluid_properties
            self.fluid_setup = self.REFPROP.fluid_setup
            for index, key in enumerate(self.fluid_data_keys):
                data = self.fluid_data_REFPROP[key]
                if key == "molar mass":
                    continue
                if isinstance(data, float):
                    if key in ["thermal conductivity", "dynamic viscosity"]:
                        _data = round(data, 9)
                    elif key in ["temperature", "pressure"]:
                        _data = round(data, 4)
                    else:
                        _data = round(data, 6)
                elif isinstance(data, str):
                    _data = data
                self.list_add_lineEdit_rp[index].setText(str(_data))

            self.temperature_comp = self.fluid_data_REFPROP["temperature"]
            self.pressure_comp = self.fluid_data_REFPROP["pressure"]
            self.update_compressor_fluid_temperature_and_pressure()  
        else:
            self.REFPROP = None

    def disable_lineEdits(self):
        lineEdits = [   self.lineEdit_fluid_density_rp,
                        self.lineEdit_speed_of_sound_rp,
                        self.lineEdit_impedance_rp,
                        self.lineEdit_isentropic_exponent_rp,
                        self.lineEdit_thermal_conductivity_rp,
                        self.lineEdit_specific_heat_Cp_rp,
                        self.lineEdit_dynamic_viscosity_rp   ]
                        
        for lineEdit in lineEdits:
            lineEdit.setDisabled(True)

    def pick_color_add_user_defined(self):
        read = PickColorInput()
        if read.complete:
            #
            color = tuple(read.color)
            str_color = str(read.color).replace(" ", "")
            #
            self.lineEdit_color.setText(str_color)
            self.lineEdit_color.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")
            #
            if self.check_add_input_fluid_color():
                self.lineEdit_color.setText("")
        return read.complete


    def pick_color_add_refprop(self):
        read = PickColorInput()
        if read.complete:
            #
            color = tuple(read.color)
            str_color = str(read.color).replace(" ", "")
            #
            self.lineEdit_color_rp.setText(str_color)
            self.lineEdit_color_rp.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")
            self.refprop_fluid = True
            #
            if self.check_add_input_fluid_color():
                self.lineEdit_color_rp.setText("")
            self.refprop_fluid = False
        return read.complete

    def pick_color_edit(self):
        read = PickColorInput()
        if read.complete:
            #
            color = tuple(read.color)
            str_color = str(read.color).replace(" ", "")
            #
            self.lineEdit_color_edit.setText(str_color)
            self.lineEdit_color_edit.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")
            #
            if self.check_edit_input_fluid_color():
                self.lineEdit_color_edit.setText("")

    def write_lines(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def create_lists_of_lineEdits(self):
        self.list_add_lineEdit = [  self.lineEdit_name,
                                    self.lineEdit_fluid_density,
                                    self.lineEdit_speed_of_sound,
                                    self.lineEdit_impedance,
                                    self.lineEdit_color,
                                    self.lineEdit_isentropic_exponent,
                                    self.lineEdit_thermal_conductivity,
                                    self.lineEdit_specific_heat_Cp,
                                    self.lineEdit_dynamic_viscosity,
                                    self.lineEdit_temperature,
                                    self.lineEdit_pressure ]  

        self.list_add_lineEdit_rp = [   self.lineEdit_name_rp,
                                        self.lineEdit_fluid_density_rp,
                                        self.lineEdit_speed_of_sound_rp,
                                        self.lineEdit_impedance_rp,
                                        self.lineEdit_isentropic_exponent_rp,
                                        self.lineEdit_thermal_conductivity_rp,
                                        self.lineEdit_specific_heat_Cp_rp,
                                        self.lineEdit_dynamic_viscosity_rp,
                                        self.lineEdit_temperature_rp,
                                        self.lineEdit_pressure_rp,
                                        self.lineEdit_color_rp   ]

        self.list_edit_lineEdit = [ self.lineEdit_id_edit,
                                    self.lineEdit_name_edit,
                                    self.lineEdit_fluid_density_edit,
                                    self.lineEdit_speed_of_sound_edit,
                                    self.lineEdit_impedance_edit,
                                    self.lineEdit_color_edit,
                                    self.lineEdit_isentropic_exponent_edit,
                                    self.lineEdit_thermal_conductivity_edit,
                                    self.lineEdit_specific_heat_Cp_edit,
                                    self.lineEdit_dynamic_viscosity_edit,
                                    self.lineEdit_temperature_edit,
                                    self.lineEdit_pressure_edit ]  


    def check_compressor_inputs(self):
        if self.compressor_thermodynamic_state:

            self.tabWidget_fluid.setTabVisible(1, False)
            self.tabWidget_add.setTabVisible(0, False)
            self.tabWidget_add.setTabVisible(2, False)
            self.tabWidget_add.setCurrentIndex(1)

            # self.pushButton_confirm_add_fluid.setText("Attribute fluid")
            # self.pushButton_confirm_add_fluid_rp.setText("Attribute fluid")
            # self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)
            # self.pushButton_confirm.clicked.connect(self.confirm_fluid_attribution)

            self.radioButton_selected_lines.setChecked(True)
            self.radioButton_selected_lines.setDisabled(True)
            self.radioButton_all.setDisabled(True)

            self.line_id_comp = self.compressor_thermodynamic_state['line_id']
            # self.node_id_comp = self.compressor_thermodynamic_state['node_id']
            self.write_lines([self.line_id_comp])
            self.lineEdit_selected_ID.setDisabled(True)

            self.connection_type_comp = self.compressor_thermodynamic_state['connection type']
            self.connection_label = "discharge" if self.connection_type_comp else "suction"
            self.setWindowTitle(f"Set a fluid thermodynamic state at the compressor {self.connection_label}")

            self.temperature_comp = self.compressor_thermodynamic_state[f'temperature (suction)']
            self.pressure_comp = self.compressor_thermodynamic_state[f'pressure (suction)']
            
            # self.suction_temperature = self.compressor_thermodynamic_state[f'temperature (suction)']
            # self.suction_pressure = self.compressor_thermodynamic_state[f'pressure (suction)']

            self.update_compressor_fluid_temperature_and_pressure()


    def update_compressor_fluid_temperature_and_pressure(self):

        temperature_lineEdits = [self.lineEdit_temperature, self.lineEdit_temperature_rp]
        pressure_lineEdits = [self.lineEdit_pressure, self.lineEdit_pressure_rp]

        for temperature_lineEdit in temperature_lineEdits:
            temperature_lineEdit.setText(str(round(self.temperature_comp,4)))
            temperature_lineEdit.setDisabled(True)

        for pressure_lineEdit in pressure_lineEdits:
            pressure_lineEdit.setText(str(round(self.pressure_comp,4)))
            pressure_lineEdit.setDisabled(True)


    def check_element_type_of_lines(self):

        self.flag_all_fluid_inputs = False

        if self.flagSelection:
            
            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_selected_ids(lineEdit, "lines")
            if self.stop:
                return True

            for line in self.lines_typed:
                _line = self.lines_from_model[line]
                if _line.acoustic_element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                    self.flag_all_fluid_inputs = True
                    break
          
        elif self.flagAll:
            for line in self.project.preprocessor.all_lines:
                _line = self.lines_from_model[line]
                if _line.acoustic_element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                    self.flag_all_fluid_inputs = True
                    break
        
        return False


    def check_input_parameters(self, lineEdit, label, _float=True, _positive=False, allow_empty_entry=True):
        title = "INPUT ERROR"
        self.value = None
        value_string = lineEdit.text()
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([window_title_1, title, message])
                    lineEdit.setFocus()
                    return True
                elif value == 0 and _positive:
                    message = "You cannot input a zero value to the {}.".format(label)
                    PrintMessageInput([window_title_1, title, message])
                    lineEdit.setFocus()
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([window_title_1, title, message])
                lineEdit.setFocus()
                return True
        else:
            # self.value = None
            if allow_empty_entry:
                return False
            else:
                message = f"An empty entry has been detected at the '{label.capitalize()}' input field. \nYou should insert a valid entry to proceed."
                PrintMessageInput([window_title_1, title, message])
                lineEdit.setFocus()
                return True


    def check_add_input_fluid_name(self):
        try:
            if self.refprop_fluid:
                fluid_name = self.lineEdit_name_rp.text()
                _lineEdit = self.lineEdit_name_rp
            else:
                fluid_name = self.lineEdit_name.text()
                _lineEdit = self.lineEdit_name
        
            if fluid_name == "":
                title = "Empty fluid name"
                message = f"An empty entry has been detected at the 'Fluid name' input field. \nYou should insert a valid entry to proceed."
                PrintMessageInput([window_title_1, title, message])
                _lineEdit.setFocus()
                return True
    
            elif fluid_name != "" or self.force_check:

                if fluid_name in self.list_names:
                    title = 'Invalid fluid name'
                    message = f"Please, inform a different fluid name. The '{fluid_name}' is already \nbeing used by another fluid."
                    PrintMessageInput([window_title_1, title, message])
                    _lineEdit.setText("")
                    _lineEdit.setFocus()
                    return True
                else:
                    self.dict_inputs['name'] = fluid_name

        except Exception as error_log:
            title = 'Invalid fluid name'
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True


    def check_add_input_fluid_id(self):
        if self.REFPROP is None:
            self.dict_inputs['identifier'] = self.fluid_id
        else:
            self.dict_inputs['identifier'] = self.fluid_id_rp


    def check_add_input_fluid_color(self):

        title = "Invalid 'r, g, b' color" 
        message_empty = "An empty entry was detected at the 'Color [r,g,b]' input field. \nYou should to select a color to proceed."
        message_invalid = " Invalid color RGB input! You must input: [value1, value2, value3] \nand the values must be inside [0, 255] interval."

        try:

            if self.refprop_fluid:
                fluid_color = self.lineEdit_color_rp.text()
            else:
                fluid_color = self.lineEdit_color.text()

            if fluid_color == "":
                PrintMessageInput([title, message_empty, window_title_1])
                return True

            elif fluid_color != "" or self.force_check:

                self.colorRGB = getColorRGB(fluid_color)
                message_color = f" The RGB color {self.colorRGB} was already used.\n Please, input a different color."

                if len(self.colorRGB) != 3:
                    PrintMessageInput([title, message_invalid, window_title_1])
                    return True

                if self.colorRGB in self.list_colors:
                    PrintMessageInput([title, message_color, window_title_1])
                    return True

                self.dict_inputs['color'] = fluid_color

        except Exception as log_error:
            message_invalid += "\n\n" + str(log_error)
            PrintMessageInput([title, message_invalid, window_title_1])
            return True


    def check_edit_input_fluid_color(self):

        title = "Invalid 'r, g, b' color" 
        message_empty = "An empty entry was detected at the 'Color [r,g,b]' input field. \nYou should to select a color to proceed."
        message_invalid = " Invalid color RGB input! You must input: [value1, value2, value3] \nand the values must be inside [0, 255] interval."

        try:

            fluid_color = self.lineEdit_color_edit.text()

            if fluid_color == "":
                PrintMessageInput([title, message_empty, window_title_1])
                return True

            if fluid_color != "" or self.force_check:
                            
                self.colorRGB = getColorRGB(fluid_color)
                message_color = f" The RGB color {self.colorRGB} was already used.\n Please, input a different color."

                if len(self.colorRGB) != 3:
                    PrintMessageInput([title, message_invalid, window_title_1])
                    self.lineEdit_color_edit.setText("")
                    return True

                temp_colorRGB = getColorRGB(self.temp_fluid_color)
                if temp_colorRGB != self.colorRGB:
                    if self.colorRGB in self.list_colors:
                        PrintMessageInput([title, message_color, window_title_1])
                        self.lineEdit_color_edit.setText("")
                        return True 
                    else:
                        self.list_colors.remove(temp_colorRGB)

                self.dict_inputs['color'] = fluid_color
                            
        except Exception as log_error:
            message_invalid += "\n\n" + str(log_error)
            PrintMessageInput([title, message_invalid, window_title_1])
            self.lineEdit_color_edit.setText("")
            return True
    

    def check_add_input_fluid_density(self):
        try:
            if self.refprop_fluid:
                str_fluid_density = self.lineEdit_fluid_density_rp.text()
                _lineEdit_fluid_density = self.lineEdit_fluid_density_rp
                _lineEdit_speed_of_sound = self.lineEdit_speed_of_sound_rp
            else:
                str_fluid_density = self.lineEdit_fluid_density.text()
                _lineEdit_fluid_density = self.lineEdit_fluid_density
                _lineEdit_speed_of_sound = self.lineEdit_speed_of_sound

            if str_fluid_density != "" or self.force_check:
                if self.check_input_parameters(_lineEdit_fluid_density, 'fluid density', _positive=True, allow_empty_entry=False):
                    _lineEdit_fluid_density.setText("")
                    _lineEdit_fluid_density.setFocus()
                    return True
                else:
                    fluid_density = self.value
                    if fluid_density > 2000:
                        title = "Invalid density value"
                        message = "The input value for fluid density must be a positive number less than 2000."
                        PrintMessageInput([window_title_1, title, message])
                        _lineEdit_fluid_density.setText("")
                        _lineEdit_fluid_density.setFocus()
                        return False

                    if _lineEdit_speed_of_sound.text() != "":
                        speed_of_sound = float(_lineEdit_speed_of_sound.text())
                        impedance = round(fluid_density*speed_of_sound, 6)
                        if self.lineEdit_impedance_rp.text() == "":
                            self.lineEdit_impedance.setText(str(impedance))
                        self.dict_inputs['impedance'] = impedance
                
                self.dict_inputs['fluid density'] = fluid_density

        except Exception as error_log:
            title = 'Invalid fluid density'
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True


    def check_add_input_speed_of_sound(self):
        try:
            if self.refprop_fluid:
                str_speed_of_sound = self.lineEdit_speed_of_sound_rp.text()
                _lineEdit_speed_of_sound = self.lineEdit_speed_of_sound_rp
                _lineEdit_fluid_density = self.lineEdit_fluid_density_rp
            else:
                str_speed_of_sound = self.lineEdit_speed_of_sound.text()
                _lineEdit_speed_of_sound = self.lineEdit_speed_of_sound
                _lineEdit_fluid_density = self.lineEdit_fluid_density

            if str_speed_of_sound != "" or self.force_check:
                if self.check_input_parameters(_lineEdit_speed_of_sound, 'speed of sound', _positive=True, allow_empty_entry=False):
                    _lineEdit_speed_of_sound.setText("")
                    _lineEdit_speed_of_sound.setFocus()
                    return True
                else:
                    speed_of_sound = self.value
                    if speed_of_sound is None:
                        _lineEdit_speed_of_sound.setText("")
                        _lineEdit_speed_of_sound.setFocus()
                        return False
                        
                    if _lineEdit_fluid_density.text() != "":
                        fluid_density = float(_lineEdit_fluid_density.text())
                        impedance = round(fluid_density*speed_of_sound, 6)
                        if self.lineEdit_impedance_rp.text() == "":
                            self.lineEdit_impedance.setText(str(impedance))
                        self.dict_inputs['impedance'] = impedance
                
                self.dict_inputs['speed of sound'] = speed_of_sound

        except Exception as error_log:
            title = 'Invalid speed of sound'
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True


    def check_edit_input_fluid_density(self):
        try:
            str_fluid_density = self.lineEdit_fluid_density_edit.text()
            if str_fluid_density != "" or self.force_check:
                if self.check_input_parameters(self.lineEdit_fluid_density_edit, 'fluid density', _positive=True, allow_empty_entry=False):
                    self.lineEdit_fluid_density_edit.setText("")
                    self.lineEdit_fluid_density_edit.setFocus()
                    return True
                else:
                    fluid_density = self.value
                    if fluid_density > 2000:
                        title = "Invalid density value"
                        message = "The input value for fluid density must be a positive number less than 2000."
                        PrintMessageInput([window_title_1, title, message])
                        self.lineEdit_fluid_density_edit.setText("")
                        self.lineEdit_fluid_density_edit.setFocus()
                        return False

                    if self.lineEdit_speed_of_sound_edit.text() != "":
                        speed_of_sound = float(self.lineEdit_speed_of_sound_edit.text())
                        impedance = round(fluid_density*speed_of_sound, 6)                
                        if self.lineEdit_impedance_rp.text() == "":
                            self.lineEdit_impedance_edit.setText(str(impedance))
                        self.dict_inputs['impedance'] = impedance

                self.dict_inputs['fluid density'] = fluid_density

        except Exception as error_log:
            title = 'Invalid fluid density'
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True


    def check_edit_input_speed_of_sound(self):
        try:
            str_speed_of_sound = self.lineEdit_speed_of_sound_edit.text()
            if str_speed_of_sound != "" or self.force_check:
                if self.check_input_parameters(self.lineEdit_speed_of_sound_edit, 'speed of sound', _positive=True, allow_empty_entry=False):
                    self.lineEdit_speed_of_sound_edit.setText("")
                    self.lineEdit_speed_of_sound_edit.setFocus()
                    return True
                else:
                    speed_of_sound = self.value
                    if speed_of_sound is None:
                        self.lineEdit_speed_of_sound_edit.setText("")
                        self.lineEdit_speed_of_sound_edit.setFocus()
                        return False
                
                    if self.lineEdit_fluid_density_edit.text() != "":
                        fluid_density = float(self.lineEdit_fluid_density_edit.text())
                        impedance = round(fluid_density*speed_of_sound, 6)
                        if self.lineEdit_impedance_rp.text() == "":
                            self.lineEdit_impedance_edit.setText(str(impedance))
                        self.dict_inputs['impedance'] = impedance

                self.dict_inputs['speed of sound'] = speed_of_sound

        except Exception as error_log:
            title = 'Invalid speed of sound'
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return True
    

    def check_all_inputs(self, parameters):

        [   self.isentropic_exponent,
            self.thermal_conductivity,
            self.specific_heat_Cp,
            self.dynamic_viscosity, 
            self.temperature,
            self.pressure  ] = list(parameters.values())

        self.incomplete_inputs = False

        if self.adding:

            if 'fluid density' in self.dict_inputs.keys():
                try:
                    float(self.dict_inputs['fluid density'])
                except Exception:
                    self.force_check = True
                    if self.check_add_input_fluid_density():
                        return True
            else:
                self.force_check = True
                if self.check_add_input_fluid_density():
                    return True

            if 'speed of sound' in self.dict_inputs.keys():
                try:
                    float(self.dict_inputs['speed of sound'])
                except Exception:
                    self.force_check = True
                    if self.check_add_input_speed_of_sound():
                        return True
            else:
                self.force_check = True
                if self.check_add_input_speed_of_sound():
                    return True

        elif self.editing:

            if 'fluid density' in self.dict_inputs.keys():
                try:
                    float(self.dict_inputs['fluid density'])
                except Exception:
                    self.force_check = True
                    if self.check_edit_input_fluid_density():
                        return True
            else:
                self.force_check = True
                if self.check_edit_input_fluid_density():
                    return True

            if 'speed of sound' in self.dict_inputs.keys():
                try:
                    float(self.dict_inputs['speed of sound'])
                except Exception:
                    self.force_check = True
                    if self.check_edit_input_speed_of_sound():
                        return True
            else:
                self.force_check = True
                if self.check_edit_input_speed_of_sound():
                    return True
                    
        self.list_empty_inputs = []

        if self.isentropic_exponent.text() != "":     
            if self.check_input_parameters(self.isentropic_exponent, 'isentropic exponent', allow_empty_entry=False):
                return True
            else:
                isentropic_exponent = self.value
                self.dict_inputs['isentropic exponent'] = isentropic_exponent
        else:
            self.list_empty_inputs.append('isentropic exponent')
            self.incomplete_inputs = True

        if self.thermal_conductivity.text() != "":    
            if self.check_input_parameters(self.thermal_conductivity, 'thermal conductivity', allow_empty_entry=False):
                return True
            else:
                thermal_conductivity = self.value 
                self.dict_inputs['thermal conductivity'] = thermal_conductivity
        else:
            self.list_empty_inputs.append('thermal conductivity')
            self.incomplete_inputs = True

        if self.specific_heat_Cp.text() != "":
            if self.check_input_parameters(self.specific_heat_Cp, 'specific heat Cp', allow_empty_entry=False):
                return True
            else:
                specific_heat_Cp = self.value 
                self.dict_inputs['specific heat Cp'] = specific_heat_Cp
        else:
            self.list_empty_inputs.append('specific heat Cp')
            self.incomplete_inputs = True

        if self.dynamic_viscosity.text() != "":           
            if self.check_input_parameters(self.dynamic_viscosity, 'dinamic viscosity', allow_empty_entry=False):
                return True
            else:
                dynamic_viscosity = self.value 
                self.dict_inputs['dynamic viscosity'] = dynamic_viscosity
        else:
            self.list_empty_inputs.append('dynamic viscosity')
            self.incomplete_inputs = True
        
        if self.check_input_parameters(self.temperature, 'temperature', allow_empty_entry=False):
            return True
        else:
            temperature = self.value
            self.dict_inputs['temperature'] = temperature
    
        if self.check_input_parameters(self.pressure, 'pressure', allow_empty_entry=False):
            return True
        else:
            pressure = self.value
            self.dict_inputs['pressure'] = pressure

        if self.lineEdit_temperature_rp.text() != "":
            if 'temperature' in self.fluid_data_REFPROP.keys():
                self.dict_inputs['temperature'] = round(self.fluid_data_REFPROP["temperature"], 4)

        if self.lineEdit_pressure_rp.text() != "":
            if 'pressure' in self.fluid_data_REFPROP.keys():
                self.dict_inputs['pressure'] = round(self.fluid_data_REFPROP["pressure"], 4)   

        if self.REFPROP is not None:
            [key_mixture, molar_fractions] = self.fluid_setup
            self.dict_inputs['key mixture'] = key_mixture
            self.dict_inputs['molar fractions'] = molar_fractions
            self.dict_inputs['molar mass'] = round(self.fluid_data_REFPROP['molar mass'], 6)

        if self.incomplete_inputs:
            self.all_fluid_properties_message()


    def check_add_edit(self, parameters):
        
        if self.adding:

            self.force_check = True
            if self.check_add_input_fluid_name():
                return True
        
            if self.check_add_input_fluid_color():
                return True

        elif self.editing:

            self.dict_inputs['name'] = self.lineEdit_name_edit.text()
            self.dict_inputs['identifier'] = self.lineEdit_id_edit.text()
            
            if 'color' not in self.dict_inputs.keys():
                self.force_check = True
                if self.check_edit_input_fluid_color():
                    return True
                
        if self.check_all_inputs(parameters):
            return True
        
        fluid_name = self.dict_inputs['name']
        if fluid_name not in self.list_names:
            self.list_names.append(fluid_name)

        fluid_id = self.dict_inputs['identifier']
        if fluid_id not in self.list_ids:
            self.list_ids.append(fluid_id)
        
        color = self.dict_inputs['color']
        if color not in self.list_colors:
            self.list_colors.append(color)

        try:
            
            fluid_name = self.dict_inputs["name"]
            config = configparser.ConfigParser()
            config.read(self.fluid_path)
            config[fluid_name] = self.dict_inputs

            with open(self.fluid_path, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as log_error:
            title = "Error while saving the fluid data to the file"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return True

        if self.adding or self.editing:    
            self.treeWidget_fluids.clear()
            self.loadList()
            self.adding = False
            self.editing = False
            self.reset_add_texts()
            self.reset_edit_texts()


    def confirm_fluid_attribution(self):

        if self.clicked_item is None:
            title = "Empty fluid selection"
            message = "Select a fluid in the list before trying to attribute a fluid to the lines."
            PrintMessageInput([window_title_1, title, message])
            return
        
        if self.check_element_type_of_lines():
            return
        
        try:

            isentropic_exponent = None
            thermal_conductivity = None
            specific_heat_Cp = None
            dynamic_viscosity = None
            list_empty_inputs = []

            identifier = int(self.clicked_item.text(0))
            name = self.clicked_item.text(1)
            fluid_density = float(self.clicked_item.text(2))
            speed_of_sound = float(self.clicked_item.text(3))
            color = self.clicked_item.text(5)
            
            title = "Empty entries in fluid properties"
            message = "Please, it is necessary update the fluid properties or select another fluid in the list " 
            message += "before trying to attribute a fluid to the lines."
            message += "\n\nEmpty entries:\n"

            if self.clicked_item.text(6) != "":
                isentropic_exponent = float(self.clicked_item.text(6))
            elif self.flag_all_fluid_inputs:
                list_empty_inputs.append("isentropic exponent")    
 
            if self.clicked_item.text(7) != "":
                thermal_conductivity = float(self.clicked_item.text(7))
            elif self.flag_all_fluid_inputs:
                list_empty_inputs.append("thermal conductivity")

            if self.clicked_item.text(8) != "":
                specific_heat_Cp = float(self.clicked_item.text(8))
            elif self.flag_all_fluid_inputs:
                list_empty_inputs.append("specific heat Cp")

            if self.clicked_item.text(9) != "":
                dynamic_viscosity = float(self.clicked_item.text(9))
            elif self.flag_all_fluid_inputs:
                list_empty_inputs.append("dynamic viscosity")    

            if self.clicked_item.text(10) != "":
                temperature = float(self.clicked_item.text(10))

            if self.clicked_item.text(11) != "":
                pressure = float(self.clicked_item.text(11))

            if list_empty_inputs != []:                
                for label in list_empty_inputs:
                    message += "\n{}".format(label)  
                PrintMessageInput([window_title_1, title, message]) 
                return                   
            
            self.fluid = Fluid( name, 
                                fluid_density, 
                                speed_of_sound, 
                                identifier = identifier, 
                                color = color,
                                isentropic_exponent = isentropic_exponent,
                                thermal_conductivity = thermal_conductivity,
                                specific_heat_Cp = specific_heat_Cp,
                                dynamic_viscosity = dynamic_viscosity,
                                temperature = temperature,
                                pressure = pressure )

            if self.flagSelection:
                if self.lineEdit_selected_ID.text() == "":
                    return
                lines = self.lines_typed
                if len(self.lines_typed) <= 20:
                    print("[Set Fluid] - {} defined at lines: {}".format(self.fluid.name, self.lines_typed))
                else:
                    print("[Set Fluid] - {} defined at {} lines".format(self.fluid.name, len(self.lines_typed)))

            elif self.flagAll:
                lines = self.project.preprocessor.all_lines
                print("[Set Fluid] - {} defined at all lines.".format(self.fluid.name))

            self.project.set_fluid_by_lines(lines, self.fluid)
            # self.update_compressor_info()
            self.project.set_compressor_info_by_lines(lines, compressor_info=self.compressor_thermodynamic_state)

            self.complete = True
            app().main_window.update_plots()

            self.close()

        except Exception as log_error:
            title = "Error with the fluid list data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return


    def update_compressor_info(self):
        if self.compressor_thermodynamic_state:
            if self.REFPROP is not None:
                if self.REFPROP.complete:
                    self.compressor_thermodynamic_state["temperature (discharge)"] = round(self.fluid_data_REFPROP["temperature"], 4)
                    self.compressor_thermodynamic_state["molar mass"] = self.fluid_data_REFPROP["molar mass"]


    def loadList(self):

        self.list_names = []
        self.list_ids = []
        self.list_colors = []     

        try:
            config = configparser.ConfigParser()
            config.read(self.fluid_path)

            self.sections = config.sections()

            for fluid in self.sections:

                rFluid = config[fluid]
                keys = config[fluid].keys()

                identifier =  str(rFluid['identifier'])
                name = str(rFluid['name'])
                fluid_density =  str(rFluid['fluid density'])
                speed_of_sound =  str(rFluid['speed of sound'])
                impedance =  str(rFluid['impedance'])
                color =  str(rFluid['color'])

                isentropic_exponent, thermal_conductivity, specific_heat_Cp, dynamic_viscosity = "", "", "", ""

                if 'isentropic exponent' in keys:
                    isentropic_exponent = str(rFluid['isentropic exponent'])
                if 'thermal conductivity' in keys:
                    thermal_conductivity = str(rFluid['thermal conductivity'])
                if 'specific heat Cp' in keys:
                    specific_heat_Cp = str(rFluid['specific heat Cp'])
                if 'dynamic viscosity' in keys:
                    dynamic_viscosity = str(rFluid['dynamic viscosity'])
                
                temperature = None
                if 'temperature' in keys:
                    temperature = str(rFluid['temperature'])

                pressure = None
                if 'pressure' in keys:
                    pressure = str(rFluid['pressure'])

                key_mixture = None
                if 'key mixture' in keys:
                    key_mixture = str(rFluid['key mixture'])  

                molar_fractions = None                  
                if 'molar fractions' in keys:
                    str_molar_fractions = str(rFluid['molar fractions'])
                    molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)

                if not None in [temperature, pressure, key_mixture, molar_fractions]:
                    self.fluid_name_to_REFPROP_data[name] = [name, temperature, pressure, key_mixture, molar_fractions]

                load_fluid = QTreeWidgetItem([  identifier,
                                                name, 
                                                fluid_density,
                                                speed_of_sound, 
                                                impedance,
                                                color,
                                                isentropic_exponent,
                                                thermal_conductivity,
                                                specific_heat_Cp,
                                                dynamic_viscosity,
                                                temperature,
                                                pressure  ])

                colorRGB = getColorRGB(color)
                self.list_names.append(name)
                self.list_ids.append(int(identifier))
                self.list_colors.append(colorRGB)

                load_fluid.setBackground(5, QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_fluid.setForeground(5, QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))

                for i in range(6):
                    load_fluid.setTextAlignment(i, Qt.AlignCenter)

                self.treeWidget_fluids.addTopLevelItem(load_fluid)

        except Exception as log_error:
            title = "Error while loading the fluid list data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            self.close()

        self.update_fluid_id_selector()
        self.lineEdit_selected_fluid_name.setText("")
        

    def update_fluid_id_selector(self):

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_fluid_id.setFont(font)
        self.comboBox_fluid_id.setStyleSheet("color: rgb(0, 0, 255);")
        self.comboBox_fluid_id_rp.setFont(font)
        self.comboBox_fluid_id_rp.setStyleSheet("color: rgb(0, 0, 255);")

        N = 100
        self.available_indexes = list(np.arange(1,N+1))
        for _id in self.list_ids:
            if _id in self.available_indexes:
                self.available_indexes.remove(_id)

        self.comboBox_fluid_id.clear()
        self.comboBox_fluid_id_rp.clear()
        for fluid_id in self.available_indexes:
            text = f"         {fluid_id}"
            self.comboBox_fluid_id.addItem(text)
            self.comboBox_fluid_id_rp.addItem(text)

        self.get_comboBox_index()


    def get_comboBox_index(self):
        index = self.comboBox_fluid_id.currentIndex()
        index_rp = self.comboBox_fluid_id_rp.currentIndex()
        self.fluid_id = self.available_indexes[index]
        self.fluid_id_rp = self.available_indexes[index_rp]
        self.check_add_input_fluid_id()


    def check_add_fluid(self):
    
        parameters = {  "isentropic exponent" : self.lineEdit_isentropic_exponent, 
                        "thermal conductivity" : self.lineEdit_thermal_conductivity, 
                        "specific heat Cp" : self.lineEdit_specific_heat_Cp, 
                        "dynamic viscosity" : self.lineEdit_dynamic_viscosity,
                        "temperature" : self.lineEdit_temperature,
                        "pressure" : self.lineEdit_pressure  }

        self.adding = True
        self.editing = False
        self.check_add_edit( parameters )


    def check_add_fluid_refprop(self):

        parameters = {  "isentropic exponent" : self.lineEdit_isentropic_exponent_rp, 
                        "thermal conductivity" : self.lineEdit_thermal_conductivity_rp, 
                        "specific heat Cp" : self.lineEdit_specific_heat_Cp_rp, 
                        "dynamic viscosity" : self.lineEdit_dynamic_viscosity_rp,
                        "temperature" : self.lineEdit_temperature_rp,
                        "pressure" : self.lineEdit_pressure_rp  }

        self.adding = True
        self.editing = False
        self.refprop_fluid = True
        if not self.check_add_edit( parameters ):
            self.reset_add_texts_rp()
    

    def all_fluid_properties_message(self):
        title = "WARNING - EMPTY ENTRIES IN FLUID INPUTS"
        message = "You should input all fluid properties if you are going to use the following acoustic element types: "
        message += "wide-duct, LRF fluid equivalent and LRF full." 
        message += "\n\nEmpty entries:\n"
        for label in self.list_empty_inputs:
            message += "\n{}".format(label)
        PrintMessageInput([window_title_2, title, message])


    def hightlight(self):
        self.treeWidget_fluids.setStyleSheet("color:rgb(0, 0, 255)")
        self.treeWidget_fluids.setLineWidth(2)


    def remove_hightlight(self):
        self.treeWidget_fluids.setStyleSheet("color:rgb(0, 0, 0)")
        self.treeWidget_fluids.setLineWidth(1)


    def check_edit_fluid(self):
        if self.lineEdit_name_edit.text() == "":
            title = "Empty fluid selection"
            message = "Please, select a fluid in the list to be edited."
            PrintMessageInput([window_title_2, title, message])
            self.hightlight()
            return

        parameters = {  "isentropic exponent" : self.lineEdit_isentropic_exponent_edit, 
                        "thermal conductivity" : self.lineEdit_thermal_conductivity_edit, 
                        "specific heat Cp" : self.lineEdit_specific_heat_Cp_edit, 
                        "dynamic viscosity" : self.lineEdit_dynamic_viscosity_edit,
                        "temperature" : self.lineEdit_temperature_edit,
                        "pressure" : self.lineEdit_pressure_edit  }

        self.adding = False
        self.editing = True
        self.remove_hightlight()
        self.check_add_edit( parameters )    


    def radioButtonEvent(self):

        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()

        if self.flagSelection:

            self.lineEdit_selected_ID.setEnabled(True)
            lines_ids = app().main_window.list_selected_lines()
            if lines_ids != []:
                self.write_lines(lines_ids)
            else:
                self.lineEdit_selected_ID.setText("")
    
        elif self.flagAll:
            self.lineEdit_selected_ID.setEnabled(False)
            self.lineEdit_selected_ID.setText("All lines")


    def on_click_item(self, item):

        self.clicked_item = item

        self.lineEdit_selected_fluid_name.setText("")
        self.pushButton_confirm.setVisible(False)
        self.pushButton_call_refprop.setDisabled(False)
        self.pushButton_edit_fluid_in_refprop.setDisabled(True)

        if self.compressor_thermodynamic_state:
            if str(round(self.temperature_comp,4)) != item.text(10):
                return
            if str(round(self.pressure_comp,4)) != item.text(11):
                return
        else:
            if self.tabWidget_fluid.currentIndex() == 0:
                self.tabWidget_fluid.setCurrentIndex(1)
            if self.tabWidget_edit.currentIndex() == 1:
                self.tabWidget_edit.setCurrentIndex(0)

        self.pushButton_confirm.setVisible(True)
        
        self.selected_fluid_to_edit()
        
        # N = len(self.list_edit_lineEdit)
        # for i in range(N):
        #     self.list_edit_lineEdit[i].setText(item.text(i))
        # self.temp_fluid_color = item.text(2)   

        fluid_name = item.text(1)
        self.lineEdit_selected_fluid_name.setText(fluid_name)

        if fluid_name in self.fluid_name_to_REFPROP_data.keys():
            self.tabWidget_fluid.setTabVisible(1, True)
            self.tabWidget_fluid.setCurrentIndex(1)
            self.tabWidget_edit.setTabVisible(1, True)
            self.tabWidget_edit.setCurrentIndex(1)
            self.pushButton_call_refprop.setDisabled(True)
            self.pushButton_edit_fluid_in_refprop.setDisabled(False)
            self.selected_REFPROP_fluid = self.fluid_name_to_REFPROP_data[fluid_name]   
        else:
            self.tabWidget_add.setCurrentIndex(0)

        self.pushButton_pickColor_edit.setDisabled(False)
        self.pushButton_confirm_fluid_edition.setDisabled(False)


    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.confirm_fluid_attribution()
    

    def selected_fluid_to_edit(self):

        if self.clicked_item is None:
            self.title = "NO FLUID SELECTION"
            self.message = "Select a fluid in the list to be edited."
            PrintMessageInput([self.title, self.message, window_title_2])
            return True
        
        try:

            self.editing = True
            self.temp_fluid_name = self.clicked_item.text(0)
            self.temp_fluid_id = self.clicked_item.text(1)
            self.temp_fluid_color = self.clicked_item.text(5)

            N = len(self.list_edit_lineEdit)
            for i in range(N):
                self.list_edit_lineEdit[i].setText(self.clicked_item.text(i))

            color = tuple(getColorRGB(self.temp_fluid_color))
            self.lineEdit_color_edit.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")

        except Exception as error_log:
            self.title = "ERROR WHILE LOADING THE FLUID LIST DATA"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title_1])
            return True

        return False
    

    def confirm_fluid_removal(self):

        self.adding = False
        self.editing = False

        if self.clicked_item is None:
            return
        try:
            selected_name = self.clicked_item.text(1)
            config = configparser.ConfigParser()
            config.read(self.fluid_path)
            if selected_name in config.sections():
                config.remove_section(selected_name)
                with open(self.fluid_path, 'w') as config_file:
                    config.write(config_file)

            for line_id, entity in self.lines_from_model.items():
                if entity.fluid is not None:
                    if entity.fluid.name == selected_name:
                        self.project.set_fluid_by_lines(line_id, None)
                        self.project.set_compressor_info_by_lines(line_id, compressor_info={})

            self.treeWidget_fluids.clear()
            self.clicked_item = None
            self.loadList()
            self.reset_add_texts()
            self.reset_edit_texts()

        except Exception as log_error:
            title = "Error with the material removal"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def reset_library_to_default(self):

        self.hide()

        title = "Resetting of fluids library"
        message = "Would you like to reset the fluid library to default values?"

        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Proceed"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:

            config_cache = configparser.ConfigParser()
            config_cache.read(self.fluid_path)  
            sections_cache = config_cache.sections()
            
            default_fluid_library(self.fluid_path)
            config = configparser.ConfigParser()
            config.read(self.fluid_path)

            fluid_names = []
            for section_cache in sections_cache:
                if section_cache not in config.sections():
                    fluid_names.append(config_cache[section_cache]["name"])

            for line_id, entity in self.lines_from_model.items():
                if entity.fluid is not None:
                    if entity.fluid.name in fluid_names:
                        self.project.set_fluid_by_lines(line_id, None)
                        self.project.set_compressor_info_by_lines(line_id, compressor_info={})

            self.treeWidget_fluids.clear()
            self.loadList()
            self.reset_add_texts()
            self.reset_edit_texts()
            app().main_window.update_plots()


    def reset_add_texts(self):
        for lineEdit in self.list_add_lineEdit:
            lineEdit.setText("")


    def reset_add_texts_rp(self):
        for lineEdit in self.list_add_lineEdit_rp:
            lineEdit.setText("")
        self.tabWidget_add.removeTab(1)
        self.tabWidget_add.addTab(self.tab_refprop_button, "REFPROP")
        self.refprop_fluid = False


    def reset_edit_texts(self):
        for lineEdit in self.list_edit_lineEdit:
            lineEdit.setText("")
        self.lineEdit_color_edit.setStyleSheet("")

    # def tab_event_update(self):
    #     self.reset_add_texts()
    #     self.reset_edit_texts()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.compressor_thermodynamic_state == {}:
                self.confirm_fluid_attribution()
            else:
                title = "Aditional action required"
                message = "Press the 'Attribute fluid' button to proceed with fluid assignment."
                PrintMessageInput([window_title_2, title, message])
        elif event.key() == Qt.Key_Delete:
            self.confirm_fluid_removal()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.keep_window_open = False