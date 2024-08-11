from PyQt5.QtWidgets import QDialog, QFrame, QComboBox, QFileDialog, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QEvent, QObject, pyqtSignal
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.handler.geometry_handler import GeometryHandler
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.project.get_user_confirmation_input import GetUserConfirmationInput
from pulse.tools.utils import get_new_path

import os
from pathlib import Path
from shutil import copyfile


class ImportGeometry(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        app().main_window.set_input_widget(self)

        self.main_window = app().main_window
        self.project = app().project
        self.config = app().config

        self.preprocessor = self.project.preprocessor

        self._initialize()
        self._config_window()
        self.import_geometry()

    def _initialize(self):

        self.complete = False
        self.folder_path = ""
        user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

        self.file = self.project.file

    def _config_window(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowIcon(app().main_window.pulse_icon)
        self.setWindowTitle("Import geometry")

    def import_geometry(self):

        self.geometry_path, _ = QFileDialog.getOpenFileName(None, 
                                                            'Open file', 
                                                            self.desktop_path, 
                                                            'Files (*.iges *.igs *.step *.stp)')

        if self.geometry_path != "":
            if os.path.exists(self.geometry_path):
  
                import_type = 0
                self.geometry_filename = os.path.basename(self.geometry_path)
                app().pulse_file.modify_project_attributes(
                                                                        import_type = import_type,
                                                                        geometry_filename = self.geometry_filename
                                                                       )

                self.process_initial_actions()

    def process_initial_actions(self):
        #
        # new_geometry_path = get_new_path(self.file._project_path, self.geometry_filename)
        # copyfile(self.geometry_path, new_geometry_path)
        # self.file.create_backup_geometry_folder()
        #
        self.project.reset(reset_all=True)
        self.file.load(self.file.project_ini_file_path)
        self.project.process_geometry_and_mesh()
        self.project.load_project_files()
        self.project.preprocessor.check_disconnected_lines()
        #
        app().main_window.update_plots()
        self.complete = True

    def print_user_message(self):
        window_title = "OpenPulse"
        title = "Geometry exported"
        message = "The geometry file has been exported."
        PrintMessageInput([window_title, title, message], auto_close=True)