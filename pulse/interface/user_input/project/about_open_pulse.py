from PyQt5.QtWidgets import QDialog, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import uic

from pulse import app, UI_DIR, __version__, __release_date__
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class AboutOpenPulseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "project/about_open_pulse.ui", self)

        self.project = app().main_window.project
        self.opv = app().main_window.opv_widget
        self.opv.setInputObject(self)

        self._load_icons()
        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._create_connections()
        self.adjustSize()
        self.exec()

    def _load_icons(self):
        self.icon = get_openpulse_icon()
        self.load_icon = QIcon(get_icons_path('loadProject.png'))
        self.new_icon = QIcon(get_icons_path('add.png'))
        self.reset_icon = QIcon(get_icons_path('refresh.png'))
    
    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(self.icon)
        self.setWindowTitle("About")
        
    def _initialize(self):
        self.version_info = f"v{__version__} {__release_date__}"
        self.licensing_info = "Copyright (c) 2020 Project OpenPulse Contributors, MIT License."
        self.main_info = "OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. "
        self.main_info += "Openpulse allows the user to solve acoustic, structural, and coupled harmonic analyzes. The acoustic and structural modal analysis also can be "
        self.main_info += "solved in the current version. Further information is available in the OpenPulse repository at GitHub."

    def _define_qt_variables(self):
        # QLabel
        self.label_licensing_information : QLabel
        self.label_main_info : QLabel
        self.label_version_information : QLabel
        self.label_licensing_information.setText(self.licensing_info)
        self.label_main_info.setText(self.main_info)
        self.label_version_information.setText(self.version_info)
        # QPushButton
        self.pushButton_repository : QPushButton

    def _create_connections(self):
        self.pushButton_repository.clicked.connect(self.open_gitHub_repository)

    def open_gitHub_repository(self):
        title = "Error reached while trying to access the project repository"
        try:
            url = QUrl('https://github.com/open-pulse/OpenPulse')
            if not QDesktopServices.openUrl(url):
                message = "The OpenPulse repository at the GitHub's site cannot be accessed.\n"
                message += "We reccomend trying again later."
                PrintMessageInput([title, message, window_title_1])
        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def continueButtonEvent(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_gitHub_repository()
        elif event.key() == Qt.Key_Escape:
            self.close()