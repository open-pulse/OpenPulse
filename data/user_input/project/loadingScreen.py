from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie, QFont, QIcon
from pathlib import Path

from data.user_input.project.printMessageInput import PrintMessageInput
from pulse import __version__, __release_date__


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
                print(log_error)
                title = "An error has been reached in LoadingScreen"
                PrintMessageInput([title, str(log_error), "ERROR"])
                
        self.finished.emit()
        self.thread().quit()

class LoadingScreen(QDialog):
    def __init__(self, title='', text='', target=None, project=None, args=None, kwargs=None):
        super().__init__()

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.project = project

        self.layout = QVBoxLayout()
        self.label_title = QLabel(self)
        self.label_message = QLabel(self)
        self.label_animation = QLabel(self)
                
        self.movie = QMovie('data/icons/loading0.gif')

        self.label_title.setText(title)
        self.label_message.setText(text)
        self.label_message.setWordWrap(True)
        # self.label_message.setAlignment(Qt.AlignHCenter)
        self.label_animation.setMovie(self.movie)
        
        self.layout.addWidget(self.label_title)
        self.layout.addWidget(self.label_message)
        self.layout.addWidget(self.label_animation)
        
        if project:
            self.pushButton_stop_process = QPushButton("Stop process", self)
            self.pushButton_stop_process.clicked.connect(self.pushButton_pressed)
            self.layout.addWidget(self.pushButton_stop_process)
            self.config_pushButton()

        self.setLayout(self.layout)
        self.configAppearance()        

        self.threadWorker = QThread()
        self.worker = QWorker(target)
        self.worker.moveToThread(self.threadWorker)
        self.threadWorker.started.connect(self.worker.run)
        self.threadWorker.finished.connect(self.close)
        self.threadWorker.start()
        self.movie.start()

        self.exec()
        self.movie.stop()

    def configWindow(self):
        self.setWindowTitle(f"OpenPulse v{__version__} ({__release_date__})")
        self.setMinimumSize(QSize(400, 250))
        self.setMaximumSize(QSize(400, 250))
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowMinimizeButtonHint)
        self.setGeometry(QRect(400, 120, 400, 250))
    
    def configAppearance(self):
        self.label_title.setAlignment(Qt.AlignTop)
        # self.label_title.setAlignment(Qt.AlignHCenter)
        self.label_animation.setAlignment(Qt.AlignCenter)
        self.movie.setScaledSize(QSize(150, 150))
        
        self.config_title()
        self.config_message()

    def config_title(self):
        font = QFont()
        font.setBold(True)
        font.setPointSize(12)
        self.label_title.setFont(font)
    
    def config_pushButton(self):
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setPointSize(12)
        self.pushButton_stop_process.setFont(font)
        self.pushButton_stop_process.setStyleSheet("color:blue")
        # self.pushButton_stop_process.setText("Stop process")
        self.pushButton_stop_process.setGeometry(QRect(175, 300, 150, 36))
        self.pushButton_stop_process.setMinimumSize(QSize(150, 36))
        self.pushButton_stop_process.setMaximumSize(QSize(150, 36))
        self.pushButton_stop_process.move(QPoint(175, 300))

    def config_message(self):
        font = QFont()
        font.setBold(False)
        font.setPointSize(12)
        self.label_message.setFont(font)
        self.label_message.setWordWrap(True)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.pushButton_pressed()
    
    def pushButton_pressed(self):
        if self.project:
            self.project.preprocessor.stop_processing = True