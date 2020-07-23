from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QProgressBar, QLabel
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
    def __init__(self, project, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/loadProjectInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.userPath = expanduser('~')
        self.complete_project_path = ""
        self.project_file_path = ""
        self.complete = False

        self.line_import_project = self.findChild(QLineEdit, 'line_import_project')

        self.text_label = self.findChild(QLabel, 'text_label')
        self.progressBar = self.findChild(QProgressBar, 'progressBar')

        self.toolButton_import_project = self.findChild(QToolButton, 'toolButton_import_project')
        self.toolButton_import_project.clicked.connect(self.import_project)
        self.progressBar.setVisible(False)
        self.text_label.setText("")
        self.text_label.setVisible(False)
        self.exec_()

    def import_project(self):

        self.complete_project_path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'OpenPulse Project (*.ini)')
        
        if self.complete_project_path != "":
            self.project_file_path = os.path.dirname(self.complete_project_path)
            self.progressBar.setVisible(True)
            self.text_label.setVisible(True)
            self.line_import_project.setText(str(self.complete_project_path))
            self.project.load_project_progress_bar(self.complete_project_path, self.progressBar, self.text_label)
            self.complete = True
            self.close()