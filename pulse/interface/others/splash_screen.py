from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QProgressBar, QSplashScreen

from pulse import ICON_DIR, UI_DIR

from molde import load_ui

from time import time

class SplashScreen(QSplashScreen):
    def __init__(self, parent):
        super().__init__()

        ui_path = UI_DIR / "project/splash.ui"
        load_ui(ui_path, self, UI_DIR)

        self._config_widget()
        self._define_qt_variables()
        self.update_position(parent)
        self.update_progress(5)

        # pixmap = QPixmap(str(ICON_DIR / "logos/OpenPulse_logo_gray.png"))
        # self.setPixmap(QPixmap())

    def _config_widget(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.progressBar.setStyleSheet( """  QProgressBar{background-color : rgba(255, 255, 255, 0); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                             QProgressBar::chunk {background-color : rgb(45, 110, 190); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                        """)

    def _define_qt_variables(self):
        self.label_loading : QLabel
        self.progressBar : QProgressBar

    def update_position(self, app):
        desktop_geometry = app.primaryScreen().geometry()
        pos_x = int((desktop_geometry.width() - self.width())/2)
        pos_y = int((desktop_geometry.height() - self.height())/2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def update_progress(self, value : int):
        self.progressBar.setValue(value)