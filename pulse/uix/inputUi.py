#
from pulse.uix.user_input.newProjectInput import NewProjectInput
from pulse.uix.user_input.loadProjectInput import LoadProjectInput
#
from pulse.uix.user_input.elementTypeInput import ElementTypeInput
from pulse.uix.user_input.couplingDOFsInput import CouplingDOFsInput
from pulse.uix.user_input.materialInput import MaterialInput
from pulse.uix.user_input.fluidInput import FluidInput
from pulse.uix.user_input.crossSectionInput import CrossSectionInput
from pulse.uix.user_input.dofInput import DOFInput
from pulse.uix.user_input.loadsInput import LoadsInput
from pulse.uix.user_input.massSpringDamperInput import MassSpringDamperInput
#
from pulse.uix.user_input.analysisTypeInput import AnalysisTypeInput
from pulse.uix.user_input.analysisSetupInput import AnalysisSetupInput
from pulse.uix.user_input.analysisOutputResultsInput import AnalysisOutputResultsInput
from pulse.uix.user_input.runAnalysisInput import RunAnalysisInput
#
from pulse.uix.user_input.acousticpressureInput import AcousticPressureInput
from pulse.uix.user_input.volumevelocityInput import VolumeVelocityInput
from pulse.uix.user_input.specificimpedanceInput import SpecificImpedanceInput
from pulse.uix.user_input.radiationImpedanceInput import RadiationImpedanceInput
from pulse.uix.user_input.elementLengthCorrectionInput import AcousticElementLengthCorrectionInput
#
from pulse.uix.user_input.plotCrossSectionInput import PlotCrossSectionInput
from pulse.uix.user_input.structuralModel_InfoInput import StructuralModelInfoInput
from pulse.uix.user_input.acousticModel_InfoInput import AcousticModelInfoInput
#
from pulse.uix.user_input.plotStructuralModeShapeInput import PlotStructuralModeShapeInput
from pulse.uix.user_input.plotDisplacementFieldInput import PlotDisplacementFieldInput
from pulse.uix.user_input.plotStructuralFrequencyResponseInput import PlotStructuralFrequencyResponseInput
from pulse.uix.user_input.plotReactionsInput import PlotReactionsInput
from pulse.uix.user_input.plotStressFieldInput import PlotStressFieldInput
from pulse.uix.user_input.plotStressFrequencyResponseInput import PlotStressFrequencyResponseInput
#
from pulse.uix.user_input.plotAcousticModeShapeInput import PlotAcousticModeShapeInput
from pulse.uix.user_input.plotAcousticPressureFieldInput import PlotAcousticPressureFieldInput
from pulse.uix.user_input.plotAcousticFrequencyResponseInput import PlotAcousticFrequencyResponseInput
from pulse.uix.user_input.plot_TL_NR_Input import Plot_TL_NR_Input
#
from pulse.uix.user_input.LogTimes import LogTimes
#
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.entity import Entity
from pulse.project import Project
from pulse.utils import error
#
from time import time


class InputUi:
    def __init__(self, project, parent=None):
        self.project = project
        self.parent = parent
        self.opv = self.parent.getOPVWidget()
        self.analysis_ID = None

        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.frequencies = None
        self.global_damping = [0,0,0,0]

        self.acoustic_pressure_frequencies = None
        self.volume_velocity_frequencies = None 
        self.specific_impedance_frequencies = None
        self.nodal_loads_frequencies = None
        self.prescribed_dofs_frequencies = None
        self.setup_analysis_complete = False
        self.flag_imported_table = False

    def beforeInput(self):
        try:
            self.opv.inputObject.close()
            self.opv.setInputObject(None)
        except:
            return

    def new_project(self):
        new_project_input = NewProjectInput(self.project)
        self.project.project_folder_path = new_project_input.project_folder_path
        return new_project_input.create

    def loadProject(self):
        load_project = LoadProjectInput(self.project)
        self.project.project_folder_path = load_project.project_folder_path
        return load_project.complete

    def setElementType(self):
        entities_id = self.opv.getListPickedEntities()
        read = ElementTypeInput(self.project, entities_id)
        # if read.element_type is None:
        #     return
        if read.flagEntity:
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.set_element_type_by_entity(entity, read.element_type)
            print("[Set Element Type] - defined in the entities {}".format(entities_id))
        else:
            self.project.set_element_type_to_all(read.element_type)
            print("[Set Element Type] - defined in all the entities")
        
        if read.update_cross_section:
            self.set_cross_section(pipe_to_beam=read.pipe_to_beam, beam_to_pipe=read.beam_to_pipe)


    def setRotationDecoupling(self):
        read = CouplingDOFsInput(self.project, self.opv)  
        if read.complete:
            self.project.mesh.rotation_decoupling(read.element_id, read.selected_node_id, read.rotations_mask)
            print("[Set Rotation Decoupling] - defined at element {} and at node {}".format(read.element_id, read.selected_node_id))


    def set_material(self):
        mat = MaterialInput(self.opv, self.project.get_material_list_path())
        if mat.material is None:
            return

        if mat.flagEntity:
            # entities_id = self.opv.getListPickedEntities()
            if len(mat.entities_id) == 0:
                return
            for entity in mat.entities_id:
                self.project.set_material_by_entity(entity, mat.material)
            print("[Set Material] - {} defined in the entities {}".format(mat.material.name, mat.entities_id))
            self.opv.changeColorEntities(mat.entities_id, mat.material.getNormalizedColorRGB())
        else:
            self.project.set_material(mat.material)
            entities = []
            for entity in self.project.get_entities():
                entities.append(entity.get_tag())
            print("[Set Material] - {} defined in all entities".format(mat.material.name))
            self.opv.changeColorEntities(entities, mat.material.getNormalizedColorRGB())

    def set_fluid(self):
        entities_id = self.opv.getListPickedEntities()
        fld = FluidInput(self.project.get_fluid_list_path(), entities_id)
        if fld.fluid is None:
            return

        if fld.flagEntity:
            entities_id = self.opv.getListPickedEntities()
            if len(entities_id) == 0:
                return
            for entity in entities_id:
                self.project.set_fluid_by_Entity(entity, fld.fluid)
            print("[Set Fluid] - {} defined in the entities {}".format(fld.fluid.name, entities_id))
            self.opv.changeColorEntities(entities_id, fld.fluid.getNormalizedColorRGB())
        else:
            self.project.set_fluid(fld.fluid)
            entities = []
            for entity in self.project.get_entities():
                entities.append(entity.get_tag())
            print("[Set Fluid] - {} defined in all entities".format(fld.fluid.name))
            self.opv.changeColorEntities(entities, fld.fluid.getNormalizedColorRGB())

    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False):
        read = CrossSectionInput(self.project, self.opv, pipe_to_beam=pipe_to_beam, beam_to_pipe=beam_to_pipe)

        if not read.complete:
            return

        if read.flagEntity:
            if len(read.lines_id) == 0:
                return
            for line in read.lines_id:
                self.project.set_cross_section_by_entity(line, read.cross_section)
                self.project.set_element_type_by_entity(line, read.element_type)
            print("[Set Cross-section] - defined at lines {}".format(read.lines_id))
        elif read.flagElements:
            if len(read.elements_id) == 0:
                return
            else:
                self.project.set_cross_section_by_elements(read.elements_id, read.cross_section)
                if len(read.elements_id)>20:
                    print("[Set Cross-section] - defined at {} selected elements".format(len(read.elements_id)))
        else:
            self.project.set_cross_section_to_all(read.cross_section)
            self.project.set_element_type_to_all(read.element_type)
            print("[Set Cross-section] - defined at all lines")
            
        self.opv.updateEntityRadius()
        self.opv.plotMesh()
    
    def plot_cross_section(self):
        PlotCrossSectionInput(self.project, self.opv)

    def setDOF(self):
        read = DOFInput(self.project, self.opv)
        if read.prescribed_dofs is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)     
        print("[Set Prescribed DOF] - defined at node(s) {}".format(read.nodes_typed))

    def setNodalLoads(self):
        read = LoadsInput(self.project, self.opv)
        if read.loads is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        print("[Set Nodal Load] - defined at node(s) {}".format(read.nodes_typed))
    
    def addMassSpringDamper(self):
        read = MassSpringDamperInput(self.project, self.opv, self.opv.transformPoints)
        if read.lumped_masses is None and read.lumped_stiffness is None and read.lumped_dampings is None:
            return
        if read.lumped_masses is not None:
            print("[Set Mass] - defined at node(s) {}".format(read.nodes_typed))
        if read.lumped_stiffness is not None:
            print("[Set Spring] - defined at node(s) {}".format(read.nodes_typed))
        if read.lumped_dampings is not None:
            print("[Set Damper] - defined at node(s) {}".format(read.nodes_typed))
            self.opv.transformPoints(read.nodes_typed)

    def setAcousticPressure(self):
        read = AcousticPressureInput(self.project, self.opv, self.opv.transformPoints)
        if read.acoustic_pressure is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        print("[Set Acoustic Pressure] - defined at node(s) {}".format(read.nodes_typed))

    def setVolumeVelocity(self):
        read = VolumeVelocityInput(self.project, self.opv, self.opv.transformPoints)
        if read.volume_velocity is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        print("[Set Volume Velocity Source] - defined at node(s) {}".format(read.nodes_typed))

    def setSpecificImpedance(self):
        read = SpecificImpedanceInput(self.project, self.opv, self.opv.transformPoints)
        if read.specific_impedance is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
            self.flag_imported_table = True
        print("[Set Specific Impedance] - defined at node(s) {}".format(read.nodes_typed))
    
    def set_radiation_impedance(self):
        read = RadiationImpedanceInput(self.project, self.opv, self.opv.transformPoints)

        if read.radiation_impedance is None:
            return
        else:
            self.project.set_radiation_impedance_bc_by_node(read.nodes_typed, read.radiation_impedance)
            print("[Set Radiation Impedance] - defined at node(s) {}".format(read.nodes_typed))

    def add_perforated_plate(self):
        # element_id = self.opv.getListPickedElements()
        error("This feature is currently under development and \nit will be available in the future updates.", title="WARNING")

    def set_acoustic_element_length_correction(self):
        read = AcousticElementLengthCorrectionInput(self.project, self.opv)
        if read.type_label is None:
            return
        
    def _load_frequencies_from_table(self, obj):
            self.project.file.f_min = obj.f_min
            self.project.file.f_max = obj.f_max
            self.project.file.f_step = obj.f_step
            self.project.file.frequencies = obj.frequencies
            self.project.file.temp_table_name = obj.imported_table_name  
            return obj.frequencies 
    
    def check_acoustic_bc_tables(self):

        if self.acoustic_pressure_frequencies is not None:
            if self.volume_velocity_frequencies is not None:
                if self.specific_impedance_frequencies is not None:
                    if self.acoustic_pressure_frequencies==self.volume_velocity_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        error("Check frequency setup of all imported tables.")
                        return
                else:
                    if self.acoustic_pressure_frequencies==self.volume_velocity_frequencies:
                        pass
                    else:
                        error("Check frequency setup of imported tables (Acoustic Pressure and Volume Velocity).")
                        return    
            else:
                if self.specific_impedance_frequencies is not None:
                    if self.acoustic_pressure_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        error("Check frequency setup of imported tables (Acoustic Pressure and Specific Impedance).")
                        return
        else:
            if self.volume_velocity_frequencies is not None:
                if self.specific_impedance_frequencies is not None:
                    if self.volume_velocity_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        error("Check frequency setup of imported tables (Volume Velocity and Specific Impedance).")
                        return

    def analysisTypeInput(self):

        inputs = AnalysisTypeInput()
        if inputs.method_ID == -1:
            return
        self.analysis_ID = inputs.analysis_ID
        self.analysis_type_label = inputs.analysis_type_label
        self.analysis_method_label = inputs.analysis_method_label
 
        if self.analysis_ID is None:
            return
 
        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.set_modes(inputs.modes)
        self.project.set_acoustic_solution(None)
        self.project.set_structural_solution(None)

        if self.analysis_ID in [2,4]:
            if not inputs.complete:
                return
            else:
                self.runAnalysis()
        else:
            self.analysisSetup()
        
    def analysisSetup(self):
        
        if self.project.analysis_ID is None:
            return
        if self.project.file._project_name == "":
            return

        #TODO: simplify the structure below
        if self.project.file.temp_table_name is None:
            self.project.load_analysis_file()
            self.f_min, self.f_max, self.f_step = self.project.f_min, self.project.f_max, self.project.f_step 
        else:
            self.project.load_frequencies_from_table()
            self.f_min, self.f_max, self.f_step = self.project.file.f_min, self.project.file.f_max, self.project.file.f_step
  
        self.global_damping = self.project.global_damping
  
        analysis_info = [self.analysis_ID, self.analysis_type_label, self.analysis_method_label]    
        setup = AnalysisSetupInput(analysis_info, self.global_damping, f_min = self.f_min, f_max = self.f_max, f_step = self.f_step)
       
        self.frequencies = setup.frequencies
        self.f_min = setup.f_min
        self.f_max = setup.f_max
        self.f_step = setup.f_step
        self.global_damping = setup.global_damping
        self.setup_analysis_complete = setup.complete

        if not setup.complete:
            return False

        self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
        self.flag_imported_table = False

        if not self.analysis_ID in [3,4]:
            self.project.set_modes(setup.modes)
            self.project.set_damping(self.global_damping)
        else:
            return False
        return True
      
    def analysisOutputResults(self):
        AnalysisOutputResultsInput()

    def runAnalysis(self):

        t0 = time()
        if self.analysis_ID is None or not self.setup_analysis_complete:
            error("Please, it is necessary to choose an analysis type and \nsetup it before trying to solve the model.")
            return

        if self.flag_imported_table:
            if self.analysisSetup():
                return
       
        if self._check_is_there_a_problem():
            return
        self.project.time_to_checking_entries = time()-t0

        t0 = time()
        self.project.load_mapped_cross_section()
        self.project.time_to_process_cross_sections = time()-t0
        self.project.get_dict_multiple_cross_sections()
        t0 = time()
        if self.analysis_ID in [0,1,3,5,6]:
            if self.frequencies is None:
                return
            if len(self.frequencies) == 0:
                return          
        
        if self.analysis_ID == 4:
            # Temporary: breaking code execution to avoid errors in interface usage
            error("The Acoustic Modal Analysis is under development \nand, therefore, it is not currently available.", title=" WARNING ")
            return

        if self.analysis_ID == 2:
            self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
            solve = self.project.get_structural_solve()
            modes = self.project.get_modes()
        elif self.analysis_ID == 4:
            solve = self.project.get_acoustic_solve()
            modes = self.project.get_modes()
        elif self.analysis_ID == 3:
            solve = self.project.get_acoustic_solve()
        elif self.analysis_ID in [5,6]:
            self.project.mesh.enable_fluid_mass_adding_effect()
            solve = self.project.get_acoustic_solve()
            modes = self.project.get_modes()
            damping = self.project.get_damping()
        else:
            self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
            solve = self.project.get_structural_solve()
            modes = self.project.get_modes()
            damping = self.project.get_damping()

        if self.analysis_ID == 2:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [], self.project)
            if solution.solution_structural is None:
                return
            self.project.set_structural_solution(solution.solution_structural)
            self.project.set_structural_natural_frequencies(solution.natural_frequencies_structural.tolist())

        elif self.analysis_ID == 4:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [], self.project)
            if solution.solution_acoustic is None:
                return
            self.project.set_acoustic_solution(solution.solution_acoustic)
            self.project.set_acoustic_natural_frequencies(solution.natural_frequencies_acoustic.tolist())

        elif self.analysis_ID == 3:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, [], [], self.project)
            if solution.solution_acoustic is None:
                return
            self.project.set_acoustic_solution(solution.solution_acoustic)
        elif self.analysis_ID in [5,6]:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, self.project)
            self.solve = solution.solve
            self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
            self.project.set_structural_solution(solution.solution_structural)
        else:
            solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, self.project)
            if solution.solution_structural is None:
                return
            self.solve = solution.solve
            self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
            self.project.set_structural_solution(solution.solution_structural)
        self.project.time_to_postprocess = (time() - t0) - self.project.time_to_solve_model
        
        LogTimes(self.project)
 
    def plotStructuralModeShapes(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID == 2:
            if solution is None:
                return
            plot = PlotStructuralModeShapeInput(self.opv, self.project.natural_frequencies_structural)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalysis(plot.mode_index)
        else:
            return

    def plotDisplacementField(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0,1,5,6]:
            if solution is None:
                return
            plot = PlotDisplacementFieldInput(self.opv, self.frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency)
        else:
            return

    def plotAcousticModeShapes(self):
        self.project.plot_pressure_field = True
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID == 2:
            if solution is None:
                return
            plot = PlotAcousticModeShapeInput(self.opv, self.project.natural_frequencies_acoustic)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalysis(plot.mode_index)
        else:
            return

    def plotAcousticPressureField(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3,5,6]:
            if solution is None:
                return
            plot = PlotAcousticPressureFieldInput(self.opv, self.frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency, acoustic=True)
        else:
            return

    def plotStructuralFrequencyResponse(self):
        node_id = self.opv.getListPickedPoints()
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStructuralFrequencyResponseInput(self.project.get_mesh(), self.analysis_method_label, self.frequencies, solution, node_id)

    def plotAcousticFrequencyResponse(self):
        node_id = self.opv.getListPickedPoints()
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            PlotAcousticFrequencyResponseInput(self.project.get_mesh(), self.analysis_method_label, self.frequencies, solution, node_id)

    def plot_TL_NR(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            Plot_TL_NR_Input(self.project.get_mesh(), self.analysis_method_label, self.frequencies, solution)

    def plotStressField(self):
        self.project.plot_pressure_field = False
        
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStressFieldInput(self.project, self.solve, self.opv)

    def plotStressFrequencyResponse(self):
        solution = self.project.get_structural_solution()
        element_id = self.opv.getListPickedElements()
       
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStressFrequencyResponseInput(self.project, self.solve, element_id, self.analysis_method_label)

    def plotReactionsFrequencyResponse(self):

        if self.analysis_ID in [0,1,5,6]:
            reactions = [self.dict_reactions_at_constrained_dofs, self.dict_reactions_at_springs, self.dict_reactions_at_dampers]
            PlotReactionsInput(self.project.get_mesh(), self.analysis_method_label, self.frequencies, reactions)
            return

    def _check_is_there_a_problem(self):

        title = " ERROR: INSUFFICIENT MODEL INPUTS! "

        cross_section_message = "You should to set a Cross-Section to all\n elements before trying to run any Analysis!"
        material_message = "You should to set a Material to all elements\n before trying to run any Analysis!"
        fluid_message = "You should to set a Fluid to all elements\n before trying to run any Analysis!"
        structural_message = "You should to apply an external load to the model or prescribe a \nnon-null DOF value before trying to solve the Harmonic Analysis!"
        acoustic_message = "You should to insert a Volume Velocity or prescribe an Acoustic \nPressure to a node before trying to solve the Harmonic Analysis!"
          
        if self.analysis_ID == 2:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
        
        elif self.analysis_ID == 4:
            self.project.mesh.check_material_all_elements()
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True

        elif self.analysis_ID == 0 or self.analysis_ID == 1:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(structural=True)
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            elif not self.project.mesh.is_there_loads:
                if not self.project.mesh.is_there_prescribed_dofs:
                    error(structural_message, title = title)
                    return True
    
        elif self.analysis_ID == 3:
            self.project.mesh.check_material_all_elements()
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(acoustic=True)
            if self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            elif not self.project.mesh.is_there_volume_velocity:
                if not self.project.mesh.is_there_acoustic_pressure:
                    error(acoustic_message, title = title)
                    return True

        elif self.analysis_ID == 5 or self.analysis_ID == 6:
            self.project.mesh.check_material_and_cross_section_in_all_elements()
            self.project.mesh.check_fluid_and_cross_section_in_all_elements()
            self.project.mesh.check_nodes_attributes(coupled=True)
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_set_crossSection:
                error(cross_section_message, title = title)
                return True
            elif not self.project.mesh.is_there_volume_velocity:
                if not self.project.mesh.is_there_acoustic_pressure:
                    error(acoustic_message, title = title)
                    return True

    def structural_model_info(self):
        StructuralModelInfoInput(self.project)

    def acoustic_model_info(self):
        AcousticModelInfoInput(self.project)