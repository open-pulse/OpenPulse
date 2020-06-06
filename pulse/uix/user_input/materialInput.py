from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from pulse.utils import error, isInteger, isFloat, getColorRGB
from os.path import basename
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
        self.colors = []

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

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

        self.pushButton_addMaterial = self.findChild(QPushButton, 'pushButton_addMaterial')
        self.pushButton_addMaterial.clicked.connect(self.check_addMaterial)

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
            error("Select a material in the list")
            return
        
        try:
            name = self.clicked_item.text(0)
            identifier = int(self.clicked_item.text(1))
            density = float(self.clicked_item.text(2))
            poisson = float(self.clicked_item.text(4))
            young = float(self.clicked_item.text(3))*(10**(9))
            color = self.clicked_item.text(5)
            new_material = Material(name, density, poisson_ratio=poisson, young_modulus=young, identifier=identifier, color=color)
            self.material = new_material
            self.close()
        except Exception as e:
            error(str(e), "Error with the material list data")
            return

    def loadList(self):
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
                self.colors.append(colorRGB)
                load_material.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_material)
            self.ID = identifier
        except Exception as e:
            error(str(e), "Error while loading the material list")
            print("parei aqui!")
            self.close()
        
    def check_addMaterial(self):
        if self.lineEdit_name.text() == "":
            error("Insert a material name!")
            return
        if self.lineEdit_id.text() == "":
            error("Insert a material ID!")
            return
        if self.lineEdit_density.text() == "":
            error("Insert a material density!")
            return
        if self.lineEdit_youngModulus.text() == "":
            error("Insert a material Young Modulus!")
            return
        if self.lineEdit_poisson.text() == "":
            error("Insert a material Poisson!")
            return
        if self.lineEdit_color.text() == "":
            error("Insert a material Color!")
            return
        else:

            name = self.lineEdit_name.text()

            if isInteger(self.lineEdit_id.text()):
                if int(self.lineEdit_id.text())>int(self.ID):
                    identifier = str(self.lineEdit_id.text())
                else:
                    error(("Input ID must be greater than {}").format(self.ID))
                    return
            else:
                error("Value error (ID)")
                return

            if isInteger(self.lineEdit_density.text()):
                if int(self.lineEdit_density.text())>0:
                    density = str(self.lineEdit_density.text())
            elif isFloat(self.lineEdit_density.text()):
                if float(self.lineEdit_density.text())>0:
                    density = str(self.lineEdit_density.text())
            else:
                error("Value error (Density)")
                return

            if isInteger(self.lineEdit_youngModulus.text()):
                if int(self.lineEdit_youngModulus.text())>0:
                    young_modulus = str(self.lineEdit_youngModulus.text())
            elif isFloat(self.lineEdit_youngModulus.text()):
                if float(self.lineEdit_youngModulus.text())>0:
                    young_modulus = str(self.lineEdit_youngModulus.text())
            else:
                error("Value error (Young Modulus)")
                return

            if isFloat(self.lineEdit_poisson.text()):
                if float(self.lineEdit_poisson.text())>0:
                    if float(self.lineEdit_poisson.text())<0.5:
                        poisson = str(self.lineEdit_poisson.text())
                    else:
                        error(" The input value for Poisson must be\n a positive float number less than 0.5")
                        return

            else:
                error("Value error (Poisson)")
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

            load_material = QTreeWidgetItem([name, identifier, density, young_modulus, poisson, color])
            load_material.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            self.treeWidget.addTopLevelItem(load_material)
            self.ID = int(self.ID)+1

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
                     
            except Exception as e:
                error(str(e), "Error while loading the material list")
                return

            with open(self.materialPath, 'w') as configfile:
                config.write(configfile)
            
    def on_click_item(self, item):
        self.clicked_item = item

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.check()
    
    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()