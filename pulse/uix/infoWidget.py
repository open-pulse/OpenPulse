from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter

from pulse.uix.dataWidget import DataWidget
from pulse.uix.treeWidget import TreeWidget
from pulse.uix.generateWidget import GenerateWidget
from pulse.uix.nodesWidget import NodesWidget
from pulse.uix.edgesWidget import EdgesWidget
from pulse.uix.plotWidget import PlotWidget

class InfoWidget(QSplitter):
    def __init__(self, main_window):
        super().__init__(Qt.Vertical)
        self.main_window = main_window
        self.tree_widget = TreeWidget(self.main_window)
        self.data_widget = DataWidget(self.main_window)

        self.addWidget(self.tree_widget)
        self.addWidget(self.data_widget)
        self.setSizes([100, 100])

    def hidden_data(self):
        pass

    def generate(self):
        generate_widget = GenerateWidget(self.main_window)
        self.data_widget.addTab(generate_widget, 'Generate')

    def list_of_nodes(self):
        nodes_widget = NodesWidget(self.main_window.project.mesh.nodes)
        self.data_widget.addTab(nodes_widget, 'Nodes')

    def list_of_connections(self):
        edges_widget = EdgesWidget(self.main_window.project.mesh.edges)
        self.data_widget.addTab(edges_widget, 'Edges')

    def plot_config(self):
        plot_widget = PlotWidget(self.main_window)
        self.data_widget.addTab(plot_widget, 'Plot')
