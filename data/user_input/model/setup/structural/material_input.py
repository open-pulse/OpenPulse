from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import configparser
import numpy as np

from pulse.preprocessing.material import Material
from pulse.lib.default_libraries import default_material_library
from data.user_input.model.setup.pickColorInput import PickColorInput
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title = "ERROR"

def getColorRGB(color):
    color = color.replace(" ", "")
    if ("[" or "(") in color:
        color = color[1:-1]
    tokens = color.split(',')
    return list(map(int, tokens))

class MaterialInput(QDialog):
    def __init__(   self, project, opv, cache_selected_lines=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui_files/Model/Setup/Structural/material_input.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_ids = self.opv.getListPickedLines()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_pre_solution_model_checks()

        self.material_path = project.get_material_list_path()
        self.cache_selected_lines = cache_selected_lines

        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()
        self.create_lists_of_lineEdits()
        self.loadList()
        self._loading_info_at_start()    
        self.exec()


    def _reset_variables(self):
        self.clicked_item = None
        self.material = None
        self.flagAll = False
        self.flagSelectedLines = False

        self.adding = False
        self.editing = False
        self.list_names = []
        self.list_ids = []
        self.list_colors = []
        self.temp_material_name = ""
        self.temp_material_id = ""
        self.temp_material_color = ""
        self.dict_inputs = {}


    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_material_id = self.findChild(QComboBox, 'comboBox_material_id')
        # QLineEdit
        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_density = self.findChild(QLineEdit, 'lineEdit_density')
        self.lineEdit_youngModulus = self.findChild(QLineEdit, 'lineEdit_youngModulus')
        self.lineEdit_poisson = self.findChild(QLineEdit, 'lineEdit_poisson')
        self.lineEdit_thermal_expansion_coefficient = self.findChild(QLineEdit, 'lineEdit_thermal_expansion_coefficient')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')
        self.lineEdit_color.setDisabled(True)
        self.lineEdit_color.setStyleSheet("color: rgb(0,0,255); background-color: rbg(255,255,255)")
        self.lineEdit_name_edit = self.findChild(QLineEdit, 'lineEdit_name_edit')
        self.lineEdit_id_edit = self.findChild(QLineEdit, 'lineEdit_id_edit')
        self.lineEdit_density_edit = self.findChild(QLineEdit, 'lineEdit_density_edit')
        self.lineEdit_youngModulus_edit = self.findChild(QLineEdit, 'lineEdit_youngModulus_edit')
        self.lineEdit_poisson_edit = self.findChild(QLineEdit, 'lineEdit_poisson_edit')
        self.lineEdit_thermal_expansion_coefficient_edit = self.findChild(QLineEdit, 'lineEdit_thermal_expansion_coefficient_edit')
        self.lineEdit_color_edit = self.findChild(QLineEdit, 'lineEdit_color_edit')
        self.lineEdit_color_edit.setDisabled(True)
        self.lineEdit_name_edit.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_id_edit.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_color_edit.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_name_remove = self.findChild(QLineEdit, 'lineEdit_name_remove')
        self.lineEdit_id_remove = self.findChild(QLineEdit, 'lineEdit_id_remove')
        self.lineEdit_density_remove = self.findChild(QLineEdit, 'lineEdit_density_remove')
        self.lineEdit_youngModulus_remove = self.findChild(QLineEdit, 'lineEdit_youngModulus_remove')
        self.lineEdit_poisson_remove = self.findChild(QLineEdit, 'lineEdit_poisson_remove')
        self.lineEdit_thermal_expansion_coefficient_remove = self.findChild(QLineEdit, 'lineEdit_thermal_expansion_coefficient_remove')
        self.lineEdit_color_remove = self.findChild(QLineEdit, 'lineEdit_color_remove')
        self.lineEdit_name_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_id_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_density_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_youngModulus_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_poisson_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_thermal_expansion_coefficient_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_color_remove.setStyleSheet("color: rgb(0,0,0); background-color: rbg(255,255,255)")
        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')
        self.lineEdit_selected_material_name = self.findChild(QLineEdit, 'lineEdit_selected_material_name')
        # QPushButton
        self.pushButton_pickColor_add = self.findChild(QPushButton, 'pushButton_pickColor_add')
        self.pushButton_pickColor_edit = self.findChild(QPushButton, 'pushButton_pickColor_edit')
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm_add_material = self.findChild(QPushButton, 'pushButton_confirm_add_material')
        self.pushButton_reset_entries_add_material = self.findChild(QPushButton, 'pushButton_reset_entries_add_material')
        self.pushButton_confirm_material_edition = self.findChild(QPushButton, 'pushButton_confirm_material_edition')
        self.pushButton_confirm_material_removal = self.findChild(QPushButton, 'pushButton_confirm_material_removal')
        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_pickColor_edit.setDisabled(True)
        self.pushButton_confirm_material_edition.setDisabled(True)
        self.pushButton_confirm_material_removal.setDisabled(True)
        # QRadioButton
        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelectedLines = self.radioButton_selected_lines.isChecked()
        # QTabWidget
        self.tabWidget_material = self.findChild(QTabWidget, 'tabWidget_material')
        self.tab_edit_material = self.tabWidget_material.findChild(QWidget, "tab_edit_material")
        self.tab_remove_material = self.tabWidget_material.findChild(QWidget, "tab_remove_material")
        self.currentTab_ = self.tabWidget_material.currentIndex()
        # QTreeWidget
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        widths = [120, 10, 120, 170, 70, 210, 10]
        for i, width in enumerate(widths):
            self.treeWidget.setColumnWidth(i, width)


    def _create_connections(self):
        #
        self.comboBox_material_id.currentIndexChanged.connect(self.get_comboBox_index)
        #
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)
        self.pushButton_confirm_material_removal.clicked.connect(self.confirm_material_removal)
        self.pushButton_confirm_material_edition.clicked.connect(self.check_edit_material)
        self.pushButton_reset_entries_add_material.clicked.connect(self.reset_add_texts)
        self.pushButton_confirm_add_material.clicked.connect(self.check_add_material)
        self.pushButton_confirm.clicked.connect(self.confirm_material_attribution)
        self.pushButton_pickColor_edit.clicked.connect(self.pick_color_edit)
        self.pushButton_pickColor_add.clicked.connect(self.pick_color_add)
        #
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)
        #
        self.tabWidget_material.currentChanged.connect(self.tabEvent_)
        #
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)


    def _loading_info_at_start(self):
        if self.cache_selected_lines != []:
            self.lines_ids = self.cache_selected_lines

        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)

        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)
            self.radioButton_all.setChecked(True) 


    def create_lists_of_lineEdits(self):
        #
        self.list_add_lineEdit = [  self.lineEdit_name,
                                    self.lineEdit_color,
                                    self.lineEdit_density,
                                    self.lineEdit_youngModulus,
                                    self.lineEdit_poisson,
                                    self.lineEdit_thermal_expansion_coefficient  ]  
        #
        self.list_edit_lineEdit = [ self.lineEdit_name_edit,
                                    self.lineEdit_id_edit,
                                    self.lineEdit_color_edit,
                                    self.lineEdit_density_edit,
                                    self.lineEdit_youngModulus_edit,
                                    self.lineEdit_poisson_edit,
                                    self.lineEdit_thermal_expansion_coefficient_edit ]  
        #
        self.list_remove_lineEdit = [   self.lineEdit_name_remove,
                                        self.lineEdit_id_remove,
                                        self.lineEdit_color_remove,
                                        self.lineEdit_density_remove,
                                        self.lineEdit_youngModulus_remove,
                                        self.lineEdit_poisson_remove,
                                        self.lineEdit_thermal_expansion_coefficient_remove   ]  


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_material_attribution()
        elif event.key() == Qt.Key_Delete:
            self.confirm_material_removal()
        elif event.key() == Qt.Key_Escape:
            self.close()


    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)


    def update(self):
        self.lines_ids = self.opv.getListPickedLines()
        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(True)
        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.radioButton_all.setChecked(True)
            self.lineEdit_selected_ID.setEnabled(False)


    def tabEvent_(self):
        self.currentTab_ = self.tabWidget_material.currentIndex()
        if self.currentTab_ == 0:
            self.adding = True
            self.editing = False
        elif self.currentTab_ == 1:
            self.adding = False
            self.editing = True
            if self.clicked_item is not None:
                self.selected_material_to_edit()
        elif self.currentTab_ == 2:
            if self.clicked_item is not None:
                self.selected_material_to_remove()


    def pick_color_add(self):

        read = PickColorInput()
        self.adding = True
        self.editing = False
        if read.complete:
            #
            color = tuple(read.color)
            str_color = str(read.color).replace(" ", "")
            #
            self.lineEdit_color.setText(str_color)
            self.lineEdit_color.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")
            #
            if self.check_color_input(self.lineEdit_color):
                self.lineEdit_color.setText("")
                PrintMessageInput([self.title, self.message, window_title])


    def pick_color_edit(self):
        
        read = PickColorInput()
        self.adding = False
        self.editing = True
        if read.complete:
            #
            color = tuple(read.color)
            str_color = str(read.color).replace(" ", "")
            #
            self.lineEdit_color_edit.setText(str_color)
            self.lineEdit_color_edit.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")
            #
            if self.check_color_input(self.lineEdit_color_edit):
                self.lineEdit_color_edit.setText("")
                PrintMessageInput([self.title, self.message, window_title])


    def confirm_material_attribution(self):

        if self.clicked_item is None:
            self.title = "NO MATERIAL SELECTION"
            self.message = "Select a material in the list before \nconfirming the material attribution."
            PrintMessageInput([self.title, self.message, window_title])
            return
        
        try:

            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            density = float(self.clicked_item.text(2))
            young = float(self.clicked_item.text(3))*(10**(9))
            poisson = float(self.clicked_item.text(4))
            thermal_expansion_coefficient = float(self.clicked_item.text(5))
            color = self.clicked_item.text(6)
            
            new_material = Material(name, 
                                    density,
                                    poisson_ratio = poisson, 
                                    young_modulus = young, 
                                    identifier = identifier, 
                                    thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                    color = color)
            self.material = new_material
            
            if self.flagSelectedLines:

                lineEdit = self.lineEdit_selected_ID.text()
                self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 
                               
                self.project.set_material_by_lines(self.lines_typed, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_typed, self.material.getNormalizedColorRGB())
            else:
                self.project.set_material_to_all_lines(self.material)       
                print("[Set Material] - {} defined in all entities".format(self.material.name))
                # self.opv.changeColorEntities(entities, self.material.getNormalizedColorRGB())
            self.close()

        except Exception as error_log:
            self.title = "ERROR WITH THE MATERIAL LIST DATA"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            return


    def loadList(self):

        self.list_names = []
        self.list_ids = []
        self.list_colors = []

        try:
            config = configparser.ConfigParser()
            config.read(self.material_path)
    
            for mat in config.sections():
                material = config[mat]
                name = str(material['name'])
                identifier =  str(material['identifier'])
                density =  str(material['density'])
                young_modulus =  str(material['young modulus'])
                poisson =  str(material['poisson'])
                thermal_expansion_coefficient = str(material['thermal expansion coefficient'])
                color =  str(material['color'])

                load_material = QTreeWidgetItem([name, identifier, density, young_modulus, poisson, thermal_expansion_coefficient, color])
                colorRGB = getColorRGB(color)
                self.list_names.append(name)
                self.list_ids.append(int(identifier))
                self.list_colors.append(colorRGB)
                load_material.setBackground(6,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_material.setForeground(6,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_material)

                for i in range(7):
                    self.treeWidget.headerItem().setTextAlignment(i, Qt.AlignCenter)
                    load_material.setTextAlignment(i, Qt.AlignCenter)
                    
        except Exception as error_log:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            self.close()
        
        self.update_material_id_selector()
        self.lineEdit_selected_material_name.setText("")


    def update_material_id_selector(self):

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox_material_id.setFont(font)
        self.comboBox_material_id.setStyleSheet("color: rgb(0, 0, 255);")

        N = 100
        self.available_indexes = list(np.arange(1,N+1))
        for _id in self.list_ids:
            if _id in self.available_indexes:
                self.available_indexes.remove(_id)

        self.comboBox_material_id.clear()
        for material_id in self.available_indexes:
            text = f"         {material_id}"
            self.comboBox_material_id.addItem(text)

        self.get_comboBox_index()


    def get_comboBox_index(self):
        index = self.comboBox_material_id.currentIndex()
        self.material_id = self.available_indexes[index] 


    def check_add_material(self):

        self.editing = False
        self.adding = True

        parameters = {  "name" : self.lineEdit_name,
                        "identifier" : self.material_id,
                        "density" : self.lineEdit_density,
                        "young_modulus" : self.lineEdit_youngModulus,
                        "poisson" : self.lineEdit_poisson,
                        "thermal expansion coefficient" : self.lineEdit_thermal_expansion_coefficient,
                        "color" : self.lineEdit_color  }

        if self.check_add_edit(parameters):
            PrintMessageInput([self.title, self.message, window_title])  


    def check_edit_material(self):

        if self.lineEdit_selected_material_name.text() == "":
            title = "None material selected"
            message = "Select a material in the material list to be edited."
            PrintMessageInput([title, message, window_title])
            return
        
        # if self.selected_material_to_edit():
        #     return

        if self.editing:

            parameters = {  "name" : self.lineEdit_name_edit,
                            "identifier" : self.lineEdit_id_edit.text(),
                            "density" : self.lineEdit_density_edit,
                            "young_modulus" : self.lineEdit_youngModulus_edit,
                            "poisson" : self.lineEdit_poisson_edit,
                            "thermal expansion coefficient" : self.lineEdit_thermal_expansion_coefficient_edit,
                            "color" : self.lineEdit_color_edit  }

            if self.check_add_edit(parameters):
                PrintMessageInput([self.title, self.message, window_title])      


    def check_color_input(self, lineEdit_color):
        
        self.title = "INVALID MATERIAL COLOR ATTRIBUTION"
        message_empty = "An empty entry was detected at the 'Color [r,g,b]' input field. \nYou should to select a color to proceed."
        message_invalid = "Insert a valid material Color in 'r, g, b' format. \nThe r, g and b values must be inside [0, 255] interval."
        color_string = lineEdit_color.text()

        if color_string == "":
            self.message = message_empty
            return True
        else:
            color = color_string
            
            try:

                colorRGB = getColorRGB(color)
                message_color = " The RGB color {} was already used.\n Please, input a different color.".format(colorRGB)
                if len(colorRGB) != 3:
                    self.message = message_invalid
                    return True

                if self.editing:
                    if getColorRGB(self.temp_material_color) != colorRGB:
                        if colorRGB in self.list_colors:
                            self.message = message_color
                            return True 
                elif self.adding:
                    if colorRGB in self.list_colors:
                        self.message = message_color
                        return True

                self.dict_inputs["color"] = color

            except Exception as error_log:
                self.message = message_invalid + "\n\n" + str(error_log)
                return True


    def check_add_edit(self, parameters):

        [   lineEdit_name,
            identifier, 
            lineEdit_density, 
            lineEdit_young_modulus, 
            lineEdit_poisson, 
            lineEdit_thermal_expansion_coefficient,
            lineEdit_color   ] = parameters.values()
        
        self.title = "INVALID MATERIAL NAME"
        message_empty = "An empty entry was detected at the 'Material name' input field. \nYou should to insert a valid entry to proceed."
        material_name = lineEdit_name.text()
        if material_name == "":
            self.message = message_empty
            lineEdit_name.setFocus()
            return True
        else:
            self.message = f"Please, inform a different material name. \nThe '{material_name}' is already \nbeing used by another material."
            
            if self.editing:
                if self.temp_material_name != material_name:
                    if material_name in self.list_names:
                        lineEdit_name.setFocus()
                        return True
            
            elif self.adding:
                if material_name in self.list_names:
                    lineEdit_name.setFocus()
                    return True
            
            self.dict_inputs["name"] = material_name    

        if isinstance(identifier, str):
            identifier = int(identifier)
        self.dict_inputs["identifier"] = identifier
           
        self.title = "INVALID MATERIAL DENSITY"
        message_invalid = "Insert a valid material density."
        message_empty = "An empty entry was detected at the 'Density' input field. \nYou should to insert a valid entry to proceed."
        
        density_string = lineEdit_density.text()
        if density_string == "":
            self.message = message_empty
            lineEdit_density.setFocus()
            return True
        else:

            try:
            
                density = float(density_string)
                if density <= 0 or density > 20000:
                    self.message = "The input value for material density must be a positive number greater than 0 and less than 20000."
                    return True
                self.dict_inputs["density"] = density
            
            except Exception as log_error:
                self.message = str(log_error) + "\n\n" + message_invalid
                return True 

        self.title = "INVALID MATERIAL YOUNG MODULUS"
        message_invalid = "Insert a valid material Young Modulus."
        message_empty = "An empty entry was detected at the 'Young Modulus' input field. You should to insert a valid entry to proceed."
        
        young_modulus_string = lineEdit_young_modulus.text()
        if young_modulus_string == "":
            self.message = message_empty
            lineEdit_young_modulus.setFocus()
            return True
        else:

            try:
                young_modulus = float(young_modulus_string)
                if young_modulus <= 0 or young_modulus > 600:
                    self.message = "The input value for Young Modulus must be a positive number greater than 0 and less than 600."
                    return True
                self.dict_inputs["young modulus"] = young_modulus
            
            except Exception as log_error:
                self.message = str(log_error) + "\n\n" + message_invalid 
                return True

        self.title = "INVALID MATERIAL POISSON"
        message_invalid = "Insert a valid material Poisson."
        message_empty = "An empty entry was detected at the 'Poisson' input field. You should to insert a valid entry to proceed."
        
        poisson_string = lineEdit_poisson.text()
        if poisson_string == "":
            lineEdit_poisson.setFocus()
            self.message = message_empty
            return True
        else:

            try:
                poisson = float(poisson_string)
                if poisson <= 0 or poisson > 0.5:
                    self.message = "The input value for Poisson must be a positive float number greater than 0 and less than 0.5"
                    return True
                self.dict_inputs["poisson"] = poisson
            
            except Exception as log_error:
                self.message = str(log_error) + "\n\n" + message_invalid
                return True 

        self.title = "INVALID MATERIAL THERMAL EXPANSION COEFFICIENT"
        message_invalid = "Insert a valid material Thermal expansion coefficient to proceed."
        message_empty = "An empty entry was detected at the 'Thermal expansion coefficient' input field. You should to insert a valid entry to proceed."
        
        thermal_expansion_coefficient_string = lineEdit_thermal_expansion_coefficient.text()
        if thermal_expansion_coefficient_string == "":
            lineEdit_thermal_expansion_coefficient.setFocus()
            self.message = message_empty
            return True
        else:
            
            try:
                thermal_expansion_coefficient = float(thermal_expansion_coefficient_string)
                if thermal_expansion_coefficient < 0 or thermal_expansion_coefficient > 6e-5:
                    self.message = "For the sake of physical consistency, the input value for Thermal Expansion Coefficient must be a positive number less than 6e-5."
                    return True
                self.dict_inputs["thermal expansion coefficient"] = thermal_expansion_coefficient
            
            except Exception as log_error:
                self.message = str(log_error) + "\n\n" + message_invalid
                return True 
        
        if self.check_color_input(lineEdit_color):
            return True

        try:

            material_name = self.dict_inputs["name"]
            config = configparser.ConfigParser()
            config.read(self.material_path)
            config[material_name] = self.dict_inputs

            with open(self.material_path, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as error_log:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST"
            self.message = str(error_log)
            return True

        self.adding = False
        self.editing = False            
        self.clicked_item = None
        self.reset_add_texts()
        self.reset_edit_texts()
        self.reset_remove_texts()
        self.treeWidget.clear()
        self.loadList()

        return False


    def selected_material_to_edit(self):

        if self.clicked_item is None:
            self.title = "NO MATERIAL SELECTION"
            self.message = "Select a material in the list to be edited."
            PrintMessageInput([self.title, self.message, window_title])
            return True
        
        try:

            self.editing = True
            self.temp_material_name = self.clicked_item.text(0)
            self.temp_material_id = self.clicked_item.text(1)
            self.temp_material_color = self.clicked_item.text(6)

            self.lineEdit_name_edit.setText(self.clicked_item.text(0))
            self.lineEdit_id_edit.setText(self.clicked_item.text(1))
            self.lineEdit_density_edit.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus_edit.setText(self.clicked_item.text(3))
            self.lineEdit_poisson_edit.setText(self.clicked_item.text(4))
            self.lineEdit_thermal_expansion_coefficient_edit.setText(self.clicked_item.text(5))
            self.lineEdit_color_edit.setText(self.clicked_item.text(6))

            color = tuple(getColorRGB(self.temp_material_color))
            self.lineEdit_color_edit.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")

        except Exception as error_log:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST DATA"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            return True

        return False


    def on_click_item(self, item):
        self.clicked_item = item
        if self.currentTab_ == 0:       
            self.tabWidget_material.setCurrentIndex(1)
        self.selected_material_to_edit()
        self.selected_material_to_remove()

        self.pushButton_pickColor_edit.setDisabled(False)
        self.pushButton_confirm_material_edition.setDisabled(False)
        self.pushButton_confirm_material_removal.setDisabled(False)
        self.lineEdit_selected_material_name.setText(item.text(0))


    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.confirm_material_attribution()
    

    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelectedLines = self.radioButton_selected_lines.isChecked()
        if self.flagSelectedLines:
            self.lineEdit_selected_ID.setEnabled(True)
            if self.lines_ids != []:
                self.write_ids(self.lines_ids)
            else:
                self.lineEdit_selected_ID.setText("")
        elif self.flagAll:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)


    def selected_material_to_remove(self):
        try:

            if self.clicked_item is None:
                self.title = "NO MATERIAL SELECTION"
                self.message = "Select a material in the list to be removed."
                PrintMessageInput([self.title, self.message, window_title])
                return True
            
            else:

                self.lineEdit_name_remove.setText(self.clicked_item.text(0))
                self.lineEdit_id_remove.setText(self.clicked_item.text(1))
                self.lineEdit_density_remove.setText(self.clicked_item.text(2))
                self.lineEdit_youngModulus_remove.setText(self.clicked_item.text(3))
                self.lineEdit_poisson_remove.setText(self.clicked_item.text(4))
                self.lineEdit_thermal_expansion_coefficient_remove.setText(self.clicked_item.text(5))
                self.lineEdit_color_remove.setText(self.clicked_item.text(6))

                color = tuple(getColorRGB(self.clicked_item.text(6)))
                self.lineEdit_color_remove.setStyleSheet(f"background-color: rgb{color}; color: rgb{color}")

        except Exception as error_log:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST DATA"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            return True

        return False


    def confirm_material_removal(self):

        if self.selected_material_to_remove():
            return

        try:

            config = configparser.ConfigParser()
            config.read(self.material_path)
            sections = config.sections()
            selected_material = self.lineEdit_selected_material_name.text()

            if selected_material in sections:
                config.remove_section(selected_material)

                with open(self.material_path, 'w') as config_file:
                    config.write(config_file)

                for line_id, entity in self.dict_tag_to_entity.items():
                    if entity.material is not None:
                        if entity.material.name == self.lineEdit_name_remove.text():
                            self.project.set_material_by_lines(line_id, None)

                self.treeWidget.clear()
                self.clicked_item = None
                self.loadList()
                self.reset_add_texts()
                self.reset_edit_texts()
                self.reset_remove_texts()
                
            else:
                return

        except Exception as error_log:
            self.title = "ERROR DURING THE MATERIAL REMOVAL"
            self.message = str(error_log)
            PrintMessageInput([self.title, self.message, window_title])
            return


    def reset_library_to_default(self):

        title = "Resetting of materials library"
        message = "Do you really want to reset the material library to default values?\n\n\n"
        message += "Press the 'Proceed' button to proceed with resetting or press 'Cancel' or 'Close' buttons to abort the current operation."
        buttons_config = {"left_button_label" : "Cancel", "right_button_label" : "Proceed"}
        read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)


        if read._doNotRun:
            return

        if read._continue:   

            config_cache = configparser.ConfigParser()
            config_cache.read(self.material_path)  
            sections_cache = config_cache.sections()

            default_material_library(self.material_path)
            config = configparser.ConfigParser()
            config.read(self.material_path)

            material_names = []
            for section_cache in sections_cache:
                if section_cache not in config.sections():
                    material_names.append(config_cache[section_cache]["name"])

            for line_id, entity in self.dict_tag_to_entity.items():
                if entity.material is not None:
                    if entity.material.name in material_names:
                        self.project.set_material_by_lines(line_id, None)

            self.treeWidget.clear()
            self.loadList()
            self.reset_add_texts()
            self.reset_edit_texts() 
            self.reset_remove_texts() 
    

    def reset_add_texts(self):
        for lineEdit in self.list_add_lineEdit:
            lineEdit.setText("")


    def reset_edit_texts(self):
        for lineEdit in self.list_edit_lineEdit:
            lineEdit.setText("")


    def reset_remove_texts(self):
        for lineEdit in self.list_remove_lineEdit:
            lineEdit.setText("")