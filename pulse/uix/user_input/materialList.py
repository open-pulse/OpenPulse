from PyQt5.QtWidgets import QDialog, QPushButton, QTreeWidget, QTreeWidgetItem
from os.path import basename
from PyQt5 import uic

class MaterialList(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/materialList.ui', self)

        self.button_insert_material = self.findChild(QPushButton, 'button_insert_material')
        self.button_close = self.findChild(QPushButton, 'button_close')
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget.itemClicked.connect(self.on_click_item)

        self.button_insert_material.clicked.connect(self.material_insert)
        self.button_close.clicked.connect(self.material_close)

        hiden_data = QTreeWidgetItem(["Sei lá", "1", "2.222", "3.33", "444.3", "#FFF555"])
        self.treeWidget.addTopLevelItem(hiden_data)

        self.exec_()
        
    def material_insert(self):
        pass

    def material_close(self):
        self.close()

    def on_click_item(self):
        print("coe")