from PyQt5 import Qt

#Temp
from os.path import expanduser
import numpy as np
from pulse.mesh import Mesh

from PyQt5.QtWidgets import *
#from PyQt5.QtCore import AlignCenter

class DataLayout(Qt.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.magic = Qt.QWidget()
        self.layout = Qt.QVBoxLayout()
        self.magic.setLayout(self.layout)

        self.mesh = Mesh()

        self.tabWidget = Qt.QTabWidget()
        self.tabWidget.addTab(self.magic, "Data")
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.hidden)
        self.addWidget(self.tabWidget)
        self.hidden()

    def hidden(self, index = -1):
        self.tabWidget.setTabText(0, "Data")
        self.tabWidget.hide()

    def show(self):
        self.tabWidget.show()

    def clearLayout(self):
        for i in range(self.layout.count()):
            if (type(self.layout.itemAt(i)) == Qt.QHBoxLayout):
                self.layout.clearLayout(self.layout.itemAt(i))
            else:
                self.layout.itemAt(i).widget().close()

    def add_mesh_input(self, value = "", badInput = False, finished = False):
        self.clearLayout()
        self.show()
        self.tabWidget.setTabText(0, "Generate")
        text = Qt.QLineEdit()
        text.setValidator(Qt.QDoubleValidator(text))
        text.setText(value)

        buttons = Qt.QWidget()
        buttons_layout = Qt.QHBoxLayout()
        buttons.setLayout(buttons_layout)
        cancel_button = Qt.QPushButton("Cancel")
        cancel_button.clicked.connect(self.mesh_cancel)

        ok_button = Qt.QPushButton("Mesh")
        ok_button.clicked.connect(lambda: self.mesh_ok(text.text()))

        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(ok_button)

        label = Qt.QLabel("Element Size")

        self.layout.addWidget(label)
        self.layout.addWidget(text)
        self.layout.addWidget(buttons)

        if badInput:
            label_badinput = Qt.QLabel("Insert a Valid Input!")
            self.layout.addWidget(label_badinput)
        if finished:
            label_finished = Qt.QLabel("Done.")
            self.layout.addWidget(label_finished)


        space = Qt.QWidget()
        self.layout.addWidget(space, 100)

    def mesh_cancel(self):
        self.hidden()

    def mesh_ok(self, value):
        try:
            self.mesh.generate(self.parent.getImportPath(),0,float(value))
            self.add_mesh_input(value, False, True)
        except:
            self.add_mesh_input(value, True)


    def getMesh(self):
        return self.mesh

    def list_nodes(self):
        self.clearLayout()
        self.show()
        nodes = Qt.QTreeWidget()
        nodes.setColumnCount(4)
        nodes.setColumnWidth(0, 50)
        nodes.setColumnWidth(1, 70)
        nodes.setColumnWidth(2, 70)
        nodes.setColumnWidth(3, 70)
        nodes.setHeaderLabels(["ID", "x", "y", "z"])
        for i in self.mesh.nodes:
            id_ = str(int(i[0]))
            x_ = str(i[1])
            y_ = str(i[2])
            z_ = str(i[3])
            temp = Qt.QTreeWidgetItem([id_, x_, y_, z_])
            nodes.addTopLevelItem(temp)
        self.layout.addWidget(nodes)

    def list_edges(self):
        self.clearLayout()
        self.show()
        edges = Qt.QTreeWidget()
        edges.setColumnCount(3)
        edges.setColumnWidth(0, 50)
        edges.setColumnWidth(1, 70)
        edges.setColumnWidth(2, 70)
        edges.setHeaderLabels(["ID", "Point 1", "Point 2"])
        for i in self.mesh.edges:
            id_ = str(int(i[0]))
            p1_ = str(i[1])
            p2_ = str(i[2])
            temp = Qt.QTreeWidgetItem([id_, p1_, p2_])
            edges.addTopLevelItem(temp)
        self.layout.addWidget(edges)