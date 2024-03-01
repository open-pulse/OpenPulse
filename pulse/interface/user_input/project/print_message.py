from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QProgressBar, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

from pathlib import Path
from time import sleep, time 

class PrintMessageInput(QDialog):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/print_message.ui"
        uic.loadUi(ui_path, self)

        self.auto_close = kwargs.get("auto_close", False)
        self.window_title, self.title, self.message = text_info

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._set_texts()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        # QFrame
        self.frame_button = self.findChild(QFrame, 'frame_button')
        self.frame_message = self.findChild(QFrame, 'frame_message')
        self.frame_progress_bar = self.findChild(QFrame, 'frame_progress_bar')
        self.frame_title = self.findChild(QFrame, 'frame_title')
        if self.auto_close:
            self.frame_button.setVisible(False)
        else:
            self.frame_progress_bar.setVisible(False)
        # QLabel
        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        # QProgressBar
        self.progress_bar_timer = self.findChild(QProgressBar, 'progress_bar_timer')
        # QPushButton
        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.setVisible(True)
        # QTimer
        self.timer = QTimer()

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.message_close)
        self.timer.timeout.connect(self.update_progress_bar)

    def message_close(self):
        self.timer.stop()
        self.close()

    def update_progress_bar(self):
        self.timer.stop()
        t0 = time()
        dt = 0
        duration = 2.5
        while dt <= duration:
            sleep(0.1)
            dt = time() - t0
            value = int(100*(dt/duration))
            self.progress_bar_timer.setValue(value)
        self.close()

    def _set_texts(self):
        self.title2 = f"   {self.title}   "
        self.label_message.setMargin(12)
        self.label_title.setText(self.title2)
        self.label_message.setText(self.message)
        self.setWindowTitle(self.window_title)
        self.adjustSize()
        self.label_message.setAlignment(Qt.AlignCenter)
        if self.auto_close:
            self.timer.timeout.connect(self.message_close)
            self.timer.start(50) 

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.message_close()
        elif event.key() == Qt.Key_Escape:
            self.close()