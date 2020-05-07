from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.cross_section import CrossSection
import numpy as np
import configparser
import os

class Project:
    def __init__(self):
        self.mesh = Mesh()

        self._projectName = ""
        self._importType = 0
        self._elementSize = 0

        self._projectPath = ""
        self._materialListPath = ""
        self._geometryPath = ""
        self._connPath = ""
        self._cordPath = ""
        self._nodePath = ""
        self._entityPath = ""

        #Analysis
        self.analysisTypeID = None
        self.analysisType = ""
        self.analysisMethod = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = []
        self.naturalFrequencies = []
        self.solution = None

    def resetInfo(self):
        self.mesh = Mesh()
        self.analysisTypeID = None
        self.analysisType = ""
        self.analysisMethod = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = []
        self.naturalFrequencies = []
        self.solution = None

    def newProject(self, projectPath, projectName, elementSize, importType, materialListPath, geometryPath = "", cordPath = "", connPath = ""):
        self.resetInfo()
        self._projectPath = projectPath
        self._projectName = projectName
        self._elementSize = float(elementSize)
        self._importType = int(importType)
        self._materialListPath = materialListPath
        self._geometryPath = geometryPath
        self._connPath = connPath
        self._cordPath = cordPath

        self._entityPath = "{}\\{}".format(self._projectPath, "entity.dat")
        self._nodePath = "{}\\{}".format(self._projectPath, "node.dat")

        if self._importType == 0:
            self.mesh.generate(self._geometryPath, self._elementSize)
        elif self._importType == 1:
            self.mesh.load_mesh(self._cordPath, self._connPath)

        self.createEntityFile()

    def loadProject(self, projectFilePath):
        self.resetInfo()
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

        self._entityPath = "{}\\{}".format(self._projectPath, "entity.dat")
        self._nodePath = "{}\\{}".format(self._projectPath, "node.dat")

        if self._importType == 0:
            self.mesh.generate(self._geometryPath, self._elementSize)
        elif self._importType == 1:
            self.mesh.load_mesh(self._cordPath, self._connPath)

        self.loadEntityFile()
        self.loadNodeFile()

    def createEntityFile(self):
        config = configparser.ConfigParser()
        for entity in self.getEntities():
            config[str(entity.getTag())] = {
                'MaterialID': '',
                'Outer Diameter': '',
                'Thickness': ''
            }
        with open(self._entityPath, 'w') as configfile:
            config.write(configfile)

    def loadEntityFile(self):
        material_list = configparser.ConfigParser()
        material_list.read(self._materialListPath)

        entityFile = configparser.ConfigParser()
        entityFile.read(self._entityPath)

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
                        self.loadMaterial_by_Entity(int(entity), temp_material)
            
            if self.isFloat(diam_ext) and self.isFloat(thickness):
                diam_ext = float(diam_ext)
                thickness = float(thickness)
                cross = CrossSection(diam_ext, thickness)
                self.loadCrossSection_by_Entity(int(entity), cross)

    def loadNodeFile(self):
        node_list = configparser.ConfigParser()
        node_list.read(self._nodePath)
        for node in node_list.sections():
            node_id = int(node)
            displacement = node_list[str(node)]['displacement']
            rotation = node_list[str(node)]['rotation']
            force = node_list[str(node)]['force']
            displacement = displacement[1:-1].split(',')
            rotation = rotation[1:-1].split(',')
            force = force[1:-1].split(',')

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

            if not ux == uy == uz == rx == ry == rz == None:
                self.loadStructuralBondaryCondition_by_Node(node_id, BC)

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
            
            if sum(Fr)>0:
                self.loadForce_by_Node(node_id, Fr)

    def addBondaryConditionInFile(self, nodes_id, bc):
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['displacement'] = "({},{},{})".format(bc[0], bc[1], bc[2])
                config[str(node_id)]['rotation'] = "({},{},{})".format(bc[3], bc[4], bc[5])
            else:
                config[str(node_id)] = {
                    'displacement': "({},{},{})".format(bc[0], bc[1], bc[2]),
                    'rotation': "({},{},{})".format(bc[3], bc[4], bc[5]),
                    'force': ""
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

    def addForceInFile(self, nodes_id, force):
        config = configparser.ConfigParser()
        config.read(self._nodePath)
        for node_id in nodes_id:
            if str(node_id) in config.sections():
                config[str(node_id)]['force'] = "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
            else:
                config[str(node_id)] = {
                    'displacement': "",
                    'rotation': "",
                    'force': "({}, {}, {}, {}, {}, {})".format(force[0], force[1], force[2], force[3], force[4], force[5])
                }
        with open(self._nodePath, 'w') as configfile:
            config.write(configfile)

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

    def setMaterial_by_Entity(self, entity_id, material):
        if self._importType == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self._importType == 1:
            self.mesh.set_material_by_element('all', material)

        self._setEntityMaterial(entity_id, material)
        self.addMaterialInFile(entity_id, material.identifier)

    def setCrossSection_by_Entity(self, entity_id, cross_section):
        if self._importType == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self._importType == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._setEntityCross(entity_id, cross_section)
        self.addCrossSectionInFile(entity_id, cross_section)

    def setMaterial(self, material):
        self.mesh.set_material_by_element('all', material)
        self._setAllEntityMaterial(material)
        for entity in self.mesh.entities:
            self.addMaterialInFile(entity.getTag(), material.identifier)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._setAllEntityCross(cross_section)
        for entity in self.mesh.entities:
            self.addCrossSectionInFile(entity.getTag(), cross_section)

    def setStructuralBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_structural_boundary_condition_by_node(node_id, bc)
        self.addBondaryConditionInFile(node_id, bc)

    def setFroce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)
        self.addForceInFile(node_id, force)

    def loadMaterial_by_Entity(self, entity_id, material):
        if self._importType == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self._importType == 1:
            self.mesh.set_material_by_element('all', material)

        self._setEntityMaterial(entity_id, material)

    def loadCrossSection_by_Entity(self, entity_id, cross_section):
        if self._importType == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self._importType == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._setEntityCross(entity_id, cross_section)

    def loadStructuralBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_structural_boundary_condition_by_node(node_id, bc)

    def loadForce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)

    def _setEntityMaterial(self, entity_id, material):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.material = material
                return

    def _setEntityCross(self, entity_id, cross):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.cross = cross
                return

    def _setAllEntityMaterial(self, material):
        for entity in self.mesh.entities:
            entity.material = material

    def _setAllEntityCross(self, cross):
        for entity in self.mesh.entities:
            entity.cross = cross

    def getMesh(self):
        return self.mesh

    def getNodesBC(self):
        return self.mesh.nodesBC

    def getNodes(self):
        return self.mesh.nodes

    def getNodesColor(self):
        return self.mesh.nodes_color

    def getElements(self):
        return self.mesh.elements

    def getEntities(self):
        return self.mesh.entities

    def getNode(self, node_id):
        return self.mesh.nodes[node_id]

    def getEntity(self, entity_id):
        for entity in self.mesh.entities:
            if entity.getTag() == entity_id:
                return entity

    def getElementSize(self):
        return self._elementSize

    def checkEntityMaterial(self):
        for entity in self.getEntities():
            if entity.getMaterial() is None:
                return False
        return True

    def checkEntityCross(self):
        for entity in self.getEntities():
            if entity.getCrossSection() is None:
                return False
        return True

    def setFrequencies(self, frequencies):
        self.frequencies = frequencies

    def setModes(self, modes):
        self.modes = modes

    def getFrequencies(self):
        return self.frequencies

    def getModes(self):
        return self.modes

    def getMaterialListPath(self):
        return self._materialListPath

    def getProjectName(self):
        return self._projectName

    def setAnalysisType(self, value, _type, _method = ""):
        self.analysisTypeID = value
        self.analysisType = _type
        self.analysisMethod = _method

    def getAnalysisTypeID(self):
        return self.analysisTypeID

    def getAnalysisType(self):
        return self.analysisType

    def getAnalysisMethod(self):
        return self.analysisMethod

    def setDamping(self, value):
        self.damping = value

    def getDamping(self):
        return self.damping

    def setSolution(self, value):
        self.solution = value
    
    def getSolution(self):
        return self.solution

    def setNaturalFrequencies(self, value):
        self.naturalFrequencies = value

    def getNaturalFrequencies(self):
        return self.naturalFrequencies

    def getUnit(self):
        analyse = self.getAnalysisTypeID()
        if analyse == 0 or analyse == 1:
            return "m"
        else:
            return "m"

    def isFloat(self, number):
        try:
            float(number)
            return True
        except Exception:
            return False