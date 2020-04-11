from PyQt5.QtWidgets import QDialog, QPushButton, QTreeWidget, QTreeWidgetItem
from pulse.uix.user_input.materialInput import MaterialInput
from os.path import basename
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import QBrush, QColor
import configparser

from pulse.preprocessing.material import Material

class MaterialList(QDialog):
    def __init__(self, material_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = material_path
        self.current_item = None
        self.material = None
        uic.loadUi('pulse/uix/user_input/ui/materialList.ui', self)

        self.button_insert_material = self.findChild(QPushButton, 'button_insert_material')
        self.button_select_material = self.findChild(QPushButton, 'button_select_material')
        self.button_close = self.findChild(QPushButton, 'button_close')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.itemClicked.connect(self.on_click_item)

        self.button_insert_material.clicked.connect(self.material_insert)
        self.button_select_material.clicked.connect(self.material_select)
        self.button_close.clicked.connect(self.material_close)

        self.load(self.path)

        self.exec_()
        
    def material_insert(self):
        if MaterialInput(self.path):
            self.treeWidget.clear()
            self.load(self.path)


    def material_select(self):
        if self.current_item is None:
            return
        
        new_material = Material(self.current_item.text(0), float(self.current_item.text(2)), 
                            young_modulus=float(self.current_item.text(3))*(10**(9)), 
                            poisson_ratio=float(self.current_item.text(4)), 
                            color=self.current_item.text(5),
                            identifier=int(self.current_item.text(1)))
        self.material = new_material
        self.close()

    def material_close(self):
        self.close()

    def on_click_item(self, item):
        self.current_item = item

    def load(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        for mat in config.sections():
            name = str(config[mat]['name'])
            identifier =  str(config[mat]['identifier'])
            density =  str(config[mat]['density'])
            youngmodulus =  str(config[mat]['youngmodulus'])
            poisson =  str(config[mat]['poisson'])
            color =  str(config[mat]['color'])
            load_material = QTreeWidgetItem([name, identifier, youngmodulus, density, poisson, color])
            #Colorir
            colorRGB = self.getColorRGB(color)
            # load_material.setForeground(0,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            # load_material.setForeground(1,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            # load_material.setForeground(2,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            # load_material.setForeground(3,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            # load_material.setForeground(4,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            load_material.setForeground(5,QBrush(QColor(colorRGB[0], colorRGB[1], colorRGB[2])))
            self.treeWidget.addTopLevelItem(load_material)

    def getColorRGB(self, color):
        temp = color[1:-1] #Remove "[ ]"
        tokens = temp.split(',')
        return list(map(int, tokens))