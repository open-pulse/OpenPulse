from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton, QTabWidget, QHeaderView
from PyQt5.QtGui import QIcon, QColor, QBrush, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from time import time

from pulse.preprocessing.fluid import Fluid
from pulse.default_libraries import default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"


def getColorRGB(color):
    temp = color[1:-1]
    tokens = temp.split(',')
    return list(map(int, tokens))

class FluidInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Model/Setup/Acoustic/fluidlnput.ui', self)
        
        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_ids = opv.getListPickedEntities()

        self.project = project
        self.mesh = project.mesh
        self.before_run = self.mesh.get_model_checks()

        self.fluid_path = project.get_fluid_list_path()

        self.dict_tag_to_entity = self.project.mesh.dict_tag_to_entity
        self.clicked_item = None
        self.fluid = None
        self.flagAll = False
        self.flagSelection = False

        self.adding = False
        self.editing = False
        self.temp_fluid_color = ""

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

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_fluid_attribution)

        self.pushButton_confirm_add_fluid = self.findChild(QPushButton, 'pushButton_confirm_add_fluid')
        self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)

        self.pushButton_reset_entries_add_fluid = self.findChild(QPushButton, 'pushButton_reset_entries_add_fluid')
        self.pushButton_reset_entries_add_fluid.clicked.connect(self.reset_add_texts)

        self.pushButton_confirm_fluid_edition = self.findChild(QPushButton, 'pushButton_confirm_fluid_edition')
        self.pushButton_confirm_fluid_edition.clicked.connect(self.check_edit_fluid)

        self.pushButton_confirm_fluid_removal = self.findChild(QPushButton, 'pushButton_confirm_fluid_removal')
        self.pushButton_confirm_fluid_removal.clicked.connect(self.confirm_fluid_removal)

        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)

        self.tabWidget_fluid = self.findChild(QTabWidget, 'tabWidget_fluid')
        # self.tabWidget_fluid.currentChanged.connect(self.tab_event_update)
        
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelection = self.radioButton_selected_lines.isChecked()

        self.loadList()
        self.exec_()

    # def tab_event_update(self):
    #     self.reset_add_texts()
    #     self.reset_edit_texts()
    #     self.reset_remove_texts()

    def update(self):
        self.lines_ids = self.opv.getListPickedEntities()
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
                                    self.lineEdit_dynamic_viscosity ]  

        self.list_edit_lineEdit = [ self.lineEdit_name_edit,
                                    self.lineEdit_id_edit,
                                    self.lineEdit_color_edit,
                                    self.lineEdit_fluid_density_edit,
                                    self.lineEdit_speed_of_sound_edit,
                                    self.lineEdit_impedance_edit,
                                    self.lineEdit_isentropic_exponent_edit,
                                    self.lineEdit_thermal_conductivity_edit,
                                    self.lineEdit_specific_heat_Cp_edit,
                                    self.lineEdit_dynamic_viscosity_edit ]  
        
        self.list_remove_lineEdit = [   self.lineEdit_name_remove,
                                        self.lineEdit_id_remove,
                                        self.lineEdit_color_remove,
                                        self.lineEdit_fluid_density_remove,
                                        self.lineEdit_speed_of_sound_remove,
                                        self.lineEdit_impedance_remove,
                                        self.lineEdit_isentropic_exponent_remove,
                                        self.lineEdit_thermal_conductivity_remove,
                                        self.lineEdit_specific_heat_Cp_remove,
                                        self.lineEdit_dynamic_viscosity_remove ]  

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_fluid_attribution()
        elif event.key() == Qt.Key_Escape:
            self.close() 

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
                      
            except Exception as err:
                title = "Invalid fluid ID"
                message = str(err)
                PrintMessageInput([title, message, window_title1])
                return True
            self.dict_inputs['identifier'] = id_string
    
    def check_input_color(self, color_string):
        if color_string == "":
            title = 'Empty [r,g,b] color'
            message = "Please, insert a valid [r,g,b] color to the fluid."
            PrintMessageInput([title, message, window_title1])
            return True
        else:
            
            message = " Invalid color RGB input! You must input: [value1, value2, value3] \nand the values must be inside [0, 255] interval."
            try:
                self.colorRGB = getColorRGB(color_string)
                message_color = (" The RGB color {} was already used.\n Please, input a different color.").format(self.colorRGB)

                if len(self.colorRGB)!=3:
                    title = 'Invalid [r,g,b] color'
                    PrintMessageInput([title, message, window_title1])
                    return True

                if self.editing:
                    temp_colorRGB = getColorRGB(self.temp_fluid_color)
                    if temp_colorRGB != self.colorRGB:
                        if self.colorRGB in self.list_colors:
                            title = 'Invalid [r,g,b] color'
                            PrintMessageInput([title, message_color, window_title1])
                            return True 
                        else:
                            self.list_colors.remove(temp_colorRGB)
                            
                elif self.adding:
                    if self.colorRGB in self.list_colors:
                        title = 'Invalid [r,g,b] color'
                        PrintMessageInput([title, message_color, window_title1])
                        return True

            except Exception as err:
                title = 'Invalid [r,g,b] color'
                message = str(err)
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
            for line in self.project.mesh.all_lines:
                _line = self.dict_tag_to_entity[line]
                if _line.acoustic_element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                    self.flag_all_fluid_inputs = True
                    break
        
        return False

    def check_input_parameters(self, input_string, label, _float=True):
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
        return False

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

            impedance = fluid_density*speed_of_sound
            impedance_string = str(fluid_density*speed_of_sound)
            if self.adding:
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
            self.dynamic_viscosity_string  ] = parameters

        self.dict_inputs = {}

        if self.check_input_name(name_string):
            return

        if self.check_input_fluid_id(id_string):
            return

        if self.check_input_color(color_string):
            return

        if name_string not in self.list_names:
            self.list_names.append(name_string)

        if self.fluid_id not in self.list_ids:
            self.list_ids.append(self.fluid_id)

        if self.colorRGB not in self.list_colors:
            self.list_colors.append(self.colorRGB)

        if self.check_all_inputs():
            return
        
        try:
            config = configparser.ConfigParser()
            config.read(self.fluid_path)
            config[name_string.upper()] = self.dict_inputs

            with open(self.fluid_path, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as err:
            title = "Error while saving the fluid data to the file"
            message = str(err)
            PrintMessageInput([title, message, window_title1])
            return

        if self.adding or self.editing:    
            self.treeWidget_fluids.clear()
            self.loadList()
            self.adding = False
            self.editing = False
            self.reset_edit_texts()

    def confirm_fluid_attribution(self):

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
                                dynamic_viscosity = dynamic_viscosity )

            if self.flagSelection:

                if self.lineEdit_selected_ID.text() == "":
                    return

                for line in self.lines_ids:
                    self.project.set_fluid_by_line(line, self.fluid)
                    
                print("[Set Fluid] - {} defined at lines: {}".format(self.fluid.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_ids, self.fluid.getNormalizedColorRGB())

            elif self.flagAll:

                self.project.set_fluid_to_all_lines(self.fluid)
                lines = self.project.mesh.all_lines

                print("[Set Fluid] - {} defined at all lines.".format(self.fluid.name))
                # self.opv.changeColorEntities(lines, self.fluid.getNormalizedColorRGB())

            self.close()

        except Exception as err:
            title = "Error with the fluid list data"
            message = str(err)
            PrintMessageInput([title, message, window_title1])
            return

    def loadList(self):

        self.list_names = []
        self.list_ids = []
        self.list_colors = []     

        try:
            config = configparser.ConfigParser()
            config.read(self.fluid_path)

            for fluid in config.sections():

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
                
                load_fluid = QTreeWidgetItem([  name, 
                                                identifier, 
                                                color, 
                                                fluid_density, 
                                                speed_of_sound, 
                                                impedance,
                                                isentropic_exponent,
                                                thermal_conductivity,
                                                specific_heat_Cp,
                                                dynamic_viscosity  ])
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

        except Exception as err:
            title = "Error while loading the fluid list data"
            message = str(err)
            PrintMessageInput([title, message, window_title1])
            self.close()
        
    def check_add_fluid(self):
        parameters = []
        for lineEdit in self.list_add_lineEdit:
            parameters.append(lineEdit.text())
        self.adding = True
        self.editing = False
        self.check_add_edit( parameters )
    
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
            self.lines_ids = self.opv.getListPickedEntities()
            if self.lines_ids != []:
                self.write_lines(self.lines_ids)
            else:
                self.lineEdit_selected_ID.setText("")
        elif self.flagAll:
            self.lineEdit_selected_ID.setEnabled(False)
            self.lineEdit_selected_ID.setText("All lines")

    def on_click_item(self, item):
        # self.current_index = self.tabWidget_fluid.currentIndex()
        self.clicked_item = item
        N = len(self.list_add_lineEdit)
        for i in range(N):
            self.list_add_lineEdit[i].setText(item.text(i))
            self.list_edit_lineEdit[i].setText(item.text(i))
            self.list_remove_lineEdit[i].setText(item.text(i))
        self.temp_fluid_color = item.text(2)            

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.confirm_fluid_attribution()
    
    def double_confirm_action(self):
        confirm_act = QMessageBox.question(
            self,
            "QUIT",
            "Are you sure you want to reset to default fluids library?",
            QMessageBox.No | QMessageBox.Yes)
        
        if confirm_act == QMessageBox.Yes:
            return False
        else:
            return True

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
                config.remove_section(self.lineEdit_name_remove.text().upper())
                with open(self.fluid_path, 'w') as config_file:
                    config.write(config_file)

                for tag, line in self.dict_tag_to_entity.items():
                    if line.fluid.name == self.lineEdit_name_remove.text():
                        self.project.set_fluid_by_line(tag, None)

                self.treeWidget_fluids.clear()
                self.clicked_item = None
                self.loadList()
                self.reset_remove_texts() 
                self.remove_hightlight()

        except Exception as err:
            title = "Error with the material removal"
            message = str(err)
            PrintMessageInput([title, message, window_title1])

    def reset_library_to_default(self):
        if self.double_confirm_action():
            return
        default_fluid_library(self.fluid_path)
        self.treeWidget_fluids.clear()
        self.loadList()
        self.reset_add_texts()
        self.reset_edit_texts() 
        self.reset_remove_texts() 
    
    def reset_add_texts(self):
        self.lineEdit_name.setText("")
        self.lineEdit_id.setText("")
        self.lineEdit_fluid_density.setText("")
        self.lineEdit_speed_of_sound.setText("")
        self.lineEdit_impedance.setText("")
        self.lineEdit_color.setText("")
        self.lineEdit_isentropic_exponent.setText("")
        self.lineEdit_thermal_conductivity.setText("") 
        self.lineEdit_specific_heat_Cp.setText("") 
        self.lineEdit_dynamic_viscosity.setText("") 

    def reset_edit_texts(self):
        self.lineEdit_name_edit.setText("")
        self.lineEdit_id_edit.setText("")
        self.lineEdit_fluid_density_edit.setText("")
        self.lineEdit_speed_of_sound_edit.setText("")
        self.lineEdit_impedance_edit.setText("")
        self.lineEdit_color_edit.setText("")
        self.lineEdit_isentropic_exponent_edit.setText("")
        self.lineEdit_thermal_conductivity_edit.setText("") 
        self.lineEdit_specific_heat_Cp_edit.setText("") 
        self.lineEdit_dynamic_viscosity_edit.setText("") 

    def reset_remove_texts(self):
        self.lineEdit_name_remove.setText("")
        self.lineEdit_id_remove.setText("")
        self.lineEdit_fluid_density_remove.setText("")
        self.lineEdit_speed_of_sound_remove.setText("")
        self.lineEdit_impedance_remove.setText("")
        self.lineEdit_color_remove.setText("")
        self.lineEdit_isentropic_exponent_remove.setText("")
        self.lineEdit_thermal_conductivity_remove.setText("") 
        self.lineEdit_specific_heat_Cp_remove.setText("") 
        self.lineEdit_dynamic_viscosity_remove.setText("") 