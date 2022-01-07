from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
# import os
# import configparser
# from shutil import copyfile
# import numpy as np

class CallDoubleConfirmationInput(QDialog):
    def __init__(self, title, message, leftButton_label='Return', rightButton_label='Remove', *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/callDoubleConfirmationInput.ui', self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.window_title = kwargs.get('window_title', 'OpenPulse Beta Version (August, 2021)')

        # self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        # self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        # self.setWindowFlag(Qt.WindowMinMaxButtonsHint, False)
        # self.setWindowFlag(Qt.FramelessWindowHint, False)

        # self.QDialog = self#.findChild(QDialog, "Dialog")
        # self.QDialog.setGeometry(100,100,1000,800)
        # self.getPx
        # self.resize(1000,600)

        self.rightButton_label = rightButton_label
        self.leftButton_label = leftButton_label

        self.QLabel_message = self.findChild(QLabel, 'QLabel_message')
        self.QLabel_title = self.findChild(QLabel, 'QLabel_title')
        self.setWindowTitle(self.window_title)

        self.QLabel_title.setText(title)
        self.QLabel_message.setText(message)
        self.QLabel_message.setWordWrap(True)
        self.create_font_title()
        self.create_font_message()
        self.QLabel_title.setFont(self.font_title)
        self.QLabel_message.setFont(self.font_message)

        self.pushButton_rightButton = self.findChild(QPushButton, 'pushButton_rightButton')
        self.pushButton_rightButton.setText(self.rightButton_label)
        self.pushButton_rightButton.clicked.connect(self.confirm_action)
        self.pushButton_leftButton = self.findChild(QPushButton, 'pushButton_leftButton')
        self.pushButton_leftButton.setText(self.leftButton_label)
        self.pushButton_leftButton.clicked.connect(self.force_to_close)
        self._continue = False
        self._doNotRun = True
        self._stop = True
        self.exec_()

    def confirm_action(self):
        self._continue = True
        self._stop = False
        self._doNotRun = False
        self.close()

    def force_to_close(self):
        self._continue = False
        self._stop = True
        self._doNotRun = False
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

