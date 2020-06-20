from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from pulse.utils import error, isInteger, isFloat, getColorRGB

from pulse.preprocessing.fluid import Fluid

class FluidInput(QDialog):
    def __init__(self, fluid_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fluidPath = fluid_path
        uic.loadUi('pulse/uix/user_input/ui/fluidInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.clicked_item = None
        self.fluid = None
        self.flagAll = False
        self.flagEntity = False

        self.same_fluid_name = False
        self.adding = False
        self.editing = False
        self.list_names = []
        self.list_ids = []
        self.list_colors = []
        self.temp_fluid_name = ""
        self.temp_fluid_id = ""
        self.temp_fluid_color = ""

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.setColumnWidth(1, 20)
        self.treeWidget.setColumnWidth(5, 30)
        self.treeWidget.setColumnWidth(3, 180)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_id = self.findChild(QLineEdit, 'lineEdit_id')
        self.lineEdit_fluid_density = self.findChild(QLineEdit, 'lineEdit_fluid_density')
        self.lineEdit_sound_velocity = self.findChild(QLineEdit, 'lineEdit_sound_velocity')
        self.lineEdit_impedance = self.findChild(QLineEdit, 'lineEdit_impedance')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')

        self.lineEdit_name_edit = self.findChild(QLineEdit, 'lineEdit_name_edit')
        self.lineEdit_id_edit = self.findChild(QLineEdit, 'lineEdit_id_edit')
        self.lineEdit_fluid_density_edit = self.findChild(QLineEdit, 'lineEdit_fluid_density_edit')
        self.lineEdit_sound_velocity_edit = self.findChild(QLineEdit, 'lineEdit_sound_velocity_edit')
        self.lineEdit_impedance_edit = self.findChild(QLineEdit, 'lineEdit_impedance_edit')
        self.lineEdit_color_edit = self.findChild(QLineEdit, 'lineEdit_color_edit')
        
        self.lineEdit_name_remove = self.findChild(QLineEdit, 'lineEdit_name_remove')
        self.lineEdit_id_remove = self.findChild(QLineEdit, 'lineEdit_id_remove')
        self.lineEdit_fluid_density_remove = self.findChild(QLineEdit, 'lineEdit_fluid_density_remove')
        self.lineEdit_sound_velocity_remove = self.findChild(QLineEdit, 'lineEdit_sound_velocity_remove')
        self.lineEdit_impedance_remove = self.findChild(QLineEdit, 'lineEdit_impedance_remove')
        self.lineEdit_color_remove = self.findChild(QLineEdit, 'lineEdit_color_remove')

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.pushButton_confirm_add_fluid = self.findChild(QPushButton, 'pushButton_confirm_add_fluid')
        self.pushButton_confirm_add_fluid.clicked.connect(self.check_add_fluid)
        
        self.pushButton_selected_fluid_to_edit = self.findChild(QPushButton, 'pushButton_selected_fluid_to_edit')
        self.pushButton_selected_fluid_to_edit.clicked.connect(self.selected_fluid_to_edit)

        self.pushButton_confirm_fluid_edition = self.findChild(QPushButton, 'pushButton_confirm_fluid_edition')
        self.pushButton_confirm_fluid_edition.clicked.connect(self.check_edit_fluid)

        self.pushButton_select_fluid_to_remove = self.findChild(QPushButton, 'pushButton_select_fluid_to_remove')
        self.pushButton_select_fluid_to_remove.clicked.connect(self.select_fluid_to_remove)

        self.pushButton_confirm_fluid_removal = self.findChild(QPushButton, 'pushButton_confirm_fluid_removal')
        self.pushButton_confirm_fluid_removal.clicked.connect(self.confirm_fluid_removal)

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

    def select_fluid_to_remove(self):

        if self.clicked_item is None:
            error("Select a fluid in the list to be edited.")
            return
        
        try:

            self.lineEdit_name_remove.setText(self.clicked_item.text(0))
            self.lineEdit_id_remove.setText(self.clicked_item.text(1))
            self.lineEdit_fluid_density_remove.setText(self.clicked_item.text(2))
            self.lineEdit_sound_velocity_remove.setText(self.clicked_item.text(3))
            self.lineEdit_impedance_remove.setText(self.clicked_item.text(4))
            self.lineEdit_color_remove.setText(self.clicked_item.text(5))

        except Exception as e:
            error(str(e), "Error with the fluid list data")
            return

    def confirm_fluid_removal(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.fluidPath)
            if self.lineEdit_name_remove.text() != "":
                config.remove_section(self.lineEdit_name_remove.text().upper())
                with open(self.fluidPath, 'w') as configfile:
                    config.write(configfile)
                self.treeWidget.clear()
                self.clicked_item = None
                self.loadList()
                self.lineEdit_name_remove.setText("")
                self.lineEdit_id_remove.setText("")
                self.lineEdit_fluid_density_remove.setText("")
                self.lineEdit_sound_velocity_remove.setText("")
                self.lineEdit_impedance_remove.setText("")
                self.lineEdit_color_remove.setText("")
                
            else:
                return
        except Exception as e:
            error(str(e), "Error with the material removal")
            return

    def check(self):
        if self.clicked_item is None:
            error("Select a fluid in the list")
            return
        
        try:
            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            fluid_density = float(self.clicked_item.text(2))
            sound_velocity = float(self.clicked_item.text(3))
            # impedance = float(self.clicked_item.text(4))
            color = self.clicked_item.text(5)
            new_fluid = Fluid(name, fluid_density, sound_velocity, identifier=identifier, color=color)
            self.fluid = new_fluid
            self.close()
        except Exception as e:
            error(str(e), "Error with the fluid list data")
            return
            
    def loadList(self):

        self.list_names = []
        self.list_ids = []
        self.list_colors = []

        try:
            config = configparser.ConfigParser()
            config.read(self.fluidPath)

            for fluid in config.sections():
                rFluid = config[fluid]
                name = str(rFluid['name'])
                identifier =  str(rFluid['identifier'])
                fluid_density =  str(rFluid['fluid density'])
                sound_velocity =  str(rFluid['sound velocity'])
                impedance =  str(rFluid['impedance'])
                color =  str(rFluid['color'])

                load_fluid = QTreeWidgetItem([name, identifier, fluid_density, sound_velocity, impedance, color])
                colorRGB = getColorRGB(color)
                self.list_names.append(name)
                self.list_ids.append(identifier)
                self.list_colors.append(colorRGB)
                load_fluid.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_fluid.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_fluid)
        except Exception as e:
            error(str(e), "Error while loading the fluid list")
            self.close()
        
    def check_add_fluid(self):
        name_string = self.lineEdit_name.text()
        id_string = self.lineEdit_id.text()
        fluid_density_string = self.lineEdit_fluid_density.text()
        sound_velocity_string = self.lineEdit_sound_velocity.text()
        # impedance_string = self.lineEdit_impedance.text()
        color_string = self.lineEdit_color.text()
        self.adding = True
        self.check_add_edit(name_string, id_string, fluid_density_string, sound_velocity_string, color_string)

    def check_edit_fluid(self):
        if self.editing:
            name_string = self.lineEdit_name_edit.text()
            id_string = self.lineEdit_id_edit.text()
            fluid_density_string = self.lineEdit_fluid_density_edit.text()
            sound_velocity_string = self.lineEdit_sound_velocity_edit.text()
            # impedance_string = self.lineEdit_impedance_edit.text()
            color_string = self.lineEdit_color_edit.text()
            self.check_add_edit(name_string, id_string, fluid_density_string, sound_velocity_string, color_string)        
        else:
            return
            
    def check_add_edit(self, name_string, id_string, fluid_density_string, sound_velocity_string, color_string):

        if name_string == "":
            error("Insert a fluid name!")
            return
        else:
            name = name_string
            message_name = "Please, inform a different fluid name. \nIt is already being used by other fluid!"
            if self.editing:
                if self.temp_fluid_name == name:
                    self.same_fluid_name = True
                else:
                    if name in self.list_names:
                        error(message_name)
                        return
            elif self.adding:
                if name in self.list_names:
                        error(message_name)
                        return

        if id_string == "":
            error("Insert a fluid ID!")
            return
        else:
            try:
                identifier = str(id_string)
                message_id = "Please, inform a different fluid ID. \nIt is already being used by other fluid!"
                if self.editing:
                    if self.temp_fluid_id != identifier:
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

        if fluid_density_string == "":
            error("Insert a fluid density!")
            return
        else:
            try:
                fluid_density = str(fluid_density_string)
                if float(fluid_density)<0 or float(fluid_density)>2000:
                    error("The input value for fluid density must be a positive \nnumber greater than 0 and less than 2000")
                    return
            except Exception:
                error("Value error (fluid density)")
                return 

        if sound_velocity_string == "":
            error("Insert the sound velocity of the fluid!")
            return
        else:
            try:
                sound_velocity = str(sound_velocity_string)
                if float(sound_velocity)<0:
                    error("The input value for sound velocity must be a positive number.")
                    return
            except Exception:
                error("Value error (sound velocity)")
                return

            try:
                impedance = str(float(fluid_density_string)*float(sound_velocity_string))
                if self.adding:
                    self.lineEdit_impedance.setText(impedance)
                elif self.editing:
                    self.lineEdit_impedance_edit.setText(impedance)
            except Exception:
                error("Some error has occurred during impedance calculation.")
                return 

        if color_string == "":
            error("Insert a fluid Color!")
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
                    if getColorRGB(self.temp_fluid_color) != colorRGB:
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
            config.read(self.fluidPath)
            config[name.upper()] = {
            'name': name,
            'identifier': identifier,
            'fluid density': fluid_density,
            'sound velocity': sound_velocity,
            'impedance': impedance,
            'color': color
            }
            with open(self.fluidPath, 'w') as configfile:
                config.write(configfile)
                    
        except Exception as e:
            error(str(e), "Error while loading the fluid list")
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
            self.lineEdit_fluid_density_edit.setText("")
            self.lineEdit_sound_velocity_edit.setText("")
            self.lineEdit_impedance_edit.setText("")
            self.lineEdit_color_edit.setText("")
            self.same_fluid_name = False

    def selected_fluid_to_edit(self):

        if self.clicked_item is None:
            error("Select a fluid in the list to be edited.")
            return
        
        try:

            self.lineEdit_name_edit.setText(self.clicked_item.text(0))
            self.lineEdit_id_edit.setText(self.clicked_item.text(1))
            self.lineEdit_fluid_density_edit.setText(self.clicked_item.text(2))
            self.lineEdit_sound_velocity_edit.setText(self.clicked_item.text(3))
            self.lineEdit_impedance_edit.setText(self.clicked_item.text(4))
            self.lineEdit_color_edit.setText(self.clicked_item.text(5))

            self.temp_fluid_name = self.clicked_item.text(0)
            self.temp_fluid_id = self.clicked_item.text(1)
            self.temp_fluid_color = self.clicked_item.text(5)
            
            self.editing = True

        except Exception as e:
            error(str(e), "Error with the fluid list data")
            return

    def default_fluid_library(self):

        config = configparser.ConfigParser()

        config['AIR'] = {
            'Name': 'air',
            'Identifier': 1,
            'Fluid density': 1.2041,
            'Sound velocity': 343.21,
            'Impedance': 413.25,
            'Color': '[0,0,255]' } #Blue     

        config['HYDROGEN'] = {
            'Name': 'hydrogen',
            'Identifier': 2,
            'Fluid density': 0.087,
            'Sound velocity': 1321.1,
            'Impedance': 114.93,
            'Color': '[255,0,255]' } #Magenta
        
        config['METHANE'] = {
            'Name': 'methane',
            'Identifier': 3,
            'Fluid density': 0.657,
            'Sound velocity': 446,
            'Impedance': 293.02,
            'Color': '[0,255,255]' } #Cyan

        with open(self.fluidPath, 'w') as configfile:
            config.write(configfile)
        
    def reset_library_to_default(self):
        self.default_fluid_library()
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