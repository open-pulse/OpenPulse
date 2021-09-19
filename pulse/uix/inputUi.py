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
from data.user_input.model.setup.structural.expansionJointInput import ExpansionJointInput
#
from data.user_input.model.setup.acoustic.acousticElementTypeInput import AcousticElementTypeInput
from data.user_input.model.setup.acoustic.fluidInput import FluidInput
from data.user_input.model.setup.acoustic.acousticpressureInput import AcousticPressureInput
from data.user_input.model.setup.acoustic.volumevelocityInput import VolumeVelocityInput
from data.user_input.model.setup.acoustic.specificimpedanceInput import SpecificImpedanceInput
from data.user_input.model.setup.acoustic.radiationImpedanceInput import RadiationImpedanceInput
from data.user_input.model.setup.acoustic.elementLengthCorrectionInput import AcousticElementLengthCorrectionInput
from data.user_input.model.setup.acoustic.perforatedPlateInput import PerforatedPlateInput
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
from data.user_input.project.printMessageInput import PrintMessageInput
#
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.entity import Entity
from pulse.project import Project
#
from time import time

window_title_1 = "ERROR MESSAGE"
window_title_2 = "WARNING MESSAGE"

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
        # self.flag_imported_table = False

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
        return read.complete

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
        mat = MaterialInput(    self.project,
                                self.opv, 
                                cache_selected_lines = cache_selected_lines)
                                
        if mat.material is None:
            return
         
    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = CrossSectionInput(   self.project, 
                                    self.opv, 
                                    pipe_to_beam = pipe_to_beam, 
                                    beam_to_pipe = beam_to_pipe, 
                                    lines_to_update_cross_section = lines_to_update_cross_section)

        if not read.complete:
            return False
        else:
            return True        

    def plot_cross_section(self):
        PlotCrossSectionInput(self.project, self.opv)

    def set_beam_xaxis_rotation(self):
        BeamXaxisRotationInput(self.project, self.opv)

    def setDOF(self):
        DOFInput(self.project, self.opv)   
        
    def setRotationDecoupling(self):
        read = DecouplingRotationDOFsInput(self.project, self.opv)  
        if read.complete:
            print("[Set Rotation Decoupling] - defined at element {} and at node {}".format(read.element_id, read.selected_node_id))

    def setNodalLoads(self):
        LoadsInput(self.project, self.opv)
        
    def addMassSpringDamper(self):
        MassSpringDamperInput(self.project, self.opv)

    def setcappedEnd(self):
        CappedEndInput(self.project, self.opv)

    def set_stress_stress_stiffening(self):
        StressStiffeningInput(self.project, self.opv)

    def add_elastic_nodal_links(self):
        ElasticNodalLinksInput(self.project, self.opv)
    
    def add_expansion_joint(self):
        ExpansionJointInput(self.project, self.opv)

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
        AcousticPressureInput(self.project, self.opv)
    
    def setVolumeVelocity(self):
        VolumeVelocityInput(self.project, self.opv)

    def setSpecificImpedance(self):
        SpecificImpedanceInput(self.project, self.opv)
    
    def set_radiation_impedance(self):
        RadiationImpedanceInput(self.project, self.opv)

    def add_perforated_plate(self):
        PerforatedPlateInput(self.project, self.opv)

    def set_acoustic_element_length_correction(self):
        AcousticElementLengthCorrectionInput(self.project, self.opv)

    def add_compressor_excitation(self):
        CompressorModelInput(self.project, self.opv)
        # self.opv.updateRendererMesh()
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
            return False
        if self.project.file._project_name == "":
            return False

        #TODO: simplify the structure below
        # if self.project.file.temp_table_name is None:
        self.project.load_analysis_file()
        self.f_min, self.f_max, self.f_step = self.project.get_frequency_setup() 
        # else:
        #     self.project.load_frequencies_from_table()
        #     self.f_min, self.f_max, self.f_step = self.project.file.f_min, self.project.file.f_max, self.project.file.f_step

        self.global_damping = self.project.global_damping    
        read = AnalysisSetupInput(self.project, f_min=self.f_min, f_max=self.f_max, f_step=self.f_step)

        if not read.complete:
            return False

        if self.project.setup_analysis_complete:
            return False

        self.frequencies = read.frequencies
        self.f_min = read.f_min
        self.f_max = read.f_max
        self.f_step = read.f_step
        self.global_damping = read.global_damping
        self.setup_analysis_complete = read.complete

        if read.complete:
            self.project.setup_analysis_complete = True
        else:
            self.project.setup_analysis_complete = False
            return False
        
        self.project.set_frequencies(self.frequencies, self.f_min, self.f_max, self.f_step)
        # self.flag_imported_table = False

        if not self.analysis_ID in [3,4]:
            self.project.set_modes_sigma(read.modes)
            self.project.set_damping(self.global_damping)
        # else:
        #     return False

        if read.flag_run:
            self.runAnalysis()
        return True
    
    def runAnalysis(self):

        # t0 = time()
        if self.analysis_ID is None or not self.setup_analysis_complete:
            
            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and \nsetup it before trying to solve the model."
            PrintMessageInput([title, message, window_title_1])
            return

        # if self.flag_imported_table:
        #     if self.analysisSetup():
        #         return

        self.before_run = self.project.get_model_checks()
        if self.before_run.check_is_there_a_problem(self.analysis_ID):
            return
        # self.project.time_to_checking_entries = time()-t0

        read = RunAnalysisInput(self.project, self.analysis_ID, self.analysis_type_label)
        if read.complete:
            if self.analysis_ID == 2:
                self.before_run.check_modal_analysis_imported_data()
            elif self.analysis_ID in [3,5,6]:
                self.before_run.check_all_acoustic_criteria()

        
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
            PlotStressFieldInput(self.project, self.opv)

    def plotStressFrequencyResponse(self):
        solution = self.project.get_structural_solution()
       
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            PlotStressFrequencyResponseInput(self.opv, self.project, self.analysis_method_label)

    def plotReactionsFrequencyResponse(self):

        if self.analysis_ID in [0,1,5,6]:
            PlotReactionsInput( self.opv, 
                                self.project,
                                self.analysis_method_label, 
                                self.frequencies    )
            return

    def structural_model_info(self):
        StructuralModelInfoInput(self.project, self.opv)

    def acoustic_model_info(self):
        AcousticModelInfoInput(self.project, self.opv)


    # def _load_frequencies_from_table(self, _read):
    #     self.project.file.f_min = _read.f_min
    #     self.project.file.f_max = _read.f_max
    #     self.project.file.f_step = _read.f_step
    #     self.project.file.frequencies = _read.frequencies
    #     # self.project.file.temp_table_name = _read.imported_table_name  
    #     # return _read.frequencies 
    

    def check_acoustic_bc_tables(self):

        title = "Error while checking tables"

        if self.acoustic_pressure_frequencies is not None:
            if self.volume_velocity_frequencies is not None:
                if self.specific_impedance_frequencies is not None:
                    if self.acoustic_pressure_frequencies==self.volume_velocity_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        message = "Check frequency setup of all imported tables."
                        PrintMessageInput([title, message, window_title_1])
                        return
                else:
                    if self.acoustic_pressure_frequencies==self.volume_velocity_frequencies:
                        pass
                    else:
                        message = "Check frequency setup of imported tables (Acoustic Pressure and Volume Velocity)."
                        PrintMessageInput([title, message, window_title_1])
                        return    
            else:
                if self.specific_impedance_frequencies is not None:
                    if self.acoustic_pressure_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        message = "Check frequency setup of imported tables (Acoustic Pressure and Specific Impedance)."
                        PrintMessageInput([title, message, window_title_1])
                        return
        else:
            if self.volume_velocity_frequencies is not None:
                if self.specific_impedance_frequencies is not None:
                    if self.volume_velocity_frequencies==self.specific_impedance_frequencies:
                        pass
                    else:
                        message = "Check frequency setup of imported tables (Volume Velocity and Specific Impedance)."
                        PrintMessageInput([title, message, window_title_1])
                        return
 

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title])