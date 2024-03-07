#
from pulse.interface.user_input.project.get_started import GetStartedInput
from pulse.interface.user_input.project.new_project import NewProjectInput
from pulse.interface.user_input.project.load_project import LoadProjectInput
from pulse.interface.user_input.project.reset_project import ResetProjectInput
from pulse.interface.user_input.project.import_geometry import ImportGeometry
from pulse.interface.user_input.project.about_open_pulse import AboutOpenPulseInput
#
from pulse.interface.user_input.project.geometryDesignerInput import GeometryDesignerInput
from pulse.interface.user_input.project.editImportedGeometryInput import EditImportedGeometryInput
from pulse.interface.user_input.project.save_project_as_input import SaveProjectAsInput
from pulse.interface.user_input.project.set_geometry_file_input import SetGeometryFileInput
from pulse.interface.user_input.model.setup.general.set_material_input import SetMaterialInput
from pulse.interface.user_input.model.setup.general.fluid_input import FluidInput
from pulse.interface.user_input.model.setup.general.set_cross_section import SetCrossSectionInput
#
from pulse.interface.user_input.model.setup.structural.structuralElementTypeInput import StructuralElementTypeInput
from pulse.interface.user_input.model.setup.structural.dof_input import DOFInput
from pulse.interface.user_input.model.setup.structural.loadsInput import LoadsInput
from pulse.interface.user_input.model.setup.structural.massSpringDamperInput import MassSpringDamperInput
from pulse.interface.user_input.model.setup.structural.elasticNodalLinksInput import ElasticNodalLinksInput
from pulse.interface.user_input.model.setup.structural.set_inertial_load import SetInertialLoad
from pulse.interface.user_input.model.setup.structural.stressStiffeningInput import StressStiffeningInput
from pulse.interface.user_input.model.setup.structural.capped_end_input import CappedEndInput
from pulse.interface.user_input.model.setup.structural.set_valves_input import ValvesInput
from pulse.interface.user_input.model.setup.structural.flangesInput import FlangesInput
from pulse.interface.user_input.model.setup.structural.expansionJointInput import ExpansionJointInput
from pulse.interface.user_input.model.setup.structural.beamXaxisRotationInput import BeamXaxisRotationInput 
from pulse.interface.user_input.model.setup.structural.decouplingRotationDOFsInput import DecouplingRotationDOFsInput
#
from pulse.interface.user_input.model.setup.acoustic.acousticElementTypeInput import AcousticElementTypeInput
from pulse.interface.user_input.model.setup.general.set_fluid_composition_input import SetFluidCompositionInput
from pulse.interface.user_input.model.setup.acoustic.acoustic_pressure_input import AcousticPressureInput
from pulse.interface.user_input.model.setup.acoustic.volumevelocityInput import VolumeVelocityInput
from pulse.interface.user_input.model.setup.acoustic.specificimpedanceInput import SpecificImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.radiationImpedanceInput import RadiationImpedanceInput
from pulse.interface.user_input.model.setup.acoustic.element_length_correction_input import AcousticElementLengthCorrectionInput
from pulse.interface.user_input.model.setup.acoustic.perforatedPlateInput import PerforatedPlateInput
from pulse.interface.user_input.model.setup.acoustic.compressor_model_input import CompressorModelInput
from pulse.interface.user_input.model.criteria.check_pulsation_criteria import CheckAPI618PulsationCriteriaInput
#
from pulse.interface.user_input.analysis.general.analysis_type import AnalysisTypeInput
from pulse.interface.user_input.analysis.general.analysis_setup import AnalysisSetupInput
from pulse.interface.user_input.analysis.general.run_analysis import RunAnalysisInput
#
from pulse.interface.user_input.plots.structural.plot_structural_mode_shape import PlotStructuralModeShape
from pulse.interface.user_input.plots.structural.plot_nodal_results_field_for_harmonic_analysis import PlotNodalResultsFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.get_nodal_results_for_harmonic_analysis import GetNodalResultsForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.get_nodal_results_for_static_analysis import GetNodalResultsForStaticAnalysis
from pulse.interface.user_input.plots.structural.get_reactions_for_harmonic_analysis import GetReactionsForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.get_reactions_for_static_analysis import GetReactionsForStaticAnalysis
from pulse.interface.user_input.plots.structural.plot_stresses_field_for_harmonic_analysis import PlotStressesFieldForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.plot_stress_field_for_static_analysis import PlotStressesFieldForStaticAnalysis
from pulse.interface.user_input.plots.structural.get_stresses_for_harmonic_analysis import GetStressesForHarmonicAnalysis
from pulse.interface.user_input.plots.structural.get_stresses_for_static_analysis import GetStressesForStaticAnalysis
#
from pulse.interface.user_input.plots.acoustic.plot_acoustic_mode_shape import PlotAcousticModeShape
from pulse.interface.user_input.plots.acoustic.plot_acoustic_pressure_field import PlotAcousticPressureField
from pulse.interface.user_input.plots.acoustic.get_acoustic_frequency_response import GetAcousticFrequencyResponse
from pulse.interface.user_input.plots.acoustic.get_acoustic_frequency_response_function import GetAcousticFrequencyResponseFunction
from pulse.interface.user_input.plots.acoustic.plot_transmission_loss import PlotTransmissionLoss
from pulse.interface.user_input.plots.acoustic.get_acoustic_delta_pressure import GetAcousticDeltaPressure
from pulse.interface.user_input.plots.acoustic.plotPerforatedPlateConvergenceData import PlotPerforatedPlateConvergenceData
#
from pulse.interface.user_input.plots.structural.plot_cross_section_input import PlotCrossSectionInput
from pulse.interface.user_input.project.render.renderer_user_preferences import RendererUserPreferencesInput
from pulse.interface.user_input.model.info.structuralModel_InfoInput import StructuralModelInfoInput
from pulse.interface.user_input.model.info.acousticModel_InfoInput import AcousticModelInfoInput
from pulse.interface.user_input.model.criteria.check_beam_criteria_input import CheckBeamCriteriaInput
#
from pulse.interface.user_input.project.print_message import PrintMessageInput
#
from pulse.interface.user_input.render.clip_plane_widget import ClipPlaneWidget
#
from pulse import app

from time import time

window_title_1 = "Error"
window_title_2 = "Warning"

class InputUi:
    def __init__(self, parent=None):

        self.main_window = app().main_window
        self.project = app().main_window.project
        self.file = app().main_window.project.file
        self.opv = app().main_window.opv_widget
        self.menu_items = app().main_window.model_and_analysis_setup_widget.model_and_analysis_setup_items
        
        self._reset()

    def _reset(self):
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
            self.opv.setInputObject(read)
            return read
        except Exception as log_error:
            title = "Error detected in process Input method"
            message = str(log_error)
            PrintMessageInput([window_title_1, title, message])
            return None

    def new_project(self):
        self.reset_geometry_render()
        new_project = self.processInput(NewProjectInput)
        if new_project.complete:
            self.main_window._update_status_bar()
            return self.initial_project_action(new_project.complete)

    def load_project(self, path=None):
        self.reset_geometry_render()
        load_project = self.processInput(LoadProjectInput, path=path)
        self.main_window.mesh_toolbar.update_mesh_attributes()
        self.main_window._update_status_bar()
        return self.initial_project_action(load_project.complete)

    def get_started(self):
        self.menu_items.modify_model_setup_items_access(True)
        get_started = self.processInput(GetStartedInput)
        self.main_window._update_status_bar()
        return get_started

    def initial_project_action(self, finalized):
        self.main_window.action_front_view_callback()
        self.main_window.update_export_geometry_file_access()
        self.menu_items.modify_model_setup_items_access(True)
        if finalized:
            if self.project.file.check_if_entity_file_is_active():
                self.project.none_project_action = False
                self.menu_items.modify_model_setup_items_access(False)
                return True
            else:
                self.menu_items.modify_geometry_item_access(False)
                return True
        else:
            self.project.none_project_action = True
            return False

    def reset_geometry_render(self):
        editor = app().geometry_toolbox.editor
        editor.reset()

    def reset_project(self):
        if not self.project.none_project_action:
            self.processInput(ResetProjectInput)

    def import_geometry(self):
        obj = self.processInput(ImportGeometry)
        return self.initial_project_action(obj.complete)

    def set_clipping_plane(self):
        if not self.opv.opvAnalysisRenderer.getInUse():
            return

        clipping_plane = self.processInput(ClipPlaneWidget, self.opv)        
        clipping_plane.value_changed.connect(self.opv.configure_clipping_plane)
        clipping_plane.slider_released.connect(self.opv.apply_clipping_plane)
        clipping_plane.exec()
        self.opv.dismiss_clipping_plane()
            
    def save_project_as(self):
        self.processInput(SaveProjectAsInput)

    def set_geometry_file(self):
        self.processInput(SetGeometryFileInput, self.project, self.opv)

    def call_geometry_designer(self):
        read = self.processInput(GeometryDesignerInput, self.project, self.opv)
        return read.complete

    def call_geometry_editor(self):
        main_window = self.main_window
        main_window.use_geometry_workspace()
        # self.processInput(CreateEditStructuresWidget, self.opv)
        # self.processInput(OPPGeometryDesignerInput, self.project, self.opv)
        # self.initial_project_action(True)

    def edit_an_imported_geometry(self):
        self.opv.Disable()
        read = self.processInput(EditImportedGeometryInput, self.project)
        self.opv.Enable()
        if read.complete:
            self.opv.updatePlots()
            self.opv.plot_entities()
        return read.complete
    
    def get_opv(self):
        return self.opv

    def set_material(self):
        self.processInput(SetMaterialInput, self.project, self.opv)   
         
    def set_cross_section(self, pipe_to_beam=False, beam_to_pipe=False, lines_to_update_cross_section=[]):
        read = self.processInput(   SetCrossSectionInput,
                                    pipe_to_beam = pipe_to_beam, 
                                    beam_to_pipe = beam_to_pipe, 
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
        
    def set_dof(self):
        self.processInput(DOFInput)
        
    def setRotationDecoupling(self):
        self.processInput(DecouplingRotationDOFsInput, self.project, self.opv)
        
    def setNodalLoads(self):
        self.processInput(LoadsInput, self.project, self.opv)
        
    def addMassSpringDamper(self):
        self.processInput(MassSpringDamperInput, self.project, self.opv)

    def set_capped_end(self):
        self.processInput(CappedEndInput)

    def set_stress_stress_stiffening(self):
        self.processInput(StressStiffeningInput, self.project, self.opv)

    def add_elastic_nodal_links(self):
        self.processInput(ElasticNodalLinksInput, self.project, self.opv)

    def set_inertial_load(self):
        return self.processInput(SetInertialLoad)
    
    def add_expansion_joint(self):
        self.processInput(ExpansionJointInput, self.project, self.opv)

    def add_valve(self):
        return self.processInput(ValvesInput)

    def set_acoustic_element_type(self):
        self.processInput(AcousticElementTypeInput, self.project, self.opv)

    def set_fluid(self):
        self.processInput(FluidInput, self.project, self.opv)

    def set_fluid_composition(self):
        self.processInput(SetFluidCompositionInput, self.project, self.opv)

    def set_acoustic_pressure(self):
        self.processInput(AcousticPressureInput)
    
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

    def analysisTypeInput(self):

        read = self.processInput(AnalysisTypeInput)

        if not read.complete:
            return

        if read.method_ID == -1:
            return

        self.analysis_ID = self.project.analysis_ID
        self.analysis_type_label = self.project.analysis_type_label
        self.analysis_method_label = self.project.analysis_method_label

        if self.analysis_ID is None:
            self.analysis_ID = None
            return
        
        if self.analysis_ID in [0, 1, 3, 5, 6, 7]:
            self.project.set_structural_solution(None)
            self.project.set_acoustic_solution(None)

        if self.analysis_ID in [2, 4, 7]:
            self.project.update_project_analysis_setup_state(True)
            self.run_analysis()
        else:
            self.analysis_setup()
                    
    def analysis_setup(self):

        if self.project.analysis_ID in [None, 2, 4]:
            return False
        if self.project.file._project_name == "":
            return False
        
        read = self.processInput(AnalysisSetupInput)
        
        if read.complete:
            if read.flag_run:
                self.run_analysis()
            return True   
        else:
            return False
       
    def run_analysis(self):

        # t0 = time()
        if self.analysis_ID is None or not self.project.setup_analysis_complete:
            
            title = "INCOMPLETE SETUP ANALYSIS" 
            message = "Please, it is necessary to choose an analysis type and "
            message += "setup it before trying to solve the model."
            PrintMessageInput([window_title_1, title, message])
            return

        self.before_run = self.project.get_pre_solution_model_checks()
        if self.before_run.check_is_there_a_problem(self.analysis_ID):
            return
        # self.project.time_to_checking_entries = time()-t0

        read = self.processInput(RunAnalysisInput)
        if read.complete:
            if self.analysis_ID == 2:
                self.before_run.check_modal_analysis_imported_data()
            elif self.analysis_ID in [3, 5, 6]:
                self.before_run.check_all_acoustic_criteria()

            self.after_run = self.project.get_post_solution_model_checks()
            self.after_run.check_all_acoustic_criterias()
            self.main_window.use_results_workspace()
        
    def plot_structural_mode_shapes(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [2, 4]:
            if solution is None:
                return None
            else:
                return self.processInput(PlotStructuralModeShape)      

    def plot_displacement_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = False
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            if solution is None:
                return None
            else:
                return self.processInput(PlotNodalResultsFieldForHarmonicAnalysis)

    def plot_structural_frequency_response(self):
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return None
            elif self.analysis_ID == 7:
                return self.processInput(GetNodalResultsForStaticAnalysis)
            else:
                return self.processInput(GetNodalResultsForHarmonicAnalysis)

    def plot_reaction_frequency_response(self):
        if self.analysis_ID in [0, 1, 5, 6]:
            return self.processInput(GetReactionsForHarmonicAnalysis)
        elif self.analysis_ID == 7:
            return self.processInput(GetReactionsForStaticAnalysis)  

    def plot_stress_field(self):
        self.project.plot_pressure_field = False
        self.project.plot_stress_field = True
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            solution = self.project.get_structural_solution()
            if solution is None:
                return
            elif self.analysis_ID == 7:
                return self.processInput(PlotStressesFieldForStaticAnalysis)
            else:
                return self.processInput(PlotStressesFieldForHarmonicAnalysis)

    def plot_stress_frequency_response(self):
        solution = self.project.get_structural_solution()
        if self.analysis_ID in [0, 1, 5, 6, 7]:
            if solution is None:
                return
            elif self.analysis_ID == 7:
                return self.processInput(GetStressesForStaticAnalysis)
            else:
                return self.processInput(GetStressesForHarmonicAnalysis)     

    def plot_acoustic_mode_shapes(self):
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [2, 4]:
            if solution is None:
                return None
            else:
                return self.processInput(PlotAcousticModeShape)           

    def plot_acoustic_pressure_field(self):
        self.project.set_min_max_type_stresses("", "", "")
        self.project.plot_pressure_field = True
        self.project.plot_stress_field = False
        solution = self.project.get_acoustic_solution()
        if self.analysis_ID in [3, 5, 6]:
            if solution is None:
                return None
            else:
                return self.processInput(PlotAcousticPressureField)

    def plot_acoustic_frequency_response(self):
        if self.analysis_ID in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.processInput(GetAcousticFrequencyResponse)

    def plot_acoustic_frequency_response_function(self):
        if self.analysis_ID in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.processInput(GetAcousticFrequencyResponseFunction)

    def plot_acoustic_delta_pressures(self):
        if self.analysis_ID in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.processInput(GetAcousticDeltaPressure)

    def plot_transmission_loss(self):
        if self.analysis_ID in [3, 5, 6]:
            solution = self.project.get_acoustic_solution()
            if solution is None:
                return None
            else:
                return self.processInput(PlotTransmissionLoss)

    def plot_perforated_plate_convergence_data(self):
        if self.project.perforated_plate_data_log:
            self.processInput(PlotPerforatedPlateConvergenceData)
    
    def check_api618_pulsation_criteria(self):
        return self.processInput(CheckAPI618PulsationCriteriaInput)

    def structural_model_info(self):
        self.processInput(StructuralModelInfoInput, self.project, self.opv)

    def acoustic_model_info(self):
        self.processInput(AcousticModelInfoInput, self.project, self.opv)

    def check_beam_criteria(self):
        self.processInput(CheckBeamCriteriaInput, self.project, self.opv)

    def about_OpenPulse(self):
        self.processInput(AboutOpenPulseInput)

    def empty_project_action_message(self):
        title = 'EMPTY PROJECT'
        message = "Please, you should create a new project or load an already existing one before start to set up the model. "
        message += "It is recommended to use the 'New Project' or the 'Import Project' buttons to continue."
        window_title = 'ERROR'
        PrintMessageInput([window_title, title, message])