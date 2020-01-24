from PyQt5 import Qt
from .dataLayout import DataLayout
from .treeLayout import TreeLayout

class InfoLayout(Qt.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.dataLayout = DataLayout()
        self.treeLayout = TreeLayout()
        self.addLayout(self.treeLayout)
        self.addLayout(self.dataLayout)