from PySide6.QtCore import Signal
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from pulse import FONT_DIR
from pulse.interface.others.splash_screen import SplashScreen


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
        from pulse.project.config import Config

        self.config = Config()

        from pulse.project.project import Project

        self.project = Project()

        # temporary solution
        self.project.initialize_pulse_file_and_loader()

        # gui
        from pulse.interface.main_window import MainWindow

        self.main_window = MainWindow()
        self.main_window.configure_window()
