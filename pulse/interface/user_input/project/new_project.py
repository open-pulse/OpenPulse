from PyQt5.QtWidgets import QComboBox, QDialog, QFrame, QFileDialog, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copyfile
from time import time

from pulse.libraries.default_libraries import default_material_library, default_fluid_library
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import get_new_path
from pulse import app, UI_DIR, __version__

window_title = "Error"

class NewProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/project/new_project_input.ui")
        uic.loadUi(ui_path, self)
        
        self.main_window = app().main_window
        self.opv = self.main_window.opv_widget
        self.opv.setInputObject(self)
        self.project = self.main_window.project
        self.file = self.project.file
        self.config = self.main_window.config

        self._initialize()
        self._config_window()
        self._define_qt_variables()
        self._create_qt_actions()
        self.update_project_directory()
        self.exec()

    def _initialize(self):

        self.stop = False
        self.complete = False

        self.project_directory = ""
        self.project_folder_path = ""
        self.project_file_path = ""
    
        user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

        self.project_file_name = self.file._project_base_name

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle(f"OpenPulse v{__version__}")

    def _define_qt_variables(self):
        # QComboBox
        self.comboBox_length_unit = self.findChild(QComboBox, 'comboBox_length_unit')
        self.comboBox_start_project = self.findChild(QComboBox, 'comboBox_start_project')
        # QFrame
        self.frame_geometry_file = self.findChild(QFrame, 'frame_geometry_file')
        self.frame_element_size = self.findChild(QFrame, 'frame_element_size')
        self.frame_geometry_tolerance = self.findChild(QFrame, 'frame_geometry_tolerance')
        # QLineEdit
        self.lineEdit_project_name = self.findChild(QLineEdit, 'lineEdit_project_name')
        self.lineEdit_project_folder = self.findChild(QLineEdit, 'lineEdit_project_folder')
        self.lineEdit_geometry_path = self.findChild(QLineEdit, 'lineEdit_geometry_path')
        self.lineEdit_element_size = self.findChild(QLineEdit, 'lineEdit_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_project_folder.setText(self.desktop_path)
        self.focus_lineEdit_project_name_if_blank()
        # QPushButton
        self.pushButton_import_geometry = self.findChild(QPushButton, 'pushButton_import_geometry')
        self.pushButton_search_project_folder = self.findChild(QPushButton, 'pushButton_search_project_folder')
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_start_project = self.findChild(QPushButton, 'pushButton_start_project')

    def _create_qt_actions(self):
        self.comboBox_start_project.currentIndexChanged.connect(self.update_available_inputs)
        self.pushButton_start_project.clicked.connect(self.start_project)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_import_geometry.clicked.connect(self.import_geometry)
        self.pushButton_search_project_folder.clicked.connect(self.search_project_folder)
        self.update_available_inputs()

    def create_project_folder(self):
        if self.lineEdit_project_name.text() == "":
            self.lineEdit_project_name.setFocus()
            title = 'Empty project name'
            message = "Please, inform a valid project name to continue."
            PrintMessageInput([window_title, title, message], auto_close=True)
            self.stop = True
            return
        
        if self.lineEdit_project_folder.text() == "":
            title = 'None project folder selected'
            message = "Please, select a folder where the project data are going to be stored."
            PrintMessageInput([window_title, title, message], auto_close=True)
            self.stop = True
            return

        if not os.path.exists(self.project_directory):
            os.mkdir(self.project_directory)

        self.stop = False

    def update_available_inputs(self):
        index = self.comboBox_start_project.currentIndex()
        if index == 0:
            self.pushButton_import_geometry.setDisabled(True)
        elif index == 1:
            self.pushButton_import_geometry.setDisabled(False)

    def focus_lineEdit_project_name_if_blank(self):
        if self.lineEdit_project_name.text() == "":
            self.lineEdit_project_name.setFocus()

    def update_project_directory(self):
        if self.project_directory != "":
            self.lineEdit_project_folder.setText(str(self.project_directory))
        else:
            self.project_directory = self.desktop_path        

    def search_project_folder(self):
        self.project_directory = QFileDialog.getExistingDirectory(None, 'Choose a folder to save the project files', self.desktop_path)
        self.update_project_directory()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.desktop_path, 'Files (*.iges *.igs *.step *.stp)')
        if self.path != "":
            self.lineEdit_geometry_path.setText(str(self.path))

    def check_project_inputs(self):
        if self.lineEdit_project_name.text() in os.listdir(self.project_directory):
            title = 'Error in project name'
            message = "This project name already exists, you should use a different project name to continue."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        
        if self.comboBox_start_project.currentIndex() == 1:
            if self.lineEdit_geometry_path.text() == "":
                title = 'Empty geometry at selection'
                message = "Please, select a valid *.iges or *.step format geometry to continue."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True
        
        if self.lineEdit_element_size.text() == "":
            title = 'Empty element size'
            message = "Please, inform a valid input to the element size."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        else:
            try:
                self.element_size = float(self.lineEdit_element_size.text())
            except Exception:
                title = 'Invalid element size'
                message = "Please, inform a valid input to the element size."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True

        if self.lineEdit_geometry_tolerance.text() == "":
            title = 'Empty geometry tolerance'
            message = "Please, inform a valid input to the geometry tolerance."
            PrintMessageInput([window_title, title, message], auto_close=True)
            return True
        else:
            try:
                self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
            except Exception:
                title = 'Invalid geometry tolerance'
                message = "Please, inform a valid input to the geometry tolerance."
                PrintMessageInput([window_title, title, message], auto_close=True)
                return True

    def start_project(self):
        t0 = time()

        self.create_project_folder()

        if self.check_project_inputs():
            return

        if self.stop:
            self.project.time_to_load_or_create_project = 0
            return
   
        if self.create_project():
            project_ini_file_path = get_new_path(self.project_folder_path, self.project_file_name)
            self.config.write_recent_project(project_ini_file_path)
            self.project.time_to_load_or_create_project = time() - t0
            self.complete = True
            self.close()

    def create_project(self):

        try:

            self.project_folder_path = get_new_path(self.project_directory, self.lineEdit_project_name.text())

            if not os.path.exists(self.project_folder_path):
                os.makedirs(self.project_folder_path)

            self.create_material_file()
            self.create_fluid_file()
            self.create_project_file()

            project_name = self.lineEdit_project_name.text()
            index = self.comboBox_start_project.currentIndex()
            
            if index == 0:

                self.project.new_empty_project( self.project_folder_path,
                                                project_name,
                                                self.length_unit,
                                                self.element_size,
                                                self.geometry_tolerance,
                                                self.import_type,
                                                self.material_list_path,
                                                self.fluid_list_path )
                return True

            elif index == 1:

                current_geometry_path = self.lineEdit_geometry_path.text()
                new_geometry_path = get_new_path(self.project_folder_path, self.geometry_filename)
                copyfile(current_geometry_path, new_geometry_path)

                self.project.new_project(   self.project_folder_path,
                                            project_name,
                                            self.length_unit,
                                            self.element_size,
                                            self.geometry_tolerance,
                                            self.import_type,
                                            self.material_list_path,
                                            self.fluid_list_path,
                                            geometry_path=new_geometry_path   )
                return True
            
            else:
                return False

        except Exception as error_log:
            
            window_title = "Error"
            title = "Error while creating new project"
            message = str(error_log)
            PrintMessageInput([window_title, title, message])
            
            return False

    def create_project_file(self):

        # self.project_name = get_new_path(self.project_folder_path, self.project_filename)
        self.project_filename = self.lineEdit_project_name.text()
        self.length_unit = self.comboBox_length_unit.currentText().replace(" ", "")
        index = self.comboBox_start_project.currentIndex()

        if index == 1:
            self.import_type = 0
            self.geometry_filename = os.path.basename(self.lineEdit_geometry_path.text())
        else:
            self.import_type = 1
            self.geometry_filename = ""
        
        project_setup = {   "project_folder_path" : self.project_folder_path,
                            "project_filename" : self.project_filename,
                            "length_unit" : self.length_unit,
                            "element_size" : self.element_size,
                            "geometry_tolerance" : self.geometry_tolerance,
                            "import_type" : self.import_type,
                            "geometry_filename" : self.geometry_filename   }

        self.file.create_project_file(**project_setup)

    def create_material_file(self):
        self.material_list_path = get_new_path(self.project_folder_path, self.file._material_file_name)
        default_material_library(self.material_list_path)

    def create_fluid_file(self):
        self.fluid_list_path = get_new_path(self.project_folder_path, self.file._fluid_file_name)
        default_fluid_library(self.fluid_list_path)