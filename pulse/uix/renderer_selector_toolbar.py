from pathlib import Path

from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QAction, QToolBar

class RendererSelectorToolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_window = parent

        self.create_actions()
        self.configure_layout()
        self.configure_appearance()

    def configure_appearance(self):
        self.setMovable(True)
        self.setFloatable(True)

    def create_actions(self):
        plot_geometry_icon = QIcon(str(Path("data/icons/render_selector/raw_geometry.png")))
        self.plot_geometry_action = QAction(plot_geometry_icon, "Plot geometry", self)
        self.plot_geometry_action.triggered.connect(self.plot_geometry_callback)

        plot_lines_icon = QIcon(str(Path("data/icons/render_selector/plot_lines.png")))
        self.plot_lines_action = QAction(plot_lines_icon, "Plot lines", self)
        self.plot_lines_action.triggered.connect(self.plot_lines_callback)

        plot_mesh_icon = QIcon(str(Path("data/icons/render_selector/plot_mesh.png")))
        self.plot_mesh_action = QAction(plot_mesh_icon, "Plot mesh", self)
        self.plot_mesh_action.triggered.connect(self.plot_mesh_callback)

        plot_lines_with_sections_icon = QIcon(str(Path("data/icons/render_selector/plot_lines_with_sections.png")))
        self.plot_lines_with_sections_action = QAction(plot_lines_with_sections_icon, "Plot lines with sections", self)
        self.plot_lines_with_sections_action.triggered.connect(self.plot_lines_with_sections_callback)

    def configure_layout(self):
        self.addSeparator()
        self.addAction(self.plot_geometry_action)
        self.addAction(self.plot_lines_action)
        self.addAction(self.plot_mesh_action)
        self.addAction(self.plot_lines_with_sections_action)
        self.addSeparator()
        
    def plot_geometry_callback(self):
        self.main_window.plot_raw_geometry()

    def plot_lines_callback(self):
        self.main_window.plot_entities()

    def plot_mesh_callback(self):
        self.main_window.plot_mesh()

    def plot_lines_with_sections_callback(self):
        self.main_window.plot_entities_with_cross_section()