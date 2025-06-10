from PySide6.QtWidgets import QDialog, QLabel, QPushButton
from PySide6.QtCore import Qt

from pulse import app, UI_DIR
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from molde import load_ui


class PsdOrDamperDeletionErrorWindow(GetUserConfirmationInput):
    def __init__(self, selected_device_type, selected_device_name, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/psd_or_damper_deletion_error_window.ui"
        load_ui(ui_path, self)
        self.selected_device_type = selected_device_type
        self.selected_device_name = selected_device_name

        self.auto_close = kwargs.get("auto_close", False)
        app().main_window.set_input_widget(self)

        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._adjust_size(kwargs)
        self._set_texts()
        self.exec()

    def _define_qt_variables(self):
        # QPushButton
        self.pushButton_cancel: QPushButton
        self.pushButton_open_editor: QPushButton

        # QLabel
        self.label_message: QLabel

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")

    def _set_texts(self):
        if self.selected_device_type == "psd":
            message = "To delete a PSD or its parts, please use the dedicated editor."

        elif self.selected_device_type == "damper":
            message = "To delete a pulsation damper or its parts, please use the dedicated editor."

        self.label_message.setText(message)
        self.label_message.setAlignment(Qt.AlignCenter)

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
        if self.selected_device_type == "psd":
            app().main_window.input_ui.pulsation_suppression_device_editor(
                device_to_delete=self.selected_device_name
            )

        elif self.selected_device_type == "damper":
            app().main_window.input_ui.pulsation_damper_editor(
                device_to_delete=self.selected_device_name
            )
