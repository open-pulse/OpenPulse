from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse import app, UI_DIR

import os
from time import time
from pathlib import Path
from shutil import copy

class LoadProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.main_window = app().main_window
        self.project = app().main_window.project
        self.config = app().main_window.config

        self.project_path = kwargs.get("path", None)

        self.reset()
        self.get_project_path()

    def reset(self):
        self.complete = False       

    def get_project_path(self):

        if os.path.exists(self.project_path):
            self.load_project()

        if self.project_path is None:
            suggested_path = self.config.get_last_folder_for("project folder")
            if suggested_path is None:
                suggested_path = str(Path().home())

            self.project_path, check = QFileDialog.getOpenFileName( 
                                                                    None, 
                                                                    'Open project', 
                                                                    suggested_path, 
                                                                    'OpenPulse Project (*.pulse)' 
                                                                   )

            if check:
                self.load_project()            

    def load_project(self):
        try:

            t0 = time()
            self.project.load_project()
            app().config.add_recent_file(self.project_path)
            app().config.write_last_folder_path_in_file("project folder", self.project_path)
            copy(self.project_path, app().main_window.temp_project_file_path)
            app().main_window.update_window_title(self.project_path)

            # if self.project.preferences:
            #     self.opv.set_user_interface_preferences(self.project.preferences)

            # self.config.write_recent_project(self.project_path)

            self.complete = True
            self.project.time_to_load_or_create_project = time() - t0
            self.close()

        except Exception as log_error:
            window_title = "Error"
            title = "Error while loading project"
            message = str(log_error)
            PrintMessageInput([window_title, title, message])