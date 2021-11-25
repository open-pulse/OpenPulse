from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QFrame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from threading import Thread

class PrintMessageInput(QDialog):
    def __init__(self, text_info, opv=None, fontsizes=[13,12], *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Messages/printMessages.ui', self)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.message_close)

        self.frame_message = self.findChild(QFrame, 'frame_message')

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        if opv is not None:
            opv.setInputObject(self)

        self.title_fontsize, self.message_fontsize = fontsizes

        self._label_title = self.findChild(QLabel, '_label_title')
        self._label_message = self.findChild(QLabel, '_label_message')
        
        self.pushButton_close.setVisible(True)
        self.create_font_title()
        self.create_font_message()
        self._label_title.setFont(self.font_title)
        self._label_message.setFont(self.font_message)
        self._label_message.setWordWrap(True)

        self.text_info = text_info
        message = self.preprocess_big_strings(self.text_info[1])

        if len(message) > 500:
            self.setMinimumWidth(600)
            self.setMinimumHeight(600)
            self.setMaximumWidth(600)
            self.setMaximumHeight(600)

            self.frame_message.setMinimumWidth(600)
            self.frame_message.setMinimumHeight(548)
            self.frame_message.setMaximumWidth(600)
            self.frame_message.setMaximumHeight(548)

            self._label_message.setMinimumWidth(580)
            self._label_message.setMinimumHeight(480)
            self._label_message.setMaximumWidth(580)
            self._label_message.setMaximumHeight(480)
            self.pushButton_close.move(250,502)    
        else:
            self.setMinimumWidth(600)
            self.setMinimumHeight(400)
            self.setMaximumWidth(600)
            self.setMaximumHeight(400)

            self.frame_message.setMinimumWidth(600)
            self.frame_message.setMinimumHeight(348)
            self.frame_message.setMaximumWidth(600)
            self.frame_message.setMaximumHeight(348)

            self._label_message.setMinimumWidth(580)
            self._label_message.setMinimumHeight(280)
            self._label_message.setMaximumWidth(580)
            self._label_message.setMaximumHeight(280)
            self.pushButton_close.move(250,302)

        self.frame_message.move(0,52)
        self._label_message.move(10,12)
        
        self._label_title.setText(text_info[0])
        self._label_message.setText(message)
        
        if len(text_info)>2:
            self.setWindowTitle(text_info[2])

        self.exec_()

    def message_close(self):
        self.close()

    def create_font_title(self):
        self.font_title = QFont()
        self.font_title.setFamily("Arial")
        self.font_title.setPointSize(self.title_fontsize)
        self.font_title.setBold(True)
        self.font_title.setItalic(False)
        self.font_title.setWeight(75) 

    def create_font_message(self):
        self.font_message = QFont()
        self.font_message.setFamily("Arial")
        self.font_message.setPointSize(self.message_fontsize)
        self.font_message.setBold(True)
        self.font_message.setItalic(False)
        self.font_message.setWeight(75) 

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        # font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self._label_message.setFont(font)
        self._label_message.setStyleSheet("color:blue")

    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self._label_title.setFont(font)
        self._label_title.setStyleSheet("color:black")
    
    def preprocess_big_strings(self, text):
        message = ""
        list_words = text.split(" ")
        for word in list_words: 
            if len(word) > 60:
                while len(word) > 60:
                    message += word[0:60] + " "
                    word = word[60:]
                message += word + " "
            else:
                message += word + " "
        return message
