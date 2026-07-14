
import logging
from collections import defaultdict
from pathlib import Path

from pulse import TEMP_PROJECT_DIR
from pulse.editor import Pipeline
from pulse.interface import error_title, warning_title
from pulse.interface.file.project_file import ProjectFile
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model import AnalysisID
from pulse.model.after_run import AfterRun
from pulse.model.before_run import BeforeRun
from pulse.model.model import Model
from pulse.processing.acoustic_solver import AcousticSolver
from pulse.processing.structural_solver import StructuralSolver
from pulse.project.load_project import LoadProject
from pulse.model.data_classes.project_setup_data_classes import ProjectSetup

from time import perf_counter


class Project:
    def __init__(self):

        self.pipeline = Pipeline()
        self.model = Model(self)

        self.project_setup = ProjectSetup()

        # default animation settings
        self.frames = 40
        self.cycles = 0

        self._initialize()
        self.reset()

    def _initialize(self):
        self.structural_reactions = dict()
        self.natural_frequencies_acoustic = None
        self.natural_frequencies_structural = None
        self.complex_natural_frequencies_acoustic = None

        self.preferences = dict()
        self.color_scale_setup = dict()

    def reset(self, reset_all=False):

        # TODO: reimplement this
        if reset_all:
            self.model.preprocessor.reset_variables()
            #TODO: reset nodal, element and line properties

        self.preferences.clear()
        self.color_scale_setup.clear()

        self.perforated_plate_data_log = None
        self.none_project_action = False
        self.stress_stiffening_enabled = False

        self.name = None
        self.save_path = None
        self.thumbnail = None

        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""
        self.stresses_values_for_color_table = None

        self.reset_solvers()
        self.reset_solutions()

    def set_project_setup(self, project_setup: ProjectSetup):
        self.project_setup = project_setup
        self.model.set_project_setup(project_setup)

    def reset_solvers(self):
        self.acoustic_solver = None
        self.structural_solver = None

    def reset_solutions(self):
        self.structural_solution = None
        self.acoustic_solution = None

        self.natural_frequencies_acoustic = None
        self.natural_frequencies_structural = None
        self.complex_natural_frequencies_acoustic = None
        self.structural_reactions.clear()

        if self.acoustic_solver is not None:
            self.acoustic_solver.reset_variables()

        if self.structural_solver is not None:
            self.structural_solver.reset_variables()

        if not self.model.analysis_setup:
            return

        # self.create_solver()

    def reset_analysis_setup(self):
        self.model.reset_analysis_setup()

    @property
    def analysis_id(self):
        return self.model.analysis_id

    @property
    def analysis_type_label(self):
        return self.model.analysis_type_label

    @property
    def analysis_method(self):
        return self.model.analysis_method

    @property
    def number_of_modes(self):
        return self.model.number_of_modes

    @property
    def sigma_factor(self):
        return self.model.sigma_factor

    @property
    def global_damping(self):
        return self.model.global_damping

    def initialize_pulse_file_and_loader(self, dir_path: Path=TEMP_PROJECT_DIR):
        self.file = ProjectFile(self, dir_path)
        self.loader = LoadProject(self)

    def initial_load_project_actions(self):

        try:
            self.reset(reset_all = True)
            self.loader.load_analysis_results()

            if self.file.check_pipeline_data():
                self.model.process_geometry_and_mesh()
                return True

        except Exception as log_error:
            from traceback import print_exception
            print_exception(log_error)

            title = "Error while processing initial load project actions"
            message = str(log_error)
            PrintMessageInput([error_title, title, message])
        
        return False

    def load_project(self):

        logging.info("Loading project data [30%]")
        if self.loader.load_project_data():
            return

        logging.info("Processing geometry and mesh [50%]")
        self.initial_load_project_actions()

        logging.info("Loading mesh dependent properties [60%]")
        self.loader.load_mesh_dependent_properties()

        logging.info("Finalizing model data loading [75%]")
        # self.model.preprocessor.process_all_transformation_matrices()
        self.model.preprocessor.check_disconnected_lines()

    def reset_project(self, **kwargs):

        self.reset(reset_all = True)
        self.file.remove_element_properties_from_project_file()
        self.file.remove_nodal_properties_from_project_file()
        self.file.remove_results_data_from_project_file()
        self.file.write_imported_table_data_in_file()

        if self.file.check_pipeline_data():
            if self.loader.load_project_data():
                return

            self.model.process_geometry_and_mesh()
            self.loader.load_mesh_dependent_properties()

    def is_analysis_setup_complete(self):

        analysis_setup = self.file.read_analysis_setup_from_file()
        if not analysis_setup:
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if AnalysisID(analysis_id).is_modal():
            if "number_of_modes" not in analysis_setup.keys():
                return False

            if not isinstance(analysis_setup["number_of_modes"], int):
                return False

            if "sigma_factor" in analysis_setup.keys():
                if not isinstance(analysis_setup["sigma_factor"], int | float):
                    return False
            else:
                return False

            return True

        elif AnalysisID(analysis_id).is_harmonic():

            for f_type in ["f_min", "f_max", "f_step"]:    
                if f_type in analysis_setup.keys():
                    if not isinstance(analysis_setup[f_type], int | float):
                        return False
                else:
                    return False
                
            if self.analysis_method == "mode_superposition":

                if "number_of_modes" not in analysis_setup.keys():
                    return False

                if not isinstance(analysis_setup["number_of_modes"], int):
                    return False

                if "sigma_factor" in analysis_setup.keys():
                    if not isinstance(analysis_setup["sigma_factor"], int | float):
                        return False

            return True
        
        elif AnalysisID(analysis_id).is_static():
            return True

    def set_perforated_plate_convergence_data_log(self, data):
        self.perforated_plate_data_log = data

    def set_color_scale_setup(self, color_scale_setup):
        self.color_scale_setup = color_scale_setup

    def map_lines_neighboors(self):
        # line_to_points = self.model.properties.map_line_to_points()
        lines_neighboors = defaultdict(list)
        for line_id, data in self.model.properties.line_properties.items():
            for coords in self.model.properties.get_line_edges(line_id):
                if coords is None:
                    return

                node_id = self.model.preprocessor.get_node_id_by_coordinates(coords)
    
                for element_id in self.model.preprocessor.elements_connected_to_node.get(node_id, list()):

                    line_id = self.model.preprocessor.mesh.get_line_from_element(element_id)
                    _data = self.model.properties.line_properties[line_id]

                    if "corner_coords" in _data.keys():
                        lines_neighboors[line_id, "curve"].append(line_id)
                    else:
                        lines_neighboors[line_id, "line"].append(line_id)

    def is_there_a_valid_solution(self):

        analysis_setup = self.file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return

        solvers = [
            self.acoustic_solver,
            self.structural_solver,
            ]

        if not any(solvers):
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.STRUCTURAL_STATIC,
            ]:
            if self.structural_solver is None:
                return

            solution  = self.structural_solver.solution
            if solution is not None:
                return True

        elif analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.COUPLED_HARMONIC,
            ]:
            if self.acoustic_solver is None:
                return

            solution  = self.acoustic_solver.solution
            if solution is not None:
                return True

        return False

    def get_analysis_type_and_physical_domain(self):

        analysis_setup = self.file.read_analysis_setup_from_file()
        if not isinstance(analysis_setup, dict):
            return "", ""

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        if analysis_id == AnalysisID.NO_ANALYSIS:
            return "", ""

        if analysis_id in [AnalysisID.STRUCTURAL_HARMONIC, AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.COUPLED_HARMONIC]:
            analysis_type = "harmonic"

        elif analysis_id == AnalysisID.STRUCTURAL_STATIC:
            analysis_type = "static"

        else:
            analysis_type = "modal"

        if analysis_id in [AnalysisID.ACOUSTIC_HARMONIC, AnalysisID.ACOUSTIC_MODAL]:
            physical_domain = "acoustic"

        elif analysis_id == AnalysisID.COUPLED_HARMONIC:
            physical_domain = "coupled"

        else:
            physical_domain = "structural"

        return analysis_type, physical_domain

    def is_there_a_valid_analysis_setup(self, **kwargs):

        current_analysis_id = kwargs.get("current_analysis_id", None)

        analysis_setup = self.file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)
        if analysis_id == AnalysisID.NO_ANALYSIS:
            return False

        if isinstance(current_analysis_id, int):
            if analysis_id != current_analysis_id:
                return False

        if analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC, 
            AnalysisID.STRUCTURAL_HARMONIC, 
            AnalysisID.COUPLED_HARMONIC
            ]:

            for key in ["f_min", "f_max", "f_step"]:
                if key not in analysis_setup.keys():
                    return False
            return True

        elif analysis_id in [
            AnalysisID.ACOUSTIC_MODAL, 
            AnalysisID.STRUCTURAL_MODAL
            ]:

            for key in ["number_of_modes", "sigma_factor"]:
                if key not in analysis_setup.keys():
                    return False
            return True
        
        elif analysis_id == AnalysisID.STRUCTURAL_STATIC:
            return True

        else:
            raise NotImplementedError("Not implemented analysis")

    def get_pre_solution_model_checks(self):
        return BeforeRun()

    def get_post_solution_model_checks(self):
        return AfterRun()

    def get_acoustic_solver(self) -> AcousticSolver:
        return AcousticSolver(self.model)

    def get_structural_solver(self) -> StructuralSolver:
        acoustic_solution = None
        if self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            acoustic_solution = self.acoustic_solution

        return StructuralSolver(self.model, acoustic_solution=acoustic_solution)

    def get_structural_solution(self):
        return self.structural_solution

    def get_acoustic_solution(self):
        return self.acoustic_solution

    def get_structural_reactions(self):
        return self.structural_reactions

    def set_stresses_values_for_color_table(self, values):
        self.stresses_values_for_color_table = values
    
    def set_min_max_type_stresses(self, min_stress, max_stress, stress_label):
        self.min_stress = min_stress
        self.max_stress = max_stress
        self.stress_label = stress_label

    def is_the_solution_finished(self):

        if self.acoustic_solution is not None:
            return True

        elif self.structural_solution is not None:
            return True

        return False

    def initialize_solver(self):

        if self.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.COUPLED_HARMONIC,
            ]:

            if self.model.frequencies is None:
                return

            if len(self.model.frequencies) == 0:
                return

        if self.model.preprocessor._process_beam_nodes_and_indexes():
            if self.analysis_id not in [
                AnalysisID.STRUCTURAL_MODAL,
                AnalysisID.STRUCTURAL_HARMONIC,
                AnalysisID.STRUCTURAL_STATIC,
                ]:

                title = "Invalid analysis type"
                message = "There are only BEAM_1 elements in the model, therefore, "
                message += "only structural analysis will be allowable."
                info_text = [warning_title, title, message]
                PrintMessageInput(info_text)
                return

        if self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.model.preprocessor.enable_fluid_mass_adding_effect(enable=False)
            self.structural_solver = self.get_structural_solver()

        elif self.analysis_id in [
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.ACOUSTIC_HARMONIC,
            ]:
            self.acoustic_solver = self.get_acoustic_solver()

        elif self.analysis_id in [AnalysisID.COUPLED_HARMONIC]:
            self.model.preprocessor.enable_fluid_mass_adding_effect(enable=True)
            self.acoustic_solver = self.get_acoustic_solver()

        elif self.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.STRUCTURAL_STATIC,
            ]:
            self.model.preprocessor.enable_fluid_mass_adding_effect(enable=False)
            self.structural_solver = self.get_structural_solver()

    def process_analysis(self):

        if not self.model.analysis_setup:
            return

        if self.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            if self.analysis_method == "direct":
                self.structural_solver.direct_method()
            else:
                self.structural_solver.mode_superposition()

            self.structural_solution = self.structural_solver.solution

        elif self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            self.acoustic_solver.direct_method()
            self.acoustic_solution = self.acoustic_solver.solution
            self.perforated_plate_data_log = self.acoustic_solver.convergence_data_log

        elif self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            self.acoustic_solver.direct_method()
            self.acoustic_solution = self.acoustic_solver.solution
            self.perforated_plate_data_log = self.acoustic_solver.convergence_data_log

            self.structural_solver = self.get_structural_solver()
            if self.analysis_method == "direct":
                self.structural_solver.direct_method()
            else:
                self.structural_solver.mode_superposition()

            self.structural_solution = self.structural_solver.solution

        elif self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.structural_solver.modal_analysis(number_of_modes = self.number_of_modes, sigma_factor = self.sigma_factor)
            self.natural_frequencies_structural = self.structural_solver.natural_frequencies
            self.structural_solution = self.structural_solver.modal_shapes

        elif self.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            self.acoustic_solver.modal_analysis(number_of_modes = self.number_of_modes, sigma_factor = self.sigma_factor)
            self.natural_frequencies_acoustic = self.acoustic_solver.natural_frequencies
            self.complex_natural_frequencies_acoustic = self.acoustic_solver.complex_natural_frequencies
            self.acoustic_solution = self.acoustic_solver.modal_shapes

        elif self.analysis_id == AnalysisID.STRUCTURAL_STATIC:
            self.structural_solver.static_analysis()
            self.structural_solution = self.structural_solver.solution

        else:
            raise NotImplementedError("Not implemented analysis")

        if isinstance(self.acoustic_solver, AcousticSolver):
            if self.analysis_id in [
                AnalysisID.ACOUSTIC_HARMONIC, 
                AnalysisID.COUPLED_HARMONIC,
                ]:

                from time import sleep
                if self.acoustic_solver.nl_pp_elements:
                    sleep(1)

    def run_analysis(self, running_by_script: bool = False):
        if LoadingWindow(self.build_model_and_solve).run(running_by_script = running_by_script):
            return True

        if running_by_script:
            return

        logging.info("Post-processing the obtained results [90%]")
        self.check_warnings()

        logging.info("Processing the post solution checks [95%]")
        self.post_solution_actions()

    def build_model_and_solve(self, running_by_script: bool = False):

        t0 = perf_counter()

        setup_complete = self.is_analysis_setup_complete()

        if not setup_complete:
            title = "Incomplete analysis setup" 
            message = "Please, it is necessary to choose an analysis type "
            message += "and setup it before trying to solve the model."
            PrintMessageInput([error_title, title, message])
            return True

        if not running_by_script:
            self.before_run = self.get_pre_solution_model_checks()
            if self.before_run.check_is_there_a_problem(self.analysis_id):
                return True

        logging.info("Processing the cross-sections [10%]")
        if self.model.preprocessor.process_cross_sections_mapping():
            self.model.preprocessor.stop_processing = False
            return True
        
        logging.info("Initializing the problem solver [30%]")
        self.initialize_solver()

        logging.info("Solution in progress [50%]")
        self.process_analysis()

        logging.info("Saving the solution data [95%]")
        self.file.write_results_data_in_file()

        if self.model.preprocessor.stop_processing:
            self.reset_solutions()
            self.model.preprocessor.stop_processing = False
            return

        dt = perf_counter() - t0
        print(f"Time to solve the model: {dt} [s]")

    def check_warnings(self):

        message = ""
        if self.analysis_id in [AnalysisID.STRUCTURAL_HARMONIC]:
            if self.structural_solver.warning_mode_sup_prescribed_dofs != "":
                message = self.structural_solver.warning_mode_sup_prescribed_dofs
            if self.structural_solver.flag_Clump and self.analysis_id==1:
                message = self.structural_solver.warning_Clump

        elif self.analysis_id in [AnalysisID.STRUCTURAL_MODAL]:
            if self.structural_solver.warning_modal_prescribed_dofs != "":
                message = self.structural_solver.warning_modal_prescribed_dofs

        elif self.analysis_id in [AnalysisID.ACOUSTIC_HARMONIC]:
            if self.acoustic_solver.warning_modal_prescribed_pressures != "":
                message = self.acoustic_solver.warning_modal_prescribed_pressures

        if message != "":
            title = self.analysis_type_label
            PrintMessageInput([warning_title, title, message])

    def calculate_structural_reactions(self):

        if self.structural_solution is None:
            return

        static_analysis = self.analysis_id == AnalysisID.STRUCTURAL_STATIC

        logging.info("Evaluating the structural reactions for constrained dofs [60%]")
        self.structural_solver.get_reactions_at_constrained_dofs(static_analysis=static_analysis)

        logging.info("Evaluating the structural reactions for lumped elements [80%]")
        self.structural_solver.get_reactions_at_springs_and_dampers(static_analysis=static_analysis)

        self.structural_reactions = {
            "reactions_at_constrained_dofs" : self.structural_solver.reactions_at_constrained_dofs,
            "reactions_at_springs" : self.structural_solver.reactions_at_springs,
            "reactions_at_dampers" : self.structural_solver.reactions_at_dampers,
            }

    def post_solution_actions(self):

        if self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            self.before_run.check_modal_analysis_imported_data()

        elif self.analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.COUPLED_HARMONIC,
            ]:
            self.before_run.check_all_acoustic_criteria()

        if self.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.COUPLED_HARMONIC,
            AnalysisID.STRUCTURAL_STATIC,
            ]:
            self.calculate_structural_reactions()

        self.after_run = self.get_post_solution_model_checks()
        self.after_run.check_all_acoustic_criterias()