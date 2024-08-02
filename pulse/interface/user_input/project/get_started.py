from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QAbstractButton, QAction
from PyQt5.QtGui import QCloseEvent, QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

from pulse import app, UI_DIR
from pulse.interface.formatters import icons
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput

import os

class GetStartedInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = UI_DIR / "project/get_started_input.ui"
        uic.loadUi(ui_path, self)

        app().main_window.set_input_widget(self)
        self.main_window = app().main_window
        self.project = app().main_window.project
       
        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.initial_actions()
        self.exec()

    def _initialize(self):
        self.config = self.main_window.config
        self.input_ui = self.main_window.input_ui
        self.complete = False

    def _load_icons(self):
        widgets = self.findChildren((QAbstractButton, QAction))
        icons.change_icon_color_for_widgets(widgets, QColor("#1a73e8"))
        self.icon = icons.get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Get started")
        
    def _define_qt_variables(self):

        # QLabel
        self.recents_label : QLabel
        self.project1_path_label : QLabel
        self.project2_path_label : QLabel
        self.project3_path_label : QLabel
        self.project4_path_label : QLabel
        self.project5_path_label : QLabel

        # QPushButton
        self.create_button : QPushButton
        self.load_button : QPushButton
        self.about_button : QPushButton
        self.project1_button : QPushButton
        self.project2_button : QPushButton
        self.project3_button : QPushButton
        self.project4_button : QPushButton
        self.project5_button : QPushButton
        self.reset_list_projects_button : QPushButton

    def _create_connections(self):
        self.create_button.clicked.connect(self.new_project)
        self.load_button.clicked.connect(self.load_project)
        self.about_button.clicked.connect(self.about_project)
        self.reset_list_projects_button.clicked.connect(self.reset_list_projects)
        self.create_lists_of_buttons_and_labels()

    def create_lists_of_buttons_and_labels(self):

        self.project_buttons = list()
        self.project_buttons.append(self.project1_button)
        self.project_buttons.append(self.project2_button)
        self.project_buttons.append(self.project3_button)
        self.project_buttons.append(self.project4_button)
        self.project_buttons.append(self.project5_button)

        self.project_path_labels = list()
        self.project_path_labels.append(self.project1_path_label)
        self.project_path_labels.append(self.project2_path_label)
        self.project_path_labels.append(self.project3_path_label)
        self.project_path_labels.append(self.project4_path_label)
        self.project_path_labels.append(self.project5_path_label)

    def update_buttons_visibility(self):
        self.project_dir = list()
        for i in range(5):
            self.project_dir.append("")
            # self.project_buttons[i].setIcon()
            self.project_buttons[i].setVisible(False)
            self.project_path_labels[i].setVisible(False)

        self.recent_projectsList = list(self.config.recent_projects.items())[::-1]
        for i in range(5 if len(self.recent_projectsList) > 5 else len(self.recent_projectsList)):
            self.project_buttons[i].setVisible(True)
            self.project_path_labels[i].setVisible(True)
            self.project_dir[i] = self.recent_projectsList[i][1]
            self.project_path_labels[i].setText(str(self.recent_projectsList[i][1]))
            self.project_path_labels[i].adjustSize()
            self.project_path_labels[i].setWordWrap(True)
            self.project_path_labels[i].setScaledContents(True)

    def initial_actions(self):
        self.update_buttons_visibility()
        self.project_buttons[0].clicked.connect(lambda: self.load_recent_project(self.project_dir[0]))
        self.project_buttons[1].clicked.connect(lambda: self.load_recent_project(self.project_dir[1]))
        self.project_buttons[2].clicked.connect(lambda: self.load_recent_project(self.project_dir[2]))
        self.project_buttons[3].clicked.connect(lambda: self.load_recent_project(self.project_dir[3]))
        self.project_buttons[4].clicked.connect(lambda: self.load_recent_project(self.project_dir[4]))

    def continueButtonEvent(self):
        self.close()

    def new_project(self):
        self.close()
        if not self.input_ui.new_project():
            self.show()
        else:
            self.complete = True

    def load_project(self):
        self.close()
        if not self.input_ui.load_project():
            self.show()
        else:
            self.complete = True

    def about_project(self):
        self.input_ui.about_OpenPulse()

    def load_recent_project(self, dir):

        if os.path.exists(dir):
            if self.input_ui.load_project(path=dir):
                self.complete = True
                self.close()

        else:
            for key, value in self.config.recent_projects.items():
                if value == dir:
                    self.config.remove_path_from_config_file(key)
                    self.update_buttons_visibility()
                    break

            window_title = "Warning"
            title = "Project folder not found"
            message = "The following project folder path cannot be found, check if the project " 
            message += f"folder have not been deleted or moved to another directory. \n\n{dir}"
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
            self.config.resetRecentProjectList()
            self.initial_actions()