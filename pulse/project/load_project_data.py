from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.project.load_project_file import LoadProjectFile
from pulse.tools.utils import *

from pulse.preprocessing.cross_section import CrossSection


from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class LoadProjectData:
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.file = app().file

        self._initialize()
        
    def _initialize(self):
        self.loader = LoadProjectFile()
        self.preprocessor = self.project.preprocessor

    def load_material_data(self):
        try:

            # Material to the entities
            for key, mat in self.loader.material_data.items():
                self.project.load_material_by_line(key, mat)

        except Exception as log_error:
            title = "Error while loading material data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_fluid_data(self):
        try:

            # Fluid to the entities
            for key, fld in self.loader.fluid_data.items():
                self.project.load_fluid_by_line(key, fld)

        except Exception as log_error:
            title = "Error while loading fluid data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_constant_section_data(self):
        try:

            # Constant cross-section to the entities
            self.number_sections_by_line = dict()
            for key, section_data in self.loader.cross_section_data.items():

                # key[0] -> tag : str
                # key[1] -> label ("pipe", "beam")

                if "-" in key[0]:

                    cross = CrossSection(pipe_section_info = section_data[1])
                    self.project.load_cross_section_by_element(section_data[0], cross)
 
                    prefix_key = int(key[0].split("-")[0])
                    if prefix_key in list(self.number_sections_by_line.keys()):
                        self.number_sections_by_line[prefix_key] += 1
                    else:
                        self.number_sections_by_line[prefix_key] = 1

                else:

                    if key not in self.loader.variable_sections_data.keys():

                        cross = None
                        if key[1] == "pipe":
                            cross = CrossSection(pipe_section_info = section_data)
                        
                        elif key[1] == "beam":
                            cross = CrossSection(beam_section_info = section_data)
                        
                        if cross is not None:
                            self.project.load_cross_section_by_line(int(key[0]), cross)

        except Exception as log_error:
            title = "Error while loading constant section data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_variable_section_data(self):
        try:

            # Variable Cross-section to the entities
            for key, value in self.loader.variable_sections_data.items():
                self.project.load_variable_cross_section_by_line(int(key[0]), value)

        except Exception as log_error:
            title = "Error while loading variable section data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_structural_element_type_data(self):
        try:
            # self.lines_with_cross_section_by_elements = list()
            # Load structural element type info
            for key, etype_data in self.loader.structural_element_type_data.items():
                if self.loader.element_type_is_structural:
                    if "-" in key:
                        self.project.load_structural_element_type_by_elements(etype_data[0], etype_data[1])
                    else:
                        self.project.load_structural_element_type_by_line(int(key), etype_data)

        except Exception as log_error:
            title = "Error while loading structural element type data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_structural_element_force_offset_data(self):
        try:

            # Structural element force offset to the entities
            for key, force_offset_data in self.loader.structural_element_force_offset_data.items():
                if "-" in key:
                    self.project.load_structural_element_force_offset_by_elements(force_offset_data[0], 
                                                                          force_offset_data[1])
                else:
                    line_id = int(key)
                    self.project.load_structural_element_force_offset_by_line(line_id, 
                                                                      force_offset_data)
   
        except Exception as log_error:
            title = "Error while loading structural element force offset data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_structural_element_wall_formulation_data(self):
        try:

            # Structural element wall formulation to the entities
            for key, wall_formulation_data in self.loader.structural_element_wall_formulation_data.items():
                if "-" in key:
                    self.project.load_structural_element_wall_formulation_by_elements(wall_formulation_data[0], 
                                                                              wall_formulation_data[1])
                else:
                    line_id = int(key)
                    self.project.load_structural_element_wall_formulation_by_line(line_id, 
                                                                          wall_formulation_data)
   
        except Exception as log_error:
            title = "Error while loading structural element wall formulation data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_acoustic_element_type_data(self):
        try:

            # Acoustic element type to the entities
            for key, [el_type, proportional_damping, vol_flow] in self.loader.acoustic_element_type_data.items():
                if self.loader.element_type_is_acoustic:
                    if "-" in key:
                        continue
                    else:
                        line_id = int(key)
                        self.project.load_acoustic_element_type_by_line(line_id, 
                                                                        el_type, 
                                                                        proportional_damping = proportional_damping, 
                                                                        vol_flow = vol_flow)

        except Exception as log_error:
            title = "Error while loading acoustic element type data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_acoustic_element_length_correction_data(self):
        try:

            for key, value in self.loader.element_length_correction_data.items():
                self.project.load_length_correction_by_elements(value[0], value[1], key)
   
        except Exception as log_error:
            title = "Error while loading acoustic element length correction data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_perforated_plate_by_elements_data(self):
        try:

            for key, value in self.loader.perforated_plate_data.items():
                frequency_setup_pass = True
                table_name = value[1].dimensionless_impedance_table_name
                if table_name is not None:
                    if self.project.change_project_frequency_setup(table_name, value[2]):
                        frequency_setup_pass = False
                        break
                if frequency_setup_pass:
                    self.project.load_perforated_plate_by_elements(value[0], value[1], key)

        except Exception as log_error:
            title = "Error while loading perforated plate data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_compressor_data(self):
        try:

            # Compressor info to the entities
            for key, _info in self.loader.compressor_info.items():
                self.project.load_compressor_info_by_line(key, _info)

        except Exception as log_error:
            title = "Error while loading compressor data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_xaxis_beam_rotation_data(self):
        try:

            # Beam X-axis rotation to the entities
            for key, angle in self.loader.beam_xaxis_rotation_data.items():
                self.project.load_beam_xaxis_rotation_by_line(key, angle)
            if len(self.loader.beam_xaxis_rotation_data) > 0:
                self.preprocessor.process_all_rotation_matrices() 

        except Exception as log_error:
            title = "Error while loading x-axis beam rotation data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_b2px_rotation_decoupling_data(self):
        try:

            # B2PX Rotation Decoupling
            for key, item in self.loader.B2XP_rotation_decoupling_data.items():
                if "B2PX ROTATION DECOUPLING" in str(key):
                    self.preprocessor.dict_B2PX_rotation_decoupling[str(item[2])] = [item[0], item[1], key]
                    for i in range(len(item[0])):
                        self.project.load_B2PX_rotation_decoupling(item[0][i], item[1][i], rotations_to_decouple=item[2])

        except Exception as log_error:
            title = "Error while loading B2PX rotation data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_expansion_joint_data(self):
        try:

            # Expansion Joint to the entities
            for key, joint_data in self.loader.expansion_joint_parameters_data.items():
                frequency_setup_pass = True
                if "-" in key:
                    parameters = joint_data[1]
                    joint_tables = joint_data[1][2]
                    joint_list_freq = joint_data[1][3]
                    if joint_data[1][1] is not None:
                        for i, joint_freq in enumerate(joint_list_freq):
                            if self.project.change_project_frequency_setup(joint_tables[i], joint_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        for list_elements in joint_data[0]:
                            self.project.load_expansion_joint_by_elements(list_elements, parameters[:-1])
                else:
                    joint_table_names = joint_data[2]
                    joint_list_freq = joint_data[3]
                    if joint_data[1] is not None:
                        for i, joint_freq in enumerate(joint_list_freq):
                            if self.project.change_project_frequency_setup(joint_table_names[i], joint_freq):
                                frequency_setup_pass = False
                                break
                        if frequency_setup_pass:
                            line_id = int(key)
                            self.project.load_expansion_joint_by_lines(line_id, joint_data[:-1])

        except Exception as log_error:
            title = "Error while loading expansion joint data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_valve_data(self):
        try:

            # Valve to the entities
            for key, [valve_data, cross_sections] in self.loader.valve_data.items():
                if "-" in key:
                    self.project.load_valve_by_elements(valve_data, cross_sections)  
                else:
                    line_id = int(key)
                    self.project.load_valve_by_lines(line_id, valve_data, cross_sections)

        except Exception as log_error:
            title = "Error while loading valve data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_capped_end_data(self):
        try:

            # Capped end to the entities and elements
            for key, group in self.loader.capped_end_data.items():
                if "CAPPED END" in key:  
                    self.project.load_capped_end_by_elements(group, True, key)
                else:
                    self.project.load_capped_end_by_line(group, True)

        except Exception as log_error:
            title = "Error while loading capped end data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_stress_stiffening_data(self):
        try:

            # Stress Stiffening to the entities and elements
            for key, parameters in self.loader.stress_stiffening_data.items():
                if "STRESS STIFFENING" in str(key):
                    self.project.load_stress_stiffening_by_elements(parameters[0], parameters[1], section=key)
                else:
                    self.project.load_stress_stiffening_by_line(key, parameters)   

        except Exception as log_error:
            title = "Error while loading stress stiffening data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_pipeline_file(self):
        try:

            self.loader.load_project_data_from_files()

            self.load_material_data()
            self.load_fluid_data()
            self.load_constant_section_data()
            self.load_variable_section_data()
            self.load_structural_element_type_data()
            self.load_structural_element_force_offset_data()
            self.load_structural_element_wall_formulation_data()
            self.load_acoustic_element_type_data()
            self.load_acoustic_element_length_correction_data()
            self.load_compressor_data()
            self.load_perforated_plate_by_elements_data()
            self.load_xaxis_beam_rotation_data()
            self.load_b2px_rotation_decoupling_data()
            self.load_expansion_joint_data()
            self.load_valve_data()
            self.load_capped_end_data()
            self.load_stress_stiffening_data()

        except Exception as log_error:
            title = "Error while loading project data"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])