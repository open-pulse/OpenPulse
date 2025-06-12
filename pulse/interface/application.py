from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

from pulse import ICON_DIR, UI_DIR, TEMP_PROJECT_FILE, FONT_DIR
from pulse.interface.main_window import MainWindow
from pulse.interface.others.splash_screen import SplashScreen

from pulse.project.config import Config
from pulse.project.project import Project
from pulse.project.load_project import LoadProject
from pulse.interface.file.project_file import ProjectFile

class Application(QApplication):
    selection_changed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        QFontDatabase.addApplicationFont(str(FONT_DIR / "bauhaus93.ttf"))

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()

        # global params
        self.config = Config()
        self.project = Project()

        # temporary solution
        self.project.initialize_pulse_file_and_loader()

        # gui
        self.main_window = MainWindow()
        self.main_window.configure_window()