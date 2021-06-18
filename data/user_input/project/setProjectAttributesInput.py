from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QRadioButton, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import configparser
from shutil import copyfile, copy, copytree, rmtree
import numpy as np

from pulse.project import Project
from pulse.default_libraries import default_material_library, default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class SetProjectAttributesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/setProjectAttributesInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
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
        self.current_geometry_path = self.project.file._geometry_path
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

        self.exec_()

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
            window_title = "WARNING"
            message_title = "Empty project name"
            message = "Please, inform a valid project name at 'New project name' input field to continue."
            PrintMessageInput([message_title, message, window_title])

    def search_project_folder(self):

        self.new_project_directory = QFileDialog.getExistingDirectory(None, 'Choose a new folder to save the project files', self.userPath)
        self.lineEdit_new_project_folder.setText(str(self.new_project_directory))        

    def copyTreeProjectFiles(self):  
        self.new_project_folder_path = self.get_new_path(self.new_project_folder, self.new_project_name)
        copytree(self.current_project_file_path, self.new_project_folder_path)

    def get_new_path(self, path, name):
        if "\\" in path:
            new_path = '{}\\{}'.format(path, name)
        elif "/" in path:
            new_path = '{}/{}'.format(path, name)
        return new_path

    def update_all_file_paths(self):
        new_geometry_path = self.get_new_path(self.new_project_folder_path, os.path.basename(self.current_geometry_path))
        new_material_list_path = self.get_new_path(self.new_project_folder_path, os.path.basename(self.current_material_list_path))
        new_fluid_list_path = self.get_new_path(self.new_project_folder_path, os.path.basename(self.current_fluid_list_path))
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
        project_ini_file_path = self.get_new_path(self.new_project_folder_path, self.project_ini)
        config = configparser.ConfigParser()
        config.read(project_ini_file_path)

        config['PROJECT']['Name'] = self.new_project_name
        
        with open(project_ini_file_path, 'w') as config_file:
            config.write(config_file)

    # def createProjectFolder(self):
    #     if self.line_project_name.text() == "":
    #         title = 'Empty project name'
    #         message = "Please, inform a valid project name to continue."
    #         PrintMessageInput([title, message, window_title1])
    #         self.stop = True
    #         return
        
    #     if self.lineEdit_project_folder.text() == "":
    #         title = 'None project folder selected'
    #         message = "Please, select a folder where the project data are going to be stored."
    #         PrintMessageInput([title, message, window_title1])
    #         self.stop = True
    #         return

    #     if not os.path.exists(self.project_directory):
    #         os.mkdir(self.project_directory)

    #     self.stop = False

    # def tabEvent(self):
    #     self.currentTab = self.tabWidget.currentIndex()

    # def accept_project(self):
    #     self.createProjectFolder()
    #     if self.stop:
    #         return

    #     if self.line_project_name.text() in os.listdir(self.project_directory):
    #         title = 'Error in project name'
    #         message = "This project name already exists, you should use a different project name to continue."
    #         PrintMessageInput([title, message, window_title1])
    #         return

    #     if self.currentTab == 0: #.iges
    #         if self.line_import_geometry.text() == "":
    #             title = 'Empty geometry at selection'
    #             message = "Please, select a valid *.iges format geometry to continue."
    #             PrintMessageInput([title, message, window_title1])
    #             return
    #         if self.line_element_size.text() == "":
    #             title = 'Empty element size'
    #             message = "Please, inform a valid input to the element size."
    #             PrintMessageInput([title, message, window_title1])
    #             return
    #         else:
    #             try:
    #                 float(self.line_element_size.text())
    #             except Exception:
    #                 title = 'Invalid element size'
    #                 message = "Please, inform a valid input to the element size."
    #                 PrintMessageInput([title, message, window_title1])
    #                 return
        
    #     if self.currentTab == 1: #.dat
    #         if self.line_import_cord.text() == "":
    #             title = 'None nodal coordinates matrix file selected'
    #             message = "Please, select a valid nodal coordinates matrix file to continue."
    #             PrintMessageInput([title, message, window_title1])
    #             return

    #         if self.line_import_conn.text() == "" :
    #             title = 'None connectivity matrix file selected'
    #             message = "Please, select a valid connectivity matrix file to continue."
    #             PrintMessageInput([title, message, window_title1])
    #             return
   
    #     if self.createProject():
    #         self.create = True
    #         self.close()

    # def reject_project(self):
    #     self.close()

    # def import_geometry(self):
    #     self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Iges Files (*.iges)')
    #     self.line_import_geometry.setText(str(self.path))

    # def import_cord(self):
    #     self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
    #     self.line_import_cord.setText(str(self.path))

    # def import_conn(self):
    #     self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
    #     self.line_import_conn.setText(str(self.path))


    #     if not os.path.exists(self.project_folder_path):
    #         os.makedirs(self.project_folder_path)

    #     self.createMaterialFile()
    #     self.createFluidFile()
    #     self.createProjectFile()
        
    #     if self.currentTab == 0:
    #         geometry_file_name = self.line_import_geometry.text().split('/')[-1]
    #         new_geometry_path = "{}\\{}".format(self.project_folder_path, geometry_file_name)
    #         copyfile(self.line_import_geometry.text(), new_geometry_path)
    #         element_size = float(self.line_element_size.text())
    #         import_type = 0
    #         self.config.writeRecentProject(self.line_project_name.text(), self.current_project_file_path)
    #         self.project.new_project(self.project_folder_path, self.line_project_name.text(), element_size, import_type, self.material_list_path, self.fluid_list_path, geometry_path=new_geometry_path)
    #         return True
            
    #     elif self.currentTab == 1:
    #         cord_file = self.line_import_cord.text().split('/')[-1]
    #         conn_file = self.line_import_conn.text().split('/')[-1]
    #         new_cord_path = "{}\\{}".format(self.project_folder_path, cord_file)
    #         new_conn_path = "{}\\{}".format(self.project_folder_path, conn_file)
    #         copyfile(self.line_import_cord.text(), new_cord_path)
    #         copyfile(self.line_import_conn.text(), new_conn_path)
    #         element_size = 0
    #         import_type = 1
    #         self.config.writeRecentProject(self.line_project_name.text(), self.current_project_file_path)
    #         self.project.new_project(self.project_folder_path, self.line_project_name.text(), element_size, import_type, self.material_list_path, self.fluid_list_path, conn_path=new_conn_path, coord_path=new_cord_path)
    #         return True
    #     return False

    # def createProjectFile(self):

    #     if "\\" in self.project_directory:
    #         self.current_project_file_path = '{}\\{}'.format(self.project_folder_path, self.projectFileName)
    #     elif "/" in self.project_directory:
    #         self.current_project_file_path = '{}/{}'.format(self.project_folder_path, self.projectFileName)

    #     config = configparser.ConfigParser()
    #     config['PROJECT'] = {}
    #     config['PROJECT']['Name'] = self.line_project_name.text()

    #     if self.currentTab == 0:
    #         geometry_file_name = self.line_import_geometry.text().split('/')[-1]
    #         element_size = self.line_element_size.text()

    #         config['PROJECT']['Import type'] = str(0)
    #         config['PROJECT']['Element size'] = str(element_size)
    #         config['PROJECT']['Geometry file'] = geometry_file_name

    #     elif self.currentTab == 1:
    #         nodal_coordinates_filename = self.line_import_cord.text().split('/')[-1]
    #         connectivity_matrix_filename = self.line_import_conn.text().split('/')[-1]
    #         config['PROJECT']['Import type'] = str(1)
    #         config['PROJECT']['Nodal coordinates file'] = nodal_coordinates_filename
    #         config['PROJECT']['Connectivity matrix file'] = connectivity_matrix_filename
        
    #     config['PROJECT']['Material list file'] = self.materialListName
    #     config['PROJECT']['Fluid list file'] = self.fluidListName
        
    #     with open(self.current_project_file_path, 'w') as config_file:
    #         config.write(config_file)

    # def createMaterialFile(self):

    #     if "\\" in self.project_directory:
    #         self.material_list_path = '{}\\{}'.format(self.project_folder_path, self.materialListName)
    #     elif "/" in self.project_directory:
    #         self.material_list_path = '{}/{}'.format(self.project_folder_path, self.materialListName)

    #     default_material_library(self.material_list_path)

    # def createFluidFile(self):

    #     if "\\" in self.project_directory:
    #         self.fluid_list_path = '{}\\{}'.format(self.project_folder_path, self.fluidListName)
    #     elif "/" in self.project_directory:
    #         self.fluid_list_path = '{}/{}'.format(self.project_folder_path, self.fluidListName)

    #     default_fluid_library(self.fluid_list_path)