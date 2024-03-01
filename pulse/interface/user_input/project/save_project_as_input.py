from PyQt5.QtWidgets import QCheckBox, QDialog, QFileDialog, QLineEdit, QPushButton, QRadioButton, QToolButton
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5 import uic

from pulse import app, UI_DIR
from pulse.interface.formatters.icons import *
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import get_new_path

import os
from pathlib import Path
from shutil import copytree, rmtree

window_title_1 = "Error"
window_title_2 = "Warning"

class SaveProjectAsInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "project/save_project_as.ui", self)

        self.main_window = app().main_window
        self.project = self.main_window.project
        self.file = self.project.file
        self.opv = self.main_window.opv_widget

        self.opv.setInputObject(self)

        self._initialize()
        self._load_icons()
        self._config_window()
        self._define_qt_variables()
        self._create_connections()
        self.exec()

    def _initialize(self):

        self.stop = False

        self.user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(self.user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

        self.current_project_path = self.file.project_path
        self.project_directory = os.path.dirname(self.current_project_path)
        self.project_name = self.file.project_name

        self.project_ini = self.file.project_ini_name
        self.current_geometry_path = self.file.geometry_path
        self.current_material_list_path = self.file._material_list_path
        self.current_fluid_list_path = self.file._fluid_list_path

    def _load_icons(self):
        self.icon = get_openpulse_icon()

    def _config_window(self):
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse")

    def _define_qt_variables(self):

        # QCheckBox
        self.remove_current_project_files : QCheckBox

        # QLineEdit
        self.current_project_name : QLineEdit
        self.new_project_name : QLineEdit
        self.current_project_directory : QLineEdit
        self.new_project_directory : QLineEdit
        #
        self.current_project_name.setText(self.project_name)
        self.current_project_directory.setText(self.project_directory)
        self.new_project_directory.setText(self.project_directory)

        # QPushButton
        self.search_project_folder_button : QPushButton
        self.cancel_button : QPushButton
        self.save_project_button : QPushButton
        # self.save_project_button.setDisabled(True)

    def _create_connections(self):
        self.save_project_button.clicked.connect(self.save_project_button_pressed)
        self.cancel_button.clicked.connect(self.cancel_and_close)
        self.search_project_folder_button.clicked.connect(self.search_project_folder)

    def search_project_folder(self):
        self.new_project_directory = QFileDialog.getExistingDirectory(None, 'Choose a folder to save the project files', self.desktop_path)
        if os.path.exists(self.new_project_directory):
            self.new_project_directory.setText(str(self.new_project_directory))
 
    def clean_project_name(self):
        self.new_project_name.setText("")

    def are_modifications_allowable(self):
        
        if self.new_project_name.text() == "":
            self.title = "Empty project name"
            self.message = "Please, inform a valid project name at 'New project name' input field to continue."
            self.new_project_name.setFocus()
            return True
        
        if self.new_project_name.text() == self.current_project_name.text():
            if self.new_project_directory.text() == self.current_project_directory.text():
                self.title = "Same project name and directory detected"
                self.message = "Please, inform a diferent project name and/or directory to continue."
                return True

    def copy_project_files(self):  
        self.new_project_path = get_new_path(self.new_project_directory.text(),
                                                  self.new_project_name.text())
        copytree(self.current_project_path, 
                 self.new_project_path)

    def update_all_file_paths(self):

        if os.path.exists(self.current_geometry_path):
            new_geometry_path = get_new_path(self.new_project_directory.text(), 
                                             os.path.basename(self.current_geometry_path))
        else:
            new_geometry_path = ""

        # new_material_list_path = get_new_path(self.new_project_directory.text(), 
        #                                       os.path.basename(self.current_material_list_path))

        # new_fluid_list_path = get_new_path(self.new_project_directory.text(), 
        #                                    os.path.basename(self.current_fluid_list_path))

        self.project.copy_project(  self.new_project_path,
                                    self.new_project_name.text(),
                                    geometry_path = new_geometry_path  )

    def save_project_button_pressed(self):

        if self.are_modifications_allowable():
            PrintMessageInput([window_title_2, self.title, self.message])  
            return
        
        project_name = self.new_project_name.text()
        if project_name == "":
            self.search_project_folder()
            return self.save_project_button_pressed()
        else:
            self.copy_project_files()
            self.update_all_file_paths()
            self.file.modify_project_attributes(project_name = project_name)
            if self.remove_current_project_files.isChecked():
                rmtree(self.current_project_path)
            self.main_window.change_window_title(self.file.project_name)
            self.close()

    def cancel_and_close(self):
        self.close()

    def keyPressEvent(self, event: QKeyEvent | None) -> None:

        if event.key() == Qt.Key_Escape:
            self.close()
        if event.key() == Qt.Key_Enter:
            self.save_project_button_pressed()

        return super().keyPressEvent(event)