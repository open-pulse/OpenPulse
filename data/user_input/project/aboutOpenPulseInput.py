import os
from os.path import basename
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox, QTreeWidget, QLabel
from pulse.utils import remove_bc_from_file
from PyQt5.QtGui import QColor, QBrush, QFont, QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

class AboutOpenPulseInput(QDialog):
    def __init__(self, project,*args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/aboutOpenPulseInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.load_icon = QIcon(icons_path + 'loadProject.png')
        self.new_icon = QIcon(icons_path + 'add.png')
        self.reset_icon = QIcon(icons_path + 'refresh.png')
        self.setWindowIcon(self.icon)

        self.project = project

        self.toolButton_repository = self.findChild(QToolButton, 'toolButton_repository')
        self.toolButton_repository.clicked.connect(self.open_gitHub_repository)

        self.label_version_information = self.findChild(QLabel, 'label_version_information')
        self.label_version_information.setText("Gamma Version (v0.1.0 October 15th 2021)")
        
        main_info = "OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. "
        main_info += "Openpulse allows the user to solve acoustic, structural, and coupled harmonic analyzes. The acoustic and structural modal analysis also can be "
        main_info += "solved in the current version. Further information is available in the OpenPulse repository at GitHub."
        self.label_main_info = self.findChild(QLabel, 'label_main_info')
        self.label_main_info.setText(main_info)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_gitHub_repository()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def open_gitHub_repository(self):
        url = QUrl('https://github.com/open-pulse/OpenPulse')
        if not QDesktopServices.openUrl(url):
            title = "Error reached while trying to access the project repository"
            message = "The OpenPulse repository at the GitHub's site cannot be accessed.\n"
            message += "We reccomend trying again later."
            PrintMessageInput([title, message, "ERROR"])
        
    def createFont(self):
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(9)
        self.font.setWeight(75)
        self.font.setBold(False)
        self.font.setItalic(False)

    def continueButtonEvent(self):
        self.close()