from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QMessageBox, QTreeWidgetItem, QPushButton
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser

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

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check)

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
            self.error("Select a fluid in the list")
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
            self.error(str(e), "Error with the fluid list data")
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
                colorRGB = self.getColorRGB(color)
                load_fluid.setBackground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                load_fluid.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
                self.treeWidget.addTopLevelItem(load_fluid)
        except Exception as e:
            self.error(str(e), "Error while loading the fluid list")
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


