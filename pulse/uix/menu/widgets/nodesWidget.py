from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *

class NodesWidget(QTreeWidget):
    """MenuInfo Widget

    This class is responsible for building a small area below of the item menu
    when some item is clicked. This has been replaced for QDialog windows and currently isn't used.

    """
    def __init__(self, nodes):
        super().__init__()
        self.nodes = nodes
        self._set_config()
        self._create_widgets()

    def _set_config(self):
        self.setColumnCount(4)
        self.setColumnWidth(0, 50)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 70)
        self.setHeaderLabels(["ID", "x", "y", "z"])

    def _create_widgets(self):
        for node in self.nodes:
            index = str(node[0])
            x = str(node[1])
            y = str(node[2])
            z = str(node[3])

            item = QTreeWidgetItem([str(index), str(x), str(y), str(z)])
            self.addTopLevelItem(item)
