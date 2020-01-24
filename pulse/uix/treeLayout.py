from PyQt5 import Qt

#Temp
from os.path import expanduser
from PyQt5.QtWidgets import *

class TreeLayout(Qt.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.tabWidget = Qt.QTabWidget()
        self.__addTabs()
        self.addWidget(self.tabWidget)

    def __addTabs(self):

        btn1 = Qt.QPushButton("Import <test>")
        btn1.clicked.connect(self.getfiles)
        self.tabWidget.addTab(btn1, "Tab 2")

        label2 = Qt.QLabel("Apenas um teste aleatorio")
        self.tabWidget.addTab(label2, "Tab 2")
        
    def getfiles(self):
        fileName = Qt.QFileDialog.getOpenFileName(None, 'Open file', '')
        if fileName:
            print(fileName[0])