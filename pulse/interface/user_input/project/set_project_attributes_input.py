from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QPushButton, QRadioButton, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copytree, rmtree

from pulse import UI_DIR
from pulse.utils import get_new_path
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class SetProjectAttributesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "/project/set_project_attributes.ui", self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.project = project
        self.opv = opv

        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.create = False
        self.stop = False

        self.currentTab = 0

        self.userPath = os.path.expanduser('~')
        self.current_project_file_path = self.project.file._project_path
        self.project_directory = os.path.dirname(self.current_project_file_path)
        self.project_name = self.project.file._project_name

        self.project_ini = self.project.file._project_base_name
        self.current_geometry_path = self.project.file.geometry_path
        self.current_material_list_path = self.project.file._material_list_path
        self.current_fluid_list_path = self.project.file._fluid_list_path

        self.current_conn_path = self.project.file._conn_path
        self.current_coord_path_path = self.project.file._coord_path
        self.import_type = self.project.file._import_type
        
        self.lineEdit_current_project_name = self.findChild(QLineEdit, 'lineEdit_current_project_name')
        self.lineEdit_current_project_folder = self.findChild(QLineEdit, 'lineEdit_current_project_folder')
        self.lineEdit_new_project_name = self.findChild(QLineEdit, 'lineEdit_new_project_name')
        self.lineEdit_new_project_folder = self.findChild(QLineEdit, 'lineEdit_new_project_folder')

        self.lineEdit_current_project_name.setText(self.project_name)
        self.lineEdit_current_project_folder.setText(self.project_directory)

        self.toolButton_clean_project_name = self.findChild(QToolButton, 'toolButton_clean_project_name')
        self.toolButton_clean_project_name.clicked.connect(self.clean_project_name)

        self.toolButton_search_project_folder = self.findChild(QToolButton, 'toolButton_search_project_folder')
        self.toolButton_search_project_folder.clicked.connect(self.search_project_folder)

        self.radioButton_projectName = self.findChild(QRadioButton, 'radioButton_projectName')
        self.radioButton_projectDirectory = self.findChild(QRadioButton, 'radioButton_projectDirectory')
        self.radioButton_projectNameDirectory = self.findChild(QRadioButton, 'radioButton_projectNameDirectory')

        self.radioButton_projectName.toggled.connect(self.update_texts_and_controls)
        self.radioButton_projectDirectory.toggled.connect(self.update_texts_and_controls)
        self.radioButton_projectNameDirectory.toggled.connect(self.update_texts_and_controls)

        self.radioButton_maintain_current_project_folder = self.findChild(QRadioButton, 'radioButton_maintain_current_project_folder')
        self.radioButton_remove_current_project_folder = self.findChild(QRadioButton, 'radioButton_remove_current_project_folder')

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.check_entries_and_confirm)

        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_cancel.clicked.connect(self.cancel_and_close)

        if self.radioButton_projectName.isChecked():
            self.lineEdit_new_project_folder.setText(self.project_directory)
            self.lineEdit_new_project_folder.setDisabled(True)
            self.toolButton_search_project_folder.setDisabled(True)

        self.exec()

    def update_texts_and_controls(self):
        if self.radioButton_projectName.isChecked():
            self.lineEdit_new_project_folder.setText(self.project_directory)
            self.lineEdit_new_project_name.setText("")
            self.lineEdit_new_project_name.setDisabled(False)
            self.lineEdit_new_project_folder.setDisabled(True)
            self.toolButton_clean_project_name.setDisabled(False)
            self.toolButton_search_project_folder.setDisabled(True)
        elif self.radioButton_projectDirectory.isChecked():
            self.lineEdit_new_project_folder.setText("")
            self.lineEdit_new_project_name.setText(self.project_name)
            self.lineEdit_new_project_name.setDisabled(True)
            self.lineEdit_new_project_folder.setDisabled(False)
            self.toolButton_clean_project_name.setDisabled(True)
            self.toolButton_search_project_folder.setDisabled(False)
        elif self.radioButton_projectNameDirectory.isChecked():
            if self.lineEdit_new_project_name.text() == self.lineEdit_current_project_name.text():
                self.lineEdit_new_project_name.setText("")
            if self.lineEdit_new_project_folder.text() == self.lineEdit_current_project_folder.text():  
                self.lineEdit_new_project_folder.setText("")
            self.lineEdit_new_project_name.setDisabled(False)
            self.toolButton_clean_project_name.setDisabled(False)
            self.lineEdit_new_project_folder.setDisabled(False)
            self.toolButton_search_project_folder.setDisabled(False)
 
    def cancel_and_close(self):
        self.close()

    def clean_project_name(self):
        self.lineEdit_new_project_name.setText("")

    def check_entries_and_confirm(self):
        self.check_modification_type()
        if self.lineEdit_new_project_name.text() != "":
            if self.lineEdit_new_project_folder.text() != "":
                self.copyTreeProjectFiles()
                self.update_all_file_paths()
                self.update_project_ini_name()
                if self.radioButton_remove_current_project_folder.isChecked():
                    rmtree(self.current_project_file_path)
                self.close()
            else:
                self.search_project_folder()
                return self.check_entries_and_confirm()
        else:
            message_title = "Empty project name"
            message = "Please, inform a valid project name at 'New project name' input field to continue."
            PrintMessageInput([message_title, message, window_title_2])

    def search_project_folder(self):
        self.new_project_directory = QFileDialog.getExistingDirectory(None, 'Choose a new folder to save the project files', self.userPath)
        self.lineEdit_new_project_folder.setText(str(self.new_project_directory))        

    def copyTreeProjectFiles(self):  
        self.new_project_folder_path = get_new_path(self.new_project_folder, self.new_project_name)
        copytree(self.current_project_file_path, self.new_project_folder_path)

    def update_all_file_paths(self):
        new_geometry_path = get_new_path(self.new_project_folder_path, os.path.basename(self.current_geometry_path))
        new_material_list_path = get_new_path(self.new_project_folder_path, os.path.basename(self.current_material_list_path))
        new_fluid_list_path = get_new_path(self.new_project_folder_path, os.path.basename(self.current_fluid_list_path))
        if self.import_type == 0:
            self.project.copy_project(  self.new_project_folder_path, 
                                        self.new_project_name, 
                                        new_material_list_path, 
                                        new_fluid_list_path, 
                                        geometry_path = new_geometry_path)
        elif self.import_type == 1:
            pass

    def check_modification_type(self):
        if self.radioButton_projectName.isChecked():
            self.new_project_folder = self.lineEdit_current_project_folder.text()
            self.new_project_name =  self.lineEdit_new_project_name.text()
            self.current_project_folder = self.lineEdit_current_project_folder.text()
            self.current_project_name = self.lineEdit_current_project_name.text()
        elif self.radioButton_projectDirectory.isChecked():
            self.new_project_folder = self.lineEdit_new_project_folder.text()
            self.new_project_name =  self.lineEdit_current_project_name.text()
            self.current_project_folder = self.lineEdit_current_project_folder.text()
            self.current_project_name = self.lineEdit_current_project_name.text()
        elif self.radioButton_projectNameDirectory.isChecked():
            self.new_project_folder = self.lineEdit_new_project_folder.text()
            self.new_project_name =  self.lineEdit_new_project_name.text()
            self.current_project_folder = self.lineEdit_current_project_folder.text()
            self.current_project_name = self.lineEdit_current_project_name.text()
        
    def update_project_ini_name(self):
        project_ini_file_path = get_new_path(self.new_project_folder_path, self.project_ini)
        config = configparser.ConfigParser()
        config.read(project_ini_file_path)

        config['PROJECT']['Name'] = self.new_project_name
        
        with open(project_ini_file_path, 'w') as config_file:
            config.write(config_file)