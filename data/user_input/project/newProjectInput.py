from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import configparser
from shutil import copyfile
import numpy as np

from pulse.project import Project
from pulse.default_libraries import default_material_library, default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class NewProjectInput(QDialog):
    def __init__(self, project, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/newProjectInput.ui', self)

        icons_path = 'data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.config = config
        self.create = False
        self.stop = False

        self.currentTab = 0

        self.userPath = os.path.expanduser('~')
        self.project_directory = ""
        self.project_folder_path = ""
        self.project_file_path = ""

        self.materialListName = "materialList.dat"
        self.fluidListName = "fluidList.dat"
        self.projectFileName = "project.ini"
        self.material_list_path = ""
        self.fluid_list_path = ""

        self.button_create_project = self.findChild(QDialogButtonBox, 'button_create_project')
        self.button_create_project.accepted.connect(self.accept_project)
        self.button_create_project.rejected.connect(self.reject_project)

        self.line_project_name = self.findChild(QLineEdit, 'line_project_name')
        self.lineEdit_project_folder = self.findChild(QLineEdit, 'lineEdit_project_folder')
        self.line_import_geometry = self.findChild(QLineEdit, 'line_import_geometry')
        self.line_element_size = self.findChild(QLineEdit, 'line_element_size')

        self.line_import_cord = self.findChild(QLineEdit, 'line_cord')
        self.line_import_conn = self.findChild(QLineEdit, 'line_conn')

        self.toolButton_import_geometry = self.findChild(QToolButton, 'toolButton_import_geometry')
        self.toolButton_import_geometry.clicked.connect(self.import_geometry)

        self.toolButton_import_cord = self.findChild(QToolButton, 'toolButton_import_cord')
        self.toolButton_import_cord.clicked.connect(self.import_cord)

        self.toolButton_import_conn = self.findChild(QToolButton, 'toolButton_import_conn')
        self.toolButton_import_conn.clicked.connect(self.import_conn)

        self.toolButton_search_project_folder = self.findChild(QToolButton, 'toolButton_search_project_folder')
        self.toolButton_search_project_folder.clicked.connect(self.search_project_folder)

        self.tabWidget = self.findChild(QTabWidget, 'tabWidget')
        self.tabWidget.currentChanged.connect(self.tabEvent)
        self.currentTab = self.tabWidget.currentIndex()

        self.exec_()

    def createProjectFolder(self):
        if self.line_project_name.text() == "":
            title = 'Empty project name'
            message = "Please, inform a valid project name to continue."
            PrintMessageInput([title, message, window_title1])
            self.stop = True
            return
        
        if self.lineEdit_project_folder.text() == "":
            title = 'None project folder selected'
            message = "Please, select a folder where the project data are going to be stored."
            PrintMessageInput([title, message, window_title1])
            self.stop = True
            return

        if not os.path.exists(self.project_directory):
            os.mkdir(self.project_directory)

        self.stop = False

    def tabEvent(self):
        self.currentTab = self.tabWidget.currentIndex()

    def search_project_folder(self):

        self.project_directory = QFileDialog.getExistingDirectory(None, 'Choose a folder to save the project files', self.userPath)
        self.lineEdit_project_folder.setText(str(self.project_directory))        

    def accept_project(self):
        self.createProjectFolder()
        if self.stop:
            return

        if self.line_project_name.text() in os.listdir(self.project_directory):
            title = 'Error in project name'
            message = "This project name already exists, you should use a different project name to continue."
            PrintMessageInput([title, message, window_title1])
            return

        if self.currentTab == 0: #.iges
            if self.line_import_geometry.text() == "":
                title = 'Empty geometry at selection'
                message = "Please, select a valid *.iges format geometry to continue."
                PrintMessageInput([title, message, window_title1])
                return
            if self.line_element_size.text() == "":
                title = 'Empty element size'
                message = "Please, inform a valid input to the element size."
                PrintMessageInput([title, message, window_title1])
                return
            else:
                try:
                    float(self.line_element_size.text())
                except Exception:
                    title = 'Invalid element size'
                    message = "Please, inform a valid input to the element size."
                    PrintMessageInput([title, message, window_title1])
                    return
        
        if self.currentTab == 1: #.dat
            if self.line_import_cord.text() == "":
                title = 'None nodal coordinates matrix file selected'
                message = "Please, select a valid nodal coordinates matrix file to continue."
                PrintMessageInput([title, message, window_title1])
                return

            if self.line_import_conn.text() == "" :
                title = 'None connectivity matrix file selected'
                message = "Please, select a valid connectivity matrix file to continue."
                PrintMessageInput([title, message, window_title1])
                return
   
        if self.createProject():
            self.create = True
            self.close()

    def reject_project(self):
        self.close()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Iges Files (*.iges)')
        self.line_import_geometry.setText(str(self.path))

    def import_cord(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.line_import_cord.setText(str(self.path))

    def import_conn(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Dat Files (*.dat)')
        self.line_import_conn.setText(str(self.path))

    def createProject(self):

        if "\\" in self.project_directory:
            self.project_folder_path = '{}\\{}'.format(self.project_directory, self.line_project_name.text())
        elif "/" in self.project_directory:
            self.project_folder_path = '{}/{}'.format(self.project_directory, self.line_project_name.text())

        if not os.path.exists(self.project_folder_path):
            os.makedirs(self.project_folder_path)

        self.createMaterialFile()
        self.createFluidFile()
        self.createProjectFile()
        
        if self.currentTab == 0:
            geometry_file_name = self.line_import_geometry.text().split('/')[-1]
            new_geometry_path = "{}\\{}".format(self.project_folder_path, geometry_file_name)
            copyfile(self.line_import_geometry.text(), new_geometry_path)
            element_size = float(self.line_element_size.text())
            import_type = 0
            self.config.writeRecentProject(self.line_project_name.text(), self.project_file_path)
            self.project.new_project(self.project_folder_path, self.line_project_name.text(), element_size, import_type, self.material_list_path, self.fluid_list_path, geometry_path=new_geometry_path)
            return True
            
        elif self.currentTab == 1:
            cord_file = self.line_import_cord.text().split('/')[-1]
            conn_file = self.line_import_conn.text().split('/')[-1]
            new_cord_path = "{}\\{}".format(self.project_folder_path, cord_file)
            new_conn_path = "{}\\{}".format(self.project_folder_path, conn_file)
            copyfile(self.line_import_cord.text(), new_cord_path)
            copyfile(self.line_import_conn.text(), new_conn_path)
            element_size = 0
            import_type = 1
            self.config.writeRecentProject(self.line_project_name.text(), self.project_file_path)
            self.project.new_project(self.project_folder_path, self.line_project_name.text(), element_size, import_type, self.material_list_path, self.fluid_list_path, conn_path=new_conn_path, coord_path=new_cord_path)
            return True
        return False

    def createProjectFile(self):

        if "\\" in self.project_directory:
            self.project_file_path = '{}\\{}'.format(self.project_folder_path, self.projectFileName)
        elif "/" in self.project_directory:
            self.project_file_path = '{}/{}'.format(self.project_folder_path, self.projectFileName)

        config = configparser.ConfigParser()
        config['PROJECT'] = {}
        config['PROJECT']['Name'] = self.line_project_name.text()

        if self.currentTab == 0:
            geometry_file_name = self.line_import_geometry.text().split('/')[-1]
            element_size = self.line_element_size.text()

            config['PROJECT']['Import type'] = str(0)
            config['PROJECT']['Element size'] = str(element_size)
            config['PROJECT']['Geometry file'] = geometry_file_name

        elif self.currentTab == 1:
            nodal_coordinates_filename = self.line_import_cord.text().split('/')[-1]
            connectivity_matrix_filename = self.line_import_conn.text().split('/')[-1]
            config['PROJECT']['Import type'] = str(1)
            config['PROJECT']['Nodal coordinates file'] = nodal_coordinates_filename
            config['PROJECT']['Connectivity matrix file'] = connectivity_matrix_filename
        
        config['PROJECT']['Material list file'] = self.materialListName
        config['PROJECT']['Fluid list file'] = self.fluidListName
        
        with open(self.project_file_path, 'w') as config_file:
            config.write(config_file)

    def createMaterialFile(self):

        if "\\" in self.project_directory:
            self.material_list_path = '{}\\{}'.format(self.project_folder_path, self.materialListName)
        elif "/" in self.project_directory:
            self.material_list_path = '{}/{}'.format(self.project_folder_path, self.materialListName)

        default_material_library(self.material_list_path)

    def createFluidFile(self):

        if "\\" in self.project_directory:
            self.fluid_list_path = '{}\\{}'.format(self.project_folder_path, self.fluidListName)
        elif "/" in self.project_directory:
            self.fluid_list_path = '{}/{}'.format(self.project_folder_path, self.fluidListName)

        default_fluid_library(self.fluid_list_path)