from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic

import os
from time import time
from pathlib import Path

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

class LoadProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.opv = self.main_window.opv_widget
        self.config = self.main_window.config
        self.path = kwargs.get("path", None)

        self._reset()
        self._get_project_path()
        self._load_project()

    def _reset(self):
        self.complete = False
        self.project_ini_file_path = ""        
        user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

    def _get_project_path(self):

        last_project_path = self.config.get_last_project_folder()
        if last_project_path is None:
            initial_project_folder_path = self.desktop_path
        else:
            initial_project_folder_path = last_project_path

        if self.path is None:
            self.project_ini_file_path, _ = QFileDialog.getOpenFileName( None, 
                                                                        'Open file', 
                                                                        initial_project_folder_path, 
                                                                        'OpenPulse Project (*.ini)' )
        else:
            self.project_ini_file_path = self.path

    def _load_project(self):
        try:
            if self.project_ini_file_path != "":
                t0 = time()
                self.project.load_project(self.project_ini_file_path)
                if self.project.preferences:
                    self.opv.set_user_interface_preferences(self.project.preferences)
                self.config.write_recent_project(self.project_ini_file_path)
                self.complete = True
                self.project.time_to_load_or_create_project = time() - t0
                self.close()
        except Exception as log_error:
            window_title = "Error"
            title = "Error while loading project"
            message = str(log_error)
            PrintMessageInput([window_title, title, message])