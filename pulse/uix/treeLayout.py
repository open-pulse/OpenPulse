from PyQt5 import Qt

#Temp
from os.path import expanduser
from PyQt5.QtWidgets import *

class TreeLayout(Qt.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.magic = Qt.QWidget()
        self.layout = Qt.QVBoxLayout()
        self.magic.setLayout(self.layout)

        self.tabWidget = Qt.QTabWidget()
        self.tabWidget.addTab(self.magic, "Import")
        self.addWidget(self.tabWidget)
        self.add_import_button()

    def clearLayout(self):
        for i in range(self.layout.count()):
            self.layout.itemAt(i).widget().close()

    def add_import_button(self):
        space = Qt.QWidget()
        widget = Qt.QPushButton("Import <test>")
        widget.clicked.connect(self.getfiles)
        self.layout.addWidget(widget, 1)
        self.layout.addWidget(space, 100)

    def getfiles(self):
        fileName = Qt.QFileDialog.getOpenFileName(None, 'Open file', '')
        self.clearLayout()
        self.create_tree(fileName[0])

    def create_tree(self, txt):
        tw = Qt.QTreeWidget()
        tw.setColumnCount(1)
        tw.setHeaderLabels([txt])

        l1 = Qt.QTreeWidgetItem(["Mesh"])
        l2 = Qt.QTreeWidgetItem(["Gerar Mesh"])
        l1.addChild(l2)
        tw.itemClicked.connect(self.onClickItem)
        
        tw.addTopLevelItem(l1)
        self.layout.addWidget(tw)

    def onClickItem(self, item, column):
        if item.text(0) == "Gerar Mesh":
            self.parent._import()
        print(item.text(0), item, column)