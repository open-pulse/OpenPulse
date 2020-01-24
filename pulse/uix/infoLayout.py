from PyQt5 import Qt
from .dataLayout import DataLayout
from .treeLayout import TreeLayout

class InfoLayout(Qt.QVBoxLayout):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.dataLayout = DataLayout(self)
        self.treeLayout = TreeLayout(self)
        self.addLayout(self.treeLayout)
        self.addLayout(self.dataLayout)

    def _import(self):
        self.dataLayout.add_mesh_input()

    def _data_hidden(self):
        self.dataLayout.hidden()

    def import_from_main(self):
        self.treeLayout.getfiles()