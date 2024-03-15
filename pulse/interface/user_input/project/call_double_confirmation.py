from PyQt5.QtWidgets import QDialog, QCheckBox, QComboBox, QFileDialog, QLabel, QLineEdit, QPushButton, QSpinBox, QTabWidget, QWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic

from pulse import UI_DIR, __version__
from pulse.interface.formatters.icons import * 


class CallDoubleConfirmationInput(QDialog):
    def __init__(self, title, message, buttons_config={}, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "messages/call_double_confirmation.ui", self)

        self.title = title
        self.message = message
        self.buttons_config = buttons_config
        self.window_title = kwargs.get('window_title', f'OpenPulse v{__version__}')

        self._load_icons()
        self._config_window()
        self._reset_variables()
        self._define_qt_variables()
        self._create_actions()
        self._configure_labels()
        self._configure_buttons()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle(self.window_title)

    def _reset_variables(self):
        self._stop = True
        self._continue = False
        self._doNotRun = True

    def _define_qt_variables(self):
        self.label_message = self.findChild(QLabel, 'label_message')
        self.label_title = self.findChild(QLabel, 'label_title')
        self.pushButton_rightButton = self.findChild(QPushButton, 'pushButton_rightButton')
        self.pushButton_leftButton = self.findChild(QPushButton, 'pushButton_leftButton')
    
    def _create_actions(self):
        self.pushButton_rightButton.clicked.connect(self.confirm_action)
        self.pushButton_leftButton.clicked.connect(self.force_to_close)

    def _configure_buttons(self):

        if self.buttons_config != {}:
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

    def confirm_action(self):
        self._continue = True
        self._stop = False
        self._doNotRun = False
        self.close()

    def force_to_close(self):
        self._continue = False
        self._stop = True
        self._doNotRun = False
        self.close()