from PyQt5.QtWidgets import QLineEdit, QDialog, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
import os
import configparser
from time import time

from pulse.utils import get_new_path
from data.user_input.project.printMessageInput import PrintMessageInput
from data.user_input.project.callDoubleConfirmationInput import CallDoubleConfirmationInput

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

class SetMeshPropertiesInput(QDialog):
    def __init__(self, project, opv, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('data/user_input/ui/Project/setMeshPropertiesInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'add.png')
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
  
        # self.config = config
        self.complete = False
        self.create = False
        self.stop = False

        self.currentTab = 0
        self.t0 = 0

        self.userPath = os.path.expanduser('~')
        self.project_file_path = self.project.file._project_path
        self.project_directory = os.path.dirname(self.project_file_path)
        self.project_name = self.project.file._project_name
        self.project_ini = self.project.file._project_base_name
        self.project_ini_file_path = get_new_path(self.project_file_path, self.project_ini)
        geometry_tolerance = self.project.file._geometry_tolerance
        
        self.lineEdit_current_element_size = self.findChild(QLineEdit, 'lineEdit_current_element_size')
        self.lineEdit_new_element_size = self.findChild(QLineEdit, 'lineEdit_new_element_size')
        self.lineEdit_geometry_tolerance = self.findChild(QLineEdit, 'lineEdit_geometry_tolerance')
        self.lineEdit_geometry_tolerance.setText(str(geometry_tolerance))
        self.lineEdit_current_element_size.setDisabled(True)
        self.lineEdit_new_element_size.setDisabled(False)
        self.lineEdit_geometry_tolerance.setDisabled(False)

        if self.project.file.element_size is not None:
            self.lineEdit_current_element_size.setText(str(self.project.file.element_size))
            self.current_element_size = self.project.file.element_size
 
        self.pushButton_confirm_and_generate_mesh = self.findChild(QPushButton, 'pushButton_confirm_and_generate_mesh')
        self.pushButton_confirm_and_generate_mesh.clicked.connect(self.confirm_and_generate_mesh)

        self.exec_()

    def update_project_attributes(self, undo_remesh=False):
        project_ini_file_path = get_new_path(self.project_file_path, self.project_ini)
        config = configparser.ConfigParser()
        config.read(project_ini_file_path)
        if undo_remesh:
            config['PROJECT']['element size'] = str(self.current_element_size)
        else:
            config['PROJECT']['element size'] = str(self.new_element_size)
        config['PROJECT']['Geometry tolerance'] = str(self.geometry_tolerance)
        with open(project_ini_file_path, 'w') as config_file:
            config.write(config_file)

    def confirm_and_generate_mesh(self):
        
        if self.check_element_size_input_value():
            return
        if self.check_geometry_tolerance_input_value():
            return

        if self.new_element_size > 0:
            if self.lineEdit_current_element_size.text() == self.lineEdit_new_element_size.text():
                title = "Same element size"
                message = "Please, you should to insert a different value at the "
                message += "'New element size' input field to update the model."
                PrintMessageInput([title, message, window_title_1])
                return
        else:
            self.print_error_message("element size", 'New element size')

        if self.geometry_tolerance > 0:
            pass
        else:
            self.print_error_message("geometry tolerance", 'Mesh tolerance') 
        self.process_intermediate_actions()


        if len(self.dict_non_mapped_bcs) > 0:
            title = "Error while mapping boundary conditions"
            message = "The boundary conditions associated to the following nodal coordinates cannot be mapped directly after remesh:\n\n"
            for coord in list(self.dict_non_mapped_bcs.keys()):
                message += f"{coord};\n"
            message = message[:-2]
            message += ".\n\nPress the Return button if you want to change the element size and process remapping once, press the"
            message += "Remove button to remove unmapped boundary conditions or press Close button to abort the mesh operation."
            read = CallDoubleConfirmationInput(title, message, leftButton_label = 'Remove', rightButton_label = 'Return')
            
            if read._doNotRun:
                self.process_intermediate_actions(undo_remesh=True, mapping=False) 
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
                self.process_intermediate_actions(undo_remesh=True, mapping=False)
                return
        else:
            self.process_final_actions()
        self.project.time_to_load_or_create_project = time() - self.t0
        self.close()

    def process_intermediate_actions(self, undo_remesh=False, mapping=True):
        self.t0 = time()
        self.update_project_attributes(undo_remesh=undo_remesh)
        self.project.initial_load_project_actions(self.project_ini_file_path)
        if mapping:
            #
            [self.dict_old_to_new_node_external_indexes, self.dict_non_mapped_bcs] = self.preprocessor.update_node_ids_after_remesh(self.cache_dict_nodes)  
            #
            self.dict_group_elements_to_update_entity_file, self.dict_non_mapped_subgroups_entity_file = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_entity_file)
            self.dict_group_elements_to_update_element_info_file, self.dict_non_mapped_subgroups_info_file = self.preprocessor.update_element_ids_after_remesh(self.cache_dict_update_element_info_file)

        if undo_remesh:
            self.project.load_project_files()     
            self.opv.opvRenderer.plot()
            self.opv.changePlotToMesh() 

    def process_final_actions(self):
        self.project.update_node_ids_in_file_after_remesh(self.dict_old_to_new_node_external_indexes)
        self.project.update_element_ids_in_entity_file_after_remesh(self.dict_group_elements_to_update_entity_file,
                                                                    self.dict_non_mapped_subgroups_entity_file)
        self.project.update_element_ids_in_element_info_file_after_remesh(  self.dict_group_elements_to_update_element_info_file,
                                                                            self.dict_non_mapped_subgroups_info_file,
                                                                            self.dict_list_elements_to_subgroups    )
        self.project.load_project_files()     
        self.opv.opvRenderer.plot()
        self.opv.opvAnalisysRenderer.plot()
        self.opv.changePlotToMesh()   
        self.complete = True

    def check_element_size_input_value(self):
        self.new_element_size = 0
        try:
            self.new_element_size = float(self.lineEdit_new_element_size.text())
        except Exception as error:
            self.print_error_message("element size", 'New element size')
            return True
        return False

    def check_geometry_tolerance_input_value(self):
        self.geometry_tolerance = 0
        try:
            self.geometry_tolerance = float(self.lineEdit_geometry_tolerance.text())
        except Exception as error:
            self.print_error_message("geometry tolerance", 'Mesh tolerance')
            return True
        return False

    def print_error_message(self, label_1, label_2):
        window_title = "ERROR"
        message_title = f"Invalid {label_1}"
        message = f"Please, inform a valid {label_1} at '{label_2}' input field to continue."
        message += "The input value should be a float or an integer number greater than zero."
        PrintMessageInput([message_title, message, window_title])