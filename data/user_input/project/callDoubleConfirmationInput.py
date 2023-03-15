from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont 
from PyQt5.QtCore import Qt, QRect
from PyQt5 import uic
from pulse import __version__, __release_date__
# import os
# import configparser
# from shutil import copyfile
# import numpy as np

class CallDoubleConfirmationInput(QDialog):
    def __init__(self, title, message, leftButton_label="Return", rightButton_label="Remove", rightButton_size=160, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/callDoubleConfirmationInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.window_title = kwargs.get('window_title', f'OpenPulse v{__version__} ({__release_date__})')

        # self.rightButton_size = kwargs.get('rightButton_size', 160)
        # self.leftButton_label = kwargs.get('leftButton_label', 'Return')
        # self.rightButton_label = kwargs.get('rightButton_label', 'Remove')

        self.leftButton_label = leftButton_label
        self.rightButton_label = rightButton_label
        self.right_button_size = rightButton_size

        self.define_qt_variables()
        self.create_actions()
        self.configure_labels(title, message)
        self.configure_buttons()
        self.setWindowTitle(self.window_title)

        self._continue = False
        self._doNotRun = True
        self._stop = True
        self.exec_()

    def define_qt_variables(self):
        self.QLabel_message = self.findChild(QLabel, 'QLabel_message')
        self.QLabel_title = self.findChild(QLabel, 'QLabel_title')
        self.pushButton_rightButton = self.findChild(QPushButton, 'pushButton_rightButton')
        self.pushButton_leftButton = self.findChild(QPushButton, 'pushButton_leftButton')
    
    def create_actions(self):
        self.pushButton_rightButton.clicked.connect(self.confirm_action)
        self.pushButton_leftButton.clicked.connect(self.force_to_close)

    def configure_buttons(self):
        self.pushButton_leftButton.setText(self.leftButton_label)
        self.pushButton_rightButton.setText(self.rightButton_label)
        self.pushButton_rightButton.setMinimumWidth(self.right_button_size)
        self.pushButton_rightButton.setMaximumWidth(self.right_button_size)
        
        x = self.pushButton_rightButton.x()
        y = self.pushButton_rightButton.y()
        height = self.pushButton_rightButton.height()
        width = self.pushButton_rightButton.width()
        
        if self.right_button_size>160:
            dx = self.right_button_size-160   
            self.pushButton_rightButton.setGeometry(QRect(int(x-dx), y, width, height))    

    def configure_labels(self, title, message):
        self.QLabel_title.setText(title)
        self.QLabel_message.setText(message)
        self.QLabel_message.setWordWrap(True)
        self.create_font_title()
        self.create_font_message()
        self.QLabel_title.setFont(self.font_title)
        self.QLabel_message.setFont(self.font_message)

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

