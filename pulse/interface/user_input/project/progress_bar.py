from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from pulse import UI_DIR
from pulse.interface.formatters.icons import *


class ProgressBar(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        uic.loadUi(UI_DIR / "project/progress_bar2.ui", self)

        self._load_icons()
        self._config_window()        
        self._initialize()
        self._define_qt_variables()
        self.show()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle("Loading project")
        self.setWindowIcon(self.icon)

    def _initialize(self):
        pass

    def _define_qt_variables(self):
        # self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        self.progress_bar = self.findChild(QProgressBar, 'progress_bar')
        self.timer = QTimer()
        self.timer.timeout.connect(self.close_window)

    def set_bar_data(self, message, value):
        self.label_message.setText(message)
        self.progress_bar.setValue(value)
        # sleep(0.5)
        # if value == 100:
        self.timer.start(300)        

    def close_window(self):
        self.timer.stop()
        # self.close()