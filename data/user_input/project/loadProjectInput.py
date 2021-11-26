from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QProgressBar, QLabel, QListWidget
from data.user_input.project.printMessageInput import PrintMessageInput
from pulse.project import Project
from PyQt5.QtGui import QIcon
from os.path import basename, expanduser, exists
from PyQt5 import uic
import os
import configparser
from shutil import ExecError, copyfile
import numpy as np
from time import time

from PyQt5 import uic

class LoadProjectInput(QDialog):
    def __init__(self, project, opv, config, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.opv = opv
        self.config = config
        self.path = path
        self.userPath = expanduser('~')
        self.complete_project_path = ""
        self.complete = False

        if self.path is None:
            self.complete_project_path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'OpenPulse Project (*.ini)')
        else:
            self.complete_project_path = self.path
        
        try:
            if self.complete_project_path != "":
                t0 = time()
                self.project.load_project(self.complete_project_path)
                if self.project.preferences:
                    self.opv.setUserInterfacePreferences(self.project.preferences)
                self.config.writeRecentProject(self.project.get_project_name(), self.complete_project_path)
                self.complete = True
                self.project.time_to_load_or_create_project = time() - t0
                self.close()
        except Exception as log_error:
            title = "Error while loading project"
            message = str(log_error)
            window_title = "ERROR"
            print(message)
            PrintMessageInput([title, message, window_title])