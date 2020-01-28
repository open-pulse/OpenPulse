from PyQt5 import Qt
import numpy as np
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

        self.importPath = ""

    def _import(self):
        self.dataLayout.add_mesh_input()

    def setImportPath(self, path):
        self.importPath = path

    def getImportPath(self):
        return self.importPath

    def _data_hidden(self):
        self.dataLayout.hidden()

    def import_from_main(self):
        self.treeLayout.getfiles()

    def plot(self):
        coordinates = np.array(self.dataLayout.getMesh().nodes)
        connectivity = np.array(self.dataLayout.getMesh().edges, int)
        self.parent.change_plot(coordinates, connectivity)

    def list_nodes(self):
        self.dataLayout.list_nodes()

    def list_edges(self):
        self.dataLayout.list_edges()