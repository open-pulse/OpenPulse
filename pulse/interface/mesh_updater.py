from time import time

from pulse.utils import get_new_path
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput

window_title_1 = "Error"
window_title_2 = "Warning"

class MeshUpdater:
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_window = main_window
        self.input_widget = main_window.getInputWidget()
        self.project = self.input_widget.project
        self.preprocessor = self.input_widget.project.preprocessor
        self.opv = self.input_widget.opv

        self.remesh_to_match_bcs = False
        self.cache_dict_nodes = self.preprocessor.dict_coordinate_to_update_bc_after_remesh.copy()
        self.cache_dict_update_entity_file = self.preprocessor.dict_element_info_to_update_indexes_in_entity_file.copy() 
        self.cache_dict_update_element_info_file = self.preprocessor.dict_element_info_to_update_indexes_in_element_info_file.copy() 
        self.dict_list_elements_to_subgroups = self.preprocessor.dict_list_elements_to_subgroups.copy()
        
        # self.userPath = os.path.expanduser('~')
        # self.project_directory = os.path.dirname(self.project_file_path)
        # self.project_name = self.project.file._project_name
        # self.project_file_path = self.project.file._project_path
        # self.project_ini = self.project.file._project_base_name      
        self._reset_variables()

    def _reset_variables(self):
        self.element_size = 0.01
        self.geometry_tolerance = 1e-6
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

    def set_project_attributes(self, element_size, geometry_tolerance):
        self.element_size = element_size
        self.geometry_tolerance = geometry_tolerance
            
    def process_mesh_and_load_project(self):

        if self.project.empty_geometry:
            self.process_intermediate_actions(undo_remesh=False, mapping=False) 
            self.complete = True
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

    def process_intermediate_actions(self):
        self.current_element_size, self.current_geometry_tolerance = self.project.file.get_mesh_attributes_from_project_file()
        self.t0 = time()
        self.project.file.update_project_attributes(element_size=self.element_size, geometry_tolerance=self.geometry_tolerance)
        self.project.initial_load_project_actions(self.project.file.project_ini_file_path )
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
        self.project.file.update_project_attributes(element_size=self.current_element_size, geometry_tolerance=self.current_geometry_tolerance)
        self.project.initial_load_project_actions(self.project.file.project_ini_file_path )
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