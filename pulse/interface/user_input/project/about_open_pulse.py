from PySide6.QtWidgets import QDialog, QLabel, QPushButton
from PySide6.QtGui import QCloseEvent, QDesktopServices
from PySide6.QtCore import Qt, QUrl

from pulse import app, UI_DIR, version, release_date

from pulse.interface.user_input.project.print_message import PrintMessageInput

from molde import load_ui

window_title_1 = "Error"
window_title_2 = "Warning"

class AboutOpenPulseInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/about_open_pulse.ui"
        load_ui(ui_path, self, UI_DIR)

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

        self.version_info = f"v{version()} {release_date()}"
        self.licensing_info = "Copyright (c) 2020 Project OpenPulse Contributors, GPL v3 License."
        self.main_info = "OpenPulse is a software written in Python for numerical modelling of low-frequency acoustically induced vibration in gas pipeline systems. "
        self.main_info += "Openpulse allows the user to solve acoustic, structural, and coupled harmonic analyzes. The acoustic and structural modal analysis also can be "
        self.main_info += "solved in the current version. Further information is available in the OpenPulse repository at GitHub."

    def _define_qt_variables(self):

        # QLabel
        self.label_licensing_information: QLabel
        self.label_main_info: QLabel
        self.label_version_information: QLabel
        self.logo_label: QLabel
        #
        self.label_licensing_information.setText(self.licensing_info)
        self.label_main_info.setText(self.main_info)
        self.label_version_information.setText(self.version_info)

        # QPushButton
        self.pushButton_repository: QPushButton

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
                PrintMessageInput([title, message, window_title_1])

        except Exception as log_error:
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])

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