from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QProgressBar, QPushButton
from PyQt5 import uic
from pulse import app, UI_DIR
from PyQt5.QtCore import Qt, QTimer
from pulse import app






class PsdOrDamperDeletionErrorWindow(QDialog):
    def __init__(self, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/psd_or_damper_deletion_error_window.ui"
        uic.loadUi(ui_path, self)

        self.auto_close = kwargs.get("auto_close", False)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        # self._config_widgets()
        self._adjust_size(kwargs)
        self.exec()

    def _define_qt_variables(self):
        # QFrame
        self.frame_button : QFrame
        self.frame_message : QFrame
        self.frame_title : QFrame

        # QPushButton
        self.pushButton_cancel : QPushButton

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)

    def _adjust_size(self, kwargs: dict):

        height = kwargs.get("height", None)
        if isinstance(height, int):
            self.setFixedHeight(height)

        width = kwargs.get("width", None)
        if isinstance(width, int):
            self.setFixedWidth(width)

    def _create_connections(self):
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_open_editor.clicked.connect(self.open_editor_callback)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.close()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def open_editor_callback(self):
        psd_editor = app().main_window.input_ui.pulsation_suppression_device_editor()
