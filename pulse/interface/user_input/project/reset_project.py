from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

import os
import configparser
import numpy as np
from shutil import copyfile
from pathlib import Path

class ResetProjectInput(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.project = app().main_window.project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_windows()
        self.get_user_confirmation()

    def _load_icons(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)

    def _config_windows(self):    
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

    def confirm_reset(self):
        self.project.reset_project()
        self.opv.opvRenderer.plot()
        self.opv.changePlotToEntities()
        self.print_final_message()
        self.close()    
    
    def print_final_message(self):
        window_title = "Warning"
        title = "Project resetting complete"
        message = "The current project setup and project data "
        message += "has been reset to default values."
        PrintMessageInput([window_title, title, message], auto_close=True)

    def get_user_confirmation(self):
        title = "Project reset"
        message = "Would you like to reset the project data to its initial state?"
        close = QMessageBox.question(self, title, message, QMessageBox.No | QMessageBox.Yes)
        if close == QMessageBox.Yes:
            self.confirm_reset()
        else:
            self.close()