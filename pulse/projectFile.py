from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection

import configparser
import os
import numpy as np


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

        self.tempPath = None

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
        min_ = 0
        max_ = 0
        step_ = 0
        temp_projectBaseFilePath = "{}\\{}".format(self._projectPath, self._projectBaseName)
        config = configparser.ConfigParser()
        config.read(temp_projectBaseFilePath)
        sections = config.sections()
        if "Frequency Setup" in sections:
            keys = list(config['Frequency Setup'].keys())
            if "frequency min" in keys and "frequency max" in keys and "frequency step" in keys:
                min_ = config['Frequency Setup']['frequency min']
                max_ = config['Frequency Setup']['frequency max']
                step_ = config['Frequency Setup']['frequency step']
        return float(min_), float(max_), float(step_)

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

        # print(temp_projectBaseFilePath)
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
        dict_fluid = {}

        for entity in entityFile.sections():
            material_id = entityFile[entity]['Material ID']
            diam_ext = entityFile[entity]['Outer Diameter']
            thickness = entityFile[entity]['Thickness']
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
            
            if self.isFloat(diam_ext) and self.isFloat(thickness):
                diam_ext = float(diam_ext)
                thickness = float(thickness)
                cross = CrossSection(diam_ext, thickness)
                dict_cross[int(entity)] = cross

            fluid_id = entityFile[entity]['Fluid ID']

            if fluid_id.isnumeric():
                fluid_id = int(fluid_id)
                for fluid in fluid_list.sections():
                    if int(fluid_list[fluid]['identifier']) == fluid_id:
                        name = str(fluid_list[fluid]['name'])
                        identifier = str(fluid_list[fluid]['identifier'])
                        fluid_density =  str(fluid_list[fluid]['fluid density'])
                        sound_velocity =  str(fluid_list[fluid]['sound velocity'])
                        # acoustic_impedance =  str(fluid_list[fluid]['impedance'])
                        color =  str(fluid_list[fluid]['color'])
                        temp_fluid = Fluid(name, float(fluid_density), float(sound_velocity), color=color, identifier=int(identifier))
                        dict_fluid[int(entity)] = temp_fluid
        
        return dict_material, dict_cross, dict_fluid

    def addCrossSectionInFile(self, entity_id, cross_section):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['Outer Diameter'] = str(cross_section.external_diameter)
        config[str(entity_id)]['Thickness'] = str(cross_section.thickness)
        config[str(entity_id)]['Offset [e_y, e_z]'] = str(cross_section.offset)
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

    #Nodes File

    def get_dict_of_structural_bc_from_file(self):
        node_structural_list = configparser.ConfigParser()
        node_structural_list.read(self._nodeStructuralPath)

        dict_boundary = {}
        dict_forces = {}
        dict_mass = {}
        dict_spring = {}
        dict_damper = {}

        for node in node_structural_list.sections():
            node_id = int(node)
            keys = list(node_structural_list[node].keys())
            if "displacement" in keys and "rotation" in keys:
                #Have boundary condition
                displacement = node_structural_list[str(node)]['displacement']
                rotation = node_structural_list[str(node)]['rotation']
                bc = self._get_prescribed_dofs_bc_from_string(displacement, rotation)
                dict_boundary[node_id] = bc
            if "force" in keys:
                #Have forces
                force = node_structural_list[str(node)]['force']
                fr = self._getForceFromString(force)
                dict_forces[node_id] = fr
            if "mass" in keys:
                #Have forces
                mass = node_structural_list[str(node)]['mass']
                ms = self._getMassFromString(mass)
                dict_mass[node_id] = ms
            if "spring" in keys:
                #Have forces
                spring = node_structural_list[str(node)]['spring']
                sp = self._getSpringFromString(spring)
                dict_spring[node_id] = sp
            if "damper" in keys:
                #Have forces
                damper = node_structural_list[str(node)]['damper']
                dm = self._getForceFromString(damper)
                dict_damper[node_id] = dm
        
        return dict_boundary, dict_forces, dict_mass, dict_spring, dict_damper

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
                #Have acoustic pressure
                pressure = node_acoustic_list[str(node)]['acoustic pressure']
                actPressure = self._getAcousticPressureBCFromString(pressure)
                dict_pressure[node_id] = actPressure
            if "volume velocity" in keys:
                #Have volume velocity
                volume_velocity = node_acoustic_list[str(node)]['volume velocity']
                volVelocity = self._getVolumeVelocityBCFromString(volume_velocity)
                dict_volume_velocity[node_id] = volVelocity
            if "specific impedance" in keys:
                #Have specific impedance
                specific_impedance = node_acoustic_list[str(node)]['specific impedance']
                specImpedance = self._getSpecificImpedanceBCFromString(specific_impedance)
                dict_specific_impedance[node_id] = specImpedance
            if "radiation impedance" in keys:
                #Have forces
                radiation_impedance = node_acoustic_list[str(node)]['radiation impedance']
                radImpedance = self._getRadiationImpedanceBCFromString(radiation_impedance)
                dict_radiation_impedance[node_id] = radImpedance
        
        return dict_pressure, dict_volume_velocity, dict_specific_impedance, dict_radiation_impedance

    def _getForceFromString(self, force):
        force = force[1:-1].split(',')
        Fx = Fy = Fz = Mx = My = Mz = 0.0
        if len(force) == 6:
            if force[0] != '0.0':
                Fx = float(force[0])
            if force[1] != '0.0':
                Fy = float(force[1])
            if force[2] != '0.0':
                Fz = float(force[2])
            if force[3] != '0.0':
                Mx = float(force[3])
            if force[4] != '0.0':
                My = float(force[4])
            if force[5] != '0.0':
                Mz = float(force[5])
            
        Fr = [Fx, Fy, Fz, Mx, My, Mz]
        return Fr

    def _getMassFromString(self, mass):
        mass = mass[1:-1].split(',')
        mx = my = mz = ix = iy = iz = 0.0
        if len(mass) == 6:
            if mass[0] != '0.0':
                mx = float(mass[0])
            if mass[1] != '0.0':
                my = float(mass[1])
            if mass[2] != '0.0':
                mz = float(mass[2])
            if mass[3] != '0.0':
                ix = float(mass[3])
            if mass[4] != '0.0':
                iy = float(mass[4])
            if mass[5] != '0.0':
                iz = float(mass[5])
            
        ms = [mx, my, mz, ix, iy, iz]
        return ms

    def _getSpringFromString(self, spring):
        spring = spring[1:-1].split(',')
        kx = ky = kz = krx = kry = krz = 0.0
        if len(spring) == 6:
            if spring[0] != '0.0':
                kx = float(spring[0])
            if spring[1] != '0.0':
                ky = float(spring[1])
            if spring[2] != '0.0':
                kz = float(spring[2])
            if spring[3] != '0.0':
                krx = float(spring[3])
            if spring[4] != '0.0':
                kry = float(spring[4])
            if spring[5] != '0.0':
                krz = float(spring[5])
            
        sp = [kx, ky, kz, krx, kry, krz]
        return sp

    def _getDamperFromString(self, damper):
        damper = damper[1:-1].split(',')
        cx = cy = cz = crx = cry = crz = 0.0
        if len(damper) == 6:
            if damper[0] != '0.0':
                cx = float(damper[0])
            if damper[1] != '0.0':
                cy = float(damper[1])
            if damper[2] != '0.0':
                cz = float(damper[2])
            if damper[3] != '0.0':
                crx = float(damper[3])
            if damper[4] != '0.0':
                cry = float(damper[4])
            if damper[5] != '0.0':
                crz = float(damper[5])
            
        dm = [cx, cy, cz, crx, cry, crz]
        return dm

    def _get_prescribed_dofs_bc_from_string(self, displacement, rotation):
        displacement = displacement[1:-1].split(',')
        rotation = rotation[1:-1].split(',')

        ux = uy = uz = rx = ry = rz = None
        if len(displacement) == 3:
            if displacement[0] != 'None':
                ux = float(displacement[0])
            if displacement[1] != 'None':
                uy = float(displacement[1])
            if displacement[2] != 'None':
                uz = float(displacement[2])
        if len(rotation) == 3:
            if rotation[0] != 'None':
                rx = float(rotation[0])
            if rotation[1] != 'None':
                ry = float(rotation[1])
            if rotation[2] != 'None':
                rz = float(rotation[2])

        BC = [ux,uy,uz,rx,ry,rz]
        return BC

    def _getAcousticPressureBCFromString(self, value):
        
        value = value[1:-1].split(',')
        load_file_path = value[0].split(self._projectName)
        project_path = str(self._projectPath).split(self._projectName)
        
        output = None
        if len(value) == 1:
            if load_file_path[0] == project_path[0]:
                data = np.loadtxt(value[0], delimiter=",")
                output = data[:,1] + 1j*data[:,2]
                self.frequencies = data[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0]
                self.tempPath = value

            elif value[0] != 'None':
                try:
                    output = float(value[0])
                except Exception:
                    return
        return output

    def _getSpecificImpedanceBCFromString(self, specific_impedance):
        specific_impedance = specific_impedance[1:-1].split(',')
        value = 0
        if len(specific_impedance) == 1:
            if specific_impedance[0] != '0.0':
                value = float(specific_impedance[0])
        return value

    def _getRadiationImpedanceBCFromString(self, radiation_impedance):
        radiation_impedance = radiation_impedance[1:-1].split(',')
        value = 0
        if len(radiation_impedance) == 1:
            if radiation_impedance[0] != '0.0':
                value = float(radiation_impedance[0])
        return value

    def _getVolumeVelocityBCFromString(self, volume_velocity):
        volume_velocity = volume_velocity[1:-1].split(',')
        value = 0
        if len(volume_velocity) == 1:
            if volume_velocity[0] != '0.0':
                value = float(volume_velocity[0])
        return value

    def addBoundaryConditionInFile(self, nodesID_list, dofs):
        # if dofs.count(None) == 6:
        #     return
        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['displacement'] = "({},{},{})".format(dofs[0], dofs[1], dofs[2])
                config[str(node_id)]['rotation'] = "({},{},{})".format(dofs[3], dofs[4], dofs[5])
            else:
                config[str(node_id)] = {
                    'displacement': "({},{},{})".format(dofs[0], dofs[1], dofs[2]),
                    'rotation': "({},{},{})".format(dofs[3], dofs[4], dofs[5]),
                }
        with open(self._nodeStructuralPath, 'w') as configfile:
            config.write(configfile)

    def addForceInFile(self, nodesID_list, force):
        # if sum(force) == 0:
        #     return
        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['force'] = "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
            else:
                config[str(node_id)] = {
                    'force': "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
                }
        with open(self._nodeStructuralPath, 'w') as configfile:
            config.write(configfile)

    def addMassInFile(self, nodesID_list, mass):
        if sum(mass) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['mass'] = "({},{},{},{},{},{})".format(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5])
            else:
                config[str(node_id)] = {
                    'mass': "({},{},{},{},{},{})".format(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5]),
                }
        with open(self._nodeStructuralPath, 'w') as configfile:
            config.write(configfile)

    def addSpringInFile(self, nodesID_list, spring):
        if sum(spring) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['spring'] = "({},{},{},{},{},{})".format(spring[0], spring[1], spring[2], spring[3], spring[4], spring[5])
            else:
                config[str(node_id)] = {
                    'spring': "({},{},{},{},{},{})".format(spring[0], spring[1], spring[2], spring[3], spring[4], spring[5]),
                }
        with open(self._nodeStructuralPath, 'w') as configfile:
            config.write(configfile)

    def addDamperInFile(self, nodesID_list, damper):
        if sum(damper) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodeStructuralPath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['damper'] = "({},{},{},{},{},{})".format(damper[0], damper[1], damper[2], damper[3], damper[4], damper[5])
            else:
                config[str(node_id)] = {
                    'damper': "({},{},{},{},{},{})".format(damper[0], damper[1], damper[2], damper[3], damper[4], damper[5]),
                }
        with open(self._nodeStructuralPath, 'w') as configfile:
            config.write(configfile)

    # # START OF ACOUSTIC METHODS

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