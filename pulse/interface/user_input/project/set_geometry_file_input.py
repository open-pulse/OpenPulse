from PyQt5.QtWidgets import QDialog, QFileDialog, QLineEdit, QToolButton, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from shutil import copyfile
import numpy as np

from pulse import UI_DIR
from pulse.tools.utils import get_new_path
from pulse.project.project import Project
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput

window_title_1 = "Error"
window_title_2 = "Warning"

class SetGeometryFileInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(UI_DIR / "project/set_geometry_file.ui", self)

        self.project = project
        self.opv = opv

        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.load_icon()
        self.reset_variables()
        self.define_qt_variables()
        self.create_connections()
        self.load_project_info()
        self.exec()

    def load_icon(self):
        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

    def reset_variables(self):
        self.material_list_path = ""
        self.fluid_list_path = ""
        self.selected_geometry_path = ""
        self.geometry_path = self.project.file.geometry_path

        self.userPath = os.path.expanduser('~')
        self.current_project_file_path = self.project.file.project_path
        self.project_directory = os.path.dirname(self.current_project_file_path)
        self.project_name = self.project.file._project_name
        self.element_size = self.project.file._element_size
        self.geometry_tolerance = self.project.file._geometry_tolerance
        self.project_ini = self.project.file._project_base_name

        self.current_geometry_path = self.project.file._geometry_path
        self.current_material_list_path = self.project.file._material_list_path
        self.current_fluid_list_path = self.project.file._fluid_list_path

        self.import_type = self.project.file._import_type

        self.materialListName = self.project.file._material_file_name
        self.fluidListName = self.project.file._fluid_file_name
        self.project_file_name = self.project.file._project_base_name


    def define_qt_variables(self):
        # QLineEdit
        self.lineEdit_current_geometry_file_path = self.findChild(QLineEdit, 'lineEdit_current_geometry_file_path')
        self.lineEdit_element_size = self.findChild(QLineEdit, 'lineEdit_element_size')        
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_new_geometry_file_path = self.findChild(QLineEdit, 'lineEdit_new_geometry_file_path')

        # QPushButton
        self.pushButton_confirm = self.findChild(QPushButton, 'pushButton_confirm')
        self.pushButton_cancel = self.findChild(QPushButton, 'pushButton_cancel')

        # QToolButton
        self.toolButton_search_new_geometry_file = self.findChild(QToolButton, 'toolButton_search_new_geometry_file')

    def create_connections(self):
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_confirm.clicked.connect(self.confirm_and_update_model)
        self.toolButton_search_new_geometry_file.clicked.connect(self.search_new_geometry_file)

    def load_project_info(self):        
        self.lineEdit_current_geometry_file_path.setText(str(self.geometry_path))
        self.lineEdit_element_size.setText(str(self.element_size))
        self.lineEdit_geometry_tolerance.setText(str(self.geometry_tolerance))

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
            if self.selected_geometry_path == "":
                return

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
        self.selected_geometry_path, _type = QFileDialog.getOpenFileName(None, 'Choose a valid geometry file', self.userPath, 'Files (*.iges; *.igs; *.step; *.stp)')        
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
        message_title = "Error in the geometry file selection"
        message = "The same geometry file has been selected inside the project's directory. Please, "
        message += "you should to select a different geometry file to update the current model setup."
        PrintMessageInput([message_title, message, window_title_2])

    def print_error_message(self, label_1, label_2):
        message_title = f"Invalid {label_1}"
        message = f"Please, inform a valid {label_1} at '{label_2}' input field to continue."
        message += "The input value should be a float or an integer number greater than zero."
        PrintMessageInput([message_title, message, window_title_1])

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
        files_to_maintain = self.project.file.get_list_filenames_to_maintain_after_reset
        for filename in list_filenames:
            if filename not in files_to_maintain:
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