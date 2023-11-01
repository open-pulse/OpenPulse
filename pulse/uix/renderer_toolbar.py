from pathlib import Path

from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QAction, QToolBar

class RendererToolbar(QToolBar):
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
        geometry_renderer_icon = QIcon(str(Path("data/icons/geometry.png")))
        self.geometry_renderer_action = QAction(geometry_renderer_icon, "Geometry", self)
        self.geometry_renderer_action.triggered.connect(self.geometry_renderer_callback)

        lines_renderer_icon = QIcon(str(Path("data/icons/lines.png")))
        self.lines_renderer_action = QAction(lines_renderer_icon, "Lines", self)
        self.lines_renderer_action.triggered.connect(self.lines_renderer_callback)

        lines_cross_section_renderer_icon = QIcon(str(Path("data/icons/lines_cross_section.png")))
        self.lines_cross_section_renderer_action = QAction(lines_cross_section_renderer_icon, "Lines With Cross Section", self)
        self.lines_cross_section_renderer_action.triggered.connect(self.lines_cross_section_renderer_callback)

        mesh_renderer_icon = QIcon(str(Path("data/icons/mesh.png")))
        self.mesh_renderer_action = QAction(mesh_renderer_icon, "Mesh", self)
        self.mesh_renderer_action.triggered.connect(self.mesh_renderer_callback)

        top_view_icon = QIcon(str(Path("data/icons/views/top.png")))
        self.top_view_action = QAction(top_view_icon, "Top view", self)
        self.top_view_action.triggered.connect(self.top_view_callback)
        self.top_view_action.setShortcut("Ctrl+Shift+1")

        bottom_view_icon = QIcon(str(Path("data/icons/views/bottom.png")))
        self.bottom_view_action = QAction(bottom_view_icon, "Bottom view", self)
        self.bottom_view_action.triggered.connect(self.bottom_view_callback)
        self.bottom_view_action.setShortcut("Ctrl+Shift+2")

        right_view_icon = QIcon(str(Path("data/icons/views/right.png")))
        self.right_view_action = QAction(right_view_icon, "Right view", self)
        self.right_view_action.triggered.connect(self.right_view_callback)
        self.right_view_action.setShortcut("Ctrl+Shift+4")

        left_view_icon = QIcon(str(Path("data/icons/views/left.png")))
        self.left_view_action = QAction(left_view_icon, "Left view", self)
        self.left_view_action.triggered.connect(self.left_view_callback)
        self.left_view_action.setShortcut("Ctrl+Shift+3")

        back_view_icon = QIcon(str(Path("data/icons/views/back.png")))
        self.back_view_action = QAction(back_view_icon, "Back view", self)
        self.back_view_action.triggered.connect(self.back_view_callback)
        self.back_view_action.setShortcut("Ctrl+Shift+6")

        front_view_icon = QIcon(str(Path("data/icons/views/front.png")))
        self.front_view_action = QAction(front_view_icon, "Front view", self)
        self.front_view_action.triggered.connect(self.front_view_callback)
        self.front_view_action.setShortcut("Ctrl+Shift+5")

        isometric_view_icon = QIcon(str(Path("data/icons/views/isometric.png")))
        self.isometric_view_action = QAction(isometric_view_icon, "Isometric view", self)
        self.isometric_view_action.triggered.connect(self.isometric_view_callback)
        self.isometric_view_action.setShortcut("Ctrl+Shift+7")

        clipping_plane_icon = QIcon(str(Path("data/icons/clipping_plane_icon.png")))
        self.clipping_plane_action = QAction(clipping_plane_icon, "Clipping Plane", self)
        self.clipping_plane_action.triggered.connect(self.clipping_plane_callback)
        # self.clipping_plane_action.setShortcut("Ctrl+Shift+7")


    def configure_layout(self):
        self.addAction(self.geometry_renderer_action)
        self.addAction(self.lines_renderer_action)
        self.addAction(self.lines_cross_section_renderer_action)
        self.addAction(self.mesh_renderer_action)
        self.addSeparator()
        self.addAction(self.top_view_action)
        self.addAction(self.bottom_view_action)
        self.addAction(self.right_view_action)
        self.addAction(self.left_view_action)
        self.addAction(self.front_view_action)
        self.addAction(self.back_view_action)
        self.addAction(self.isometric_view_action)
        self.addSeparator()
        self.addAction(self.clipping_plane_action)

    # Callbacks
    def top_view_callback(self):
        self.main_window.cameraTop_call()

    def bottom_view_callback(self):
        self.main_window.cameraBottom_call()

    def left_view_callback(self):
        self.main_window.cameraLeft_call()

    def right_view_callback(self):
        self.main_window.cameraRight_call()

    def front_view_callback(self):
        self.main_window.cameraFront_call()

    def back_view_callback(self):
        self.main_window.cameraBack_call()

    def isometric_view_callback(self):
        self.main_window.cameraIsometric_call()

    def clipping_plane_callback(self):
        self.main_window.inputWidget.set_clipping_plane()

    def geometry_renderer_callback(self):
        self.main_window.plot_raw_geometry()

    def lines_renderer_callback(self):
        self.main_window.plot_entities()

    def lines_cross_section_renderer_callback(self):
        self.main_window.plot_entities_with_cross_section()

    def mesh_renderer_callback(self):
        self.main_window.plot_mesh()
