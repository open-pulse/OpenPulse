# fmt: off

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import *
from pulse.interface.user_input.project.loading_window import LoadingWindow
#
from opps.model import Pipeline
from pulse.model.model import Model
from pulse.model.after_run import AfterRun
from pulse.model.before_run import BeforeRun
from pulse.processing.structural_solver import StructuralSolver
from pulse.processing.acoustic_solver import AcousticSolver
from pulse.tools.utils import *
#
import logging
from collections import defaultdict


window_title = "Error"

class Project:
    def __init__(self):

        self.pipeline = Pipeline()

        self.model = Model(self)
        self.preprocessor = self.model.preprocessor

        self.name = None
        self.save_path = None
        self.thumbnail = None

        self.reset()

    def reset(self, reset_all=False):

        # TODO: reimplement this
        if reset_all:
            self.preprocessor.reset_variables()
            #TODO: reset nodal, element and line properties

        self.preferences = dict()
        self.color_scale_setup = dict()

        self.perforated_plate_data_log = None
        self.none_project_action = False
        self.stress_stiffening_enabled = False

        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""
        self.stresses_values_for_color_table = None

        # default animation settings
        self.frames = 40
        self.cycles = 3

        self.reset_analysis_setup()
        self.reset_solvers()
        self.reset_solution()

    def reset_solvers(self):
        self.acoustic_solver = None
        self.structural_solver = None

    def reset_solution(self):
        self.structural_solution = None
        self.acoustic_solution = None

        self.natural_frequencies_acoustic = list()
        self.natural_frequencies_structural = list()

        self.acoustic_harmonic_solution = None
        self.acoustic_modal_solution = None
        self.structural_harmonic_solution = None
        self.structural_modal_solution = None
        self.structural_static_solution = None
        self.structural_reactions = dict()

    def reset_analysis_setup(self):
        self.modes = 0
        self.global_damping = [0, 0, 0, 0]
        self.analysis_id = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""

    def initial_load_project_actions(self):

        try:

            self.reset(reset_all = True)
            app().loader.load_analysis_id()
            app().loader.load_analysis_results()

            if app().pulse_file.check_pipeline_data():
                self.process_geometry_and_mesh()
                return True
            else:
                return False

        except Exception as log_error:
            title = "Error while processing initial load project actions"
            message = str(log_error)
            PrintMessageInput([window_title, title, message])
            return False

    def load_project(self):

        logging.info("Loading project data [30%]")
        app().loader.load_project_data()

        logging.info("Processing geometry and mesh [50%]")
        self.initial_load_project_actions()

        logging.info("Loading mesh dependent properties [60%]")
        app().loader.load_mesh_dependent_properties()

        logging.info("Finalizing model data loading [75%]")
        self.preprocessor.process_all_rotation_matrices()
        self.preprocessor.check_disconnected_lines()

    def reset_project(self, **kwargs):

        self.reset(reset_all = True)
        app().pulse_file.remove_element_properties_from_project_file()
        app().pulse_file.remove_nodal_properties_from_project_file()

        if app().pulse_file.check_pipeline_data():
            app().loader.load_project_data()
            self.process_geometry_and_mesh()
            app().loader.load_mesh_dependent_properties()

    def process_geometry_and_mesh(self):
        # t0 = time()
        self.preprocessor.generate()
        app().main_window.update_status_bar_info()
        # dt = time()-t0
        # print(f"Time to process_geometry_and_mesh: {dt} [s]")

    def enhance_pipe_sections_appearance(self):
        """ 
        This method adds lids to cross-section variations and terminations.
        """
        for elements in self.preprocessor.structural_elements_connected_to_node.values():

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

                if len(self.preprocessor.neighbors[first_node]) == 1:
                    first_node_id = first_node.external_index
                    if self.is_there_an_acoustic_attribute_in_the_node(first_node_id) == 0:
                        inner_diameter = 0

                elif len(self.preprocessor.neighbors[last_node]) == 1:
                    last_node_id = last_node.external_index
                    if self.is_there_an_acoustic_attribute_in_the_node(last_node_id) == 0:
                        inner_diameter = 0

            if element:

                if element.element_type == 'expansion_joint':

                    d_eff = element.cross_section.section_parameters[1]
                    plot_key = element.cross_section.section_parameters[0]

                    thickness = (outer_diameter - inner_diameter) / 2
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
                                "compressor_excitation",
                                "psd_acoustic_link"
                                ]

        for (property, *args) in self.model.properties.nodal_properties.keys():
            if property in acoustic_properties and node_id in args:
                    return True

        return False

    def is_analysis_setup_complete(self):
        self.analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        if isinstance(self.analysis_setup, dict):
            if "analysis_id" in self.analysis_setup.keys():
                self.analysis_id = self.analysis_setup["analysis_id"]
                self.modes = self.analysis_setup.get("modes", 40)
                self.sigma_factor = self.analysis_setup.get("sigma_factor", 40)
                return True
        return False

    def get_structural_elements(self):
        return self.preprocessor.structural_elements
    
    def get_structural_element(self, element_id):
        return self.preprocessor.structural_elements[element_id]

    def get_acoustic_elements(self):
        return self.preprocessor.acoustic_elements 

    def get_acoustic_element(self, element_id):
        return self.preprocessor.acoustic_elements[element_id]

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

                node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                neigh_elements = self.preprocessor.structural_elements_connected_to_node[node_id]
    
                for element in neigh_elements:

                    element_line = self.preprocessor.mesh.line_from_element[element.index]
                    _data = self.model.properties.line_properties[element_line]

                    if "corner_coords" in _data.keys():
                        lines_neighboors[line_id, "curve"].append(element_line)
                    else:
                        lines_neighboors[line_id, "line"].append(element_line)

    def get_geometry_points(self):
        points = dict()
        for i in self.preprocessor.mesh.geometry_points:
            points[i] = self.preprocessor.nodes[i]
        return points

    def set_analysis_id(self, analysis_id: int):

        self.analysis_id = analysis_id

        if analysis_id in [0, 1]:
            self.analysis_type_label = "Structural Harmonic Analysis"
        elif analysis_id == 2:
            self.analysis_type_label = "Structural Modal Analysis"
        elif analysis_id == 3:
            self.analysis_type_label = "Acoustic Harmonic Analysis"
        elif analysis_id == 4:
            self.analysis_type_label = "Acoustic Modal Analysis"
        elif analysis_id in [5, 6]:
            self.analysis_type_label = "Coupled Harmonic Analysis"
        elif analysis_id == 7:
            self.analysis_type_label = "Structural Static Analysis"
        else:
            self.analysis_type_label = None

        if self.analysis_id in [0, 5, 3]:
            self.analysis_method_label = "Direct method"
        elif self.analysis_id in [1, 6]:
            self.analysis_method_label = "Mode superposition method"
        else:
            self.analysis_method_label = None

    def load_analysis_setup(self):
        self.analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        self.analysis_id = self.analysis_setup["analysis_id"]
        self.modes = self.analysis_setup.get("modes", 40)
        self.sigma_factor = self.analysis_setup.get("sigma_factor", 40)

    def get_pre_solution_model_checks(self):
        return BeforeRun()

    def get_post_solution_model_checks(self):
        return AfterRun()

    def get_acoustic_solver(self) -> AcousticSolver:
        return AcousticSolver(self.model)

    def get_structural_solver(self) -> StructuralSolver:
        if self.analysis_id in [5, 6]:
            return StructuralSolver(self.model, acoustic_solution=self.acoustic_solution)
        else:
            return StructuralSolver(self.model)

    def get_structural_solution(self):
        return self.structural_solution

    def get_acoustic_harmonic_solution(self):
        return self.acoustic_harmonic_solution

    def get_acoustic_modal_solution(self):
        return self.acoustic_modal_solution

    def get_structural_harmonic_solution(self):
        return self.structural_harmonic_solution

    def get_structural_modal_solution(self):
        return self.structural_modal_solution

    def get_structural_static_solution(self):
        return self.structural_static_solution

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

        else:
            return False

    def get_harmonic_analysis_method(self):

        analysis_setup = app().pulse_file.read_analysis_setup_from_file()
        if isinstance(analysis_setup, dict):
            analysis_id = analysis_setup.get("analysis_id", None)

        if analysis_id is None:
            return ""
        
        elif analysis_id in [0, 3, 5]:
            return "Direct method"
        
        elif analysis_id in [1, 6]:
            return "Mode superposition method"

    def initialize_solver(self):

        if self.analysis_id in [0, 1, 3, 5, 6]:
            if self.model.frequencies is None:
                return

            if len(self.model.frequencies) == 0:
                return

        if self.preprocessor._process_beam_nodes_and_indexes():
            if self.analysis_id not in [0, 1, 2]:
                title = "Invalid analysis type"
                message = "There are only BEAM_1 elements in the model, therefore, "
                message += "only structural analysis are allowable."
                info_text = [window_title_2, title, message]
                PrintMessageInput(info_text)
                return

        if self.analysis_id == 2:
            self.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.structural_solver = self.get_structural_solver()

        elif self.analysis_id in [3, 4]:
            self.acoustic_solver = self.get_acoustic_solver()

        elif self.analysis_id in [5, 6]:
            self.preprocessor.enable_fluid_mass_adding_effect()
            self.acoustic_solver = self.get_acoustic_solver()

        else:
            self.preprocessor.enable_fluid_mass_adding_effect(reset=True)
            self.structural_solver = self.get_structural_solver()

    def process_analysis(self):

        if self.analysis_id == 0: # Structural Harmonic Analysis - Direct Method
            self.structural_solver.direct_method()
            self.structural_solution = self.structural_solver.solution
            # self.structural_harmonic_solution = self.structural_solver.solution

        elif self.analysis_id == 1: # Structural Harmonic Analysis - Mode Superposition Method
            self.structural_solver.mode_superposition(self.modes)
            self.structural_solution = self.structural_solver.solution
            # self.structural_harmonic_solution = self.structural_solver.solution

        elif self.analysis_id == 3: # Acoustic Harmonic Analysis - Direct Method
            self.acoustic_solver.direct_method()
            self.acoustic_solution = self.acoustic_solver.solution
            self.perforated_plate_data_log = self.acoustic_solver.convergence_data_log

        elif self.analysis_id == 5: # Coupled Harmonic Analysis - Direct Method
            self.acoustic_solver.direct_method()
            self.acoustic_solution = self.acoustic_solver.solution
            self.perforated_plate_data_log = self.acoustic_solver.convergence_data_log

            self.structural_solver = self.get_structural_solver()
            self.structural_solver.direct_method()
            self.structural_solution = self.structural_solver.solution
            # self.structural_harmonic_solution = self.structural_solver.solution

        elif self.analysis_id == 6: # Coupled Harmonic Analysis - Mode Superposition Method
            self.acoustic_solver.direct_method()
            self.acoustic_solution = self.acoustic_solver.solution
            self.perforated_plate_data_log = self.acoustic_solver.convergence_data_log
            self.structural_solver = self.get_structural_solver()
            self.structural_solver.mode_superposition(self.modes)
            self.structural_solution = self.structural_solver.solution
            # self.structural_harmonic_solution = self.structural_solver.solution

        elif self.analysis_id == 2: # Structural Modal Analysis
            self.structural_solver.modal_analysis(modes = self.modes, sigma_factor = self.sigma_factor)
            self.natural_frequencies_structural = self.structural_solver.natural_frequencies
            self.structural_solution = self.structural_solver.modal_shapes
            # self.structural_modal_solution = self.structural_solver.modal_shapes

        elif self.analysis_id == 4: # Acoustic Modal Analysis
            self.acoustic_solver.modal_analysis(modes = self.modes, sigma_factor = self.sigma_factor)
            self.natural_frequencies_acoustic = self.acoustic_solver.natural_frequencies
            self.acoustic_solution = self.acoustic_solver.modal_shapes
            # self.structural_modal_solution = self.acoustic_solver.modal_shapes

        elif self.analysis_id == 7: # Static Analysis
            self.structural_solver.static_analysis()
            self.structural_solution = self.structural_solver.solution
            # self.structural_static_solution = self.structural_solver.solution

        else:
            raise NotImplementedError("Not implemented analysis")

        if isinstance(self.acoustic_solver, AcousticSolver):
            if self.analysis_id in [3, 5, 6]:
                from time import sleep
                if self.acoustic_solver.nl_pp_elements:
                    sleep(1)

    def run_analysis(self):
        LoadingWindow(self.build_model_and_solve).run()

    def build_model_and_solve(self):

        setup_complete = self.is_analysis_setup_complete()

        if not setup_complete:
            title = "Incomplete analysis setup" 
            message = "Please, it is necessary to choose an analysis type "
            message += "and setup it before trying to solve the model."
            PrintMessageInput([window_title_1, title, message])
            return

        self.before_run = self.get_pre_solution_model_checks()
        if self.before_run.check_is_there_a_problem(self.analysis_id):
            return

        logging.info("Processing the cross-sections [10%]")
        if self.model.preprocessor.process_cross_sections_mapping():
            self.preprocessor.stop_processing = False
            return

        logging.info("Initializing the problem solver [30%]")
        self.initialize_solver()

        logging.info("Solution in progress [50%]")
        self.process_analysis()

        logging.info("Saving the solution data [95%]")
        app().pulse_file.write_results_data_in_file()

        if self.preprocessor.stop_processing:
            self.reset_solution()
            self.preprocessor.stop_processing = False
            return

        logging.info("Post-processing the obtained results [90%]")
        self.check_warnings()

        logging.info("Processing the post solution checks [95%]")
        self.post_solution_actions()

    def check_warnings(self):

        message = ""
        if self.analysis_id in [0, 1]:
            if self.structural_solver.warning_mode_sup_prescribed_dofs != "":
                message = self.structural_solver.warning_mode_sup_prescribed_dofs
            if self.structural_solver.flag_Clump and self.analysis_id==1:
                message = self.structural_solver.warning_Clump

        elif self.analysis_id in [2]:
            if self.structural_solver.warning_modal_prescribed_dofs != "":
                message = self.structural_solver.warning_modal_prescribed_dofs

        elif self.analysis_id in [3]:
            if self.acoustic_solver.warning_modal_prescribed_pressures != "":
                message = self.acoustic_solver.warning_modal_prescribed_pressures

        if message != "":
            title = self.analysis_type_label
            PrintMessageInput([window_title_2, title, message])

    def calculate_structural_reactions(self):

        if self.structural_solution is None:
            return

        if self.analysis_id == 7:
            static_analysis = True
        else:
            static_analysis = False

        self.structural_solver.get_reactions_at_constrained_dofs(static_analysis=static_analysis)
        self.structural_solver.get_reactions_at_springs_and_dampers(static_analysis=static_analysis)

        self.structural_reactions = {
                                     "reactions_at_constrained_dofs" : self.structural_solver.reactions_at_constrained_dofs,
                                     "reactions_at_springs" : self.structural_solver.dict_reactions_at_springs,
                                     "reactions_at_dampers" : self.structural_solver.dict_reactions_at_dampers,
                                     }

    def post_solution_actions(self):

        if self.analysis_id == 2:
            self.before_run.check_modal_analysis_imported_data()

        elif self.analysis_id in [3, 5, 6]:
            self.before_run.check_all_acoustic_criteria()

        if self.analysis_id in [0, 1, 5, 6, 7]:
            self.calculate_structural_reactions()

        self.after_run = self.get_post_solution_model_checks()
        self.after_run.check_all_acoustic_criterias()

        app().main_window.use_results_workspace()
        app().main_window.results_widget.show_empty()
        app().main_window.results_viewer_wigdet.bottom_widget.hide()

# fmt: on