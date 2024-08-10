from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from pulse import ICON_DIR, UI_DIR
from pulse.interface.main_window import MainWindow
from pulse.interface.others.splash_screen import SplashScreen

from pulse.project.config import Config
from pulse.project.project import Project
from pulse.interface.file.project_file import ProjectFile
from pulse.project.load_project import LoadProject

from opps.interface.toolboxes import GeometryToolbox


class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        self.config = Config()
        self.file = ProjectFile()
        self.project = Project()
        self.loader = LoadProject()

        # gui
        self.main_window = MainWindow()
        self.main_window.configure_window()
        self.main_window.update_plots()