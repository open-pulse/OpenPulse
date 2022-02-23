from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton, QTabWidget, QHeaderView, QWidget
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from time import time

# from PyQt5.uic.uiparser import QtWidgets

from pulse.preprocessing.fluid import Fluid
from pulse.default_libraries import default_fluid_library
from data.user_input.model.setup.pickColorInput import PickColorInput
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput
from data.user_input.model.setup.acoustic.setFluidCompositionInput import SetFluidCompositionInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class FluidInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__()
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/fluidlnput.ui', self)
        
        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_ids = opv.getListPickedLines()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()
        self.compressor_thermodynamic_state = kwargs.get("compressor_thermodynamic_state", {})

        self.fluid_path = project.get_fluid_list_path()

        self.dict_tag_to_entity = self.project.preprocessor.dict_tag_to_entity
        self.REFPROP = None
        self.fluid_data_REFPROP = {}
        self.fluid_name_to_REFPROP_data = {}
        self.clicked_item = None
        self.fluid = None
        self.flagAll = False
        self.flagSelection = False
        self.complete = False

        self.adding = False
        self.editing = False
        self.temp_fluid_color = ""

        self.fluid_data_keys = ["fluid name", 
                                "id", 
                                "color", 
                                "fluid density", 
                                "speed of sound", 
                                "impedance", 
                                "isentropic coefficient", 
                                "thermal conductivity", 
                                "specific heat Cp", 
                                "dynamic viscosity",
                                "temperature",
                                "pressure"]

        self.treeWidget_fluids = self.findChild(QTreeWidget, 'treeWidget_fluids')
        header = self.treeWidget_fluids.headerItem()
        
        fnt = QFont()
        fnt.setPointSize(11)
        fnt.setBold(True)
        # fnt.setItalic(True)
        fnt.setFamily("Arial")

        for col_index, width in enumerate([140, 50, 80, 170, 180, 172]):
            self.treeWidget_fluids.setColumnWidth(col_index, width)
            header.setFont(col_index, fnt)
            # header.setBackground(col_index, QBrush(QColor(200, 200, 200)))
            # header.setForeground(col_index, QBrush(QColor(200, 200, 200)))
        for col_index in [6,7,8,9]:
            self.treeWidget_fluids.hideColumn(col_index)
        #
        self.treeWidget_fluids.itemClicked.connect(self.on_click_item)
        self.treeWidget_fluids.itemDoubleClicked.connect(self.on_doubleclick_item)
        #
        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_id = self.findChild(QLineEdit, 'lineEdit_id')
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
        self.lineEdit_name_remove = self.findChild(QLineEdit, 'lineEdit_name_remove')
        self.lineEdit_id_remove = self.findChild(QLineEdit, 'lineEdit_id_remove')
        self.lineEdit_color_remove = self.findChild(QLineEdit, 'lineEdit_color_remove')
        self.lineEdit_fluid_density_remove = self.findChild(QLineEdit, 'lineEdit_fluid_density_remove')
        self.lineEdit_speed_of_sound_remove = self.findChild(QLineEdit, 'lineEdit_speed_of_sound_remove')
        self.lineEdit_impedance_remove = self.findChild(QLineEdit, 'lineEdit_impedance_remove')
        self.lineEdit_isentropic_exponent_remove = self.findChild(QLineEdit, 'lineEdit_isentropic_exponent_remove')
        self.lineEdit_thermal_conductivity_remove = self.findChild(QLineEdit, 'lineEdit_thermal_conductivity_remove')
        self.lineEdit_specific_heat_Cp_remove = self.findChild(QLineEdit, 'lineEdit_specific_heat_Cp_remove')
        self.lineEdit_dynamic_viscosity_remove = self.findChild(QLineEdit, 'lineEdit_dynamic_viscosity_remove') 
        self.lineEdit_temperature_remove = self.findChild(QLineEdit, 'lineEdit_temperature_remove')
        self.lineEdit_pressure_remove = self.findChild(QLineEdit, 'lineEdit_pressure_remove')   
        #
        self.create_lists_of_lineEdit()

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')

        if self.lines_ids != []:
            self.write_lines(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)
            self.radioButton_all.setChecked(True)

        self.pushButton_pickColor_add_user_defined = self.findChild(QPushButton, 'pushButton_pickColor_add_user_defined')
        self.pushButton_pickColor_add_user_defined.clicked.connect(self.pick_color_add_user_defined)

        self.pushButton_pickColor_add_refprop = self.findChild(QPushButton, 'pushButton_pickColor_add_refprop')
        self.pushButton_pickColor_add_refprop.clicked.connect(self.pick_color_add_refprop)
        
        self.pushButton_pickColor_edit = self.findChild(QPushButton, 'pushButton_pickColor_edit')
        self.pushButton_pickColor_edit.clicked.connect(self.pick_color_edit)

        self.pushButton_confirm_add_fluid = self.findChild(QPushButton, 'pushButton_confirm_add_fluid')
        self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)

        self.pushButton_confirm_add_fluid_rp = self.findChild(QPushButton, 'pushButton_confirm_add_fluid_rp')
        self.pushButton_confirm_add_fluid_rp.clicked.connect(self.check_add_fluid_refprop)

        self.pushButton_reset_entries_add_fluid = self.findChild(QPushButton, 'pushButton_reset_entries_add_fluid')
        self.pushButton_reset_entries_add_fluid.clicked.connect(self.reset_add_texts)

        # self.pushButton_reset_entries_add_fluid_rp = self.findChild(QPushButton, 'pushButton_reset_entries_add_fluid_rp')
        # self.pushButton_reset_entries_add_fluid_rp.clicked.connect(self.reset_add_texts_rp)

        self.pushButton_call_refprop = self.findChild(QPushButton, 'pushButton_call_refprop')
        self.pushButton_call_refprop.clicked.connect(self.call_refprop_interface)

        self.pushButton_confirm_fluid_edition = self.findChild(QPushButton, 'pushButton_confirm_fluid_edition')
        self.pushButton_confirm_fluid_edition.clicked.connect(self.check_edit_fluid)

        self.pushButton_confirm_fluid_removal = self.findChild(QPushButton, 'pushButton_confirm_fluid_removal')
        self.pushButton_confirm_fluid_removal.clicked.connect(self.confirm_fluid_removal)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_fluid_attribution)

        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)

        self.pushButton_edit_fluid_in_refprop = self.findChild(QPushButton, 'pushButton_edit_fluid_in_refprop')
        self.pushButton_edit_fluid_in_refprop.clicked.connect(self.edit_REFPROP_fluid)
        self.pushButton_edit_fluid_in_refprop.setVisible(False)

        self.tabWidget_fluid = self.findChild(QTabWidget, 'tabWidget_fluid')
        # self.tabWidget_fluid.currentChanged.connect(self.tab_event_update)

        self.tabWidget_add = self.findChild(QTabWidget, 'tabWidget_add')
        self.tab_user_defined = self.tabWidget_add.findChild(QWidget, 'tab_user_defined')
        self.tab_refprop_button = self.tabWidget_add.findChild(QWidget, 'tab_refprop_button')
        self.tab_refprop_all_entries = self.tabWidget_add.findChild(QWidget, 'tab_refprop_all_entries')
        self.tabWidget_add.removeTab(2)
        
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()

        self.loadList()
        if self.compressor_thermodynamic_state:
            self.check_compressor_inputs()
        self.exec_()

    def edit_REFPROP_fluid(self):
        self.REFPROP = SetFluidCompositionInput(self.project, self.opv, selected_fluid_to_edit=self.selected_REFPROP_fluid)
        self.after_get_fluid_properties_from_REFPROP()

    def call_refprop_interface(self):
        self.REFPROP = SetFluidCompositionInput(self.project, self.opv)
        self.after_get_fluid_properties_from_REFPROP()

    def after_get_fluid_properties_from_REFPROP(self):
        if self.REFPROP.complete:
            self.tabWidget_add.removeTab(1)
            self.tabWidget_add.addTab(self.tab_refprop_all_entries, "REFPROP")
            self.tabWidget_add.setCurrentIndex(1)
            self.fluid_data_REFPROP = self.REFPROP.fluid_properties
            self.fluid_setup = self.REFPROP.fluid_setup
            for index, key in enumerate(self.fluid_data_keys):
                data = self.fluid_data_REFPROP[key]
                if isinstance(data, float):
                    if key in ["thermal conductivity", "dynamic viscosity"]:
                        _data = round(data, 9)
                    elif key in ["temperature", "pressure"]:
                        _data = round(data, 4)
                    else:
                        _data = round(data, 6)
                self.list_add_lineEdit_rp[index].setText(str(_data))

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
            str_color = str(read.color)[1:-1]
            self.lineEdit_color.setText(str_color)

    def pick_color_add_refprop(self):
        read = PickColorInput()
        if read.complete:
            str_color = str(read.color)[1:-1]
            self.lineEdit_color_rp.setText(str_color)

    def pick_color_edit(self):
        read = PickColorInput()
        if read.complete:
            str_color = str(read.color)[1:-1]
            self.lineEdit_color_edit.setText(str_color)

    # def tab_event_update(self):
    #     self.reset_add_texts()
    #     self.reset_edit_texts()
    #     self.reset_remove_texts()

    def update(self):
        self.lines_ids = self.opv.getListPickedLines()
        if self.lines_ids != []:
            self.write_lines(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(False)

    def write_lines(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_selected_ID.setText(text)

    def create_lists_of_lineEdit(self):
        self.list_add_lineEdit = [  self.lineEdit_name,
                                    self.lineEdit_id,
                                    self.lineEdit_color,
                                    self.lineEdit_fluid_density,
                                    self.lineEdit_speed_of_sound,
                                    self.lineEdit_impedance,
                                    self.lineEdit_isentropic_exponent,
                                    self.lineEdit_thermal_conductivity,
                                    self.lineEdit_specific_heat_Cp,
                                    self.lineEdit_dynamic_viscosity,
                                    self.lineEdit_temperature,
                                    self.lineEdit_pressure ]  

        self.list_add_lineEdit_rp = [   self.lineEdit_name_rp,
                                        self.lineEdit_id_rp,
                                        self.lineEdit_color_rp,
                                        self.lineEdit_fluid_density_rp,
                                        self.lineEdit_speed_of_sound_rp,
                                        self.lineEdit_impedance_rp,
                                        self.lineEdit_isentropic_exponent_rp,
                                        self.lineEdit_thermal_conductivity_rp,
                                        self.lineEdit_specific_heat_Cp_rp,
                                        self.lineEdit_dynamic_viscosity_rp,
                                        self.lineEdit_temperature_rp,
                                        self.lineEdit_pressure_rp   ]  

        self.list_edit_lineEdit = [ self.lineEdit_name_edit,
                                    self.lineEdit_id_edit,
                                    self.lineEdit_color_edit,
                                    self.lineEdit_fluid_density_edit,
                                    self.lineEdit_speed_of_sound_edit,
                                    self.lineEdit_impedance_edit,
                                    self.lineEdit_isentropic_exponent_edit,
                                    self.lineEdit_thermal_conductivity_edit,
                                    self.lineEdit_specific_heat_Cp_edit,
                                    self.lineEdit_dynamic_viscosity_edit,
                                    self.lineEdit_temperature_edit,
                                    self.lineEdit_pressure_edit ]  
        
        self.list_remove_lineEdit = [   self.lineEdit_name_remove,
                                        self.lineEdit_id_remove,
                                        self.lineEdit_color_remove,
                                        self.lineEdit_fluid_density_remove,
                                        self.lineEdit_speed_of_sound_remove,
                                        self.lineEdit_impedance_remove,
                                        self.lineEdit_isentropic_exponent_remove,
                                        self.lineEdit_thermal_conductivity_remove,
                                        self.lineEdit_specific_heat_Cp_remove,
                                        self.lineEdit_dynamic_viscosity_remove,
                                        self.lineEdit_temperature_remove,
                                        self.lineEdit_pressure_remove ]  

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_fluid_attribution()
        elif event.key() == Qt.Key_Escape:
            self.close() 

    def check_compressor_inputs(self):
        if self.compressor_thermodynamic_state:

            width = 800
            height = 720

            self.setMinimumWidth(width)
            self.setMinimumHeight(height)
            self.setMaximumWidth(width)
            self.setMaximumHeight(height)

            self.tabWidget_fluid.removeTab(1)
            self.tabWidget_fluid.removeTab(1)
            self.tabWidget_fluid.removeTab(1)

            self.pushButton_confirm_add_fluid.setText("Attribute fluid")
            self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)
            self.pushButton_confirm.clicked.connect(self.confirm_fluid_attribution)

            self.radioButton_selected_lines.setChecked(True)
            self.radioButton_selected_lines.setDisabled(True)
            self.radioButton_all.setDisabled(True)

            self.connection_type = self.compressor_thermodynamic_state['connection_type']
            self.temperature_comp = self.compressor_thermodynamic_state['temperature']
            self.pressure_comp = self.compressor_thermodynamic_state['pressure']
            self.line_id_comp = self.compressor_thermodynamic_state['line_id']

            self.write_lines(self.line_id_comp)
            self.lineEdit_selected_ID.setDisabled(True)

            temperature_lineEdits = [   self.lineEdit_temperature_rp, self.lineEdit_temperature, self.lineEdit_temperature_edit   ]
            pressure_lineEdits = [  self.lineEdit_pressure_rp, self.lineEdit_pressure, self.lineEdit_pressure_edit  ]

            for temperature_lineEdit in temperature_lineEdits:
                temperature_lineEdit.setText(str(round(self.temperature_comp,4)))
                temperature_lineEdit.setDisabled(True)

            for pressure_lineEdit in pressure_lineEdits:
                pressure_lineEdit.setText(str(round(self.pressure_comp,4)))
                pressure_lineEdit.setDisabled(True)

            self.treeWidget_fluids.setDisabled(True)

    def check_input_name(self, name_string):
        if name_string == "":
            title = 'Empty fluid name'
            message = "Please, insert a valid fluid name."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            if self.adding:
                if name_string in self.list_names:
                    title = 'Invalid fluid name'
                    message = "Please, inform a different fluid name. It is already being used by other fluid!"
                    PrintMessageInput([title, message, window_title1])
                    return True

                if self.lineEdit_temperature_rp.text() != "":
                    _temperature = self.lineEdit_temperature_rp.text()
                    name_string += f" @ {_temperature}K"
                if self.lineEdit_pressure_rp.text() != "":
                    _pressure = self.lineEdit_pressure_rp.text()
                    name_string += f" & {_pressure}Pa"

            self.dict_inputs['name'] = name_string
        
    def check_input_fluid_id(self, id_string):
        if id_string == "":
            title = 'Empty fluid ID'
            message = "Please, insert a valid fluid ID."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            try:
                self.fluid_id = int(id_string)
                if self.adding:
                    if self.fluid_id in self.list_ids:
                        title = 'Invalid fluid name'
                        message = "Please, inform a different fluid ID. It is already being used by other fluid."
                        PrintMessageInput([title, message, window_title1])
                        return True
                      
            except Exception as log_error:
                title = "Invalid fluid ID"
                message = str(log_error)
                PrintMessageInput([title, message, window_title1])
                return True
            self.dict_inputs['identifier'] = id_string
    
    def check_input_color(self, color_string):
        if color_string == "":
            title = "Empty 'r, g, b' color"
            message = "Please, insert a valid 'r, g, b' color to the fluid."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            
            message = " Invalid color RGB input! You must input: [value1, value2, value3] \nand the values must be inside [0, 255] interval."
            try:
                self.colorRGB = getColorRGB(color_string)
                title = "Invalid 'r, g, b' color"
                message_color = (" The RGB color {} was already used.\n Please, input a different color.").format(self.colorRGB)

                if len(self.colorRGB)!=3:
                    PrintMessageInput([title, message, window_title1])
                    return True

                if self.editing:
                    temp_colorRGB = getColorRGB(self.temp_fluid_color)
                    if temp_colorRGB != self.colorRGB:
                        if self.colorRGB in self.list_colors:
                            PrintMessageInput([title, message_color, window_title1])
                            return True 
                        else:
                            self.list_colors.remove(temp_colorRGB)
                            
                elif self.adding:
                    if self.colorRGB in self.list_colors:
                        PrintMessageInput([title, message_color, window_title1])
                        return True

            except Exception as log_error:
                message = str(log_error)
                PrintMessageInput([title, message, window_title1])
                return True
            self.dict_inputs['color'] = color_string
       
    def check_element_type_of_lines(self):

        self.flag_all_fluid_inputs = False

        if self.flagSelection:
            
            lineEdit = self.lineEdit_selected_ID.text()
            self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
            if self.stop:
                return True

            for line in self.lines_typed:
                _line = self.dict_tag_to_entity[line]
                if _line.acoustic_element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                    self.flag_all_fluid_inputs = True 
                    break
          
        elif self.flagAll:
            for line in self.project.preprocessor.all_lines:
                _line = self.dict_tag_to_entity[line]
                if _line.acoustic_element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                    self.flag_all_fluid_inputs = True
                    break
        
        return False

    def check_input_parameters(self, input_string, label, _float=True, allow_empty_entry=True):
        title = "INPUT ERROR"
        value_string = input_string
        if value_string != "":
            try:
                if _float:
                    value = float(value_string)
                else:
                    value = int(value_string) 
                if value < 0:
                    message = "You cannot input a negative value to the {}.".format(label)
                    PrintMessageInput([title, message, window_title1])
                    return True
                else:
                    self.value = value
            except Exception:
                message = "You have typed an invalid value to the {}.".format(label)
                PrintMessageInput([title, message, window_title1])
                return True
        else:
            self.value = None
            if allow_empty_entry:
                return False
            else:
                message = f"An empty entry has been detected at the '{label}' input field. You should insert a valid entry to proceed."
                PrintMessageInput([title, message, window_title1])
                return True

    def check_all_inputs(self):

        self.incomplete_inputs = False

        if self.check_input_parameters(self.fluid_density_string, 'fluid density'):
            return True
        else:
            fluid_density = self.value
            if fluid_density > 2000:
                title = "Invalid density value"
                message = "The input value for fluid density must be a positive number less than 2000."
                PrintMessageInput([title, message, window_title1])
                return False
            self.dict_inputs['fluid density'] = fluid_density

        if self.check_input_parameters(self.speed_of_sound_string, 'speed of sound'):
            return True
        else:
            speed_of_sound = self.value
            self.dict_inputs['speed of sound'] = speed_of_sound

            impedance = round(fluid_density*speed_of_sound, 4)
            impedance_string = str(fluid_density*speed_of_sound)
            if self.adding:
                if self.lineEdit_impedance_rp.text() == "":
                    self.lineEdit_impedance.setText(impedance_string)
            elif self.editing:
                self.lineEdit_impedance_edit.setText(impedance_string)
            self.dict_inputs['impedance'] = impedance
        
        self.list_empty_inputs = []

        if self.isentropic_exponent_string != "":     
            if self.check_input_parameters(self.isentropic_exponent_string, 'isentropic exponent'):
                return True
            else:
                isentropic_exponent = self.value
                self.dict_inputs['isentropic exponent'] = isentropic_exponent
        else:
            self.list_empty_inputs.append('isentropic exponent')
            self.incomplete_inputs = True

        if self.thermal_conductivity_string != "":    
            if self.check_input_parameters(self.thermal_conductivity_string, 'thermal conductivity'):
                return True
            else:
                thermal_conductivity = self.value 
                self.dict_inputs['thermal conductivity'] = thermal_conductivity
        else:
            self.list_empty_inputs.append('thermal conductivity')
            self.incomplete_inputs = True

        if self.specific_heat_Cp_string != "":
            if self.check_input_parameters(self.specific_heat_Cp_string, 'specific heat Cp'):
                return True
            else:
                specific_heat_Cp = self.value 
                self.dict_inputs['specific heat Cp'] = specific_heat_Cp
        else:
            self.list_empty_inputs.append('specific heat Cp')
            self.incomplete_inputs = True

        if self.dynamic_viscosity_string != "":           
            if self.check_input_parameters(self.dynamic_viscosity_string, 'dinamic viscosity'):
                return True
            else:
                dynamic_viscosity = self.value 
                self.dict_inputs['dynamic viscosity'] = dynamic_viscosity
        else:
            self.list_empty_inputs.append('dynamic viscosity')
            self.incomplete_inputs = True
        
        if self.check_input_parameters(self.temperature_string, 'temperature', allow_empty_entry=False):
            return True
        else:
            temperature = self.value
            self.dict_inputs['temperature'] = temperature
    
        if self.check_input_parameters(self.pressure_string, 'pressure', allow_empty_entry=False):
            return True
        else:
            pressure = self.value
            self.dict_inputs['pressure'] = pressure

        if self.lineEdit_temperature_rp.text() != "":
            if 'temperature' in self.fluid_data_REFPROP.keys():
                self.dict_inputs['temperature'] = self.fluid_data_REFPROP["temperature"]

        if self.lineEdit_pressure_rp.text() != "":
            if 'pressure' in self.fluid_data_REFPROP.keys():
                self.dict_inputs['pressure'] = self.fluid_data_REFPROP["pressure"]   

        if self.REFPROP is not None:
            [key_mixture, molar_fractions] = self.fluid_setup
            self.dict_inputs['key mixture'] = key_mixture
            self.dict_inputs['molar fractions'] = molar_fractions

        if self.incomplete_inputs:
            self.all_fluid_properties_message()

    def check_add_edit(self, parameters):

        [   name_string, id_string, color_string,
            self.fluid_density_string,
            self.speed_of_sound_string,
            self.impedance_string,
            self.isentropic_exponent_string,
            self.thermal_conductivity_string,
            self.specific_heat_Cp_string,
            self.dynamic_viscosity_string, 
            self.temperature_string,
            self.pressure_string  ] = parameters

        self.dict_inputs = {}

        if self.check_input_name(name_string):
            return True           

        if self.check_input_fluid_id(id_string):
            return True

        if self.check_input_color(color_string):
            return True

        if self.check_all_inputs():
            # self.list_names.remove(name_string)
            # self.list_ids.remove(self.fluid_id)
            # self.list_colors.remove(self.colorRGB)
            return True
        
        if name_string not in self.list_names:
            self.list_names.append(name_string)

        if self.fluid_id not in self.list_ids:
            self.list_ids.append(self.fluid_id)

        if self.colorRGB not in self.list_colors:
            self.list_colors.append(self.colorRGB)

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
            PrintMessageInput([title, message, window_title1])
            return True

        if self.adding or self.editing:    
            self.treeWidget_fluids.clear()
            self.loadList()
            self.adding = False
            self.editing = False
            self.reset_edit_texts()

    def confirm_fluid_attribution(self):

        if self.compressor_thermodynamic_state:
            self.clicked_item = self.treeWidget_fluids.topLevelItem(len(self.sections))

        if self.clicked_item is None:
            title = "Empty fluid selection"
            message = "Select a fluid in the list before trying to attribute a fluid to the lines."
            PrintMessageInput([title, message, window_title1])
            return
        
        if self.check_element_type_of_lines():
            return
        
        try:
            isentropic_exponent = None
            thermal_conductivity = None
            specific_heat_Cp = None
            dynamic_viscosity = None
            list_empty_inputs = []

            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            color = self.clicked_item.text(2)
            fluid_density = float(self.clicked_item.text(3))
            speed_of_sound = float(self.clicked_item.text(4))
            
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
                PrintMessageInput([title, message, window_title1]) 
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
                # self.opv.changeColorEntities(self.lines_ids, self.fluid.getNormalizedColorRGB())

            elif self.flagAll:
                lines = self.project.preprocessor.all_lines
                print("[Set Fluid] - {} defined at all lines.".format(self.fluid.name))
                # self.opv.changeColorEntities(lines, self.fluid.getNormalizedColorRGB())

            self.project.set_fluid_by_lines(lines, self.fluid)
            self.complete = True
            self.close()

        except Exception as log_error:
            title = "Error with the fluid list data"
            message = str(log_error)
            PrintMessageInput([title, message, window_title1])
            return

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

                name = str(rFluid['name'])
                identifier =  str(rFluid['identifier'])
                color =  str(rFluid['color'])
                fluid_density =  str(rFluid['fluid density'])
                speed_of_sound =  str(rFluid['speed of sound'])
                impedance =  str(rFluid['impedance'])

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
                    molar_fractions = self.project.file._get_list_of_values_from_string(str_molar_fractions, are_values_int=False)

                if not None in [temperature, pressure, key_mixture, molar_fractions]:
                    self.fluid_name_to_REFPROP_data[name] = [name, temperature, pressure, key_mixture, molar_fractions]

                load_fluid = QTreeWidgetItem([  name, 
                                                identifier, 
                                                color, 
                                                fluid_density, 
                                                speed_of_sound, 
                                                impedance,
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
                load_fluid.setBackground(2, QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_fluid.setForeground(2, QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                for i in range(6):
                    load_fluid.setTextAlignment(i, Qt.AlignCenter)
                    # load_fluid.setForeground(i, QColor(0,0,0))
                self.treeWidget_fluids.addTopLevelItem(load_fluid)

        except Exception as log_error:
            title = "Error while loading the fluid list data"
            message = str(log_error)
            PrintMessageInput([title, message, window_title1])
            self.close()
        
    def check_add_fluid(self):
        parameters = []
        for lineEdit in self.list_add_lineEdit:
            parameters.append(lineEdit.text())
        self.adding = True
        self.editing = False
        self.check_add_edit( parameters )

    def check_add_fluid_refprop(self):
        parameters = []
        for lineEdit in self.list_add_lineEdit_rp:
            parameters.append(lineEdit.text())
        self.adding = True
        self.editing = False
        if not self.check_add_edit( parameters ):
            self.reset_add_texts_rp()
    
    def all_fluid_properties_message(self):
        title = "WARNING - EMPTY ENTRIES IN FLUID INPUTS"
        message = "You should input all fluid properties if you are going to use the following acoustic element types: "
        message += "wide-duct, LRF fluid equivalent and LRF full." 
        message += "\n\nEmpty entries:\n"
        for label in self.list_empty_inputs:
            message += "\n{}".format(label)
        PrintMessageInput([title, message, window_title2])

    def hightlight(self):
        self.treeWidget_fluids.setStyleSheet("color:rgb(0, 0, 255)")
        self.treeWidget_fluids.setLineWidth(2)

    def remove_hightlight(self):
        self.treeWidget_fluids.setStyleSheet("color:rgb(0, 0, 0)")
        self.treeWidget_fluids.setLineWidth(1)
    #     t0 = time()
    #     dt = 0
    #     while dt < 2:
    #         dt = time() - t0
    #     self.treeWidget_fluids.setStyleSheet("color:rgb(0, 0, 0)")
    #     self.treeWidget_fluids.setLineWidth(1)

    def check_edit_fluid(self):
        if self.lineEdit_name_edit.text() == "":
            title = "Empty fluid selection"
            message = "Please, select a fluid in the list to be edited."
            PrintMessageInput([title, message, window_title2])
            self.hightlight()
            return
        parameters = []
        for lineEdit in self.list_edit_lineEdit:
            parameters.append(lineEdit.text())
        self.adding = False
        self.editing = True
        self.remove_hightlight()
        self.check_add_edit( parameters )    

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()
        if self.flagSelection:
            self.lineEdit_selected_ID.setEnabled(True)
            self.lines_ids = self.opv.getListPickedLines()
            if self.lines_ids != []:
                self.write_lines(self.lines_ids)
            else:
                self.lineEdit_selected_ID.setText("")
        elif self.flagAll:
            self.lineEdit_selected_ID.setEnabled(False)
            self.lineEdit_selected_ID.setText("All lines")

    def on_click_item(self, item):
        # self.current_index = self.tabWidget_fluid.currentIndex()
        self.tabWidget_add.setCurrentIndex(0)
        self.pushButton_edit_fluid_in_refprop.setVisible(False)
        self.clicked_item = item
        N = len(self.list_add_lineEdit)

        for i in range(N):
            self.list_add_lineEdit[i].setText(item.text(i))
            self.list_edit_lineEdit[i].setText(item.text(i))
            self.list_remove_lineEdit[i].setText(item.text(i))
        
        self.temp_fluid_color = item.text(2)   

        fluid_name = item.text(0)
        self.tabWidget_add.removeTab(1)
        self.tabWidget_add.addTab(self.tab_refprop_button, "REFPROP")

        if fluid_name in self.fluid_name_to_REFPROP_data.keys():
            self.tabWidget_add.setCurrentIndex(1)
            self.pushButton_edit_fluid_in_refprop.setVisible(True)
            self.selected_REFPROP_fluid = self.fluid_name_to_REFPROP_data[fluid_name]   
        else:
            self.tabWidget_add.setCurrentIndex(0)

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.confirm_fluid_attribution()
    
    def confirm_fluid_removal(self):
        self.adding = False
        self.editing = False
        try:

            if self.lineEdit_name_remove.text() == "":
                title = "Empty fluid selection"
                message = "Please, select a fluid in the list before confirm the removal."
                PrintMessageInput([title, message, window_title2])
                self.hightlight()
                return

            else:
                config = configparser.ConfigParser()
                config.read(self.fluid_path)
                config.remove_section(self.lineEdit_name_remove.text())
                with open(self.fluid_path, 'w') as config_file:
                    config.write(config_file)

                for tag, line in self.dict_tag_to_entity.items():
                    if line.fluid is not None:
                        if line.fluid.name == self.lineEdit_name_remove.text():
                            self.project.set_fluid_by_lines(tag, None)

                self.treeWidget_fluids.clear()
                self.clicked_item = None
                self.loadList()
                self.reset_remove_texts() 
                self.remove_hightlight()

        except Exception as log_error:
            title = "Error with the material removal"
            message = str(log_error)
            PrintMessageInput([title, message, window_title1])

    def reset_library_to_default(self):

        title = "Resetting of fluids library"
        message = "Do you really want to reset the fluid library to default values?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        read = CallDoubleConfirmationInput(title, message, leftButton_label='Cancel', rightButton_label='Proceed')

        if read._doNotRun:
            return

        if read._continue:
            default_fluid_library(self.fluid_path)
            self.treeWidget_fluids.clear()
            self.loadList()
            self.reset_add_texts()
            self.reset_edit_texts() 
            self.reset_remove_texts() 
    
    def reset_add_texts(self):
        for lineEdit in self.list_add_lineEdit:
            lineEdit.setText("")

    def reset_add_texts_rp(self):
        for lineEdit in self.list_add_lineEdit_rp:
            lineEdit.setText("")
        self.tabWidget_add.removeTab(1)
        self.tabWidget_add.addTab(self.tab_refprop_button, "REFPROP")

    def reset_edit_texts(self):
        for lineEdit in self.list_edit_lineEdit:
            lineEdit.setText("")

    def reset_remove_texts(self):
        for lineEdit in self.list_remove_lineEdit:
            lineEdit.setText("")