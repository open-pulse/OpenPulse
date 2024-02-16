from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import uic
from pathlib import Path

from pulse import app

class PrintMessageInput(QDialog):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__()

        main_window = app().main_window

        ui_path = Path(f"{main_window.ui_dir}/messages/print_message.ui")
        uic.loadUi(ui_path, self)

        self.auto_close = kwargs.get("auto_close", False)
        self.window_title, self.title, self.message = text_info

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._set_texts()
        self.exec()

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def _define_qt_variables(self):
        self.frame_message = self.findChild(QFrame, 'frame_message')
        self.frame_title = self.findChild(QFrame, 'frame_title')
        self.label_title = self.findChild(QLabel, 'label_title')
        self.label_message = self.findChild(QLabel, 'label_message')
        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.timer = QTimer()
        self.pushButton_close.clicked.connect(self.message_close)
        self.pushButton_close.setVisible(True)

    def _set_texts(self):
        self.title2 = f"   {self.title}   "
        self.label_message.setMargin(12)
        self.label_title.setText(self.title2)
        self.label_message.setText(self.message)
        self.setWindowTitle(self.window_title)
        self.adjustSize()
        self.label_message.setAlignment(Qt.AlignJustify)
        if self.auto_close:
            self.timer.timeout.connect(self.message_close)
            self.timer.start(2000) 

    def message_close(self):
        self.timer.stop()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.message_close()
        elif event.key() == Qt.Key_Escape:
            self.close()