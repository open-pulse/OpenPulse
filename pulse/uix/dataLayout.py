from PyQt5 import Qt

#Temp
from os.path import expanduser
from PyQt5.QtWidgets import *

class DataLayout(Qt.QVBoxLayout):
    def __init__(self):
        super().__init__()
        
        home_directory = expanduser('~')
        model = Qt.QDirModel()
        tree = Qt.QTreeView()
        tree.setModel(model)
        tree.setRootIndex(model.index(home_directory))
        self.addWidget(tree)