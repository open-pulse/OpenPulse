from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path

import os

from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput
from pulse import __version__, __release_date__

def get_icons_path(filename):
    path = f"data/icons/{filename}"
    if os.path.exists(path):
        return str(Path(path))

class AboutOpenPulseInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        uic.loadUi(Path('data/user_input/ui/Project/aboutOpenPulseInput.ui'), self)

        self.icon = QIcon(get_icons_path('pulse.png'))
        self.load_icon = QIcon(get_icons_path('loadProject.png'))
        self.new_icon = QIcon(get_icons_path('add.png'))
        self.reset_icon = QIcon(get_icons_path('refresh.png'))
        self.setWindowIcon(self.icon)

        self.project = project

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.opv = opv
        self.opv.setInputObject(self)

        version_info = f"v{__version__} {__release_date__}"
        licensing_info = "Copyright (c) 2020 Project OpenPulse Contributors, MIT License."
        main_info = "OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. "
        main_info += "Openpulse allows the user to solve acoustic, structural, and coupled harmonic analyzes. The acoustic and structural modal analysis also can be "
        main_info += "solved in the current version. Further information is available in the OpenPulse repository at GitHub."

        self.label_version_information = self.findChild(QLabel, 'label_version_information')
        self.label_version_information.setText(version_info)
        
        self.label_licensing_information = self.findChild(QLabel, 'label_licensing_information')
        self.label_licensing_information.setText(licensing_info)

        self.label_main_info = self.findChild(QLabel, 'label_main_info')
        self.label_main_info.setText(main_info)
        
        self.toolButton_repository = self.findChild(QToolButton, 'toolButton_repository')
        self.toolButton_repository.clicked.connect(self.open_gitHub_repository)

        self.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_gitHub_repository()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def open_gitHub_repository(self):
        title = "Error reached while trying to access the project repository"
        try:
            url = QUrl('https://github.com/open-pulse/OpenPulse')
            if not QDesktopServices.openUrl(url):
                message = "The OpenPulse repository at the GitHub's site cannot be accessed.\n"
                message += "We reccomend trying again later."
                PrintMessageInput([title, message, "ERROR"])
        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([title, message, "OpenPulse"])

    def continueButtonEvent(self):
        self.close()