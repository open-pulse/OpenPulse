from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplitter

from pulse.uix.menu import *
from pulse.uix.menu.widgets import *

class Menu(QSplitter):
    """Menu

    This class creates and configures the interface.
    Also is responsible for creating the MenuItems Object.

    """
    def __init__(self, main_window):
        super().__init__(Qt.Vertical)
        self.main_window = main_window
        self.menu_items = MenuItems(self.main_window)
        self.menu_info = MenuInfo(self.main_window, self.menu_items)
        self.addWidget(self.menu_info)
        self.addWidget(self.menu_items)
        self.setSizes([60, 800])

    def hidden_data(self):
        pass

    def generate(self):
        generate_widget = GenerateWidget(self.main_window)
        self.data_widget.addTab(generate_widget, 'Generate')

    def list_of_nodes(self):
        nodes_widget = NodesWidget(self.main_window.project.get_nodes())
        self.data_widget.addTab(nodes_widget, 'Nodes')

    def list_of_connections(self):
        edges_widget = EdgesWidget(self.main_window.project.get_structural_elements())
        self.data_widget.addTab(edges_widget, 'Edges')

    def plot_config(self):
        plot_widget = PlotWidget(self.main_window)
        self.data_widget.addTab(plot_widget, 'Plot')
