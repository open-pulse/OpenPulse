from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic
from pathlib import Path

from pulse import UI_DIR
from threading import Thread

class PrintMessageInput(QDialog):
    def __init__(self, text_info, opv=None, fontsizes=[13,12], alignment=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "/messages/printMessages.ui", self)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.message_close)

        self.frame_message = self.findChild(QFrame, 'frame_message')

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        if opv is not None:
            opv.setInputObject(self)

        self.title_fontsize, self.message_fontsize = fontsizes

        self.alignment = alignment

        self._label_title = self.findChild(QLabel, '_label_title')
        self._label_message = self.findChild(QLabel, '_label_message')
        
        self.pushButton_close.setVisible(True)
        self.create_font_title()
        self.create_font_message()
        self._label_title.setFont(self.font_title)
        self._label_message.setFont(self.font_message)
        self._label_message.setWordWrap(True)
        self._label_message.setMargin(20)

        try:
            if alignment is None:
                self._label_message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            else:
                self._label_message.setAlignment(alignment | Qt.AlignVCenter)
        except:
            self._label_message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        self.text_info = text_info
        message = self.preprocess_big_strings(self.text_info[1])

        if 0 < len(message) < 200:
            height = 300
            width = 600
        elif 200 <= len(message) < 400:
            height = 400
            width = 600
        elif 400 <= len(message) < 1000:
            height = 600
            width = 600
        elif len(message) >= 1000:
            height = 800
            width = 600

        self.setMinimumWidth(width)
        self.setMinimumHeight(height)
        self.setMaximumWidth(width)
        self.setMaximumHeight(height)

        self.frame_message.setMinimumWidth(width)
        self.frame_message.setMinimumHeight(height-52)
        self.frame_message.setMaximumWidth(width)
        self.frame_message.setMaximumHeight(height-52)

        self._label_message.setMinimumWidth(width-20)
        self._label_message.setMinimumHeight(height-120)
        self._label_message.setMaximumWidth(width-20)
        self._label_message.setMaximumHeight(height-120)

        self.pushButton_close.move(250,height-98)   

        self.frame_message.move(0,52)
        self._label_message.move(10,12)
        
        self._label_title.setText(text_info[0])
        self._label_message.setText(message)
        
        if len(text_info)>2:
            self.setWindowTitle(text_info[2])

        self.exec()

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
