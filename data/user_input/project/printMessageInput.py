from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic

class PrintMessageInput(QDialog):
    def __init__(self, text_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Messages/printMessages.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.Label_title = self.findChild(QLabel, 'Label_title')
        self.Label_message = self.findChild(QLabel, 'Label_message')
       
        self.create_font_title()
        self.create_font_message()
        self.Label_title.setFont(self.font_title)
        self.Label_message.setFont(self.font_message)
        self.Label_message.setWordWrap(True)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.message_close)

        self.text_info = text_info
        self.Label_title.setText(text_info[0])
        self.Label_message.setText(text_info[1])
        
        if len(text_info)>2:
            self.setWindowTitle(text_info[2])

        self.exec_()

    def message_close(self):
        self.close()

    def create_font_title(self):
        self.font_title = QFont()
        self.font_title.setFamily("Arial")
        self.font_title.setPointSize(14)
        self.font_title.setBold(True)
        self.font_title.setItalic(False)
        self.font_title.setWeight(75) 

    def create_font_message(self):
        self.font_message = QFont()
        self.font_message.setFamily("Arial")
        self.font_message.setPointSize(12)
        self.font_message.setBold(True)
        self.font_message.setItalic(False)
        self.font_message.setWeight(75) 