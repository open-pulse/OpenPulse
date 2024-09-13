from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic

from pulse import app, UI_DIR, version


class GetUserConfirmationInput(QDialog):
    def __init__(self, title, message, buttons_config={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "messages/get_user_confirmation.ui"
        uic.loadUi(ui_path, self)

        self.title = title
        self.message = message
        self.buttons_config = buttons_config
        self.window_title = kwargs.get('window_title', f'OpenPulse v{version()}')

        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        self._create_connections()

        self._configure_labels()
        self._configure_buttons()
        self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle(self.window_title)

    def _reset_variables(self):
        self._stop = True
        self._continue = False
        self._cancel = True

    def _define_qt_variables(self):

        # QLabel
        self.label_message : QLabel
        self.label_title : QLabel

        # QPushButton
        self.pushButton_rightButton : QPushButton
        self.pushButton_leftButton : QPushButton

    def _create_connections(self):
        self.pushButton_rightButton.clicked.connect(self.right_callback)
        self.pushButton_leftButton.clicked.connect(self.left_callback)

    def _configure_buttons(self):
        if self.buttons_config:
            if "left_button_label" in self.buttons_config.keys():
                self.pushButton_leftButton.setText(self.buttons_config["left_button_label"])
            if "right_button_label" in self.buttons_config.keys():
                self.pushButton_rightButton.setText(self.buttons_config["right_button_label"])
            if "left_toolTip" in self.buttons_config.keys():
                self.pushButton_leftButton.setToolTip(self.buttons_config["left_toolTip"])
            if "right_toolTip" in self.buttons_config.keys():
                self.pushButton_rightButton.setToolTip(self.buttons_config["right_toolTip"])
            if "left_button_size" in self.buttons_config.keys():
                self.pushButton_leftButton.setFixedWidth(self.buttons_config["left_button_size"])
            if "right_button_size" in self.buttons_config.keys():
                self.pushButton_rightButton.setFixedWidth(self.buttons_config["right_button_size"])

    def _configure_labels(self):
        self.label_title.setText(self.title)
        self.label_message.setText(self.message)
        self.label_message.setWordWrap(True)
        self.label_message.setAlignment(Qt.AlignJustify)
        self.label_message.setAlignment(Qt.AlignCenter)
        self.label_message.setMargin(12)
        self.label_message.adjustSize()
        self.adjustSize()

    def right_callback(self):
        self._cancel = False
        self._continue = True
        # self._stop = False
        self.close()

    def left_callback(self):
        self._cancel = True
        self._continue = False
        # self._stop = True
        self.close()