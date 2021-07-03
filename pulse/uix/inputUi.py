#
from data.user_input.project.newProjectInput import NewProjectInput
from data.user_input.project.loadProjectInput import LoadProjectInput
from data.user_input.project.getStartedInput import GetStartedInput
from data.user_input.project.resetProjectInput import ResetProjectInput
from data.user_input.project.setProjectAttributesInput import SetProjectAttributesInput
from data.user_input.project.setGeometryFileInput import SetGeometryFileInput
from data.user_input.project.setMeshPropertiesInput import SetMeshPropertiesInput
#
from data.user_input.model.setup.structural.structuralElementTypeInput import StructuralElementTypeInput
from data.user_input.model.setup.structural.materialInput import MaterialInput
from data.user_input.model.setup.structural.crossSectionInput import CrossSectionInput
from data.user_input.model.setup.structural.beamXaxisRotationInput import BeamXaxisRotationInput 
from data.user_input.model.setup.structural.dofInput import DOFInput
from data.user_input.model.setup.structural.decouplingRotationDOFsInput import DecouplingRotationDOFsInput
from data.user_input.model.setup.structural.loadsInput import LoadsInput
from data.user_input.model.setup.structural.massSpringDamperInput import MassSpringDamperInput
from data.user_input.model.setup.structural.cappedEndInput import CappedEndInput
from data.user_input.model.setup.structural.stressStiffeningInput import StressStiffeningInput
from data.user_input.model.setup.structural.elasticNodalLinksInput import ElasticNodalLinksInput
#
from data.user_input.model.setup.acoustic.acousticElementTypeInput import AcousticElementTypeInput
from data.user_input.model.setup.acoustic.fluidInput import FluidInput
from data.user_input.model.setup.acoustic.acousticpressureInput import AcousticPressureInput
from data.user_input.model.setup.acoustic.volumevelocityInput import VolumeVelocityInput
from data.user_input.model.setup.acoustic.specificimpedanceInput import SpecificImpedanceInput
from data.user_input.model.setup.acoustic.radiationImpedanceInput import RadiationImpedanceInput
from data.user_input.model.setup.acoustic.elementLengthCorrectionInput import AcousticElementLengthCorrectionInput
from data.user_input.model.setup.acoustic.compressorModelinput import CompressorModelInput
#
from data.user_input.analysis.analysisTypeInput import AnalysisTypeInput
from data.user_input.analysis.analysisSetupInput import AnalysisSetupInput
from data.user_input.analysis.runAnalysisInput import RunAnalysisInput
#
from data.user_input.plots.structural.plotStructuralModeShapeInput import PlotStructuralModeShapeInput
from data.user_input.plots.structural.plotDisplacementFieldInput import PlotDisplacementFieldInput
from data.user_input.plots.structural.plotStructuralFrequencyResponseInput import PlotStructuralFrequencyResponseInput
from data.user_input.plots.structural.plotReactionsInput import PlotReactionsInput
from data.user_input.plots.structural.plotStressFieldInput import PlotStressFieldInput
from data.user_input.plots.structural.plotStressFrequencyResponseInput import PlotStressFrequencyResponseInput
#
from data.user_input.plots.acoustic.plotAcousticModeShapeInput import PlotAcousticModeShapeInput
from data.user_input.plots.acoustic.plotAcousticPressureFieldInput import PlotAcousticPressureFieldInput
from data.user_input.plots.acoustic.plotAcousticFrequencyResponseInput import PlotAcousticFrequencyResponseInput
from data.user_input.plots.acoustic.plot_TL_NR_Input import Plot_TL_NR_Input
#
from data.user_input.plots.structural.plotCrossSectionInput import PlotCrossSectionInput
from data.user_input.model.info.structuralModel_InfoInput import StructuralModelInfoInput
from data.user_input.model.info.acousticModel_InfoInput import AcousticModelInfoInput
#
from data.user_input.project.LogTimes import LogTimes
from data.user_input.project.printMessageInput import PrintMessageInput
#
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.entity import Entity
from pulse.project import Project
from pulse.utils import error
#
from time import time

window_title1 = "ERROR MESSAGE"
window_title2 = "WARNING MESSAGE"

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
        self.project.none_project_action = False
        self.setup_analysis_complete = False
        self.flag_imported_table = False

    def beforeInput(self):
        try:
            self.opv.inputObject.close()
            self.opv.setInputObject(None)
        except:
            return

    def new_project(self, config):
        new_project_input = NewProjectInput(self.project, config)
        return self.initial_project_action(new_project_input.create)

    def loadProject(self, config, path=None):
        load_project = LoadProjectInput(self.project, config, path)
        return self.initial_project_action(load_project.complete) 

    def getStarted(self, config):
        getStarted = GetStartedInput(self.project, config, self)
        return self.initial_project_action(getStarted.draw)          
    
    def initial_project_action(self, obj):
        if obj:
            self.project.none_project_action = False
            self.parent.menuWidget.tree_widget.modify_model_setup_items_access(False) 
            self.parent.set_enable_menuBar(True)
            return True
        else:
            self.project.none_project_action = True
            self.parent.menuWidget.tree_widget.modify_model_setup_items_access(True)
            self.parent.set_enable_menuBar(False)
            return False                 

    def reset_project(self):
        if not self.project.none_project_action:
            ResetProjectInput(self.project, self.opv)

    def set_project_attributes(self):
        SetProjectAttributesInput(self.project, self.opv)
        self.parent.changeWindowTitle(self.project._project_name)

    def set_geometry_file(self):
        SetGeometryFileInput(self.project, self.opv)

    def set_mesh_properties(self):
        read = SetMeshPropertiesInput(self.project, self.opv)

    def setStructuralElementType(self):
        read = StructuralElementTypeInput(self.project, self.opv)
        if read.complete:           
            if self.set_cross_section(  pipe_to_beam=read.pipe_to_beam, 
                                        beam_to_pipe=read.beam_to_pipe, 
                                        lines_to_update_cross_section=read.list_lines_to_update_cross_section ):
                if read.lines_id != []:
                    _cache_selected_lines = read.lines_id
                else:
                    _cache_selected_lines = read.list_lines_to_update_cross_section
                self.set_material(cache_selected_lines = _cache_selected_lines)
            self.opv.updateEntityRadius()
            self.opv.changePlotToEntitiesWithCrossSection()

    def set_material(self, cache_selected_lines=[]):
        mat = MaterialInput(    self.opv, 
                                self.project.get_material_list_path(), 
                                cache_selected_lines = cache_selected_lines)
                                
        if mat.material is None:
            return

        if mat.flagSelectedLines:
            # entities_id = self.opv.getListPickedEntities()
            if len(mat.lines_ids) == 0:
                return
            for line in mat.lines_ids:
                self.project.set_material_by_line(line, mat.material)
            print("[Set Material] - {} defined in the entities {}".format(mat.material.name, mat.lines_ids))
            # self.opv.changeColorEntities(mat.lines_ids, mat.material.getNormalizedColorRGB())
        else:
            self.project.set_material(mat.material)
            entities = []
            for entity in self.project.entities:#get_entities():
                entities.append(entity.get_tag())
            print("[Set Material] - {} defined in all entities".format(mat.material.name))
            # self.opv.changeColorEntities(entities, mat.material.getNormalizedColorRGB())
            
    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = CrossSectionInput(   self.project, 
                                    self.opv, 
                                    pipe_to_beam = pipe_to_beam, 
                                    beam_to_pipe = beam_to_pipe, 
                                    lines_to_update_cross_section = lines_to_update_cross_section)

        if not read.complete:
            return False

        if read.flagEntity:
            if len(read.lines_typed) == 0:
                return False
            for line in read.lines_typed:
                self.project.set_cross_section_by_entity(line, read.cross_section)
                self.project.set_structural_element_type_by_entity(line, read.element_type)
            print("[Set Cross-section] - defined at lines {}".format(read.lines_typed))

        elif read.flagElements:
            if len(read.elements_typed) == 0:
                return False
            else:
                self.project.set_cross_section_by_elements(read.elements_typed, read.cross_section)
                if len(read.elements_typed) > 20:
                    print("[Set Cross-section] - defined at {} selected elements".format(len(read.elements_typed)))

        else:
            self.project.set_cross_section_to_all(read.cross_section)
            self.project.set_structural_element_type_to_all(read.element_type)
            print("[Set Cross-section] - defined at all lines")
            
        self.opv.updateEntityRadius()
        self.opv.changePlotToMesh()
        return True
    
    def plot_cross_section(self):
        PlotCrossSectionInput(self.project, self.opv)

    def set_beam_xaxis_rotation(self):
        BeamXaxisRotationInput(self.project, self.opv)

    def setDOF(self):
        read = DOFInput(self.project, self.opv)
        if read.prescribed_dofs is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)     
        print("[Set Prescribed DOF] - defined at node(s) {}".format(read.nodes_typed))

    def setRotationDecoupling(self):
        read = DecouplingRotationDOFsInput(self.project, self.opv)  
        if read.complete:
            print("[Set Rotation Decoupling] - defined at element {} and at node {}".format(read.element_id, read.selected_node_id))

    def setNodalLoads(self):
        read = LoadsInput(self.project, self.opv)
        if read.loads is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        print("[Set Nodal Load] - defined at node(s) {}".format(read.nodes_typed))
        
    def addMassSpringDamper(self):
        read = MassSpringDamperInput(self.project, self.opv)
        if read.lumped_masses is None and read.lumped_stiffness is None and read.lumped_dampings is None:
            return
        if read.lumped_masses is not None:
            print("[Set Mass] - defined at node(s) {}".format(read.nodes_typed))
        if read.lumped_stiffness is not None:
            print("[Set Spring] - defined at node(s) {}".format(read.nodes_typed))
        if read.lumped_dampings is not None:
            print("[Set Damper] - defined at node(s) {}".format(read.nodes_typed))
        # self.opv.transformPoints(read.nodes_typed)

    def setcappedEnd(self):
        read = CappedEndInput(self.project, self.opv)
        if not read.complete:
            return

    def set_stress_stress_stiffening(self):
        StressStiffeningInput(self.project, self.opv)
        return

    def add_elastic_nodal_links(self):
        ElasticNodalLinksInput(self.project, self.opv)
        return

    def set_acoustic_element_type(self):
        read = AcousticElementTypeInput(self.project, self.opv)
        if not read.complete:
            return
        self.set_fluid()

    def set_fluid(self):
        fld = FluidInput(self.project, self.opv)
        if fld.fluid is None:
            return

    def setAcousticPressure(self):
        read = AcousticPressureInput(self.project, self.opv, self.opv.transformPoints)
        if read.acoustic_pressure is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        self.opv.updateRendererMesh()
        print("[Set Acoustic Pressure] - defined at node(s) {}".format(read.nodes_typed))

    def setVolumeVelocity(self):
        read = VolumeVelocityInput(self.project, self.opv, self.opv.transformPoints)
        if read.volume_velocity is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
        self.opv.updateRendererMesh()
        print("[Set Volume Velocity Source] - defined at node(s) {}".format(read.nodes_typed))

    def setSpecificImpedance(self):
        read = SpecificImpedanceInput(self.project, self.opv, self.opv.transformPoints)
        if read.specific_impedance is None:
            return
        if read.imported_table:
            self.prescribed_dofs_frequencies = self._load_frequencies_from_table(read)
            self.flag_imported_table = True
        self.opv.updateRendererMesh()
        print("[Set Specific Impedance] - defined at node(s) {}".format(read.nodes_typed))
    
    def set_radiation_impedance(self):
        read = RadiationImpedanceInput(self.project, self.opv, self.opv.transformPoints)

        if read.radiation_impedance is None:
            return
        else:
            self.project.set_radiation_impedance_bc_by_node(read.nodes_typed, read.radiation_impedance)
            self.opv.updateRendererMesh()
            print("[Set Radiation Impedance] - defined at node(s) {}".format(read.nodes_typed))

    def add_perforated_plate(self):
        title = "UNAVAILABLE FUNCTIONALITY"
        message = "This feature is currently under development and \nit will be available in the future updates."
        PrintMessageInput([title, message, window_title2])

    def set_acoustic_element_length_correction(self):
        read = AcousticElementLengthCorrectionInput(self.project, self.opv)
        if read.type_label is None:
            return

    def add_compressor_excitation(self):
        CompressorModelInput(self.project, self.opv)
        self.opv.updateRendererMesh()
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

        read = AnalysisTypeInput()
        if read.method_ID == -1:
            return
        self.analysis_ID = read.analysis_ID
        self.analysis_type_label = read.analysis_type_label
        self.analysis_method_label = read.analysis_method_label

        if self.analysis_ID is None:
            self.project.analysis_ID = None
            return

        self.project.set_analysis_type(self.analysis_ID, self.analysis_type_label, self.analysis_method_label)
        self.project.set_modes_sigma(read.modes, sigma=read.sigma_factor)
        self.project.set_acoustic_solution(None)
        self.project.set_structural_solution(None)

        if self.analysis_ID in [2,4]:
            if not read.complete:
                return
            else:
                self.setup_analysis_complete = True
                self.runAnalysis()
        else:
            self.setup_analysis_complete = False
            self.analysisSetup()
        
    def analysisSetup(self):

        if self.project.analysis_ID in [None, 2, 4]:
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
        read = AnalysisSetupInput(self.project, f_min = self.f_min, f_max = self.f_max, f_step = self.f_step)

        if not read.complete and self.project.setup_analysis_complete:
            return

        self.frequencies = read.frequencies
        self.f_min = read.f_min
        self.f_max = read.f_max
        self.f_step = read.f_step
        self.global_damping = read.global_damping
        self.setup_analysis_complete = read.complete

        if not read.complete:
            self.project.setup_analysis_complete = False
            return False
        else:
            self.project.setup_analysis_complete = True

        self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
        self.flag_imported_table = False

        if not self.analysis_ID in [3,4]:
            self.project.set_modes_sigma(read.modes)
            self.project.set_damping(self.global_damping)
        # else:
        #     return False

        if read.flag_run:
            self.runAnalysis()
        return True
    
    def runAnalysis(self):
        t0 = time()
        if self.analysis_ID is None or not self.setup_analysis_complete:
            
            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and \nsetup it before trying to solve the model."
            PrintMessageInput([title, message, window_title1])
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

        if self.analysis_ID in [0,1,3,5,6]:
            if self.frequencies is None:
                return
            if len(self.frequencies) == 0:
                return

        if self.project.mesh._process_beam_nodes_and_indexes():
            if self.analysis_ID not in [0,1,2]:
                title = "INCORRECT ANALYSIS TYPE"
                message = "There are only BEAM_1 elements in the model, therefore, \nonly structural analysis are allowable."
                info_text = [title, message, window_title2]
                PrintMessageInput(info_text)
                return 
        
        logWindow = LogTimes(self.project, self.analysis_ID, self.analysis_type_label)

        # As coisas que eu copiei e colei no LogTimes sairam daqui.
        # Apagar isso quando as coisas estiverem prontas por favor.


        # t0 = time()
        # self.project.load_mapped_cross_section()
        # self.project.time_to_process_cross_sections = time()-t0
        # self.project.get_dict_multiple_cross_sections()

        # if self.analysis_ID in [0,1,3,5,6]:
        #     if self.frequencies is None:
        #         return
        #     if len(self.frequencies) == 0:
        #         return

        # if self.project.mesh._process_beam_nodes_and_indexes():
        #     if self.analysis_ID not in [0,1,2]:
        #         title = "INCORRECT ANALYSIS TYPE"
        #         message = "There are only BEAM_1 elements in the model, therefore, \nonly structural analysis are allowable."
        #         info_text = [title, message, window_title2]
        #         PrintMessageInput(info_text)
        #         return
        
        # if self.analysis_ID == 2:
        #     self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
        #     solve = self.project.get_structural_solve()
        #     modes = self.project.get_modes()
        # elif self.analysis_ID == 4:
        #     solve = self.project.get_acoustic_solve()
        #     modes = self.project.get_modes()
        # elif self.analysis_ID == 3:
        #     solve = self.project.get_acoustic_solve()
        # elif self.analysis_ID in [5,6]:
        #     self.project.mesh.enable_fluid_mass_adding_effect()
        #     solve = self.project.get_acoustic_solve()
        #     modes = self.project.get_modes()
        #     damping = self.project.get_damping()
        # else:
        #     self.project.mesh.enable_fluid_mass_adding_effect(reset=True)
        #     solve = self.project.get_structural_solve()
        #     modes = self.project.get_modes()
        #     damping = self.project.get_damping()

        # self.project.time_to_preprocess_model = time() - t0

        #################################

        # if self.analysis_ID == 2:
        #     solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [], self.project)
        #     if solution.solution_structural is None:
        #         return
        #     self.project.set_structural_solution(solution.solution_structural)
        #     self.project.set_structural_natural_frequencies(solution.natural_frequencies_structural.tolist())

        # elif self.analysis_ID == 4:
        #     solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, [], modes, [], self.project)
        #     if solution.solution_acoustic is None:
        #         return
        #     self.project.set_acoustic_solution(solution.solution_acoustic)
        #     self.project.set_acoustic_natural_frequencies(solution.natural_frequencies_acoustic.tolist())
        
        # elif self.analysis_ID == 3:
        #     solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, [], [], self.project)
        #     if solution.solution_acoustic is None:
        #         return
        #     self.project.set_acoustic_solution(solution.solution_acoustic)
        # elif self.analysis_ID in [5,6]:
        #     solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, self.project)
        #     self.solve = solution.solve
        #     self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
        #     self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
        #     self.project.set_structural_solution(solution.solution_structural)
        # else:
        #     solution = RunAnalysisInput(solve, self.analysis_ID, self.analysis_type_label, self.frequencies, modes, damping, self.project)
        #     if solution.solution_structural is None:
        #         return
        #     self.solve = solution.solve
        #     self.dict_reactions_at_constrained_dofs = solution.dict_reactions_at_constrained_dofs
        #     self.dict_reactions_at_springs, self.dict_reactions_at_dampers = solution.dict_reactions_at_springs, solution.dict_reactions_at_dampers
        #     self.project.set_structural_solution(solution.solution_structural)
        
        # self.project.time_to_postprocess = time() - (t0 + self.project.time_to_solve_model + self.project.time_to_preprocess_model)
        # self.project.total_time = time() - t0

    def plotStructuralModeShapes(self):
            self.project.set_min_max_type_stresses("", "", "")
            self.project.plot_pressure_field = False
            self.project.plot_stress_field = False
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
        self.project.plot_stress_field = False
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
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID == 4:
            if solution is None:
                return
            plot = PlotAcousticModeShapeInput(self.opv, self.project.natural_frequencies_acoustic)
            if plot.mode_index is None:
                return
            self.opv.changeAndPlotAnalysis(plot.mode_index, pressure_field_plot=True, real_part=plot.flag_real_part)
        else:
            return

    def plotAcousticPressureField(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3,5,6]:
            if solution is None:
                return
            plot = PlotAcousticPressureFieldInput(self.opv, self.frequencies)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency, pressure_field_plot=True)
        else:
            return

    def plotStructuralFrequencyResponse(self):
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStructuralFrequencyResponseInput(self.project, self.opv, self.analysis_method_label, self.frequencies, solution)

    def plotAcousticFrequencyResponse(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            PlotAcousticFrequencyResponseInput(self.project, self.opv, self.analysis_method_label, self.frequencies, solution)

    def plot_TL_NR(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            Plot_TL_NR_Input(self.project, self.opv, self.analysis_method_label, self.frequencies, solution)

    def plotStressField(self):
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = True
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStressFieldInput(self.project, self.solve, self.opv)

    def plotStressFrequencyResponse(self):
        solution = self.project.get_structural_solution()
       
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStressFrequencyResponseInput(self.opv, self.project, self.solve, self.analysis_method_label)

    def plotReactionsFrequencyResponse(self):

        if self.analysis_ID in [0,1,5,6]:
            reactions = [self.dict_reactions_at_constrained_dofs, self.dict_reactions_at_springs, self.dict_reactions_at_dampers]
            PlotReactionsInput(self.opv, self.project.get_mesh(), self.analysis_method_label, self.frequencies, reactions)
            return

    def _check_is_there_a_problem(self):

        title = " ERROR: INSUFFICIENT MODEL INPUTS! "

        cross_section_message = "You should to set a Cross-Section to all\n elements before trying to run any Analysis!"
        material_message = "You should to set a Material to all elements\n before trying to run any Analysis!"
        fluid_message = "You should to set a Fluid to all elements\n before trying to run any Analysis!"
        all_fluid_inputs_message = "You should insert all fluid properties for wide-duct, LRF \nfluid equivalent and LRF full acoustic element types."
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
            self.project.mesh.check_fluid_inputs_in_all_elements()
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_all_fluid_inputs:
                error(all_fluid_inputs_message, title = title)
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
            self.project.mesh.check_fluid_inputs_in_all_elements()
            self.project.mesh.check_nodes_attributes(acoustic=True)
            if self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_all_fluid_inputs:
                error(all_fluid_inputs_message, title = title)
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
            self.project.mesh.check_fluid_inputs_in_all_elements()
            self.project.mesh.check_nodes_attributes(coupled=True)
            if self.project.mesh.check_set_material:
                error(material_message, title = title)
                return True
            elif self.project.mesh.check_set_fluid:
                error(fluid_message, title = title)
                return True
            elif self.project.mesh.check_all_fluid_inputs:
                error(all_fluid_inputs_message, title = title)
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

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title])