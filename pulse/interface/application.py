from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

from pulse import FONT_DIR
from pulse.interface.others.splash_screen import SplashScreen


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        QFontDatabase.addApplicationFont(str(FONT_DIR / "bauhaus93.ttf"))

        # create the splash screen
        self.splash = SplashScreen(self)
        self.splash.show()
        self.processEvents()
        self.filter_scroll_by_wheel_event()

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
    
    def filter_scroll_by_wheel_event(self):
        from PySide6.QtCore import QEvent, QObject
        from PySide6.QtWidgets import QComboBox

        class Filter(QObject):
            def eventFilter(self, obj, event):
                if event.type() != QEvent.Wheel:
                    return False
                
                if isinstance(obj, QComboBox):
                    return True
                
                return False

        filter = Filter(self)
        self.installEventFilter(filter)
