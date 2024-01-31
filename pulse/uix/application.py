from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.toolboxes import GeometryToolbox
from pulse.interface.main_window import MainWindow

from pulse.project import Project
from pulse.uix.config import Config

class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = Config()
        self.project = Project()
        self.geometry_toolbox = GeometryToolbox()

        self.main_window = MainWindow()
        self.main_window.show()
        self.update()

    def update(self):
        self.geometry_toolbox.update()
