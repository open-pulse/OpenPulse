# fmt: off

import logging
from collections import defaultdict
from pathlib import Path

import numpy as np

from pulse import TEMP_PROJECT_DIR, app
from pulse.editor import Pipeline
from pulse.interface.file.project_file import ProjectFile
from pulse.interface.user_input.project.loading_window import LoadingWindow
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model import AnalysisID
from pulse.model.after_run import AfterRun
from pulse.model.before_run import BeforeRun
from pulse.model.model import Model
from pulse.processing.assemblers.acoustic_assembler import AcousticAssembler
from pulse.processing.assemblers.structural_assembler import StructuralAssembler
from pulse.processing.solvers.harmonic_solver import HarmonicSolver
from pulse.processing.solvers.modal_solver import ModalSolver
from pulse.processing.solvers.static_solver import StaticSolver
from pulse.postprocessing.structural_post_processor import StructuralPostProcessor
from pulse.postprocessing.acoustic_post_processor import AcousticPostProcessor
from pulse.project.load_project import LoadProject

error_title = "Error"
warning_title = "Warning"

class Project:
    def __init__(self):

        self.pipeline = Pipeline()
        self.model = Model(self)

        self.name = None
        self.save_path = None
        self.thumbnail = None

        # default animation settings
        self.frames = 40
        self.cycles = 3

        self._initialize()
        self.reset()

    def _initialize(self):
        self.structural_reactions = dict()

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

        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""
        self.stresses_values_for_color_table = None

        self.reset_solvers()

    def reset_solvers(self):
        self.acoustic_assembler: AcousticAssembler | None = None
        self.structural_assembler: StructuralAssembler | None = None
        self.structural_solver = None
        self.acoustic_solver = None
        self.structural_post_processor = StructuralPostProcessor(self)
        self.acoustic_post_processor = AcousticPostProcessor(self)
        self.structural_reactions.clear()
        # Warnings generated during the solution
        self._warning_mode_sup_prescribed_dofs = ""
        self._warning_modal_prescribed_dofs = ""
        self._warning_modal_prescribed_pressures = ""
        self._warning_clump = ""
        self._flag_clump = False
    
    @property
    def structural_solution(self):
        if self.structural_solver is None:
            return None
        return self.structural_solver.solution

    @property
    def acoustic_solution(self):
        if self.acoustic_solver is None:
            return None
        return self.acoustic_solver.solution

    @property
    def natural_frequencies_structural(self):
        if self.structural_solver is None:
            return None
        return getattr(self.structural_solver, "natural_frequencies", None)

    @property
    def natural_frequencies_acoustic(self):
        if self.acoustic_solver is None:
            return None
        return getattr(self.acoustic_solver, "natural_frequencies", None)

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
                self.process_geometry_and_mesh()
                return True
            else:
                return False

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
        self.model.preprocessor.process_all_rotation_matrices()
        self.model.preprocessor.check_disconnected_lines()

    def reset_project(self, **kwargs):

        self.reset(reset_all = True)
        self.file.remove_element_properties_from_project_file()
        self.file.remove_nodal_properties_from_project_file()

        if self.file.check_pipeline_data():
            if self.loader.load_project_data():
                return

            self.process_geometry_and_mesh()
            self.loader.load_mesh_dependent_properties()

    def process_geometry_and_mesh(self):
        # t0 = time()
        self.model.preprocessor.generate()
        if app() is None:
            return

        app().main_window.update_status_bar_info()
        # dt = time()-t0
        # print(f"Time to process_geometry_and_mesh: {dt} [s]")

    def enhance_pipe_sections_appearance(self):
        """ 
        This method adds lids to cross-section variations and terminations.
        """
        for elements in self.model.preprocessor.structural_elements_connected_to_node.values():

            element = None
            if len(elements) == 2:
                first_element, last_element = elements
                
                if 'beam_1' not in [first_element.element_type, last_element.element_type]:
                    first_cross = first_element.cross_section
                    last_cross = last_element.cross_section
                    
                    if not (first_cross and last_cross):
                        continue

                    first_outer_diameter = first_cross.outer_diameter
                    first_inner_diameter = first_cross.inner_diameter
                    last_outer_diameter = last_cross.outer_diameter
                    last_inner_diameter = last_cross.inner_diameter

                    if first_outer_diameter < last_inner_diameter:
                        inner_diameter = first_inner_diameter 
                        element = last_element

                    if last_outer_diameter < first_inner_diameter:
                        inner_diameter = last_inner_diameter 
                        element = first_element

            elif len(elements) == 1: 

                element = elements[0]   
                if element.element_type == 'beam_1':
                    continue  

                first_node = element.first_node
                last_node = element.last_node  

                if element.cross_section is None:
                    continue

                inner_diameter = element.cross_section.inner_diameter 

                if len(self.model.preprocessor.neighbors[first_node]) == 1:
                    first_node_id = first_node.external_index
                    if self.is_there_an_acoustic_attribute_in_the_node(first_node_id) == 0:
                        inner_diameter = 0

                elif len(self.model.preprocessor.neighbors[last_node]) == 1:
                    last_node_id = last_node.external_index
                    if self.is_there_an_acoustic_attribute_in_the_node(last_node_id) == 0:
                        inner_diameter = 0

            if element:

                if element.element_type == 'expansion_joint':

                    d_eff = element.cross_section.section_parameters[1]
                    plot_key = element.cross_section.section_parameters[0]

                    # thickness = (outer_diameter - inner_diameter) / 2
                    parameters = [plot_key, d_eff, inner_diameter]

                    element.section_parameters_render = parameters

                else:

                    cross = element.cross_section
                    outer_diameter = cross.outer_diameter
                    offset_y = cross.offset_y
                    offset_z = cross.offset_z
                    insulation_thickness = cross.insulation_thickness

                    thickness = (outer_diameter - inner_diameter) / 2
                    parameters = [  
                                    outer_diameter, 
                                    thickness, 
                                    offset_y, 
                                    offset_z, 
                                    insulation_thickness
                                  ]

                    element.section_parameters_render = parameters

    def is_there_an_acoustic_attribute_in_the_node(self, node_id: int):

        acoustic_properties = [
                                "acoustic_pressure", 
                                "volume_velocity", 
                                "specific_impedance", 
                                "radiation_impedance", 
                                "reciprocating_compressor_excitation",
                                "reciprocating_pump_excitation",
                                "psd_acoustic_link",
                                "acoustic_transfer_element"
                                ]

        for (property, *args) in self.model.properties.nodal_properties.keys():
            if property in acoustic_properties and node_id in args:
                    return True

        return False

    def is_analysis_setup_complete(self):

        analysis_setup = self.file.read_analysis_setup_from_file()

        if isinstance(analysis_setup, dict):
            analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

            if analysis_id in [
                AnalysisID.STRUCTURAL_MODAL,
                AnalysisID.ACOUSTIC_MODAL,
            ]:
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

            elif analysis_id in [
                AnalysisID.STRUCTURAL_HARMONIC,
                AnalysisID.ACOUSTIC_HARMONIC,
                AnalysisID.COUPLED_HARMONIC,
                ]:

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
            
            elif analysis_id == AnalysisID.STRUCTURAL_STATIC:
                return True

        return False

    def get_structural_elements(self):
        return self.model.preprocessor.structural_elements
    
    def get_structural_element(self, element_id):
        return self.model.preprocessor.structural_elements[element_id]

    def get_acoustic_elements(self):
        return self.model.preprocessor.acoustic_elements 

    def get_acoustic_element(self, element_id):
        return self.model.preprocessor.acoustic_elements[element_id]

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
                neigh_elements = self.model.preprocessor.structural_elements_connected_to_node[node_id]
    
                for element in neigh_elements:

                    element_line = self.model.preprocessor.mesh.line_from_element[element.index]
                    _data = self.model.properties.line_properties[element_line]

                    if "corner_coords" in _data.keys():
                        lines_neighboors[line_id, "curve"].append(element_line)
                    else:
                        lines_neighboors[line_id, "line"].append(element_line)

    def get_geometry_points(self):
        points = dict()
        for i in self.model.preprocessor.mesh.geometry_points:
            points[i] = self.model.preprocessor.nodes[i]
        return points

    def is_there_a_valid_solution(self):

        analysis_setup = self.file.read_analysis_setup_from_file()
        if analysis_setup is None:
            return

        if self.acoustic_assembler is None and self.structural_assembler is None:
            return False

        analysis_id = analysis_setup.get("analysis_id", AnalysisID.NO_ANALYSIS)

        if analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.STRUCTURAL_MODAL,
            AnalysisID.STRUCTURAL_STATIC,
            ]:
            if self.structural_assembler is None:
                return
            if self.structural_solution is not None:
                return True

        elif analysis_id in [
            AnalysisID.ACOUSTIC_HARMONIC,
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.COUPLED_HARMONIC,
            ]:
            if self.acoustic_assembler is None:
                return
            if self.acoustic_solution is not None:
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

    def _get_acoustic_assembler(self) -> AcousticAssembler:
        return AcousticAssembler(self.model)

    def _get_structural_assembler(
        self, acoustic_solution=None
    ) -> StructuralAssembler:
        return StructuralAssembler(self.model, acoustic_solution=acoustic_solution)

    def get_structural_solution(self):
        if self.structural_solver is None:
            return None

        return self.structural_solver.solution

    def get_acoustic_solution(self):
        if self.acoustic_solver is None:
            return None

        return self.acoustic_solver.solution

    def get_structural_reactions(self):
        return self.structural_reactions

    def set_stresses_values_for_color_table(self, values):
        self.stresses_values_for_color_table = values
    
    def set_min_max_type_stresses(self, min_stress, max_stress, stress_label):
        self.min_stress = min_stress
        self.max_stress = max_stress
        self.stress_label = stress_label

    def is_the_solution_finished(self):
        return self.acoustic_solver is not None or self.structural_solver is not None

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
            self.model.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.structural_assembler = self._get_structural_assembler()

        elif self.analysis_id in [
            AnalysisID.ACOUSTIC_MODAL,
            AnalysisID.ACOUSTIC_HARMONIC,
            ]:
            self.acoustic_assembler = self._get_acoustic_assembler()

        elif self.analysis_id in [AnalysisID.COUPLED_HARMONIC]:
            self.model.preprocessor.enable_fluid_mass_adding_effect()
            self.acoustic_assembler = self._get_acoustic_assembler()

        elif self.analysis_id in [
            AnalysisID.STRUCTURAL_HARMONIC,
            AnalysisID.STRUCTURAL_STATIC,
            ]:
            self.model.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.structural_assembler = self._get_structural_assembler()

    def process_analysis(self):

        if not self.model.analysis_setup:
            return

        freqs = self.model.frequencies

        if self.analysis_id == AnalysisID.STRUCTURAL_HARMONIC:
            assembler = self.structural_assembler
            self._apply_stress_stiffening_if_needed(assembler)
            solver = HarmonicSolver(assembler)
            if self.analysis_method == "direct":
                solver.direct_method(freqs)
            else:
                self._run_mode_superposition(solver, freqs)
            self.structural_solver = solver

        elif self.analysis_id == AnalysisID.ACOUSTIC_HARMONIC:
            solver = HarmonicSolver(self.acoustic_assembler)
            self._run_acoustic_harmonic(solver, freqs)
            self.perforated_plate_data_log = solver.assembler.convergence_data_log
            self.acoustic_solver = solver

        elif self.analysis_id == AnalysisID.COUPLED_HARMONIC:
            # 1. Solve acoustic
            acoustic_solver = HarmonicSolver(self.acoustic_assembler)
            self._run_acoustic_harmonic(acoustic_solver, freqs)
            self.perforated_plate_data_log = acoustic_solver.assembler.convergence_data_log
            self.acoustic_solver = acoustic_solver

            # 2. Solve structural with coupled acoustic solution
            struct_assembler = self._get_structural_assembler(
                acoustic_solution=acoustic_solver.solution
            )
            self.structural_assembler = struct_assembler
            self._apply_stress_stiffening_if_needed(struct_assembler)
            struct_solver = HarmonicSolver(struct_assembler)
            if self.analysis_method == "direct":
                struct_solver.direct_method(freqs)
            else:
                self._run_mode_superposition(struct_solver, freqs)
            self.structural_solver = struct_solver

        elif self.analysis_id == AnalysisID.STRUCTURAL_MODAL:
            assembler = self.structural_assembler
            self._apply_stress_stiffening_if_needed(assembler)
            solver = ModalSolver(assembler)
            solver.solve(n_modes=self.number_of_modes, sigma=self.sigma_factor)
            self._check_modal_prescribed_dofs_warning(assembler)
            self.structural_solver = solver

        elif self.analysis_id == AnalysisID.ACOUSTIC_MODAL:
            assembler = self.acoustic_assembler
            solver = ModalSolver(assembler)
            solver.solve(n_modes=self.number_of_modes, sigma=self.sigma_factor)
            self._check_acoustic_modal_prescribed_warning(assembler)
            self.acoustic_solver = solver

        elif self.analysis_id == AnalysisID.STRUCTURAL_STATIC:
            solver = StaticSolver(self.structural_assembler)
            solver.solve()
            self.structural_solver = solver

        else:
            raise NotImplementedError("Not implemented analysis")

        # Brief pause after nonlinear PP acoustic analysis to allow UI update
        if self.acoustic_assembler is not None:
            if self.analysis_id in [
                AnalysisID.ACOUSTIC_HARMONIC,
                AnalysisID.COUPLED_HARMONIC,
            ]:
                from time import sleep
                if self.acoustic_assembler.nl_elements:
                    sleep(1)

    # ── Auxiliares de process_analysis ───────────────────────────────────

    def _run_acoustic_harmonic(
        self, solver: HarmonicSolver, freqs
    ) -> None:
        """Run the acoustic harmonic analysis (linear or nonlinear) on solver."""
        assembler = solver.assembler
        if assembler.nl_elements:
            assembler.reset_nl_elements()
            solver.nonlinear_direct_method(freqs)
        else:
            solver.direct_method(freqs)

    def _apply_stress_stiffening_if_needed(
        self, assembler: StructuralAssembler
    ) -> None:
        """Apply stress stiffening to the assembler if enabled in the model."""
        if self.model.preprocessor.stress_stiffening_enabled:
            static_solver = StaticSolver(assembler)
            static_solver.solve()
            assembler.apply_stress_stiffening(static_solver.solution)

    def _run_mode_superposition(
        self, solver: HarmonicSolver, freqs
    ) -> None:
        """Run mode superposition or fall back to direct if conditions are not met."""
        assembler = solver.assembler
        if not assembler.has_no_table():
            solver.direct_method(freqs)
            return

        if np.sum(assembler._prescribed_values) > 0:
            self._warning_mode_sup_prescribed_dofs = (
                "The Harmonic Analysis of prescribed DOF problems "
                "had been solved through the Direct Method."
            )
            solver.direct_method(freqs)
            return

        self._flag_clump = assembler.flag_Clump
        if assembler.flag_Clump:
            self._warning_clump = (
                "There are external dampers connecting nodes to the ground. "
                "The damping, treated as a viscous non-proportional model, will be "
                "ignored in mode superposition. It's recommended to solve the harmonic "
                "analysis through direct method if you want to get more accurate results!"
            )

        solver.mode_superposition(freqs, n_modes=self.number_of_modes)

    def _check_modal_prescribed_dofs_warning(
        self, assembler: StructuralAssembler
    ) -> None:
        for value in assembler._prescribed_values:
            if value is not None:
                if (
                    (isinstance(value, complex) and value != complex(0))
                    or (isinstance(value, np.ndarray) and sum(value) != complex(0))
                ):
                    self._warning_modal_prescribed_dofs = (
                        "The Prescribed DOFs of non-zero values have been ignored "
                        "in the modal analysis. The null value has been attributed "
                        "to those DOFs with non-zero values."
                    )
                    break

    def _check_acoustic_modal_prescribed_warning(
        self, assembler: AcousticAssembler
    ) -> None:
        for value in assembler._prescribed_values:
            if value is not None:
                if (
                    (isinstance(value, complex) and value != complex(0))
                    or (isinstance(value, np.ndarray) and sum(value) != complex(0))
                ):
                    self._warning_modal_prescribed_pressures = (
                        "The Prescribed Pressure values have been ignored in the "
                        "modal analysis. The null value has been attributed to those DOFs."
                    )
                    break

    def run_analysis(self):
        return LoadingWindow(self.build_model_and_solve).run()

    def build_model_and_solve(self, running_by_script=False):

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
            self.reset_solvers()
            self.model.preprocessor.stop_processing = False
            return

        if not running_by_script:

            logging.info("Post-processing the obtained results [90%]")
            self.check_warnings()

            logging.info("Processing the post solution checks [95%]")
            self.post_solution_actions()

    def check_warnings(self):

        message = ""
        if self.analysis_id in [AnalysisID.STRUCTURAL_HARMONIC]:
            if self._warning_mode_sup_prescribed_dofs:
                message = self._warning_mode_sup_prescribed_dofs
            if self._flag_clump and self.analysis_id == 1:
                message = self._warning_clump

        elif self.analysis_id in [AnalysisID.STRUCTURAL_MODAL]:
            if self._warning_modal_prescribed_dofs:
                message = self._warning_modal_prescribed_dofs

        elif self.analysis_id in [AnalysisID.ACOUSTIC_HARMONIC]:
            if self._warning_modal_prescribed_pressures:
                message = self._warning_modal_prescribed_pressures

        if message:
            title = self.analysis_type_label
            PrintMessageInput([warning_title, title, message])

    def calculate_structural_reactions(self):

        if self.structural_solver is None:
            return

        static_analysis = self.analysis_id == AnalysisID.STRUCTURAL_STATIC

        post = self.structural_post_processor

        logging.info("Evaluating the structural reactions for constrained dofs [60%]")
        post.get_reactions_at_constrained_dofs(static_analysis=static_analysis)

        logging.info("Evaluating the structural reactions for lumped elements [80%]")
        post.get_reactions_at_springs_and_dampers(static_analysis=static_analysis)

        self.structural_reactions = {
            "reactions_at_constrained_dofs": post.reactions_at_constrained_dofs,
            "reactions_at_springs": post.dict_reactions_at_springs,
            "reactions_at_dampers": post.dict_reactions_at_dampers,
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
# fmt: on