from PyQt5.QtWidgets import QComboBox, QDialog, QFrame, QFileDialog, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copyfile
from time import time

from pulse.lib.default_libraries import default_material_library, default_fluid_library
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.utils import get_new_path
from pulse import app, UI_DIR

window_title = "Error"

class NewProjectInput(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ui_path = Path(f"{UI_DIR}/project/new_project_input.ui")
        uic.loadUi(ui_path, self)
        
        self.main_window = app().main_window
        self.opv = self.main_window.getOPVWidget()
        self.opv.setInputObject(self)
        self.project = self.main_window.getProject()
        self.config = self.main_window.config

        self._reset()
        self._config_window()
        self._define_qt_variables()
        self._create_qt_actions()
        self.exec()

    def _reset(self):

        self.stop = False
        self.complete = False

        self.project_directory = ""
        self.project_folder_path = ""
        self.project_file_path = ""
    
        user_path = os.path.expanduser('~')
        desktop_path = Path(os.path.join(os.path.join(user_path, 'Desktop')))
        self.desktop_path = str(desktop_path)

        self.material_list_name = self.project.file._material_file_name
        self.fluid_list_name = self.project.file._fluid_file_name
        self.project_file_name = self.project.file._project_base_name

    def _config_window(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("OpenPulse - New project")

    def _define_qt_variables(self):
        # QComboBox
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
            # self.lineEdit_element_size.setDisabled(True)
            # self.lineEdit_geometry_tolerance.setDisabled(True)
        elif index == 1:
            self.pushButton_import_geometry.setDisabled(False)
            # self.lineEdit_element_size.setDisabled(False)
            # self.lineEdit_geometry_tolerance.setDisabled(False)

    def focus_lineEdit_project_name_if_blank(self):
        if self.lineEdit_project_name.text() == "":
            self.lineEdit_project_name.setFocus()

    def search_project_folder(self):
        self.project_directory = QFileDialog.getExistingDirectory(None, 'Choose a folder to save the project files', self.desktop_path)
        if self.project_directory != "":
            self.lineEdit_project_folder.setText(str(self.project_directory))
        else:
            self.project_directory = self.desktop_path        

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
            self.config.write_recent_project(self.project_file_path)
            self.complete = True
            self.project.time_to_load_or_create_project = time() - t0
            self.close()

    def create_project(self):

        self.project_folder_path = get_new_path(self.project_directory, self.lineEdit_project_name.text())

        if not os.path.exists(self.project_folder_path):
            os.makedirs(self.project_folder_path)

        self.create_material_file()
        self.create_fluid_file()
        self.create_project_file()

        project_name = self.lineEdit_project_name.text()
        index = self.comboBox_start_project.currentIndex()
        
        if index == 0:
            import_type = 1
            self.project.new_empty_project( self.project_folder_path, 
                                            project_name,
                                            self.element_size,
                                            self.geometry_tolerance, 
                                            import_type,
                                            self.material_list_path, 
                                            self.fluid_list_path )
            return True

        elif index == 1:
            geometry_filename = os.path.basename(self.lineEdit_geometry_path.text())
            new_geometry_path = get_new_path(self.project_folder_path, geometry_filename)
            copyfile(self.lineEdit_geometry_path.text(), new_geometry_path)
            import_type = 0
            self.project.new_project(   self.project_folder_path, 
                                        project_name, 
                                        self.element_size,
                                        self.geometry_tolerance, 
                                        import_type, 
                                        self.material_list_path, 
                                        self.fluid_list_path, 
                                        geometry_path=new_geometry_path   )
        
        return True

    def create_project_file(self):

        self.project_file_path = get_new_path(self.project_folder_path, self.project_file_name)

        config = configparser.ConfigParser()
        config['PROJECT'] = {}
        config['PROJECT']['Name'] = self.lineEdit_project_name.text()

        index = self.comboBox_start_project.currentIndex()

        if index == 0:
            config['PROJECT']['Import type'] = str(1)
            # config['PROJECT']['Geometry file'] = ""

        elif index == 1:
            geometry_file_name = os.path.basename(self.lineEdit_geometry_path.text())
            element_size = self.lineEdit_element_size.text()
            geometry_tolerance = self.lineEdit_geometry_tolerance.text()

            config['PROJECT']['Import type'] = str(0)
            config['PROJECT']['Geometry file'] = geometry_file_name
            config['PROJECT']['Geometry state'] = str(0)
            config['PROJECT']['Element size'] = element_size
            config['PROJECT']['Geometry tolerance'] = geometry_tolerance

        config['PROJECT']['Material list file'] = self.material_list_name
        config['PROJECT']['Fluid list file'] = self.fluid_list_name
        
        with open(self.project_file_path, 'w') as config_file:
            config.write(config_file)

    def create_material_file(self):
        self.material_list_path = get_new_path(self.project_folder_path, self.material_list_name)
        default_material_library(self.material_list_path)

    def create_fluid_file(self):
        self.fluid_list_path = get_new_path(self.project_folder_path, self.fluid_list_name)
        default_fluid_library(self.fluid_list_path)