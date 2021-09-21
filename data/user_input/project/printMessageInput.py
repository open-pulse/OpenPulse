from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
from threading import Thread

class PrintMessageInput(QDialog):
    def __init__(self, text_info, opv=None, opvAnalysisRenderer=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Plots/Messages/printMessages.ui', self)

        self.pushButton_close = self.findChild(QPushButton, 'pushButton_close')
        self.pushButton_close.clicked.connect(self.message_close)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        if opv is not None:
            opv.setInputObject(self)

        self.Label_title = self.findChild(QLabel, '_label_title')
        self.Label_message = self.findChild(QLabel, '_label_message')
        
        if opvAnalysisRenderer is None:
            self.pushButton_close.setVisible(True)
            self.create_font_title()
            self.create_font_message()
            self.Label_title.setFont(self.font_title)
            self.Label_message.setFont(self.font_message)
            self.Label_message.setWordWrap(True)
        else:
            self.close()
            self.pushButton_close.setVisible(False)
            self.config_title_font()
            self.config_message_font()

        self.text_info = text_info
        message = self.preprocess_big_strings(self.text_info[1])
        self.Label_title.setText(text_info[0])
        self.Label_message.setText(message)
        
        if len(text_info)>2:
            self.setWindowTitle(text_info[2])
        
        if opvAnalysisRenderer is None:
            self.exec_()
        else:
            # Thread(target=self.exec_).start()
            Thread(target=opvAnalysisRenderer._cacheFrames).start()
            self.exec_()

    def message_close(self):
        self.close()

    def create_font_title(self):
        self.font_title = QFont()
        self.font_title.setFamily("Arial")
        self.font_title.setPointSize(13)
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

    def config_message_font(self):
        font = QFont()
        font.setPointSize(17)
        font.setBold(True)
        # font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_message.setFont(font)
        self.label_message.setStyleSheet("color:blue")

    def config_title_font(self):
        font = QFont()
        font.setPointSize(19)
        font.setBold(True)
        font.setItalic(True)
        font.setFamily("Arial")
        # font.setWeight(60)
        self.label_title.setFont(font)
        self.label_title.setStyleSheet("color:black")
    
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
