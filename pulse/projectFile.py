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
        self._projectName = ""
        self._importType = 0
        self._projectPath = ""
        self._materialListPath = ""
        self._fluidListPath = ""
        self._geometryPath = ""
        self._connPath = ""
        self._cordPath = ""
        self._nodeStructuralPath = ""
        self._nodeAcousticPath = ""
        self._entityPath = ""
        self._analysisPath = ""
        self.temp_table_name = None

        self.element_type_is_structural = False

        self._entityFileName = "entity.dat"
        self._nodeStructuralFileName = "structural_boundary_conditions_info.dat"
        self._nodeAcousticFileName = "acoustic_boundary_conditions_info.dat"
        self._projectBaseName = "project.ini"

    def _reset(self):
        self._projectName = ""
        self._importType = 0
        self._projectPath = ""
        self._materialListPath = ""
        self._fluidListPath = ""
        self._geometryPath = ""
        self._connPath = ""
        self._cordPath = ""
        self._nodeStructuralPath = ""
        self._nodeAcousticPath = ""
        self.element_type_is_structural = False

    def new(self, projectPath, projectName, elementSize, importType, materialListPath, fluidListPath, geometryPath = "", cordPath = "", connPath = ""):
        self._projectPath = projectPath
        self._projectName = projectName
        self._elementSize = float(elementSize)
        self._importType = int(importType)
        self._materialListPath = materialListPath
        self._fluidListPath = fluidListPath
        self._geometryPath = geometryPath
        self._connPath = connPath
        self._cordPath = cordPath
        self._entityPath = "{}\\{}".format(self._projectPath, self._entityFileName)
        self._nodeStructuralPath = "{}\\{}".format(self._projectPath, self._nodeStructuralFileName)
        self._nodeAcousticPath = "{}\\{}".format(self._projectPath, self._nodeAcousticFileName)

    def load(self, projectFilePath):
        self.projectFilePath = projectFilePath
        projectFilePath = projectFilePath.replace('/', '\\')
        projectFolderPath = os.path.dirname(projectFilePath)
        config = configparser.ConfigParser()
        config.read(projectFilePath)

        projectName = config['PROJECT']['Name']
        elementSize = config['PROJECT']['Element Size']
        importType = config['PROJECT']['Import Type']
        geometryFile = config['PROJECT']['Geometry File']
        cordFile = config['PROJECT']['Cord File']
        connFile = config['PROJECT']['Conn File']
        materialListFile = config['PROJECT']['MaterialList File']
        fluidListFile = config['PROJECT']['FluidList File']

        self._projectPath = projectFolderPath
        self._projectName = projectName
        self._elementSize = float(elementSize)
        self._importType = int(importType)
        self._materialListPath = "{}\\{}".format(self._projectPath, materialListFile)
        self._fluidListPath = "{}\\{}".format(self._projectPath, fluidListFile)
        self._geometryPath = "{}\\{}".format(self._projectPath, geometryFile)
        self._connPath = "{}\\{}".format(self._projectPath, connFile)
        self._cordPath = "{}\\{}".format(self._projectPath, cordFile)

        self._entityPath = "{}\\{}".format(self._projectPath, self._entityFileName)
        self._nodeStructuralPath = "{}\\{}".format(self._projectPath, self._nodeStructuralFileName)
        self._nodeAcousticPath = "{}\\{}".format(self._projectPath, self._nodeAcousticFileName)

    #Frequency Setup Analysis
    def load_analysis_file(self):
        f_min = 0
        f_max = 0
        f_step = 0
        temp_projectBaseFilePath = "{}\\{}".format(self._projectPath, self._projectBaseName)
        config = configparser.ConfigParser()
        config.read(temp_projectBaseFilePath)
        sections = config.sections()
        if "Frequency Setup" in sections:
            keys = list(config['Frequency Setup'].keys())
            if "frequency min" in keys and "frequency max" in keys and "frequency step" in keys:
                f_min = config['Frequency Setup']['frequency min']
                f_max = config['Frequency Setup']['frequency max']
                f_step = config['Frequency Setup']['frequency step']
        return float(f_min), float(f_max), float(f_step)

    def addFrequencyInFile(self, min_, max_, step_):
        min_ = str(min_)
        max_ = str(max_)
        step_ = str(step_)
        temp_projectBaseFilePath = "{}\\{}".format(self._projectPath, self._projectBaseName)
        config = configparser.ConfigParser()
        config.read(temp_projectBaseFilePath)
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

        with open(temp_projectBaseFilePath, 'w') as configfile:
            config.write(configfile)

    def createEntityFile(self, entities):
        config = configparser.ConfigParser()

        for entity in entities:
            config[str(entity.getTag())] = {
                'Material ID': '',
                'Outer Diameter': '',
                'Thickness': '',
                'Offset [e_y, e_z]': '',
                'Element Type': '',
                'Fluid ID': ''
            }
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def getDictOfEntitiesFromFile(self):
        material_list = configparser.ConfigParser()
        material_list.read(self._materialListPath)

        fluid_list = configparser.ConfigParser()
        fluid_list.read(self._fluidListPath)

        entityFile = configparser.ConfigParser()
        entityFile.read(self._entityPath)

        dict_material = {}
        dict_cross = {}
        dict_element_type = {}
        dict_fluid = {}

        for entity in entityFile.sections():

            element_type = entityFile[entity]['Element Type']

            if element_type != "":
                dict_element_type[int(entity)] = element_type
                self.element_type_is_structural = True
            else:
                dict_element_type[int(entity)] = 'pipe_1'
    
            material_id = entityFile[entity]['Material ID']

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
            
            diam_ext = entityFile[entity]['Outer Diameter']
            thickness = entityFile[entity]['Thickness']
            offset = entityFile[entity]['Offset [e_y, e_z]']
            offset_y, offset_z = self._get_offset_from_string(offset) 

            try:
                if self.isFloat(diam_ext) and self.isFloat(thickness):
                    diam_ext = float(diam_ext)
                    thickness = float(thickness)
                    offset_y = float(offset_y)
                    offset_z = float(offset_z)
                    cross = CrossSection(diam_ext, thickness, offset_y, offset_z)#, poisson_ratio=poisson, element_type=element_type)
                    dict_cross[int(entity)] = cross
            except Exception:
                print('Error - load cross-section parameters from file!')
                return

            fluid_id = entityFile[entity]['Fluid ID']

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
        
        return dict_material, dict_cross, dict_element_type, dict_fluid

    def addCrossSectionInFile(self, entity_id, cross_section):   
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['Outer Diameter'] = str(cross_section.external_diameter)
        config[str(entity_id)]['Thickness'] = str(cross_section.thickness)
        config[str(entity_id)]['Offset [e_y, e_z]'] = str(cross_section.offset)
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)
    
    def add_element_type_in_file(self, entity_id, element_type):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['Element Type'] = element_type
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def addMaterialInFile(self, entity_id, material_id):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['Material ID'] = str(material_id)
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def addFluidInFile(self, entity_id, fluid_id):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['Fluid ID'] = str(fluid_id)
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def get_dict_of_structural_bc_from_file(self):
        node_structural_list = configparser.ConfigParser()
        node_structural_list.read(self._nodeStructuralPath)

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
                prescribed_dofs = self._get_structural_bc_from_string(displacement_strings, rotation_strings)
                if prescribed_dofs == []:
                    return
                self.dict_prescribed_dofs[node_id] = prescribed_dofs
            
            if "forces" in keys and "moments" in keys:
                forces_strings = node_structural_list[str(node)]['forces'] 
                moments_strings = node_structural_list[str(node)]['moments']
                nodal_loads = self._get_structural_bc_from_string(forces_strings, moments_strings)
                if nodal_loads == []:
                    return
                self.dict_nodal_loads[node_id] = nodal_loads
            
            if "masses" in keys and "moments of inertia" in keys:
                masses = node_structural_list[str(node)]['masses']
                moments_of_inertia = node_structural_list[str(node)]['moments of inertia']
                lumped_inertia = self._get_structural_bc_from_string(masses, moments_of_inertia)
                if lumped_inertia == []:
                    return
                self.dict_lumped_inertia[node_id] = lumped_inertia

            if "spring stiffness" in keys and "torsional spring stiffness" in keys:
                spring_stiffness = node_structural_list[str(node)]['spring stiffness']
                torsional_spring_stiffness = node_structural_list[str(node)]['torsional spring stiffness']
                lumped_stiffness = self._get_structural_bc_from_string(spring_stiffness, torsional_spring_stiffness)
                if lumped_stiffness == []:
                    return
                self.dict_lumped_stiffness[node_id] = lumped_stiffness

            if "damping coefficients" in keys and "torsional damping coefficients":
                damping_coefficients = node_structural_list[str(node)]['damping coefficients']
                torsional_damping_coefficients = node_structural_list[str(node)]['torsional damping coefficients']
                lumped_damping = self._get_structural_bc_from_string(damping_coefficients, torsional_damping_coefficients)
                if lumped_damping == []:
                    return
                self.dict_lumped_damping[node_id] = lumped_damping
        
        return self.dict_prescribed_dofs, self.dict_nodal_loads, self.dict_lumped_inertia, self.dict_lumped_stiffness, self.dict_lumped_damping

    def getDictOfAcousticBCFromFile(self):

        node_acoustic_list = configparser.ConfigParser()
        node_acoustic_list.read(self._nodeAcousticPath)

        dict_pressure = {}
        dict_volume_velocity = {}  
        dict_specific_impedance = {}
        dict_radiation_impedance = {}

        for node in node_acoustic_list.sections():
            node_id = int(node)
            keys = list(node_acoustic_list[node].keys())
            
            if "acoustic pressure" in keys:
                pressure = node_acoustic_list[str(node)]['acoustic pressure']
                message = "The loaded acoustic pressure table has invalid data \nstructure, therefore, it will be ignored in analysis."
                actPressure = self._get_acoustic_bc_from_string(pressure, message)
                dict_pressure[node_id] = actPressure

            if "volume velocity" in keys:
                volume_velocity = node_acoustic_list[str(node)]['volume velocity']
                message = "The loaded volume velocity table has invalid data \nstructure, therefore, it will be ignored in analysis."
                volVelocity = self._get_acoustic_bc_from_string(volume_velocity, message)
                dict_volume_velocity[node_id] = volVelocity

            if "specific impedance" in keys:
                specific_impedance = node_acoustic_list[str(node)]['specific impedance']
                message = "The loaded specific impedance table has invalid data \nstructure, therefore, it will be ignored in analysis."
                specImpedance = self._get_acoustic_bc_from_string(specific_impedance, message)
                dict_specific_impedance[node_id] = specImpedance

            if "radiation impedance" in keys:
                radiation_impedance = node_acoustic_list[str(node)]['radiation impedance']
                radImpedance = self._getRadiationImpedanceBCFromString(radiation_impedance)
                dict_radiation_impedance[node_id] = radImpedance

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

    def _get_acoustic_bc_from_string(self, value, message):
        
        load_path_table = ""
        value = value[1:-1].split(',')
        
        output = None
        if len(value) == 1:
            if value[0] != 'None':

                try:
                    output = complex(value[0])
                except Exception:

                    try:
                        path = os.path.dirname(self.projectFilePath)
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
                        
                    except Exception:
                        error(message)
                        # error(str(e), title="ERROR WHILE LOADING ACOUSTIC BOUNDARY CONDITIONS")
                        
        return output

    def _get_structural_bc_from_string(self, first, last):
        
        first = first[1:-1].split(',')
        last = last[1:-1].split(',')
          
        bc_1 = bc_2 = bc_3 = bc_4 = bc_5 = bc_6 = None

        if len(first)==3 and len(last)==3:

            try:

                if first[0] != 'None':
                    bc_1 = complex(first[0])
                if first[1] != 'None':
                    bc_2 = complex(first[1])
                if first[2] != 'None':
                    bc_3 = complex(first[2])

                if last[0] != 'None':
                    bc_4 = complex(last[0])
                if last[1] != 'None':
                    bc_5 = complex(last[1])
                if last[2] != 'None':
                    bc_6 = complex(last[2])
                
                output = [bc_1, bc_2, bc_3, bc_4, bc_5, bc_6]

            except Exception:

                output = []

                try:  

                    for i in range(3):
                        tables_first = self.structural_tables_load(first[i])
                        output.append(tables_first)

                    for i in range(3):
                        tables_last = self.structural_tables_load(last[i])
                        output.append(tables_last)

                except Exception as e:
                    error(str(e), title="ERROR WHILE LOADING STRUCTURAL BOUNDARY CONDITIONS")
                        
        return output


    def structural_tables_load(self, table_name):

        if table_name == "None":
            return None

        load_path_table = ""
        path = os.path.dirname(self.projectFilePath)
        if "/" in path:
            load_path_table = "{}/{}".format(path, table_name)
        elif "\\" in path:
            load_path_table = "{}\\{}".format(path, table_name)
        data = np.loadtxt(load_path_table, delimiter=",")
        output = data[:,1] + 1j*data[:,2]

        f = open(load_path_table)
        header_read = f.readline()
        
        self.frequencies = data[:,0]
        self.f_min = self.frequencies[0]
        self.f_max = self.frequencies[-1]
        self.f_step = self.frequencies[1] - self.frequencies[0]

        if ('[m/s]' or '[rad/s]') in header_read:
            output = output/(2*pi*self.frequencies)
        elif ('[m/s²]' or '[rad/s²]') in header_read:
            output = output/((2*pi*self.frequencies)**2)

        return output

    def _getRadiationImpedanceBCFromString(self, radiation_impedance):
        radiation_impedance = radiation_impedance[1:-1].split(',')
        value = 0
        if len(radiation_impedance) == 1:
            if radiation_impedance[0] != '0.0':
                value = float(radiation_impedance[0])
        return value
    
    def _single_structural_excitation_bc(self, node_id, labels):
        if labels[0] == 'displacements' and labels[1] == 'rotations':
            key_strings = ['forces', 'moments']
        elif labels[0] == 'forces' and labels[1] == 'moments':
            key_strings = ['displacements', 'rotations']
        remove_bc_from_file(node_id, self._nodeStructuralPath, key_strings, None)

    def _single_acoustic_excitation_bc(self, node_id, label):
        if label[0] == 'acoustic pressure':
            # print("acoustic pressure input")
            key_strings = ['volume velocity']
            remove_bc_from_file(node_id, self._nodeAcousticPath, key_strings, None)
        elif label[0] == 'volume velocity':
            # print("volume velocity input")
            key_strings = ['acoustic pressure']
            remove_bc_from_file(node_id, self._nodeAcousticPath, key_strings, None)

    def add_structural_bc_in_file(self, nodesID_list, values, loaded_table, table_name, labels):

        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():

                if loaded_table:
                    config[str(node_id)][labels[0]]  = "[{},{},{}]".format(table_name[0], table_name[1], table_name[2])
                    config[str(node_id)][labels[1]] = "[{},{},{}]".format(table_name[3], table_name[4], table_name[5])
                else:
                    config[str(node_id)][labels[0]]  = "[{},{},{}]".format(values[0], values[1], values[2])
                    config[str(node_id)][labels[1]] = "[{},{},{}]".format(values[3], values[4], values[5])
                self.write_bc_in_file(self._nodeStructuralPath, config)
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
                self.write_bc_in_file(self._nodeStructuralPath, config)


    def write_bc_in_file(self, path, config):
        with open(path, 'w') as configfile:
            config.write(configfile)

    # # START OF ACOUSTIC METHODS

    def add_acoustic_bc_in_file(self, list_nodesID, value, loaded_table, table_name, label):
        config = configparser.ConfigParser()
        config.read(self._nodeAcousticPath)
        for node_id in list_nodesID:
            if str(node_id) in config.sections():

                if loaded_table:
                    config[str(node_id)][label[0]]  = "[{}]".format(table_name)
                else:
                    config[str(node_id)][label[0]] = "[{}]".format(value)
                
                self.write_bc_in_file(self._nodeAcousticPath, config)
                self._single_acoustic_excitation_bc([node_id], label)

            else:

                if loaded_table:
                    config[str(node_id)] =  {label[0]: "[{}]".format(table_name)}
                else:    
                    config[str(node_id)] = {label[0]: "[{}]".format(value)}

                self.write_bc_in_file(self._nodeAcousticPath, config)

    def addAcousticPressureBCInFile(self, nodes_id, pressure):
        config = configparser.ConfigParser()
        config.read(self._nodeAcousticPath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['acoustic pressure'] = "[{}]".format(pressure)
            else:
                config[str(node_id)] = {
                    'acoustic pressure': "[{}]".format(pressure)
                }
        with open(self._nodeAcousticPath, 'w') as configfile:
            config.write(configfile)

    def addSpecificImpedanceBCInFile(self, nodes_id, specific_impedance):
        config = configparser.ConfigParser()
        config.read(self._nodeAcousticPath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['specific impedance'] = "[{}]".format(specific_impedance)
            else:
                config[str(node_id)] = {
                    'specific impedance': "[{}]".format(specific_impedance)
                }
        with open(self._nodeAcousticPath, 'w') as configfile:
            config.write(configfile)

    def addVolumeVelocityBCInFile(self, nodes_id, volume_velocity):
        config = configparser.ConfigParser()
        config.read(self._nodeAcousticPath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['volume velocity'] = "[{}]".format(volume_velocity)
            else:
                config[str(node_id)] = {
                    'volume velocity': "[{}]".format(volume_velocity)
                }
        with open(self._nodeAcousticPath, 'w') as configfile:
            config.write(configfile)
    
    def addRadiationImpedanceBCInFile(self, nodes_id, radiation_impedance):
        config = configparser.ConfigParser()
        config.read(self._nodeAcousticPath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['radiation impedance'] = "[{}]".format(radiation_impedance)
            else:
                config[str(node_id)] = {
                    'radiation impedance': "[{}]".format(radiation_impedance)
                }
        with open(self._nodeAcousticPath, 'w') as configfile:
            config.write(configfile)






    def getImportType(self):
        return self._importType

    @property
    def elementSize(self):
        return self._elementSize

    @property
    def geometryPath(self):
        return self._geometryPath

    @property
    def cordPath(self):
        return self._cordPath

    @property
    def connPath(self):
        return self._connPath

    @property
    def materialListPath(self):
        return self._materialListPath

    def isFloat(self, number):
        try:
            float(number)
            return True
        except Exception:
            return False