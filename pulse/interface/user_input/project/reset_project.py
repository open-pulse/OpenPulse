from PyQt5.QtWidgets import QPushButton, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copyfile
import numpy as np

from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

window_title = "WARNING"
title = "Project resetting complete"
message = "The current project setup and project data\n"
message += "has been reset to default values."

class ResetProjectInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('pulse/interface/ui_files/project/reset_project.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.project = project
        self.opv = opv

        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_reset)
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_cancel.clicked.connect(self.force_to_close)

        self.exec()
    
    def confirm_reset(self):
        self.project.reset_project()
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntities()
        PrintMessageInput([title, message, window_title])
        self.close()

    def force_to_close(self):
        self.close()