from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_structural import SolutionStructural
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.projectFile import ProjectFile
import numpy as np
import configparser
import os

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.file = ProjectFile()

        self._projectName = ""

        #Analysis
        self.analysisID = None
        self.analysisType = ""
        self.analysisMethod = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = []
        self.minFrequency = 0
        self.maxFrequency = 0
        self.stepFrequency = 0
        self.naturalFrequencies = []
        self.solution_structural = None
        self.solution_acoustic = None
        # self.notrun = True
        self.flag_setMaterial = False
        self.flag_setCrossSection = False

    def resetInfo(self):
        self.mesh = Mesh()
        self.analysisID = None
        self.analysisType = ""
        self.analysisMethod = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = []
        self.minFrequency = 0
        self.maxFrequency = 0
        self.stepFrequency = 0
        self.naturalFrequencies = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_setMaterial = False
        self.flag_setCrossSection = False
        # self.notrun = True

    def newProject(self, projectPath, projectName, elementSize, importType, materialListPath, fluidListPath, geometryPath = "", cordPath = "", connPath = ""):
        self.resetInfo()
        self.file.new(projectPath, projectName, elementSize, importType, materialListPath, fluidListPath, geometryPath, cordPath, connPath)

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
        self.loadStructuralBCFile()
        self.loadAcousticBCFile()
        self.loadAnalysisFile()

    def loadEntityFile(self):
        material, cross, fluid = self.file.getDictOfEntitiesFromFile()
        for key, mater in material.items():
            self.loadMaterial_by_Entity(key, mater)
        for key, crossSection in cross.items():
            self.loadCrossSection_by_Entity(key, crossSection)
        for key, fld in fluid.items():
            self.loadFluid_by_Entity(key, fld)

    def loadStructuralBCFile(self):
        boundary, force, mass, spring, damper = self.file.getDictOfStructuralBCFromFile()
        for key, bc in boundary.items():
            if bc.count(None) != 6:
                self.loadStructuralBondaryCondition_by_Node(key, bc)
        for key, fr in force.items():
            if sum(fr) > 0:
                self.loadForce_by_Node(key, fr)
        for key, ms in mass.items():
            if sum(ms) > 0:
                self.loadMass_by_Node(key, ms)
        for key, sp in spring.items():
            if sum(sp) > 0:
                self.loadSpring_by_Node(key, sp)
        for key, dm in damper.items():
            if sum(dm) > 0:
                self.loadDamper_by_Node(key, dm)

    def loadAcousticBCFile(self):
        pressure, volume_velocity, specific_impedance, radiation_impedance = self.file.getDictOfAcousticBCFromFile()
        for key, ActPres in pressure.items():
            if ActPres != None:
                self.loadAcousticPressureBC_by_Node(key, ActPres)
        for key, VelVol in volume_velocity.items():
            if VelVol != 0:
                self.loadVolumeVelocityBC_by_Node(key, VelVol)
        for key, SpecImp in specific_impedance.items():
            if SpecImp != 0:
                self.loadSpecificImpedanceBC_by_Node(key, SpecImp)
        for key, RadImp in radiation_impedance.items():
            if RadImp != 0:
                self.loadRadiationImpedanceBC_by_Node(key, RadImp)

    def loadAnalysisFile(self):
        self.minFrequency, self.maxFrequency, self.stepFrequency = self.file.loadAnalysisFile()

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

    def setStructuralBoundaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_prescribed_DOFs_BC_by_node(node_id, bc)
        self.file.addBoundaryConditionInFile(node_id, bc)

    def setForce_by_Node(self, node_id, force):
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

    def loadFluid_by_Entity(self, entity_id, fluid):
        if self.file.getImportType() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.getImportType() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._setEntityFluid(entity_id, fluid)

    def loadCrossSection_by_Entity(self, entity_id, cross_section):
        if self.file.getImportType() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.getImportType() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._setEntityCross(entity_id, cross_section)

    def loadForce_by_Node(self, node_id, force):
        self.mesh.set_force_by_node(node_id, force)

    def loadMass_by_Node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)

    def loadSpring_by_Node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)

    def loadDamper_by_Node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)

    def getNodesBC(self):
        return self.mesh.StructuralBCnodes

    def getElements(self):
        return self.mesh.structural_elements

    def setFrequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.minFrequency, self.maxFrequency, self.stepFrequency = min_, max_, step_
            self.file.addFrequencyInFile(min_, max_, step_)
        self.frequencies = frequencies

    def getMinMaxStepFrequency(self):
        return self.minFrequency, self.maxFrequency, self.stepFrequency

    def loadStructuralBondaryCondition_by_Node(self, node_id, bc):
        self.mesh.set_prescribed_DOFs_BC_by_node(node_id, bc)

    def _setEntityMaterial(self, entity_id, material):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.material = material
                return

    def _setEntityCross(self, entity_id, cross):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.crossSection = cross
                return

    def _setAllEntityMaterial(self, material):
        for entity in self.mesh.entities:
            entity.material = material
            
    def _setAllEntityCross(self, cross):
        for entity in self.mesh.entities:
            entity.crossSection = cross

    def getStructuralBCNodes(self):
        return self.mesh.StructuralBCnodes

    def getStructuralElements(self):
        return self.mesh.structural_elements

    def setFluid_by_Entity(self, entity_id, fluid):
        if self.file.getImportType() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.getImportType() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._setEntityFluid(entity_id, fluid)
        self.file.addFluidInFile(entity_id, fluid.identifier)

    def setFluid(self, fluid):
        self.mesh.set_fluid_by_element('all', fluid)
        self._setAllEntityFluid(fluid)
        for entity in self.mesh.entities:
            self.file.addFluidInFile(entity.getTag(), fluid.identifier)

    def setAcousticPressureBC_by_Node(self, node_id, acoustic_pressure):
        self.mesh.set_acoustic_pressure_BC_by_node(node_id, acoustic_pressure)
        self.file.addAcousticPressureBCInFile(node_id, acoustic_pressure)
    
    def setVolumeVelocityBC_by_Node(self, node_id, volume_velocity):
        self.mesh.set_volume_velocity_BC_by_node(node_id, volume_velocity)
        self.file.addVolumeVelocityBCInFile(node_id, volume_velocity)

    def setSpecificImpedanceBC_by_Node(self, node_id, specific_impedance):
        self.mesh.set_specific_impedance_BC_by_node(node_id, specific_impedance)
        self.file.addSpecificImpedanceBCInFile(node_id, specific_impedance)

    def setRadiationImpedanceBC_by_Node(self, node_id, radiation_impedance):
        self.mesh.set_radiation_impedance_BC_by_node(node_id, radiation_impedance)
        self.file.addRadiationImpedanceBCInFile(node_id, radiation_impedance)

    def getAcousticBCNodes(self):
        return self.mesh.nodesAcousticBC

    def getAcousticElements(self):
        return self.mesh.acoustic_elements

    def loadAcousticPressureBC_by_Node(self, node_id, bc):
        self.mesh.set_acoustic_pressure_BC_by_node(node_id, bc)

    def loadVolumeVelocityBC_by_Node(self, node_id, force):
        self.mesh.set_volume_velocity_BC_by_node(node_id, force)

    def loadSpecificImpedanceBC_by_Node(self, node_id, force):
        self.mesh.set_specific_impedance_BC_by_node(node_id, force)

    def loadRadiationImpedanceBC_by_Node(self, node_id, force):
        self.mesh.set_radiation_impedance_BC_by_node(node_id, force)

    def _setEntityFluid(self, entity_id, fluid):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.fluid = fluid
                return

    def _setAllEntityFluid(self, fluid):
        for entity in self.mesh.entities:
            entity.fluid = fluid

## END OF ACOUSTIC METHODS

    def getMesh(self):
        return self.mesh

    def getNodesColor(self):
        return self.mesh.nodes_color

    def getNodes(self):
        return self.mesh.nodes

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

    def setModes(self, modes):
        self.modes = modes

    def getFrequencies(self):
        return self.frequencies

    def getMinMaxStepFrequency(self):
        return self.minFrequency, self.maxFrequency, self.stepFrequency

    def getModes(self):
        return self.modes

    def getMaterialListPath(self):
        return self.file.materialListPath
    
    def getFluidListPath(self):
        return self.file._fluidListPath

    def getProjectName(self):
        return self._projectName

    def setAnalysisType(self, value, _type, _method = ""):
        self.analysisID = value
        self.analysisType = _type
        self.analysisMethod = _method

    def getAnalysisTypeID(self): 
        return self.analysisID

    def getAnalysisType(self):
        return self.analysisType

    def getAnalysisMethod(self):
        return self.analysisMethod

    def setDamping(self, value):
        self.damping = value

    def getDamping(self):
        return self.damping

    def getStructuralSolve(self):
        if self.getAnalysisType == "Harmonic Analysis - Coupled":
            results = SolutionStructural(self.mesh, acoustic_solution=self.getAcousticSolve())
        else:
            results = SolutionStructural(self.mesh)
        return results

    def setStructuralSolution(self, value):
        self.solution_structural = value

    def getStructuralSolution(self):
        return self.solution_structural

    def getAcousticSolve(self):
        return SolutionAcoustic(self.mesh, self.frequencies)

    def setAcousticSolution(self, value):
        self.solution_acoustic = value
    
    def getAcousticSolution(self):
        return self.solution_acoustic

    def setNaturalFrequencies(self, value):
        self.naturalFrequencies = value

    def getNaturalFrequencies(self):
        return self.naturalFrequencies

    def getUnit(self):
        analysis = self.getAnalysisTypeID()
        if analysis == 0 or analysis == 1:
            if self.getAnalysisType()  == "Harmonic Analysis - Acoustic":
                return "Pa"
            else:
                return "m"
        else:
            return "m"

    def isFloat(self, number):
        try:
            float(number)
            return True
        except Exception:
            return False   