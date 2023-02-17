#
from data.user_input.project.newProjectInput import NewProjectInput
from data.user_input.project.loadProjectInput import LoadProjectInput
from data.user_input.project.getStartedInput import GetStartedInput
from data.user_input.project.resetProjectInput import ResetProjectInput
from data.user_input.project.geometryDesignerInput import GeometryDesignerInput
from data.user_input.project.setProjectAttributesInput import SetProjectAttributesInput
from data.user_input.project.setGeometryFileInput import SetGeometryFileInput
from data.user_input.project.setMeshPropertiesInput import SetMeshPropertiesInput
from data.user_input.project.aboutOpenPulseInput import AboutOpenPulseInput
#
from data.user_input.model.setup.structural.structuralElementTypeInput import StructuralElementTypeInput
from data.user_input.model.setup.structural.materialInput import MaterialInput
from data.user_input.model.setup.structural.crossSectionInput import CrossSectionInput
from data.user_input.model.setup.structural.flangesInput import FlangesInput
from data.user_input.model.setup.structural.beamXaxisRotationInput import BeamXaxisRotationInput 
from data.user_input.model.setup.structural.dofInput import DOFInput
from data.user_input.model.setup.structural.decouplingRotationDOFsInput import DecouplingRotationDOFsInput
from data.user_input.model.setup.structural.loadsInput import LoadsInput
from data.user_input.model.setup.structural.massSpringDamperInput import MassSpringDamperInput
from data.user_input.model.setup.structural.cappedEndInput import CappedEndInput
from data.user_input.model.setup.structural.stressStiffeningInput import StressStiffeningInput
from data.user_input.model.setup.structural.elasticNodalLinksInput import ElasticNodalLinksInput
from data.user_input.model.setup.structural.expansionJointInput import ExpansionJointInput
from data.user_input.model.setup.structural.valvesInput import ValvesInput
#
from data.user_input.model.setup.acoustic.acousticElementTypeInput import AcousticElementTypeInput
from data.user_input.model.setup.acoustic.fluidInput import FluidInput
from data.user_input.model.setup.acoustic.setFluidCompositionInput import SetFluidCompositionInput
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
from data.user_input.plots.acoustic.plotPerforatedPlateConvergenceData import PlotPerforatedPlateConvergenceData
#
from data.user_input.plots.animation.animationSettingsInput import AnimationSettingsInput
from data.user_input.plots.structural.plotCrossSectionInput import PlotCrossSectionInput
from data.user_input.plots.render.rendererUserPreferencesInput import RendererUserPreferencesInput
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
        self.global_damping = [0,0,0,0]

        self.project.none_project_action = False

    def beforeInput(self):
        try:
            self.opv.inputObject.close()
            self.opv.setInputObject(None)
        except:
            return

    def processInput(self, workingClass, *args, **kwargs):
        try:
            self.beforeInput()
            read = workingClass(*args, **kwargs)
            self.opv.setInputObject(None)
            return read
        except Exception as log_error:
            title = "Error detected in processInput method"
            message = str(log_error)
            PrintMessageInput([title, message, window_title_1])
            # return read

    def new_project(self, config):
        new_project_input = self.processInput(NewProjectInput, self.project, self.opv, config)
        return self.initial_project_action(new_project_input.create)

    def loadProject(self, config, path=None):
        load_project = self.processInput(LoadProjectInput, self.project, self.opv, config, path)
        return self.initial_project_action(load_project.complete) 

    def getStarted(self, config):
        self.parent.menuWidget.tree_widget.modify_model_setup_items_access(True)
        get_started = self.processInput(GetStartedInput, self.project, self.opv, config, self)
        return self.initial_project_action(get_started.draw)          
    
    def initial_project_action(self, obj):
        if self.project.empty_geometry:
            self.parent.set_enable_menuBar(False)
            self.parent.menuWidget.tree_widget.modify_create_geometry_item_access(False)
            return True  
        if obj:
            self.project.none_project_action = False
            self.parent.set_enable_menuBar(True)
            self.parent.menuWidget.tree_widget.modify_model_setup_items_access(False) 
            return True
        else:
            self.project.none_project_action = True
            self.parent.set_enable_menuBar(False)
            self.parent.menuWidget.tree_widget.modify_model_setup_items_access(True)
            return False                 

    def reset_project(self):
        if not self.project.none_project_action:
            self.processInput(ResetProjectInput, self.project, self.opv)
            
    def set_project_attributes(self):
        self.processInput(SetProjectAttributesInput, self.project, self.opv)
        self.parent.changeWindowTitle(self.project._project_name)

    def set_geometry_file(self):
        self.processInput(SetGeometryFileInput, self.project, self.opv)

    def call_geometry_designer(self):
        read = self.processInput(GeometryDesignerInput, self.project, self.opv)
        return read.complete

    def set_mesh_properties(self):
        read = self.processInput(SetMeshPropertiesInput, self.project, self.opv)
        return read.complete

    def set_material(self):
        self.processInput(MaterialInput, self.project, self.opv)   
         
    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = self.processInput(   CrossSectionInput, self.project, self.opv, 
                                    pipe_to_beam = pipe_to_beam, beam_to_pipe = beam_to_pipe, 
                                    lines_to_update_cross_section = lines_to_update_cross_section   ) 
        return read.complete

    def add_flanges(self):
        self.processInput(FlangesInput, self.project, self.opv)

    def setStructuralElementType(self):
        read = self.processInput(StructuralElementTypeInput, self.project, self.opv)
        if read.complete:
            if read.pipe_to_beam or read.beam_to_pipe:         
                self.set_cross_section( pipe_to_beam=read.pipe_to_beam, beam_to_pipe=read.beam_to_pipe, 
                                        lines_to_update_cross_section=read.list_lines_to_update_cross_section )

    def plot_cross_section(self):
        self.processInput(PlotCrossSectionInput, self.project, self.opv)

    def mesh_setup_visibility(self):
        self.processInput(RendererUserPreferencesInput, self.project, self.opv)
        
    def set_beam_xaxis_rotation(self):
        self.processInput(BeamXaxisRotationInput, self.project, self.opv)
        
    def setDOF(self):
        self.processInput(DOFInput, self.project, self.opv)   
        
    def setRotationDecoupling(self):
        self.processInput(DecouplingRotationDOFsInput, self.project, self.opv)
        
    def setNodalLoads(self):
        self.processInput(LoadsInput, self.project, self.opv)
        
    def addMassSpringDamper(self):
        self.processInput(MassSpringDamperInput, self.project, self.opv)

    def setcappedEnd(self):
        self.processInput(CappedEndInput, self.project, self.opv)

    def set_stress_stress_stiffening(self):
        self.processInput(StressStiffeningInput, self.project, self.opv)

    def add_elastic_nodal_links(self):
        self.processInput(ElasticNodalLinksInput, self.project, self.opv)
    
    def add_expansion_joint(self):
        self.processInput(ExpansionJointInput, self.project, self.opv)

    def add_valve(self):
        return self.processInput(ValvesInput, self.project, self.opv)

    def set_acoustic_element_type(self):
        self.processInput(AcousticElementTypeInput, self.project, self.opv)

    def set_fluid(self):
        self.processInput(FluidInput, self.project, self.opv)

    def set_fluid_composition(self):
        self.processInput(SetFluidCompositionInput, self.project, self.opv)

    def setAcousticPressure(self):
        self.processInput(AcousticPressureInput, self.project, self.opv)
    
    def setVolumeVelocity(self):
        self.processInput(VolumeVelocityInput, self.project, self.opv)

    def setSpecificImpedance(self):
        self.processInput(SpecificImpedanceInput, self.project, self.opv)
    
    def set_radiation_impedance(self):
        self.processInput(RadiationImpedanceInput, self.project, self.opv)

    def add_perforated_plate(self):
        self.processInput(PerforatedPlateInput, self.project, self.opv)

    def set_acoustic_element_length_correction(self):
        self.processInput(AcousticElementLengthCorrectionInput, self.project, self.opv)

    def add_compressor_excitation(self):
        self.processInput(CompressorModelInput, self.project, self.opv)
        # self.opv.updateRendererMesh()                                

    def analysisTypeInput(self):

        read = self.processInput(AnalysisTypeInput)

        if not read.complete:
            return

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
        
        if self.analysis_ID in [0, 1, 3, 5, 6]:
            self.project.set_structural_solution(None)
            self.project.set_acoustic_solution(None)
        
        if self.analysis_ID in [2, 4]:
            self.project.update_project_analysis_setup_state(True)
            self.runAnalysis()
        else:
            self.analysisSetup()
                    
    def analysisSetup(self):

        if self.project.analysis_ID in [None, 2, 4]:
            return False
        if self.project.file._project_name == "":
            return False

        read = self.processInput(AnalysisSetupInput, self.project)
        
        if read.complete:
            if read.flag_run:
                self.runAnalysis() 
            return True   
        else:
            return False
       
    def runAnalysis(self):

        # t0 = time()
        if self.analysis_ID is None or not self.project.setup_analysis_complete:
            
            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and \nsetup it before trying to solve the model."
            PrintMessageInput([title, message, window_title_1])
            return

        self.before_run = self.project.get_pre_solution_model_checks(opv=self.opv)
        if self.before_run.check_is_there_a_problem(self.analysis_ID):
            return
        # self.project.time_to_checking_entries = time()-t0

        read = self.processInput(RunAnalysisInput, self.project, self.analysis_ID, self.analysis_type_label)
        if read.complete:
            if self.analysis_ID == 2:
                self.before_run.check_modal_analysis_imported_data()
            elif self.analysis_ID in [3,5,6]:
                self.before_run.check_all_acoustic_criteria()

            self.after_run = self.project.get_post_solution_model_checks(opv=self.opv)
            self.after_run.check_all_acoustic_criterias()
        
    def plotStructuralModeShapes(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if solution is None:
            return
        if self.analysis_ID in [2, 4]:
            self.processInput(PlotStructuralModeShapeInput, self.project, self.opv)      

    def plotDisplacementField(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0,1,5,6]:
            if solution is None:
                return
            plot = self.processInput(PlotDisplacementFieldInput, self.project, self.opv)
            if plot.frequency is None:
                return
            self.opv.changeAndPlotAnalysis(plot.frequency)

    def plotAcousticModeShapes(self):
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if solution is None:
            return
        if self.analysis_ID in [2, 4]:
            self.processInput(PlotAcousticModeShapeInput, self.project, self.opv)           

    def plotAcousticPressureField(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3,5,6]:
            if solution is None:
                return
            self.processInput(PlotAcousticPressureFieldInput, self.project, self.opv)           

    def plotStructuralFrequencyResponse(self):
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            self.processInput(  PlotStructuralFrequencyResponseInput, self.project, self.opv, 
                                self.analysis_method_label, solution  )

    def plotAcousticFrequencyResponse(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            self.processInput(  PlotAcousticFrequencyResponseInput, self.project, self.opv, 
                                self.analysis_method_label, solution )

    def plot_TL_NR(self):
        if self.analysis_ID in [3,5,6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return
            self.processInput(  Plot_TL_NR_Input, self.project, self.opv, 
                                self.analysis_method_label, solution  )

    def plotPerforatedPlateConvergenceDataLog(self):
        if self.project.perforated_plate_dataLog:
            self.processInput( PlotPerforatedPlateConvergenceData, self.project.perforated_plate_dataLog )

    def plotStressField(self):
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = True
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            self.processInput(PlotStressFieldInput, self.project, self.opv)

    def plotStressFrequencyResponse(self):
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0,1,5,6]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            self.processInput(PlotStressFrequencyResponseInput, self.project, self.opv, self.analysis_method_label)

    def plotReactionsFrequencyResponse(self):
        if self.analysis_ID in [0,1,5,6]:
            self.processInput(PlotReactionsInput, self.project, self.opv, self.analysis_method_label)

    def animationSettings(self):
        self.processInput(AnimationSettingsInput, self.project, self.opv)

    def structural_model_info(self):
        self.processInput(StructuralModelInfoInput, self.project, self.opv)

    def acoustic_model_info(self):
        self.processInput(AcousticModelInfoInput, self.project, self.opv)

    def about_OpenPulse(self):
        self.processInput(AboutOpenPulseInput, self.project, self.opv)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = 'Please, you should create a new project or load an already existing one before start to set up the model.'
        message += "\n\nIt is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([title, message, window_title])