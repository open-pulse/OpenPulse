from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QLabel, QProgressBar, QSplashScreen

from pulse import ICON_DIR, UI_DIR, FONT_DIR, app

from molde import load_ui

from time import time

class SplashScreen(QSplashScreen):
    def __init__(self, parent):
        super().__init__()

        ui_path = UI_DIR / "project/splash.ui"
        load_ui(ui_path, self, UI_DIR)

        self._config_widget()
        self._define_qt_variables()
        self._config_logo_label()
        self.update_position(parent)
        self.update_progress(5)

    def _config_widget(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.progressBar.setStyleSheet( """  QProgressBar{background-color : rgba(255, 255, 255, 0); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                             QProgressBar::chunk {background-color : rgb(45, 110, 190); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                        """)

    def _define_qt_variables(self):
        self.label_loading : QLabel
        self.logo_label: QLabel
        self.progressBar : QProgressBar
    
    def _config_logo_label(self):
        logo_text = f"""<html><head/><body style=\" font-size:60pt; font-family: 'Bauhaus 93'\"><p align="center"><span style=\"
            color:#0055ff;\">O</span><span style=\" color:#c8c8c8;\">pen</span><span style=\"
            color:#0055ff;\">P</span><span style=\" color:#c8c8c8;\">ulse</span></p></body></html>"""        

        self.logo_label.setText(logo_text)       

    def update_position(self, app):
        desktop_geometry = app.primaryScreen().geometry()
        pos_x = int((desktop_geometry.width() - self.width())/2)
        pos_y = int((desktop_geometry.height() - self.height())/2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def update_progress(self, value : int):
        self.progressBar.setValue(value)