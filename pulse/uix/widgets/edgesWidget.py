from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

class EdgesWidget(QTreeWidget):
    def __init__(self, edges):
        super().__init__()
        self.edges = edges
        self._set_config()
        self._create_widgets()

    def _set_config(self):
        self.setColumnCount(3)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setHeaderLabels(["ID", "Point 1", "Point 2"])

    def _create_widgets(self):
        for edge in self.edges:
            index = str(edge[0])
            point1 = str(edge[1])
            point2 = str(edge[2])

            item = QTreeWidgetItem([str(index), str(point1), str(point2)])
            self.addTopLevelItem(item)
