from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QLineEdit, QTabWidget, QToolButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copyfile
from time import time

from pulse.project import Project
from pulse.lib.default_libraries import default_material_library, default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.geometryDesignerInput import GeometryDesignerInput
from pulse.utils import get_new_path

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class NewProjectInput(QDialog):
    def __init__(self, project, opv, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Project/newProjectInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.opv = opv
        self.config = config
        self.create = False
        self.stop = False

        self.currentTab = 0

        self.userPath = os.path.expanduser('~')
        self.project_directory = ""
        self.project_folder_path = ""
        self.project_file_path = ""

        self.materialListName = self.project.file._material_file_name
        self.fluidListName = self.project.file._fluid_file_name
        self.projectFileName = self.project.file._project_base_name
        self.material_list_path = ""
        self.fluid_list_path = ""

        self._define_Qt_variables()
        self._create_Qt_actions()
        self.currentTab = self.tabWidget_new_project.currentIndex()

        self.exec()

    def _define_Qt_variables(self):
        self.lineEdit_project_name = self.findChild(QLineEdit, 'lineEdit_project_name')
        self.lineEdit_project_folder = self.findChild(QLineEdit, 'lineEdit_project_folder')
        self.lineEdit_import_geometry = self.findChild(QLineEdit, 'lineEdit_import_geometry')
        self.lineEdit_element_size = self.findChild(QLineEdit, 'lineEdit_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_import_nodal_coordinates = self.findChild(QLineEdit, 'lineEdit_import_nodal_coordinates')
        self.lineEdit_import_connectivity = self.findChild(QLineEdit, 'lineEdit_import_connectivity')
        self.focus_lineEdit_project_name_if_blank()

        self.toolButton_import_geometry = self.findChild(QToolButton, 'toolButton_import_geometry')
        self.toolButton_create_empty_project = self.findChild(QToolButton, 'toolButton_create_empty_project')
        self.toolButton_import_cord = self.findChild(QToolButton, 'toolButton_import_cord')
        self.toolButton_import_conn = self.findChild(QToolButton, 'toolButton_import_conn')
        self.toolButton_search_project_folder = self.findChild(QToolButton, 'toolButton_search_project_folder')

        self.button_create_project = self.findChild(QDialogButtonBox, 'button_create_project')
        self.tabWidget_new_project = self.findChild(QTabWidget, 'tabWidget_new_project')
        self.tabWidget_new_project.removeTab(2)

    def _create_Qt_actions(self):    
        self.button_create_project.accepted.connect(self.accept_project)
        self.button_create_project.rejected.connect(self.reject_project)
        self.toolButton_import_geometry.clicked.connect(self.import_geometry)
        self.toolButton_create_empty_project.clicked.connect(self.accept_project)
        self.toolButton_import_cord.clicked.connect(self.import_cord)
        self.toolButton_import_conn.clicked.connect(self.import_conn)
        self.toolButton_search_project_folder.clicked.connect(self.search_project_folder)
        self.tabWidget_new_project.currentChanged.connect(self.tabEvent)

    def createProjectFolder(self):
        if self.lineEdit_project_name.text() == "":
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
        self.currentTab = self.tabWidget_new_project.currentIndex()
        self.focus_lineEdit_project_name_if_blank()

    def focus_lineEdit_project_name_if_blank(self):
        if self.lineEdit_project_name.text() == "":
            self.lineEdit_project_name.setFocus()

    def search_project_folder(self):

        self.project_directory = QFileDialog.getExistingDirectory(None, 'Choose a folder to save the project files', self.userPath)
        self.lineEdit_project_folder.setText(str(self.project_directory))        

    def accept_project(self):
        t0 = time()
        self.createProjectFolder()
        if self.stop:
            self.project.time_to_load_or_create_project = 0
            return

        if self.lineEdit_project_name.text() in os.listdir(self.project_directory):
            title = 'Error in project name'
            message = "This project name already exists, you should use a different project name to continue."
            PrintMessageInput([title, message, window_title1])
            return

        if self.currentTab == 1: # .iges & .step
            if self.lineEdit_import_geometry.text() == "":
                title = 'Empty geometry at selection'
                message = "Please, select a valid *.iges or *.step format geometry to continue."
                PrintMessageInput([title, message, window_title1])
                return
            if self.lineEdit_element_size.text() == "":
                title = 'Empty element size'
                message = "Please, inform a valid input to the element size."
                PrintMessageInput([title, message, window_title1])
                return
            else:
                try:
                    float(self.lineEdit_element_size.text())
                except Exception:
                    title = 'Invalid element size'
                    message = "Please, inform a valid input to the element size."
                    PrintMessageInput([title, message, window_title1])
                    return

            if self.lineEdit_geometry_tolerance.text() == "":
                title = 'Empty geometry tolerance'
                message = "Please, inform a valid input to the geometry tolerance."
                PrintMessageInput([title, message, window_title1])
                return
            else:
                try:
                    float(self.lineEdit_geometry_tolerance.text())
                except Exception:
                    title = 'Invalid geometry tolerance'
                    message = "Please, inform a valid input to the geometry tolerance."
                    PrintMessageInput([title, message, window_title1])
                    return        

        if self.currentTab == 2: #.dat
            if self.lineEdit_import_nodal_coordinates.text() == "":
                title = 'None nodal coordinates matrix file selected'
                message = "Please, select a valid nodal coordinates matrix file to continue."
                PrintMessageInput([title, message, window_title1])
                return

            if self.lineEdit_import_connectivity.text() == "" :
                title = 'None connectivity matrix file selected'
                message = "Please, select a valid connectivity matrix file to continue."
                PrintMessageInput([title, message, window_title1])
                return
   
        if self.createProject():
            self.create = True
            self.project.time_to_load_or_create_project = time() - t0
            self.close()

    def reject_project(self):
        self.close()

    def import_geometry(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.iges *.igs *.step *.stp)')
        self.lineEdit_import_geometry.setText(str(self.path))

    def import_cord(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.csv; *.dat; *.txt)')
        self.lineEdit_import_nodal_coordinates.setText(str(self.path))

    def import_conn(self):
        self.path, _type = QFileDialog.getOpenFileName(None, 'Open file', self.userPath, 'Files (*.csv; *.dat; *.txt)')
        self.lineEdit_import_connectivity.setText(str(self.path))

    def createProject(self):

        self.project_folder_path = get_new_path(self.project_directory, self.lineEdit_project_name.text())

        if not os.path.exists(self.project_folder_path):
            os.makedirs(self.project_folder_path)

        self.createMaterialFile()
        self.createFluidFile()
        self.createProjectFile()
        
        if self.tabWidget_new_project.currentIndex() == 0:
            project_name = self.lineEdit_project_name.text()
            import_type = 1
            self.config.writeRecentProject(self.project_file_path)
            self.project.new_empty_project( self.project_folder_path, 
                                            project_name,
                                            import_type, 
                                            self.material_list_path, 
                                            self.fluid_list_path )
            return True

        elif self.tabWidget_new_project.currentIndex() == 1:
            geometry_filename = os.path.basename(self.lineEdit_import_geometry.text())
            new_geometry_path = get_new_path(self.project_folder_path, geometry_filename)
            copyfile(self.lineEdit_import_geometry.text(), new_geometry_path)
            project_name = self.lineEdit_project_name.text()
            element_size = float(self.lineEdit_element_size.text())
            geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
            import_type = 0
            self.config.writeRecentProject(self.project_file_path)
            self.project.new_project(   self.project_folder_path, 
                                        project_name, 
                                        element_size,
                                        geometry_tolerance, 
                                        import_type, 
                                        self.material_list_path, 
                                        self.fluid_list_path, 
                                        geometry_path=new_geometry_path   )
            return True
        
        elif self.tabWidget_new_project.currentIndex() == 2:
            nodal_coordinates_filename = os.path.basename(self.lineEdit_import_nodal_coordinates.text())
            connectivity_filename = os.path.basename(self.lineEdit_import_connectivity.text())
            new_cord_path = get_new_path(self.project_folder_path, nodal_coordinates_filename)
            new_conn_path = get_new_path(self.project_folder_path, connectivity_filename)
            copyfile(self.lineEdit_import_nodal_coordinates.text(), new_cord_path)
            copyfile(self.lineEdit_import_connectivity.text(), new_conn_path)
            project_name = self.lineEdit_project_name.text()
            element_size = 0
            import_type = 2
            self.config.writeRecentProject(self.project_file_path)
            self.project.new_project(   self.project_folder_path, 
                                        project_name, 
                                        element_size, import_type, 
                                        self.material_list_path, 
                                        self.fluid_list_path, 
                                        conn_path=new_conn_path, 
                                        coord_path=new_cord_path   )
            return True
        return False

    def createProjectFile(self):

        self.project_file_path = get_new_path(self.project_folder_path, self.projectFileName)

        config = configparser.ConfigParser()
        config['PROJECT'] = {}
        config['PROJECT']['Name'] = self.lineEdit_project_name.text()

        if self.tabWidget_new_project.currentIndex() == 0:
            config['PROJECT']['Import type'] = str(1)
            # config['PROJECT']['Geometry file'] = ""

        elif self.tabWidget_new_project.currentIndex() == 1:
            geometry_file_name = os.path.basename(self.lineEdit_import_geometry.text())
            element_size = self.lineEdit_element_size.text()
            geometry_tolerance = self.lineEdit_geometry_tolerance.text()

            config['PROJECT']['Import type'] = str(0)
            config['PROJECT']['Geometry file'] = geometry_file_name
            config['PROJECT']['Geometry state'] = str(0)
            config['PROJECT']['Element size'] = element_size
            config['PROJECT']['Geometry tolerance'] = geometry_tolerance

        elif self.tabWidget_new_project.currentIndex() == 2:
            nodal_coordinates_filename = os.path.basename(self.lineEdit_import_nodal_coordinates.text())
            connectivity_matrix_filename = os.path.basename(self.lineEdit_import_connectivity.text())
            config['PROJECT']['Import type'] = str(2)
            config['PROJECT']['Nodal coordinates file'] = nodal_coordinates_filename
            config['PROJECT']['Connectivity matrix file'] = connectivity_matrix_filename
        
        config['PROJECT']['Material list file'] = self.materialListName
        config['PROJECT']['Fluid list file'] = self.fluidListName
        
        with open(self.project_file_path, 'w') as config_file:
            config.write(config_file)

    def createMaterialFile(self):
        self.material_list_path = get_new_path(self.project_folder_path, self.materialListName)
        default_material_library(self.material_list_path)

    def createFluidFile(self):
        self.fluid_list_path = get_new_path(self.project_folder_path, self.fluidListName)
        default_fluid_library(self.fluid_list_path)