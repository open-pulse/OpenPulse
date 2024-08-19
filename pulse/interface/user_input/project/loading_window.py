import logging
import re
from time import sleep

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QProgressBar, QWidget

from pulse import UI_DIR, app

# Catches every message that contains something like [n/N]
PROGRESS_MESSAGE_REGEX = re.compile(r"\[\d+/\d+\]")


class LoadingWindow(QWidget):
    """
    This function is intended to be called for functions that take
    a long time to run and should run together with a progress bar.

    The indended use is explained in the following example:
    ```
    def long_function(param_a, param_b=0):
        ...
        return value_c
    ```

    To run this function with a progress bar you just need to write
    ```
    value_c = LoadingWindow(long_function, param_a, param_b=1234)
    ```

    Disclaimers:
    This is a monstruosity, but it works.
    I hope no one ever needs to modify it.
    I am trying my best to explain every part of this code.

    An easier way to do it would be using a QWorker and a QThread,
    but it does not work for our Application.
    Qt manages the windows in the main thread, therefore the function
    to be loaded would need to run in a secondary thread.
    The problem is GMSH (wow, what a surprise).

    GMSH, for some reason, refuses to run in secondary thread.
    And GMSH is an important part of our software, that of course
    need a progress bar when it is running.
    So this is an attempt to run everything (both GMSH and QT) in the
    main thread without conflicts.

    I also don't want to mix the interface code with the engine code
    because it can easily became a mess and make the creation of
    automated tests really hard.
    """

    def __init__(self, _function):
        super().__init__()

        ui_path = UI_DIR / "messages/new_loading_window.ui"
        uic.loadUi(ui_path, self)

        self._function = _function
        self._config_window()

    def _config_window(self):
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
        )
        self.setWindowModality(Qt.ApplicationModal)
        self.update_position()
        self.progress_bar.setValue(0)

    def _define_qt_variables(self):
        self.progress_bar: QProgressBar
        self.progress_label: QLabel

    def update_position(self):
        '''
        Place the window on the center of the screen.
        '''
        desktop_geometry = app().desktop().screenGeometry()
        pos_x = int((desktop_geometry.width() - self.width())/2)
        pos_y = int((desktop_geometry.height() - self.height())/2)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())

    def run(self, *args, **kwargs):
        self.show()

        # Changes the cursor to wait
        QApplication.setOverrideCursor(Qt.WaitCursor)

        # Creates a handler to update progress_bar and progress_label
        # every time a logging containing [n/N] appears
        progress_handler = ProgressBarLogUpdater(logging.DEBUG, loading_window=self)
        logging.getLogger().addHandler(progress_handler)

        # Waits the loading bar to appear and uptates pyqt
        sleep(0.1)
        QApplication.processEvents()

        try:
            # Calls the actual function
            return_value = self._function(*args, **kwargs)

        finally:
            """
            This piece of code will run even if the function have errors.
            Because the error is not handled here it will propagate to the
            function that called it.
            The error should be threated there, here we are just mitigating
            things related to the loading window.
            """

            # Restores the previous cursor
            QApplication.restoreOverrideCursor()

            # Removes the ProgressBarLogUpdater
            logging.getLogger().removeHandler(progress_handler)

            self.hide()

        return return_value

    def __call__(self, *args, **kwargs):
        return self.run(self._function, *args, **kwargs)


class ProgressBarLogUpdater(logging.Handler):
    """
    This class is an log observer. It is meant to watch logs
    and use it to update an instance of the loading window.
    """

    def __init__(self, level=0, *, loading_window: LoadingWindow) -> None:
        super().__init__(level)
        self.loading_window = loading_window

    def emit(self, record):
        """
        This function is fired when something is logged.
        If the log have a marker like [n/N] in its message it
        will update the LoadingWindow associated with this class.
        """

        # Updates QT to prevent freezing
        QApplication.processEvents()

        percent = self.get_percentage(record.msg)
        if percent is None:
            return

        self.loading_window.progress_label.setText(record.msg)
        self.loading_window.progress_bar.setValue(percent)

        # Updates QT to show the window modifications
        QApplication.processEvents()

    def get_percentage(self, message: str):
        """
        Uses regex to check if the message have a marker like [2/10]
        If it does, it extracts the step (2) and the max_step (10) and
        calculates the percentage (20%).
        Otherwise it just returns None.
        """

        if not isinstance(message, str):
            return

        matches = PROGRESS_MESSAGE_REGEX.findall(message)
        if not matches:
            return

        first_match: str = matches[0]
        step, max_step = first_match.strip("[]").split("/")
        percentage = 100 * int(step) // int(max_step)
        return percentage
