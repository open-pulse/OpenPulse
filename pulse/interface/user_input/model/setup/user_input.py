from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtGui import QColor, Qt, QCloseEvent

from pulse import app
from pulse.interface.formatters import icons

from molde.colors import color_names

from abc import ABC, abstractmethod


class UserInput(ABC, QDialog):

    def __init__(self):
        super().__init__()

        self._config_window()
        self._paint_icons()

        app().main_window.theme_changed.connect(self.paint_icons)
    
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")


    def paint_icons(self):
        theme = self.config.user_preferences.interface_theme

        if theme == "dark":
            icon_color = QColor(color_names.BLUE_6.to_hex())

        elif theme == "light":
            icon_color = QColor(color_names.BLUE_4.to_hex())

        widgets = self.findChildren(QWidget)

        icons.change_icon_color_for_widgets(widgets, icon_color)
    
    @abstractmethod
    def selection_callback(self):
        pass
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        app().main_window.selection_changed.disconnect(self.selection_callback)
        return super().closeEvent(a0)