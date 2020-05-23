from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_structural import SolutionStructural
from pulse.processing.solution_acoustic import SolutionAcoustic
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
        self.solution_structural = None
        self.solution_acoustic = None

    def resetInfo(self):
        self.mesh = Mesh()
        self.analysisTypeID = None
        self.analysisType = ""
        self.analysisMethod = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = []
        self.naturalFrequencies = []
        self.solution_structural = None
        self.solution_acoustic = None

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

    #TODO: add acoustics physical quantities 
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

    #TODO: add acoustics physical quantities 
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

    #TODO: add acoustics physical quantities 
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

    #TODO: add acoustics physical quantities 
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

    #TODO: duplicate this function to acoustics boundary conditions
    #TODO: rename: addStructuralBoundaryConditionInFile
    def addStructuralBoundaryConditionInFile(self, nodes_id, bc):
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

    #TODO: duplicate this function to volume_velocity entries
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

    # def addFluidInFile(self, entity_id, fluid_id):
    #     config = configparser.ConfigParser()
    #     config.read(self._entityPath)
    #     config[str(entity_id)]['FluidID'] = str(fluid_id)
    #     with open(self._entityPath, 'w') as configfile:
    #         config.write(configfile)

    # def setFluid_by_Entity(self, entity_id, fluid):
    #     if self._importType == 0:
    #         self.mesh.set_fluid_by_line(entity_id, fluid)
    #     elif self._importType == 1:
    #         self.mesh.set_fluid_by_element('all', fluid)

    #     self._setEntityFluid(entity_id, fluid)
    #     self.addFluidInFile(entity_id, fluid.identifier)

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

    # def setFluid(self, fluid):
    #     self.mesh.set_fluid_by_element('all', fluid)
    #     self._setAllEntityFluid(fluid)
    #     for entity in self.mesh.entities:
    #         self.addFluidInFile(entity.getTag(), fluid.identifier)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._setAllEntityCross(cross_section)
        for entity in self.mesh.entities:
            self.addCrossSectionInFile(entity.getTag(), cross_section)

    def setStructuralBoundaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_structural_boundary_condition_by_node(node_id, bc)
        # self.addBoundaryConditionInFile(node_id, bc)
        self.addStructuralBoundaryConditionInFile(node_id, bc)

    # def setAcousticBoundaryCondition_by_Node(self, node_id, bc):
    #     self.mesh.set_acoustic_boundary_condition_by_node(node_id, bc)
    #     self.addAcousticBoundaryConditionInFile(node_id, bc)

    def setForce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)
        self.addForceInFile(node_id, force)

    def setMass_by_Node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)

    def setSpring_by_Node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)

    def setDamper_by_Node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)
    #
    # def setVolumeVelocity_by_Node(self, node_id, volume_velocity):
    #     self.mesh.set_volume_velocity_by_node(node_id, volume_velocity)
    #     self.addVolumeVelocityInFile(node_id, volume_velocity)

    # def setImpedanceSpecific_by_Node(self, node_id, impedance_specific):
    #     self.mesh.add_impedance_specific_to_node(node_id, impedance_specific)

    # def setImpedanceAcoustic_by_Node(self, node_id, impedance_acoustic):
    #     self.mesh.add_impedance_acoustic_to_node(node_id, impedance_acoustic)

    # def setImpedanceRadiation_by_Node(self, node_id, impedance_radiation):
    #     self.mesh.add_impedance_radiation_to_node(node_id, impedance_radiation)

    def loadMaterial_by_Entity(self, entity_id, material):
        if self._importType == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self._importType == 1:
            self.mesh.set_material_by_element('all', material)

        self._setEntityMaterial(entity_id, material)

    # def loadFluid_by_Entity(self, entity_id, fluid):
    #     if self._importType == 0:
    #         self.mesh.set_fluid_by_line(entity_id, fluid)
    #     elif self._importType == 1:
    #         self.mesh.set_fluid_by_element('all', fluid)

    #     self._setEntityFluid(entity_id, fluid)

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

    # def loadAcousticBondaryCondition_by_Node(self, node_id, bc):
    #     self.mesh.set_acoustic_boundary_condition_by_node(node_id, bc)

    # def loadVolumeVelocity_by_Node(self, node_id, force):
    #     self.mesh.set_volume_velocity_by_node(node_id, force)

    # def _setEntityFluid(self, entity_id, fluid):
    #     for entity in self.mesh.entities:
    #         if entity.tag == entity_id:
    #             entity.fluid = fluid
    #             return

    # def _setAllEntityFluid(self, fluid):
    #     for entity in self.mesh.entities:
    #         entity.fluid = fluid

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

    def getStructuralBCNodes(self):
        return self.mesh.StructuralBCnodes

    def getAcousticBCNodes(self):
        return self.mesh.nodesAcousticBC

    def getNodes(self):
        return self.mesh.nodes

    def getNodesColor(self):
        return self.mesh.nodes_color

    def getStructuralElements(self):
        return self.mesh.structural_elements

    def getAcousticElements(self):
        return self.mesh.acoustic_elements

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

    def setStructuralSolution(self, value):
        self.solution_structural = value
    
    def getStructuralSolution(self):
        return self.solution_structural

    def getStructuralSolve(self):
        self.solution_structural = SolutionStructural(self.mesh)
        return self.solution_structural

    # def getSolveAcoustic(self):
    #     self.solution_acoustic = SolutionAcoustic(self.mesh, self.frequencies)
    #     return self.solution_acoustic

    # def setSolutionAcoustic(self, value):
    #     self.solution_acoustic = value
    
    # def getSolutionAcoustic(self):
    #     return self.solution_acoustic

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