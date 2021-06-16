from distutils.log import error
from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QRadioButton, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5 import uic
# import os
# import configparser
# from shutil import copyfile
# import numpy as np

class CallDoubleConfirmationInput(QDialog):
    def __init__(self, title, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/callDoubleConfirmationInput.ui', self)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        # self.QDialog = self#.findChild(QDialog, "Dialog")
        # print(self.QDialog)
        # print(self.x(),self.y())
        # self.QDialog.setGeometry(100,100,1000,800)
        # self.getPx
        # self.resize(1000,600)

        self.QLabel_message = self.findChild(QLabel, 'QLabel_message')
        self.QLabel_title = self.findChild(QLabel, 'QLabel_title')

        self.QLabel_title.setText(title)
        self.QLabel_message.setText(message)
        self.QLabel_message.setWordWrap(True)
        self.create_font_title()
        self.create_font_message()
        self.QLabel_title.setFont(self.font_title)
        self.QLabel_message.setFont(self.font_message)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_action)
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_cancel.clicked.connect(self.force_to_close)
        self._doNotRun = True
        self.exec_()

    def confirm_action(self):
        self._stop = False
        self._continue = True
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

