from PyQt5.QtWidgets import QToolButton, QLineEdit, QDialogButtonBox, QFileDialog, QDialog, QMessageBox, QTabWidget, QRadioButton, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import configparser
from shutil import copyfile
import numpy as np

from pulse.utils import get_new_path
from pulse.project import Project
from pulse.default_libraries import default_material_library, default_fluid_library
from data.user_input.project.printMessageInput import PrintMessageInput

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

class SetGeometryFileInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/setGeometryFileInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
        self.setWindowIcon(self.icon)

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.project = project
        self.opv = opv
        # self.config = config
        self.create = False
        self.stop = False

        self.currentTab = 0

        self.userPath = os.path.expanduser('~')
        self.current_project_file_path = self.project.file._project_path
        self.project_directory = os.path.dirname(self.current_project_file_path)
        self.project_name = self.project.file._project_name
        self.element_size = self.project.file._element_size
        self.geometry_tolerance = self.project.file._geometry_tolerance
        self.project_ini = self.project.file._project_base_name

        self.current_geometry_path = self.project.file._geometry_path
        self.current_material_list_path = self.project.file._material_list_path
        self.current_fluid_list_path = self.project.file._fluid_list_path

        # self.current_conn_path = self.project.file._conn_path
        # self.current_coord_path_path = self.project.file._coord_path
        self.import_type = self.project.file._import_type

        self.materialListName = "materialList.dat"
        self.fluidListName = "fluidList.dat"
        self.projectFileName = "project.ini"
        self.material_list_path = ""
        self.fluid_list_path = ""

        self.lineEdit_current_geometry_file_path = self.findChild(QLineEdit, 'lineEdit_current_geometry_file_path')
        self.lineEdit_new_geometry_file_path = self.findChild(QLineEdit, 'lineEdit_new_geometry_file_path')

        self.lineEdit_current_geometry_file_path.setText(self.project.file._geometry_path)

        self.lineEdit_element_size = self.findChild(QLineEdit, 'lineEdit_element_size')
        self.lineEdit_element_size.setText(str(self.element_size))
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_geometry_tolerance.setText(str(self.geometry_tolerance))
       
        self.toolButton_search_new_geometry_file = self.findChild(QToolButton, 'toolButton_search_new_geometry_file')
        self.toolButton_search_new_geometry_file.clicked.connect(self.search_new_geometry_file)

        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_confirm.clicked.connect(self.confirm_and_update_model)
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')
        self.pushButton_cancel.clicked.connect(self.cancel)

        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_update_model()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def cancel(self):
        self.close()

    def confirm_and_update_model(self):
        if self.lineEdit_new_geometry_file_path.text() == "":
            self.search_new_geometry_file()

        if self.check_all_input_mesh_settings():
            if self.copy_geometry_file_to_project_folder():
                self.print_warning_same_geometry_selected()
                return
            else:
                self.remove_other_files()
            
            self.project.new_project(   self.current_project_file_path,
                                        self.project_name,
                                        self.new_element_size,
                                        self.new_geometry_tolerance,
                                        self.import_type,
                                        self.current_material_list_path,
                                        self.current_fluid_list_path,
                                        geometry_path = self.new_geometry_path   )

            # self.project.reset_project()

            self.update_project_settings()
            self.project.file.reset_project_setup()
            # self.remove_other_files()
            self.opv.opvRenderer.plot()
            self.opv.changePlotToEntities()
            self.close()

    def search_new_geometry_file(self):
        self.selected_geometry_path, _type = QFileDialog.getOpenFileName(None, 'Choose a valid geometry file', self.userPath, 'Iges Files (*.iges)')        
        self.geometry_filename = os.path.basename(self.selected_geometry_path)
        self.lineEdit_new_geometry_file_path.setText(str(self.selected_geometry_path))  

    def check_all_input_mesh_settings(self):
        if self.check_element_size_input_value():
            return False
        if self.check_geometry_tolerance_input_value():
            return False       
        if self.new_element_size > 0:
            self.lineEdit_element_size.setText(str(self.new_element_size))
        else:
            self.print_error_message("element size", 'New element size')
            return False
        if self.new_geometry_tolerance > 0:
            self.lineEdit_geometry_tolerance.setText(str(self.new_geometry_tolerance))
        else:
            self.print_error_message("geometry tolerance", 'Mesh tolerance')
            return False
        return True

    def check_element_size_input_value(self):
        self.new_element_size = 0
        try:
            self.new_element_size = float(self.lineEdit_element_size.text())
        except Exception as error:
            self.print_error_message("element size", 'New element size')
            return True
        return False

    def check_geometry_tolerance_input_value(self):
        self.new_geometry_tolerance = 0
        try:
            self.new_geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except Exception as error:
            self.print_error_message("geometry tolerance", 'Mesh tolerance')
            return True
        return False

    def print_warning_same_geometry_selected(self):
        window_title = "WARNING"
        message_title = "Error in the geometry file selection"
        message = "The same geometry file has been selected inside the project's directory. Please, "
        message += "you should to select a different geometry file to update the current model setup."
        PrintMessageInput([message_title, message, window_title])

    def print_error_message(self, label_1, label_2):
        window_title = "ERROR"
        message_title = f"Invalid {label_1}"
        message = f"Please, inform a valid {label_1} at '{label_2}' input field to continue."
        message += "The input value should be a float or an integer number greater than zero."
        PrintMessageInput([message_title, message, window_title])

    def copy_geometry_file_to_project_folder(self):
        self.new_geometry_path = get_new_path(self.current_project_file_path, self.geometry_filename)
        if not os.path.samefile(self.lineEdit_new_geometry_file_path.text(), self.lineEdit_current_geometry_file_path.text()):
            if not os.path.samefile(os.path.dirname(self.lineEdit_new_geometry_file_path.text()), os.path.dirname(self.lineEdit_current_geometry_file_path.text())):
                copyfile(self.selected_geometry_path, self.new_geometry_path)
                return False
        else:
            return True
    
    def remove_other_files(self):
        list_filenames = os.listdir(self.current_project_file_path).copy()
        for filename in list_filenames:
            if filename not in ["entity.dat", "fluidList.dat", "materialList.dat", "project.ini", self.geometry_filename]:
                file_path = get_new_path(self.current_project_file_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

    def update_project_settings(self):
        project_ini_file_path = get_new_path(self.current_project_file_path, self.project_ini)
        config = configparser.ConfigParser()
        config.read(project_ini_file_path)

        config['PROJECT']['geometry file'] = self.geometry_filename
        config['PROJECT']['element size'] = str(self.new_element_size)
        config['PROJECT']['geometry tolerance'] = str(self.new_geometry_tolerance)

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
   
        # if self.createProject():
        #     self.create = True
        #     self.close()

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

    # def createProject(self):

    #     if "\\" in self.project_directory:
    #         self.project_folder_path = '{}\\{}'.format(self.project_directory, self.line_project_name.text())
    #     elif "/" in self.project_directory:
    #         self.project_folder_path = '{}/{}'.format(self.project_directory, self.line_project_name.text())

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
    #         self.config.writeRecentProject(self.line_project_name.text(), self.project_file_path)
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
    #         self.config.writeRecentProject(self.line_project_name.text(), self.project_file_path)
    #         self.project.new_project(self.project_folder_path, self.line_project_name.text(), element_size, import_type, self.material_list_path, self.fluid_list_path, conn_path=new_conn_path, coord_path=new_cord_path)
    #         return True
    #     return False

    # def createProjectFile(self):

    #     if "\\" in self.project_directory:
    #         self.project_file_path = '{}\\{}'.format(self.project_folder_path, self.projectFileName)
    #     elif "/" in self.project_directory:
    #         self.project_file_path = '{}/{}'.format(self.project_folder_path, self.projectFileName)

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
        
    #     with open(self.project_file_path, 'w') as config_file:
    #         config.write(config_file)