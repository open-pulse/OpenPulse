from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QThread
from PyQt5 import uic
from pathlib import Path

from pulse import UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import __version__, __release_date__

window_title_1 = "Error"
window_title_2 = "Warning"

class QWorker(QObject):
    finished = pyqtSignal()
    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        if self.target is not None:
            try:
                self.target()
            except Exception as log_error:
                title = "An error has been reached in LoadingScreen"
                message = str(log_error)
                PrintMessageInput([window_title_1, title, message])
                
        self.finished.emit()
        self.thread().quit()

class LoadingScreen(QDialog):
    def __init__(self, target=None, *args, **kwargs):
        super().__init__()

        ui_path = UI_DIR / "messages/loading_window.ui"
        uic.loadUi(ui_path, self)
        
        self.target = target
        self.title = kwargs.get("title", "")
        self.message = kwargs.get("message", "")
        self.project = kwargs.get("project", None)

        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self._config_widgets()
        self._set_texts_and_animation()
        self._start_threading()
        self.exec()
        self.movie.stop()

    def _load_icons(self):
        self.icon = get_openpulse_icon()
        self.gif_path = str(Path('data/icons/gifs/loading_blue.gif'))

    def _config_window(self):
        self.setWindowTitle(f"OpenPulse v{__version__}")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(self.icon)

    def _define_qt_variables(self):
        self.label_animation : QLabel
        self.label_message : QLabel
        self.label_title : QLabel
        self.pushButton_stop_processing : QPushButton
        
    def _create_connections(self):
        self.pushButton_stop_processing.clicked.connect(self.pushButton_pressed)

    def _config_widgets(self):
        self.movie = QMovie(self.gif_path)
        self.movie.setScaledSize(QSize(100,100))
        if self.project is None:
            self.pushButton_stop_processing.setDisabled(True)

    def _set_texts_and_animation(self):
        self.label_title.setText(self.title)
        self.label_message.setText(self.message)
        self.label_animation.setMovie(self.movie)
        self.label_animation.setScaledContents(True)
        self.label_animation.adjustSize()
        self.adjustSize()

    def _start_threading(self):
        self.threadWorker = QThread()
        self.worker = QWorker(self.target)
        self.worker.moveToThread(self.threadWorker)
        self.threadWorker.started.connect(self.worker.run)
        self.threadWorker.finished.connect(self.close)
        self.threadWorker.start()
        self.movie.start()

    def pushButton_pressed(self):
        if self.project is not None:
            self.project.preprocessor.stop_processing = True

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.pushButton_pressed()