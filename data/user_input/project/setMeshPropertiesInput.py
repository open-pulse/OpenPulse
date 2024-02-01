from PyQt5.QtWidgets import QDialog, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5 import uic
from pathlib import Path

import os
import configparser
from time import time

from pulse.utils import get_new_path
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.call_double_confirmation_input import CallDoubleConfirmationInput

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class SetMeshPropertiesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)

        uic.loadUi(Path('data/user_input/ui_files/Project/setMeshPropertiesInput.ui'), self)

        icons_path = str(Path('data/icons/pulse.png'))
        self.icon = QIcon(icons_path)
        self.setWindowIcon(self.icon)

        self.project = project
        self.preprocessor = project.preprocessor
        self.opv = opv

        self.opv.setInputObject(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.WindowModal)

        self.remesh_to_match_bcs = False
        self.cache_dict_nodes = self.preprocessor.dict_coordinate_to_update_bc_after_remesh.copy()
        self.cache_dict_update_entity_file = self.preprocessor.dict_element_info_to_update_indexes_in_entity_file.copy() 
        self.cache_dict_update_element_info_file = self.preprocessor.dict_element_info_to_update_indexes_in_element_info_file.copy() 
        self.dict_list_elements_to_subgroups = self.preprocessor.dict_list_elements_to_subgroups.copy()
        # print(self.cache_dict_nodes)
        # print(self.cache_dict_update_entity_file)
  
        # self.userPath = os.path.expanduser('~')
        # self.project_directory = os.path.dirname(self.project_file_path)
        # self.project_name = self.project.file._project_name
        # self.project_file_path = self.project.file._project_path
        # self.project_ini = self.project.file._project_base_name
        self.project_ini_file_path = get_new_path(self.project.file._project_path, self.project.file._project_base_name)

        self._reset_variables()
        self._define_Qt_variables()
        self._create_actions()
        self.check_geometry_and_mesh_before()
        self.exec()

    def _define_Qt_variables(self):
        self.label_new_element_size = self.findChild(QLabel, 'label_new_element_size')
        self.label_current_element_size = self.findChild(QLabel, 'label_current_element_size')
        self.label_geometry_tolerance = self.findChild(QLabel, 'label_geometry_tolerance')
        self.lineEdit_current_element_size = self.findChild(QLineEdit, 'lineEdit_current_element_size')
        self.lineEdit_new_element_size = self.findChild(QLineEdit, 'lineEdit_new_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.pushButton_confirm_and_generate_mesh = self.findChild(QPushButton, 'pushButton_confirm_and_generate_mesh')
        self.frame_current_element_size = self.findChild(QFrame, 'frame_current_element_size')
        self.lineEdit_current_element_size.setDisabled(True)
        self.lineEdit_new_element_size.setDisabled(False)
        self.lineEdit_geometry_tolerance.setDisabled(False)
        if self.project.file.element_size is not None:
            self.lineEdit_current_element_size.setText(str(self.project.file.element_size))
            self.current_element_size = self.project.file.element_size
        if self.project.file._geometry_tolerance is not None:
            self.lineEdit_geometry_tolerance.setText(str(self.project.file._geometry_tolerance))
    
    def _create_actions(self):
        self.pushButton_confirm_and_generate_mesh.clicked.connect(self.confirm_and_generate_mesh)

    def _reset_variables(self):
        self.dict_old_to_new_node_external_indexes = {}
        self.dict_non_mapped_bcs = {}
        self.dict_group_elements_to_update_entity_file = {}
        self.dict_group_elements_to_update_element_info_file = {}
        self.dict_non_mapped_subgroups_entity_file = {}
        self.dict_non_mapped_subgroups_info_file = {}
        self.dict_list_elements_to_subgroups = {}
        # self.config = config
        self.complete = False
        self.create = False
        self.stop = False
        self.t0 = 0

    def check_geometry_and_mesh_before(self):
        if self.project.empty_geometry or len(self.project.preprocessor.structural_elements) == 0:
                y, dy = 75, 55
                self.lineEdit_current_element_size.setText("")
                self.frame_current_element_size.setVisible(False)
                self.label_new_element_size.setText("Element size:")
                self.label_new_element_size.setGeometry(QRect(42, y, 150, 25))
                self.label_geometry_tolerance.setGeometry(QRect(42, y+dy, 150, 25))
                self.lineEdit_new_element_size.setGeometry(QRect(200, y, 100, 25))
                self.lineEdit_geometry_tolerance.setGeometry(QRect(200, y+dy, 100, 25))
                self.pushButton_confirm_and_generate_mesh.setText("Confirm mesh setup")
                self.pushButton_confirm_and_generate_mesh.setMinimumSize(QSize(250, 32))
                self.pushButton_confirm_and_generate_mesh.setMaximumSize(QSize(250, 32))
                self.pushButton_confirm_and_generate_mesh.setGeometry(QRect(50,y+2*dy,250,30))
            
    def confirm_and_generate_mesh(self):
        
        if self.check_element_size_input_value():
            self.lineEdit_new_element_size.setFocus()
            return
        
        if self.check_geometry_tolerance_input_value():
            self.lineEdit_geometry_tolerance.setFocus()
            return
         
        if self.lineEdit_current_element_size.text() == self.lineEdit_new_element_size.text():
            title = "Same element size"
            message = "Please, you should to insert a different value at the "
            message += "'New element size' input field to update the model."
            PrintMessageInput([title, message, window_title_1])
            return

        if self.new_element_size <= 1e-5:
            title = "Too small element size"
            message = f"The attributed element size can be small enough to lead to rounding errors. \n"
            message += "It is recommended to consider this information while checking the model results."
            PrintMessageInput([title, message, window_title_2])
    
        if self.geometry_tolerance >= 1e-3:
            title = "Too big geometry tolerance"
            message = f"The attributed geometry tolerance can be big enough to lead to rounding errors in geometry construction. "
            message += "As a suggestion, we recommend reducing the geometry tolerance to values less or equal to 1e-6."
            PrintMessageInput([title, message, window_title_2])
            return

        if self.project.empty_geometry:
            self.process_intermediate_actions(undo_remesh=False, mapping=False) 
            self.complete = True
            self.close()
            return
        else:
            self.process_intermediate_actions()

        if len(self.dict_non_mapped_bcs) > 0:
            title = "Error while mapping boundary conditions"
            message = "The boundary conditions associated to the following nodal coordinates cannot be mapped directly after remesh:\n\n"
            for coord in list(self.dict_non_mapped_bcs.keys()):
                message += f"{coord};\n"
            message = message[:-2]
            message += ".\n\nPress the Return button if you want to change the element size and process remapping once, press the "
            message += "Remove button to remove unmapped boundary conditions or press Close button to abort the mesh operation."
            buttons_config = {"left_button_label" : "Remove", "right_button_label" : "Return"}
            read = CallDoubleConfirmationInput(title, message, buttons_config=buttons_config)
            
            if read._doNotRun:
                self.undo_mesh_actions()
                # self.process_intermediate_actions(undo_remesh=True, mapping=False) 
            elif read._stop:
                self.process_final_actions()
                title = "Removal of unmapped boundary conditions"
                message = "The boundary conditions associated to the following nodal coordinates "
                message += "has been removed from the current model setup:\n\n"
                for coord in list(self.dict_non_mapped_bcs.keys()):
                    message += f"{coord};\n"
                message = message[:-2] 
                message += ".\n\nPlease, take this information into account henceforward."
                PrintMessageInput([title, message, window_title_2])
            elif read._continue:
                self.undo_mesh_actions()
                # self.process_intermediate_actions(undo_remesh=True, mapping=False)
                return
        else:
            self.process_final_actions()
        self.project.time_to_load_or_create_project = time() - self.t0
        self.close()

    def process_intermediate_actions(self):
        self.t0 = time()
        self.project.file.update_project_attributes(element_size=self.new_element_size, geometry_tolerance=self.geometry_tolerance)
        self.project.initial_load_project_actions(self.project_ini_file_path)
        if len(self.preprocessor.structural_elements) > 0:
            #
            data_1 = self.preprocessor.update_node_ids_after_remesh(self.cache_dict_nodes)
            data_2 = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_entity_file)
            data_3 = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_element_info_file)
            #
            [self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs] = data_1
            [self.dict_group_elements_to_update_entity_file, self.dict_non_mapped_subgroups_entity_file] = data_2
            [self.dict_group_elements_to_update_element_info_file, self.dict_non_mapped_subgroups_info_file] = data_3

    def undo_mesh_actions(self):
        self.t0 = time()
        self.project.file.update_project_attributes(element_size=self.current_element_size, geometry_tolerance=self.geometry_tolerance)
        self.project.initial_load_project_actions(self.project_ini_file_path)
        self.project.load_project_files()     
        self.opv.updatePlots()
        self.opv.changePlotToMesh() 

    def process_final_actions(self):
        if len(self.dict_old_to_new_node_external_indexes) > 0:
            self.project.update_node_ids_in_file_after_remesh(self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs)
        
        if (len(self.dict_group_elements_to_update_entity_file) + len(self.dict_non_mapped_subgroups_entity_file)) > 0:
            self.project.update_element_ids_in_entity_file_after_remesh(self.dict_group_elements_to_update_entity_file,
                                                                        self.dict_non_mapped_subgroups_entity_file)

        if len(self.dict_non_mapped_subgroups_entity_file) > 0:
            title = "Non mapped elements"
            message = "There are elements that have not been mapped after the meshing process. Therefore, the line "
            message += "attributes will be reset to prevent errors decurrent of element lack attribution.\n\n"
            for list_elements in self.dict_non_mapped_subgroups_entity_file.values():
                if len(list_elements) > 10:
                    message += f"{str(list_elements[0:3])[:-1]}...{str(list_elements[-3:])[1:]}\n"
            PrintMessageInput([title, message, window_title_2])

        if len(self.dict_group_elements_to_update_element_info_file) > 0:
            self.project.update_element_ids_in_element_info_file_after_remesh(  self.dict_group_elements_to_update_element_info_file,
                                                                                self.dict_non_mapped_subgroups_info_file,
                                                                                self.dict_list_elements_to_subgroups    )
        self.project.load_project_files()     
        self.opv.updatePlots()
        self.opv.changePlotToMesh()   
        self.complete = True

    def check_element_size_input_value(self):

        title = "Invalid element size input"
        message = f"Please, inform a valid element size at the input field to continue. The input value should be, "
        message += "preferabley, a small positive float number. Remember that the element size units are in meters.\n\n"

        self.new_element_size = 0
        try:
            self.new_element_size = float(self.lineEdit_new_element_size.text())
            if self.new_element_size <= 0:
                PrintMessageInput([title, message, window_title_1])
                return True 
        except Exception as _error:
            message += str(_error)
            PrintMessageInput([title, message, window_title_1])
            return True
        return False

    def check_geometry_tolerance_input_value(self):
        
        title = "Invalid geometry tolerance input"
        message = f"Please, inform a valid geometry tolerance to continue. The input value"
        message += " should be a float or an integer number greater than zero.\n\n"
            
        self.geometry_tolerance = 0
        try:
            self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
            if self.geometry_tolerance <= 0:
                PrintMessageInput([title, message, window_title_1])
                return True 
        except Exception as _error:
            message += str(_error)
            PrintMessageInput([title, message, window_title_1])
            return True
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.confirm_and_generate_mesh()
        elif event.key() == Qt.Key_Escape:
            self.close()