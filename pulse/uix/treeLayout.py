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
        txt = Qt.QLabel(fileName[0])
        self.layout.addWidget(txt)
        space = Qt.QWidget()
        self.layout.addWidget(space, 100)
        self.parent._import()