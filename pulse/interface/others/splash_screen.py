from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from pulse import ICON_DIR
from pulse.interface.ui_generated.project.splash_ui import Splash_UI


class SplashScreen(Splash_UI):
    def __init__(self, parent):
        super().__init__()

        self._config_widget()
        self._config_logo_label()
        self.update_position(parent)
        self.update_progress(5)

    def _config_widget(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.progressBar.setStyleSheet( """  QProgressBar{background-color : rgba(255, 255, 255, 0); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                             QProgressBar::chunk {background-color : rgb(45, 110, 190); border-radius: 6px; border-style: ridge; border-width: 0px;}
                                        """)

    def _config_logo_label(self):
        logo_path = ICON_DIR / "logos/op_dark_theme.png"
        pixmap = QPixmap(str(logo_path))

        dpr = self.devicePixelRatioF()
        pixmap = pixmap.scaledToWidth(int(360 * dpr), Qt.SmoothTransformation)
        pixmap.setDevicePixelRatio(dpr)

        self.logo_label.setPixmap(pixmap)

    def update_position(self, qt_app):
        desktop_geometry = qt_app.primaryScreen().geometry()
        pos_x = int((desktop_geometry.width() - self.width())/2)
        pos_y = int((desktop_geometry.height() - self.height())/2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def update_progress(self, value : int):
        self.progressBar.setValue(value)