from PyQt5.QtWidgets import QPushButton, QDialog
from pulse.project import Project
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from os.path import basename, expanduser, exists
from PyQt5 import uic
import os
import configparser
from shutil import copyfile
import numpy as np

from data.user_input.project.printMessageInput import PrintMessageInput

window_title = "WARNING MESSAGE"
title = "Project data reseted"
message = "All project data has been reseted to default values."

class ResetProjectInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/resetProjectInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.opv = opv

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_reset)
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_cancel.clicked.connect(self.force_to_close)

        self.exec_()
    
    def confirm_reset(self):
        self.project.reset_project()
        self.opv.changePlotToEntities()
        PrintMessageInput([title, message, window_title])
        self.close()

    def force_to_close(self):
        self.close()