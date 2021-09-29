from threading import Thread
from time import sleep

from PyQt5.QtCore import Qt, QSize, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QMovie, QFont, QIcon


class QWorker(QObject):
    finished = pyqtSignal()
    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        if self.target is not None:
            self.target()
        self.finished.emit()

class LoadingScreen(QDialog):
    def __init__(self, title='', text='', target=None, args=None, kwargs=None):
        super().__init__()
        self.icon = QIcon('data\\icons\\pulse.png')
        self.setWindowIcon(self.icon)

        self.layout = QVBoxLayout()
        self.label_title = QLabel(self)
        self.label_message = QLabel(self)
        self.label_animation = QLabel(self)
        self.movie = QMovie('data/icons/loading0.gif')

        self.label_title.setText(title)
        self.label_message.setText(text)
        self.label_animation.setMovie(self.movie)

        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.label_message)
        self.layout.addWidget(self.label_animation)

        self.setLayout(self.layout)
        self.configAppearance()

        self.thread = QThread()
        self.worker = QWorker(target)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.close)
        self.thread.start()

        self.movie.start()
        self.exec()

    def configAppearance(self):
        self.movie.setScaledSize(QSize(150, 150))
        self.setMinimumSize(QSize(400, 200))
        self.setMaximumSize(QSize(400, 800))
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.label_title.setAlignment(Qt.AlignTop)
        self.label_animation.setAlignment(Qt.AlignCenter)

        self.config_title()
        self.config_message()

    def config_title(self):
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.label_title.setFont(font)
    
    def config_message(self):
        font = QFont()
        font.setBold(False)
        font.setPointSize(12)
        self.label_message.setFont(font)
        self.label_message.setWordWrap(True)