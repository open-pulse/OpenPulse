from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_structural import SolutionStructural
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.cross_section import CrossSection
from pulse.projectFile import ProjectFile
from pulse.utils import error
import numpy as np
import configparser
import os

class Project:
    def __init__(self):
        self.mesh = Mesh()
        self.file = ProjectFile()

        self._projectName = ""

        #Analysis
        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.natural_frequencies_structural = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False

    def reset_info(self):
        self.mesh = Mesh()
        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.damping = [0,0,0,0]
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.natural_frequencies_structural = []
        self.solution_structural = None
        self.solution_acoustic = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False

    def new_project(self, projectPath, projectName, elementSize, importType, materialListPath, fluidListPath, geometryPath = "", cordPath = "", connPath = ""):
        self.reset_info()
        self.file.new(projectPath, projectName, elementSize, importType, materialListPath, fluidListPath, geometryPath, cordPath, connPath)
        self._projectName = projectName

        if self.file.getImportType() == 0:
            self.mesh.generate(self.file.geometryPath, self.file.elementSize)
        elif self.file.getImportType() == 1:
            self.mesh.load_mesh(self.file.cordPath, self.file.connPath)

        self.file.createEntityFile(self.get_entities())

    def load_project(self, projectFilePath):

        self.reset_info()
        self.file.load(projectFilePath)
        self._projectName = self.file._projectName

        if self.file.getImportType() == 0:
            self.mesh.generate(self.file.geometryPath, self.file.elementSize)
        elif self.file.getImportType() == 1:
            self.mesh.load_mesh(self.file.cordPath, self.file.connPath)

        self.load_structural_bc_file()
        self.load_acoustic_bc_file()
        self.load_entity_file()

        if self.file.tempPath is None:
            self.load_analysis_file()
        else:
            self.load_frequencies_from_table()
  

    def load_entity_file(self):
        material, cross, fluid = self.file.getDictOfEntitiesFromFile()
        for key, mater in material.items():
            self.load_material_by_entity(key, mater)
        for key, crossSection in cross.items():
            self.load_crossSection_by_entity(key, crossSection)
        for key, fld in fluid.items():
            self.load_fluid_by_entity(key, fld)

    def load_structural_bc_file(self):
        prescribed_dofs, external_loads, mass, spring, damper = self.file.get_dict_of_structural_bc_from_file()
        for key, bc in prescribed_dofs.items():
            if bc.count(None) != 6:
                self.load_prescribed_dofs_bc_by_node(key, bc)
        for key, fr in external_loads.items():
            if sum(fr) > 0:
                self.load_structural_loads_by_node(key, fr)
        for key, ms in mass.items():
            if sum(ms) > 0:
                self.load_mass_by_node(key, ms)
        for key, sp in spring.items():
            if sum(sp) > 0:
                self.load_spring_by_node(key, sp)
        for key, dm in damper.items():
            if sum(dm) > 0:
                self.load_damper_by_node(key, dm)

    def load_acoustic_bc_file(self):
        pressure, volume_velocity, specific_impedance, radiation_impedance = self.file.getDictOfAcousticBCFromFile()
        for key, ActPres in pressure.items():
            if ActPres is not None:
                self.load_acoustic_pressure_bc_by_node(key, ActPres)
        for key, VelVol in volume_velocity.items():
            if VelVol != 0:
                self.load_volume_velocity_bc_by_node(key, VelVol)
        for key, SpecImp in specific_impedance.items():
            if SpecImp != 0:
                self.load_specific_impedance_bc_by_node(key, SpecImp)
        for key, RadImp in radiation_impedance.items():
            if RadImp != 0:
                self.load_radiation_impedance_bc_by_node(key, RadImp)

    def load_analysis_file(self):
        self.f_min, self.f_max, self.f_step = self.file.load_analysis_file()

    def load_frequencies_from_table(self):
        self.f_min, self.f_max, self.f_step = self.file.f_min, self.file.f_max, self.file.f_step
        self.frequencies = self.file.frequencies 

    def set_material_by_entity(self, entity_id, material):
        if self.file.getImportType() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.getImportType() == 1:
            self.mesh.set_material_by_element('all', material)

        self._set_entity_material(entity_id, material)
        self.file.addMaterialInFile(entity_id, material.identifier)

    def set_crossSection_by_entity(self, entity_id, cross_section):
        if self.file.getImportType() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.getImportType() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._set_entity_crossSection(entity_id, cross_section)
        self.file.addCrossSectionInFile(entity_id, cross_section)

    def set_material(self, material):
        self.mesh.set_material_by_element('all', material)
        self._set_all_entity_material(material)
        for entity in self.mesh.entities:
            self.file.addMaterialInFile(entity.getTag(), material.identifier)

    def set_crossSection(self, cross_section):
        self.mesh.set_cross_section_by_element('all', cross_section)
        self._set_all_entity_crossSection(cross_section)
        for entity in self.mesh.entities:
            self.file.addCrossSectionInFile(entity.getTag(), cross_section)

    def set_prescribed_dofs_bc_by_node(self, node_id, bc):
        self.mesh.set_prescribed_dofs_bc_by_node(node_id, bc)
        self.file.addBoundaryConditionInFile(node_id, bc)

    def set_force_by_node(self, node_id, force):
        self.mesh.set_load_bc_by_node(node_id, force)
        self.file.addForceInFile(node_id, force)

    def set_mass_by_node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)
        self.file.addMassInFile(node_id, mass)

    def set_spring_by_node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)
        self.file.addSpringInFile(node_id, spring)

    def set_damper_by_node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)
        self.file.addDamperInFile(node_id, damper)

    def load_material_by_entity(self, entity_id, material):
        if self.file.getImportType() == 0:
            self.mesh.set_material_by_line(entity_id, material)
        elif self.file.getImportType() == 1:
            self.mesh.set_material_by_element('all', material)

        self._set_entity_material(entity_id, material)

    def load_fluid_by_entity(self, entity_id, fluid):
        if self.file.getImportType() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.getImportType() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._set_entity_fluid(entity_id, fluid)

    def load_crossSection_by_entity(self, entity_id, cross_section):
        if self.file.getImportType() == 0:
            self.mesh.set_cross_section_by_line(entity_id, cross_section)
        elif self.file.getImportType() == 1:
            self.mesh.set_cross_section_by_element('all', cross_section)

        self._set_entity_crossSection(entity_id, cross_section)

    def load_structural_loads_by_node(self, node_id, load):
        self.mesh.set_structural_load_bc_by_node(node_id, load)

    def load_mass_by_node(self, node_id, mass):
        self.mesh.add_mass_to_node(node_id, mass)

    def load_spring_by_node(self, node_id, spring):
        self.mesh.add_spring_to_node(node_id, spring)

    def load_damper_by_node(self, node_id, damper):
        self.mesh.add_damper_to_node(node_id, damper)

    def get_nodes_bc(self):
        return self.mesh.structural_nodes_with_bc

    def get_elements(self):
        return self.mesh.structural_elements

    def set_frequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.f_min, self.f_max, self.f_step = min_, max_, step_
            self.file.addFrequencyInFile(min_, max_, step_)
        self.frequencies = frequencies

    def load_prescribed_dofs_bc_by_node(self, node_id, bc):
        self.mesh.set_prescribed_dofs_bc_by_node(node_id, bc)

    def _set_entity_material(self, entity_id, material):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.material = material
                return

    def _set_entity_crossSection(self, entity_id, cross):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.crossSection = cross
                return

    def _set_all_entity_material(self, material):
        for entity in self.mesh.entities:
            entity.material = material
            
    def _set_all_entity_crossSection(self, cross):
        for entity in self.mesh.entities:
            entity.crossSection = cross

    def get_nodes_with_prescribed_dofs_bc(self):
        return self.mesh.structural_nodes_with_bc

    def get_structural_elements(self):
        return self.mesh.structural_elements

    def set_fluid_by_entity(self, entity_id, fluid):
        if self.file.getImportType() == 0:
            self.mesh.set_fluid_by_line(entity_id, fluid)
        elif self.file.getImportType() == 1:
            self.mesh.set_fluid_by_element('all', fluid)

        self._set_entity_fluid(entity_id, fluid)
        self.file.addFluidInFile(entity_id, fluid.identifier)

    def set_fluid(self, fluid):
        self.mesh.set_fluid_by_element('all', fluid)
        self._set_all_entity_fluid(fluid)
        for entity in self.mesh.entities:
            self.file.addFluidInFile(entity.getTag(), fluid.identifier)

    def set_acoustic_pressure_bc_by_node(self, node_id, acoustic_pressure):
        self.mesh.set_acoustic_pressure_bc_by_node(node_id, acoustic_pressure)        
        if isinstance(acoustic_pressure, np.ndarray):
            self.file.addAcousticPressureBCInFile(node_id, self.file.tempPath)
        else:
            self.file.addAcousticPressureBCInFile(node_id, acoustic_pressure)
    
    def set_volume_velocity_bc_by_node(self, node_id, volume_velocity):
        self.mesh.set_volume_velocity_bc_by_node(node_id, volume_velocity)
        self.file.addVolumeVelocityBCInFile(node_id, volume_velocity)

    def set_specific_impedance_bc_by_node(self, node_id, specific_impedance):
        self.mesh.set_specific_impedance_bc_by_node(node_id, specific_impedance)
        self.file.addSpecificImpedanceBCInFile(node_id, specific_impedance)

    def set_radiation_impedance_bc_by_node(self, node_id, radiation_impedance):
        self.mesh.set_radiation_impedance_bc_by_node(node_id, radiation_impedance)
        self.file.addRadiationImpedanceBCInFile(node_id, radiation_impedance)

    def get_nodes_with_acoustic_pressure_bc(self):
        return self.mesh.nodesAcousticBC

    def get_acoustic_elements(self):
        return self.mesh.acoustic_elements

    def load_acoustic_pressure_bc_by_node(self, node_id, bc):
        self.mesh.set_acoustic_pressure_bc_by_node(node_id, bc)

    def load_volume_velocity_bc_by_node(self, node_id, force):
        self.mesh.set_volume_velocity_bc_by_node(node_id, force)

    def load_specific_impedance_bc_by_node(self, node_id, force):
        self.mesh.set_specific_impedance_bc_by_node(node_id, force)

    def load_radiation_impedance_bc_by_node(self, node_id, force):
        self.mesh.set_radiation_impedance_bc_by_node(node_id, force)

    def _set_entity_fluid(self, entity_id, fluid):
        for entity in self.mesh.entities:
            if entity.tag == entity_id:
                entity.fluid = fluid
                return

    def _set_all_entity_fluid(self, fluid):
        for entity in self.mesh.entities:
            entity.fluid = fluid

    def get_mesh(self):
        return self.mesh

    def get_nodes_color(self):
        return self.mesh.nodes_color

    def get_nodes(self):
        return self.mesh.nodes

    def get_entities(self):
        return self.mesh.entities

    def get_node(self, node_id):
        return self.mesh.nodes[node_id]

    def get_entity(self, entity_id):
        for entity in self.mesh.entities:
            if entity.getTag() == entity_id:
                return entity

    def get_element_size(self):
        return self.file.elementSize

    def check_entity_material(self):
        for entity in self.get_entities():
            if entity.getMaterial() is None:
                return False
        return True

    def check_entity_crossSection(self):
        for entity in self.get_entities():
            if entity.getCrossSection() is None:
                return False
        return True

    def set_modes(self, modes):
        self.modes = modes

    def get_frequencies(self):
        return self.frequencies

    def get_frequency_setup(self):
        return self.f_min, self.f_max, self.f_step

    def get_modes(self):
        return self.modes

    def get_material_list_path(self):
        return self.file.materialListPath
    
    def get_fluid_list_path(self):
        return self.file._fluidListPath

    def get_project_name(self):
        return self._projectName

    def set_analysis_type(self, ID, analysis_text, method_text = ""):
        self.analysis_ID = ID
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_analysis_id(self): 
        return self.analysis_ID

    def get_analysis_type_label(self):
        return self.analysis_type_label

    def get_analysis_method_label(self):
        return self.analysis_method_label

    def set_damping(self, value):
        self.damping = value

    def get_damping(self):
        return self.damping

    def get_structural_solve(self):
        if self.analysis_ID in [5,6]:
            results = SolutionStructural(self.mesh, acoustic_solution=self.solution_acoustic)
        else:
            results = SolutionStructural(self.mesh)
        return results

    def set_structural_solution(self, value):
        self.solution_structural = value

    def get_structural_solution(self):
        return self.solution_structural

    def get_acoustic_solve(self):
        return SolutionAcoustic(self.mesh, self.frequencies)

    def set_acoustic_solution(self, value):
        self.solution_acoustic = value
    
    def get_acoustic_solution(self):
        return self.solution_acoustic

    def set_acoustic_natural_frequencies(self, value):
        self.natural_frequencies_acoustic = value
    
    def set_structural_natural_frequencies(self, value):
        self.natural_frequencies_structural  = value

    def get_structural_natural_frequencies(self):
        return self.natural_frequencies_structural

    def get_unit(self):
        analysis = self.analysis_ID
        if analysis >=0 and analysis <= 6:
            if analysis in [3,5,6] and self.plot_pressure_field:
                return "Pa"
            else:
                return "m"

    # def isFloat(self, number):
    #     try:
    #         float(number)
    #         return True
    #     except Exception:
    #         return False   