from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QCloseEvent, QDesktopServices

from pulse import app, RELEASE_DATE, VERSION
from pulse.interface import error_title
from pulse.interface.ui_generated.project.about_open_pulse_ui import AboutOpenPulse_UI
from pulse.interface.user_input.project.print_message import PrintMessageInput


class AboutOpenPulseInput(AboutOpenPulse_UI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        app().main_window.set_input_widget(self)
        self.project = app().main_window.project

        self._config_window()
        self._initialize()
        self._define_qt_variables()
        self._define_logo_variables()
        self.update_logo_text()
        self._create_connections()
        self.adjustSize()

        while self.keep_window_open:
            self.exec()

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("OpenPulse")
    

    def _initialize(self):

        self.keep_window_open = True

        self.version_info = f"v{VERSION} {RELEASE_DATE}"
        self.licensing_info = "Copyright (c) 2020 Project OpenPulse Contributors, GPL v3 License."
        self.main_info = "OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. "
        self.main_info += "Openpulse allows the user to solve acoustic, structural, and coupled harmonic analyzes. The acoustic and structural modal analysis also can be "
        self.main_info += "solved in the current version. Further information is available in the OpenPulse repository at GitHub."

    def _define_qt_variables(self):
        self.label_licensing_information.setText(self.licensing_info)
        self.label_main_info.setText(self.main_info)
        self.label_version_information.setText(self.version_info)

    def _create_connections(self):
        self.pushButton_repository.clicked.connect(self.open_gitHub_repository)
        app().main_window.theme_changed.connect(self.update_logo_text)
    
    def _define_logo_variables(self):
        self.light_logo_text = """<html><head/><body style=\"font-size: 35pt; font-family: 'Bauhaus 93';
                                \"><p><span style=\" color:#0055ff;\">O</span><span style=\" color:#4F4F4F;\">pen</span><span style=\"
                                 color:#0055ff;\">P</span><span style=\" color:#4F4F4F;\">ulse</span></p></body></html>"""
    
        self.dark_logo_text = """<html><head/><body style=\"font-size: 35pt; font-family: 'Bauhaus 93';
                                \"><p><span style=\" color:#0055ff;\">O</span><span style=\" color:#c8c8c8;\">pen</span><span style=\"
                                 color:#0055ff;\">P</span><span style=\" color:#c8c8c8;\">ulse</span></p></body></html>"""

    def update_logo_text(self):
        if app().config.user_preferences.interface_theme == "dark":
            self.logo_label.setText(self.dark_logo_text)
        else:
            self.logo_label.setText(self.light_logo_text)

    def open_gitHub_repository(self):

        title = "Error reached while trying to access the project repository"

        try:

            self.hide()
            url = QUrl('https://github.com/open-pulse/OpenPulse')
            if not QDesktopServices.openUrl(url):
                message = "The OpenPulse repository at the GitHub's site cannot be accessed.\n"
                message += "We reccomend trying again later."
                PrintMessageInput([error_title, title, message])

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([error_title, title, message])

        self.close()

    def continueButtonEvent(self):
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.open_gitHub_repository()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)