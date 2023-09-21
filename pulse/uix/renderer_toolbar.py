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
        view_up_icon = QIcon(str(Path("data/icons/top.png")))
        self.view_up_action = QAction(view_up_icon, "Up View", self)
        self.view_up_action.triggered.connect(self.view_up_callback)
        self.view_up_action.setShortcut("Ctrl+Shift+1")

        view_down_icon = QIcon(str(Path("data/icons/bottom.png")))
        self.view_down_action = QAction(view_down_icon, "Down View", self)
        self.view_down_action.triggered.connect(self.view_down_callback)
        self.view_down_action.setShortcut("Ctrl+Shift+2")

        view_right_icon = QIcon(str(Path("data/icons/right.png")))
        self.view_right_action = QAction(view_right_icon, "Right View", self)
        self.view_right_action.triggered.connect(self.view_right_callback)
        self.view_right_action.setShortcut("Ctrl+Shift+4")

        view_left_icon = QIcon(str(Path("data/icons/left.png")))
        self.view_left_action = QAction(view_left_icon, "Left View", self)
        self.view_left_action.triggered.connect(self.view_left_callback)
        self.view_left_action.setShortcut("Ctrl+Shift+3")

        view_back_icon = QIcon(str(Path("data/icons/back.png")))
        self.view_back_action = QAction(view_back_icon, "Back View", self)
        self.view_back_action.triggered.connect(self.view_back_callback)
        self.view_back_action.setShortcut("Ctrl+Shift+6")

        view_front_icon = QIcon(str(Path("data/icons/front.png")))
        self.view_front_action = QAction(view_front_icon, "Front View", self)
        self.view_front_action.triggered.connect(self.view_front_callback)
        self.view_front_action.setShortcut("Ctrl+Shift+5")

        view_orthogonal_icon = QIcon(str(Path("data/icons/orthogonal.png")))
        self.view_orthogonal_action = QAction(view_orthogonal_icon, "Orthogonal View", self)
        self.view_orthogonal_action.triggered.connect(self.view_orthogonal_callback)
        self.view_orthogonal_action.setShortcut("Ctrl+Shift+7")

    def configure_layout(self):
        self.addSeparator()
        self.addAction(self.view_up_action)
        self.addAction(self.view_down_action)
        self.addAction(self.view_right_action)
        self.addAction(self.view_left_action)
        self.addAction(self.view_front_action)
        self.addAction(self.view_back_action)
        self.addAction(self.view_orthogonal_action)

    # Callbacks
    def view_up_callback(self):
        self.main_window.cameraTop_call()

    def view_down_callback(self):
        self.main_window.cameraBottom_call()

    def view_left_callback(self):
        self.main_window.cameraLeft_call()

    def view_right_callback(self):
        self.main_window.cameraRight_call()

    def view_front_callback(self):
        self.main_window.cameraFront_call()

    def view_back_callback(self):
        self.main_window.cameraBack_call()

    def view_orthogonal_callback(self):
        self.main_window.cameraIsometric_call()
