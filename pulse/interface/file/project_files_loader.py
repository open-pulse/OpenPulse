
from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse.model.perforated_plate import PerforatedPlate
from pulse.model.cross_section import CrossSection, get_beam_section_properties

from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.file.project_file import ProjectFile
from pulse.tools.utils import *

from pulse import app

import configparser
from collections import defaultdict
from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class ProjectFilesLoader:
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.file = app().file
        self._initialize()
        
    def _initialize(self):
        self.element_type_is_acoustic = False
        self.element_type_is_structural = False

    def load_project_data_from_files(self):
        t0 = time()

        # self.pipeline_data = app().pulse_file.read_pipeline_data_from_file()

        self.initialize_dictionaries_for_load_data()
        self.load_valve_data_from_file()
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

    def load_valve_data_from_file(self):

        try:
            
            for tag in self.pipeline_data.sections():

                section = self.pipeline_data[tag]
                keys = section.keys()

                structural_element_type = ""
                number_valve_elements = 0
                number_flange_elements = 0

                valve_data = dict()
                dict_element_to_diameters = dict()
                valve_section_parameters = list()
                flange_section_parameters = list()
                valve_cross, flange_cross = list(), list()

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

                    if len(valve_section_parameters) == 6:
                        valve_data["valve_section_parameters"] = valve_section_parameters
                        valve_section_info = {  "section_type_label" : "Valve section",
                                                "section_parameters" : valve_section_parameters  }
                                            
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

                        dict_outer_diameters = dict(zip(list_valve_elements, np.round(list_outer_diameters, 6)))                      
                        dict_inner_diameters = dict(zip(list_valve_elements, np.round(list_inner_diameters, 6)))

                        for _id in list_inner_elements:
                            dict_element_to_diameters[_id] = [dict_outer_diameters[_id], dict_inner_diameters[_id]]
                            valve_section_info["diameters_to_plot"] = dict_element_to_diameters[_id]
                            valve_cross.append(CrossSection(valve_section_info = valve_section_info)) 

                    if len(flange_section_parameters) == 6:
                        valve_data["flange_section_parameters"] = flange_section_parameters
                        flange_section_info = { "section_type_label" : "Valve section",
                                                "section_parameters" : flange_section_parameters }

                        for _id in list_flange_elements:
                            dict_element_to_diameters[_id] = [dict_outer_diameters[_id], dict_inner_diameters[_id]]   
                            flange_section_info["diameters_to_plot"] = dict_element_to_diameters[_id]       
                            flange_cross.append(CrossSection(valve_section_info = flange_section_info))
                    
                    valve_data["valve_diameters"] = dict_element_to_diameters

                    if valve_data:
                        cross_sections = [valve_cross, flange_cross] 
                        self.valve_data[tag] = [valve_data, cross_sections]

        except Exception as error_log:

            title = "Error while loading valves data from file"
            message = f"Problem detected at line: {tag}\n\n"
            message += str(error_log)
            PrintMessageInput([window_title_1, title, message])


    def load_elements_data_from_file(self):

        element_file = configparser.ConfigParser()
        element_file.read(self.file._element_info_path)

        for section in list(element_file.sections()):

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
                title = "Error while loading acoustic element perforated plate from file"
                message = str(log_error)
                PrintMessageInput([window_title_1, title, message])