from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

# from pulse.preprocessing.element import Element

class EdgesWidget(QTreeWidget):
    """MenuInfo Widget

    This class is responsible for building a small area below of the item menu
    when some item is clicked. This has been replaced for QDialog windows and currently isn't used.

    """
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
        for key, edge in self.edges.items():
            index = str(key)
            point1 = str(edge.first_node)
            point2 = str(edge.last_node)

            item = QTreeWidgetItem([str(index), str(point1), str(point2)])
            self.addTopLevelItem(item)
