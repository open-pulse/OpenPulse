
from pulse import app
from pulse.model.cross_section import get_beam_section_properties
from pulse.model.node import DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.libraries.default_libraries import default_material_library, default_fluid_library
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

import os
import configparser
import json
import numpy as np
from math import pi
from pathlib import Path
from collections import defaultdict
from shutil import copyfile, rmtree

window_title = "Error"

class ProjectFile:
    def __init__(self):
        self.reset()

    def reset(self):

        self._import_type = 0
        self._section = 0
        self._length_unit = "meter"
        self._element_size = 0.01 # default value to the element size (in meters)

        self._geometry_path = ""
        self._geometry_filename = ""
        self._geometry_tolerance = 1e-6 # default value to gmsh geometry tolerance (in millimeters)
        self._pipeline_path = ""
        self._node_structural_path = ""
        self._node_acoustic_path = ""
        self._element_info_path = ""
        self._analysis_path = ""

        self.default_filenames()
        self.reset_frequency_setup()

    def reset_frequency_setup(self):
        self.f_min = None
        self.f_max = None
        self.f_step = None
        self.zero_frequency = False
        self.non_zero_frequency_info = list()

    def default_filenames(self):
        self._project_ini_name = "project.ini"
        self._fluid_file_name = "fluid_list.dat"
        self._material_file_name = "material_list.dat"
        self._node_acoustic_file_name = "acoustic_nodal_info.dat"
        self._node_structural_file_name = "structural_nodal_info.dat"
        self._elements_file_name = "elements_info.dat"
        self._imported_data_folder_name = "imported_data"
        self._backup_geometry_foldername = "geometry_backup"

    # def new(self,
    #         length_unit, 
    #         element_size, 
    #         geometry_tolerance, 
    #         import_type,
    #         geometry_path = ""):

    #     self._length_unit = length_unit
    #     self._element_size = float(element_size)
    #     self._geometry_tolerance = float(geometry_tolerance)
    #     self._import_type = int(import_type)
    #     self._geometry_path = geometry_path
    #     #
    #     self._project_path = app().main_window.temp_project_file_path
    #     self._project_ini_file_path = get_new_path(self._project_path, self._project_ini_name)
    #     #
    #     self._node_acoustic_path = get_new_path(self._project_path, self._node_acoustic_file_name)
    #     self._node_structural_path = get_new_path(self._project_path, self._node_structural_file_name)
    #     self._element_info_path = get_new_path(self._project_path, self._elements_file_name)
    #     self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
    #     self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
    #     self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")
    
    def copy(self,
             project_path,
             geometry_path = ""):
        
        self._project_path = project_path
        self._geometry_path = geometry_path
        #
        self._project_ini_file_path = get_new_path(self._project_path, self._project_ini_name)
        self._node_structural_path = get_new_path(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path = get_new_path(self._project_path, self._node_acoustic_file_name)
        self._element_info_path = get_new_path(self._project_path, self._elements_file_name)
        self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
        self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
        self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")

    def get_list_filenames_to_maintain_after_reset(self, **kwargs):

        reset_fluids = kwargs.get('reset_fluids', False)
        reset_materials = kwargs.get('reset_materials', False)
        reset_acoustic_model = kwargs.get('reset_acoustic_model', False)
        reset_structural_model = kwargs.get('reset_structural_model', False)

        list_filenames = os.listdir(self._project_path).copy()
        imported_data_files = list()
        if self._imported_data_folder_name in list_filenames:
            imported_data_files = os.listdir(self._imported_data_folder_path).copy()

        files_to_maintain_after_reset = list()
        files_to_maintain_after_reset.append(self._project_ini_name)

        if not reset_fluids:
            files_to_maintain_after_reset.append(self._fluid_file_name)

        if not reset_materials:
            files_to_maintain_after_reset.append(self._material_file_name)

        if reset_acoustic_model:
            if self._imported_data_folder_name in list_filenames:
                if "acoustic" in imported_data_files:
                    file_path = get_new_path(self._imported_data_folder_path, "acoustic")
                    rmtree(file_path)
        else:
            files_to_maintain_after_reset.append(self._node_acoustic_file_name)

        if reset_structural_model:
            if self._imported_data_folder_name in list_filenames:
                if "structural" in imported_data_files:
                    file_path = get_new_path(self._imported_data_folder_path, "structural")
                    rmtree(file_path)
        else:
            files_to_maintain_after_reset.append(self._node_structural_file_name)
            
        if os.path.exists(self._geometry_path):
            files_to_maintain_after_reset.append(os.path.basename(self._geometry_path))

        return files_to_maintain_after_reset

    def remove_all_unnecessary_files(self, **kwargs):
        list_filenames = os.listdir(self._project_path).copy()
        files_to_maintain = self.get_list_filenames_to_maintain_after_reset(**kwargs)
        for filename in list_filenames:
            if filename not in files_to_maintain:
                file_path = get_new_path(self._project_path, filename)
                if os.path.exists(file_path):
                    if filename == self._imported_data_folder_name:
                        if len(os.listdir(file_path).copy()):
                            continue
                    if "." in filename:
                        os.remove(file_path)
                    else:
                        rmtree(file_path)

    # def load(self, project_file_path):

    #     self.project_file_path = Path(project_file_path)
    #     self._project_path = os.path.dirname(self.project_file_path)

    #     config = configparser.ConfigParser()
    #     config.read(project_file_path)

    #     section = config['PROJECT']
    #     # project_name = section['name']
    #     import_type = int(section['import type'])

    #     keys = list(section.keys())

    #     if 'length unit' in keys:
    #         self._length_unit = section['length unit']

    #     if 'geometry file' in keys:
    #         geometry_file = section['geometry file']
    #         self._geometry_path =  get_new_path(self._project_path, geometry_file)

    #     if 'element size' in keys:
    #         element_size = section['element size']
    #         self._element_size = float(element_size)

    #     if 'geometry tolerance' in keys:
    #         geometry_tolerance = section['geometry tolerance']
    #         self._geometry_tolerance = float(geometry_tolerance)

    #     if 'material list file' in keys:
    #         self._material_file_name = section['material list file']

    #     if 'fluid list file' in keys:
    #         self._fluid_file_name = section['fluid list file']

    #     # self._project_name = project_name
    #     self._import_type = import_type
    #     self._project_ini_file_path = get_new_path(self._project_path, self._project_ini_name)
    #     self._element_info_path =  get_new_path(self._project_path, self._elements_file_name)
    #     self._node_structural_path =  get_new_path(self._project_path, self._node_structural_file_name)
    #     self._node_acoustic_path =  get_new_path(self._project_path, self._node_acoustic_file_name)
    #     self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
    #     self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
    #     self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")

    #Frequency Setup Analysis
    def load_analysis_file(self):

        analysis_setup = app().main_window.pulse_file.read_analysis_setup_from_file()

        if analysis_setup is None:
            f_min = 0.
            f_max = 0.
            f_step = 0.
            global_damping = [0., 0., 0., 0.]

        else:
            f_min = analysis_setup["f_min"]
            f_max = analysis_setup["f_max"]
            f_step = analysis_setup["f_step"]
            global_damping = analysis_setup["global damping"]

        return f_min, f_max, f_step, global_damping

    def add_frequency_in_file(self, f_min, f_max, f_step):

        analysis_setup = app().main_window.pulse_file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        analysis_setup["f_min"] = f_min
        analysis_setup["f_max"] = f_max
        analysis_setup["f_step"] = f_step

        app().main_window.pulse_file.write_analysis_setup_in_file(analysis_setup)

    def add_damping_in_file(self, global_damping):

        analysis_setup = app().main_window.pulse_file.read_analysis_setup_from_file()
        if analysis_setup is None:
            analysis_setup = dict()

        analysis_setup["global damping"] = global_damping

        app().main_window.pulse_file.write_analysis_setup_in_file(analysis_setup)

    def reset_project_setup(self, **kwargs):

        reset_analysis_setup = kwargs.get('reset_analysis_setup', False)

        if reset_analysis_setup:

            temp_project_base_file_path =  get_new_path(self._project_path, self._project_ini_name)
            config = configparser.ConfigParser()
            config.read(temp_project_base_file_path)
            sections = config.sections()

            if "Frequency setup" in sections:
                config.remove_section("Frequency setup")

            if "Global damping setup" in sections:
                config.remove_section("Global damping setup")

            self.write_data_in_file(temp_project_base_file_path, config)

    def reset_entity_file(self, **kwargs):

        reset_fluids = kwargs.get('reset_fluids', False)
        reset_materials = kwargs.get('reset_materials', False)

        keys_to_ignore = list()
        keys_to_ignore.append("structure name")
        keys_to_ignore.append("structural element type")
        keys_to_ignore.append("section parameters")
        keys_to_ignore.append("start coords")
        keys_to_ignore.append("corner coords")
        keys_to_ignore.append("end coords")
        keys_to_ignore.append("curvature radius")

        if not reset_fluids:
            keys_to_ignore.append("fluid id")

        if not reset_materials:
            keys_to_ignore.append("material id")

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        if os.path.exists(self._pipeline_path):

            for tag in config.sections():
                keys = list(config[tag].keys())
                for key in keys:
                    if key in keys_to_ignore:
                        continue
                    else:
                        config.remove_option(tag, key)

            self.write_data_in_file(self._pipeline_path, config)


    def update_entity_file(self, entities, dict_map_lines={}):

        try:
            
            if os.path.exists(self._pipeline_path):

                config = configparser.ConfigParser()
                config2 = configparser.ConfigParser()
                config2.read(self._pipeline_path)
                sections = config2.sections()

                mapped_entities = list()
                for entity_id in entities:
                    if len(dict_map_lines) == 0:
                        config[str(entity_id)] = {}
                    elif str(entity_id) not in sections:
                        config[str(entity_id)] = {}
                    elif entity_id not in dict_map_lines.keys():
                        config[str(entity_id)] = {} 
                    else:
                        for section in sections:
                            if "-" in section:
                                prefix = int(section.split("-")[0])
                                sufix = int(section.split("-")[1])
                                if dict_map_lines[entity_id] == prefix:
                                    _key = f"{entity_id}-{sufix}"
                                    config[_key] = config2[section]
                            else:
                                if entity_id not in mapped_entities:
                                    config[str(entity_id)] = config2[str(dict_map_lines[entity_id])]
                                    mapped_entities.append(entity_id)
            
                self.write_data_in_file(self._pipeline_path, config)

        except Exception as _error:
            print(str(_error))

    def get_entity_file_data(self):

        entity_data = {}
        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for entity in config.sections():
            keys = config[entity].keys()
            if len(config[entity].keys()) > 0:
                dict_section = {}
                for key in keys:
                    dict_section[key] = config[entity][key]
                
                entity_data[entity] = dict_section

        return entity_data

    def check_if_there_are_tables_at_the_model(self):
        if os.path.exists(self._structural_imported_data_folder_path):
            return True
        if os.path.exists(self._acoustic_imported_data_folder_path):
            return True
        return False

    def get_cross_sections_from_file(self):
        """ This method returns a dictionary of already applied cross-sections.
        """
        try:

            entityFile = configparser.ConfigParser()
            entityFile.read(self._pipeline_path)
            sections = entityFile.sections()

            _id = 1
            section_info = dict()
            variable_section_line_ids = list()
            parameters_to_entity_id = defaultdict(list)
            parameters_to_elements_id = defaultdict(list)

            for entity in sections:

                line_prefix = ""
                list_elements = list()

                section = entityFile[entity]
                keys = section.keys()

                if 'structural element type' in keys:
                    structural_element_type = section['structural element type']
                else:
                    structural_element_type = "pipe_1"

                if 'section type' in keys:
                    section_type_label = section['section type']
                else:
                    section_type_label = "Pipe section"

                if structural_element_type in ["expansion_joint", "valve"]:
                    continue
                
                section_parameters = list()
                if structural_element_type == "pipe_1":

                    if 'section parameters' in keys:
                        str_section_parameters = section['section parameters']
                        section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
  
                    if len(section_parameters) == 10:
                        if line_prefix not in variable_section_line_ids:
                            variable_section_line_ids.append(entity)

                    if "-" in entity:
                        line_prefix = entity.split("-")[0]
                        if line_prefix in variable_section_line_ids:
                            continue
                        elif 'list of elements' in keys:
                            str_list_elements = section['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)                 

                else:

                        structural_element_type = f"beam_1 - {section_type_label}"
                        if section_type_label == "Generic section":   
                            continue              

                        else:
                            if 'section parameters' in keys:
                                str_section_parameters = section['section parameters']
                                section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)

                str_section_parameters = str(section_parameters)
                if str_section_parameters not in parameters_to_entity_id.keys():
                    section_info[_id] = [structural_element_type, section_parameters]
                    _id += 1

                if line_prefix == "":
                    parameters_to_entity_id[str_section_parameters].append(int(entity))

                else:
                    if list_elements:
                        for element_id in list_elements:
                            parameters_to_elements_id[str_section_parameters].append(element_id)
                    else:    
                        parameters_to_entity_id[str_section_parameters].append(int(entity))

            id_1 = 0
            id_2 = 0
            section_info_elements = dict()
            section_info_lines = dict()

            for _id, _data in section_info.items():

                _section_parameters = _data[1]
                str_section_parameters = str(_section_parameters)

                if str_section_parameters in parameters_to_entity_id.keys():
                    id_1 += 1
                    data_lines = _data.copy()
                    data_lines.append("line ids")
                    data_lines.append(parameters_to_entity_id[str_section_parameters])
                    section_info_lines[id_1] = data_lines

                if str_section_parameters in parameters_to_elements_id.keys():
                    id_2 += 1
                    data_elements = _data.copy()
                    data_elements.append("element ids")
                    data_elements.append(parameters_to_elements_id[str_section_parameters])
                    section_info_elements[id_2] = data_elements

        except Exception as error_log:

            title = "Error while processing cross-sections"
            message = "Error detected while processing the 'get_cross_sections_from_file' method.\n\n"
            message += f"Last line id: {entity}\n\n"
            message += f"Details: \n\n {str(error_log)}"
            PrintMessageInput([window_title, title, message])

            return dict(), dict()

        return section_info_lines, section_info_elements
    
    def add_cross_section_in_file(self, lines, cross_section):  

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            line_id = str(line_id)

            for section in config.sections():
                section_prefix = line_id + '-'
                if section_prefix in section:
                    config.remove_section(section)
        
            str_keys = [    'section type',
                            'section parameters',
                            'section properties',
                            'expansion joint parameters',
                            'expansion joint stiffness',
                            'valve parameters',
                            'valve center coordinates',
                            'valve section parameters',
                            'flange section parameters',
                            'list of elements',
                            'number of flange elements'    ]

            for str_key in str_keys:
                if str_key in list(config[line_id].keys()):
                    config.remove_option(section=line_id, option=str_key)

            if cross_section is not None:
                config[line_id]['section type'] = cross_section.section_label
                if cross_section.beam_section_info is not None:
                    if line_id in list(config.sections()):
                        
                        if "Generic section" == cross_section.section_label:
                            config[line_id]['section properties'] = str(cross_section.section_properties)
                        else:
                            config[line_id]['section parameters'] = str(cross_section.section_parameters)
                else:
                    if line_id in list(config.sections()):
                        section_parameters = cross_section.section_parameters
                        config[line_id]['section parameters'] = str(section_parameters)
        
        self.write_data_in_file(self._pipeline_path, config)      

    def add_cross_section_segment_in_file(self, section_info : dict):
        
        try:

            config = app().main_window.pulse_file.read_pipeline_data_from_file()

            for line_id, data in section_info.items():

                line_id = str(line_id)

                str_keys = [    'section parameters',
                                'section properties',
                                'section type',
                                'expansion joint parameters',
                                'expansion joint stiffness',
                                'valve parameters',
                                'valve center coordinates',
                                'valve section parameters',
                                'flange section parameters'   ]

                for str_key in str_keys:
                    if str_key in list(config[line_id].keys()):
                        config.remove_option(section=line_id, option=str_key)

                if data is not None:

                    section_type_label = data["section_type_label"]
                    config[line_id]['section type'] = section_type_label

                    if section_type_label == "Pipe section":
                        if line_id in list(config.sections()):
                            section_parameters = data["section_parameters"]
                            config[line_id]['section parameters'] = str(section_parameters)

                    else:

                        if line_id in list(config.sections()):

                            if section_type_label == "Generic section":
                                section_properties = data["section_properties"]
                                config[line_id]['section properties'] = str(section_properties)

                            else:
                                section_parameters = data["section_parameters"]
                                config[line_id]['section parameters'] = str(section_parameters)                    

        except Exception as error_log:
            title = "Error while writing cross-section data in file"
            message = str(error_log)
            PrintMessageInput([window_title_1, title, message])
            return

        app().main_window.pulse_file.write_pipeline_data_in_file(config)

    def add_multiple_cross_section_in_file(self, lines, map_cross_sections_to_elements):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        str_keys = [    'structural element type',
                        'section type',
                        'section parameters',
                        'section properties',
                        'expansion joint parameters',
                        'expansion joint stiffness'    ]

        for line_id in lines:
            subkey = 0
            str_line = str(line_id)
            if 'structural element type' in config[str_line].keys():
                etype = config[str_line]['structural element type']
            else:
                etype = 'pipe_1'
            for str_key in str_keys:
                if str_key in list(config[str_line].keys()):
                    config.remove_option(section=str_line, option=str_key)

            for key, elements in map_cross_sections_to_elements.items():
                                
                cross_strings = key[1:-1].split(',')
                vals = [float(value) for value in cross_strings] 
                section_parameters = [vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]]

                subkey += 1
                key = str_line + "-" + str(subkey)

                config[key] = { 'structural element type' : etype,
                                'section type' : 'Pipe section',
                                'section parameters' : str(section_parameters),
                                'list of elements' : str(elements) }

        self.write_data_in_file(self._pipeline_path, config)


    def modify_variable_cross_section_in_file(self, lines, section_info):
        
        if isinstance(lines, int):
            lines = [lines]

        parameters = section_info["section_parameters"]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        sections = list(config.sections())

        for line_id in lines:
            str_line = str(line_id)
            if str_line in sections:
                config[str_line]['section parameters'] = str(parameters)

            for section in sections:
                prefix = f"{line_id}-"
                if prefix in section:
                    config.remove_section(section=section)
            
        self.write_data_in_file(self._pipeline_path, config)


    def modify_valve_in_file(self, lines, parameters):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        sections = config.sections()

        list_keys = [   'section type',
                        'section parameters',
                        'section properties',
                        'expansion joint parameters',
                        'expansion joint stiffness',
                        'valve parameters',
                        'valve center coordinates',
                        'valve section parameters',
                        'flange section parameters',
                        'list of elements',
                        'number of flange elements'   ]
        
        for line_id in lines:
            str_line = str(line_id)
            for _key in list_keys:
                if _key in list(config[str_line].keys()):
                    config.remove_option(section=str_line, option=_key)
            
            for section in sections:
                if f'{line_id}-' in section:
                    config.remove_section(section)
            
            if parameters:
                valve_length = parameters["valve_length"]
                stiffening_factor = parameters["stiffening_factor"]
                valve_mass = parameters["valve_mass"]
                valve_center_coordinates = parameters["valve_center_coordinates"]
                
                list_valve_elements = parameters["valve_elements"]
                valve_section_parameters = parameters["valve_section_parameters"]  
                valve_parameters = [valve_length, stiffening_factor, valve_mass]

                config[str_line]['valve parameters'] = str(valve_parameters)
                config[str_line]['valve center coordinates'] = str(list(valve_center_coordinates))
                config[str_line]['valve section parameters'] = str(valve_section_parameters)
                config[str_line]['list of elements'] = str(list_valve_elements)
                
                if "number_flange_elements" in parameters.keys():
                    flange_parameters = parameters["flange_section_parameters"]
                    number_flange_elements = parameters["number_flange_elements"]
                    config[str_line]['flange section parameters'] = str(flange_parameters)
                    config[str_line]['number of flange elements'] = str(number_flange_elements)

        self.write_data_in_file(self._pipeline_path, config)


    def modify_expansion_joint_in_file(self, lines, parameters):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        sections = config.sections()

        list_keys = [   'section type',
                        'section parameters',
                        'section properties',
                        'expansion joint parameters',
                        'expansion joint stiffness',
                        'valve parameters',
                        'valve center coordinates',
                        'valve section parameters',
                        'flange section parameters',
                        'list of elements',
                        'number of flange elements'   ]
        
        for line_id in lines:
            str_line = str(line_id)
            for _key in list_keys:
                if _key in list(config[str_line].keys()):
                    config.remove_option(section=str_line, option=_key)
            
            for section in sections:
                if f'{line_id}-' in section:
                    config.remove_section(section)
            
            if parameters is not None:
                list_table_names = parameters[2]
                config[str_line]['expansion joint parameters'] = str(parameters[0])
                if list_table_names == [None, None, None, None]:
                    config[str_line]['expansion joint stiffness'] = str(parameters[1])
                else:
                    str_table_names = f"[{list_table_names[0]},{list_table_names[1]},{list_table_names[2]},{list_table_names[3]}]"
                    config[str_line]['expansion joint stiffness'] = str_table_names

        self.write_data_in_file(self._pipeline_path, config)

    def add_multiple_cross_sections_expansion_joints_valves_in_file(self, 
                                                                    lines, 
                                                                    map_cross_sections_to_elements, 
                                                                    map_expansion_joint_to_elements, 
                                                                    map_valve_to_elements,
                                                                    update_by_cross=False):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        config_base = configparser.ConfigParser()
        config_base.read(self._pipeline_path)

        sections = config_base.sections()
        
        str_keys = [    'structural element type',
                        'section type',
                        'section parameters',
                        'section properties',
                        'expansion joint parameters',
                        'expansion joint stiffness',
                        'valve parameters',
                        'valve center coordinates',
                        'valve section parameters',
                        'flange section parameters',
                        'list of elements',
                        'number of flange elements'    ]
        
        for line_id in lines:
            
            str_line = str(line_id) 

            for str_key in str_keys:
                if str_key in config[str_line].keys():
                    config.remove_option(section=str_line, option=str_key)
            
            for section in sections:
                if f'{line_id}-' in section:
                    config.remove_section(section)        
            
            counter_1 = 0
            for (cross_key, elements) in map_cross_sections_to_elements.items():
                
                counter_1 += 1
                section_key = f"{line_id}-{counter_1}"             
                cross_strings = cross_key[1:-1].split(',')

                vals = [float(value) for value in cross_strings] 
                section_parameters = [vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]]
                
                index_etype = int(vals[6])
                if index_etype == 0:
                    etype = 'pipe_1'
            
                config[section_key] = { 'structural element type' : etype,
                                        'section type' : 'Pipe section',
                                        'section parameters': str(section_parameters),
                                        'list of elements': str(elements) }

            counter_2 = 0
            if update_by_cross:    
                for section in sections:
                    if f'{line_id}-' in section:
                        if 'valve parameters' in config_base[section].keys():
                            counter_2 += 1
                            section_key = f"{line_id}-{counter_1 + counter_2}"
                            config[section_key] = config_base[section]
            
            else:

                for [valve_data, _] in map_valve_to_elements.values():
                    counter_2 += 1
                    section_key = f"{line_id}-{counter_1 + counter_2}"
                
                    valve_elements = valve_data["valve_elements"]
                    valve_parameters = [valve_data["valve_length"], valve_data["stiffening_factor"], valve_data["valve_mass"]]
                    valve_center_coordinates = valve_data["valve_center_coordinates"]
                    valve_section_parameters = list(valve_data["valve_section_parameters"])

                    if "flange_elements" in valve_data.keys():

                        number_flange_elements = valve_data["number_flange_elements"]
                        flange_section_parameters = list(valve_data["flange_section_parameters"])

                        config[section_key] = { 'structural element type' : 'valve',
                                                'valve parameters' : f'{valve_parameters}',
                                                'valve center coordinates' : f'{valve_center_coordinates}',
                                                'valve section parameters' : f'{valve_section_parameters}',
                                                'flange section parameters' : f'{flange_section_parameters}',
                                                'list of elements' : f'{valve_elements}',
                                                'number of flange elements' : f'{number_flange_elements}' }

                    else:

                        config[section_key] = { 'structural element type' : 'valve',
                                                'valve parameters' : f'{valve_parameters}',
                                                'valve center coordinates' : f'{valve_center_coordinates}',
                                                'valve section parameters' : f'{valve_section_parameters}',
                                                'list of elements' : f'{valve_elements}' }

            counter_3 = 0
            if update_by_cross:    
                for section in sections:
                    if f'{line_id}-' in section:
                        if 'expansion joint parameters' in config_base[section].keys():
                            counter_3 += 1
                            section_key = f"{line_id}-{counter_1 + counter_2 + counter_3}"
                            config[section_key] = config_base[section]

            else:

                for [exp_joint_parameters, list_elements, list_table_names] in map_expansion_joint_to_elements.values():

                    counter_2 += 1
                    section_key = f"{line_id}-{counter_1 + counter_2 + counter_3}"
                
                    if list_table_names.count(None) == 4:

                        config[section_key] = { 'structural element type' : 'expansion_joint',
                                                'expansion joint parameters' : f'{exp_joint_parameters[0]}',
                                                'expansion joint stiffness' : f'{exp_joint_parameters[1]}',
                                                'list of elements' : f'{list_elements}' }
                            
                    else:

                        str_table_names = f"[{list_table_names[0]},{list_table_names[1]},{list_table_names[2]},{list_table_names[3]}]"

                        config[section_key] = { 'structural element type' : 'expansion_joint',
                                                'expansion joint parameters' : f'{exp_joint_parameters[0]}',
                                                'expansion joint stiffness' : str_table_names,
                                                'list of elements' : f'{list_elements}' }

        self.write_data_in_file(self._pipeline_path, config)

    def add_length_correction_in_file(self, elements, _type, section, psd_label=""): 
        
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if section in list(config.sections()):
            config[section]['length correction type'] = str(_type)
            config[section]['list of elements'] = str(elements)
            if psd_label != "":
                config[section]['psd label'] = psd_label

        else:
            config[section] =   {   'length correction type': str(_type),
                                    'list of elements': str(elements),
                                    'psd label' : psd_label   }

        self.write_data_in_file(self._element_info_path, config)

    def add_perforated_plate_in_file(self, elements, perforated_plate, section): 
        
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        data  = [   perforated_plate.hole_diameter,
                    perforated_plate.thickness,
                    perforated_plate.porosity,
                    perforated_plate.linear_discharge_coefficient,
                    int(perforated_plate.single_hole),
                    int(perforated_plate.nonlinear_effect),
                    perforated_plate.nonlinear_discharge_coefficient,
                    perforated_plate.correction_factor,
                    int(perforated_plate.bias_effect),
                    perforated_plate.bias_coefficient,
                    int(perforated_plate.type)   ]
        
        if perforated_plate.dimensionless_impedance_table_name is not None:
            dimensionless_impedance = perforated_plate.dimensionless_impedance_table_name
        else:
            dimensionless_impedance = perforated_plate.dimensionless_impedance

        if section in list(config.sections()):
            config[section]['perforated plate data'] = str(data)
            config[section]['dimensionless impedance'] = f"[{dimensionless_impedance}]"
            config[section]['list of elements'] = str(elements)
        else:
            config[section] =   { 'perforated plate data': str(data),
                                  'dimensionless impedance' : f"[{dimensionless_impedance}]",
                                  'list of elements': str(elements) }

        if len(list(config.sections())):
            self.write_data_in_file(self._element_info_path, config)
        else:
            os.remove(self._element_info_path)

    def modify_B2PX_rotation_decoupling_in_file(self, 
                                                elements = None, 
                                                nodes = None, 
                                                rotations_maks = None, 
                                                section = None, 
                                                remove = False, 
                                                reset = False):

        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if remove:
            config.remove_section(section)

        elif reset:
            for section in list(config.sections()):
                if 'B2PX ROTATION DECOUPLING' in section:
                    config.remove_section(section) 

        else:
            if section in list(config.sections()):
                config[section]['list of elements'] = str(elements)
                config[section]['list of nodes'] = str(nodes)
                config[section]['rotation dofs mask'] = str(rotations_maks)
            else:
                config[section] = { 'list of elements': str(elements),
                                    'list of nodes': str(nodes),
                                    'rotation dofs mask': str(rotations_maks) }

        if len(list(config.sections())):
            self.write_data_in_file(self._element_info_path, config)
        else:
            os.remove(self._element_info_path)

    def modify_stress_stiffnening_line_in_file(self, lines, pressures, remove=False):
        
        if isinstance(lines, int):
            lines = [lines] 
        
        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            str_entity_id = str(line_id)
            if remove:
                if str_entity_id in list(config.sections()):
                    config.remove_option(section=str_entity_id, option='stress stiffening parameters')
            else:
                config[str_entity_id]['stress stiffening parameters'] = str(pressures)

        self.write_data_in_file(self._pipeline_path, config)

    def modify_stress_stiffnening_element_in_file(self, elements, parameters, section, remove=False):

        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if remove:
            config.remove_section(section)
        else:
            if section in list(config.sections()):
                config[section]['stress stiffening parameters'] = str(parameters)
                config[section]['list of elements'] = str(elements)
            else:
                config[section] = { 'stress stiffening parameters' : str(parameters),
                                    'list of elements': str(elements) }
                
        if len(list(config.sections())):
            self.write_data_in_file(self._element_info_path, config)
        else:
            os.remove(self._element_info_path)

    def modify_capped_end_elements_in_file(self, elements, value, section): 
        
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if value:
            if section in list(config.sections()):
                config[section]['list of elements'] = str(elements)
            else:
                config[section] = {'list of elements' : str(elements)}
        else:
            if section in list(config.sections()):    
                config.remove_section(section)

        if len(list(config.sections())):
            self.write_data_in_file(self._element_info_path, config)
        else:
            os.remove(self._element_info_path)

    def modify_capped_end_lines_in_file(self, lines, value):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        
        for line_id in lines:
            str_entity_id = str(line_id)
            if value:    
                config[str_entity_id]['capped end'] = str(value)
            else:
                config.remove_option(section=str_entity_id, option='capped end')

        self.write_data_in_file(self._pipeline_path, config)

    def modify_structural_element_type_in_file(self, lines, element_type):
        
        if isinstance(lines, int):
            lines = [lines]

        config = app().main_window.pulse_file.read_pipeline_data_from_file()

        for line_id in lines:
            str_line = str(line_id)
            if element_type in ["beam_1"]:
                str_keys = ['fluid id', 'stress stiffening parameters']
                
                for str_key in str_keys:
                    if str_key in config[str_line].keys():
                        config.remove_option(section=str_line, option=str_key)

            config[str_line]['structural element type'] = element_type

        app().main_window.pulse_file.write_pipeline_data_in_file(config)

    def modify_structural_element_wall_formulation_in_file(self, lines, formulation):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            str_line = str(line_id)     
            if formulation is None:
                str_key = 'structural element wall formulation'
                config.remove_option(section=str_line, option=str_key)
            else:
                config[str_line]['structural element wall formulation'] = formulation

        self.write_data_in_file(self._pipeline_path, config)

    def modify_structural_element_force_offset_in_file(self, lines, force_offset):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            str_line = str(line_id)     
            if force_offset is None:
                str_key = 'force offset'
                config.remove_option(section=str_line, option=str_key)
            else:
                config[str_line]['force offset'] = str(force_offset)

        self.write_data_in_file(self._pipeline_path, config)

    def modify_acoustic_element_type_in_file(self, lines, element_type, proportional_damping=None, vol_flow=None):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        
        for line_id in lines:
            _section = str(line_id)

            config[_section]['acoustic element type'] = element_type
            if element_type == 'proportional':
                config[_section]['proportional damping'] = str(proportional_damping)
                
            if element_type != 'proportional' and 'proportional damping' in config[_section].keys():
                config.remove_option(section=_section, option='proportional damping')  

            if element_type in ["undamped mean flow", "peters", "howe"]:
                config[_section]['volume flow rate'] = str(vol_flow)

            if element_type not in ["undamped mean flow", "peters", "howe"] and 'volume flow rate' in config[_section].keys():
                config.remove_option(section=_section, option='volume flow rate')  
    
        self.write_data_in_file(self._pipeline_path, config)

    def add_pipeline_data_in_file(self, structures_data : dict):

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id, structure_data in structures_data.items():
            for key, data in structure_data.items():
                config[str(line_id)][key] = str(data)

        self.write_data_in_file(self._pipeline_path, config)

    # def get_pipeline_data_from_file(self):
    #     '''
    #     This method returns the all required data to build pipeline segments.
    #     '''

    #     config = configparser.ConfigParser()
    #     config.read(self._pipeline_path)
    #     segment_build_data = dict()

    #     for section in config.sections():

    #         if "-" in section:
    #             continue

    #         tag = int(section)
    #         keys = config[section].keys()
    #         aux = dict()

    #         if "start coords" in keys:
    #             start_coords = config[section]["start coords"]
    #             aux["start_coords"] = get_list_of_values_from_string(start_coords, int_values=False)

    #         if "end coords" in keys:
    #             end_coords = config[section]["end coords"]
    #             aux["end_coords"] = get_list_of_values_from_string(end_coords, int_values=False)

    #         if "corner coords" in keys:
    #             corner_coords = config[section]["corner coords"]
    #             aux["corner_coords"] = get_list_of_values_from_string(corner_coords, int_values=False)

    #         if "curvature radius" in keys:
    #             curvature_radius = config[section]["curvature radius"]
    #             aux["curvature_radius"] = float(curvature_radius)

    #         if 'structural element type' in keys:
    #             structural_element_type = config[section]["structural element type"]
    #             aux["structural_element_type"] = structural_element_type
    #         else:
    #             structural_element_type = "pipe_1"

    #         if 'section type' in keys:
    #             section_type_label = config[section]["section type"]
    #             aux["section_type_label"] = section_type_label

    #         if 'section parameters' in keys:
    #             section_parameters = config[section]["section parameters"]
    #             aux["section_parameters"] = get_list_of_values_from_string(section_parameters, int_values=False)

    #         if structural_element_type == "beam_1":
    #             if 'section properties' in keys:
    #                 section_properties = config[section]["section properties"]
    #                 aux["section_properties"] = get_list_of_values_from_string(section_properties, int_values=False)
    #             else:
    #                 aux["section_properties"] = get_beam_section_properties(section_type_label, aux["section_parameters"])

    #         if 'material id' in keys:
    #             try:
    #                 aux["material_id"] = int(config[section]["material id"])
    #             except:
    #                 pass

    #         if 'psd label' in keys:
    #             aux["psd_label"] = config[section]["psd label"]

    #         if 'link type' in keys:
    #             aux["link type"] = config[section]["link type"]

    #         is_bend = ('corner coords' in keys) and ('curvature radius' in keys)
    #         if is_bend:
    #             segment_build_data[tag, "Bend"] = aux

    #         else:
    #             segment_build_data[tag, "Pipe"] = aux

    #     return segment_build_data

    def add_material_in_file(self, lines, material):

        if isinstance(lines, int):
            lines = [lines]
        
        if material is None:
            material_id = ""
        else:
            material_id = material.identifier

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            config[str(line_id)]['material id'] = str(material_id)
            
        self.write_data_in_file(self._pipeline_path, config)

    def add_material_segment_in_file(self, lines, material_id):

        if isinstance(lines, int):
            lines = [lines]

        if material_id is None:
            material_id = ""

        config = app().main_window.pulse_file.read_pipeline_data_from_file()

        for line_id in lines:
            config[str(line_id)]['material id'] = str(material_id)

        app().main_window.pulse_file.write_pipeline_data_in_file(config)

    def add_psd_label_in_file(self, lines, psd_label):

        if isinstance(lines, int):
            lines = [lines]
        
        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            config[str(line_id)]['psd label'] = psd_label
            
        self.write_data_in_file(self._pipeline_path, config)

    # def get_material_properties(self, material_id):
    #     config = configparser.ConfigParser()
    #     config.read(self._material_list_path)
    #     sections = config.sections()

    #     if isinstance(material_id, int):
    #         material_id = str(material_id)
    #         for section in sections:
    #             if material_id == config[section]["identifier"]:

    #                 name = str(config[section]['name'])
    #                 identifier = int(config[section]['identifier'])
    #                 density =  float(config[section]['density'])
    #                 elasticity_modulus =  float(config[section]['elasticity modulus'])
    #                 poisson =  float(config[section]['poisson'])
    #                 thermal_expansion_coefficient = config[section]['thermal expansion coefficient']
    #                 # color =  str(config[section]['color'])
    #                 # elasticity_modulus *= (10**(9))
    #                 if thermal_expansion_coefficient == "":
    #                     thermal_expansion_coefficient = float(0)
    #                 else:
    #                     thermal_expansion_coefficient = float(thermal_expansion_coefficient)

    #                 return [name, identifier, density, elasticity_modulus, poisson, thermal_expansion_coefficient]
    #         return None

    def add_fluid_in_file(self, lines, fluid):
        
        if isinstance(lines, int):
            lines = [lines]

        if fluid is None:
            fluid_id = ""
        else:
            fluid_id = fluid.identifier

        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            config[str(line_id)]['fluid id'] = str(fluid_id)

        self.write_data_in_file(self._pipeline_path, config)

    def modify_compressor_info_in_file(self, lines, compressor_info={}):
        
        if isinstance(lines, int):
            lines = [lines]
        
        config = configparser.ConfigParser()
        config.read(self._pipeline_path)

        for line_id in lines:
            if compressor_info:
                config[str(line_id)]['compressor info'] = str(list(compressor_info.values()))
            else:
                _section = str(line_id)
                if 'compressor info' in config[str(line_id)].keys():
                    config.remove_option(section=_section, option='compressor info')  

        self.write_data_in_file(self._pipeline_path, config) 

    def get_structural_bc_data_from_dat_file(self):

        config = configparser.ConfigParser()
        config.read(self._node_structural_path)

        prescribed_dofs_data = dict()
        nodal_loads_data = dict()
        lumped_inertia_data = dict()
        lumped_stiffness_data = dict()
        lumped_damping_data = dict()
        elastic_link_stiffness_data = dict()
        elastic_link_damping_data = dict()

        for key in config.sections():

            if "-" in key:
                node_id = key
            else:
                node_id = int(key)

            section = config[key]
            bc_keys = list(section.keys())

            # node_id = int(key.split(" - ")[0])
            # try:
            #     node_id = int(node)
            # except:
            #     node_id = node

            if "displacements" in bc_keys and "rotations" in bc_keys:
                displacement_strings = section['displacements']
                rotation_strings = section['rotations']
                labels = [["Ux","Uy","Uz"],["Rx","Ry","Rz"]]
                folder_table_name = "prescribed_dofs_files"
                prescribed_dofs, prescribed_dofs_table_names, prescribed_dofs_freq = self._get_structural_bc_from_string(   displacement_strings, 
                                                                                                                            rotation_strings, 
                                                                                                                            labels,
                                                                                                                            folder_table_name=folder_table_name   )    
                if prescribed_dofs is not None:
                    if sum([1 if value is None else 0 for value in prescribed_dofs]) != 6:
                        prescribed_dofs_data[node_id] = [prescribed_dofs, prescribed_dofs_table_names, prescribed_dofs_freq]
                               
            if "forces" in bc_keys and "moments" in bc_keys:
                forces_strings = section['forces'] 
                moments_strings = section['moments']
                labels = [["Fx","Fy","Fz"],["Mx","My","Mz"]]
                folder_table_name = "nodal_loads_files"
                nodal_loads, nodal_loads_table_names, nodal_loads_freq = self._get_structural_bc_from_string(   forces_strings, 
                                                                                                                moments_strings, 
                                                                                                                labels,
                                                                                                                folder_table_name=folder_table_name   )
                if nodal_loads is not None:
                    if sum([1 if value is None else 0 for value in nodal_loads]) != 6:
                        nodal_loads_data[node_id] = [nodal_loads, nodal_loads_table_names, nodal_loads_freq]
            
            if "masses" in bc_keys and "moments of inertia" in bc_keys:
                masses = section['masses']
                moments_of_inertia = section['moments of inertia']
                labels = [["m_x","m_y","m_z"],["Jx","Jy","Jz"]]
                folder_table_name = "lumped_elements_files"
                lumped_inertia, inertia_table_names, inertia_freq = self._get_structural_bc_from_string(masses, 
                                                                                                        moments_of_inertia, 
                                                                                                        labels,
                                                                                                        folder_table_name=folder_table_name, 
                                                                                                        _complex=False)
                if lumped_inertia is not None:
                    if sum([1 if value is None else 0 for value in lumped_inertia]) != 6:
                        lumped_inertia_data[node_id] = [lumped_inertia, inertia_table_names, inertia_freq]

            if "spring stiffness" in bc_keys and "torsional spring stiffness" in bc_keys:
                spring_stiffness = section['spring stiffness']
                torsional_spring_stiffness = section['torsional spring stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                folder_table_name = "lumped_elements_files"
                lumped_stiffness, stiffness_table_names, stiffness_freq = self._get_structural_bc_from_string(  spring_stiffness, 
                                                                                                                torsional_spring_stiffness, 
                                                                                                                labels, 
                                                                                                                folder_table_name=folder_table_name,
                                                                                                                _complex=False  )
                if lumped_stiffness is not None:
                    if sum([1 if value is None else 0 for value in lumped_stiffness]) != 6:
                        lumped_stiffness_data[node_id] = [lumped_stiffness, stiffness_table_names, stiffness_freq]

            if "damping coefficients" in bc_keys and "torsional damping coefficients" in bc_keys:
                damping_coefficients = section['damping coefficients']
                torsional_damping_coefficients = section['torsional damping coefficients']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                folder_table_name = "lumped_elements_files"
                lumped_damping, damping_table_names, damping_freq = self._get_structural_bc_from_string(damping_coefficients, 
                                                                                                        torsional_damping_coefficients, 
                                                                                                        labels,
                                                                                                        folder_table_name=folder_table_name, 
                                                                                                        _complex=False)
                if lumped_damping is not None:
                    if sum([1 if value is None else 0 for value in lumped_damping]) != 6:
                        lumped_damping_data[node_id] = [lumped_damping, damping_table_names, damping_freq]

            if "connecting stiffness" in bc_keys and "connecting torsional stiffness" in bc_keys:
                connecting_stiffness = section['connecting stiffness']
                connecting_torsional_stiffness = section['connecting torsional stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                folder_table_name = "elastic_links_files"
                connecting_stiffness, connecting_stiffness_table_names, connecting_stiffness_freq = self._get_structural_bc_from_string(connecting_stiffness, 
                                                                                                                                        connecting_torsional_stiffness, 
                                                                                                                                        labels,
                                                                                                                                        folder_table_name=folder_table_name, 
                                                                                                                                        _complex=False)
                if connecting_stiffness is not None:
                    if sum([1 if value is None else 0 for value in connecting_stiffness]) != 6:
                        elastic_link_stiffness_data[node_id] = [connecting_stiffness, connecting_stiffness_table_names, connecting_stiffness_freq]
        
            if "connecting damping" in bc_keys and "connecting torsional damping" in bc_keys:
                connecting_damping = section['connecting damping']
                connecting_torsional_damping = section['connecting torsional damping']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                folder_table_name = "elastic_links_files"
                connecting_damping, connecting_damping_table_names, connecting_damping_freq = self._get_structural_bc_from_string(  connecting_damping, 
                                                                                                                                    connecting_torsional_damping, 
                                                                                                                                    labels, 
                                                                                                                                    folder_table_name=folder_table_name,
                                                                                                                                    _complex=False  )
                if connecting_damping is not None:
                    if sum([1 if value is None else 0 for value in connecting_damping]) != 6:
                        elastic_link_damping_data[node_id] = [connecting_damping, connecting_damping_table_names, connecting_damping_freq]
            
        bc_data = { "prescribed_dofs" : prescribed_dofs_data, 
                    "nodal_loads" : nodal_loads_data, 
                    "lumped_inertia" : lumped_inertia_data, 
                    "lumped_stiffness" : lumped_stiffness_data, 
                    "lumped_damping" : lumped_damping_data, 
                    "elastic_link_stiffness" : elastic_link_stiffness_data, 
                    "elastic_link_damping" : elastic_link_damping_data }

        return bc_data

    def get_acoustic_bc_data_from_dat_file(self):

        config = configparser.ConfigParser()
        config.read(self._node_acoustic_path)

        acoustic_pressure_data = dict()
        volume_velocity_data = dict() 
        specific_impedance_data = dict()
        radiation_impedance_data = dict()
        compressor_excitation_data = defaultdict(list)

        for key in config.sections():

            if "-" in key:
                node_id = key
            else:
                node_id = int(key)

            section = config[key]
            bc_keys = list(section.keys())

            if "acoustic pressure" in bc_keys:
                str_acoustic_pressure = section['acoustic pressure']
                acoustic_pressure, table_name, frequencies = self._get_acoustic_bc_from_string( str_acoustic_pressure, 
                                                                                                "acoustic pressure", 
                                                                                                "acoustic_pressure_files" )
                if acoustic_pressure is not None:
                    acoustic_pressure_data[node_id] = [acoustic_pressure, table_name, frequencies]
           
            if "volume velocity" in bc_keys:
                str_volume_velocity = section["volume velocity"]
                volume_velocity, table_name, frequencies = self._get_acoustic_bc_from_string(   str_volume_velocity, 
                                                                                                "volume velocity", 
                                                                                                "volume_velocity_files"   )
                if volume_velocity is not None:
                    volume_velocity_data[node_id] = [volume_velocity, table_name, frequencies]

            for bc_key in bc_keys:
                if "compressor excitation -" in bc_key:
                    str_compressor_excitation = section[bc_key]
                    if 'suction' in str_compressor_excitation:
                        connection_info = 'suction'
                    elif 'discharge' in str_compressor_excitation:
                        connection_info = 'discharge'
                    compressor_excitation, table_name, frequencies = self._get_acoustic_bc_from_string( str_compressor_excitation, 
                                                                                                        bc_key, 
                                                                                                        "compressor_excitation_files" )
                    if compressor_excitation is not None:
                        compressor_excitation_data[node_id].append([compressor_excitation, table_name, connection_info, frequencies])

            if "specific impedance" in bc_keys:
                str_specific_impedance = section['specific impedance']
                specific_impedance, table_name, frequencies = self._get_acoustic_bc_from_string(str_specific_impedance, 
                                                                                                "specific impedance", 
                                                                                                "specific_impedance_files")
                if specific_impedance is not None:
                    specific_impedance_data[node_id] = [specific_impedance, table_name, frequencies]

            if "radiation impedance" in bc_keys:
                str_radiation_impedance = section['radiation impedance']
                radiation_impedance_type, _, _ = self._get_acoustic_bc_from_string( str_radiation_impedance, 
                                                                                    "radiation impedance", "" )
                if radiation_impedance_type is not None:
                    radiation_impedance_data[node_id] = int(np.real(radiation_impedance_type))

        bc_data = {"acoustic_pressure" : acoustic_pressure_data,
                   "volume_velocity" : volume_velocity_data,
                   "specific_impedance" : specific_impedance_data,
                   "radiation_impedance" : radiation_impedance_data,
                   "compressor_excitation" : compressor_excitation_data}

        return bc_data

    # def get_acoustic_bc_data_from_file(self):
    #     path = self._node_acoustic_path
    #     if path.exists():
    #         with open(path) as file:
    #             read_data = json.load(file)
    #     else:
    #         read_data = dict()

    #     acoustic_pressure_data = dict()
    #     volume_velocity_data = dict() 
    #     specific_impedance_data = dict()
    #     radiation_impedance_data = dict()
    #     compressor_excitation_data = defaultdict(list)

    #     for key, data in read_data.items():

    #         node_id = int(key.split(" - ")[0])
    #         bc_keys = list(data.keys())
            
    #         if "acoustic pressure" in bc_keys:
    #             str_acoustic_pressure = data['acoustic pressure']
    #             acoustic_pressure, table_name, frequencies = self._get_acoustic_bc_from_string( str_acoustic_pressure, 
    #                                                                                             "acoustic pressure", 
    #                                                                                             "acoustic_pressure_files" )
    #             if acoustic_pressure is not None:
    #                 acoustic_pressure_data[node_id] = [acoustic_pressure, table_name, frequencies]
           
    #         if "volume velocity" in bc_keys:
    #             str_volume_velocity = data["volume velocity"]
    #             volume_velocity, table_name, frequencies = self._get_acoustic_bc_from_string(   str_volume_velocity, 
    #                                                                                             "volume velocity", 
    #                                                                                             "volume_velocity_files"   )
    #             if volume_velocity is not None:
    #                 volume_velocity_data[node_id] = [volume_velocity, table_name, frequencies]

    #         for bc_key in bc_keys:
    #             if "compressor excitation -" in bc_key:
    #                 str_compressor_excitation = data[bc_key]
    #                 if 'suction' in str_compressor_excitation:
    #                     connection_info = 'suction'
    #                 elif 'discharge' in str_compressor_excitation:
    #                     connection_info = 'discharge'
    #                 compressor_excitation, table_name, frequencies = self._get_acoustic_bc_from_string( str_compressor_excitation, 
    #                                                                                                     bc_key, 
    #                                                                                                     "compressor_excitation_files" )
    #                 if compressor_excitation is not None:
    #                     compressor_excitation_data[node_id].append([compressor_excitation, table_name, connection_info, frequencies])

    #         if "specific impedance" in bc_keys:
    #             str_specific_impedance = data['specific impedance']
    #             specific_impedance, table_name, frequencies = self._get_acoustic_bc_from_string(str_specific_impedance, 
    #                                                                                             "specific impedance", 
    #                                                                                             "specific_impedance_files")
    #             if specific_impedance is not None:
    #                 specific_impedance_data[node_id] = [specific_impedance, table_name, frequencies]

    #         if "radiation impedance" in bc_keys:
    #             str_radiation_impedance = data['radiation impedance']
    #             radiation_impedance_type, _, _ = self._get_acoustic_bc_from_string( str_radiation_impedance, 
    #                                                                                 "radiation impedance", "" )
    #             if radiation_impedance_type is not None:
    #                 radiation_impedance_data[node_id] = int(np.real(radiation_impedance_type))

    #     bc_data = {"acoustic_pressure" : acoustic_pressure_data,
    #                "volume_velocity" : volume_velocity_data,
    #                "specific_impedance" : specific_impedance_data,
    #                "radiation_impedance" : radiation_impedance_data,
    #                "compressor_excitation" : compressor_excitation_data}

    #     return bc_data

    def _get_acoustic_bc_from_string(self, str_value, label, folder_table_name):
        
        load_path_table = ""
        read_value = str_value[1:-1]
        output = None
        table_name = None
        self.frequencies = None

        if read_value != 'None':
            try:
                output = complex(read_value)
            except Exception:
                try:
                    folder_table_path = get_new_path(self._acoustic_imported_data_folder_path, folder_table_name)
                    load_path_table = get_new_path(folder_table_path, read_value)
                    table_file = open(load_path_table)
                    table_name = read_value

                    data = np.loadtxt(load_path_table, delimiter=",")
                    table_name = read_value
                    output = data[:,1] + 1j*data[:,2]
                    self.frequencies = data[:,0]
                    self.f_min = self.frequencies[0]
                    self.f_max = self.frequencies[-1]
                    self.f_step = self.frequencies[1] - self.frequencies[0]
                    
                    if self.f_min != 0:
                        self.non_zero_frequency_info = [False, self.f_min, read_value]
                    else:
                        self.zero_frequency = True
                    table_file.close()
                
                except Exception as log_error:
                    title = f"{label} - Error while loading table of values"
                    message = str(log_error) 
                    PrintMessageInput([window_title, title, message])       

        return output, table_name, self.frequencies

    def _get_structural_bc_from_string(self, first, last, labels, _complex=True, folder_table_name=""):
        
        first = first[1:-1].split(',')
        last = last[1:-1].split(',')
        output = [None, None, None, None, None, None]
        table_names = [None, None, None, None, None, None]
        list_frequencies = [None, None, None, None, None, None]

        if len(first)==3 and len(last)==3:
            for i in range(3):
                try:
                    if first[i] != 'None':
                        if _complex:
                            output[i] = complex(first[i])
                        else:
                            output[i] = float(first[i])
                    if last[i] != 'None':
                        if _complex:
                            output[i+3] = complex(last[i])
                        else:
                            output[i+3] = float(last[i])
                except Exception:
                    try:
                        output[i], list_frequencies[i] = self.structural_tables_load(first[i], labels[0][i], folder_table_name)
                        output[i+3], list_frequencies[i+3] = self.structural_tables_load(last[i], labels[1][i], folder_table_name)
                        if first[i] != 'None':
                            table_names[i] = first[i]
                        if last[i] != 'None':
                            table_names[i+3] = last[i] 
                    except Exception as err:
                        title = "ERROR WHILE LOADING STRUCTURAL MODEL INFO"
                        message = str(err)
                        PrintMessageInput([window_title, title, message])
                        return None, None, None
        return output, table_names, list_frequencies

    def structural_tables_load(self, table_name, label, folder_table_name):
        output = None
        
        labels = [  'm_x','m_y','m_z','Jx','Jy','Jz',
                    'k_x','k_y','k_z','k_rx','k_ry','k_rz',
                    'c_x','c_y','c_z','c_rx','c_ry','c_rz'  ]
               
        try:
            if table_name == "None":
                return None, None
            if folder_table_name != "":
                folder_table_path = get_new_path(self._structural_imported_data_folder_path, folder_table_name)
            else:
                folder_table_path = self._structural_imported_data_folder_path
            
            load_path_table = get_new_path(folder_table_path, table_name) 
            table_file = open(load_path_table)           
            header_read = table_file.readline()
            data = np.loadtxt(load_path_table, delimiter=",")

            if label in labels:
                output = data[:,1]
            else:
                output = data[:,1] + 1j*data[:,2]
            
            self.frequencies = data[:,0]
            self.f_min = self.frequencies[0]
            self.f_max = self.frequencies[-1]
            self.f_step = self.frequencies[1] - self.frequencies[0]
            
            if self.f_min != 0:
                self.non_zero_frequency_info = [False, self.f_min, table_name]
            else:
                self.zero_frequency = True
            if ('[m/s]' or '[rad/s]') in header_read:
                output = output/(2*pi*self.frequencies)
            elif ('[m/s²]' or '[rad/s²]') in header_read:
                output = output/((2*pi*self.frequencies)**2)
            
            table_file.close()

        except Exception: 

            title = "ERROR WHILE LOADING '{}' TABLE OF STRUCTURAL MODEL".format(label)
            message = "The loaded {} table has invalid data structure, \ntherefore, it will be ignored in analysis.".format(label)  
            PrintMessageInput([window_title, title, message]) 

        return output, self.frequencies

    def get_acoustic_bc_keys_to_remove(self, current_label):

        keys_to_remove = list()

        if "acoustic pressure" == current_label:
            keys_to_remove.append("volume velocity")
            keys_to_remove.append("compressor excitation -")

        elif "volume velocity" == current_label:
            keys_to_remove.append("acoustic pressure")
            keys_to_remove.append("compressor excitation -")

        elif "compressor excitation -" == current_label:
            keys_to_remove.append("acoustic pressure")
            keys_to_remove.append("volume velocity")

        elif "radiation impedance" == current_label:
            keys_to_remove.append("specific impedance")

        elif "specific impedance" == current_label:
            keys_to_remove.append("radiation impedance")

        return keys_to_remove

    def get_structural_bc_keys_to_remove(self, current_labels):

        keys_to_remove = list()
        if "displacements" in current_labels and "rotations" in current_labels:
            keys_to_remove = ["forces", "moments"]
        elif "forces" in current_labels and "moments" in current_labels:
            keys_to_remove = ["displacements", "rotations"]

        return keys_to_remove

    def filter_bc_data_from_dat_file(self, selection_key, bc_keys_to_remove, path):
        
        def internal_check(bc_label):
            for bc_key_to_remove in bc_keys_to_remove:
                if bc_label in bc_key_to_remove:
                    return True
            return False

        if path.exists():
            
            config_input = configparser.ConfigParser()
            config_output = configparser.ConfigParser()
            config_input.read(path)

            for key in config_input.sections():

                if "-" in key:
                    _key = key
                else:
                    _key = int(key)

                node_data = config_input[key]
                if _key not in selection_key:
                    config_output[key] = node_data

                else:

                    bc_data = dict()
                    for bc_key, value in node_data.items():

                        if internal_check(bc_key):
                            continue
                        else:
                            bc_data[bc_key] = value

                    if bc_data:
                        # if only "coords" exists ignore the section
                        if len(bc_data) > 1:
                            config_output[key] = bc_data

            if len(config_output.sections()):
                self.write_data_in_file(path, config_output)
            else:
                os.remove(path)

    def add_acoustic_bc_in_file(self, node_ids, data, label):

        preprocessor = app().main_window.project.preprocessor
        nodes = preprocessor.nodes

        path = self._node_acoustic_path
        bc_keys_to_remove = self.get_acoustic_bc_keys_to_remove(label[0])
        self.filter_bc_data_from_dat_file(node_ids, bc_keys_to_remove, path)

        config = configparser.ConfigParser()
        config.read(path)

        [value, table_name] = data

        for node_id in node_ids:

            if isinstance(node_id, str):

                if "-" not in node_id:
                    continue

                _nodes = [int(_id) for _id in node_id.split("-")]
                coords_1 = np.round(nodes[_nodes[0]].coordinates, 5)
                coords_2 = np.round(nodes[_nodes[1]].coordinates, 5)
                coords = np.concatenate((coords_1, coords_2)).flatten()
                # key = f"{_nodes[0]} - {_nodes[1]} - {list(coords_1)} - {list(coords_2)}"
                key = node_id

            elif isinstance(node_id, int):

                coords = np.round(nodes[node_id].coordinates, 5)
                # key = f"{node_id} - {list(coords)}"
                key = f"{node_id}"

            else:
                continue

            bc_key = label[0]
            if isinstance(table_name, str):
                _value = table_name
            else:
                _value = value

            if key in config.sections():
                config[key]["coords"] = f"{list(coords)}"
                config[key][bc_key] = f"[{_value}]"
            else:
                config[key] =  { "coords" : f"{list(coords)}",
                                   bc_key : f"[{_value}]" }

            self.write_data_in_file(path, config)

    def add_structural_bc_in_file(self, node_ids, values, labels):

        preprocessor = app().main_window.project.preprocessor
        nodes = preprocessor.nodes

        path = self._node_structural_path
        bc_keys_to_remove = self.get_structural_bc_keys_to_remove(labels)
        self.filter_bc_data_from_dat_file(node_ids, bc_keys_to_remove, path)

        config = configparser.ConfigParser()
        config.read(path)

        for node_id in node_ids:

            if isinstance(node_id, str):

                if "-" not in node_id:
                    continue

                _nodes = [int(_id) for _id in node_id.split("-")]
                coords_1 = np.round(nodes[_nodes[0]].coordinates, 5)
                coords_2 = np.round(nodes[_nodes[1]].coordinates, 5)
                coords = np.concatenate((coords_1, coords_2)).flatten()
                # key = f"{_nodes[0]} - {_nodes[1]} - {list(coords_1)} - {list(coords_2)}"

            elif isinstance(node_id, int):

                coords = np.round(nodes[node_id].coordinates, 5)
                # key = f"{node_id} - {list(coords)}"

            else:
                continue

            key = f"{node_id}"

            if key in config.sections():
                config[key]["coords"] = f"{list(coords)}"
                config[key][labels[0]]  = f"[{values[0]},{values[1]},{values[2]}]"
                config[key][labels[1]] = f"[{values[3]},{values[4]},{values[5]}]"

                if len(labels)==3:
                    config[key][labels[2]]  = f"{values[6]}"

            else:

                if len(labels)==3:
                    config[key] =  {     "coords" : f"{list(coords)}",
                                        labels[0] : f"[{values[0]},{values[1]},{values[2]}]",
                                        labels[1] : f"[{values[3]},{values[4]},{values[5]}]",
                                        labels[2] : f"{values[6]}"   }

                else:
                    config[key] =  {     "coords" : f"{list(coords)}",
                                        labels[0] : f"[{values[0]},{values[1]},{values[2]}]",
                                        labels[1] : f"[{values[3]},{values[4]},{values[5]}]"   }

            self.write_data_in_file(self._node_structural_path, config)

    def update_node_ids_after_mesh_changed(self):

        path_1 = self._node_acoustic_path
        path_2 = self._node_structural_path

        non_mapped_nodes = list()
        preprocessor = app().main_window.project.preprocessor

        print(path_1, path_2)
        return

        for path in [path_1, path_2]:
            if path.exists():

                config_input = configparser.ConfigParser()
                config_output = configparser.ConfigParser()
                config_input.read(path)

                for key in config_input.sections():

                    str_coords = config_input[key]["coords"]
                    _coords = get_list_of_values_from_string(str_coords, int_values=False)
                    coords = np.array(_coords)

                    if "-" in key:
                        coords_1 = coords[:3]
                        coords_2 = coords[3:]
                        new_node_id1 = preprocessor.get_node_id_by_coordinates(coords_1)
                        new_node_id2 = preprocessor.get_node_id_by_coordinates(coords_2)
                        new_key = f"{new_node_id1}-{new_node_id2}"

                        if new_node_id1 is None:
                            if new_node_id1 not in non_mapped_nodes:
                                non_mapped_nodes.append((key, coords))
                            continue

                        if new_node_id2 is None:
                            if new_node_id2 not in non_mapped_nodes:
                                non_mapped_nodes.append((key, coords))
                            continue

                    else:
                        new_node_id = preprocessor.get_node_id_by_coordinates(coords)
                        new_key = f"{new_node_id}"

                        if new_node_id is None:
                            if new_node_id not in non_mapped_nodes:
                                non_mapped_nodes.append((key, coords))
                            continue

                    # print(key, new_node_id)
                    config_output[new_key] = config_input[key]

                if len(config_output.sections()):
                    self.write_data_in_file(path, config_output)
                else:
                    os.remove(path)

        if non_mapped_nodes:
            print(f"List of non-mapped nodes: {non_mapped_nodes}")

        return non_mapped_nodes

    ## METHODS FOR *.json FILES

    # def _remove_bcs_from_json_file(self, node_ids, bc_keys_to_remove, path):

    #     def internal_check(bc_label):
    #         for bc_key_to_remove in bc_keys_to_remove:
    #             if bc_label in bc_key_to_remove:
    #                 return True
    #         return False

    #     if path.exists():
    #         with open(path) as file:
    #             read_data = json.load(file)

    #             output_data = dict()
    #             for key, node_data in read_data.items():

    #                 bc_node_id = int(key.split(" - ")[0])
    #                 print(bc_node_id)

    #                 if bc_node_id not in node_ids:
    #                     print("normal")
    #                     output_data[key] = node_data

    #                 else:
    #
    #                     bc_data = dict()
    #                     for bc_key, value in node_data.items():
    #                         print(bc_key, value)
    #                         if internal_check(bc_key):
    #
    #                             continue
    #                         else:
    #
    #                             bc_data[bc_key] = value

    #                     if bc_data:
    #                         output_data[key] = bc_data

    #         if output_data:
    #             with open(path, "w") as file:
    #                 json.dump(output_data, file, indent=2)
    #         else:
    #             os.remove(path)

    # def add_acoustic_bc_in_file(self, node_ids, data, label):

    #     [value, table_name] = data

    #     preprocessor = app().main_window.project.preprocessor
    #     nodes = preprocessor.nodes

    #     path = self._project_path / "acoustic_nodal_info.json"
    #     bc_keys_to_remove = self.get_acoustic_bc_keys_to_remove(label[0])
    #     self._remove_bcs_from_json_file(node_ids, bc_keys_to_remove, path)

    #     if path.exists():
    #         with open(path) as file:
    #             output_data = json.load(file)
    #     else:
    #         output_data = dict()

    #     for node_id in node_ids:

    #         coords = np.round(nodes[node_id].coordinates, 5)

    #         _key = label[0]
    #         if isinstance(table_name, str):
    #             _value = table_name
    #         else:
    #             _value = value

    #         key = f"{node_id} - {list(coords)}"
    #         if key in output_data.keys():
    #             output_data[key][_key] =  f"[{_value}]"
    #         else:
    #             output_data[key] = {_key: f"[{_value}]"}

    #     if output_data:
    #         with open(path, "w") as file:
    #             json.dump(output_data, file, indent=2)
    #     else:
    #         if path.exists():
    #             os.remove(path)

    # def add_structural_bc_in_file(self, node_ids, data, labels):

    #     preprocessor = app().main_window.project.preprocessor
    #     nodes = preprocessor.nodes

    #     path = self._project_path / "structural_nodal_info.json"
    #     bc_keys_to_remove = self.get_structural_bc_keys_to_remove(labels)
    #     self._remove_bcs_from_json_file(node_ids, bc_keys_to_remove, path)

    #     if path.exists():
    #         with open(path) as file:
    #             output_data = json.load(file)
    #     else:
    #         output_data = dict()

    #     for node_id in node_ids:

    #         coords = np.round(nodes[node_id].coordinates, 5)

    #         key = f"{node_id} - {list(coords)}"
    #         if key in output_data.keys():
                
    #             output_data[key][labels[0]] =  f"[{data[0]},{data[1]},{data[2]}]"
    #             output_data[key][labels[1]] =  f"[{data[3]},{data[4]},{data[5]}]"

    #             if len(labels)==3:
    #                 output_data[key][labels[2]]  = "{}".format(data[6])

    #         else:

    #             if len(labels)==3:
    #                 output_data[key] =  {   labels[0]: f"[{data[0]},{data[1]},{data[2]}]",
    #                                         labels[1]: f"[{data[3]},{data[4]},{data[5]}]",
    #                                         labels[2]: f"{data[6]}"   }
    #             else:
    #                 output_data[key] =  {   labels[0]: f"[{data[0]},{data[1]},{data[2]}]",
    #                                         labels[1]: f"[{data[3]},{data[4]},{data[5]}]"   }
    
    #     if output_data:
    #         with open(path, "w") as file:
    #             json.dump(output_data, file, indent=2)
    #     else:
    #         if path.exists():
    #             os.remove(path)

    # def update_node_ids_after_mesh_changed(self):

    #     path_1 = self._project_path / "acoustic_nodal_info.json"
    #     path_2 = self._project_path / "structural_nodal_info.json"

    #     non_mapped_nodes = list()
    #     preprocessor = app().main_window.project.preprocessor

    #     for path in [path_1, path_2]:
    #         if path.exists():

    #             with open(path) as file:
    #                 bc_info = json.load(file)

    #             if bc_info:
    #                 new_bc_info = dict()
    #                 for key, data in bc_info.items():

    #                     str_node_id, str_coords = key.split(" - ")
    #                     _coords = get_list_of_values_from_string(str_coords, int_values=False)
    #                     coords = np.array(_coords)
    #                     new_node_id = preprocessor.get_node_id_by_coordinates(coords)

    #                     if new_node_id is None:
    #                         non_mapped_nodes.append((int(str_node_id), coords))
    #                         continue

    #                     print(str_node_id, new_node_id)
    #                     new_key = f"{new_node_id} - {list(coords)}"
    #                     new_bc_info[new_key] = data

    #                 with open(path, "w") as file:
    #                     json.dump(new_bc_info, file, indent=2)

    #                 with open(path) as file:
    #                     read_data = json.load(file)

    #                 if read_data == {}:
    #                     os.remove(path)

    #     return non_mapped_nodes

    def check_if_table_can_be_removed_in_acoustic_model(self, input_id, str_key, table_name, 
                                                        folder_table_name, node_info=True, label=""):

        config = configparser.ConfigParser()
        if node_info:
            config.read(self._node_acoustic_path)
        else:
            config.read(self._element_info_path)

        sections = config.sections()
        str_input_id = str(input_id)
        if label == "":
            label = str_key.capitalize()

        for section in sections:
            if section != str_input_id:
                for key in config[section].keys():
                    if str_key in key:
                        str_value = config[section][key]
                        _, table_name_info_file, _ = self._get_acoustic_bc_from_string(str_value, label, folder_table_name)
                        if table_name_info_file == table_name:
                            return False
        return True

    def get_dict_of_compressor_excitation_from_file(self):
        config = configparser.ConfigParser()
        config.read(self._node_acoustic_path)
        sections = config.sections()
        dict_node_to_compressor_excitation = defaultdict(list)  
        for node_id in sections:
            keys = list(config[node_id].keys())
            for key in keys:
                if "compressor excitation - " in key:
                    table_file_name = config[node_id][key]
                    dict_node_to_compressor_excitation[int(node_id)].append([key, table_file_name])   
        return dict_node_to_compressor_excitation

    # def check_if_table_can_be_removed_in_structural_model(self, node_id, str_keys, table_name, folder_table_name, node_info=True, labels=["", ""]):
    #     config = configparser.ConfigParser()
    #     if node_info:
    #         config.read(self._node_structural_path)
    #     else:
    #         config.read(self._element_info_path)        
    #     sections = config.sections()
    #     str_node_id = str(node_id)
    #     if labels == ["", ""]:
    #         labels = [str_key.capitalize() for str_key in str_keys]

    #     list_table_names = list()
    #     for section in sections:
    #         if section != str_node_id:
    #             list_file_keys = list(config[section].keys()) 
    #             for str_key in str_keys:
    #                 if str_key in list_file_keys:
    #                     str_values_first = config[section][list_file_keys[0]]
    #                     str_values_last = config[section][list_file_keys[1]]
    #                     _, list_table_names_info_file = self._get_structural_bc_from_string(str_values_first,
    #                                                                                         str_values_last, 
    #                                                                                         labels, 
    #                                                                                         folder_table_name)
    #                     if table_name in list_table_names_info_file:
    #                         return False
    #                     break
    #                     # for table_name_info_file in list_table_names_info_file:
    #                     #     if table_name_info_file is not None:
    #                     #         if table_name_info_file == table_name:
    #                     #             return False                     
    #     return True


    # def remove_table_files_from_imported_data_folder_by_line(self, line_id):

    #     str_line_id = str(line_id)
    #     config = configparser.ConfigParser()
    #     config.read(self._pipeline_path)
    #     sections = config.sections()

    #     list_table_names = list()
    #     list_joint_stiffness = list()
    #     if str_line_id in sections:
    #         keys = list(config[str_line_id].keys())
    #         if 'expansion joint stiffness' in keys:
    #             read_joint_stiffness = config[str_line_id]['expansion joint stiffness']
    #             list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
    #             cache_section = str_line_id
        
    #     if list_joint_stiffness == list():
    #         return

    #     for stiffness_value in list_joint_stiffness:
    #         try:
    #             float(stiffness_value)
    #             return
    #         except:
    #             break
        
    #     list_table_multiple_joints = list()
    #     list_table_names = list_joint_stiffness
        
    #     for section in sections:
    #         if section != cache_section:
    #             keys = list(config[section].keys())
    #             if 'expansion joint stiffness' in keys:
    #                 read_table_names = config[section]['expansion joint stiffness']
    #                 for table_name in list_table_names:
    #                     if table_name in read_table_names:
    #                         list_table_multiple_joints.append(table_name)
        
    #     if len(list_table_multiple_joints)==0:
    #         self.confirm_table_file_removal(list_table_names)

    # def modify_node_ids_in_acoustic_bc_file(self, dict_old_to_new_indexes, dict_non_mapped_indexes):
    #     if os.path.exists(self._node_acoustic_path):
    #         config = configparser.ConfigParser()
    #         config.read(self._node_acoustic_path)
    #         for node_id in list(config.sections()):
    #             try:
    #                 new_key = str(dict_old_to_new_indexes[node_id])
    #                 if node_id != new_key:
    #                     config[new_key] = config[node_id]
    #                     config.remove_section(node_id)
    #             except Exception as log_error:
    #                 config.remove_section(node_id)
    #         self.write_data_in_file(self._node_acoustic_path, config)


    # def modify_node_ids_in_structural_bc_file(self, dict_old_to_new_indexes, dict_non_mapped_nodes):
    #     if os.path.exists(self._node_structural_path):

    #         config = configparser.ConfigParser()
    #         config_new = configparser.ConfigParser()
    #         config.read(self._node_structural_path)
    #         sections = list(config.sections())
            
    #         for section in sections:
    #             try:
    #                 if section not in dict_non_mapped_nodes.values():     
    #                     if "-" in section:
    #                         [_node_id1, _node_id2]  = section.split("-")
    #                         key_id1 = str(dict_old_to_new_indexes[_node_id1])
    #                         key_id2 = str(dict_old_to_new_indexes[_node_id2])
    #                         new_key = f"{key_id1}-{key_id2}"
    #                     else:
    #                         new_key = str(dict_old_to_new_indexes[section])
    #                         # if section != new_key:
    #                         #     config2[new_key] = config[section]
    #                         #     config.remove_section(section)   
    #                     if section != new_key:
    #                         config_new[new_key] = config[section]
    #                         # config.remove_section(section)
    #                     else:
    #                         config_new[section] = config[section]                     
                
    #             except Exception as log_error:
    #                 config.remove_section(section)
            
    #         self.write_data_in_file(self._node_structural_path, config_new)


    def modify_list_of_element_ids_in_entity_file(self, dict_group_elements_to_update_after_remesh, dict_non_mapped_subgroups_entity_file):
        """ This method updates the lists of elements in entity file after remesh process. A mapping process checks the boundaries of the
            attribution before and after meshing process. If the mapping process could not find boundaries of atribution after remesh, 
            so the all attribuiton from line related to the group of elements will be removed.
        
        """
        if os.path.exists(self._pipeline_path):
            config = configparser.ConfigParser()
            config.read(self._pipeline_path)
            sections = config.sections()
            
            for section in sections:
                if section in config.sections():
                    if 'list of elements' in config[section].keys():
                        str_list_elements = config[section]['list of elements']
                        list_elements = get_list_of_values_from_string(str_list_elements)
                        list_subgroup_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)
                        temp_list = list()
                        lines_to_reset = list()
                        try:

                            for subgroup_elements in list_subgroup_elements:
                                str_subgroup_elements = str(subgroup_elements)
                                if str_subgroup_elements in dict_group_elements_to_update_after_remesh.keys():
                                    temp_list.append(dict_group_elements_to_update_after_remesh[str_subgroup_elements])
                                elif str_subgroup_elements in dict_non_mapped_subgroups_entity_file.keys():
                                    lines_to_reset.append(section)    

                            if lines_to_reset:
                                for line_to_reset in lines_to_reset:
                                    prefix = line_to_reset.split("-")[0] + "-"
                                    for _section in sections:
                                        if prefix in _section:
                                            config.remove_section(section=_section)
                            elif temp_list:
                                new_list_elements = [value for group in temp_list for value in group]
                                config[section]['list of elements'] =  str(new_list_elements)
                            else:
                                config.remove_section(section=section)

                        except Exception as log_error:

                            if "-" in section:
                                line_id = section.split("-")[0]
                                subkey = f"{line_id}-"
                                config.remove_section(section)
                                if line_id in sections:
                                    for key in config[line_id].keys():                                                     
                                        # for key in config[line_id].keys():
                                        config.remove_option(section=line_id, option=key)
                                for _section in sections:
                                    if subkey in _section:
                                        config.remove_section(_section)       

            self.write_data_in_file(self._pipeline_path, config)


    def modify_element_ids_in_element_info_file(self, dict_old_to_new_subgroups_elements, dict_non_mapped_subgroups, dict_list_elements_to_subgroups):
        config = configparser.ConfigParser()
        config.read(self._element_info_path)
        sections = config.sections()
        
        for section in sections:
            if 'list of elements' in config[section].keys():
                
                str_list_elements = config[section]['list of elements']
                list_subgroups_elements = dict_list_elements_to_subgroups[str_list_elements]

                temp_list = list()
                try:

                    for subgroup_elements in list_subgroups_elements:
                        str_group_elements = str(subgroup_elements)
                        if str_group_elements not in dict_non_mapped_subgroups.keys():
                            temp_list.append(dict_old_to_new_subgroups_elements[str(subgroup_elements)])
                    
                    if temp_list:
                        new_list_elements = [value for group in temp_list for value in group]
                        config[section]['list of elements'] =  str(new_list_elements)
                    else:
                        config.remove_section(section)

                except:
                    
                    config.remove_section(section) 

        self.write_data_in_file(self._element_info_path, config)

    def modify_beam_xaxis_rotation_by_lines_in_file(self, line_id, value):
        _line_id = str(line_id)
        config = configparser.ConfigParser()
        config.read(self._pipeline_path)
        if _line_id in list(config.sections()):
            if value == 0:
                if "beam x-axis rotation" in list(config[_line_id].keys()):
                    config.remove_option(section=str(_line_id), option="beam x-axis rotation")
            else:                    
                config[_line_id]["beam x-axis rotation"] = str(value)               
            self.write_data_in_file(self._pipeline_path, config)

    def write_data_in_file(self, path, config):
        with open(path, 'w') as config_file:
            config.write(config_file)

    def get_import_type(self):
        return self._import_type

    @property
    def project_name(self):
        return self._project_name
    
    @property
    def project_ini_name(self):
        return self._project_ini_name
    
    @property
    def project_path(self):
        return self._project_path

    @property
    def project_ini_file_path(self):
        return self._project_ini_file_path

    @property
    def geometry_path(self):
        return self._geometry_path
    
    @property
    def length_unit(self):
        return self._length_unit
    
    @property
    def element_size(self):
        return self._element_size

    @property
    def geometry_tolerance(self):
        return self._geometry_tolerance

    # def update_list_elements_already_exists_in_entity_file(self, line_id, config, ext_list_elements):
    #     dict_section_to_list_elements = {}
    #     sections = config.sections()
    #     prefix = f"{line_id}-"
    #     for section in sections:
    #         if prefix in section:
    #             if 'list of elements' in config[section].keys():
    #                 str_list_elements = config[section]['list of elements']
    #                 old_list_elements = get_list_of_values_from_string(str_list_elements)
    #                 new_list_elements = list()
    #                 temp_list = old_list_elements.copy()
    #                 for element_id in temp_list:
    #                     if element_id not in ext_list_elements:
    #                         new_list_elements.append(element_id)
    #                 config[section]['list of elements'] = str(new_list_elements)


def normalize(prop: dict):
    """
    Sadly json doesn't accepts tuple keys,
    so we need to convert it to a string like:
    "property id" = value
    """
    return {f"{p} {i}": v for (p, i), v in prop.items()}


def denormalize(prop: dict):
    new_prop = dict()
    for key, val in prop.items():
        p, i = key.split()
        p = p.strip()
        i = int(i)
        new_prop[p, i] = val
    return new_prop