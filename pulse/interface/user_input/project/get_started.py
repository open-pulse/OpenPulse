from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QAbstractButton
from PySide6.QtGui import QCloseEvent, QColor, QAction
from PySide6.QtCore import Qt
from pathlib import Path

from pulse import app, UI_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

from molde import load_ui

import os

class GetStartedInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/get_started_input.ui"
        load_ui(ui_path, self)

        # app().main_window.set_input_widget(self)
        self.project = app().main_window.project

        self.config = app().main_window.config
        
        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.initial_actions()

        while self.keep_window_open:
            app().main_window.set_input_widget(self)
            self.exec()

    def _initialize(self):
        self.complete = False
        self.keep_window_open = True

    def _load_icons(self):
        widgets = list()
        for widget in [QAbstractButton, QAction]:
            widgets += self.findChildren(widget)
        icons.change_icon_color_for_widgets(widgets, QColor("#1a73e8"))

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Get started")
        
    def _define_qt_variables(self):

        # QLabel
        self.recents_label : QLabel
        self.project_path_label_1 : QLabel
        self.project_path_label_2 : QLabel
        self.project_path_label_3 : QLabel
        self.project_path_label_4 : QLabel
        self.project_path_label_5 : QLabel

        # QPushButton
        self.create_button : QPushButton
        self.load_button : QPushButton
        self.about_button : QPushButton
        self.project_button_1 : QPushButton
        self.project_button_2 : QPushButton
        self.project_button_3 : QPushButton
        self.project_button_4 : QPushButton
        self.project_button_5 : QPushButton
        self.reset_list_projects_button : QPushButton

    def _create_connections(self):
        self.create_button.clicked.connect(self.new_project)
        self.load_button.clicked.connect(self.open_project)
        self.about_button.clicked.connect(self.about_project)
        self.reset_list_projects_button.clicked.connect(self.reset_list_projects)
        self.create_lists_of_buttons_and_labels()

    def create_lists_of_buttons_and_labels(self):

        self.project_buttons = list()
        self.project_buttons.append(self.project_button_1)
        self.project_buttons.append(self.project_button_2)
        self.project_buttons.append(self.project_button_3)
        self.project_buttons.append(self.project_button_4)
        self.project_buttons.append(self.project_button_5)

        self.project_path_labels = list()
        self.project_path_labels.append(self.project_path_label_1)
        self.project_path_labels.append(self.project_path_label_2)
        self.project_path_labels.append(self.project_path_label_3)
        self.project_path_labels.append(self.project_path_label_4)
        self.project_path_labels.append(self.project_path_label_5)

    def update_buttons_visibility(self):
        self.project_path = list()
        for i in range(5):
            self.project_path.append("")
            # self.project_buttons[i].setIcon()
            self.project_buttons[i].setVisible(False)
            self.project_path_labels[i].setVisible(False)

        recents = app().config.get_recent_files()

        for i, project_path in enumerate(recents):
            if i <= 4:
                self.project_buttons[i].setVisible(True)
                self.project_path_labels[i].setVisible(True)
                self.project_path[i] = project_path
                self.project_path_labels[i].setText(str(project_path))
                self.project_path_labels[i].adjustSize()
                self.project_path_labels[i].setWordWrap(True)
                self.project_path_labels[i].setScaledContents(True)

    def initial_actions(self):
        self.update_buttons_visibility()
        self.project_buttons[0].clicked.connect(lambda: self.open_recent_project(self.project_path[0]))
        self.project_buttons[1].clicked.connect(lambda: self.open_recent_project(self.project_path[1]))
        self.project_buttons[2].clicked.connect(lambda: self.open_recent_project(self.project_path[2]))
        self.project_buttons[3].clicked.connect(lambda: self.open_recent_project(self.project_path[3]))
        self.project_buttons[4].clicked.connect(lambda: self.open_recent_project(self.project_path[4]))

    def continueButtonEvent(self):
        self.close()

    def new_project(self):
        self.hide()
        if app().main_window.new_project():
            self.complete = True
            self.close()

    def open_project(self):
        self.hide()
        if app().main_window.open_project_dialog():
            return       
        self.complete = True
        self.close()

    def about_project(self):
        app().main_window.action_about_openpulse_callback()

    def open_recent_project(self, project_path: str | Path):
        if os.path.exists(project_path):
            self.hide()
            app().main_window.open_project(project_path)
            self.complete = True
            self.close()

        else:
            for path in self.config.get_recent_files():
                if str(path) == str(project_path):
                    self.config.remove_path_from_config_file(path)
                    self.update_buttons_visibility()
                    break

            window_title = "Warning"
            title = "Project folder not found"
            message = "The following project folder path cannot be found, check if the project " 
            message += f"folder have not been deleted or moved to another directory. \n\n{project_path}"
            PrintMessageInput([window_title, title, message])

    def reset_list_projects(self):

        self.hide()

        title = "Resetting of the recent projects list"
        message = "Dear user, do you want to proceed with the 'Recent Projects' list clean-up and resetting?"

        buttons_config = {"left_button_label" : "No", "right_button_label" : "Yes"}
        read = GetUserConfirmationInput(title, message, buttons_config=buttons_config)

        if read._cancel:
            return

        if read._continue:
            self.config.reset_recent_projects()
            self.initial_actions()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.keep_window_open = False
        return super().closeEvent(a0)