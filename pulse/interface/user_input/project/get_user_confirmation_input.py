from PySide6.QtWidgets import QDialog, QLabel, QPushButton
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

from pulse import app, UI_DIR, version

from molde import load_ui


class GetUserConfirmationInput(QDialog):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args)

        ui_path = UI_DIR / "messages/get_user_confirmation.ui"
        load_ui(ui_path, self, UI_DIR)

        self.title = title
        self.message = message
        self.buttons_config = kwargs.get("buttons_config", dict())
        self.window_title = kwargs.get('window_title', f'OpenPulse v{version()}')

        app().main_window.set_input_widget(self)

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
        self.close()

    def left_callback(self):
        self.close()
    
    def closeEvent(self, a0):
        return super().closeEvent(a0)