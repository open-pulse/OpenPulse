from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.uix.user_input.project.printMessageInput import PrintMessageInput
from pulse.utils import error, remove_bc_from_file
import configparser
from collections import defaultdict
import os
import numpy as np
from math import pi

window_title = "ERROR"

class ProjectFile:
    def __init__(self):
        self._project_name = ""
        self._import_type = 0
        self._section = 0
        self._project_path = ""
        self._material_list_path = ""
        self._fluid_list_path = ""
        self._geometry_path = ""
        self._conn_path = ""
        self._coord_path = ""
        self._node_structural_path = ""
        self._node_acoustic_path = ""
        self._entity_path = ""
        self._element_info_path = ""
        self._analysis_path = ""
        self.temp_table_name = None
        self.lines_multiples_cross_sections = []

        self.element_type_is_structural = False

        self._entity_file_name = "entity.dat"
        self._node_structural_file_name = "structural_nodal_info.dat"
        self._node_acoustic_file_name = "acoustic_nodal_info.dat"
        self._elements_file_name = "elements_info.dat"
        self._project_base_name = "project.ini"

    def _reset(self):
        self._project_name = ""
        self._import_type = 0
        self._project_path = ""
        self._material_list_path = ""
        self._fluid_list_path = ""
        self._geometry_path = ""
        self._conn_path = ""
        self._coord_path = ""
        self._node_structural_path = ""
        self._node_acoustic_path = ""
        self.element_type_is_structural = False
        self.lines_multiples_cross_sections = []

    def new(self, project_path, project_name, element_size, import_type, material_list_path, fluid_list_path, geometry_path = "", coord_path = "", conn_path = ""):
        self._project_path = project_path
        self._project_name = project_name
        self._element_size = float(element_size)
        self._import_type = int(import_type)
        self._material_list_path = material_list_path
        self._fluid_list_path = fluid_list_path
        self._geometry_path = geometry_path
        self._conn_path = conn_path
        self._coord_path = coord_path
        self._entity_path = "{}\\{}".format(self._project_path, self._entity_file_name)
        self._node_structural_path = "{}\\{}".format(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path = "{}\\{}".format(self._project_path, self._node_acoustic_file_name)

    def load(self, project_file_path):
        self.project_file_path = project_file_path
        project_file_path = project_file_path.replace('/', '\\')
        project_folder_path = os.path.dirname(project_file_path)
        self._project_path = project_folder_path
                
        config = configparser.ConfigParser()
        config.read(project_file_path)

        project_name = config['PROJECT']['Name']
        import_type = int(config['PROJECT']['Import type'])

        if import_type == 0:
            element_size = config['PROJECT']['Element size']
            geometry_file = config['PROJECT']['Geometry file']
            self._element_size = float(element_size)
            self._geometry_path = "{}\\{}".format(self._project_path, geometry_file)

        elif import_type == 1:
            coord_file = config['PROJECT']['Nodal coordinates file']
            conn_file = config['PROJECT']['Connectivity matrix file']
            self._conn_path = "{}\\{}".format(self._project_path, conn_file)
            self._coord_path = "{}\\{}".format(self._project_path, coord_file)

        material_list_file = config['PROJECT']['Material list file']
        fluid_list_file = config['PROJECT']['Fluid list file']

        self._project_name = project_name
        self._import_type = import_type
        self._material_list_path = "{}\\{}".format(self._project_path, material_list_file)
        self._fluid_list_path = "{}\\{}".format(self._project_path, fluid_list_file)
        self._entity_path = "{}\\{}".format(self._project_path, self._entity_file_name)
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)
        self._node_structural_path = "{}\\{}".format(self._project_path, self._node_structural_file_name)
        self._node_acoustic_path = "{}\\{}".format(self._project_path, self._node_acoustic_file_name)

    #Frequency Setup Analysis
    def load_analysis_file(self):
        f_min = 0
        f_max = 0
        f_step = 0
        alpha_v, beta_v = 0, 0
        alpha_h, beta_h = 0, 0
        
        temp_project_base_file_path = "{}\\{}".format(self._project_path, self._project_base_name)
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

    def add_frequency_in_file(self, min_, max_, step_):
        min_ = str(min_)
        max_ = str(max_)
        step_ = str(step_)
        temp_project_base_file_path = "{}\\{}".format(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        # sections = config.sections()
        config["Frequency setup"] = {}
        config['Frequency setup']['frequency min'] = min_
        config['Frequency setup']['frequency max'] = max_
        config['Frequency setup']['frequency step'] = step_

        with open(temp_project_base_file_path, 'w') as config_file:
            config.write(config_file)

    def add_damping_in_file(self, global_damping):

        alpha_v = str(global_damping[0])
        beta_v = str(global_damping[1])
        alpha_h = str(global_damping[2])
        beta_h = str(global_damping[3])
        temp_project_base_file_path = "{}\\{}".format(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)

        config['Global damping setup'] = {}
        config['Global damping setup']['alpha_v'] = alpha_v
        config['Global damping setup']['beta_v'] = beta_v
        config['Global damping setup']['alpha_h'] = alpha_h
        config['Global damping setup']['beta_h'] = beta_h

        with open(temp_project_base_file_path, 'w') as config_file:
            config.write(config_file)

    def reset_project_setup(self):
        temp_project_base_file_path = "{}\\{}".format(self._project_path, self._project_base_name)
        config = configparser.ConfigParser()
        config.read(temp_project_base_file_path)
        sections = config.sections()

        if "Frequency setup" in sections:
            config.remove_section("Frequency setup")

        if "Global damping setup" in sections:
            config.remove_section("Global damping setup")
        
        with open(temp_project_base_file_path, 'w') as config_file:
            config.write(config_file)

    def create_entity_file(self, entities):
        config = configparser.ConfigParser()
        for entity_id in entities:
            config[str(entity_id)] = {}

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)
    
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
        self.dict_structural_element_type = {}
        self.dict_acoustic_element_type = {}
        self.dict_fluid = {}
        self.dict_length_correction = {}
        self.temp_dict = {}
        self.dict_stress_stiffening = {}
        self.dict_capped_end = defaultdict(list)
        self.dict_B2XP_rotation_decoupling = {}

        title = "ERROR WHILE LOADING DATA FROM FILE"

        for entity in entityFile.sections():

            if 'structural element type' in entityFile[entity].keys():
                structural_element_type = entityFile[entity]['structural element type']
                if structural_element_type != "":
                    self.dict_structural_element_type[int(entity)] = structural_element_type
                    self.element_type_is_structural = True
                else:
                    self.dict_structural_element_type[int(entity)] = 'pipe_1'
            
            if 'acoustic element type' in entityFile[entity].keys():
                acoustic_element_type = entityFile[entity]['acoustic element type']
                if acoustic_element_type != "":
                    if acoustic_element_type == 'hysteretic':
                        hysteretic_damping = entityFile[entity]['hysteretic damping']
                        self.dict_acoustic_element_type[int(entity)] = [acoustic_element_type, float(hysteretic_damping)]
                    else:
                        self.dict_acoustic_element_type[int(entity)] = [acoustic_element_type, None]
                    self.element_type_is_acoustic = True
                else:
                    self.dict_acoustic_element_type[int(entity)] = 'dampingless'

            diam_ext = ""
            thickness = ""
            offset_y, offset_z = 0., 0.
            insulation_thickness = 0.
            insulation_density = 0.

            if "-" in entity:
                if 'outer diameter' in entityFile[entity].keys():
                    diam_ext = entityFile[entity]['outer diameter']
                if 'thickness' in entityFile[entity].keys():
                    thickness = entityFile[entity]['thickness']
                if 'offset [e_y, e_z]' in entityFile[entity].keys():
                    offset = entityFile[entity]['offset [e_y, e_z]']
                    offset_y, offset_z = self._get_offset_from_string(offset) 
                if 'insulation thickness' in entityFile[entity].keys():
                    insulation_thickness = entityFile[entity]['insulation thickness']
                if 'insulation density' in entityFile[entity].keys():
                    insulation_density = entityFile[entity]['insulation density']
                if 'list of elements (cross-sections)' in entityFile[entity].keys():
                    list_elements = entityFile[entity]['list of elements (cross-sections)']
                    get_list_elements = self._get_list_of_values_from_string(list_elements)
    
                if diam_ext!="" and thickness!="":
                    try:
                        diam_ext = float(diam_ext)
                        thickness = float(thickness)
                        offset_y = float(offset_y)
                        offset_z = float(offset_z)
                        insulation_thickness = float(insulation_thickness)
                        insulation_density = float(insulation_density)
                        cross = CrossSection(diam_ext, thickness, offset_y, offset_z, insulation_thickness=insulation_thickness, insulation_density=insulation_density)
                        self.dict_cross[entity] = [cross, get_list_elements]
                    except Exception as er:
                        title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                        message = str(er)
                        PrintMessageInput([title, message, window_title])

            else:

                area, Iyy, Izz, Iyz, section_type, section_parameters = "", "", "", "", "", ""

                if 'area' in entityFile[entity].keys():
                    area = entityFile[entity]['area']
                if 'second moment of area y' in entityFile[entity].keys():
                    Iyy = entityFile[entity]['second moment of area y']
                if 'second moment of area z' in entityFile[entity].keys():
                    Izz = entityFile[entity]['second moment of area z']
                if 'second moment of area yz' in entityFile[entity].keys():
                    Iyz = entityFile[entity]['second moment of area yz']
                if 'beam section type' in entityFile[entity].keys():
                    section_type = entityFile[entity]['beam section type']
                if 'section parameters' in entityFile[entity].keys():
                    section_parameters = entityFile[entity]['section parameters']
                if 'shear coefficient' in entityFile[entity].keys():
                    shear_coefficient = entityFile[entity]['shear coefficient']

                if not "" in [area, Iyy, Izz, section_type]:

                    try:

                        area = float(area)
                        Iyy = float(Iyy)
                        Izz = float(Izz)
                        Iyz = float(Iyz)
                        external_diameter = 2*np.abs(np.sqrt(area/np.pi))

                        _shear_coefficient = [float(shear_coefficient) if "Generic section" in section_type else None]

                        if "Generic" not in section_type:
                            list_section_parameters = self._get_list_of_values_from_string(section_parameters, are_values_int=False)
                        else:
                            list_section_parameters = None
                            shear_coefficient = float(shear_coefficient)
                        cross = CrossSection(   external_diameter, 0, 0, 0, area=area, Iyy=Iyy, Izz=Izz, Iyz=Iyz, 
                                                additional_section_info=[section_type, list_section_parameters], 
                                                shear_coefficient=_shear_coefficient[0])
                        
                        self.dict_cross[entity] = cross
                        
                    except Exception as er:
                        title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                        message = str(er)
                        PrintMessageInput([title, message, window_title])
                
                if 'outer diameter' in entityFile[entity].keys():
                    diam_ext = entityFile[entity]['outer Diameter']
                if 'thickness' in entityFile[entity].keys():    
                    thickness = entityFile[entity]['thickness']
                if 'offset [e_y, e_z]' in entityFile[entity].keys(): 
                    offset = entityFile[entity]['offset [e_y, e_z]']
                    offset_y, offset_z = self._get_offset_from_string(offset) 
                if 'insulation thickness' in entityFile[entity].keys():
                    insulation_thickness = entityFile[entity]['insulation thickness']
                if 'insulation density' in entityFile[entity].keys():
                    insulation_density = entityFile[entity]['insulation density']
                        
                if diam_ext != "" and thickness != "":
                    try:
                        diam_ext = float(diam_ext)
                        thickness = float(thickness)
                        offset_y = float(offset_y)
                        offset_z = float(offset_z)
                        insulation_thickness = float(insulation_thickness)
                        insulation_density = float(insulation_density)
                        section_info = ["Pipe section", [diam_ext, thickness, offset_y, offset_z, insulation_thickness]]
                        cross = CrossSection(   diam_ext, thickness, offset_y, offset_z, 
                                                insulation_thickness=insulation_thickness, 
                                                insulation_density=insulation_density, 
                                                additional_section_info=section_info)
                        self.dict_cross[entity] = cross
                    except Exception as er:
                        title = "ERROR WHILE LOADING CROSS-SECTION PARAMETERS FROM FILE"
                        message = str(er)
                        PrintMessageInput([title, message, window_title])
                    
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
                            fluid_density =  fluid_list[fluid]['fluid density']
                            speed_of_sound =  fluid_list[fluid]['speed of sound']
                            
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
                            temp_fluid = Fluid(name,
                                               float(fluid_density),
                                               float(speed_of_sound),
                                               isentropic_exponent = isentropic_exponent,
                                               thermal_conductivity = thermal_conductivity,
                                               specific_heat_Cp = specific_heat_Cp,
                                               dynamic_viscosity = dynamic_viscosity,
                                               color=color, identifier=int(identifier))
                            self.dict_fluid[int(entity)] = temp_fluid
                                
                if 'capped end' in entityFile[entity].keys():
                    capped_end = entityFile[entity]['capped end']
                    if capped_end != "":
                        self.dict_capped_end[capped_end].append(int(entity))
            
            if 'stress stiffening parameters' in entityFile[entity].keys():
                list_parameters = entityFile[entity]['stress stiffening parameters']
                _list_parameters = self._get_list_of_values_from_string(list_parameters, are_values_int=False)
                try:
                    self.dict_stress_stiffening[int(entity)] = _list_parameters
                except Exception as er:
                    window_title = "ERROR WHILE LOADING STRESS STIFFENING FROM FILE"
                    message = str(er)
                    PrintMessageInput([title, message, window_title])

        for section in list(element_file.sections()):

            try:
                if "ACOUSTIC ELEMENT LENGTH CORRECTION" in section:
                    if 'length correction type' in  element_file[section].keys():
                        length_correction_type = int(element_file[section]['length correction type'])   
                    if 'list of elements' in  element_file[section].keys():
                        list_elements = element_file[section]['list of elements']
                        get_list_elements = self._get_list_of_values_from_string(list_elements)
                    if length_correction_type in [0,1,2] and get_list_elements != []:
                        self.dict_length_correction[section] = [get_list_elements, length_correction_type]
            except Exception as er:  
                window_title = "ERROR WHILE LOADING ACOUSTIC ELEMENT LENGTH CORRECTION FROM FILE"
                message = str(er)
                PrintMessageInput([title, message, window_title])

            try:
                if "CAPPED END" in section:
                    if 'list of elements' in element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = self._get_list_of_values_from_string(_list_elements)
                        self.dict_capped_end[section] = get_list_elements
            except Exception as er:  
                window_title = "ERROR WHILE LOADING CAPPED END FROM FILE"
                message = str(er)
                PrintMessageInput([title, message, window_title])

            try:
                if "STRESS STIFFENING" in section:
                    if 'stress stiffening parameters' in  element_file[section].keys():
                        _list_parameters = element_file[section]['stress stiffening parameters']
                        get_list_parameters = self._get_list_of_values_from_string(_list_parameters, are_values_int=False)
                    if 'list of elements' in  element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = self._get_list_of_values_from_string(_list_elements)
                    self.dict_stress_stiffening[section] = [get_list_elements, get_list_parameters]
            except Exception as er: 
                window_title = "ERROR WHILE LOADING STRESS STIFFENING FROM FILE" 
                message = str(er)
                PrintMessageInput([title, message, window_title])

            try:
                if "B2PX ROTATION DECOUPLING" in section:
                    if 'list of elements' in  element_file[section].keys():
                        _list_elements = element_file[section]['list of elements']
                        get_list_elements = self._get_list_of_values_from_string(_list_elements)
                    if 'list of nodes' in  element_file[section].keys():
                        _list_nodes = element_file[section]['list of nodes']
                        get_list_nodes = self._get_list_of_values_from_string(_list_nodes)
                    if 'rotation dofs mask' in  element_file[section].keys():
                        _dofs_mask = element_file[section]['rotation dofs mask']
                        get_dofs_mask = self._get_list_bool_from_string(_dofs_mask)
                    self.dict_B2XP_rotation_decoupling[section] = [get_list_elements, get_list_nodes, get_dofs_mask]
            except Exception as er: 
                window_title = "ERROR WHILE LOADING B2PX ROTATION DECOUPLING FROM FILE" 
                message = str(er)
                PrintMessageInput([title, message, window_title])
                

    def add_cross_section_in_file(self, entity_id, cross_section):   
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for section in list(config.sections()):
            section_sub = str(entity_id) + '-'
            if section_sub in section:
                config.remove_section(section)
    
        if cross_section.thickness == 0:
            if str(entity_id) in list(config.sections()):
                
                config.remove_option(section=str(entity_id), option='outer diameter')
                config.remove_option(section=str(entity_id), option='thickness')
                config.remove_option(section=str(entity_id), option='offset [e_y, e_z]')
                config.remove_option(section=str(entity_id), option='insulation thickness')
                config.remove_option(section=str(entity_id), option='insulation density')
                config.remove_option(section=str(entity_id), option='section parameters'),
                config.remove_option(section=str(entity_id), option='shear coefficient')

                config[str(entity_id)]['area'] = str(cross_section.area)
                config[str(entity_id)]['second moment of area y'] = str(cross_section.second_moment_area_y)
                config[str(entity_id)]['second moment of area z'] = str(cross_section.second_moment_area_z)
                config[str(entity_id)]['second moment of area yz'] = str(cross_section.second_moment_area_yz)
                config[str(entity_id)]['beam section type'] = cross_section.additional_section_info[0]
                
                if not "Generic" in cross_section.additional_section_info[0]:
                    config[str(entity_id)]['section parameters'] = str(cross_section.additional_section_info[1])
                else:
                    config[str(entity_id)]['shear coefficient'] = str(cross_section.shear_coefficient)
              
        else:

            config.remove_option(section=str(entity_id), option='area')
            config.remove_option(section=str(entity_id), option='second moment of area y')
            config.remove_option(section=str(entity_id), option='second moment of area z')
            config.remove_option(section=str(entity_id), option='second moment of area yz')
            config.remove_option(section=str(entity_id), option='beam section type')
            config.remove_option(section=str(entity_id), option='section parameters')
            config.remove_option(section=str(entity_id), option='shear coefficient')

            if str(entity_id) in list(config.sections()):

                config[str(entity_id)]['outer diameter'] = str(cross_section.external_diameter)
                config[str(entity_id)]['thickness'] = str(cross_section.thickness)
                config[str(entity_id)]['offset [e_y, e_z]'] = str(cross_section.offset)
                config[str(entity_id)]['insulation thickness'] = str(cross_section.insulation_thickness)
                config[str(entity_id)]['insulation density'] = str(cross_section.insulation_density)
 
        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_multiple_cross_section_in_file(self, lines, map_cross_sections_to_elements):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        for line in [lines]:
            subkey = 0
            for str_key in ['outer diameter', 'thickness', 'offset [e_y, e_z]', 'insulation thickness', 'insulation density']:
                if str_key in list(config[str(line)].keys()):
                    config.remove_option(section=str(line), option=str_key)

            for key, elements in map_cross_sections_to_elements.items():
                
                self.lines_multiples_cross_sections.append(int(line))
                
                cross_strings = key[1:-1].split(',')
                vals = [float(value) for value in cross_strings] 

                subkey += 1
                key = str(line) + "-" + str(subkey)

                if key in config.sections():
                    config[key]['outer diameter'] = '{}'.format(vals[0])
                    config[key]['thickness'] = '{}'.format(vals[1])
                    config[key]['offset [e_y, e_z]'] = '[{}, {}]'.format(vals[2],vals[3])
                    config[key]['insulation thickness'] = '{}'.format(vals[4])
                    config[key]['insulation density'] = '{}'.format(vals[5])
                    config[key]['list of elements (cross-sections)'] = '{}'.format(elements)
                else:
                    config[key] = { 'outer diameter': '{}'.format(vals[0]),
                                    'thickness': '{}'.format(vals[1]),
                                    'offset [e_y, e_z]': '[{}, {}]'.format(vals[2],vals[3]),
                                    'insulation thickness': '{}'.format(vals[4]),
                                    'insulation density': '{}'.format(vals[5]),
                                    'list of elements (cross-sections)': '{}'.format(elements) }

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_length_correction_in_file(self, elements, _type, section): 
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)  
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if section in list(config.sections()):
            config[section]['length correction type'] = str(_type)
            config[section]['list of elements'] = str(elements)
        else:
            config[section] =   { 
                                  'length correction type': str(_type),
                                  'list of elements': str(elements)
                                }
        with open(self._element_info_path, 'w') as config_file:
            config.write(config_file)
    
    def modify_B2PX_rotation_decoupling_in_file(self, elements, nodes, rotations_maks, section, remove=False, reset=False):
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)  
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

        with open(self._element_info_path, 'w') as config_file:
            config.write(config_file)

    def modify_stress_stiffnening_entity_in_file(self, entity_id, parameters, remove=False,): 
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        if remove:
            if str(entity_id) in list(config.sections()):
                config.remove_option(section=str(entity_id), option='stress stiffening parameters')
        else:
            if str(entity_id) in list(config.sections()):
                config[str(entity_id)]['stress stiffening parameters'] = str(parameters)
            else:
                config[str(entity_id)] = { 'stress stiffening parameters': str(parameters) }  

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def modify_stress_stiffnening_element_in_file(self, elements, parameters, section, remove=False):
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)  
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if remove:
            config.remove_section(section)
        else:
            if section in list(config.sections()):
                config[section]['stress stiffening parameters'] = str(parameters)
                config[section]['list of elements'] = str(elements)
            else:
                config[section] =  { 'stress stiffening parameters': str(parameters),
                                     'list of elements': str(elements)                }

        with open(self._element_info_path, 'w') as config_file:
            config.write(config_file)

    def remove_all_stress_stiffnening_in_file_by_group_elements(self): 
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)  
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        for section in list(config.sections()):
            if "STRESS STIFFENING" in section:
                config.remove_section(section)

        with open(self._element_info_path, 'w') as config_file:
            config.write(config_file)

    def modify_capped_end_element_in_file(self, elements, value, section): 
        self._element_info_path = "{}\\{}".format(self._project_path, self._elements_file_name)  
        config = configparser.ConfigParser()
        config.read(self._element_info_path)

        if value:
            if section in list(config.sections()):
                config[section]['list of elements'] = str(elements)
            else:
                config[section] =   { 'list of elements': str(elements) }
        else:    
            config.remove_section(section)
        
        with open(self._element_info_path, 'w') as config_file:
            config.write(config_file)

    def modify_capped_end_entity_in_file(self, entity_id, value):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        if value:    
            if str(entity_id) in list(config.sections()):
                config[str(entity_id)]['capped end'] = str(value)
            else:
                config[str(entity_id)] = { 'capped end': str(value) }
        else:
            config.remove_option(section=str(entity_id), option='capped end')

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def modify_structural_element_type_in_file(self, entity_id, element_type):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        config[str(entity_id)]['structural element type'] = element_type

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def modify_acoustic_element_type_in_file(self, entity_id, element_type, hysteretic_damping=None):
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        _section = str(entity_id)

        config[_section]['acoustic element type'] = element_type
        if element_type == 'hysteretic':
            config[_section]['hysteretic damping'] = str(hysteretic_damping)
            
        if element_type != 'hysteretic' and 'hysteretic damping' in config[_section].keys():
            config.remove_option(section=_section, option='hysteretic damping')  
    
        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_material_in_file(self, entity_id, material_id):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        config[str(entity_id)]['material id'] = str(material_id)
        
        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_fluid_in_file(self, entity_id, fluid_id):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        config[str(entity_id)]['fluid id'] = str(fluid_id)
        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def get_dict_of_structural_bc_from_file(self):

        node_structural_list = configparser.ConfigParser()
        node_structural_list.read(self._node_structural_path)

        self.dict_prescribed_dofs = {}
        self.dict_nodal_loads = {}
        self.dict_lumped_inertia = {}
        self.dict_lumped_stiffness = {}
        self.dict_lumped_damping = {}
        self.dict_elastic_link_stiffness = {}
        self.dict_elastic_link_damping = {}

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
                prescribed_dofs = self._get_structural_bc_from_string(displacement_strings, rotation_strings, labels)
                if prescribed_dofs is not None:
                    self.dict_prescribed_dofs[node_id] = prescribed_dofs
                               
            if "forces" in keys and "moments" in keys:
                forces_strings = node_structural_list[str(node)]['forces'] 
                moments_strings = node_structural_list[str(node)]['moments']
                labels = [["Fx","Fy","Fz"],["Mx","My","Mz"]]
                nodal_loads = self._get_structural_bc_from_string(forces_strings, moments_strings, labels)
                if nodal_loads is not None:
                    self.dict_nodal_loads[node_id] = nodal_loads
            
            if "masses" in keys and "moments of inertia" in keys:
                masses = node_structural_list[str(node)]['masses']
                moments_of_inertia = node_structural_list[str(node)]['moments of inertia']
                labels = [["m_x","m_y","m_z"],["Jx","Jy","Jz"]]
                lumped_inertia = self._get_structural_bc_from_string(masses, moments_of_inertia, labels, _complex=False)
                if lumped_inertia is not None:
                    self.dict_lumped_inertia[node_id] = lumped_inertia

            if "spring stiffness" in keys and "torsional spring stiffness" in keys:
                spring_stiffness = node_structural_list[str(node)]['spring stiffness']
                torsional_spring_stiffness = node_structural_list[str(node)]['torsional spring stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                lumped_stiffness = self._get_structural_bc_from_string(spring_stiffness, torsional_spring_stiffness, labels, _complex=False)
                if lumped_stiffness is not None:
                    self.dict_lumped_stiffness[node_id] = lumped_stiffness

            if "damping coefficients" in keys and "torsional damping coefficients":
                damping_coefficients = node_structural_list[str(node)]['damping coefficients']
                torsional_damping_coefficients = node_structural_list[str(node)]['torsional damping coefficients']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                lumped_damping = self._get_structural_bc_from_string(damping_coefficients, torsional_damping_coefficients, labels, _complex=False)
                if lumped_damping is not None:
                    self.dict_lumped_damping[node_id] = lumped_damping

            if "connecting stiffness" in keys and "connecting torsional stiffness" in keys:
                connecting_stiffness = node_structural_list[str(node)]['connecting stiffness']
                connecting_torsional_stiffness = node_structural_list[str(node)]['connecting torsional stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                connecting_stiffness = self._get_structural_bc_from_string(connecting_stiffness, connecting_torsional_stiffness, labels, _complex=False)
                if connecting_stiffness.count(None) != 6:
                    self.dict_elastic_link_stiffness[node_id] = connecting_stiffness
        
            if "connecting damping" in keys and "connecting torsional damping" in keys:
                connecting_damping = node_structural_list[str(node)]['connecting damping']
                connecting_torsional_damping = node_structural_list[str(node)]['connecting torsional damping']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                connecting_damping = self._get_structural_bc_from_string(connecting_damping, connecting_torsional_damping, labels, _complex=False)
                if connecting_damping.count(None) != 6:
                    self.dict_elastic_link_damping[node_id] = connecting_damping

        return self.dict_prescribed_dofs, self.dict_nodal_loads, self.dict_lumped_inertia, self.dict_lumped_stiffness, self.dict_lumped_damping, self.dict_elastic_link_stiffness, self.dict_elastic_link_damping

    def get_dict_of_acoustic_bc_from_file(self):

        node_acoustic_list = configparser.ConfigParser()
        node_acoustic_list.read(self._node_acoustic_path)

        dict_pressure = {}
        dict_volume_velocity = defaultdict(list)  
        dict_specific_impedance = {}
        dict_radiation_impedance = {}

        for node in node_acoustic_list.sections():
            node_id = int(node)
            keys = list(node_acoustic_list[node].keys())
            
            if "acoustic pressure" in keys:
                str_acoustic_pressure = node_acoustic_list[str(node)]['acoustic pressure']
                acoustic_pressure = self._get_acoustic_bc_from_string(str_acoustic_pressure, "acoustic pressure")
                if acoustic_pressure is not None:
                    dict_pressure[node_id] = acoustic_pressure

            for key in keys:
                if "volume velocity" in key:
                    str_volume_velocity = node_acoustic_list[str(node)][key]
                    volume_velocity = self._get_acoustic_bc_from_string(str_volume_velocity, key)
                    if volume_velocity is not None:
                        dict_volume_velocity[node_id].append(volume_velocity)

            if "specific impedance" in keys:
                str_specific_impedance = node_acoustic_list[str(node)]['specific impedance']
                specific_impedance = self._get_acoustic_bc_from_string(str_specific_impedance, "specific impedance")
                if specific_impedance is not None:
                    dict_specific_impedance[node_id] = specific_impedance

            if "radiation impedance" in keys:
                str_radiation_impedance = node_acoustic_list[str(node)]['radiation impedance']
                radiation_impedance_type = self._get_acoustic_bc_from_string(str_radiation_impedance, "radiation impedance")
                # radImpedance = self._getRadiationImpedanceBCFromString(radiation_impedance)
                if radiation_impedance_type is not None:
                    dict_radiation_impedance[node_id] = int(np.real(radiation_impedance_type))

        return dict_pressure, dict_volume_velocity, dict_specific_impedance, dict_radiation_impedance

    def _get_offset_from_string(self, offset):
        offset = offset[1:-1].split(',')
        offset_y = offset_z = 0.0
        if len(offset) == 2:
            if offset[0] != '0.0':
                offset_y = float(offset[0])
            if offset[1] != '0.0':
                offset_z = float(offset[1])
        return offset_y, offset_z

    def _get_list_bool_from_string(self, input_string):
        for text in ["[", "]", " "]:
            input_string = input_string.replace(text,"")
        list_of_strings = input_string.strip().split(",")
        list_bool = [True if item=="True" else False for item in list_of_strings]
        return list_bool

    def _get_list_of_values_from_string(self, input_string, are_values_int=True):
        
        input_string = input_string[1:-1].split(',')
        list_values = []
        
        if are_values_int:
            for value in input_string:
                list_values.append(int(value))
        else:
            for value in input_string:
                list_values.append(float(value))

        return list_values

    def _get_acoustic_bc_from_string(self, value, label):
        
        load_path_table = ""
        value = value[1:-1].split(',')
        output = None

        if len(value) == 1:
            if value[0] != 'None':
                try:
                    output = complex(value[0])
                except Exception:
                    try:
                        path = os.path.dirname(self.project_file_path)
                        if "/" in path:
                            load_path_table = "{}/{}".format(path, value[0])
                        elif "\\" in path:
                            load_path_table = "{}\\{}".format(path, value[0])
                        data = np.loadtxt(load_path_table, delimiter=",")
                        output = data[:,1] + 1j*data[:,2]
                        self.frequencies = data[:,0]
                        self.f_min = self.frequencies[0]
                        self.f_max = self.frequencies[-1]
                        self.f_step = self.frequencies[1] - self.frequencies[0]
                        self.temp_table_name = value[0]
                    except Exception:
                        message = "The loaded {} table has invalid data structure, \ntherefore, it will be ignored in analysis.".format(label) 
                        error(message, title = "LOADING TABLE ERROR")             
        return output

    def _get_structural_bc_from_string(self, first, last, labels, _complex=True):
        
        first = first[1:-1].split(',')
        last = last[1:-1].split(',')
        output = [None, None, None, None, None, None]

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
                        output[i] = self.structural_tables_load(first[i], labels[0][i])
                        output[i+3] = self.structural_tables_load(last[i], labels[1][i])
                    except Exception as err:
                        error(str(err), title = "ERROR")
        # print("Output: ", output)
        return output

    def structural_tables_load(self, table_name, label):
        output = None
        try:
            if table_name == "None":
                return output

            load_path_table = ""
            path = os.path.dirname(self.project_file_path)
            if "/" in path:
                load_path_table = "{}/{}".format(path, table_name)
            elif "\\" in path:
                load_path_table = "{}\\{}".format(path, table_name)
            data = np.loadtxt(load_path_table, delimiter=",")
            if label in ['m_x','m_y','m_z','Jx','Jy','Jz','k_x','k_y','k_z','k_rx','k_ry','k_rz','c_x','c_y','c_z','c_rx','c_ry','c_rz']:
                output = data[:,1]
            else:
                output = data[:,1] + 1j*data[:,2]

            f = open(load_path_table)
            header_read = f.readline()
            
            self.frequencies = data[:,0]
            self.f_min = self.frequencies[0]
            self.f_max = self.frequencies[-1]
            self.f_step = self.frequencies[1] - self.frequencies[0]
            self.temp_table_name = table_name

            if ('[m/s]' or '[rad/s]') in header_read:
                output = output/(2*pi*self.frequencies)
            elif ('[m/s²]' or '[rad/s²]') in header_read:
                output = output/((2*pi*self.frequencies)**2)

        except Exception: 
            message = "The loaded {} table has invalid data structure, \ntherefore, it will be ignored in analysis.".format(label)  
            error(message, title="LOADING TABLE ERROR")     
        return output
    
    def _single_structural_excitation_bc(self, node_id, labels):
        if labels[0] == 'displacements' and labels[1] == 'rotations':
            key_strings = ['forces', 'moments']
            remove_bc_from_file(node_id, self._node_structural_path, key_strings, None)
        elif labels[0] == 'forces' and labels[1] == 'moments':
            key_strings = ['displacements', 'rotations']
            remove_bc_from_file(node_id, self._node_structural_path, key_strings, None)

    def _single_acoustic_excitation_bc(self, node_id, label):
        # if label[0] == 'acoustic pressure':
        if 'acoustic pressure' in label[0]:
            key_strings = ['volume velocity']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        # elif label[0] == 'volume velocity':
        elif 'volume velocity' in  label[0]:
            key_strings = ['acoustic pressure']
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
                # if loaded_table:
                #     table_name = values
                #     config[str(node_id)][labels[0]]  = "[{},{},{}]".format(table_name[0], table_name[1], table_name[2])
                #     config[str(node_id)][labels[1]] = "[{},{},{}]".format(table_name[3], table_name[4], table_name[5])
                #     if len(labels)==3:
                #         config[str(node_id)][labels[2]]  = "{}".format(table_name[6])
                # else:
                config[str(node_id)][labels[0]]  = "[{},{},{}]".format(values[0], values[1], values[2])
                config[str(node_id)][labels[1]] = "[{},{},{}]".format(values[3], values[4], values[5])
                if len(labels)==3:
                    config[str(node_id)][labels[2]]  = "{}".format(values[6])
                self.write_bc_in_file(self._node_structural_path, config)
                self._single_structural_excitation_bc([node_id], labels)
            else:
                # if loaded_table:
                #     if len(labels)==3:
                #         config[str(node_id)] =  {   labels[0]: "[{},{},{}]".format(table_name[0], table_name[1], table_name[2]),
                #                                     labels[1]: "[{},{},{}]".format(table_name[3], table_name[4], table_name[5]),
                #                                     labels[2]: "{}".format(table_name[6])   }
                #     else:
                #         config[str(node_id)] =  {   labels[0]: "[{},{},{}]".format(table_name[0], table_name[1], table_name[2]),
                #                                     labels[1]: "[{},{},{}]".format(table_name[3], table_name[4], table_name[5])   }
                # else:
                if len(labels)==3:
                    config[str(node_id)] =  {   labels[0]: "[{},{},{}]".format(values[0], values[1], values[2]),
                                                labels[1]: "[{},{},{}]".format(values[3], values[4], values[5]),
                                                labels[2]: "{}".format(values[6])   }
                else:
                    config[str(node_id)] =  {   labels[0]: "[{},{},{}]".format(values[0], values[1], values[2]),
                                                labels[1]: "[{},{},{}]".format(values[3], values[4], values[5])   }

                self.write_bc_in_file(self._node_structural_path, config)


    def add_acoustic_bc_in_file(self, list_nodesID, value, loaded_table, table_name, label):
        for node_id in list_nodesID:
            config = configparser.ConfigParser()
            config.read(self._node_acoustic_path)
            if str(node_id) in config.sections():
                if loaded_table:
                    config[str(node_id)][label[0]]  = "[{}]".format(table_name)
                else:
                    config[str(node_id)][label[0]] = "[{}]".format(value)
                self.write_bc_in_file(self._node_acoustic_path, config)
                self._single_acoustic_excitation_bc([node_id], label)
                self._single_impedance_at_node([node_id], label)
            else:
                if loaded_table:
                    config[str(node_id)] =  {label[0]: "[{}]".format(table_name)}
                else:    
                    config[str(node_id)] = {label[0]: "[{}]".format(value)}
                self.write_bc_in_file(self._node_acoustic_path, config)

    def write_bc_in_file(self, path, config):
        with open(path, 'w') as config_file:
            config.write(config_file)

    def get_import_type(self):
        return self._import_type

    @property
    def element_size(self):
        return self._element_size

    @property
    def geometry_path(self):
        return self._geometry_path

    @property
    def coord_path(self):
        return self._coord_path

    @property
    def conn_path(self):
        return self._conn_path

    @property
    def material_list_path(self):
        return self._material_list_path