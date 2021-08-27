from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton, QTabWidget, QWidget
from pulse.utils import getColorRGB
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.material import Material
from pulse.default_libraries import default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput

window_title = "ERROR"

class MaterialInput(QDialog):
    def __init__(   self, project, opv,  cache_selected_lines=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi('data/user_input/ui/Model/Setup/Structural/materialInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)
        self.lines_ids = self.opv.getListPickedEntities()

        self.project = project
        self.preprocessor = project.preprocessor
        self.before_run = project.get_model_checks()

        self.materialPath = project.get_material_list_path()
        self.cache_selected_lines = cache_selected_lines
        
        self.clicked_item = None
        self.material = None
        self.flagAll = False
        self.flagSelectedLines = False

        self.no_material_selected_to_edit = True
        self.no_material_selected_to_remove = True

        self.same_material_name = False
        self.adding = False
        self.editing = False
        self.list_names = []
        self.list_ids = []
        self.list_colors = []
        self.temp_material_name = ""
        self.temp_material_id = ""
        self.temp_material_color = ""

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.setColumnWidth(0, 120)
        self.treeWidget.setColumnWidth(1, 10)
        self.treeWidget.setColumnWidth(2, 120)
        self.treeWidget.setColumnWidth(3, 170)
        self.treeWidget.setColumnWidth(4, 70)
        self.treeWidget.setColumnWidth(5, 210)
        self.treeWidget.setColumnWidth(6, 10)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.tabWidget_material = self.findChild(QTabWidget, 'tabWidget_material')
        self.tabWidget_material.currentChanged.connect(self.tabEvent_)
        self.currentTab_ = self.tabWidget_material.currentIndex()
        self.tab_edit_material = self.tabWidget_material.findChild(QWidget, "tab_edit_material")
        self.tab_remove_material = self.tabWidget_material.findChild(QWidget, "tab_remove_material")

        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_id = self.findChild(QLineEdit, 'lineEdit_id')
        self.lineEdit_density = self.findChild(QLineEdit, 'lineEdit_density')
        self.lineEdit_youngModulus = self.findChild(QLineEdit, 'lineEdit_youngModulus')
        self.lineEdit_poisson = self.findChild(QLineEdit, 'lineEdit_poisson')
        self.lineEdit_thermal_expansion_coefficient = self.findChild(QLineEdit, 'lineEdit_thermal_expansion_coefficient')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')

        self.lineEdit_name_edit = self.findChild(QLineEdit, 'lineEdit_name_edit')
        self.lineEdit_id_edit = self.findChild(QLineEdit, 'lineEdit_id_edit')
        self.lineEdit_density_edit = self.findChild(QLineEdit, 'lineEdit_density_edit')
        self.lineEdit_youngModulus_edit = self.findChild(QLineEdit, 'lineEdit_youngModulus_edit')
        self.lineEdit_poisson_edit = self.findChild(QLineEdit, 'lineEdit_poisson_edit')
        self.lineEdit_thermal_expansion_coefficient_edit = self.findChild(QLineEdit, 'lineEdit_thermal_expansion_coefficient_edit')
        self.lineEdit_color_edit = self.findChild(QLineEdit, 'lineEdit_color_edit')

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_selected_lines = self.findChild(QRadioButton, 'radioButton_selected_lines')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_selected_lines.toggled.connect(self.radioButtonEvent)

        self.lineEdit_selected_ID = self.findChild(QLineEdit, 'lineEdit_selected_ID')

        if self.cache_selected_lines != []:
            self.lines_ids = self.cache_selected_lines

        if self.lines_ids != []:
            self.write_ids(self.lines_ids)
            self.radioButton_selected_lines.setChecked(True)

        else:
            self.lineEdit_selected_ID.setText("All lines")
            self.lineEdit_selected_ID.setEnabled(False)
            self.radioButton_all.setChecked(True)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.pushButton_confirm_add_material = self.findChild(QPushButton, 'pushButton_confirm_add_material')
        self.pushButton_confirm_add_material.clicked.connect(self.check_add_material)

        self.pushButton_reset_entries_add_material = self.findChild(QPushButton, 'pushButton_reset_entries_add_material')
        self.pushButton_reset_entries_add_material.clicked.connect(self.reset_add_texts)
        
        self.pushButton_confirm_material_edition = self.findChild(QPushButton, 'pushButton_confirm_material_edition')
        self.pushButton_confirm_material_edition.clicked.connect(self.check_edit_material)

        self.pushButton_confirm_material_removal = self.findChild(QPushButton, 'pushButton_confirm_material_removal')
        self.pushButton_confirm_material_removal.clicked.connect(self.confirm_material_removal)

        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagSelectedLines = self.radioButton_selected_lines.isChecked()

        self.loadList()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def write_ids(self, list_ids):
        text = ""
        for _id in list_ids:
            text += "{}, ".format(_id)
        self.lineEdit_selected_ID.setText(text)

    def update(self):
        self.lines_ids = self.opv.getListPickedEntities()
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
        if self.currentTab_ == 1:
            if self.clicked_item is not None:
                self.selected_material_to_edit()
        elif self.currentTab_ == 2:
            if self.clicked_item is not None:
                self.selected_material_to_remove()
            
    def check(self):

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
            
            new_material = Material(name, density,
                                            poisson_ratio=poisson, 
                                            young_modulus=young, 
                                            identifier=identifier, 
                                            thermal_expansion_coefficient=thermal_expansion_coefficient, 
                                            color=color)
            self.material = new_material
            
            if self.flagSelectedLines:

                lineEdit = self.lineEdit_selected_ID.text()
                self.stop, self.lines_typed = self.before_run.check_input_LineID(lineEdit)
                if self.stop:
                    return True 
                               
                for line in self.lines_typed:
                    self.project.set_material_by_line(line, self.material)
                print("[Set Material] - {} defined in the entities {}".format(self.material.name, self.lines_typed))
                # self.opv.changeColorEntities(self.lines_typed, self.material.getNormalizedColorRGB())
            else:
                self.project.set_material(self.material)       
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
            config.read(self.materialPath)
    
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
                self.list_ids.append(identifier)
                self.list_colors.append(colorRGB)
                load_material.setBackground(6,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_material.setForeground(6,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_material)

                for i in range(7):
                    self.treeWidget.headerItem().setTextAlignment(i, Qt.AlignCenter)
                    load_material.setTextAlignment(i, Qt.AlignCenter)
                    
        except Exception as e:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST"
            self.message = str(e)
            PrintMessageInput([self.title, self.message, window_title])
            self.close()
        
    def check_add_material(self):
        name_string = self.lineEdit_name.text()
        id_string = self.lineEdit_id.text()
        density_string = self.lineEdit_density.text()
        young_modulus_string = self.lineEdit_youngModulus.text()
        poisson_string = self.lineEdit_poisson.text()
        thermal_expansion_coefficient_string = self.lineEdit_thermal_expansion_coefficient.text()
        color_string = self.lineEdit_color.text()
        self.editing = False
        self.adding = True
        if self.check_add_edit(name_string, id_string, density_string, young_modulus_string, poisson_string, thermal_expansion_coefficient_string, color_string):
            PrintMessageInput([self.title, self.message, window_title])  

    def check_edit_material(self):
        if self.no_material_selected_to_edit:
            if self.selected_material_to_edit():
                return
        if self.editing:
            name_string = self.lineEdit_name_edit.text()
            id_string = self.lineEdit_id_edit.text()
            density_string = self.lineEdit_density_edit.text()
            young_modulus_string = self.lineEdit_youngModulus_edit.text()
            poisson_string = self.lineEdit_poisson_edit.text()
            thermal_expansion_coefficient_string = self.lineEdit_thermal_expansion_coefficient_edit.text()
            color_string = self.lineEdit_color_edit.text()

            if self.check_add_edit(name_string, id_string, density_string, young_modulus_string, poisson_string, thermal_expansion_coefficient_string, color_string):
                PrintMessageInput([self.title, self.message, window_title])        
        else:
            return

    def check_add_edit(self, name_string, id_string, density_string, young_modulus_string, poisson_string, thermal_expansion_coefficient_string, color_string):
        
        self.title = "INVALID MATERIAL NAME"
        if name_string == "":
            self.message = "Insert a valid material name."
            return True
        else:
            name = name_string
            self.message = "Please, inform a different material name. \nIt is already being used by other material!"
            if self.editing:
                if self.temp_material_name == name:
                    self.same_material_name = True
                else:
                    if name in self.list_names:
                        return True
            elif self.adding:
                if name in self.list_names:
                        return True

        self.title = "INVALID MATERIAL ID"
        self.message = "Insert a valid material ID."
        if id_string == "":
            return True
        else:
            try:
                identifier = str(id_string)
                self.message = "Please, inform a different material ID. \nIt is already being used by other material!"
                if self.editing:
                    if self.temp_material_id != identifier:
                        if identifier in self.list_ids:
                            return True
                elif self.adding:
                    if identifier in self.list_ids:
                        return True
            except Exception:
                return True

        self.title = "INVALID MATERIAL DENSITY"
        self.message = "Insert a valid material density."
        if density_string == "":
            return True
        else:
            try:
                density = str(density_string)
                if float(density)<0 or float(density)>20000:
                    self.message = "The input value for Density must be a positive number \ngreater than 0 and less than 20000."
                    return True
            except Exception:
                return True 

        self.title = "INVALID MATERIAL YOUNG MODULUS"
        self.message = "Insert a valid material Young Modulus."
        if young_modulus_string == "":
            return True
        else:
            try:
                young_modulus = str(young_modulus_string)
                if float(young_modulus)<0 or float(young_modulus)>600:
                    self.message = "The input value for Young Modulus must be a positive \nnumber greater than 0 and less than 600."
                    return True
            except Exception:
                return True

        self.title = "INVALID MATERIAL POISSON"
        self.message = "Insert a valid material Poisson."
        if poisson_string == "":
            return True
        else:
            try:
                poisson = str(poisson_string)
                if float(poisson)<=0 or float(poisson)>0.5:
                    self.message = "The input value for Poisson must be a positive \nfloat number greater than 0 and less than 0.5"
                    return True
            except Exception:
                return True 

        self.title = "INVALID MATERIAL THERMAL EXPANSION COEFFICIENT"
        self.message = "Insert a valid material Thermal Expansion Coefficient."
        if thermal_expansion_coefficient_string == "":
            thermal_expansion_coefficient = ""
        else:
            try:
                thermal_expansion_coefficient = str(thermal_expansion_coefficient_string)
                if float(thermal_expansion_coefficient)<0 or float(thermal_expansion_coefficient)>4e-5:
                    self.message = "For the sake of physical consistency, the input \nvalue for Thermal Expansion Coefficient must \nbe a positive number less than 4e-5."
                    return True
            except Exception:
                return True 

        self.title = "INVALID MATERIAL COLOR ATTRIBUTION"
        message_1 = "Insert a valid material Color in [r,g,b] format. \nThe r, g and b values must be inside [0, 255] interval."
        if color_string == "":
            self.message = message_1
            return True
        else:
            color = color_string
            
            try:

                colorRGB = getColorRGB(color)
                message_2 = " The RGB color {} was already used.\n Please, input a different color.".format(colorRGB)
                if len(colorRGB)!=3:
                    self.message = message_1
                    return True

                if self.editing:
                    if getColorRGB(self.temp_material_color) != colorRGB:
                        if colorRGB in self.list_colors:
                            self.message = message_2
                            return True 
                elif self.adding:
                    if colorRGB in self.list_colors:
                        self.message = message_2
                        return True

            except Exception as e:
                self.message = message_1
                return True
        
        try:
            config = configparser.ConfigParser()
            config.read(self.materialPath)
            config[name.upper()] = {
            'Name': name,
            'Identifier': identifier,
            'Density': density,
            'Young Modulus': young_modulus,
            'Poisson': poisson,
            'Thermal expansion coefficient': thermal_expansion_coefficient,
            'Color': color
            }
            with open(self.materialPath, 'w') as config_file:
                config.write(config_file)
                    
        except Exception as e:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST"
            self.message = str(e)
            return True

        if self.adding:
            self.treeWidget.clear()
            self.loadList()
            self.adding = False

        elif self.editing:    
            self.treeWidget.clear()
            self.clicked_item = None
     
            self.loadList()
            self.editing = False
            self.reset_edit_texts()
            self.same_material_name = False
            self.no_material_selected_to_edit = True

        return False

    def selected_material_to_add(self):      
        try:
            self.lineEdit_name.setText(self.clicked_item.text(0))
            self.lineEdit_id.setText(self.clicked_item.text(1))
            self.lineEdit_density.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus.setText(self.clicked_item.text(3))
            self.lineEdit_poisson.setText(self.clicked_item.text(4))
            self.lineEdit_thermal_expansion_coefficient.setText(self.clicked_item.text(5))
            self.lineEdit_color.setText(self.clicked_item.text(6))    
        except Exception as e:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST DATA"
            self.message = str(e)
            PrintMessageInput([self.title, self.message, window_title])
            return True
        return False

    def selected_material_to_edit(self):

        if self.clicked_item is None:
            self.title = "NO MATERIAL SELECTION"
            self.message = "Select a material in the list to be edited."
            PrintMessageInput([self.title, self.message, window_title])
            return True
        
        try:

            self.lineEdit_name_edit.setText(self.clicked_item.text(0))
            self.lineEdit_id_edit.setText(self.clicked_item.text(1))
            self.lineEdit_density_edit.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus_edit.setText(self.clicked_item.text(3))
            self.lineEdit_poisson_edit.setText(self.clicked_item.text(4))
            self.lineEdit_thermal_expansion_coefficient_edit.setText(self.clicked_item.text(5))
            self.lineEdit_color_edit.setText(self.clicked_item.text(6))
            
            self.temp_material_name = self.clicked_item.text(0)
            self.temp_material_id = self.clicked_item.text(1)
            self.temp_material_color = self.clicked_item.text(6)
            
            self.editing = True

        except Exception as e:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST DATA"
            self.message = str(e)
            PrintMessageInput([self.title, self.message, window_title])
            return True
        self.no_material_selected_to_edit = False
        return False

    def on_click_item(self, item):
        self.clicked_item = item
        if self.currentTab_ == 0:       
            self.selected_material_to_add() 
        elif self.currentTab_ == 1:
            self.selected_material_to_edit()
        elif self.currentTab_ == 2:
            self.selected_material_to_remove()

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.check()
    
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

        if self.clicked_item is None:
            self.title = "NO MATERIAL SELECTION"
            self.message = "Select a material in the list to be removed."
            PrintMessageInput([self.title, self.message, window_title])
            return True
        
        try:

            self.lineEdit_name_remove.setText(self.clicked_item.text(0))
            self.lineEdit_id_remove.setText(self.clicked_item.text(1))
            self.lineEdit_density_remove.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus_remove.setText(self.clicked_item.text(3))
            self.lineEdit_poisson_remove.setText(self.clicked_item.text(4))
            self.lineEdit_thermal_expansion_coefficient_remove.setText(self.clicked_item.text(5))
            self.lineEdit_color_remove.setText(self.clicked_item.text(6))

        except Exception as e:
            self.title = "ERROR WHILE LOADING THE MATERIAL LIST DATA"
            self.message = str(e)
            PrintMessageInput([self.title, self.message, window_title])
            return True
        self.no_material_selected_to_remove = False

        return False

    def confirm_material_removal(self):

        if self.no_material_selected_to_remove:
            if self.selected_material_to_remove():
                return

        try:

            config = configparser.ConfigParser()
            config.read(self.materialPath)

            if self.lineEdit_name_remove.text() != "":
                config.remove_section(self.lineEdit_name_remove.text().upper())

                with open(self.materialPath, 'w') as config_file:
                    config.write(config_file)
                self.treeWidget.clear()
                self.clicked_item = None
                self.loadList()
                self.lineEdit_name_remove.setText("")
                self.lineEdit_id_remove.setText("")
                self.lineEdit_density_remove.setText("")
                self.lineEdit_youngModulus_remove.setText("")
                self.lineEdit_poisson_remove.setText("")
                self.lineEdit_thermal_expansion_coefficient_remove.setText("")
                self.lineEdit_color_remove.setText("")
                self.no_material_selected_to_remove = True
                
            else:
                return

        except Exception as e:
            self.title = "ERROR DURING THE MATERIAL REMOVAL"
            self.message = str(e)
            PrintMessageInput([self.title, self.message, window_title])
            return


    def default_material_library(self):

        config = configparser.ConfigParser()

        config['STEEL'] = {
            'Name': 'steel',
            'Identifier': 1,
            'Density': 7860,
            'Young Modulus': 210,
            'Poisson': 0.3,
            'Thermal expansion coefficient': 1.2e-5,
            'Color': '[170,170,170]' #Light Gray
        }

        config['STAINLESS_STEEL'] = {
            'Name': 'stainless_steel',
            'Identifier': 2,
            'Density': 7750,
            'Young Modulus': 193,
            'Poisson': 0.31,
            'Thermal expansion coefficient': 1.7e-5,
            'Color': '[126,46,31]' #Wood color
        }

        config['NI-CO-CR_ALLOY'] = {
            'Name': 'Ni-Co-Cr_alloy',
            'Identifier': 3,
            'Density': 8220,
            'Young Modulus': 212,
            'Poisson': 0.315,
            'Thermal expansion coefficient': 1.2e-5,
            'Color': '[0,255,255]' #Cyan
        }

        config['CAST_IRON'] = {
            'Name': 'cast_iron',
            'Identifier': 4,
            'Density': 7200,
            'Young Modulus': 110,
            'Poisson': 0.28,
            'Thermal expansion coefficient': 1.1e-5,
            'Color': '[50,50,50]' #Dark Grey
        }

        config['ALUMINUM'] = {
            'Name': 'aluminum',
            'Identifier': 5,
            'Density': 2770,
            'Young Modulus': 71,
            'Poisson': 0.333,
            'Thermal expansion coefficient': 2.3e-5,
            'Color': '[255,255,255]' #White
        }

        config['BRASS'] = {
            'Name': 'brass',
            'Identifier': 6,
            'Density': 8150,
            'Young Modulus': 96,
            'Poisson': 0.345,
            'Thermal expansion coefficient': 1.9e-5,
            'Color': '[181,166,66]' #Brass color
        }

        with open(self.materialPath, 'w') as config_file:
            config.write(config_file)
        
    def reset_library_to_default(self):
        self.default_material_library()
        self.treeWidget.clear()
        self.loadList()
        self.reset_add_texts()
        self.reset_edit_texts() 
        self.reset_remove_texts() 

    def reset_add_texts(self):
        self.lineEdit_name.setText("")
        self.lineEdit_id.setText("")
        self.lineEdit_density.setText("")
        self.lineEdit_youngModulus.setText("")
        self.lineEdit_poisson.setText("")
        self.lineEdit_thermal_expansion_coefficient.setText("")
        self.lineEdit_color.setText("")
    
    def reset_edit_texts(self):
        self.lineEdit_name_edit.setText("")
        self.lineEdit_id_edit.setText("")
        self.lineEdit_density_edit.setText("")
        self.lineEdit_youngModulus_edit.setText("")
        self.lineEdit_poisson_edit.setText("")
        self.lineEdit_thermal_expansion_coefficient_edit.setText("")
        self.lineEdit_color_edit.setText("")

    def reset_remove_texts(self):
        self.lineEdit_name_remove.setText("")
        self.lineEdit_id_remove.setText("")
        self.lineEdit_density_remove.setText("")
        self.lineEdit_youngModulus_remove.setText("")
        self.lineEdit_poisson_remove.setText("")
        self.lineEdit_thermal_expansion_coefficient_remove.setText("")
        self.lineEdit_color_remove.setText("")