from PyQt5 import Qt

#Temp
from os.path import expanduser, basename
from PyQt5.QtWidgets import *

class TreeLayout(Qt.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.currentFileName = ""
        self.magic = Qt.QWidget()
        self.layout = Qt.QVBoxLayout()
        self.magic.setLayout(self.layout)

        self.tabWidget = Qt.QTabWidget()
        self.tabWidget.addTab(self.magic, "Import")
        self.addWidget(self.tabWidget)
        self.add_import_button()

    def reset(self):
        self.clearLayout()
        self.add_import_button()

    def clearLayout(self):
        self.tabWidget.setTabText(0,"Import")
        self.currentFileName = ""
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().close()

    def add_import_button(self):
        space = Qt.QWidget()
        widget = Qt.QPushButton("Import Geometry")
        widget.clicked.connect(self.getfiles)
        self.layout.addWidget(widget, 1)
        self.layout.addWidget(space, 100)

    def getfiles(self):
        fileName, _type = Qt.QFileDialog.getOpenFileName(None, 'Open file', '', 'Iges Files (*.iges)')
        self.clearLayout()
        self.parent.setImportPath(fileName)
        self.tabWidget.setTabText(0,basename(fileName))
        self.parent._data_hidden()
        self.create_tree()

    def create_tree(self):
        tw = Qt.QTreeWidget()
        tw.setColumnCount(1)
        tw.setHeaderLabels(["OpenPulse"])

        hidden_data = Qt.QTreeWidgetItem(["Hidden Data"])

        mesh = Qt.QTreeWidgetItem(["Mesh"])
        g_mesh = Qt.QTreeWidgetItem(["Generate"])
        nodes = Qt.QTreeWidgetItem(["List of Nodes"])
        edges = Qt.QTreeWidgetItem(["List Connections"])
        mesh.addChild(g_mesh)
        mesh.addChild(nodes)
        mesh.addChild(edges)

        opv = Qt.QTreeWidgetItem(["Graphic"])
        plot_opv = Qt.QTreeWidgetItem(["Plot"])
        opv.addChild(plot_opv)
        
        tw.addTopLevelItem(hidden_data)
        tw.addTopLevelItem(mesh)
        tw.addTopLevelItem(opv)

        tw.itemClicked.connect(self.onClickItem)
        self.layout.addWidget(tw)

    def onClickItem(self, item, column):
        if item.text(0) == "Generate":
            self.parent._import()
        elif item.text(0) == "Hidden Data":
            self.parent._data_hidden()
        elif item.text(0) == "Plot":
            self.parent.plot()
        elif item.text(0) == "List of Nodes":
            self.parent.list_nodes()
        elif item.text(0) == "List Connections":
            self.parent.list_edges()
        print(item.text(0), item, column)