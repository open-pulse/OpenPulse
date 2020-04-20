from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem
from os.path import basename
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

        self.clicked_item = None
        self.material = None
        self.flagAll = False
        self.flagEntity = False

        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.setColumnWidth(1, 20)
        self.treeWidget.setColumnWidth(5, 30)
        self.treeWidget.setColumnWidth(3, 180)
        self.treeWidget.itemClicked.connect(self.on_click_item)
        self.treeWidget.itemDoubleClicked.connect(self.on_doubleclick_item)

        self.radioButton_all = self.findChild(QRadioButton, 'radioButton_all')
        self.radioButton_entity = self.findChild(QRadioButton, 'radioButton_entity')
        self.radioButton_all.toggled.connect(self.radioButtonEvent)
        self.radioButton_entity.toggled.connect(self.radioButtonEvent)

        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()

        self.loadList()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.check()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def error(self, msg, title = "Error"):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(msg)
        msg_box.setWindowTitle(title)
        msg_box.exec_()

    def check(self):
        if self.clicked_item is None:
            self.error("Select a material in the list")
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
            self.error(str(e), "Error with the material list data")
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
                youngmodulus =  str(material['youngmodulus'])
                poisson =  str(material['poisson'])
                color =  str(material['color'])

                load_material = QTreeWidgetItem([name, identifier, density, youngmodulus, poisson, color])
                colorRGB = self.getColorRGB(color)
                load_material.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_material)
        except Exception as e:
            self.error(str(e), "Error while loading the material list")
            self.close()
        
    def getColorRGB(self, color):
        temp = color[1:-1] #Remove "[ ]"
        tokens = temp.split(',')
        return list(map(int, tokens))

    def on_click_item(self, item):
        self.clicked_item = item

    def on_doubleclick_item(self, item):
        self.clicked_item = item
        self.check()
    
    def radioButtonEvent(self):
        self.flagAll = self.radioButton_all.isChecked()
        self.flagEntity = self.radioButton_entity.isChecked()