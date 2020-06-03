from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from os.path import basename
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
        self.fluid= None
        self.flagAll = False
        self.flagEntity = False
        self.colors = []

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.setColumnWidth(1, 20)
        self.treeWidget.setColumnWidth(5, 30)
        self.treeWidget.setColumnWidth(3, 180)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.lineEdit_name = self.findChild(QLineEdit, 'lineEdit_name')
        self.lineEdit_id = self.findChild(QLineEdit, 'lineEdit_id')
        self.lineEdit_density = self.findChild(QLineEdit, 'lineEdit_fluid_density')
        self.lineEdit_sound_velocity = self.findChild(QLineEdit, 'lineEdit_sound_velocity')
        self.lineEdit_impedance = self.findChild(QLineEdit, 'lineEdit_impedance')
        self.lineEdit_color = self.findChild(QLineEdit, 'lineEdit_color')

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.pushButton_addFluid = self.findChild(QPushButton, 'pushButton_addFluid')
        self.pushButton_addFluid.clicked.connect(self.check_addFluid)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

        self.loadList()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

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
                self.colors.append(colorRGB)
                load_fluid.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_fluid.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_fluid)
            self.ID = identifier
        except Exception as e:
            error(str(e), "Error while loading the fluid list")
            self.close()
        
    def check_addFluid(self):
        if self.lineEdit_name.text() == "":
            error("Insert a fluid name!")
            return
        if self.lineEdit_id.text() == "":
            error("Insert a fluid ID!")
            return
        if self.lineEdit_fluid_density.text() == "":
            error("Insert a fluid density!")
            return
        if self.lineEdit_sound_velocity.text() == "":
            error("Insert a sound velocity!")
            return
        if self.lineEdit_impedance.text() == "":
            error("Insert an acoustic_impedance!")
            return
        if self.lineEdit_color.text() == "":
            error("Insert a fluid Color!")
            return
        else:

            name = self.lineEdit_name.text()

            try:
                if int(self.lineEdit_id.text())>int(self.ID):
                    identifier = str(self.lineEdit_id.text())
                else:
                    error(("Input ID must be greater than {}").format(self.ID))
                    return
            except Exception:
                error("Invalid ID input value")
                return

            try:
                if float(self.lineEdit_fluid_density.text())>0:
                    fluid_density = str(self.lineEdit_fluid_density.text())
            except Exception:
                error("Invalid Fluid Density input value")
                return

            try:
                if float(self.lineEdit_sound_velocity.text())>0:
                    sound_velocity = str(self.lineEdit_sound_velocity.text())
            except Exception:
                error("Invalid Sound Velocity input value)")
                return

            try:
                if float(self.lineEdit_impedance.text())>0:
                    impedance = str(self.lineEdit_impedance.text())
            except Exception:
                error(" The input value for Poisson must be\n a positive float number less than 0.5")
                return   

            color = self.lineEdit_color.text()
            message = " Invalid color RGB input!\n You must input: [value1, value2, value3]"

            try:
                colorRGB = getColorRGB(color)

                if len(colorRGB)!=3:
                    error(message)
                    return
                elif colorRGB in self.colors:
                    error((" The RGB color {} was already used.\n Please, input a different color.").format(colorRGB))
                    return
                else:
                    self.colors.append(colorRGB)
            except:
                error(message)
                return

            load_material = QTreeWidgetItem([name, identifier, fluid_density, sound_velocity, impedance, color])
            load_material.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            self.treeWidget.addTopLevelItem(load_material)
            self.ID = int(self.ID)+1

            try:
                config = configparser.ConfigParser()
                config.read(self.fluidPath)
                config[name.upper()] = {
                'Name': name,
                'Identifier': identifier,
                'Fluid density': fluid_density,
                'Sound velocity': sound_velocity,
                'Impedance': impedance,
                'Color': color
                }
                     
            except Exception as e:
                error(str(e), "Error while loading the material list")
                return

            with open(self.fluidPath, 'w') as configfile:
                config.write(configfile)

    def on_click_item(self, item):
        self.clicked_item = item

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.check()
    
    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()


