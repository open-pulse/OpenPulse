from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from pulse.utils import error, isInteger, isFloat, getColorRGB
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

from pulse.preprocessing.material import Material

class MaterialInput(QDialog):
    def __init__(self, material_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.materialPath = material_path
        uic.loadUi('pulse/uix/user_input/ui/materialInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.clicked_item = None
        self.material = None
        self.flagAll = False
        self.flagEntity = False

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
        self.treeWidget.setColumnWidth(1, 20)
        self.treeWidget.setColumnWidth(5, 30)
        self.treeWidget.setColumnWidth(3, 180)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_id = self.findChild(QLineEdit, 'lineEdit_id')
        self.lineEdit_density = self.findChild(QLineEdit, 'lineEdit_density')
        self.lineEdit_youngModulus = self.findChild(QLineEdit, 'lineEdit_youngModulus')
        self.lineEdit_poisson = self.findChild(QLineEdit, 'lineEdit_poisson')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')

        self.lineEdit_name_edit = self.findChild(QLineEdit, 'lineEdit_name_edit')
        self.lineEdit_id_edit = self.findChild(QLineEdit, 'lineEdit_id_edit')
        self.lineEdit_density_edit = self.findChild(QLineEdit, 'lineEdit_density_edit')
        self.lineEdit_youngModulus_edit = self.findChild(QLineEdit, 'lineEdit_youngModulus_edit')
        self.lineEdit_poisson_edit = self.findChild(QLineEdit, 'lineEdit_poisson_edit')
        self.lineEdit_color_edit = self.findChild(QLineEdit, 'lineEdit_color_edit')

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.pushButton_confirm_add_material = self.findChild(QPushButton, 'pushButton_confirm_add_material')
        self.pushButton_confirm_add_material.clicked.connect(self.check_add_material)
        
        self.pushButton_selected_material_to_edit = self.findChild(QPushButton, 'pushButton_selected_material_to_edit')
        self.pushButton_selected_material_to_edit.clicked.connect(self.selected_material_to_edit)

        self.pushButton_confirm_material_edition = self.findChild(QPushButton, 'pushButton_confirm_material_edition')
        self.pushButton_confirm_material_edition.clicked.connect(self.check_edit_material)

        self.pushButton_select_material_to_remove = self.findChild(QPushButton, 'pushButton_select_material_to_remove')
        self.pushButton_select_material_to_remove.clicked.connect(self.select_material_to_remove)

        self.pushButton_confirm_material_removal = self.findChild(QPushButton, 'pushButton_confirm_material_removal')
        self.pushButton_confirm_material_removal.clicked.connect(self.confirm_material_removal)

        self.pushButton_reset_library = self.findChild(QPushButton, 'pushButton_reset_library')
        self.pushButton_reset_library.clicked.connect(self.reset_library_to_default)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

        self.loadList()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def select_material_to_remove(self):

        if self.clicked_item is None:
            error("Select a material in the list to be edited.")
            return
        
        try:

            self.lineEdit_name_remove.setText(self.clicked_item.text(0))
            self.lineEdit_id_remove.setText(self.clicked_item.text(1))
            self.lineEdit_density_remove.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus_remove.setText(self.clicked_item.text(3))
            self.lineEdit_poisson_remove.setText(self.clicked_item.text(4))
            self.lineEdit_color_remove.setText(self.clicked_item.text(5))

        except Exception as e:
            error(str(e), "Error with the material list data")
            return

    def confirm_material_removal(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.materialPath)
            if self.lineEdit_name_remove.text() != "":
                config.remove_section(self.lineEdit_name_remove.text().upper())
                with open(self.materialPath, 'w') as configfile:
                    config.write(configfile)
                self.treeWidget.clear()
                self.clicked_item = None
                self.loadList()
                self.lineEdit_name_remove.setText("")
                self.lineEdit_id_remove.setText("")
                self.lineEdit_density_remove.setText("")
                self.lineEdit_youngModulus_remove.setText("")
                self.lineEdit_poisson_remove.setText("")
                self.lineEdit_color_remove.setText("")
                
            else:
                return
        except Exception as e:
            error(str(e), "Error with the material removal")
            return
            
    def check(self):
        if self.clicked_item is None:
            error("Select a material in the list")
            return
        
        try:
            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            density = float(self.clicked_item.text(2))
            young = float(self.clicked_item.text(3))*(10**(9))
            poisson = float(self.clicked_item.text(4))
            color = self.clicked_item.text(5)
            new_material = Material(name, density, poisson_ratio=poisson, young_modulus=young, identifier=identifier, color=color)
            self.material = new_material
            self.close()
        except Exception as e:
            error(str(e), "Error with the material list data")
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
                color =  str(material['color'])

                load_material = QTreeWidgetItem([name, identifier, density, young_modulus, poisson, color])
                colorRGB = getColorRGB(color)
                self.list_names.append(name)
                self.list_ids.append(identifier)
                self.list_colors.append(colorRGB)
                load_material.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_material)
        except Exception as e:
            error(str(e), "Error while loading the material list")
            self.close()
        
    def check_add_material(self):
        name_string = self.lineEdit_name.text()
        id_string = self.lineEdit_id.text()
        density_string = self.lineEdit_density.text()
        young_modulus_string = self.lineEdit_youngModulus.text()
        poisson_string = self.lineEdit_poisson.text()
        color_string = self.lineEdit_color.text()
        self.adding = True
        self.check_add_edit(name_string, id_string, density_string, young_modulus_string, poisson_string, color_string)

    def check_edit_material(self):
        if self.editing:
            name_string = self.lineEdit_name_edit.text()
            id_string = self.lineEdit_id_edit.text()
            density_string = self.lineEdit_density_edit.text()
            young_modulus_string = self.lineEdit_youngModulus_edit.text()
            poisson_string = self.lineEdit_poisson_edit.text()
            color_string = self.lineEdit_color_edit.text()
            self.check_add_edit(name_string, id_string, density_string, young_modulus_string, poisson_string, color_string)        
        else:
            return

    def check_add_edit(self, name_string, id_string, density_string, young_modulus_string, poisson_string, color_string):
        
        if name_string == "":
            error("Insert a material name!")
            return
        else:
            name = name_string
            message_name = "Please, inform a different material name. \nIt is already being used by other material!"
            if self.editing:
                if self.temp_material_name == name:
                    self.same_material_name = True
                else:
                    if name in self.list_names:
                        error(message_name)
                        return
            elif self.adding:
                if name in self.list_names:
                        error(message_name)
                        return

        if id_string == "":
            error("Insert a material ID!")
            return
        else:
            try:
                identifier = str(id_string)
                message_id = "Please, inform a different material ID. \nIt is already being used by other material!"
                if self.editing:
                    if self.temp_material_id != identifier:
                        if identifier in self.list_ids:
                            error(message_id)
                            return
                elif self.adding:
                    if identifier in self.list_ids:
                        error(message_id)
                        return
            except Exception:
                error("Value error (ID)")
                return

        if density_string == "":
            error("Insert a material density!")
            return
        else:
            try:
                density = str(density_string)
                if float(density)<0 or float(density)>20000:
                    error("The input value for Density must be a positive number \n greater than 0 and less than 20000")
                    return
            except Exception:
                error("Value error (Density)")
                return 

        if young_modulus_string == "":
            error("Insert a material Young Modulus!")
            return
        else:
            try:
                young_modulus = str(young_modulus_string)
                if float(young_modulus)<0 or float(young_modulus)>600:
                    error("The input value for Young Modulus must be a positive number \n greater than 0 and less than 600")
                    return
            except Exception:
                error("Value error (Young Modulus)")
                return

        if poisson_string == "":
            error("Insert a material Poisson!")
            return
        else:
            try:
                poisson = str(poisson_string)
                if float(poisson)<0 or float(poisson)>0.5:
                    error("The input value for Poisson must be a positive \nfloat number greater than 0 and less than 0.5")
                    return
            except Exception:
                error("Value error (Poisson)")
                return 

        if color_string == "":
            error("Insert a material Color!")
            return
        else:
            color = color_string
            message = " Invalid color RGB input! You must input: [value1, value2, value3] \nand the values must be inside [0, 255] interval."
            try:

                colorRGB = getColorRGB(color)
                message_color = (" The RGB color {} was already used.\n Please, input a different color.").format(colorRGB)

                if len(colorRGB)!=3:
                    error(message)
                    return

                if self.editing:
                    if getColorRGB(self.temp_material_color) != colorRGB:
                        if colorRGB in self.list_colors:
                            error(message_color)
                            return 
                elif self.adding:
                    if colorRGB in self.list_colors:
                        error(message_color)
                        return

            except:
                error(message)
                return
        
        try:
            config = configparser.ConfigParser()
            config.read(self.materialPath)
            config[name.upper()] = {
            'Name': name,
            'Identifier': identifier,
            'Density': density,
            'Young Modulus': young_modulus,
            'Poisson': poisson,
            'Color': color
            }
            with open(self.materialPath, 'w') as configfile:
                config.write(configfile)
                    
        except Exception as e:
            error(str(e), "Error while loading the material list")
            return

        if self.adding:
            self.treeWidget.clear()
            self.loadList()
            self.adding = False

        elif self.editing:    
            self.treeWidget.clear()
            self.clicked_item = None
     
            self.loadList()
            self.editing = False
            self.lineEdit_name_edit.setText("")
            self.lineEdit_id_edit.setText("")
            self.lineEdit_density_edit.setText("")
            self.lineEdit_youngModulus_edit.setText("")
            self.lineEdit_poisson_edit.setText("")
            self.lineEdit_color_edit.setText("")
            self.same_material_name = False

    def selected_material_to_edit(self):

        if self.clicked_item is None:
            error("Select a material in the list to be edited.")
            return
        
        try:

            self.lineEdit_name_edit.setText(self.clicked_item.text(0))
            self.lineEdit_id_edit.setText(self.clicked_item.text(1))
            self.lineEdit_density_edit.setText(self.clicked_item.text(2))
            self.lineEdit_youngModulus_edit.setText(self.clicked_item.text(3))
            self.lineEdit_poisson_edit.setText(self.clicked_item.text(4))
            self.lineEdit_color_edit.setText(self.clicked_item.text(5))

            self.temp_material_name = self.clicked_item.text(0)
            self.temp_material_id = self.clicked_item.text(1)
            self.temp_material_color = self.clicked_item.text(5)
            
            self.editing = True

        except Exception as e:
            error(str(e), "Error with the material list data")
            return

    def default_material_library(self):

        config = configparser.ConfigParser()

        config['STEEL'] = {
            'Name': 'steel',
            'Identifier': 1,
            'Density': 7860,
            'Young Modulus': 210,
            'Poisson': 0.3,
            'Color': '[0,0,255]' } #Blue

        config['STAINLESS_STEEL'] = {
            'Name': 'stainless_steel',
            'Identifier': 2,
            'Density': 7750,
            'Young Modulus': 193,
            'Poisson': 0.31,
            'Color': '[126,46,31]' } #Wood color

        config['NI-CO-CR_ALLOY'] = {
            'Name': 'Ni-Co-Cr_alloy',
            'Identifier': 3,
            'Density': 8220,
            'Young Modulus': 212,
            'Poisson': 0.315,
            'Color': '[0,255,255]' } #Cyan
        
        config['CAST_IRON'] = {
            'Name': 'cast_iron',
            'Identifier': 4,
            'Density': 7200,
            'Young Modulus': 110,
            'Poisson': 0.28,
            'Color': '[50,50,50]' } #Dark Grey

        config['ALUMINUM'] = {
            'Name': 'aluminum',
            'Identifier': 5,
            'Density': 2770,
            'Young Modulus': 71,
            'Poisson': 0.333,
            'Color': '[160,160,160]' } #Grey

        config['BRASS'] = {
            'Name': 'brass',
            'Identifier': 6,
            'Density': 8150,
            'Young Modulus': 96,
            'Poisson': 0.345,
            'Color': '[181,166,66]' } #Brass color

        with open(self.materialPath, 'w') as configfile:
            config.write(configfile)
        
    def reset_library_to_default(self):
        self.default_material_library()
        self.treeWidget.clear()
        self.loadList()

    def on_click_item(self, item):
        self.clicked_item = item

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.check()
    
    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()