from pulse.preprocessing.material import Material
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
        self._geometryPath = ""
        self._connPath = ""
        self._cordPath = ""
        self._nodePath = ""
        self._entityPath = ""
        self._analysePath = ""

        self._entityFileName = "entity.dat"
        self._nodeFileName = "node.dat"
        self._projectBaseName = "project.ini"

    def _reset(self):
        self._projectName = ""
        self._importType = 0
        self._projectPath = ""
        self._materialListPath = ""
        self._geometryPath = ""
        self._connPath = ""
        self._cordPath = ""
        self._nodePath = ""

    def new(self, projectPath, projectName, elementSize, importType, materialListPath, geometryPath = "", cordPath = "", connPath = ""):
        self._projectPath = projectPath
        self._projectName = projectName
        self._elementSize = float(elementSize)
        self._importType = int(importType)
        self._materialListPath = materialListPath
        self._geometryPath = geometryPath
        self._connPath = connPath
        self._cordPath = cordPath
        self._entityPath = "{}\\{}".format(self._projectPath, self._entityFileName)
        self._nodePath = "{}\\{}".format(self._projectPath, self._nodeFileName)

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

        self._projectPath = projectFolderPath
        self._projectName = projectName
        self._elementSize = float(elementSize)
        self._importType = int(importType)
        self._materialListPath = "{}\\{}".format(self._projectPath, materialListFile)
        self._geometryPath = "{}\\{}".format(self._projectPath, geometryFile)
        self._connPath = "{}\\{}".format(self._projectPath, connFile)
        self._cordPath = "{}\\{}".format(self._projectPath, cordFile)

        self._entityPath = "{}\\{}".format(self._projectPath, self._entityFileName)
        self._nodePath = "{}\\{}".format(self._projectPath, self._nodeFileName)

    #Analyse
    def loadAnalyseFile(self):
        min_ = 0
        max_ = 0
        step_ = 0
        temp_projectBaseFilePath = "{}\\{}".format(self._projectPath, self._projectBaseName)
        config = configparser.ConfigParser()
        config.read(temp_projectBaseFilePath)
        sections = config.sections()
        if "analyse" in sections:
            keys = list(config['analyse'].keys())
            if "frequency min" in keys and "frequency max" in keys and "frequency step" in keys:
                min_ = config['analyse']['frequency min']
                max_ = config['analyse']['frequency max']
                step_ = config['analyse']['frequency step']

        return float(min_), float(max_), float(step_)

    def addFrequencyInFile(self, min_, max_, step_):
        min_ = str(min_)
        max_ = str(max_)
        step_ = str(step_)
        temp_projectBaseFilePath = "{}\\{}".format(self._projectPath, self._projectBaseName)
        config = configparser.ConfigParser()
        config.read(temp_projectBaseFilePath)
        sections = config.sections()
        if "analyse" in sections:
            keys = list(config['analyse'].keys())
            if "frequency min" in keys:
                config['analyse']['frequency min'] = min_
            else:
                config['analyse'] = {
                    'frequency min' : min_
                }
            if "frequency max" in keys:
                config['analyse']['frequency max'] = max_
            else:
                config['analyse'] = {
                    'frequency max' : max_
                }
            if "frequency step" in keys:
                config['analyse']['frequency step'] = step_
            else:
                config['analyse'] = {
                    'frequency step' : step_
                }
        else:
            config['analyse'] = {
                'frequency min' : min_,
                'frequency max' : max_,
                'frequency step': step_,
            }

        print(temp_projectBaseFilePath)
        with open(temp_projectBaseFilePath, 'w') as configfile:
            config.write(configfile)

    #Entity File

    def createEntityFile(self, entities):
        config = configparser.ConfigParser()
        for entity in entities:
            config[str(entity.getTag())] = {
                'MaterialID': '',
                'Outer Diameter': '',
                'Thickness': ''
            }
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def getDictOfEntitiesFromFile(self):
        material_list = configparser.ConfigParser()
        material_list.read(self._materialListPath)

        entityFile = configparser.ConfigParser()
        entityFile.read(self._entityPath)

        dict_material = {}
        dict_cross = {}

        for entity in entityFile.sections():
            material_id = entityFile[entity]['MaterialID']
            diam_ext = entityFile[entity]['outer diameter']
            thickness = entityFile[entity]['thickness']
            if material_id.isnumeric():
                material_id = int(material_id)
                for material in material_list.sections():
                    if int(material_list[material]['identifier']) == material_id:
                        name = str(material_list[material]['name'])
                        identifier = str(material_list[material]['identifier'])
                        density =  str(material_list[material]['density'])
                        youngmodulus =  str(material_list[material]['youngmodulus'])
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
        
        return dict_material, dict_cross

    def addCrossSectionInFile(self, entity_id, cross_section):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['outer diameter'] = str(cross_section.external_diameter)
        config[str(entity_id)]['thickness'] = str(cross_section.thickness)
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def addMaterialInFile(self, entity_id, material_id):
        config = configparser.ConfigParser()
        config.read(self._entityPath)
        config[str(entity_id)]['MaterialID'] = str(material_id)
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    #Nodes File

    def getDictOfNodesFromFile(self):
        node_list = configparser.ConfigParser()
        node_list.read(self._nodePath)

        dict_boundary = {}
        dict_forces = {}
        dict_mass = {}
        dict_spring = {}
        dict_damper = {}

        for node in node_list.sections():
            node_id = int(node)
            keys = list(node_list[node].keys())
            if "displacement" in keys and "rotation" in keys:
                #Have boundary condition
                displacement = node_list[str(node)]['displacement']
                rotation = node_list[str(node)]['rotation']
                bc = self._getBoundaryFromString(displacement, rotation)
                dict_boundary[node_id] = bc
            if "force" in keys:
                #Have forces
                force = node_list[str(node)]['force']
                fr = self._getForceFromString(force)
                dict_forces[node_id] = fr
            if "mass" in keys:
                #Have forces
                mass = node_list[str(node)]['mass']
                ms = self._getMassFromString(mass)
                dict_mass[node_id] = ms
            if "spring" in keys:
                #Have forces
                spring = node_list[str(node)]['spring']
                sp = self._getSpringFromString(spring)
                dict_spring[node_id] = sp
            if "damper" in keys:
                #Have forces
                damper = node_list[str(node)]['damper']
                dm = self._getForceFromString(damper)
                dict_damper[node_id] = dm
        
        return dict_boundary, dict_forces, dict_mass, dict_spring, dict_damper

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

    def _getBoundaryFromString(self, displacement, rotation):
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

    def addBondaryConditionInFile(self, nodesID_list, boundaryCondition):
        if boundaryCondition.count(None) == 6:
            return
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['displacement'] = "({},{},{})".format(boundaryCondition[0], boundaryCondition[1], boundaryCondition[2])
                config[str(node_id)]['rotation'] = "({},{},{})".format(boundaryCondition[3], boundaryCondition[4], boundaryCondition[5])
            else:
                config[str(node_id)] = {
                    'displacement': "({},{},{})".format(boundaryCondition[0], boundaryCondition[1], boundaryCondition[2]),
                    'rotation': "({},{},{})".format(boundaryCondition[3], boundaryCondition[4], boundaryCondition[5]),
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

    def addForceInFile(self, nodesID_list, force):
        if sum(force) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['force'] = "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
            else:
                config[str(node_id)] = {
                    'force': "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

    def addMassInFile(self, nodesID_list, mass):
        if sum(mass) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['mass'] = "({},{},{},{},{},{})".format(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5])
            else:
                config[str(node_id)] = {
                    'mass': "({},{},{},{},{},{})".format(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5]),
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

    def addSpringInFile(self, nodesID_list, spring):
        if sum(spring) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['spring'] = "({},{},{},{},{},{})".format(spring[0], spring[1], spring[2], spring[3], spring[4], spring[5])
            else:
                config[str(node_id)] = {
                    'spring': "({},{},{},{},{},{})".format(spring[0], spring[1], spring[2], spring[3], spring[4], spring[5]),
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

    def addDamperInFile(self, nodesID_list, damper):
        if sum(damper) == 0:
            return
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodesID_list:
            if str(node_id) in config.sections():
                config[str(node_id)]['damper'] = "({},{},{},{},{},{})".format(damper[0], damper[1], damper[2], damper[3], damper[4], damper[5])
            else:
                config[str(node_id)] = {
                    'damper': "({},{},{},{},{},{})".format(damper[0], damper[1], damper[2], damper[3], damper[4], damper[5]),
                }
        with open(self._nodePath, 'w') as configfile:
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