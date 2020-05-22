from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution import Solution
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.cross_section import CrossSection
from pulse.project_file import ProjectFile
import numpy as np
import configparser
import os

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.file = ProjectFile()

        self._projectName = ""

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
        self.file.new(projectPath, projectName, elementSize, importType, materialListPath, geometryPath, cordPath, connPath)

        if self.file.getImportType() == 0:
            self.mesh.generate(self.file.geometryPath, self.file.elementSize)
        elif self.file.getImportType() == 1:
            self.mesh.load_mesh(self.file.cordPath, self.file.connPath)

        self.file.createEntityFile(self.getEntities())

    def loadProject(self, projectFilePath):
        self.resetInfo()
        self.file.load(projectFilePath)

        if self.file.getImportType() == 0:
            self.mesh.generate(self.file.geometryPath, self.file.elementSize)
        elif self.file.getImportType() == 1:
            self.mesh.load_mesh(self.file.cordPath, self.file.connPath)

        self.loadEntityFile()
        self.loadNodeFile()
        self.loadAnalyseFile()

    def loadEntityFile(self):
        material, cross = self.file.getDictOfEntitiesFromFile()
        for key, mater in material.items():
            self.loadMaterial_by_Entity(key, mater)
        for key, crossSection in cross.items():
            self.loadCrossSection_by_Entity(key, crossSection)

    def loadNodeFile(self):
        boundary, force, mass, spring, damper = self.file.getDictOfNodesFromFile()
        for key, bc in boundary.items():
            if bc.count(None) != 6:
                self.loadStructuralBondaryCondition_by_Node(key, bc)
        for key, fr in force.items():
            if sum(fr) > 0:
                self.loadForce_by_Node(key, fr)
        for key, ms in mass.items():
            if sum(fr) > 0:
                self.loadMass_by_Node(key, ms)
        for key, sp in spring.items():
            if sum(fr) > 0:
                self.loadSpring_by_Node(key, sp)
        for key, dm in damper.items():
            if sum(fr) > 0:
                self.loadDamper_by_Node(key, dm)

    def loadAnalyseFile(self):
        self.frequencies = self.file.loadAnalyseFile()

    def setMaterial_by_Entity(self, entity_id, material):
        if self.file.getImportType() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.getImportType() == 1:
            self.mesh.set_material_by_element('all', material)

        self._setEntityMaterial(entity_id, material)
        self.file.addMaterialInFile(entity_id, material.identifier)

    def setCrossSection_by_Entity(self, entity_id, cross_section):
        if self.file.getImportType() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.getImportType() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._setEntityCross(entity_id, cross_section)
        self.file.addCrossSectionInFile(entity_id, cross_section)

    def setMaterial(self, material):
        self.mesh.set_material_by_element('all', material)
        self._setAllEntityMaterial(material)
        for entity in self.mesh.entities:
            self.file.addMaterialInFile(entity.getTag(), material.identifier)

    def setCrossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._setAllEntityCross(cross_section)
        for entity in self.mesh.entities:
            self.file.addCrossSectionInFile(entity.getTag(), cross_section)

    def setStructuralBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_structural_boundary_condition_by_node(node_id, bc)
        self.file.addBondaryConditionInFile(node_id, bc)

    def setFroce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)
        self.file.addForceInFile(node_id, force)

    def setMass_by_Node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)
        self.file.addMassInFile(node_id, mass)

    def setSpring_by_Node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)
        self.file.addSpringInFile(node_id, spring)

    def setDamper_by_Node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)
        self.file.addDamperInFile(node_id, damper)

    def loadMaterial_by_Entity(self, entity_id, material):
        if self.file.getImportType() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.getImportType() == 1:
            self.mesh.set_material_by_element('all', material)

        self._setEntityMaterial(entity_id, material)

    def loadCrossSection_by_Entity(self, entity_id, cross_section):
        if self.file.getImportType() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.getImportType() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._setEntityCross(entity_id, cross_section)

    def loadStructuralBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_structural_boundary_condition_by_node(node_id, bc)

    def loadForce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)

    def loadMass_by_Node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)

    def loadSpring_by_Node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)

    def loadDamper_by_Node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)

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
        return self.file.elementSize

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

    def setFrequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.file.addFrequencyInFile(min_, max_, step_)
        self.frequencies = frequencies

    def setModes(self, modes):
        self.modes = modes

    def getFrequencies(self):
        return self.frequencies

    def getModes(self):
        return self.modes

    def getMaterialListPath(self):
        return self.file.materialListPath

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

    def getSolve(self):
        self.solution = Solution(self.mesh)
        return self.solution

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