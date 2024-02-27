from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection, get_beam_section_properties
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.perforated_plate import PerforatedPlate
from pulse.interface.user_input.project.printMessageInput import PrintMessageInput
from pulse.tools.utils import *
from pulse import app

from opps.model import Pipe, Bend, Point

import os
import configparser
import numpy as np
from math import pi

from collections import defaultdict
from shutil import copyfile, rmtree
from pathlib import Path

window_title = "Error"

class ProjectFile:
    def __init__(self):
        self.reset()

    def reset(self):
        self._project_name = ""
        self._import_type = 0
        self._section = 0
        self._length_unit = "meter"
        self._element_size = 0.01 # default value to the element size (in meters)
        self._project_path = ""
        self._material_list_path = ""
        self._fluid_list_path = ""
        self._geometry_path = ""
        self._geometry_filename = ""
        self._geometry_tolerance = 1e-8 # default value to gmsh geometry tolerance (in milimeters)
        self._entity_path = ""
        self._segment_path = ""
        self._backup_geometry_path = ""
        self._node_structural_path = ""
        self._node_acoustic_path = ""
        self._element_info_path = ""
        self._analysis_path = ""
        self.element_type_is_structural = False
        self.default_filenames()
        self.reset_frequency_setup()

    def reset_frequency_setup(self):
        self.f_min = None
        self.f_max = None
        self.f_step = None
        self.non_zero_frequency_info = []
        self.zero_frequency = False

    def default_filenames(self):
        self._entity_file_name = "entity.dat"
        self._segment_file_name = "segment_data.dat"
        self._material_file_name = "material_list.dat"
        self._fluid_file_name = "fluid_list.dat"
        self._geometry_entities_file_name = "geometry_entities.dat"
        self._node_structural_file_name = "structural_nodal_info.dat"
        self._node_acoustic_file_name = "acoustic_nodal_info.dat"
        self._elements_file_name = "elements_info.dat"
        self._project_base_name = "project.ini"
        self._imported_data_folder_name = "imported_data"
        self._backup_geometry_foldername = "geometry_backup"

    def get_list_filenames_to_maintain_after_reset(self):
        files_to_maintain_after_reset = []
        files_to_maintain_after_reset.append(self._project_base_name)
        files_to_maintain_after_reset.append(self._material_file_name)
        files_to_maintain_after_reset.append(self._fluid_file_name)
        files_to_maintain_after_reset.append(self._geometry_entities_file_name)
        if os.path.exists(self._geometry_path):
            files_to_maintain_after_reset.append(os.path.basename(self._geometry_path))
        return files_to_maintain_after_reset

    def new(self, 
            project_path, 
            project_name,
            length_unit, 
            element_size, 
            geometry_tolerance, 
            import_type, 
            material_list_path, 
            fluid_list_path, 
            geometry_path = ""):

        self._project_path = project_path
        self._project_name = project_name
        self._length_unit = length_unit
        self._element_size = float(element_size)
        self._geometry_tolerance = float(geometry_tolerance)
        self._import_type = int(import_type)
        self._material_list_path = material_list_path
        self._fluid_list_path = fluid_list_path
        if geometry_path != "":
            self._geometry_path = geometry_path
        self._project_ini_file_path = get_new_path(self._project_path, self._project_base_name)
        self._entity_path = get_new_path(self._project_path, self._entity_file_name)
        self._segment_path = get_new_path(self._project_path, self._segment_file_name)
        self._node_structural_path = get_new_path(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path = get_new_path(self._project_path, self._node_acoustic_file_name)
        self._element_info_path = get_new_path(self._project_path, self._elements_file_name)
        self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
        self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
        self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")
        self._backup_geometry_path = get_new_path(self._project_path, "geometry_backup")
    
    def copy(self, project_path, project_name, material_list_path, fluid_list_path, geometry_path = "", coord_path = "", conn_path = ""):
        self._project_path = project_path
        self._project_name = project_name
        self._material_list_path = material_list_path
        self._fluid_list_path = fluid_list_path
        self._geometry_path = geometry_path
        self._project_ini_file_path = get_new_path(self._project_path, self._project_base_name)
        self._entity_path = get_new_path(self._project_path, self._entity_file_name)
        self._segment_path = get_new_path(self._project_path, self._segment_file_name)
        self._node_structural_path = get_new_path(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path = get_new_path(self._project_path, self._node_acoustic_file_name)
        self._element_info_path = get_new_path(self._project_path, self._elements_file_name)
        self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
        self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
        self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")
        self._backup_geometry_path = get_new_path(self._project_path, "geometry_backup")

    def get_file_path_inside_project_directory(self, filename):
        return get_new_path(self._project_path, filename)

    def get_element_size_from_project_file(self):
        if self._project_path != "":
            config = configparser.ConfigParser()
            config.read(self._project_ini_file_path)
            if 'element size' in config['PROJECT'].keys():
                element_size = config['PROJECT']['element size']
                if element_size != "":
                    return float(element_size)
            else:
                return ""

    def get_mesh_attributes_from_project_file(self):
        element_size = None
        geometry_tolerance = None
        if self._project_path != "":
            config = configparser.ConfigParser()
            config.read(self.project_ini_file_path)
            keys = config['PROJECT'].keys()
            if 'element size' in keys:
                str_element_size = config['PROJECT']['element size']
                if str_element_size != "":
                    element_size = float(str_element_size)
            if 'geometry tolerance' in keys:
                str_geometry_tolerance = config['PROJECT']['geometry tolerance']
                if str_geometry_tolerance != "":
                    geometry_tolerance = float(str_geometry_tolerance)
            return element_size, geometry_tolerance
        else:
            return None, None

    def get_geometry_entities_path(self):
        return get_new_path(self._project_path, self._geometry_entities_file_name)

    def create_backup_geometry_folder(self):
        """ This method creates a backup geometry folder if it was not create yet. Additionally, a geometry file copy
            is pasted inside geometry backup folder just after its creation. This geometry file will be used in resetting
            geometry process.
        """
        if not os.path.exists(self._backup_geometry_path):
            os.mkdir(self._backup_geometry_path)

        if os.path.exists(self._geometry_path):
            basename = os.path.basename(self._geometry_path)
            if basename != "":
                new_geometry_path = get_new_path(self._backup_geometry_path, basename)
                copyfile(self._geometry_path, new_geometry_path)

    def update_geometry_path(self, geometry_path):
        self._geometry_path = geometry_path

    def load(self, project_file_path):

        self.project_file_path = Path(project_file_path)
        self._project_path = os.path.dirname(self.project_file_path)

        config = configparser.ConfigParser()
        config.read(project_file_path)

        section = config['PROJECT']
        project_name = section['name']
        import_type = int(section['import type'])

        keys = list(section.keys())

        if import_type in [0, 1]:

            if 'length unit' in keys:
                self._length_unit = section['length unit']

            if 'geometry file' in keys:
                geometry_file = section['geometry file']
                self._geometry_path =  get_new_path(self._project_path, geometry_file)

            if 'element size' in keys:
                element_size = section['element size']
                self._element_size = float(element_size)

            if 'geometry tolerance' in keys:
                geometry_tolerance = section['geometry tolerance']
                self._geometry_tolerance = float(geometry_tolerance)

        material_list_file = section['material list file']
        fluid_list_file = section['fluid list file']

        self._project_name = project_name
        self._import_type = import_type
        self._project_ini_file_path = get_new_path(self._project_path, self._project_base_name)
        self._material_list_path = get_new_path(self._project_path, material_list_file)
        self._fluid_list_path =  get_new_path(self._project_path, fluid_list_file)
        self._entity_path =  get_new_path(self._project_path, self._entity_file_name)
        self._segment_path = get_new_path(self._project_path, self._segment_file_name)
        self._element_info_path =  get_new_path(self._project_path, self._elements_file_name)
        self._node_structural_path =  get_new_path(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path =  get_new_path(self._project_path, self._node_acoustic_file_name)
        self._imported_data_folder_path = get_new_path(self._project_path, self._imported_data_folder_name)
        self._structural_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "structural")
        self._acoustic_imported_data_folder_path = get_new_path(self._imported_data_folder_path, "acoustic")
        self._backup_geometry_path = get_new_path(self._project_path, "geometry_backup")

    def update_project_attributes(self, **kwargs):

        length_unit = kwargs.get('length_unit', None)
        element_size = kwargs.get('element_size', None)
        geometry_tolerance = kwargs.get('geometry_tolerance', None)
        geometry_filename = kwargs.get('geometry_filename', None)
        
        config = configparser.ConfigParser()
        config.read(self._project_ini_file_path)

        section = config['PROJECT']
        keys = section.keys()

        if length_unit is not None:
            section['Length unit'] = length_unit

        if element_size is not None:
            if 'element size' in keys: 
                read_element_size = section['element size']
                if read_element_size != str(element_size):
                    section['element size'] = str(element_size)
            else:
                section['element size'] = str(element_size)
        
        if geometry_tolerance is not None:
            section['geometry tolerance'] = str(geometry_tolerance)

        if geometry_filename is not None:
            section['geometry file'] = geometry_filename

        self.write_data_in_file(self._project_ini_file_path, config)
        self.load(self._project_ini_file_path)

    def add_geometry_entities_to_file(self, entities_data):
        
        geometry_file_path = self.get_geometry_entities_path()
        config = configparser.ConfigParser()
        config.read(geometry_file_path)

        if len(entities_data["points_data"]) > 0:
            config['Points'] = entities_data["points_data"]
        else:
            if 'Points' in config.sections():
                config.remove_section('Points')
        
        if len(entities_data["lines_data"]) > 0:
            config['Lines'] = entities_data["lines_data"]
        else:
            if 'Lines' in config.sections():
                config.remove_section('Lines')

        if len(entities_data["fillets_data"]) > 0:
            config['Fillets'] = entities_data["fillets_data"]
        else:
            if 'Fillets' in config.sections():
                config.remove_section('Fillets')

        self.write_data_in_file(geometry_file_path, config)
        
    def load_geometry_entities_file(self):

        geometry_file_path = self.get_geometry_entities_path()
        if os.path.exists(geometry_file_path):
            config = configparser.ConfigParser()
            config.read(geometry_file_path)
            sections = config.sections()
            entities_data = {}

            if 'Points' in sections:
                points_data = {}
                keys = list(config['Points'].keys())
                for key in keys:
                    points_data[int(key)] = get_list_of_values_from_string(config['Points'][key], int_values=False)
                entities_data['points_data'] = points_data   

            if 'Lines' in sections:
                lines_data = {}
                keys = list(config['Lines'].keys())
                for key in keys:
                    lines_data[int(key)] = get_list_of_values_from_string(config['Lines'][key])
                entities_data['lines_data'] = lines_data 

            if 'Fillets' in sections:
                fillets_data = {}
                keys = list(config['Fillets'].keys())
                for key in keys:
                    fillets_data[int(key)] = get_list_of_values_from_string(config['Fillets'][key], int_values=False)
                entities_data['fillets_data'] = fillets_data 
            
            return entities_data
        else:
            return None

    #Frequency Setup Analysis
    def load_analysis_file(self):

        f_min = 0
        f_max = 0
        f_step = 0
        alpha_v, beta_v = 0, 0
        alpha_h, beta_h = 0, 0
        
        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        sections = config.sections()
        
        if "Frequency setup" in sections:
            keys = list(config['Frequency setup'].keys())
            if "frequency min" in keys and "frequency max" in keys and "frequency step" in keys:
                f_min = config['Frequency setup']['frequency min']
                f_max = config['Frequency setup']['frequency max']
                f_step = config['Frequency setup']['frequency step']

        if "Global damping setup" in sections:
            keys = list(config['Global damping setup'].keys())
            if "alpha_v" in keys and "beta_v" in keys and "alpha_h" in keys and "beta_h" in keys:
                alpha_v = config['Global damping setup']['alpha_v']
                beta_v = config['Global damping setup']['beta_v']
                alpha_h = config['Global damping setup']['alpha_h']
                beta_h = config['Global damping setup']['beta_h']
        
        global_damping = [float(alpha_v),float(beta_v),float(alpha_h),float(beta_h)]

        return float(f_min), float(f_max), float(f_step), global_damping

    def load_visibility_preferences_file(self):

        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        sections = config.sections()

        preferences = {}
        if "User interface preferences" in sections:

            #temporary default preferences to maintain compatibility with the other versions
            background_color = '(1,1,1)'
            font_color = '(0,0,0)'
            nodes_color = '(255,255,63)'
            lines_color = '(255,255,255)'
            surfaces_color = '(255,255,255)'
            transparency = 0.8
            OpenPulse_logo = '1'
            mopt_logo = '1'
            reference_scale = '1'

            config_preferences = config['User interface preferences']
            keys = config_preferences.keys() 
            if 'background color' in keys:
                background_color = config_preferences['background color']
            if 'font color' in keys:
                font_color = config_preferences['font color']
            if 'nodes color' in keys:
                nodes_color = config_preferences['nodes color']
            if 'lines color' in keys:
                lines_color = config_preferences['lines color']
            if 'surfaces color' in keys:
                surfaces_color = config_preferences['surfaces color']
            if 'transparency' in keys:
                transparency = float(config_preferences['transparency'])
            if 'openpulse logo' in keys:
                OpenPulse_logo = config_preferences['openpulse logo']
            if 'mopt logo' in keys:
                mopt_logo = config_preferences['mopt logo']
            if 'reference scale' in keys:
                reference_scale = config_preferences['reference scale']
    
            background_color = background_color[1:-1].split(",")
            background_color = tuple([float(val) for val in background_color])
            
            font_color = font_color[1:-1].split(",")
            font_color = tuple([float(val) for val in font_color])

            nodes_color = nodes_color[1:-1].split(",")
            nodes_color = tuple([float(val) for val in nodes_color])

            lines_color = lines_color[1:-1].split(",")
            lines_color = tuple([float(val) for val in lines_color])

            surfaces_color = surfaces_color[1:-1].split(",")
            surfaces_color = tuple([float(val) for val in surfaces_color])
        
            preferences = { 'background_color' : background_color,
                            'font_color' : font_color,
                            'nodes_color' :  nodes_color,
                            'lines_color' : lines_color,
                            'surfaces_color' : surfaces_color,
                            'transparency' : transparency,
                            'OpenPulse_logo' : bool(int(OpenPulse_logo)),
                            'mopt_logo' : bool(int(mopt_logo)),
                            'reference_scale' : bool(int(reference_scale)) }
        
        return preferences

    def add_frequency_in_file(self, min_, max_, step_):
        min_ = str(min_)
        max_ = str(max_)
        step_ = str(step_)
        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        # sections = config.sections()
        config["Frequency setup"] = {}
        config['Frequency setup']['frequency min'] = min_
        config['Frequency setup']['frequency max'] = max_
        config['Frequency setup']['frequency step'] = step_

        self.write_data_in_file(temp_project_base_file_path, config)

    def add_damping_in_file(self, global_damping):

        alpha_v = str(global_damping[0])
        beta_v = str(global_damping[1])
        alpha_h = str(global_damping[2])
        beta_h = str(global_damping[3])
        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)

        config['Global damping setup'] = {}
        config['Global damping setup']['alpha_v'] = alpha_v
        config['Global damping setup']['beta_v'] = beta_v
        config['Global damping setup']['alpha_h'] = alpha_h
        config['Global damping setup']['beta_h'] = beta_h

        self.write_data_in_file(temp_project_base_file_path, config)

    def reset_project_setup(self):

        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        sections = config.sections()

        if "Frequency setup" in sections:
            config.remove_section("Frequency setup")

        if "Global damping setup" in sections:
            config.remove_section("Global damping setup")

        self.write_data_in_file(temp_project_base_file_path, config)

    def add_user_preferences_to_file(self, preferences):

        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)

        config['User interface preferences'] = preferences
        
        self.write_data_in_file(temp_project_base_file_path, config)
        
    def add_inertia_load_setup_to_file(self, gravity, stiffening_effect):
        
        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)

        key_effect = int(stiffening_effect)

        config['Inertia load setup'] = {'gravity' : list(gravity),
                                        'stiffening_effect' : key_effect}

        self.write_data_in_file(temp_project_base_file_path, config)

    def load_inertia_load_setup(self):

        temp_project_base_file_path =  get_new_path(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        sections = config.sections()
        
        gravity = np.zeros(DOF_PER_NODE_STRUCTURAL, dtype=float)
        key_stiffening = 0
        
        if 'Inertia load setup' in sections:
            section = config['Inertia load setup']
            if 'gravity' in section.keys():
                gravity = get_list_of_values_from_string(section['gravity'], int_values=False)
            if 'stiffening_effect' in section.keys():
                key_stiffening = int(section['stiffening_effect'])

        return np.array(gravity, dtype=float), bool(key_stiffening)

    def create_entity_file(self, entities):

        if isinstance(entities, (int, float)):
            entities = [entities]

        config = configparser.ConfigParser()
        
        if os.path.exists(self._entity_path):
            sections = config.sections()
            for entity_id in entities:
                if str(entity_id) not in sections:
                    config[str(entity_id)] = {}
        else:
            for entity_id in entities:
                config[str(entity_id)] = {}
        
        self.write_data_in_file(self._entity_path, config)

    def create_segment_file(self, segments):

        if isinstance(segments, (int, float)):
            segments = [segments]

        config = configparser.ConfigParser()
        
        if os.path.exists(self._segment_path):
            config.read(self._segment_path)
            sections = config.sections()
            for segment_id in segments:
                if str(segment_id) not in sections:
                    config[str(segment_id)] = {}
        else:
            for segment_id in segments:
                config[str(segment_id)] = {}
        
        self.write_data_in_file(self._segment_path, config)

    def update_entity_file(self, entities, dict_map_lines={}):

        try:
            
            if os.path.exists(self._entity_path):

                config = configparser.ConfigParser()
                config2 = configparser.ConfigParser()
                config2.read(self._entity_path)
                sections = config2.sections()

                mapped_entities = []
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
            
                self.write_data_in_file(self._entity_path, config)

        except Exception as _error:
            print(str(_error))

    def get_entity_file_data(self):

        entity_data = {}
        config = configparser.ConfigParser()
        config.read(self._entity_path)

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
            entityFile.read(self._entity_path)
            sections = entityFile.sections()
            section_info = {}
            parameters_to_entity_id = defaultdict(list)
            parameters_to_elements_id = {}
            variable_section_line_ids = []
            _id = 1

            for entity in sections:

                line_prefix = ""
                list_elements = []
                outerDiameter = ""
                thickness = ""

                if 'structural element type' in entityFile[entity].keys():
                    
                    structural_element_type = entityFile[entity]['structural element type']
                    if structural_element_type == 'pipe_1':

                        if 'variable section parameters' in entityFile[entity].keys():
                            if line_prefix not in variable_section_line_ids:
                                variable_section_line_ids.append(entity)
                        
                        if "-" in entity:
                            line_prefix = entity.split("-")[0]
                            if line_prefix in variable_section_line_ids:
                                continue
                            elif 'list of elements' in entityFile[entity].keys():
                                str_list_elements = entityFile[entity]['list of elements']
                                list_elements = get_list_of_values_from_string(str_list_elements)

                        if 'outer diameter' in entityFile[entity].keys():
                            outerDiameter = entityFile[entity]['outer diameter']
                        
                        if 'thickness' in entityFile[entity].keys():
                            thickness = entityFile[entity]['thickness']
                        
                        if 'offset [e_y, e_z]' in entityFile[entity].keys():
                            offset = entityFile[entity]['offset [e_y, e_z]']
                            offset_y, offset_z = self._get_offset_from_string(offset) 
                        
                        if 'insulation thickness' in entityFile[entity].keys():
                            insulation_thickness = entityFile[entity]['insulation thickness']
                        
                        if 'insulation density' in entityFile[entity].keys():
                            insulation_density = entityFile[entity]['insulation density']
            
                        if outerDiameter != "" and thickness != "":
                            outerDiameter = float(outerDiameter)
                            thickness = float(thickness)
                            offset_y = float(offset_y)
                            offset_z = float(offset_z)
                            insulation_thickness = float(insulation_thickness)
                            insulation_density = float(insulation_density)
                            section_parameters = [outerDiameter, thickness, offset_y, offset_z, insulation_thickness, insulation_density]
                        
                        if 'section parameters' in entityFile[entity].keys():
                            str_section_parameters = entityFile[entity]['section parameters']
                            section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)                  
                    
                        if 'variable section parameters' in entityFile[entity].keys():
                            str_section_variable_parameters = entityFile[entity]['variable section parameters']
                            section_parameters = get_list_of_values_from_string(str_section_variable_parameters, int_values=False)                  
                    
                    elif 'beam section type' in entityFile[entity].keys():
                            section_type = entityFile[entity]['beam section type']
                            structural_element_type = f"beam_1 - {section_type}"
                            if section_type == "Generic section":   
                                continue              
                            else:
                                if 'section parameters' in entityFile[entity].keys():
                                    str_section_parameters = entityFile[entity]['section parameters']
                                    section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)

                    str_section_parameters = str(section_parameters)
                    if str_section_parameters not in parameters_to_entity_id.keys():
                        section_info[_id] = [structural_element_type, section_parameters]
                        _id += 1
                    
                    if line_prefix == "":
                        parameters_to_entity_id[str_section_parameters].append(int(entity))
                    else:   
                        if list_elements == []:
                            parameters_to_entity_id[str_section_parameters].append(int(entity)) 
                        else:
                            if str_section_parameters not in parameters_to_elements_id.keys():
                                parameters_to_elements_id[str_section_parameters] = list_elements
            
            section_info_elements = {}
            section_info_lines = {}
            id_1 = 0
            id_2 = 0
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
            message = "An error has been reached while processing the 'get_cross_sections_from_file' method.\n\n"
            message += f"Last line id: {entity}\n\n"
            message += f"Details: \n\n {str(error_log)}"
            PrintMessageInput([title, message, window_title])
            return {}, {}
    
        return section_info_lines, section_info_elements
                    
    def get_dict_of_entities_from_file(self):

        material_list = configparser.ConfigParser()
        material_list.read(self._material_list_path)

        fluid_list = configparser.ConfigParser()
        fluid_list.read(self._fluid_list_path)

        entityFile = configparser.ConfigParser()
        entityFile.read(self._entity_path)

        element_file = configparser.ConfigParser()
        element_file.read(self._element_info_path)
   
        self.dict_material = {}
        self.dict_cross = {}
        self.dict_variable_sections = {}
        self.dict_expansion_joint_parameters = {}
        self.dict_expansion_joint_sections = {}
        self.dict_valve = {}
        self.dict_valve_sections = {}
        self.dict_beam_xaxis_rotation = {}
        self.dict_structural_element_type = {}
        self.dict_structural_element_force_offset = {}
        self.dict_structural_element_wall_formulation = {}
        self.dict_acoustic_element_type = {}
        self.dict_fluid = {}
        self.compressor_info = {}
        self.dict_length_correction = {}
        self.dict_perforated_plate = {}
        self.temp_dict = {}
        self.dict_stress_stiffening = {}
        self.dict_capped_end = defaultdict(list)
        self.dict_B2XP_rotation_decoupling = {}

        window_title = "Error"
        title = "Error while loading data from project file"
        
        for entity in entityFile.sections():

            structural_element_type = ""
            acoustic_element_type = ""
            list_elements = ""

            if 'structural element type' in entityFile[entity].keys():
                structural_element_type = entityFile[entity]['structural element type']
                if structural_element_type != "":
                    if 'list of elements' in entityFile[entity].keys():
                        if "-" in entity:
                            str_list_elements = entityFile[entity]['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)
                            self.dict_structural_element_type[entity] = [list_elements, structural_element_type]
                    else:
                        self.dict_structural_element_type[entity] = structural_element_type
                    self.element_type_is_structural = True
                else:
                    self.dict_structural_element_type[entity] = 'pipe_1'
       
            if 'structural element wall formulation' in entityFile[entity].keys():
                wall_formulation = entityFile[entity]['structural element wall formulation']
                if wall_formulation != "":
                    if "-" in entity:
                        if 'list of elements' in entityFile[entity].keys():
                            str_list_elements = entityFile[entity]['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)
                            self.dict_structural_element_wall_formulation[entity] = [list_elements, wall_formulation]
                    else:
                        self.dict_structural_element_wall_formulation[entity] = wall_formulation
                    self.element_type_is_structural = True
                else:
                    self.dict_structural_element_wall_formulation[entity] = 'thick_wall'

            if 'force offset' in entityFile[entity].keys():
                force_offset = entityFile[entity]['force offset']
                if force_offset != "":
                    if "-" in entity:
                        if 'list of elements' in entityFile[entity].keys():
                            str_list_elements = entityFile[entity]['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)
                            self.dict_structural_element_force_offset[entity] = [list_elements, int(force_offset)]
                    else:
                        self.dict_structural_element_force_offset[entity] = int(force_offset)
                    self.element_type_is_structural = True
                else:
                    self.dict_structural_element_force_offset[entity] = None

            if 'acoustic element type' in entityFile[entity].keys():
                acoustic_element_type = entityFile[entity]['acoustic element type']
                if acoustic_element_type != "":
                    if acoustic_element_type == 'proportional':
                        proportional_damping = entityFile[entity]['proportional damping']
                        self.dict_acoustic_element_type[int(entity)] = [acoustic_element_type, float(proportional_damping), None]
                    elif acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                        vol_flow = entityFile[entity]['volume flow rate']
                        self.dict_acoustic_element_type[int(entity)] = [acoustic_element_type, None, float(vol_flow)]
                    else:
                        self.dict_acoustic_element_type[int(entity)] = [acoustic_element_type, None, None]
                    self.element_type_is_acoustic = True
                else:
                    self.dict_acoustic_element_type[int(entity)] = 'undamped'

            if 'compressor info' in entityFile[entity].keys():
                str_compressor_info = entityFile[entity]['compressor info']
                _data = get_list_of_values_from_string(str_compressor_info, int_values=False)
                self.compressor_info[int(entity)] = {   "temperature (suction)" : _data[0],
                                                        "pressure (suction)" : _data[1],
                                                        "line_id" : int(_data[2]),
                                                        "node_id" : int(_data[3]),
                                                        "pressure ratio" : _data[4],
                                                        "connection type" : int(_data[5])   }
                                           
            str_joint_parameters = ""
            if 'expansion joint parameters' in entityFile[entity].keys():
                str_joint_parameters = entityFile[entity]['expansion joint parameters']
                joint_parameters = get_list_of_values_from_string(str_joint_parameters, int_values=False)

            str_joint_stiffness = ""
            if 'expansion joint stiffness' in entityFile[entity].keys():
                str_joint_stiffness = entityFile[entity]['expansion joint stiffness']
                joint_stiffness, joint_table_names, joint_list_freq = self._get_expansion_joint_stiffness_from_string(str_joint_stiffness)

            outerDiameter = ""
            thickness = ""
            offset_y, offset_z = 0., 0.
            insulation_thickness = 0.
            insulation_density = 0.

            if "-" in entity:

                if 'list of elements' in entityFile[entity].keys():
                    str_list_elements = entityFile[entity]['list of elements']
                    list_elements = get_list_of_values_from_string(str_list_elements)

                if structural_element_type == "":
                    line_id = entity.split("-")[0]
                    if 'structural element type' in entityFile[line_id].keys():
                        structural_element_type = entityFile[line_id]['structural element type']
            
                if structural_element_type == 'pipe_1':

                    if 'outer diameter' in entityFile[entity].keys():
                        outerDiameter = entityFile[entity]['outer diameter']
                    if 'thickness' in entityFile[entity].keys():
                        thickness = entityFile[entity]['thickness']
                    if 'offset [e_y, e_z]' in entityFile[entity].keys():
                        offset = entityFile[entity]['offset [e_y, e_z]']
                        offset_y, offset_z = self._get_offset_from_string(offset) 
                    if 'insulation thickness' in entityFile[entity].keys():
                        insulation_thickness = entityFile[entity]['insulation thickness']
                    if 'insulation density' in entityFile[entity].keys():
                        insulation_density = entityFile[entity]['insulation density']
                    
                    if 'section parameters' in entityFile[entity].keys():
                        str_section_parameters = entityFile[entity]['section parameters']
                        parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
                        outerDiameter = parameters[0]
                        thickness = parameters[1] 
                        offset_y = parameters[2] 
                        offset_z = parameters[3] 
                        insulation_thickness = parameters[4]
                        insulation_density = parameters[5]
        
                    if outerDiameter != "" and thickness != "":
                        try:
                            outerDiameter = float(outerDiameter)
                            thickness = float(thickness)
                            offset_y = float(offset_y)
                            offset_z = float(offset_z)
                            insulation_thickness = float(insulation_thickness)
                            insulation_density = float(insulation_density)

                            section_parameters = {  "outer_diameter" : outerDiameter,
                                                    "thickness" : thickness, 
                                                    "offset_y" : offset_y, 
                                                    "offset_z" : offset_z, 
                                                    "insulation_thickness" : insulation_thickness, 
                                                    "insulation_density" : insulation_density }
            
                            pipe_section_info = {   "section_type_label" : "Pipe section" ,
                                                    "section_parameters" : section_parameters  }

                            cross = CrossSection(pipe_section_info=pipe_section_info)
                            
                            self.dict_cross[entity] = [cross, list_elements]
                        except Exception as log_error:
                            title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                            message = str(log_error)
                            message += f"\n\n {entity}"
                            PrintMessageInput([title, message, window_title])
    
                if str_joint_parameters != "" and str_joint_stiffness != "":
                    _list_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)
                    _data = [joint_parameters, joint_stiffness, joint_table_names, joint_list_freq]
                    self.dict_expansion_joint_parameters[entity]= [_list_elements, _data]
            
            else:
        
                if structural_element_type == 'beam_1':

                    if 'beam section type' in entityFile[entity].keys():
                        section_type = entityFile[entity]['beam section type']

                    try:
    
                        if section_type == "Generic section":                 
                            if 'section properties' in entityFile[entity].keys():
                                str_section_properties =  entityFile[entity]['section properties']
                                section_properties = get_list_of_values_from_string(str_section_properties, int_values=False)
                                section_properties = get_beam_section_properties(section_type, section_properties)
                                section_parameters = None
                        else:
                            if 'section parameters' in entityFile[entity].keys():
                                str_section_parameters = entityFile[entity]['section parameters']
                                section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
                                section_properties = get_beam_section_properties(section_type, section_parameters)
    
                        beam_section_info = {   "section_type_label" : section_type,
                                                "section_parameters" : section_parameters,
                                                "section_properties" : section_properties   }

                        cross = CrossSection(beam_section_info=beam_section_info)
                        self.dict_cross[entity] = cross
                        
                    except Exception as err:
                        title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                        message = str(err)
                        message += f"\n\nProblem detected at line: {entity}"
                        PrintMessageInput([title, message, window_title])

                else:

                    if 'outer diameter' in entityFile[entity].keys():
                        outerDiameter = entityFile[entity]['outer Diameter']
                    if 'thickness' in entityFile[entity].keys():    
                        thickness = entityFile[entity]['thickness']
                    if 'offset [e_y, e_z]' in entityFile[entity].keys(): 
                        offset = entityFile[entity]['offset [e_y, e_z]']
                        offset_y, offset_z = self._get_offset_from_string(offset) 
                    if 'insulation thickness' in entityFile[entity].keys():
                        insulation_thickness = entityFile[entity]['insulation thickness']
                    if 'insulation density' in entityFile[entity].keys():
                        insulation_density = entityFile[entity]['insulation density']

                    if 'section parameters' in entityFile[entity].keys():
                        str_section_parameters = entityFile[entity]['section parameters']
                        parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
                        outerDiameter = parameters[0]
                        thickness = parameters[1] 
                        offset_y = parameters[2] 
                        offset_z = parameters[3] 
                        insulation_thickness = parameters[4] 
                        insulation_density = parameters[5]

                    if 'variable section parameters' in entityFile[entity].keys():
                        str_section_variable_parameters = entityFile[entity]['variable section parameters']
                        section_variable_parameters = get_list_of_values_from_string(str_section_variable_parameters, int_values=False)
                        self.dict_variable_sections[entity] = section_variable_parameters

                    if outerDiameter != "" and thickness != "":
                        try:

                            section_parameters = {  "outer_diameter" : float(outerDiameter),
                                                    "thickness" : float(thickness), 
                                                    "offset_y" : float(offset_y), 
                                                    "offset_z" : float(offset_z), 
                                                    "insulation_thickness" : float(insulation_thickness), 
                                                    "insulation_density" : float(insulation_density) }
        
                            pipe_section_info = {   "section_type_label" : "Pipe section" ,
                                                    "section_parameters" : section_parameters  }

                            cross = CrossSection(pipe_section_info=pipe_section_info)

                            self.dict_cross[entity] = cross

                        except Exception as err:
                            title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                            message = str(err)
                            message += f"\n\nProblem detected at line: {entity}"
                            PrintMessageInput([title, message, window_title])
                
                    if str_joint_parameters != "" and str_joint_stiffness != "":
                        _data = [joint_parameters, joint_stiffness, joint_table_names, joint_list_freq]
                        self.dict_expansion_joint_parameters[entity] = _data
            
            valve_data = {}
            dict_element_to_diameters = {}
            valve_section_parameters = []
            flange_section_parameters = []
            valve_cross, flange_cross = [], []
            number_valve_elements = 0
            number_flange_elements = 0

            if structural_element_type == "valve":

                if "valve parameters" in entityFile[entity].keys():
                    str_valve_parameters = entityFile[entity]['valve parameters']
                    valve_parameters = get_list_of_values_from_string(str_valve_parameters, int_values=False)
                    [valve_length, stiffening_factor, valve_mass] = valve_parameters
                    valve_data["valve_length"] = valve_length
                    valve_data["stiffening_factor"] = stiffening_factor
                    valve_data["valve_mass"] = valve_mass
                
                if "valve center coordinates" in entityFile[entity].keys():
                    str_valve_coord = entityFile[entity]['valve center coordinates']
                    valve_data["valve_center_coordinates"] = get_list_of_values_from_string(str_valve_coord, int_values=False)
                
                if "valve section parameters" in entityFile[entity].keys():
                    str_valve_section_parameters = entityFile[entity]['valve section parameters'] 
                    valve_section_parameters = get_list_of_values_from_string(str_valve_section_parameters, int_values=False)
                
                if "flange section parameters" in entityFile[entity].keys():
                    str_flange_section_parameters = entityFile[entity]['flange section parameters']
                    flange_section_parameters = get_list_of_values_from_string(str_flange_section_parameters, int_values=False)
                
                if 'list of elements' in entityFile[entity].keys():
                    str_valve_list_elements = entityFile[entity]['list of elements']
                    valve_data["valve_elements"] = get_list_of_values_from_string(str_valve_list_elements)
                    number_valve_elements = len(valve_data["valve_elements"])
                    
                if 'number of flange elements' in entityFile[entity].keys():
                    str_number_flange_elements = entityFile[entity]['number of flange elements']
                    number_flange_elements = int(str_number_flange_elements)
                    valve_data["number_flange_elements"] = number_flange_elements

                cross_section_labels = ["outer_diameter", "thickness", "offset_y", "offset_z", "insulation_thickness", "insulation_density"]
                if len(valve_section_parameters) == 6:
                    valve_data["valve_section_parameters"] = dict(zip(cross_section_labels, valve_section_parameters))
                    valve_section_info = {  "section_type_label" : "Valve section",
                                            "section_parameters" : valve_data["valve_section_parameters"]  }
                                        
                    list_valve_elements = valve_data["valve_elements"]
                    valve_thickness = valve_section_parameters[1]

                    N = number_valve_elements - number_flange_elements
                    nf = int(number_flange_elements/2) 
                    if number_flange_elements == 0:
                        list_inner_elements = valve_data["valve_elements"]
                        list_outer_diameters =  get_V_linear_distribution(valve_section_parameters[0], N)
                        list_inner_diameters = list_outer_diameters - 2*valve_thickness
                    else:
                        flange_thickness = flange_section_parameters[1]
                        list_inner_elements = valve_data["valve_elements"][nf:-nf]

                        flange_diameter = flange_section_parameters[0]
                        list_outer_diameters = np.ones(number_valve_elements)*flange_diameter
                        list_inner_diameters = list_outer_diameters - 2*flange_thickness

                        list_outer_diameters[nf:-nf] = get_V_linear_distribution(valve_section_parameters[0], N)
                        list_inner_diameters[nf:-nf] = list_outer_diameters[nf:-nf] - 2*valve_thickness

                        lists_flange_elements = [list_valve_elements[0:nf], list_valve_elements[-nf:]]
                        list_flange_elements = [element_id for _list_elements in lists_flange_elements for element_id in _list_elements]
                        valve_data["flange_elements"] = list_flange_elements
                    
                    dict_outer_diameters = dict(zip(list_valve_elements, np.round(list_outer_diameters, decimals=6)))                      
                    dict_inner_diameters = dict(zip(list_valve_elements, np.round(list_inner_diameters, decimals=6)))

                    for _id in list_inner_elements:
                        dict_element_to_diameters[_id] = [dict_outer_diameters[_id], dict_inner_diameters[_id]]
                        valve_section_info["diameters_to_plot"] = dict_element_to_diameters[_id]
                        valve_cross.append(CrossSection(valve_section_info=valve_section_info)) 
                
                if len(flange_section_parameters) == 6:
                    valve_data["flange_section_parameters"] = dict(zip(cross_section_labels, flange_section_parameters))
                    flange_section_info = { "section_type_label" : "Valve section",
                                            "section_parameters" : valve_data["flange_section_parameters"]  }

                    for _id in list_flange_elements:
                        dict_element_to_diameters[_id] = [dict_outer_diameters[_id], dict_inner_diameters[_id]]   
                        flange_section_info["diameters_to_plot"] = dict_element_to_diameters[_id]       
                        flange_cross.append(CrossSection(valve_section_info=flange_section_info))
                
                valve_data["valve_diameters"] = dict_element_to_diameters

                if valve_data:
                    cross_sections = [valve_cross, flange_cross] 
                    self.dict_valve[entity] = [valve_data, cross_sections]

            if 'material id' in entityFile[entity].keys():
                material_id = entityFile[entity]['material id']

                if material_id.isnumeric():
                    material_id = int(material_id)
                    for material in material_list.sections():
                        if int(material_list[material]['identifier']) == material_id:
                            name = str(material_list[material]['name'])
                            identifier = str(material_list[material]['identifier'])
                            density =  str(material_list[material]['density'])
                            youngmodulus =  str(material_list[material]['young modulus'])
                            poisson =  str(material_list[material]['poisson'])
                            thermal_expansion_coefficient = str(material_list[material]['thermal expansion coefficient'])
                            color =  str(material_list[material]['color'])
                            youngmodulus = float(youngmodulus)*(10**(9))
                            if thermal_expansion_coefficient == "":
                                thermal_expansion_coefficient = float(0)
                            else:
                                thermal_expansion_coefficient = float(thermal_expansion_coefficient)
                            temp_material = Material(name, float(density), 
                                                            young_modulus = youngmodulus, 
                                                            poisson_ratio = float(poisson), 
                                                            thermal_expansion_coefficient = thermal_expansion_coefficient,
                                                            color = color,
                                                            identifier = int(identifier))
                            self.dict_material[int(entity)] = temp_material

            if 'fluid id' in entityFile[entity].keys():    
                fluid_id = entityFile[entity]['fluid id']

                if fluid_id.isnumeric():
                    fluid_id = int(fluid_id)
                    for fluid in fluid_list.sections():
                        keys = list(fluid_list[fluid].keys())
                        if int(fluid_list[fluid]['identifier']) == fluid_id:
                            name = fluid_list[fluid]['name']
                            identifier = fluid_list[fluid]['identifier']
                            fluid_density =  float(fluid_list[fluid]['fluid density'])
                            speed_of_sound =  float(fluid_list[fluid]['speed of sound'])

                            temperature = None
                            if 'temperature' in keys:
                                temperature = float(fluid_list[fluid]['temperature'])

                            pressure = None
                            if 'pressure' in keys:
                                pressure = float(fluid_list[fluid]['pressure'])

                            isentropic_exponent = None
                            if 'isentropic exponent' in keys:
                                isentropic_exponent =  float(fluid_list[fluid]['isentropic exponent'])
                            
                            thermal_conductivity = None
                            if 'thermal conductivity' in keys:
                                thermal_conductivity =  float(fluid_list[fluid]['thermal conductivity'])

                            specific_heat_Cp = None
                            if 'specific heat cp' in keys:
                                specific_heat_Cp =  float(fluid_list[fluid]['specific heat cp'])
                            
                            dynamic_viscosity = None
                            if 'dynamic viscosity' in keys:
                                dynamic_viscosity =  float(fluid_list[fluid]['dynamic viscosity'])
                            
                            # acoustic_impedance =  fluid_list[fluid]['impedance']
                            color =  fluid_list[fluid]['color']
                            temp_fluid = Fluid( name,
                                                fluid_density,
                                                speed_of_sound,
                                                isentropic_exponent = isentropic_exponent,
                                                thermal_conductivity = thermal_conductivity,
                                                specific_heat_Cp = specific_heat_Cp,
                                                dynamic_viscosity = dynamic_viscosity,
                                                color=color, identifier = int(identifier),
                                                temperature = temperature,
                                                pressure = pressure )

                            self.dict_fluid[int(entity)] = temp_fluid
                                
            if 'capped end' in entityFile[entity].keys():
                capped_end = entityFile[entity]['capped end']
                if capped_end != "":
                    self.dict_capped_end[capped_end].append(int(entity))
            
            if 'beam x-axis rotation' in entityFile[entity].keys():
                beam_xaxis_rotation = entityFile[entity]['beam x-axis rotation']
                self.dict_beam_xaxis_rotation[int(entity)] = float(beam_xaxis_rotation)

            if 'stress stiffening parameters' in entityFile[entity].keys():
                list_parameters = entityFile[entity]['stress stiffening parameters']
                _list_parameters = get_list_of_values_from_string(list_parameters, int_values=False)
                try:
                    self.dict_stress_stiffening[int(entity)] = _list_parameters
                except Exception as err:
                    title = "ERROR WHILE LOADING STRESS STIFFENING FROM FILE"
                    message = str(err)
                    PrintMessageInput([title, message, window_title])

        for section in list(element_file.sections()):

            try:
                if "ACOUSTIC ELEMENT LENGTH CORRECTION" in section:
                    if 'length correction type' in  element_file[section].keys():
                        length_correction_type = int(element_file[section]['length correction type'])   
                    if 'list of elements' in  element_file[section].keys():
                        list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(list_elements)
                    if length_correction_type in [0,1,2] and get_list_elements != []:
                        self.dict_length_correction[section] = [get_list_elements, length_correction_type]
            except Exception as log_error:  
                title = "ERROR WHILE LOADING ACOUSTIC ELEMENT LENGTH CORRECTION FROM FILE"
                message = str(log_error)
                PrintMessageInput([title, message, window_title])

            try:
                if "PERFORATED PLATE" in section:
                    if 'perforated plate data' in  element_file[section].keys():
                        list_data = element_file[section]['perforated plate data']   
                        pp_data = get_list_of_values_from_string(list_data, False)

                    if 'list of elements' in  element_file[section].keys():
                        list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(list_elements)
                    
                    if pp_data != [] and get_list_elements != []:
                        perforated_plate = PerforatedPlate( float(pp_data[0]), 
                                                            float(pp_data[1]),
                                                            float(pp_data[2]),
                                                            discharge_coefficient = float(pp_data[3]),
                                                            single_hole = bool(pp_data[4]),
                                                            nonlinear_effect = bool(pp_data[5]),
                                                            nonlinear_discharge_coefficient = float(pp_data[6]),
                                                            correction_factor = float(pp_data[7]),
                                                            bias_effect = bool(pp_data[8]),
                                                            bias_coefficient = float(pp_data[9]),
                                                            type = int(pp_data[10]) )

                        if 'dimensionless impedance' in  element_file[section].keys():
                            dimensionless_data = element_file[section]['dimensionless impedance'] 

                            [dim_impedance, dim_impedance_table_name, frequencies] = self._get_acoustic_bc_from_string( dimensionless_data, 
                                                                                                                        "dimensionless impedance", 
                                                                                                                        "perforated_plate_files" )
                            perforated_plate.dimensionless_impedance = dim_impedance 
                            perforated_plate.dimensionless_impedance_table_name = dim_impedance_table_name
                            
                        self.dict_perforated_plate[section] = [get_list_elements, perforated_plate, frequencies]
            except Exception as log_error:  
                window_title = "Error while loading acoustic element perforated plate from file"
                message = str(log_error)
                PrintMessageInput([title, message, window_title])

            try:
                if "CAPPED END" in section:
                    if 'list of elements' in element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(_list_elements)
                        self.dict_capped_end[section] = get_list_elements
            except Exception as err:  
                title = "ERROR WHILE LOADING CAPPED END FROM FILE"
                message = str(err)
                PrintMessageInput([title, message, window_title])

            try:
                if "STRESS STIFFENING" in section:
                    if 'stress stiffening parameters' in  element_file[section].keys():
                        _list_parameters = element_file[section]['stress stiffening parameters']
                        get_list_parameters = get_list_of_values_from_string(_list_parameters, int_values=False)
                    if 'list of elements' in  element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(_list_elements)
                    self.dict_stress_stiffening[section] = [get_list_elements, get_list_parameters]
            except Exception as err: 
                title = "ERROR WHILE LOADING STRESS STIFFENING FROM FILE" 
                message = str(err)
                PrintMessageInput([title, message, window_title])

            try:
                if "B2PX ROTATION DECOUPLING" in section:
                    if 'list of elements' in  element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(_list_elements)
                    if 'list of nodes' in  element_file[section].keys():
                        _list_nodes = element_file[section]['list of nodes']
                        get_list_nodes = get_list_of_values_from_string(_list_nodes)
                    if 'rotation dofs mask' in  element_file[section].keys():
                        _dofs_mask = element_file[section]['rotation dofs mask']
                        get_dofs_mask = get_list_bool_from_string(_dofs_mask)
                    self.dict_B2XP_rotation_decoupling[section] = [get_list_elements, get_list_nodes, get_dofs_mask]
            except Exception as err: 
                title = "ERROR WHILE LOADING B2PX ROTATION DECOUPLING FROM FILE" 
                message = str(err)
                PrintMessageInput([title, message, window_title]) 

    def add_cross_section_in_file(self, lines, cross_section):  

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            line_id = str(line_id)

            for section in config.sections():
                section_prefix = line_id + '-'
                if section_prefix in section:
                    config.remove_section(section)
        
            str_keys = [    'outer diameter', 
                            'thickness', 
                            'offset [e_y, e_z]', 
                            'insulation thickness', 
                            'insulation density',
                            'variable section parameters',
                            'beam section type',
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
                if cross_section.beam_section_info is not None:
                    if line_id in list(config.sections()):
                        config[line_id]['beam section type'] = cross_section.section_label
                        if "Generic section" == cross_section.section_label:
                            config[line_id]['section properties'] = str(cross_section.section_properties)
                        else:
                            config[line_id]['section parameters'] = str(cross_section.section_parameters)
                else:
                    if line_id in list(config.sections()):
                        # config[line_id]['outer diameter'] = str(cross_section.outer_diameter)
                        # config[line_id]['thickness'] = str(cross_section.thickness)
                        # config[line_id]['offset [e_y, e_z]'] = str(cross_section.offset)
                        # config[line_id]['insulation thickness'] = str(cross_section.insulation_thickness)
                        # config[line_id]['insulation density'] = str(cross_section.insulation_density)
                        section_parameters = list(cross_section.section_parameters.values())
                        config[line_id]['section parameters'] = str(section_parameters)
        
        self.write_data_in_file(self._entity_path, config)      

    def add_cross_section_segment_in_file(self, segments, data):
        
        if isinstance(segments, int):
            segments = [segments]

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for segment_id in segments:
            segment_id = str(segment_id)

            str_keys = [    'section parameters',
                            'section properties',
                            'variable section parameters',
                            'beam section type',
                            'expansion joint parameters',
                            'expansion joint stiffness',
                            'valve parameters',
                            'valve center coordinates',
                            'valve section parameters',
                            'flange section parameters'   ]

            for str_key in str_keys:
                if str_key in list(config[segment_id].keys()):
                    config.remove_option(section=segment_id, option=str_key)

            if data is not None:

                if segment_id in list(config.sections()):
                    config[segment_id]['section label'] = data["section label"]

                if "pipe" in data["section label"]:
                    if segment_id in list(config.sections()):
                        section_parameters = data["section parameters"]
                        config[segment_id]['section parameters'] = str(section_parameters)
                else:
                    if segment_id in list(config.sections()):
                        config[segment_id]['beam section type'] = data["section label"]
                        if data["section label"] == "Generic section":
                            section_properties = data["section properties"]
                            config[segment_id]['section properties'] = str(section_properties)
                        else:
                            section_parameters = data["section parameters"]
                            config[segment_id]['section parameters'] = str(section_parameters)                    

        self.write_data_in_file(self._entity_path, config)

    def add_multiple_cross_section_in_file(self, lines, map_cross_sections_to_elements):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        
        str_keys = [    'structural element type',
                        'outer diameter', 
                        'thickness', 
                        'offset [e_y, e_z]', 
                        'insulation thickness', 
                        'insulation density',
                        'beam section type',
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

                subkey += 1
                key = str_line + "-" + str(subkey)

                config[key] = { 'structural element type' : etype,
                                'outer diameter': f'{vals[0]}',
                                'thickness': f'{vals[1]}',
                                'offset [e_y, e_z]': f'[{vals[2]}, {vals[3]}]',
                                'insulation thickness': f'{vals[4]}',
                                'insulation density': f'{vals[5]}',
                                'list of elements': f'{elements}' }

        self.write_data_in_file(self._entity_path, config)


    def modify_variable_cross_section_in_file(self, lines, parameters):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = list(config.sections())

        for line_id in lines:
            str_line = str(line_id)
            if str_line in sections:
                config[str_line]['variable section parameters'] = str(parameters)

            for section in sections:
                prefix = f"{line_id}-"
                if prefix in section:
                    config.remove_section(section=section)
            
        self.write_data_in_file(self._entity_path, config)


    def modify_valve_in_file(self, lines, parameters):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_keys = [   'outer diameter', 
                        'thickness', 
                        'offset [e_y, e_z]', 
                        'insulation thickness', 
                        'insulation density',
                        'variable section parameters',
                        'beam section type',
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
                
                valve_section_parameters = []
                list_valve_elements = parameters["valve_elements"]
                for value in parameters["valve_section_parameters"].values():
                    valve_section_parameters.append(value)      

                valve_parameters = [valve_length, stiffening_factor, valve_mass]
                config[str_line]['valve parameters'] = str(valve_parameters)
                config[str_line]['valve center coordinates'] = str(list(valve_center_coordinates))
                config[str_line]['valve section parameters'] = str(valve_section_parameters)
                config[str_line]['list of elements'] = str(list_valve_elements)
                
                if "number_flange_elements" in parameters.keys():
                    flange_parameters = []
                    number_flange_elements = parameters["number_flange_elements"]
                    for value in parameters["flange_section_parameters"].values():
                        flange_parameters.append(value)  
                    config[str_line]['flange section parameters'] = str(flange_parameters)
                    config[str_line]['number of flange elements'] = str(number_flange_elements)

        self.write_data_in_file(self._entity_path, config)


    def modify_expansion_joint_in_file(self, lines, parameters):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        sections = config.sections()

        list_keys = [   'outer diameter', 
                        'thickness', 
                        'offset [e_y, e_z]', 
                        'insulation thickness', 
                        'insulation density',
                        'variable section parameters',
                        'beam section type',
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

        self.write_data_in_file(self._entity_path, config)

    def add_multiple_cross_sections_expansion_joints_valves_in_file(self, 
                                                                    lines, 
                                                                    map_cross_sections_to_elements, 
                                                                    map_expansion_joint_to_elements, 
                                                                    map_valve_to_elements,
                                                                    update_by_cross=False):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        config_base = configparser.ConfigParser()
        config_base.read(self._entity_path)

        sections = config_base.sections()
        
        str_keys = [    'structural element type',
                        'outer diameter', 
                        'thickness', 
                        'offset [e_y, e_z]', 
                        'insulation thickness', 
                        'insulation density',
                        'beam section type',
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
                
                index_etype = int(vals[6])
                if index_etype == 0:
                    etype = 'pipe_1'
                
                config[section_key] = { 'structural element type' : etype,
                                        'outer diameter': f'{vals[0]}',
                                        'thickness': f'{vals[1]}',
                                        'offset [e_y, e_z]': f'[{vals[2]}, {vals[3]}]',
                                        'insulation thickness': f'{vals[4]}',
                                        'insulation density': f'{vals[5]}',
                                        'list of elements': f'{elements}' }
            
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
                    valve_section_parameters = list(valve_data["valve_section_parameters"].values())

                    if "flange_elements" in valve_data.keys():
                        number_flange_elements = valve_data["number_flange_elements"]
                        flange_section_parameters = list(valve_data["flange_section_parameters"].values())

                    config[section_key] = { 'structural element type' : 'valve',
                                            'valve parameters' : f'{valve_parameters}',
                                            'valve center coordinates' : f'{valve_center_coordinates}',
                                            'valve section parameters' : f'{valve_section_parameters}',
                                            'flange section parameters' : f'{flange_section_parameters}',
                                            'list of elements' : f'{valve_elements}',
                                            'number of flange elements' : f'{number_flange_elements}' }

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

        self.write_data_in_file(self._entity_path, config)

    def add_length_correction_in_file(self, elements, _type, section): 
        
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if section in list(config.sections()):
            config[section]['length correction type'] = str(_type)
            config[section]['list of elements'] = str(elements)
        else:
            config[section] =   { 'length correction type': str(_type),
                                  'list of elements': str(elements) 
                                  }
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

        self.write_data_in_file(self._element_info_path, config)
    
    def modify_B2PX_rotation_decoupling_in_file(self, elements, nodes, rotations_maks, section, remove=False, reset=False):
         
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

        self.write_data_in_file(self._element_info_path, config)

    def modify_stress_stiffnening_line_in_file(self, lines, pressures, remove=False):
        
        if isinstance(lines, int):
            lines = [lines] 
        
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            str_entity_id = str(line_id)
            if remove:
                if str_entity_id in list(config.sections()):
                    config.remove_option(section=str_entity_id, option='stress stiffening parameters')
            else:
                config[str_entity_id]['stress stiffening parameters'] = str(pressures)

        self.write_data_in_file(self._entity_path, config)

    def modify_stress_stiffnening_element_in_file(self, elements, parameters, section, remove=False):
        
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if remove:
            config.remove_section(section)
        else:
            config[section]['stress stiffening parameters'] = str(parameters)
            config[section]['list of elements'] = str(elements)
  
        self.write_data_in_file(self._element_info_path, config)

    def remove_all_stress_stiffnening_in_file_by_group_elements(self): 
          
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        for section in list(config.sections()):
            if "STRESS STIFFENING" in section:
                config.remove_section(section)

        self.write_data_in_file(self._element_info_path, config)

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
               
        self.write_data_in_file(self._element_info_path, config)

    def modify_capped_end_lines_in_file(self, lines, value):

        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        
        for line_id in lines:
            str_entity_id = str(line_id)
            if value:    
                config[str_entity_id]['capped end'] = str(value)
            else:
                config.remove_option(section=str_entity_id, option='capped end')

        self.write_data_in_file(self._entity_path, config)

    def modify_structural_element_type_in_file(self, lines, element_type):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            str_line = str(line_id)
            if element_type in ["beam_1"]:
                str_keys = ['fluid id', 'stress stiffening parameters']
                
                for str_key in str_keys:
                    if str_key in config[str_line].keys():
                        config.remove_option(section=str_line, option=str_key)
            
            config[str_line]['structural element type'] = element_type

        self.write_data_in_file(self._entity_path, config)

    def modify_structural_element_wall_formulation_in_file(self, lines, formulation):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            str_line = str(line_id)     
            if formulation is None:
                str_key = 'structural element wall formulation'
                config.remove_option(section=str_line, option=str_key)
            else:
                config[str_line]['structural element wall formulation'] = formulation

        self.write_data_in_file(self._entity_path, config)

    def modify_structural_element_force_offset_in_file(self, lines, force_offset):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            str_line = str(line_id)     
            if force_offset is None:
                str_key = 'force offset'
                config.remove_option(section=str_line, option=str_key)
            else:
                config[str_line]['force offset'] = str(force_offset)

        self.write_data_in_file(self._entity_path, config)

    def modify_acoustic_element_type_in_file(self, lines, element_type, proportional_damping=None, vol_flow=None):
        
        if isinstance(lines, int):
            lines = [lines]

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        
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
    
        self.write_data_in_file(self._entity_path, config)

    def add_segment_build_data_in_file(self, lines, data):

        if isinstance(lines, int):
            lines = [lines]
        
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            if len(data) == 2:
                config[str(line_id)]['start point'] = str(data[0])
                config[str(line_id)]['end point'] = str(data[1])
            else:
                config[str(line_id)]['start point'] = str(data[0])
                config[str(line_id)]['corner point'] = str(data[1])
                config[str(line_id)]['end point'] = str(data[2])
                config[str(line_id)]['curvature'] = str(data[3])

        self.write_data_in_file(self._entity_path, config)

    def load_segment_build_data_from_file(self):
        '''
        This method returns the all required data to build pipeline segments.
        '''

        config = configparser.ConfigParser()
        config.read(self._entity_path)
        segment_build_data = dict()

        for section in config.sections():

            tag = int(section)
            keys = config[section].keys()

            if "start point" in keys:
                start_point = get_list_of_values_from_string(config[section]["start point"], int_values=False)

            if "end point" in keys:
                end_point = get_list_of_values_from_string(config[section]["end point"], int_values=False)

            if "corner point" in keys:
                corner_point = get_list_of_values_from_string(config[section]["corner point"], int_values=False)

            if "curvature" in keys:
                curvature = float(config[section]["curvature"])

            if 'section label' in keys:
                section_label = config[section]["section label"]

            if 'section parameters' in keys:
                section_parameters = get_list_of_values_from_string(config[section]["section parameters"], int_values=False)

            material_id = None
            if 'material id' in keys:
                material_id = int(config[section]["material id"])

            is_bend = ('corner point' in keys) and ('curvature' in keys)
            if is_bend:
                
                segment_build_data[tag, "Bend"] = { 'start point' : start_point,
                                                    'corner point' : corner_point,
                                                    'end point' : end_point,
                                                    'curvature' : curvature,
                                                    'section label' : section_label,
                                                    'section parameters' : section_parameters,
                                                    'material id' : material_id }

            else:

                segment_build_data[tag, "Pipe"] = { 'start point' : start_point,
                                                    'end point' : end_point,
                                                    'section label' : section_label,
                                                    'section parameters' : section_parameters,
                                                    'material id' : material_id }

        return segment_build_data

    def add_material_in_file(self, lines, material):

        if isinstance(lines, int):
            lines = [lines]
        
        if material is None:
            material_id = ""
        else:
            material_id = material.identifier

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            config[str(line_id)]['material id'] = str(material_id)
            
        self.write_data_in_file(self._entity_path, config)

    def add_material_segment_in_file(self, lines, material_id):

        if isinstance(lines, int):
            lines = [lines]
        
        if material_id is None:
            material_id = ""

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            config[str(line_id)]['material id'] = str(material_id)
            
        self.write_data_in_file(self._entity_path, config)

    def get_material_properties(self, material_id):
        config = configparser.ConfigParser()
        config.read(self._material_list_path)
        sections = config.sections()

        if isinstance(material_id, int):
            material_id = str(material_id)
            for section in sections:
                if material_id == config[section]["identifier"]:

                    name = str(config[section]['name'])
                    identifier = int(config[section]['identifier'])
                    density =  float(config[section]['density'])
                    elasticity_modulus =  float(config[section]['young modulus'])
                    poisson =  float(config[section]['poisson'])
                    thermal_expansion_coefficient = config[section]['thermal expansion coefficient']
                    # color =  str(config[section]['color'])
                    # elasticity_modulus *= (10**(9))
                    if thermal_expansion_coefficient == "":
                        thermal_expansion_coefficient = float(0)
                    else:
                        thermal_expansion_coefficient = float(thermal_expansion_coefficient)

                    return [name, identifier, density, elasticity_modulus, poisson, thermal_expansion_coefficient]
            return None

    def add_fluid_in_file(self, lines, fluid):
        
        if isinstance(lines, int):
            lines = [lines]

        if fluid is None:
            fluid_id = ""
        else:
            fluid_id = fluid.identifier

        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            config[str(line_id)]['fluid id'] = str(fluid_id)

        self.write_data_in_file(self._entity_path, config)

    def modify_compressor_info_in_file(self, lines, compressor_info={}):
        
        if isinstance(lines, int):
            lines = [lines]
        
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for line_id in lines:
            if compressor_info:
                config[str(line_id)]['compressor info'] = str(list(compressor_info.values()))
            else:
                _section = str(line_id)
                if 'compressor info' in config[str(line_id)].keys():
                    config.remove_option(section=_section, option='compressor info')  

        self.write_data_in_file(self._entity_path, config) 

    def get_dict_of_structural_bc_from_file(self):

        node_structural_list = configparser.ConfigParser()
        node_structural_list.read(self._node_structural_path)

        self.dict_prescribed_dofs = {}
        self.dict_nodal_loads = {}
        self.dict_lumped_inertia = {}
        self.dict_lumped_stiffness = {}
        self.dict_lumped_damping = {}
        self.dict_elastic_link_stiffness = {}
        self.dict_elastic_link_dampings = {}

        for node in node_structural_list.sections():
            try:
                node_id = int(node)
            except:
                node_id = node
            keys = list(node_structural_list[node].keys())

            if "displacements" in keys and "rotations" in keys:
                displacement_strings = node_structural_list[str(node)]['displacements']
                rotation_strings = node_structural_list[str(node)]['rotations']
                labels = [["Ux","Uy","Uz"],["Rx","Ry","Rz"]]
                folder_table_name = "prescribed_dofs_files"
                prescribed_dofs, prescribed_dofs_table_names, prescribed_dofs_freq = self._get_structural_bc_from_string(   displacement_strings, 
                                                                                                                            rotation_strings, 
                                                                                                                            labels,
                                                                                                                            folder_table_name=folder_table_name   )    
                if prescribed_dofs is not None:
                    if sum([1 if value is None else 0 for value in prescribed_dofs]) != 6:
                        self.dict_prescribed_dofs[node_id] = [prescribed_dofs, prescribed_dofs_table_names, prescribed_dofs_freq]
                               
            if "forces" in keys and "moments" in keys:
                forces_strings = node_structural_list[str(node)]['forces'] 
                moments_strings = node_structural_list[str(node)]['moments']
                labels = [["Fx","Fy","Fz"],["Mx","My","Mz"]]
                folder_table_name = "nodal_loads_files"
                nodal_loads, nodal_loads_table_names, nodal_loads_freq = self._get_structural_bc_from_string(   forces_strings, 
                                                                                                                moments_strings, 
                                                                                                                labels,
                                                                                                                folder_table_name=folder_table_name   )
                if nodal_loads is not None:
                    if sum([1 if value is None else 0 for value in nodal_loads]) != 6:
                        self.dict_nodal_loads[node_id] = [nodal_loads, nodal_loads_table_names, nodal_loads_freq]
            
            if "masses" in keys and "moments of inertia" in keys:
                masses = node_structural_list[str(node)]['masses']
                moments_of_inertia = node_structural_list[str(node)]['moments of inertia']
                labels = [["m_x","m_y","m_z"],["Jx","Jy","Jz"]]
                folder_table_name = "lumped_elements_files"
                lumped_inertia, inertia_table_names, inertia_freq = self._get_structural_bc_from_string(masses, 
                                                                                                        moments_of_inertia, 
                                                                                                        labels,
                                                                                                        folder_table_name=folder_table_name, 
                                                                                                        _complex=False)
                if lumped_inertia is not None:
                    if sum([1 if value is None else 0 for value in lumped_inertia]) != 6:
                        self.dict_lumped_inertia[node_id] = [lumped_inertia, inertia_table_names, inertia_freq]

            if "spring stiffness" in keys and "torsional spring stiffness" in keys:
                spring_stiffness = node_structural_list[str(node)]['spring stiffness']
                torsional_spring_stiffness = node_structural_list[str(node)]['torsional spring stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                folder_table_name = "lumped_elements_files"
                lumped_stiffness, stiffness_table_names, stiffness_freq = self._get_structural_bc_from_string(  spring_stiffness, 
                                                                                                                torsional_spring_stiffness, 
                                                                                                                labels, 
                                                                                                                folder_table_name=folder_table_name,
                                                                                                                _complex=False  )
                if lumped_stiffness is not None:
                    if sum([1 if value is None else 0 for value in lumped_stiffness]) != 6:
                        self.dict_lumped_stiffness[node_id] = [lumped_stiffness, stiffness_table_names, stiffness_freq]

            if "damping coefficients" in keys and "torsional damping coefficients":
                damping_coefficients = node_structural_list[str(node)]['damping coefficients']
                torsional_damping_coefficients = node_structural_list[str(node)]['torsional damping coefficients']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                folder_table_name = "lumped_elements_files"
                lumped_damping, damping_table_names, damping_freq = self._get_structural_bc_from_string(damping_coefficients, 
                                                                                                        torsional_damping_coefficients, 
                                                                                                        labels,
                                                                                                        folder_table_name=folder_table_name, 
                                                                                                        _complex=False)
                if lumped_damping is not None:
                    if sum([1 if value is None else 0 for value in lumped_damping]) != 6:
                        self.dict_lumped_damping[node_id] = [lumped_damping, damping_table_names, damping_freq]

            if "connecting stiffness" and "connecting torsional stiffness" in keys:
                connecting_stiffness = node_structural_list[str(node)]['connecting stiffness']
                connecting_torsional_stiffness = node_structural_list[str(node)]['connecting torsional stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                folder_table_name = "elastic_links_files"
                connecting_stiffness, connecting_stiffness_table_names, connecting_stiffness_freq = self._get_structural_bc_from_string(connecting_stiffness, 
                                                                                                                                        connecting_torsional_stiffness, 
                                                                                                                                        labels,
                                                                                                                                        folder_table_name=folder_table_name, 
                                                                                                                                        _complex=False)
                if connecting_stiffness is not None:
                    if sum([1 if value is None else 0 for value in connecting_stiffness]) != 6:
                        self.dict_elastic_link_stiffness[node_id] = [connecting_stiffness, connecting_stiffness_table_names, connecting_stiffness_freq]
        
            if "connecting damping" and "connecting torsional damping" in keys:
                connecting_damping = node_structural_list[str(node)]['connecting damping']
                connecting_torsional_damping = node_structural_list[str(node)]['connecting torsional damping']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                folder_table_name = "elastic_links_files"
                connecting_damping, connecting_damping_table_names, connecting_damping_freq = self._get_structural_bc_from_string(  connecting_damping, 
                                                                                                                                    connecting_torsional_damping, 
                                                                                                                                    labels, 
                                                                                                                                    folder_table_name=folder_table_name,
                                                                                                                                    _complex=False  )
                if connecting_damping is not None:
                    if sum([1 if value is None else 0 for value in connecting_damping]) != 6:
                        self.dict_elastic_link_dampings[node_id] = [connecting_damping, connecting_damping_table_names, connecting_damping_freq]
            
        output = [  self.dict_prescribed_dofs, 
                    self.dict_nodal_loads, 
                    self.dict_lumped_inertia, 
                    self.dict_lumped_stiffness, 
                    self.dict_lumped_damping, 
                    self.dict_elastic_link_stiffness, 
                    self.dict_elastic_link_dampings  ]

        return output

    def get_dict_of_acoustic_bc_from_file(self):

        node_acoustic_list = configparser.ConfigParser()
        node_acoustic_list.read(self._node_acoustic_path)

        dict_pressure = {}
        dict_volume_velocity = {} 
        dict_specific_impedance = {}
        dict_radiation_impedance = {}
        dict_compressor_excitation = defaultdict(list)

        for node in node_acoustic_list.sections():
            node_id = int(node)
            keys = list(node_acoustic_list[node].keys())
            
            if "acoustic pressure" in keys:
                str_acoustic_pressure = node_acoustic_list[str(node)]['acoustic pressure']
                acoustic_pressure, table_name, frequencies = self._get_acoustic_bc_from_string( str_acoustic_pressure, 
                                                                                                "acoustic pressure", 
                                                                                                "acoustic_pressure_files" )
                if acoustic_pressure is not None:
                    dict_pressure[node_id] = [acoustic_pressure, table_name, frequencies]
           
            if "volume velocity" in keys:
                str_volume_velocity = node_acoustic_list[str(node)]["volume velocity"]
                volume_velocity, table_name, frequencies = self._get_acoustic_bc_from_string(   str_volume_velocity, 
                                                                                                "volume velocity", 
                                                                                                "volume_velocity_files"   )
                if volume_velocity is not None:
                    dict_volume_velocity[node_id] = [volume_velocity, table_name, frequencies]

            for key in keys:
                if "compressor excitation -" in key:
                    str_compressor_excitation = node_acoustic_list[str(node)][key]
                    if 'suction' in str_compressor_excitation:
                        connection_info = 'suction'
                    elif 'discharge' in str_compressor_excitation:
                        connection_info = 'discharge'
                    compressor_excitation, table_name, frequencies = self._get_acoustic_bc_from_string( str_compressor_excitation, 
                                                                                                        key, 
                                                                                                        "compressor_excitation_files" )
                    if compressor_excitation is not None:
                        dict_compressor_excitation[node_id].append([compressor_excitation, table_name, connection_info, frequencies])

            if "specific impedance" in keys:
                str_specific_impedance = node_acoustic_list[str(node)]['specific impedance']
                specific_impedance, table_name, frequencies = self._get_acoustic_bc_from_string(str_specific_impedance, 
                                                                                                "specific impedance", 
                                                                                                "specific_impedance_files")
                if specific_impedance is not None:
                    dict_specific_impedance[node_id] = [specific_impedance, table_name, frequencies]

            if "radiation impedance" in keys:
                str_radiation_impedance = node_acoustic_list[str(node)]['radiation impedance']
                radiation_impedance_type, _, _ = self._get_acoustic_bc_from_string( str_radiation_impedance, 
                                                                                    "radiation impedance", "" )
                # radImpedance = self._getRadiationImpedanceBCFromString(radiation_impedance)
                if radiation_impedance_type is not None:
                    dict_radiation_impedance[node_id] = int(np.real(radiation_impedance_type))

        output_list = [ dict_pressure, 
                        dict_volume_velocity, 
                        dict_specific_impedance, 
                        dict_radiation_impedance, 
                        dict_compressor_excitation ]

        return output_list

    def _get_offset_from_string(self, offset):
        offset = offset[1:-1].split(',')
        offset_y = offset_z = 0.0
        if len(offset) == 2:
            if offset[0] != '0.0':
                offset_y = float(offset[0])
            if offset[1] != '0.0':
                offset_z = float(offset[1])
        return offset_y, offset_z

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
                    PrintMessageInput([title, message, window_title])       

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
                        PrintMessageInput([title, message, window_title])
                        return None, None, None
        return output, table_names, list_frequencies

    def _get_expansion_joint_stiffness_from_string(self, input_string):   
        labels = ['Kx', 'Kyz', 'Krx', 'Kryz']
        read = input_string[1:-1].replace(" ","").split(',')
        N = len(read)
        output = [None, None, None, None]
        list_table_names = [None, None, None, None]
        list_frequencies = [None, None, None, None]

        if N==4:
            for i in range(N):
                if read[i] == "None":
                    continue
                try:
                    output[i] = float(read[i])
                except Exception:
                    try:

                        load_path_table = ""    
                        expansion_joints_tables_folder_path = get_new_path( self._structural_imported_data_folder_path, 
                                                                            "expansion_joints_files" )
                        load_path_table = get_new_path(expansion_joints_tables_folder_path, read[i])
        
                        data = np.loadtxt(load_path_table, delimiter=",")
                        output[i] = data[:,1]
                        
                        self.frequencies = data[:,0]
                        self.f_min = self.frequencies[0]
                        self.f_max = self.frequencies[-1]
                        self.f_step = self.frequencies[1] - self.frequencies[0]
                        list_table_names[i] = read[i]

                        if self.f_min != 0:
                            self.non_zero_frequency_info = [False, self.f_min, read[i]]
                        else:
                            self.zero_frequency = True
                        list_frequencies[i] = self.frequencies

                    except Exception as log_error:
                        title = f"Expansion joint: error while loading {labels[i]} table of values"
                        message = str(log_error)
                        PrintMessageInput([title, message, window_title])
                        return None, None, None
        return output, list_table_names, list_frequencies

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
            PrintMessageInput([title, message, window_title]) 

        return output, self.frequencies
    
    def _single_structural_excitation_bc(self, node_id, labels):
        if labels[0] == 'displacements' and labels[1] == 'rotations':
            key_strings = ['forces', 'moments']
            remove_bc_from_file(node_id, self._node_structural_path, key_strings, None)
        elif labels[0] == 'forces' and labels[1] == 'moments':
            key_strings = ['displacements', 'rotations']
            remove_bc_from_file(node_id, self._node_structural_path, key_strings, None)

    def _single_acoustic_pressure_or_volume_velocity_excitation(self, node_id, label):
        if 'acoustic pressure' in label[0]:
            key_strings = ['volume velocity']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        elif 'volume velocity' in  label[0]:
            key_strings = ['acoustic pressure']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)

    def _single_volume_velocity_or_compressor_excitation(self, node_id, label):
        if 'volume velocity' in label[0]:
            key_strings = ['compressor excitation -']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        elif 'compressor excitation -' in  label[0]:
            key_strings = ['volume velocity']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)

    def _single_impedance_at_node(self, node_id, label):
        if label[0] == 'specific impedance':
            key_strings = ['radiation impedance']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        elif label[0] == 'radiation impedance':
            key_strings = ['specific impedance']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)

    def add_structural_bc_in_file(self, nodesID_list, values, labels):
        for node_id in nodesID_list:
            config = configparser.ConfigParser()
            config.read(self._node_structural_path)
            if str(node_id) in config.sections():
                config[str(node_id)][labels[0]]  = f"[{values[0]},{values[1]},{values[2]}]"
                config[str(node_id)][labels[1]] = f"[{values[3]},{values[4]},{values[5]}]"
                if len(labels)==3:
                    config[str(node_id)][labels[2]]  = "{}".format(values[6])

                self.write_data_in_file(self._node_structural_path, config)
                self._single_structural_excitation_bc([node_id], labels)
            else:
                if len(labels)==3:
                    config[str(node_id)] =  {   labels[0]: f"[{values[0]},{values[1]},{values[2]}]",
                                                labels[1]: f"[{values[3]},{values[4]},{values[5]}]",
                                                labels[2]: f"{values[6]}"   }
                else:
                    config[str(node_id)] =  {   labels[0]: f"[{values[0]},{values[1]},{values[2]}]",
                                                labels[1]: f"[{values[3]},{values[4]},{values[5]}]"   }
        
                self.write_data_in_file(self._node_structural_path, config)


    def add_acoustic_bc_in_file(self, list_nodesID, data, loaded_table, label):
        [value, table_name] = data
        for node_id in list_nodesID:
            config = configparser.ConfigParser()
            config.read(self._node_acoustic_path)
            if str(node_id) in config.sections():
                if loaded_table:
                    config[str(node_id)][label[0]]  = f"[{table_name}]"
                else:
                    config[str(node_id)][label[0]] = f"[{value}]"
                self.write_data_in_file(self._node_acoustic_path, config)
                self._single_acoustic_pressure_or_volume_velocity_excitation([node_id], label)
                self._single_volume_velocity_or_compressor_excitation([node_id], label)
                self._single_impedance_at_node([node_id], label)
            else:
                if loaded_table:
                    config[str(node_id)] =  {label[0]: f"[{table_name}]"}
                else:    
                    config[str(node_id)] = {label[0]: f"[{value}]"}
                self.write_data_in_file(self._node_acoustic_path, config)


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

    #     list_table_names = []
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
    #     config.read(self._entity_path)
    #     sections = config.sections()

    #     list_table_names = []
    #     list_joint_stiffness = []
    #     if str_line_id in sections:
    #         keys = list(config[str_line_id].keys())
    #         if 'expansion joint stiffness' in keys:
    #             read_joint_stiffness = config[str_line_id]['expansion joint stiffness']
    #             list_joint_stiffness = read_joint_stiffness[1:-1].replace(" ","").split(',')
    #             cache_section = str_line_id
        
    #     if list_joint_stiffness == []:
    #         return

    #     for stiffness_value in list_joint_stiffness:
    #         try:
    #             float(stiffness_value)
    #             return
    #         except:
    #             break
        
    #     list_table_multiple_joints = []
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


    def modify_node_ids_in_acoustic_bc_file(self, dict_old_to_new_indexes, dict_non_mapped_indexes):
        if os.path.exists(self._node_acoustic_path):
            config = configparser.ConfigParser()
            config.read(self._node_acoustic_path)
            for node_id in list(config.sections()):
                try:
                    new_key = str(dict_old_to_new_indexes[node_id])
                    if node_id != new_key:
                        config[new_key] = config[node_id]
                        config.remove_section(node_id)
                except Exception as log_error:
                    config.remove_section(node_id)
            self.write_data_in_file(self._node_acoustic_path, config)


    def modify_node_ids_in_structural_bc_file(self, dict_old_to_new_indexes, dict_non_mapped_nodes):
        if os.path.exists(self._node_structural_path):

            config = configparser.ConfigParser()
            config_new = configparser.ConfigParser()
            config.read(self._node_structural_path)
            sections = list(config.sections())
            
            for section in sections:
                try:
                    if section not in dict_non_mapped_nodes.values():     
                        if "-" in section:
                            [_node_id1, _node_id2]  = section.split("-")
                            key_id1 = str(dict_old_to_new_indexes[_node_id1])
                            key_id2 = str(dict_old_to_new_indexes[_node_id2])
                            new_key = f"{key_id1}-{key_id2}"
                        else:
                            new_key = str(dict_old_to_new_indexes[section])
                            # if section != new_key:
                            #     config2[new_key] = config[section]
                            #     config.remove_section(section)   
                        if section != new_key:
                            config_new[new_key] = config[section]
                            # config.remove_section(section)
                        else:
                            config_new[section] = config[section]                     
                
                except Exception as log_error:
                    config.remove_section(section)
            
            self.write_data_in_file(self._node_structural_path, config_new)


    def modify_list_of_element_ids_in_entity_file(self, dict_group_elements_to_update_after_remesh, dict_non_mapped_subgroups_entity_file):
        """ This method updates the lists of elements in entity file after remesh process. A mapping process checks the boundaries of the
            attribution before and after meshing process. If the mapping process could not find boundaries of atribution after remesh, 
            so the all attribuiton from line related to the group of elements will be removed.
        
        """
        if os.path.exists(self._entity_path):
            config = configparser.ConfigParser()
            config.read(self._entity_path)
            sections = config.sections()
            
            for section in sections:
                if section in config.sections():
                    if 'list of elements' in config[section].keys():
                        str_list_elements = config[section]['list of elements']
                        list_elements = get_list_of_values_from_string(str_list_elements)
                        list_subgroup_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)
                        temp_list = []
                        lines_to_reset = []
                        try:

                            for subgroup_elements in list_subgroup_elements:
                                str_subgroup_elements = str(subgroup_elements)
                                if str_subgroup_elements in dict_group_elements_to_update_after_remesh.keys():
                                    temp_list.append(dict_group_elements_to_update_after_remesh[str_subgroup_elements])
                                elif str_subgroup_elements in dict_non_mapped_subgroups_entity_file.keys():
                                    lines_to_reset.append(section)    

                            if lines_to_reset != []:
                                for line_to_reset in lines_to_reset:
                                    prefix = line_to_reset.split("-")[0] + "-"
                                    for _section in sections:
                                        if prefix in _section:
                                            config.remove_section(section=_section)
                            elif temp_list != []:
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

            self.write_data_in_file(self._entity_path, config)


    def modify_element_ids_in_element_info_file(self, dict_old_to_new_subgroups_elements, dict_non_mapped_subgroups, dict_list_elements_to_subgroups):
        config = configparser.ConfigParser()
        config.read(self._element_info_path)
        sections = config.sections()
        
        for section in sections:
            if 'list of elements' in config[section].keys():
                
                str_list_elements = config[section]['list of elements']
                list_subgroups_elements = dict_list_elements_to_subgroups[str_list_elements]

                temp_list = []
                try:

                    for subgroup_elements in list_subgroups_elements:
                        str_group_elements = str(subgroup_elements)
                        if str_group_elements not in dict_non_mapped_subgroups.keys():
                            temp_list.append(dict_old_to_new_subgroups_elements[str(subgroup_elements)])
                    
                    if temp_list != []:
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
        config.read(self._entity_path)
        if _line_id in list(config.sections()):
            if value == 0:
                if "beam x-axis rotation" in list(config[_line_id].keys()):
                    config.remove_option(section=str(_line_id), option="beam x-axis rotation")
            else:                    
                config[_line_id]["beam x-axis rotation"] = str(value)               
            self.write_data_in_file(self._entity_path, config)

    def write_data_in_file(self, path, config):
        with open(path, 'w') as config_file:
            config.write(config_file)

    def get_import_type(self):
        return self._import_type

    @property
    def project_name(self):
        return self._project_name

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
    def material_list_path(self):
        return self._material_list_path

    @property
    def fluid_list_path(self):
        return self._fluid_list_path
    
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
    #                 new_list_elements = []
    #                 temp_list = old_list_elements.copy()
    #                 for element_id in temp_list:
    #                     if element_id not in ext_list_elements:
    #                         new_list_elements.append(element_id)
    #                 config[section]['list of elements'] = str(new_list_elements)