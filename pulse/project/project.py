from pulse.tools.utils import *
#
# from pulse.project.load_project import LoadProject
# from pulse.model.line import Line
# from pulse.model.preprocessor import Preprocessor
from pulse.model.cross_section import CrossSection
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.model.after_run import AfterRun
from pulse.model.before_run import BeforeRun
from pulse.processing.structural_solver import StructuralSolver
from pulse.processing.acoustic_solver import AcousticSolver
#
from pulse import app
from pulse.model.model import Model
from pulse.interface.user_input.project.loading_screen import LoadingScreen
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import *

#
from opps.model import Pipeline
#
import numpy as np
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

        self.analysis_id = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0, 0, 0, 0]
        self.preferences = dict()
        self.modes = 0

        self.solution_structural = None
        self.solution_acoustic = None
        self.natural_frequencies_structural = None
        self.natural_frequencies_acoustic = None
        self.perforated_plate_data_log = None
        self.flag_set_material = False
        self.flag_set_crossSection = False
        self.plot_pressure_field = False
        self.plot_stress_field = False
        self.is_file_loaded = False
        self.setup_analysis_complete = False
        self.none_project_action = False
        self.stress_stiffening_enabled = False

        self.color_scale_setup = dict()

        self.time_to_load_or_create_project = 0
        self.time_to_checking_entries = 0
        self.time_to_process_cross_sections = 0
        self.time_to_preprocess_model = 0
        self.time_to_solve_model = 0
        self.time_to_solve_acoustic_model = 0
        self.time_to_solve_structural_model = 0
        self.time_to_postprocess = 0
        self.total_time = 0

        self.number_sections_by_line = dict()
        # self.lines_with_cross_section_by_elements = list()
        self.stresses_values_for_color_table = None
        self.min_stress = ""
        self.max_stress = ""
        self.stress_label = ""

    def initial_load_project_actions(self):

        try:

            self.reset(reset_all=True)

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

        # def load_callback():
        #     app().loader.load_project_data()

        # if self.initial_load_project_actions():
        #     LoadingScreen(  
        #                     title = 'Loading Project', 
        #                     message = "Loading project files",
        #                     target = load_callback
        #                   )

        app().loader.load_project_data()
        self.initial_load_project_actions()
        app().loader.load_mesh_dependent_properties()

        # self.enhance_pipe_sections_appearance()
        self.preprocessor.process_all_rotation_matrices()
        self.preprocessor.check_disconnected_lines()

    def reset_project(self, **kwargs):

        self.reset(reset_all=True)
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
        self.update_node_ids_after_mesh_changed()
        # dt = time()-t0
        # print(f"Time to process_geometry_and_mesh: {dt} [s]")

    def enhance_pipe_sections_appearance(self):
        """ 
        This method adds lids to cross-section variations and terminations.
        """
        for elements in self.preprocessor.elements_connected_to_node.values():

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
                    parameters = [  outer_diameter, 
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

    def update_project_analysis_setup_state(self, _bool):
        self.setup_analysis_complete = _bool

    def update_element_ids_in_element_info_file_after_remesh(self, dict_group_elements_to_update,
                                                                   dict_non_mapped_subgroups,
                                                                   dict_list_elements_to_subgroups ):
        self.modify_element_ids_in_element_info_file(  dict_group_elements_to_update,
                                                            dict_non_mapped_subgroups,
                                                            dict_list_elements_to_subgroups  )

    def update_node_ids_after_mesh_changed(self):

        aux = dict()
        non_mapped_nodes = list()

        for key, data in self.model.properties.nodal_properties.items():

            (property, *args) = key

            if "coords" in data.keys():
                coords = np.array(data["coords"], dtype=float)
                if len(coords) == 6:

                    node_id1, node_id2 = args

                    coords_1 = coords[:3]
                    coords_2 = coords[3:]
                    new_node_id1 = self.preprocessor.get_node_id_by_coordinates(coords_1)
                    new_node_id2 = self.preprocessor.get_node_id_by_coordinates(coords_2)
                    sorted_indexes = np.sort([new_node_id1, new_node_id2])

                    new_key = (property, sorted_indexes[0], sorted_indexes[1])

                    if new_node_id1 is None:
                        if new_node_id1 not in non_mapped_nodes:
                            non_mapped_nodes.append((node_id1, coords))
                        continue

                    if new_node_id2 is None:
                        if new_node_id2 not in non_mapped_nodes:
                            non_mapped_nodes.append((node_id2, coords))
                        continue

                elif len(coords) == 3:

                    node_id = args
                    new_node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                    new_key = (property, new_node_id)

                    if new_node_id is None:
                        if new_node_id not in non_mapped_nodes:
                            non_mapped_nodes.append((node_id, coords))
                        continue

                aux[key] = [new_key, data]
                
                if non_mapped_nodes:
                    print(f"List of non-mapped nodes: {non_mapped_nodes}")
                    return non_mapped_nodes

        self.model.properties.nodal_properties.clear()

        for [new_key, data] in aux.values():
            (property, *args) = new_key
            if len(new_key) == 2:
                property = new_key[0]
                node_ids = new_key[1]
            elif len(new_key) == 3:
                property = new_key[0]
                node_ids = (new_key[1], new_key[2])
            else:
                return

            self.model.properties._set_nodal_property(property, data, node_ids)

    def add_valve_by_line(self, line_ids, parameters, reset_cross=True):
        if parameters is None:
            remove = True
            capped = False
            etype = "pipe_1"
        else:
            remove = False
            capped = True
            etype = "valve"

        self.preprocessor.add_expansion_joint_by_lines(line_ids, None, remove=True)
        self.preprocessor.add_valve_by_lines(line_ids, parameters, remove=remove, reset_cross=reset_cross)
        # self.set_structural_element_type_by_lines(line_ids, etype)

    def load_valve_by_lines(self, line_id, data, cross_sections):
        valve_elements = data["valve_elements"]
        valve_cross, flange_cross = cross_sections
        self.preprocessor.add_valve_by_line(line_id, data)

        if 'flange_elements' in data.keys():
            flange_elements = data["flange_elements"]
            _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
            self.preprocessor.set_cross_section_by_element(_valve_elements, valve_cross)
            self.preprocessor.set_cross_section_by_element(flange_elements, flange_cross)
        else:
            self.preprocessor.set_cross_section_by_element(valve_elements, valve_cross)
        self.preprocessor.set_structural_element_type_by_lines(line_id, 'valve')

    # def load_valve_by_elements(self, data, cross_sections):
    #     valve_elements = data["valve_elements"]
    #     valve_cross, flange_cross = cross_sections
    #     self.preprocessor.add_valve_by_elements(valve_elements, data)
    #     self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(valve_elements)
        
    #     if 'flange_elements' in data.keys():
    #         flange_elements = data["flange_elements"]
    #         _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
    #         self.preprocessor.set_cross_section_by_elements(_valve_elements, valve_cross)
    #         self.preprocessor.set_cross_section_by_elements(flange_elements, flange_cross)
    #     else:
    #         self.preprocessor.set_cross_section_by_elements(valve_elements, valve_cross)
    #     self.preprocessor.set_structural_element_type_by_element(valve_elements, "valve")

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

    def get_geometry_points(self):
        points = dict()
        for i in self.preprocessor.mesh.geometry_points:
            points[i] = self.preprocessor.nodes[i]
        return points

    def set_modes_sigma(self, modes, sigma=1e-2):
        self.modes = modes
        self.sigma = sigma

    def get_modes(self):
        return self.modes

    def set_analysis_type(self, analysis_id: int, analysis_text: str, method_text = ""):
        self.analysis_id = analysis_id
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_pre_solution_model_checks(self):
        return BeforeRun()

    def get_post_solution_model_checks(self):
        return AfterRun()

    def set_structural_solve(self, structural_solve: StructuralSolver):
        self.structural_solve = structural_solve

    def get_structural_solve(self):
        if self.analysis_id in [5, 6]:
            results = StructuralSolver(self.model, acoustic_solution=self.solution_acoustic)
        else:
            results = StructuralSolver(self.model)
        return results

    def set_structural_solution(self, value):
        self.solution_structural = value

    def get_structural_solution(self):
        return self.solution_structural

    def get_acoustic_solve(self):
        return AcousticSolver(self.model)

    def set_acoustic_solution(self, value):
        self.solution_acoustic = value
    
    def get_acoustic_solution(self):
        return self.solution_acoustic

    def set_acoustic_natural_frequencies(self, value):
        self.natural_frequencies_acoustic = value

    def get_acoustic_natural_frequencies(self):
        return self.natural_frequencies_acoustic
    
    def set_structural_natural_frequencies(self, value):
        self.natural_frequencies_structural  = value

    def set_structural_reactions(self, value: dict):
        self.structural_reactions = value

    def get_structural_natural_frequencies(self):
        return self.natural_frequencies_structural

    def get_structural_reactions(self):
        return self.structural_reactions

    def get_unit(self):
        if self.analysis_id is None:
            return self.analysis_id
        analysis = self.analysis_id
        if analysis >=0 and analysis <= 7:
            if (analysis in [3, 5, 6] and self.plot_pressure_field) or self.plot_stress_field:
                return "Pa"
            elif analysis in [5, 6] and not self.plot_pressure_field:
                return "m"            
            elif analysis in [0, 1, 7]:
                return "m"
            else:
                return "-"

    def set_stresses_values_for_color_table(self, values):
        self.stresses_values_for_color_table = values
    
    def set_min_max_type_stresses(self, min_stress, max_stress, stress_label):
        self.min_stress = min_stress
        self.max_stress = max_stress
        self.stress_label = stress_label

    def is_the_solution_finished(self):
        if self.solution_acoustic is not None:
            return True
        elif self.solution_structural is not None:
            return True
        else:
            return False