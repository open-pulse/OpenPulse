from abc import abstractmethod

from molde.colors import color_names
from PySide6.QtGui import QCloseEvent, QColor, Qt
from PySide6.QtWidgets import QDialog, QWidget

from pulse import app
from pulse.interface.formatters import icons


class UserInput(QDialog):
    def __init__(self):
        super().__init__()

        app().main_window.set_input_widget(self)

        self._config_window()
        self._paint_icons()

        app().main_window.theme_changed.connect(self._paint_icons)

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _paint_icons(self):
        theme = app().main_window.config.user_preferences.interface_theme

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
