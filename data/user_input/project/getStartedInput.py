import os
from os.path import basename
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox, QTreeWidget, QLabel
from pulse.utils import remove_bc_from_file
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic

from data.user_input.project.printMessageInput import PrintMessageInput

class GetStartedInput(QDialog):
    def __init__(self, project, config, inputUi, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/getStarted.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.load_icon = QIcon(icons_path + 'loadProject.png')
        self.new_icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.config = config
        self.inputUi = inputUi

        self.draw = False

        self.recents_label = self.findChild(QLabel, 'recents_label')
        
        self.create_button = self.findChild(QPushButton, 'create_button')
        self.load_button = self.findChild(QPushButton, 'load_button')
        self.about_button = self.findChild(QPushButton, 'about_button')
        self.continue_button = self.findChild(QPushButton, 'continue_button')

        self.project_button = []
        self.project_dir = []
        self.project_button.append(self.findChild(QPushButton, 'project1_button'))
        self.project_button.append(self.findChild(QPushButton, 'project2_button'))
        self.project_button.append(self.findChild(QPushButton, 'project3_button'))
        self.project_button.append(self.findChild(QPushButton, 'project4_button'))

        self.create_button.setIcon(self.new_icon)
        self.load_button.setIcon(self.load_icon)
        self.about_button.setIcon(self.icon)

        for i in range(4):
            self.project_dir.append("")
            self.project_button[i].setIcon(self.load_icon)
            self.project_button[i].setVisible(False)

        self.create_button.clicked.connect(self.newProject)
        self.load_button.clicked.connect(self.loadProject)
        self.about_button.clicked.connect(self.aboutProject)
        self.continue_button.clicked.connect(self.continueButtonEvent)

        self.recentProjectsList = list(self.config.recentProjects.items())[::-1]
        for i in range(4 if len(self.recentProjectsList) > 4 else len(self.recentProjectsList)):
            self.project_button[i].setVisible(True)
            self.project_dir[i] = self.recentProjectsList[i][1]
            text = str(self.recentProjectsList[i][0]) + "\n" + str(self.recentProjectsList[i][1])
            self.project_button[i].setText(text)

        self.project_button[0].clicked.connect(lambda: self.loadRecentProject(self.project_dir[0]))
        self.project_button[1].clicked.connect(lambda: self.loadRecentProject(self.project_dir[1]))
        self.project_button[2].clicked.connect(lambda: self.loadRecentProject(self.project_dir[2]))
        self.project_button[3].clicked.connect(lambda: self.loadRecentProject(self.project_dir[3]))

        self.exec_()

    def continueButtonEvent(self):
        self.close()

    def newProject(self):
        if self.inputUi.new_project(self.config):
            self.draw = True
            self.close()

    def loadProject(self):
        if self.inputUi.loadProject(self.config):
            self.draw = True
            self.close()

    def aboutProject(self):
        window_title = "OpenPulse" 
        message_title = "Version information"
        message = "OpenPulse Beta Version (August, 2021)"
        PrintMessageInput([message_title, message, window_title])

    def loadRecentProject(self, dir):
        if self.inputUi.loadProject(self.config, path=dir):
            self.draw = True
            self.close()