from PyQt5.QtWidgets import QLabel, QToolButton, QLineEdit, QDialogButtonBox, QDialog, QMessageBox, QTreeWidget, QTreeWidgetItem
from pulse.utils import error
from os.path import basename
from PyQt5 import uic
from PyQt5.QtGui import QBrush, QColor
import configparser

class PreProcessingInfo(QDialog):
    def __init__(self, entityPath, nodePath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/visualization.ui', self)

        self.button_box = self.findChild(QDialogButtonBox, 'info_button_box')
        self.button_box.accepted.connect(self.info_continue)
        self.button_box.rejected.connect(self.info_close)
        self.treeWidget = self.findChild(QTreeWidget, 'treeWidget')
        self.treeWidget2 = self.findChild(QTreeWidget, 'treeWidget_2')

        self.treeWidget.setColumnWidth(0, 200)
        self.treeWidget.setColumnWidth(1, 200)
        self.treeWidget.setColumnWidth(2, 200)

        self.treeWidget2.setColumnWidth(0, 200)
        self.treeWidget2.setColumnWidth(1, 200)
        self.treeWidget2.setColumnWidth(2, 200)

        self.hasError = False
        self.errorColor = QBrush(QColor(255, 0, 0))
        self.loadItems(entityPath, nodePath)

        self.exec_()

    def info_continue(self):
        if self.hasError:
            error("Material ou Cross Section não foi definido para alguma entidade", "Error")
            return
        print("Ok")
        self.close()

    def info_close(self):
        self.hasError = True
        self.close()

    def loadItems(self, entityPath, nodePath):
        self.loadLines(entityPath)
        self.loadNodes(nodePath)

    def loadLines(self, entityPath):
        entityFile = configparser.ConfigParser()
        entityFile.read(entityPath)
        for entity in entityFile.sections():
            material_id = entityFile[entity]['MaterialID']
            diam_ext = entityFile[entity]['external diam']
            diam_int = entityFile[entity]['internal diam']
            item1 = QTreeWidgetItem(["Entity ID {}".format(entity)])
            item2 = QTreeWidgetItem(["Material ID: {}".format(material_id), "Diam Ext: {}".format(diam_ext), "Diam Int: {}".format(diam_int)])

            if not material_id.isnumeric():
                item2.setForeground(0, self.errorColor)
                item1.setForeground(0, self.errorColor)
                self.hasError = True

            try:
                float(diam_ext)
            except Exception:
            # if not self.isFloat(diam_ext):
                item2.setForeground(1, self.errorColor)
                item1.setForeground(0, self.errorColor)
                self.hasError = True

            try:
                float(diam_int)
            except Exception:
            # if not self.isFloat(diam_int):
                item2.setForeground(2, self.errorColor)
                item1.setForeground(0, self.errorColor)
                self.hasError = True
                
            item1.addChild(item2)
            self.treeWidget.addTopLevelItem(item1)

    def loadNodes(self, nodePath):
        node_list = configparser.ConfigParser()
        node_list.read(nodePath)
        for node in node_list.sections():
            node_id = node
            displacement = node_list[str(node)]['displacement']
            rotation = node_list[str(node)]['rotation']
            item1 = QTreeWidgetItem([node_id, displacement, rotation])
            self.treeWidget2.addTopLevelItem(item1)