from pulse import app

from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.file.project_files_loader import ProjectFilesLoader
from pulse.tools.utils import *

from pulse.model.cross_section import CrossSection

from time import time
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class LoadProject:
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties
        self.preprocessor = app().project.preprocessor

        self.files_loader = ProjectFilesLoader()

        self._initialize()
        
    def _initialize(self):
        self.bc_loader = None

    def load_project_data(self):
        self.load_mesh_setup_from_file()
        self.load_pipeline_file()
        self.load_imported_table_data_from_file()
        #
        self.load_fluid_library()
        self.load_material_library()
        self.load_model_properties()
        self.load_lines_properties()
        #
        self.load_analysis_file()
        self.load_inertia_load_setup()
        self.load_psd_data_from_file()

    # def load_material_data(self):
    #     try:

    #         # Material to the entities
    #         for key, mat in self.files_loader.material_data.items():
    #             self.project.load_material_by_line(key, mat)

    #     except Exception as log_error:
    #         title = "Error while loading material data"
    #         message = "Local: 'LoadProjectData' class\n\n"
    #         message += str(log_error)
    #         PrintMessageInput([window_title_1, title, message])

    # def load_fluid_data(self):
    #     try:

    #         # Fluid to the entities
    #         for key, fld in self.files_loader.fluid_data.items():
    #             self.project.load_fluid_by_line(key, fld)

    #     except Exception as log_error:
    #         title = "Error while loading fluid data"
    #         message = "Local: 'LoadProjectData' class\n\n"
    #         message += str(log_error)
    #         PrintMessageInput([window_title_1, title, message])

    def load_constant_section_data(self):
        try:

            # Constant cross-section to the entities
            self.number_sections_by_line = dict()
            for key, section_data in self.files_loader.cross_section_data.items():

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

                    if key not in self.files_loader.variable_sections_data.keys():

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
            for key, value in self.files_loader.variable_sections_data.items():
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
            for key, etype_data in self.files_loader.structural_element_type_data.items():
                if self.files_loader.element_type_is_structural:
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
            for key, force_offset_data in self.files_loader.structural_element_force_offset_data.items():
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
            for key, wall_formulation_data in self.files_loader.structural_element_wall_formulation_data.items():
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

    def load_acoustic_element_length_correction_data(self):
        try:

            for key, value in self.files_loader.element_length_correction_data.items():
                self.project.load_length_correction_by_elements(value[0], value[1], key)
   
        except Exception as log_error:
            title = "Error while loading acoustic element length correction data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_perforated_plate_by_elements_data(self):
        try:

            for key, value in self.files_loader.perforated_plate_data.items():
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
            for key, _info in self.files_loader.compressor_info.items():
                self.project.load_compressor_info_by_line(key, _info)

        except Exception as log_error:
            title = "Error while loading compressor data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_xaxis_beam_rotation_data(self):
        try:

            # Beam X-axis rotation to the entities
            for key, angle in self.files_loader.beam_xaxis_rotation_data.items():
                self.project.load_beam_xaxis_rotation_by_line(key, angle)
            if len(self.files_loader.beam_xaxis_rotation_data) > 0:
                self.preprocessor.process_all_rotation_matrices() 

        except Exception as log_error:
            title = "Error while loading x-axis beam rotation data"
            message = "Local: 'LoadProjectData' class\n\n"
            message += str(log_error)
            PrintMessageInput([window_title_1, title, message])

    def load_b2px_rotation_decoupling_data(self):
        try:

            # B2PX Rotation Decoupling
            for key, item in self.files_loader.B2XP_rotation_decoupling_data.items():
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
            for key, joint_data in self.files_loader.expansion_joint_parameters_data.items():
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
            for key, [valve_data, cross_sections] in self.files_loader.valve_data.items():
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
            for key, group in self.files_loader.capped_end_data.items():
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
            for key, parameters in self.files_loader.stress_stiffening_data.items():
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

            self.files_loader.load_project_data_from_files()

            # self.load_material_data()
            # self.load_fluid_data()
            self.load_constant_section_data()
            self.load_variable_section_data()
            self.load_structural_element_type_data()
            self.load_structural_element_force_offset_data()
            self.load_structural_element_wall_formulation_data()
            # self.load_acoustic_element_type_data()
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

    def load_fluid_library(self):

        self.library_fluids = dict()
        config = app().pulse_file.read_fluid_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            keys = section.keys()

            name = section['name']
            density =  float(section['density'])
            speed_of_sound =  float(section['speed of sound'])
            identifier =  int(section['identifier'])
            color =  get_color_rgb(section['color'])

            if len(color) == 4:
                color = color[:3]

            if 'isentropic exponent' in keys:
                isentropic_exponent = float(section['isentropic exponent'])
            else:
                isentropic_exponent = ""

            if 'thermal conductivity' in keys:
                thermal_conductivity = float(section['thermal conductivity'])
            else:
                thermal_conductivity = ""

            if 'specific heat Cp' in keys:
                specific_heat_Cp = float(section['specific heat Cp'])
            else:
                specific_heat_Cp = ""

            if 'dynamic viscosity' in keys:
                dynamic_viscosity = float(section['dynamic viscosity'])
            else:
                dynamic_viscosity = ""
            
            if 'temperature' in keys:
                temperature = float(section['temperature'])
            else:
                temperature = None

            if 'pressure' in keys:
                pressure = float(section['pressure'])
            else:
                pressure = None

            # if 'key mixture' in keys:
            #     key_mixture = section['key mixture']
            # else:
            #     key_mixture = None

            # if 'molar fractions' in keys:
            #     str_molar_fractions = section['molar fractions']
            #     molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
            # else:
            #     molar_fractions = None

            if 'molar mass' in keys:
                if section['molar mass'] == "None":
                    molar_mass = None
                else:
                    molar_mass = float(section['molar mass'])
            else:
                molar_mass = None

            fluid = Fluid(  name = name,
                            density = density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure,
                            molar_mass = molar_mass  )
            
            self.library_fluids[identifier] = fluid

    def load_material_library(self):

        self.library_materials = dict()
        config = app().pulse_file.read_material_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            # keys = section.keys()

            name = section['name']
            identifier = int(section['identifier'])
            density = float(section['density'])
            poisson_ratio = float(section['poisson ratio'])
            elasticity_modulus = float(section['elasticity modulus']) * 1e9
            thermal_expansion_coefficient = float(section['thermal expansion coefficient'])
            color =  get_color_rgb(section['color'])

            if len(color) == 4:
                color = color[:3]

            material = Material(
                                name = name,
                                identifier = identifier, 
                                density = density,
                                poisson_ratio = poisson_ratio,
                                elasticity_modulus = elasticity_modulus,
                                thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                color = color
                                )
            
            self.library_materials[identifier] = material

    def load_model_properties(self):

        model_properties = self.files_loader.load_model_properties_from_file()

        for key, data in model_properties.items():
            if isinstance(data, dict):
                for (property, id), prop_data in data.items():

                    if key == "nodal_properties":
                        self.properties._set_nodal_property(property, prop_data, node_ids=id)

                    elif key == "element_properties":
                        self.properties._set_element_property(property, prop_data, element=id)

    def load_lines_properties(self):

        line_properties = app().pulse_file.read_line_properties_from_file()
        if line_properties is None:
            return

        for line_id, data in line_properties.items():

            if isinstance(data, dict):
                for property, prop_data in data.items():

                    if property == "fluid":
                        fluid_id = prop_data
                        if fluid_id not in self.library_fluids.keys():
                            continue

                        prop_data = self.library_fluids[fluid_id]

                    elif property == "material":
                        material_id = prop_data
                        if material_id not in self.library_materials.keys():
                            continue

                        prop_data = self.library_materials[material_id]

                    self.properties._set_line_property(property, prop_data, line_ids=int(line_id))

        print(line_properties)
        if line_properties:
            self.send_lines_properties_to_elements()

    def send_lines_properties_to_elements(self):
        for line_id, data in self.properties.line_properties.items():
            # acoustic
            self.load_fluid_from_lines(line_id, data)
            self.load_acoustic_element_type_from_lines(line_id, data)
            # structural
            self.load_material_from_lines(line_id, data)

    def load_imported_table_data_from_file(self):
        imported_tables = self.files_loader.load_imported_table_data_from_file()
        if "acoustic" in imported_tables.keys():
            app().project.model.properties.acoustic_imported_tables = imported_tables["acoustic"]
        elif "structural" in imported_tables.keys():
            app().project.model.properties.structural_imported_tables = imported_tables["structural"]

    def load_mesh_setup_from_file(self):

        project_setup = app().pulse_file.read_project_setup_from_file()
        if project_setup is None:
            return

        if "mesher setup" in project_setup.keys():
            self.preprocessor.mesh.set_mesher_setup(mesh_setup=project_setup["mesher setup"])

    def load_inertia_load_setup(self):

        inertia_load = app().pulse_file.read_inertia_load_from_file()
        if inertia_load is None:
            return

        gravity = np.array(inertia_load["gravity"], dtype=float)
        stiffening_effect = inertia_load["stiffening effect"]

        self.project.model.set_gravity_vector(gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)

    def load_analysis_file(self):

        analysis_setup = self.files_loader.load_analysis_file()

        if analysis_setup is None:
            return

        self.model.set_frequency_setup(analysis_setup)
        self.model.set_global_damping(analysis_setup)

    def load_psd_data_from_file(self):

        psd_data = app().pulse_file.read_psd_data_from_file()
        if psd_data is None:
            return
        
        self.model.set_psd_data(psd_data)

        link_data = defaultdict(list)

        for psd_label, data in psd_data.items():
            for key, value in data.items():

                if "Link-" in key:
                    link_type = value["link type"]
                    start_coords = value["start coords"]
                    end_coords = value["end coords"]
                    link_data[(psd_label, link_type)].append((start_coords, end_coords))

        if link_data:
            self.add_psd_link_data_to_nodes(link_data)

    def add_psd_link_data_to_nodes(self, link_data: dict):

        for key, values in link_data.items():
            for (start_coords, end_coords) in values:

                id_1 = self.preprocessor.get_node_id_by_coordinates(start_coords)
                id_2 = self.preprocessor.get_node_id_by_coordinates(end_coords)
                nodes = (id_1, id_2)

                if key[1] == "acoustic_link":
                    property = "psd_acoustic_link"
                    node_ids, data = self.preprocessor.get_acoustic_link_data(nodes)
                else:
                    property = "psd_structural_link"
                    node_ids, data = self.preprocessor.get_structural_link_data(nodes)

                self.model.properties._set_nodal_property(property, data, node_ids=node_ids)

    def get_device_related_lines(self):

        psd_lines = defaultdict(list)
        config = app().pulse_file.read_pipeline_data_from_file()

        for section in config.sections():
            if "psd label" in config[section].keys():
                psd_label = config[section]["psd label"]
                psd_lines[psd_label].append(int(section))

        return psd_lines

    ## line loaders

    def load_fluid_from_lines(self, line_id: int, data: dict):

        fluid = None
        if "fluid" in data.keys():
            fluid = data["fluid"]

        self.preprocessor.set_fluid_by_lines(line_id, fluid)

    def load_acoustic_element_type_from_lines(self, line_id: int, data: dict):

        element_type = None
        if "acoustic_element_type" in data.keys():
            element_type = data["acoustic_element_type"]

        proportional_damping = None
        if "proportional_damping" in data.keys():
            proportional_damping = data["proportional_damping"]

        volume_flow = None
        if "volume_flow" in data.keys():
            volume_flow = data["volume_flow"]

        self.preprocessor.set_acoustic_element_type_by_lines(   
                                                                line_id, 
                                                                element_type, 
                                                                proportional_damping = proportional_damping,
                                                                vol_flow = volume_flow    
                                                             )
        
    def load_material_from_lines(self, line_id: int, data: dict):

        material = None
        if "material" in data.keys():
            material = data["material"]

        self.preprocessor.set_material_by_lines(line_id, material)