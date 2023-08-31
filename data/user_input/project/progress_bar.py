from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

from time import time, sleep
import os

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class ProgressBar(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()
        uic.loadUi(Path('data/user_input/ui_files/Project/progress_bar2.ui'), self)
        
        self.icon = QIcon(get_icons_path('pulse.png'))
        self.setWindowIcon(self.icon)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle("Loading project")

        self._reset_variables()
        self._define_qt_variables()
        self.show()
        # self.exec()

    def _reset_variables(self):
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