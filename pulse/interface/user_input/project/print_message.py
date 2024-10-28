from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QProgressBar, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *

from time import sleep, time 

class PrintMessageInput(QDialog):
    def __init__(self, text_info, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/print_message.ui"
        uic.loadUi(ui_path, self)

        self.auto_close = kwargs.get("auto_close", False)
        self.window_title, self.title, self.message = text_info

        app().main_window.set_input_widget(self)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._set_texts()
        self._adjust_size(kwargs)
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _define_qt_variables(self):

        # QFrame
        self.frame_button : QFrame
        self.frame_message : QFrame
        self.frame_progress_bar : QFrame
        self.frame_title : QFrame

        # QLabel
        self.label_title : QLabel
        self.label_message : QLabel

        # QProgressBar
        self.progress_bar_timer : QProgressBar

        # QPushButton
        self.pushButton_close : QPushButton

        # QTimer
        self.timer = QTimer()

    def _create_connections(self):
        self.pushButton_close.clicked.connect(self.message_close)
        self.timer.timeout.connect(self.update_progress_bar)

    def _config_widgets(self):

        if self.auto_close:
            self.frame_button.setVisible(False)
        else:
            self.frame_progress_bar.setVisible(False)

        self.pushButton_close.setVisible(True)

    def message_close(self):
        self.timer.stop()
        self.close()

    def update_progress_bar(self):
        self.timer.stop()
        t0 = time()
        elapsed_time = 0
        duration = 2.5
        while elapsed_time <= duration:
            sleep(0.1)
            elapsed_time = time() - t0
            value = int(100*(elapsed_time / duration))
            self.progress_bar_timer.setValue(value)
        self.close()

    def _set_texts(self):
        self.title2 = f"   {self.title}   "
        self.label_title.setText(self.title2)
        self.label_message.setText(self.message)
        self.setWindowTitle(self.window_title)

        if self.window_title in ["Error", "ERROR"]:
            icon = get_error_icon(QColor(255,0,0,200))
            self.setWindowIcon(icon)

        elif self.window_title in ["Warning", "WARNING"]:
            icon = get_warning_icon()
            self.setWindowIcon(icon)
        
        self.adjustSize()
        self.label_message.adjustSize()
        self.label_message.setAlignment(Qt.AlignCenter)

        if self.auto_close:
            self.timer.timeout.connect(self.message_close)
            self.timer.start(50) 

    def _adjust_size(self, kwargs: dict):

        height = kwargs.get("height", None)
        if isinstance(height, int):
            self.setFixedHeight(height)

        width = kwargs.get("width", None)
        if isinstance(width, int):
            self.setFixedWidth(width)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.message_close()
        elif event.key() == Qt.Key_Escape:
            self.close()