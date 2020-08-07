from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.utils import error
import configparser
import os
import numpy as np
from math import pi
from pulse.utils import remove_bc_from_file

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
        self._node_structural_file_name = "structural_boundary_conditions_info.dat"
        self._node_acoustic_file_name = "acoustic_boundary_conditions_info.dat"
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
        config = configparser.ConfigParser()
        config.read(project_file_path)

        project_name = config['PROJECT']['Name']
        element_size = config['PROJECT']['Element Size']
        import_type = config['PROJECT']['Import Type']
        geometry_file = config['PROJECT']['Geometry File']
        coord_file = config['PROJECT']['Cord File']
        conn_file = config['PROJECT']['Conn File']
        material_list_file = config['PROJECT']['MaterialList File']
        fluid_list_file = config['PROJECT']['FluidList File']

        self._project_path = project_folder_path
        self._project_name = project_name
        self._element_size = float(element_size)
        self._import_type = int(import_type)
        self._material_list_path = "{}\\{}".format(self._project_path, material_list_file)
        self._fluid_list_path = "{}\\{}".format(self._project_path, fluid_list_file)
        self._geometry_path = "{}\\{}".format(self._project_path, geometry_file)
        self._conn_path = "{}\\{}".format(self._project_path, conn_file)
        self._coord_path = "{}\\{}".format(self._project_path, coord_file)

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
        if "Frequency Setup" in sections:
            keys = list(config['Frequency Setup'].keys())
            if "frequency min" in keys and "frequency max" in keys and "frequency step" in keys:
                f_min = config['Frequency Setup']['frequency min']
                f_max = config['Frequency Setup']['frequency max']
                f_step = config['Frequency Setup']['frequency step']

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
        sections = config.sections()
        if "Frequency Setup" in sections:
            keys = list(config['Frequency Setup'].keys())
            if "frequency min" in keys:
                config['Frequency Setup']['frequency min'] = min_
            else:
                config['Frequency Setup'] = {
                    'frequency min' : min_
                }
            if "frequency max" in keys:
                config['Frequency Setup']['frequency max'] = max_
            else:
                config['Frequency Setup'] = {
                    'frequency max' : max_
                }
            if "frequency step" in keys:
                config['Frequency Setup']['frequency step'] = step_
            else:
                config['Frequency Setup'] = {
                    'frequency step' : step_
                }
        else:
            config['Frequency Setup'] = {
                'frequency min' : min_,
                'frequency max' : max_,
                'frequency step': step_,
            }

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
        sections = config.sections()
        if "Global damping setup" in sections:
            keys = list(config['Global damping setup'].keys())
            
            if 'alpha_v' in keys:
                config['Global damping setup']['alpha_v'] = alpha_v
            else:
                config['Global damping setup'] = {'alpha_v' : alpha_v}

            if 'beta_v' in keys:
                config['Global damping setup']['beta_v'] = beta_v
            else:
                config['Global damping setup'] = {'beta_v' : beta_v}

            if 'alpha_h' in keys:
                config['Global damping setup']['alpha_h'] = alpha_h
            else:
                config['Global damping setup'] = {'alpha_h' : alpha_h}

            if 'beta_h' in keys:
                config['Global damping setup']['beta_h'] = beta_h
            else:
                config['Global damping setup'] = {'beta_h' : beta_h}

        else:
            config['Global damping setup'] = {  'alpha_v' : alpha_v,
                                                'beta_v' : beta_v,
                                                'alpha_h': alpha_h,
                                                'beta_h': beta_h  } 

        with open(temp_project_base_file_path, 'w') as config_file:
            config.write(config_file)

    def create_entity_file(self, entities):
        config = configparser.ConfigParser()
        for entity in entities:
            config[str(entity.get_tag())] = {
                'material id': '',
                'outer diameter': '',
                'thickness': '',
                'offset [e_y, e_z]': '',
                'element type': '',
                'fluid id': ''
            }
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
   
        dict_material = {}
        dict_cross = {}
        dict_element_type = {}
        dict_fluid = {}
        dict_length_correction = {}

        for entity in entityFile.sections():
            
            if "-" in entity:
                if 'outer diameter' in entityFile[entity].keys():
                    diam_ext = entityFile[entity]['outer diameter']
                if 'thickness' in entityFile[entity].keys():
                    thickness = entityFile[entity]['thickness']
                if 'offset [e_y, e_z]' in entityFile[entity].keys():
                    offset = entityFile[entity]['offset [e_y, e_z]']
                    offset_y, offset_z = self._get_offset_from_string(offset) 
                if 'list of elements (cross-sections)' in entityFile[entity].keys():
                    list_elements = entityFile[entity]['list of elements (cross-sections)']
                    get_list_elements = self._get_list_elements_from_string(list_elements)
    
                if diam_ext!="" and thickness!="":
                    try:
                        diam_ext = float(diam_ext)
                        thickness = float(thickness)
                        offset_y = float(offset_y)
                        offset_z = float(offset_z)
                        cross = CrossSection(diam_ext, thickness, offset_y, offset_z)
                        dict_cross[entity] = [cross, get_list_elements]
                    except Exception as er:
                        error(str(er), title = "Error while loading cross-section parameters from file")
                        return {}, {}, {}, {}
            else:
                diam_ext = ""
                thickness = ""
                if 'outer diameter' in entityFile[entity].keys():
                    diam_ext = entityFile[entity]['outer Diameter']
                if 'thickness' in entityFile[entity].keys():    
                    thickness = entityFile[entity]['thickness']
                if 'offset [e_y, e_z]' in entityFile[entity].keys(): 
                    offset = entityFile[entity]['offset [e_y, e_z]']
                    offset_y, offset_z = self._get_offset_from_string(offset) 
                        
                if diam_ext != "" and thickness != "":
                    try:
                        diam_ext = float(diam_ext)
                        thickness = float(thickness)
                        offset_y = float(offset_y)
                        offset_z = float(offset_z)
                        cross = CrossSection(diam_ext, thickness, offset_y, offset_z)
                        dict_cross[entity] = cross
                    except Exception as er:
                        error(str(er), title = "Error while loading cross-section parameters from file")
                        return {}, {}, {}, {}

                if 'element type' in entityFile[entity].keys():

                    element_type = entityFile[entity]['Element Type']

                    if element_type != "":
                        dict_element_type[int(entity)] = element_type
                        self.element_type_is_structural = True
                    else:
                        dict_element_type[int(entity)] = 'pipe_1'
                        
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
                                color =  str(material_list[material]['color'])
                                youngmodulus = float(youngmodulus)*(10**(9))
                                temp_material = Material(name, float(density), identifier=int(identifier), young_modulus=youngmodulus, poisson_ratio=float(poisson), color=color)
                                dict_material[int(entity)] = temp_material
                
                if 'fluid id' in entityFile[entity].keys():    
                    fluid_id = entityFile[entity]['fluid id']

                    if fluid_id.isnumeric():
                        fluid_id = int(fluid_id)
                        for fluid in fluid_list.sections():
                            if int(fluid_list[fluid]['identifier']) == fluid_id:
                                name = str(fluid_list[fluid]['name'])
                                identifier = str(fluid_list[fluid]['identifier'])
                                fluid_density =  str(fluid_list[fluid]['fluid density'])
                                speed_of_sound =  str(fluid_list[fluid]['speed of sound'])
                                # acoustic_impedance =  str(fluid_list[fluid]['impedance'])
                                color =  str(fluid_list[fluid]['color'])
                                temp_fluid = Fluid(name, float(fluid_density), float(speed_of_sound), color=color, identifier=int(identifier))
                                dict_fluid[int(entity)] = temp_fluid

        for section in list(element_file.sections()):
            try:
                if 'length correction type' in  element_file[section].keys():
                    length_correction_type = int(element_file[section]['length correction type'])   
                if 'list of elements' in  element_file[section].keys():
                    list_elements = element_file[section]['list of elements']
                    get_list_elements = self._get_list_elements_from_string(list_elements)
                if length_correction_type in [0,1,2] and get_list_elements != []:
                    dict_length_correction[section] = [get_list_elements, length_correction_type]
            except Exception as er:  
                error(str(er), title="ERROR WHILE LOADING ACOUSTIC ELEMENT LENGTH CORRECTION")

        return dict_material, dict_cross, dict_element_type, dict_fluid, dict_length_correction

    def add_cross_section_in_file(self, entity_id, cross_section):   
        config = configparser.ConfigParser()
        config.read(self._entity_path)

        for section in list(config.sections()):
            section_sub = str(entity_id) + '-'
            if section_sub in section:
                # print("Section removed: {}".format(section))
                config.remove_section(section)
    
        if str(entity_id) in list(config.sections()):
            config[str(entity_id)]['outer diameter'] = str(cross_section.external_diameter)
            config[str(entity_id)]['thickness'] = str(cross_section.thickness)
            config[str(entity_id)]['offset [e_y, e_z]'] = str(cross_section.offset)
        else:
            config[str(entity_id)] = { 
                                        'outer diameter': str(cross_section.external_diameter),
                                        'thickness': str(cross_section.thickness),
                                        'offset [e_y, e_z]': str(cross_section.offset)
                                     }

        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_multiple_cross_section_in_file(self, lines, map_cross_sections_to_elements):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        for line in [lines]:
            subkey = 0
            for str_key in ['outer diameter', 'thickness', 'offset [e_y, e_z]']:
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
                    config[key]['list of elements (cross-sections)'] = '{}'.format(elements)
                else:
                    config[key] = { 'outer diameter': '{}'.format(vals[0]),
                                    'thickness': '{}'.format(vals[1]),
                                    'offset [e_y, e_z]': '[{}, {}]'.format(vals[2],vals[3]),
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
    
    def add_element_type_in_file(self, entity_id, element_type):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        if str(entity_id) in list(config.sections()):
            config[str(entity_id)]['element type'] = element_type
        else:
            config[str(entity_id)] = { 
                                        'element type': element_type
                                     }
        with open(self._entity_path, 'w') as config_file:
            config.write(config_file)

    def add_material_in_file(self, entity_id, material_id):
        config = configparser.ConfigParser()
        config.read(self._entity_path)
        if str(entity_id) in list(config.sections()):
            config[str(entity_id)]['material id'] = str(material_id)
        else:
            config[str(entity_id)] = { 
                                        'material id': str(material_id)
                                     }            
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

        for node in node_structural_list.sections():
            node_id = int(node)
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
                lumped_inertia = self._get_structural_bc_from_string(masses, moments_of_inertia, labels)
                if lumped_inertia is not None:
                    self.dict_lumped_inertia[node_id] = lumped_inertia

            if "spring stiffness" in keys and "torsional spring stiffness" in keys:
                spring_stiffness = node_structural_list[str(node)]['spring stiffness']
                torsional_spring_stiffness = node_structural_list[str(node)]['torsional spring stiffness']
                labels = [["k_x","k_y","k_z"],["k_rx","k_ry","k_rz"]]
                lumped_stiffness = self._get_structural_bc_from_string(spring_stiffness, torsional_spring_stiffness, labels)
                if lumped_stiffness is not None:
                    self.dict_lumped_stiffness[node_id] = lumped_stiffness

            if "damping coefficients" in keys and "torsional damping coefficients":
                damping_coefficients = node_structural_list[str(node)]['damping coefficients']
                torsional_damping_coefficients = node_structural_list[str(node)]['torsional damping coefficients']
                labels = [["c_x","c_y","c_z"],["c_rx","c_ry","c_rz"]]
                lumped_damping = self._get_structural_bc_from_string(damping_coefficients, torsional_damping_coefficients, labels)
                if lumped_damping is not None:
                    self.dict_lumped_damping[node_id] = lumped_damping
        
        return self.dict_prescribed_dofs, self.dict_nodal_loads, self.dict_lumped_inertia, self.dict_lumped_stiffness, self.dict_lumped_damping

    def get_dict_of_acoustic_bc_from_file(self):

        node_acoustic_list = configparser.ConfigParser()
        node_acoustic_list.read(self._node_acoustic_path)

        dict_pressure = {}
        dict_volume_velocity = {}  
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

            if "volume velocity" in keys:
                str_volume_velocity = node_acoustic_list[str(node)]['volume velocity']
                volume_velocity = self._get_acoustic_bc_from_string(str_volume_velocity, "volume velocity")
                if volume_velocity is not None:
                    dict_volume_velocity[node_id] = volume_velocity

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

    def _get_list_elements_from_string(self, list_elements):
        list_elements = list_elements[1:-1].split(',')
        _list_elements = []
        for element in list_elements:
            _list_elements.append(int(element))
        return _list_elements

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

    def _get_structural_bc_from_string(self, first, last, labels):
        
        first = first[1:-1].split(',')
        last = last[1:-1].split(',')
        output = [None, None, None, None, None, None]

        if len(first)==3 and len(last)==3:
            for i in range(3):
                try:
                    if first[i] != 'None':
                        output[i] = complex(first[i])
                    if last[i] != 'None':
                        output[i+3] = complex(last[i])
                except Exception:
                    try:
                        output[i] = self.structural_tables_load(first[i], labels[0][i])
                        output[i+3] = self.structural_tables_load(last[i], labels[1][i])
                    except Exception as e:
                        error(str(e), title = "ERROR")
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
        if label[0] == 'acoustic pressure':
            key_strings = ['volume velocity']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        elif label[0] == 'volume velocity':
            key_strings = ['acoustic pressure']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)

    def _single_impedance_at_node(self, node_id, label):
        if label[0] == 'specific impedance':
            key_strings = ['radiation impedance']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)
        elif label[0] == 'radiation impedance':
            key_strings = ['specific impedance']
            remove_bc_from_file(node_id, self._node_acoustic_path, key_strings, None)

    def add_structural_bc_in_file(self, nodesID_list, values, loaded_table, table_name, labels):
        for node_id in nodesID_list:
            config = configparser.ConfigParser()
            config.read(self._node_structural_path)
            if str(node_id) in config.sections():
                if loaded_table:
                    config[str(node_id)][labels[0]]  = "[{},{},{}]".format(table_name[0], table_name[1], table_name[2])
                    config[str(node_id)][labels[1]] = "[{},{},{}]".format(table_name[3], table_name[4], table_name[5])
                else:
                    config[str(node_id)][labels[0]]  = "[{},{},{}]".format(values[0], values[1], values[2])
                    config[str(node_id)][labels[1]] = "[{},{},{}]".format(values[3], values[4], values[5])
                self.write_bc_in_file(self._node_structural_path, config)
                self._single_structural_excitation_bc([node_id], labels)
            else:
                if loaded_table:
                    config[str(node_id)] =  {
                                            labels[0]: "[{},{},{}]".format(table_name[0], table_name[1], table_name[2]),
                                            labels[1]: "[{},{},{}]".format(table_name[3], table_name[4], table_name[5])
                                            }
                else:
                    config[str(node_id)] =  {
                                            labels[0]: "[{},{},{}]".format(values[0], values[1], values[2]),
                                            labels[1]: "[{},{},{}]".format(values[3], values[4], values[5])
                                            }
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