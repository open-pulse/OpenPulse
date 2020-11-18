from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QProgressBar, QLabel, QListWidget
from pulse.project import Project
from PyQt5.QtGui import QIcon
from os.path import basename, expanduser, exists
from PyQt5 import uic
import os
import configparser
from shutil import copyfile
import numpy as np

from PyQt5 import uic

class LoadProjectInput(QDialog):
    def __init__(self, project, config, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project
        self.config = config
        self.path = path
        self.userPath = expanduser('~')
        self.complete_project_path = ""
        self.complete = False

        if self.path is None:
            self.complete_project_path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'OpenPulse Project (*.ini)')
        else:
            self.complete_project_path = self.path
        
        if self.complete_project_path != "":
            self.project.load_project(self.complete_project_path)
            self.config.writeRecentProject(self.project.get_project_name(), self.complete_project_path)
            self.complete = True
            self.close()