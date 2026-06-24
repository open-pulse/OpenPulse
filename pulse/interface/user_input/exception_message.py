from PySide6.QtGui import QColor, QShowEvent
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pulse import USER_PATH
from pulse.interface.formatters.icons import get_error_icon, get_warning_icon
from pulse.interface.ui_generated.messages.exception_message_ui import (
    ExceptionMessage_UI,
)
from pulse.utils.text_utils import pascal_to_spaced_case
from traceback import format_tb


class ExceptionMessage(ExceptionMessage_UI):
    def __init__(self, exception: Exception, stack_trace = None):
        super().__init__()

        self._config_window()
        self._create_connections()

        if isinstance(exception, Warning):
            self.setWindowIcon(get_warning_icon())
            self.setWindowTitle("Warning")
        else:
            self.setWindowIcon(get_error_icon(QColor(255, 0, 0, 200)))
            self.setWindowTitle("Error")

        if stack_trace is None:
            self.stack_trace_text_browser.hide()
            self.copy_log_button.hide()
            self.copy_stacktrace_button.hide()
        else:
            self.traceback = "\n".join(format_tb(stack_trace))

            limited_traceback = "\n".join(format_tb(stack_trace, limit=-5))
            if stderr := getattr(exception, "stderr", ""):
                self.traceback = (
                    f"{self.traceback}\n"
                    f"{stderr}"
                )
                limited_traceback = (
                    f"{limited_traceback}\n"
                    f"{stderr}"
                )

            self.stack_trace_text_browser.setText(
                "<pre>"
                + "Traceback (most recent call last):\n"
                + limited_traceback
                + "</pre>"
            )

        title = pascal_to_spaced_case(exception.__class__.__name__)
        self.title_label.setText(title)

        message = " ".join(str(i) for i in exception.args)
        self.error_message.setText(message)

        self.adjustSize()

    def _config_window(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def _create_connections(self):
        self.ok_button.clicked.connect(self.close)
        self.copy_log_button.clicked.connect(self.copy_log)
        self.copy_stacktrace_button.clicked.connect(self.copy_stacktrace)

    def copy_log(self):
        log_path = USER_PATH / ".pulse.log"

        if log_path.exists():
            log_text = log_path.read_text(encoding="utf-8", errors="replace")
            QApplication.clipboard().setText(log_text)
        else:
            QApplication.clipboard().setText("Log file not found")

    def copy_stacktrace(self):
        QApplication.clipboard().setText(self.traceback)

    def move_stacktrace_to_bottom(self):
        v_scrollbar = self.stack_trace_text_browser.verticalScrollBar()
        v_scrollbar.setValue(v_scrollbar.maximum())

    def showEvent(self, arg__1: QShowEvent, /):
        super().showEvent(arg__1)
        self.raise_()
        self.activateWindow()
