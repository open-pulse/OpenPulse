from PyQt5 import Qt
from .dataLayout import DataLayout
from .treeLayout import TreeLayout

class InfoLayout(Qt.QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.dataLayout = DataLayout(self)
        self.treeLayout = TreeLayout(self)
        self.addLayout(self.treeLayout)
        self.addLayout(self.dataLayout)

    def _import(self):
        self.dataLayout.add_mesh_input()

    def import_from_main(self):
        self.treeLayout.getfiles()