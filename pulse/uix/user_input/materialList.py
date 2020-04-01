from PyQt5.QtWidgets import QDialog, QPushButton, QTreeWidget, QTreeWidgetItem
from os.path import basename
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import QBrush, QColor

from pulse.preprocessing.material import Material

class MaterialList(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path = kwargs.get("material_path", "material_library.dat")
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
        pass

    def material_select(self):
        if self.current_item is None:
            return
        
        new_material = Material(self.current_item.text(0), float(self.current_item.text(2)), 
                            young_modulus=float(self.current_item.text(3)), 
                            poisson_ratio=float(self.current_item.text(4)), 
                            color=self.current_item.text(5))
        self.material = new_material
        self.close()

    def material_close(self):
        self.close()

    def on_click_item(self, item):
        self.current_item = item

    def load(self, path):
        imported_library = np.loadtxt(path, dtype=str, skiprows=1, delimiter=";")
        name = np.array(imported_library[:,0])
        material_ID = np.array(imported_library[:,1], dtype=int)
        density = np.array(imported_library[:,2], dtype=float)
        YoungModulus = np.array(imported_library[:,3], dtype=float)
        poisson = np.array(imported_library[:,4], dtype=float)
        color = np.array(imported_library[:,5])
        for i in range(len(material_ID)):
            load_material = QTreeWidgetItem([str(name[i]).strip(), str(material_ID[i]).strip(), str(density[i]).strip(), str(YoungModulus[i]).strip(), str(poisson[i]).strip(), str(color[i]).strip()])
            #load_material.setForeground(0,QBrush(QColor(255, 0, 0, 255)))
            self.treeWidget.addTopLevelItem(load_material)