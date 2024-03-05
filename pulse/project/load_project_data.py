
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.material import Material
from pulse.preprocessing.perforated_plate import PerforatedPlate
from pulse.preprocessing.cross_section import CrossSection, get_beam_section_properties

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.project.project_file import ProjectFile
from pulse.tools.utils import *

from pulse import app

import configparser
from collections import defaultdict
from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class LoadProjectData:
    def __init__(self):
        super().__init__()

        self.file = app().file
        self._initialize()
        
    def _initialize(self):
        self.element_type_is_acoustic = False
        self.element_type_is_structural = False

    def load_project_data_from_files(self):
        t0 = time()
        self.initialize_dictionaries_for_load_data()
        self.load_material_data_from_file()
        self.load_fluid_data_from_file()
        self.load_cross_section_data_from_file()
        self.load_element_type_data_from_file()
        self.load_valve_data_from_file()
        self.load_capped_end_data_from_file()
        self.load_stress_stiffening_data_from_file()
        self.load_compressor_info_from_file()
        self.load_elements_data_from_file()
        # print(self.cross_section_data)
        # print(self.acoustic_element_type_data)
        # print(self.structural_element_type_data)
        # print(self.variable_sections_data)
        # print(self.material_data)
        # print(self.fluid_data)
        # dt = time() - t0
        # print(f"Elapsed time to load project data: {dt} [s]")

    def initialize_dictionaries_for_load_data(self):
        self.material_data = dict()
        self.cross_section_data = dict()
        self.variable_sections_data = dict()
        self.expansion_joint_parameters_data = dict()
        self.valve_data = dict()
        self.valve_data_sections = dict()
        self.beam_xaxis_rotation_data = dict()
        self.structural_element_type_data = dict()
        self.structural_element_force_offset_data = dict()
        self.structural_element_wall_formulation_data = dict()
        self.acoustic_element_type_data = dict()
        self.fluid_data = dict()
        self.compressor_info = dict()
        self.perforated_plate_data = dict()
        self.stress_stiffening_data = dict()
        self.capped_end_data = defaultdict(list)
        self.B2XP_rotation_decoupling_data = dict()
        self.element_length_correction_data = dict()

    def load_material_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)

        material_list = configparser.ConfigParser()
        material_list.read(self.file._material_list_path)
        
        try:
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                if 'material id' in keys:

                    material_id = section['material id']

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
                                
                                temp_material = Material(   name, 
                                                            float(density), 
                                                            young_modulus = youngmodulus, 
                                                            poisson_ratio = float(poisson), 
                                                            thermal_expansion_coefficient = thermal_expansion_coefficient,
                                                            color = color,
                                                            identifier = int(identifier)   )
                                
                                self.material_data[int(tag)] = temp_material

        except Exception as error_log:

            title = "Error while loading material data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])

    def load_fluid_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)

        fluid_list = configparser.ConfigParser()
        fluid_list.read(self.file._fluid_list_path)

        try:
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                if 'fluid id' in keys:    
                    fluid_id = section['fluid id']

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

                                self.fluid_data[int(tag)] = temp_fluid

        except Exception as error_log:
            
            title = "Error while loading fluid data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_cross_section_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)

        try:
            
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                list_elements = ""
                structural_element_type = ""

                if 'structural element type' in keys:
                    structural_element_type = section['structural element type']
                
                if 'section type' in keys:
                    section_type_label = section['section type']

                if structural_element_type != "":
                    if 'list of elements' in keys:
                        if "-" in tag:
                            str_list_elements = section['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)
                            self.structural_element_type_data[tag] = [list_elements, structural_element_type]
                    else:
                        self.structural_element_type_data[tag] = structural_element_type
                    self.element_type_is_structural = True
                else:
                    self.structural_element_type_data[tag] = 'pipe_1'

                if 'beam x-axis rotation' in keys:
                    beam_xaxis_rotation = section['beam x-axis rotation']
                    self.beam_xaxis_rotation_data[int(tag)] = float(beam_xaxis_rotation)

                str_joint_parameters = ""
                if 'expansion joint parameters' in keys:
                    str_joint_parameters = section['expansion joint parameters']
                    joint_parameters = get_list_of_values_from_string(str_joint_parameters, int_values=False)

                str_joint_stiffness = ""
                if 'expansion joint stiffness' in keys:
                    str_joint_stiffness = section['expansion joint stiffness']
                    joint_stiffness, joint_table_names, joint_list_freq = self._get_expansion_joint_stiffness_from_string(str_joint_stiffness)

                if "-" in tag:

                    if 'list of elements' in keys:
                        str_list_elements = section['list of elements']
                        list_elements = get_list_of_values_from_string(str_list_elements)
                
                    if structural_element_type == 'pipe_1':

                        section_parameters = list()
                        
                        if 'outer diameter' in keys:
                            section_parameters.append(section['outer diameter'])
                        
                        if 'thickness' in keys:    
                            section_parameters.append(section['thickness'])
                        
                        if 'offset [e_y, e_z]' in keys: 
                            offset = section['offset [e_y, e_z]']
                            offset_y, offset_z = get_offset_from_string(offset)
                            section_parameters.append(offset_y)
                            section_parameters.append(offset_z)
                        
                        if 'insulation thickness' in keys:
                            section_parameters.append(section['insulation thickness'])
                        
                        if 'insulation density' in keys:
                            section_parameters.append(section['insulation density'])
                        
                        if 'section parameters' in keys:
                            str_section_parameters = section['section parameters']
                            section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
            
                        if len(section_parameters) == 6:
            
                                pipe_section_info = {   "section_type_label" : section_type_label ,
                                                        "section_parameters" : section_parameters  }

                                self.cross_section_data[tag, "pipe"] = [list_elements, pipe_section_info]
                        
                        elif len(section_parameters) == 12:
                                
                                pipe_section_info = {   "section_type_label" : section_type_label ,
                                                        "section_parameters" : section_parameters  }

                                self.variable_sections_data[tag, "pipe"] = [list_elements, pipe_section_info]
        
                    if str_joint_parameters != "" and str_joint_stiffness != "":
                        _list_elements = check_is_there_a_group_of_elements_inside_list_elements(list_elements)
                        _data = [joint_parameters, joint_stiffness, joint_table_names, joint_list_freq]
                        self.expansion_joint_parameters_data[tag]= [_list_elements, _data]
                
                else:
            
                    if structural_element_type == 'beam_1':

    
                        if section_type_label == "Generic section":                 
                            if 'section properties' in keys:
                                str_section_properties =  section['section properties']
                                section_properties = get_list_of_values_from_string(str_section_properties, int_values=False)
                                section_properties = get_beam_section_properties(section_type_label, section_properties)
                                section_parameters = None
                        else:
                            if 'section parameters' in keys:
                                str_section_parameters = section['section parameters']
                                section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)
                                section_properties = get_beam_section_properties(section_type_label, section_parameters)
    
                        beam_section_info = {   "section_type_label" : section_type_label,
                                                "section_parameters" : section_parameters,
                                                "section_properties" : section_properties   }

                        self.cross_section_data[tag, "beam"] = beam_section_info

                    else:

                        
                        if "section parameters" in keys:
                            
                            str_section_parameters = section['section parameters']
                            section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)

                        else:

                            section_parameters = list()
                            
                            if 'outer diameter' in keys:
                                outer_diameter = float(section['outer diameter'])
                                section_parameters.append(outer_diameter)
                            
                            if 'thickness' in keys:
                                thickness = float(section['thickness'])
                                section_parameters.append(thickness)
                            
                            if 'offset [e_y, e_z]' in keys: 
                                offset = section['offset [e_y, e_z]']
                                offset_y, offset_z = get_offset_from_string(offset)
                                section_parameters.append(offset_y)
                                section_parameters.append(offset_z)
                            
                            if 'insulation thickness' in keys:
                                insulation_thickness = float(section['insulation thickness'])
                                section_parameters.append(insulation_thickness)
                            
                            if 'insulation density' in keys:
                                insulation_density = float(section['insulation density'])
                                section_parameters.append(insulation_density)

                            if 'section parameters' in keys:
                                str_section_parameters = section['section parameters']
                                section_parameters = get_list_of_values_from_string(str_section_parameters, int_values=False)

                            if 'variable section parameters' in keys:
                                str_section_variable_parameters = section['variable section parameters']
                                section_variable_parameters = get_list_of_values_from_string(str_section_variable_parameters, int_values=False)
                                self.variable_sections_data[tag] = section_variable_parameters

                        if len(section_parameters) == 6:
            
                                pipe_section_info = {   "section_type_label" : "Pipe section" ,
                                                        "section_parameters" : section_parameters  }

                                self.cross_section_data[tag, "pipe"] = pipe_section_info
                        
                        elif len(section_parameters) == 12:
                                
                                pipe_section_info = {   "section_type_label" : "Pipe section" ,
                                                        "section_parameters" : section_parameters  }

                                self.variable_sections_data[tag, "pipe"] = pipe_section_info
        
                    
                        if str_joint_parameters != "" and str_joint_stiffness != "":
                            _data = [joint_parameters, joint_stiffness, joint_table_names, joint_list_freq]
                            self.expansion_joint_parameters_data[tag] = _data

        except Exception as error_log:

            title = "Error while loading cross-section data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_element_type_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)

        try:
            
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                list_elements = ""
                acoustic_element_type = ""
                structural_element_type = ""

                if 'structural element type' in keys:
                    structural_element_type = section['structural element type']
                
                if structural_element_type != "":
                    if 'list of elements' in keys:
                        if "-" in tag:
                            str_list_elements = section['list of elements']
                            list_elements = get_list_of_values_from_string(str_list_elements)
                            self.structural_element_type_data[tag] = [list_elements, structural_element_type]
                    else:
                        self.structural_element_type_data[tag] = structural_element_type
                    self.element_type_is_structural = True
                else:
                    self.structural_element_type_data[tag] = 'pipe_1'

                if 'structural element wall formulation' in keys:
                    wall_formulation = section['structural element wall formulation']
                    if wall_formulation != "":
                        if "-" in tag:
                            if 'list of elements' in keys:
                                str_list_elements = section['list of elements']
                                list_elements = get_list_of_values_from_string(str_list_elements)
                                self.structural_element_wall_formulation_data[tag] = [list_elements, wall_formulation]
                        else:
                            self.structural_element_wall_formulation_data[tag] = wall_formulation
                        self.element_type_is_structural = True
                    else:
                        self.structural_element_wall_formulation_data[tag] = 'thick_wall'

                if 'force offset' in keys:
                    force_offset = section['force offset']
                    if force_offset != "":
                        if "-" in tag:
                            if 'list of elements' in keys:
                                str_list_elements = section['list of elements']
                                list_elements = get_list_of_values_from_string(str_list_elements)
                                self.structural_element_force_offset_data[tag] = [list_elements, int(force_offset)]
                        else:
                            self.structural_element_force_offset_data[tag] = int(force_offset)
                        self.element_type_is_structural = True
                    else:
                        self.structural_element_force_offset_data[tag] = None

                if 'acoustic element type' in keys:
                    acoustic_element_type = section['acoustic element type']
                
                if acoustic_element_type != "":
                    if acoustic_element_type == 'proportional':
                        proportional_damping = section['proportional damping']
                        self.acoustic_element_type_data[int(tag)] = [acoustic_element_type, float(proportional_damping), None]
                    elif acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                        vol_flow = section['volume flow rate']
                        self.acoustic_element_type_data[int(tag)] = [acoustic_element_type, None, float(vol_flow)]
                    else:
                        self.acoustic_element_type_data[int(tag)] = [acoustic_element_type, None, None]
                    self.element_type_is_acoustic = True
                else:
                    self.acoustic_element_type_data[int(tag)] = ['undamped', None, None]
        
        except Exception as error_log:

            title = "Error while loading element type data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_valve_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)
   
        try:
            
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                structural_element_type = ""
                                                        
                valve_data = {}
                dict_element_to_diameters = {}
                valve_section_parameters = []
                flange_section_parameters = []
                valve_cross, flange_cross = [], []
                number_valve_elements = 0
                number_flange_elements = 0

                if 'structural element type' in keys:
                    structural_element_type = section["structural element type"]

                if structural_element_type == "valve":

                    if "valve parameters" in keys:
                        str_valve_parameters = section['valve parameters']
                        valve_parameters = get_list_of_values_from_string(str_valve_parameters, int_values=False)
                        [valve_length, stiffening_factor, valve_mass] = valve_parameters
                        valve_data["valve_length"] = valve_length
                        valve_data["stiffening_factor"] = stiffening_factor
                        valve_data["valve_mass"] = valve_mass
                    
                    if "valve center coordinates" in keys:
                        str_valve_coord = section['valve center coordinates']
                        valve_data["valve_center_coordinates"] = get_list_of_values_from_string(str_valve_coord, int_values=False)
                    
                    if "valve section parameters" in keys:
                        str_valve_section_parameters = section['valve section parameters'] 
                        valve_section_parameters = get_list_of_values_from_string(str_valve_section_parameters, int_values=False)
                    
                    if "flange section parameters" in keys:
                        str_flange_section_parameters = section['flange section parameters']
                        flange_section_parameters = get_list_of_values_from_string(str_flange_section_parameters, int_values=False)
                    
                    if 'list of elements' in keys:
                        str_valve_list_elements = section['list of elements']
                        valve_data["valve_elements"] = get_list_of_values_from_string(str_valve_list_elements)
                        number_valve_elements = len(valve_data["valve_elements"])
                        
                    if 'number of flange elements' in keys:
                        str_number_flange_elements = section['number of flange elements']
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
                        self.valve_data[tag] = [valve_data, cross_sections]

        except Exception as error_log:

            title = "Error while loading valves data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_compressor_info_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)

        try:
            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                if 'compressor info' in keys:
                    str_compressor_info = section['compressor info']
                    _data = get_list_of_values_from_string(str_compressor_info, int_values=False)
                    self.compressor_info[int(tag)] = {  "temperature (suction)" : _data[0],
                                                        "pressure (suction)" : _data[1],
                                                        "line_id" : int(_data[2]),
                                                        "node_id" : int(_data[3]),
                                                        "pressure ratio" : _data[4],
                                                        "connection type" : int(_data[5])  }

        except Exception as error_log:

            title = "Error while loading compressor info data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_capped_end_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)
        
        try:

            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()
        
                if 'capped end' in keys:
                    capped_end = section['capped end']
                    if capped_end != "":
                        self.capped_end_data[capped_end].append(int(tag))

        except Exception as error_log:

            title = "Error while loading capped-end data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_stress_stiffening_data_from_file(self):

        entity_file = configparser.ConfigParser()
        entity_file.read(self.file._entity_path)
        
        try:

            for tag in entity_file.sections():

                section = entity_file[tag]
                keys = section.keys()

                if 'stress stiffening parameters' in keys:
                    list_parameters = section['stress stiffening parameters']
                    _list_parameters = get_list_of_values_from_string(list_parameters, int_values=False)
                    self.stress_stiffening_data[int(tag)] = _list_parameters

        except Exception as error_log:

            title = "Error while loading stress-stiffening data from file"
            message = str(error_log)
            message += f"\n\nProblem detected at line: {tag}"
            PrintMessageInput([window_title_1, title, message])


    def load_elements_data_from_file(self):

        element_file = configparser.ConfigParser()
        element_file.read(self.file._element_info_path)

        for section in list(element_file.sections()):

            try:
                if "ACOUSTIC ELEMENT LENGTH CORRECTION" in section:
                    if 'length correction type' in  element_file[section].keys():
                        length_correction_type = int(element_file[section]['length correction type'])   
                    if 'list of elements' in  element_file[section].keys():
                        list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(list_elements)
                    if length_correction_type in [0,1,2] and get_list_elements != []:
                        self.element_length_correction_data[section] = [get_list_elements, length_correction_type]
            except Exception as log_error:  
                title = "Error while loading acoustic element length correction from file"
                message = str(log_error)
                PrintMessageInput([window_title, title, message])

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

                            bc_data = self.file._get_acoustic_bc_from_string(   dimensionless_data, 
                                                                                "dimensionless impedance", 
                                                                                "perforated_plate_files"   )
                            [dim_impedance, dim_impedance_table_name, frequencies] = bc_data
                            perforated_plate.dimensionless_impedance = dim_impedance 
                            perforated_plate.dimensionless_impedance_table_name = dim_impedance_table_name
                            
                        self.perforated_plate_data[section] = [get_list_elements, perforated_plate, frequencies]
            
            except Exception as log_error:  
                window_title = "Error while loading acoustic element perforated plate from file"
                message = str(log_error)
                PrintMessageInput([window_title, title, message])

            try:
                if "CAPPED END" in section:
                    if 'list of elements' in element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(_list_elements)
                        self.capped_end_data[section] = get_list_elements
            except Exception as err:  
                title = "Error while loading capped-end data from file"
                message = str(err)
                PrintMessageInput([window_title, title, message])

            try:
                if "STRESS STIFFENING" in section:
                    if 'stress stiffening parameters' in  element_file[section].keys():
                        _list_parameters = element_file[section]['stress stiffening parameters']
                        get_list_parameters = get_list_of_values_from_string(_list_parameters, int_values=False)
                    if 'list of elements' in  element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = get_list_of_values_from_string(_list_elements)
                    self.stress_stiffening_data[section] = [get_list_elements, get_list_parameters]
            except Exception as err: 
                title = "Error while loading stress stiffening from file" 
                message = str(err)
                PrintMessageInput([window_title, title, message])

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
                    self.B2XP_rotation_decoupling_data[section] = [get_list_elements, get_list_nodes, get_dofs_mask]
            except Exception as err: 
                title = "Error while loading B2PX rotationg decoupling from file" 
                message = str(err)
                PrintMessageInput([window_title, title, message]) 
    
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
                        expansion_joints_tables_folder_path = get_new_path( self.file._structural_imported_data_folder_path, 
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
                        PrintMessageInput([window_title_1, title, message])
                        return None, None, None

        return output, list_table_names, list_frequencies
