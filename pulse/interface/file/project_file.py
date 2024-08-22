
from pulse.tools.utils import *

import os
import configparser

window_title = "Error"

class ProjectFile:
    def __init__(self):
        self.reset()

    def reset(self):
        pass

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