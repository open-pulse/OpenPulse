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

        self.file = app().file
        self.pipeline = Pipeline()

        self.model = Model(self)
        self.preprocessor = self.model.preprocessor

        self.name = None
        self.save_path = None
        self.thumbnail = None

        self.reset()

    def reset(self, reset_all=False):

        if reset_all:
            self.preprocessor.reset_variables()
            self.file.reset()

        self.analysis_id = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0, 0, 0, 0]
        self.preferences = dict()
        self.modes = 0
 
        self.natural_frequencies_structural = list()

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

        self.initial_load_project_actions()
        app().loader.load_project_data()
        # self.model.PSD.load_psd_data_from_file()
        self.enhance_pipe_sections_appearance()
        self.preprocessor.process_all_rotation_matrices()

        self.preprocessor.check_disconnected_lines()

    def reset_project(self, **kwargs):
        # TODO: reimplement the project resetting
        self.reset()
        # self.file.remove_all_unnecessary_files(**kwargs)
        # self.file.reset_project_setup(**kwargs)
        self.file.reset_entity_file(**kwargs)
        if app().pulse_file.check_pipeline_data():
            self.process_geometry_and_mesh()
            # self.load_project_files()
            app().loader.load_project_data()

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

                cross = element.cross_section
                outer_diameter = cross.outer_diameter
                offset_y = cross.offset_y
                offset_z = cross.offset_z
                insulation_thickness = cross.insulation_thickness
                section_label = cross.section_type_label

                if element.element_type == 'expansion_joint':
                    _key = element.cross_section.expansion_joint_plot_key
                    thickness = (outer_diameter - inner_diameter) / 2
                    parameters = [  outer_diameter, 
                                    thickness, 
                                    offset_y, 
                                    offset_z, 
                                    insulation_thickness,
                                    _key
                                  ]

                else:
                    thickness = (outer_diameter - inner_diameter) / 2
                    parameters = [  outer_diameter, 
                                    thickness, 
                                    offset_y, 
                                    offset_z, 
                                    insulation_thickness
                                  ]

                element.section_parameters_render = parameters
                element.cross_section_points = cross.get_circular_section_points(parameters, 
                                                                                 section_label)

    def is_there_an_acoustic_attribute_in_the_node(self, node_id: int):

        acoustic_properties = [
                                "acoustic_pressure", 
                                "volume_velocity", 
                                "specific_impedance", 
                                "radiation_impedance", 
                                "compressor_excitation"
                                ]

        for (property, *args) in self.model.properties.nodal_properties.keys():
            if property in acoustic_properties and node_id == args[0]:
                    return True
        return False

    def update_project_analysis_setup_state(self, _bool):
        self.setup_analysis_complete = _bool

    def update_element_ids_in_element_info_file_after_remesh(self, dict_group_elements_to_update,
                                                                   dict_non_mapped_subgroups,
                                                                   dict_list_elements_to_subgroups ):
        self.file.modify_element_ids_in_element_info_file(  dict_group_elements_to_update,
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

            self.model.properties._set_nodal_property(property, data, node_ids=node_ids)

    # def get_dict_multiple_cross_sections_from_line(self, line_id):
    #     '''This methods returns a dictionary of multiples cross-sections associated to 
    #         the line of interest.        
    #     '''
    #     label_etypes = ['pipe_1']
    #     indexes = [0]
    #     dict_etype_index = dict(zip(label_etypes,indexes))

    #     dict_multiple_cross_sections = defaultdict(list)
    #     list_elements_from_line = list(self.model.mesh.line_to_elements[line_id])
        
    #     elements = self.preprocessor.structural_elements
    #     count_sections = 0
    #     single_cross = False

    #     for element_id in list_elements_from_line:

    #         element = elements[element_id]
    #         e_type  = element.element_type
    #         if e_type in ['beam_1', 'expansion_joint', 'valve', None]:
    #             continue
            
    #         index_etype = dict_etype_index[e_type]
    #         cross_section = elements[element_id].cross_section
    #         if cross_section:
    #             outer_diameter = cross_section.outer_diameter
    #             thickness = cross_section.thickness
    #             offset_y = cross_section.offset_y
    #             offset_z = cross_section.offset_z
    #             insultation_thickness = cross_section.insulation_thickness
    #             insultation_density = cross_section.insulation_density
    #             key_string = str([  outer_diameter, 
    #                                 thickness, 
    #                                 offset_y, 
    #                                 offset_z, 
    #                                 insultation_thickness, 
    #                                 insultation_density,
    #                                 index_etype ])

    #             if key_string not in list(dict_multiple_cross_sections.keys()):
    #                 count_sections += 1

    #             dict_multiple_cross_sections[key_string].append(element_id)

    #     self.number_sections_by_line[line_id] = count_sections

    #     if len(dict_multiple_cross_sections) == 1:
    #         if count_sections == 1:
    #             list_elements_from_cross_section = dict_multiple_cross_sections[key_string]
    #             if list_elements_from_cross_section == list_elements_from_line:
    #                 _element_type = elements[element_id].element_type
    #                 self.set_structural_element_type_by_lines(line_id, _element_type)
    #                 _cross_section = elements[element_id].cross_section
    #                 self.set_cross_section_by_lines(line_id, _cross_section)
    #                 if line_id in self.number_sections_by_line.keys():
    #                     self.number_sections_by_line.pop(line_id)
    #                 single_cross = True 

    #     return dict_multiple_cross_sections, single_cross

    # def set_variable_cross_section_by_line(self, line_id, section_data):
    #     """
    #     This method sets the variable section info by line selection.
    #     """
    #     if section_data:

    #         [   outer_diameter_initial, thickness_initial, offset_y_initial, offset_z_initial,
    #             outer_diameter_final, thickness_final, offset_y_final, offset_z_final,
    #             insulation_thickness, insulation_density  ] = section_data["section_parameters"]

    #         elements_from_line = self.model.mesh.line_to_elements[line_id]
    #         self.preprocessor.add_expansion_joint_by_lines(line_id, None, remove=True)

    #         first_element = self.preprocessor.structural_elements[elements_from_line[0]]
    #         last_element = self.preprocessor.structural_elements[elements_from_line[-1]]
            
    #         coord_first_1 = first_element.first_node.coordinates
    #         coord_last_1 = last_element.last_node.coordinates
            
    #         coord_first_2 = last_element.first_node.coordinates
    #         coord_last_2 = first_element.last_node.coordinates
            
    #         lines_vertex_coords = self.preprocessor.get_lines_vertex_coordinates(_array=False)
    #         vertex_coords = lines_vertex_coords[line_id]

    #         N = len(elements_from_line)
    #         if list(coord_first_1) in vertex_coords and list(coord_last_1) in vertex_coords:
    #             outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_initial, outer_diameter_final, N)
    #             thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_initial, thickness_final, N)
    #             offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_initial, offset_y_final, N)
    #             offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_initial, offset_z_final, N)

    #         elif list(coord_first_2) in vertex_coords and list(coord_last_2) in vertex_coords:
    #             outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_final, outer_diameter_initial, N)
    #             thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_final, thickness_initial, N)
    #             offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_final, offset_y_initial, N)
    #             offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_final, offset_z_initial, N)
            
    #         cross_sections_first = list()
    #         cross_sections_last = list()
    #         for index, element_id in enumerate(elements_from_line):
                
    #             element = self.preprocessor.structural_elements[element_id]
    #             first_node = element.first_node
    #             last_node = element.last_node
                
    #             section_parameters_first = [outer_diameter_first[index],
    #                                         thickness_first[index],
    #                                         offset_y_first[index],
    #                                         offset_z_first[index],
    #                                         insulation_thickness,
    #                                         insulation_density]
                
    #             pipe_section_info_first = { "section_type_label" : "Pipe" ,
    #                                         "section_parameters" : section_parameters_first }

    #             section_parameters_last = [outer_diameter_last[index],
    #                                         thickness_last[index],
    #                                         offset_y_last[index],
    #                                         offset_z_last[index],
    #                                         insulation_thickness,
    #                                         insulation_density]
                
    #             pipe_section_info_last = { "section_type_label" : "Pipe" ,
    #                                         "section_parameters" : section_parameters_last }

    #             cross_section_first = CrossSection(pipe_section_info = pipe_section_info_first)
    #             cross_section_last = CrossSection(pipe_section_info = pipe_section_info_last)

    #             cross_sections_first.append(cross_section_first)
    #             # cross_sections_last.append(cross_section_last)

    #             first_node.cross_section = cross_section_first
    #             last_node.cross_section = cross_section_last

    #         self.set_cross_section_by_elements( elements_from_line,
    #                                             cross_sections_first,
    #                                             remesh_mapping = False,
    #                                             variable_section = True )
        
    # def set_cross_section_by_lines(self, lines, cross_section):
    #     """
    #     """
    #     self.preprocessor.add_expansion_joint_by_lines(lines, None, remove=True)
    #     self.preprocessor.set_cross_section_by_lines(lines, cross_section)
    #     self._set_cross_section_to_selected_line(lines, cross_section)
    #     self.file.add_cross_section_in_file(lines, cross_section)

    # def set_cross_section_by_elements(self, list_elements, cross_section, remesh_mapping=True, variable_section=False):
    #     """
    #     """
    #     if remesh_mapping:
    #         self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(list_elements)
    #     self.preprocessor.set_cross_section_by_element(list_elements, cross_section, variable_section=variable_section)       
        # for element in list_elements:
        #     line = self.model.mesh.elements_to_line[element]
        #     if line not in self.lines_with_cross_section_by_elements:
        #         self.lines_with_cross_section_by_elements.append(line)

    # def reset_number_sections_by_line(self, line_id):
    #     if line_id in list(self.number_sections_by_line.keys()):
    #         self.number_sections_by_line.pop(line_id)

    # def add_cross_sections_expansion_joints_valves_in_file(self, list_elements):
    #     list_lines = list()
    #     for element_id in list_elements:
    #         line_id = self.model.mesh.elements_to_line[element_id]
    #         if line_id not in list_lines:
    #             list_lines.append(line_id)
    #     for _line_id in list_lines:
    #         map_expansion_joints_to_elements = dict()
    #         map_valves_to_elements = dict()
    #         map_cross_sections_to_elements, single_cross = self.get_dict_multiple_cross_sections_from_line(_line_id)
    #         if not single_cross:
                  
    #             map_expansion_joints_to_elements = self.get_map_expansion_joints_to_elements(_line_id)
    #             map_valves_to_elements = self.get_map_valves_to_elements(_line_id)

    #             self.file.add_multiple_cross_sections_expansion_joints_valves_in_file(  _line_id, 
    #                                                                                     map_cross_sections_to_elements, 
    #                                                                                     map_expansion_joints_to_elements,
    #                                                                                     map_valves_to_elements )  
                
    #             for list_elements_mapped in map_cross_sections_to_elements.values():
    #                 self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(list_elements_mapped)

    def add_lumped_masses_by_node(self, node_id, data, imported_table):
        self.preprocessor.add_mass_to_node(node_id, data)

    def add_lumped_stiffness_by_node(self, node_id, data, imported_table):
        self.preprocessor.add_spring_to_node(node_id, data)

    def add_lumped_dampings_by_node(self, node_id, data, imported_table):
        self.preprocessor.add_damper_to_node(node_id, data)

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
        self.preprocessor.add_valve_by_line(line_ids, parameters, remove=remove, reset_cross=reset_cross)
        self.set_structural_element_type_by_lines(line_ids, etype)

    # def add_expansion_joint_by_lines(self, lines_id, parameters):

    #     if isinstance(lines_id, int):
    #         lines_id = [lines_id]

    #     if parameters is None:
    #         remove = True
    #         capped = False
    #         etype = "pipe_1"
    #     else:
    #         remove = False
    #         capped = True
    #         etype = "expansion_joint"

    #     self.preprocessor.add_expansion_joint_by_lines(lines_id, parameters, remove=remove)
    #     self.set_capped_end_by_lines(lines_id, capped)
    #     self.set_structural_element_type_by_lines(lines_id, etype)
    #     # if etype == "pipe_1":
    #     #     self.set_cross_section_by_lines(lines_id, None)  
    #     self._set_expansion_joint_to_selected_lines(lines_id, parameters)

    #     for line_id in lines_id:
    #         if line_id in self.number_sections_by_line.keys():
    #             self.number_sections_by_line.pop(line_id)

    #     self.file.modify_expansion_joint_in_file(line_id, parameters)   

    def get_map_expansion_joints_to_elements(self, line_id):
        structural_elements = self.preprocessor.structural_elements
        dict_multiple_expansion_joints = dict()
        dict_exp_joint_key_parameters_to_parameters = dict()
        dict_exp_joint_key_parameters_to_table_names = dict()
        dict_exp_joint_key_parameters_to_elements = defaultdict(list)
        for element_id in self.model.mesh.line_to_elements[line_id]:
            element = structural_elements[element_id]
            if element.expansion_joint_data:
                dict_exp_joint_key_parameters_to_elements[str(element.expansion_joint_data)].append(element_id)
                dict_exp_joint_key_parameters_to_parameters[str(element.expansion_joint_data)] = element.expansion_joint_data
                dict_exp_joint_key_parameters_to_table_names[str(element.expansion_joint_data)] = element.joint_stiffness_table_names
        for ind, (key_parameters, _group_elements) in enumerate(dict_exp_joint_key_parameters_to_elements.items()):
            section_key = f"{line_id}-{ind + 1}"
            parameters_exp_joint = dict_exp_joint_key_parameters_to_parameters[key_parameters]
            table_names = dict_exp_joint_key_parameters_to_table_names[key_parameters]
            dict_multiple_expansion_joints[section_key] = [parameters_exp_joint, _group_elements, table_names]
        return dict_multiple_expansion_joints

    def get_map_valves_to_elements(self, line_id):
        structural_elements = self.preprocessor.structural_elements
        dict_multiple_valves = dict()
        dict_valve_key_parameters_to_parameters = dict()
        dict_valve_key_parameters_to_elements = defaultdict(list)
        for element_id in self.model.mesh.line_to_elements[line_id]:
            element = structural_elements[element_id]
            if element.valve_parameters:
                dict_valve_key_parameters_to_elements[str(element.valve_parameters)].append(element_id)
                dict_valve_key_parameters_to_parameters[str(element.valve_parameters)] = element.valve_parameters
        for ind, (key_parameters, _group_elements) in enumerate(dict_valve_key_parameters_to_elements.items()):
            section_key = f"{line_id}-{ind + 1}"
            parameters_valve = dict_valve_key_parameters_to_parameters[key_parameters]
            dict_multiple_valves[section_key] = [parameters_valve, _group_elements]
        return dict_multiple_valves

    def load_valve_by_lines(self, line_id, data, cross_sections):
        valve_elements = data["valve_elements"]
        valve_cross, flange_cross = cross_sections
        self.preprocessor.add_valve_by_line(line_id, data)
        self._set_valve_to_selected_lines(line_id, data)

        if 'flange_elements' in data.keys():
            flange_elements = data["flange_elements"]
            _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
            self.preprocessor.set_cross_section_by_element(_valve_elements, valve_cross)
            self.preprocessor.set_cross_section_by_element(flange_elements, flange_cross)
        else:
            self.preprocessor.set_cross_section_by_element(valve_elements, valve_cross)
        self.preprocessor.set_structural_element_type_by_lines(line_id, 'valve')

    def load_valve_by_elements(self, data, cross_sections):
        valve_elements = data["valve_elements"]
        valve_cross, flange_cross = cross_sections
        self.preprocessor.add_valve_by_elements(valve_elements, data)
        self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(valve_elements)
        
        if 'flange_elements' in data.keys():
            flange_elements = data["flange_elements"]
            _valve_elements = [element_id for element_id in valve_elements if element_id not in flange_elements]
            self.preprocessor.set_cross_section_by_element(_valve_elements, valve_cross)
            self.preprocessor.set_cross_section_by_element(flange_elements, flange_cross)
        else:
            self.preprocessor.set_cross_section_by_element(valve_elements, valve_cross)
        self.preprocessor.set_structural_element_type_by_element(valve_elements, "valve")

    def get_structural_elements(self):
        return self.preprocessor.structural_elements
    
    def get_structural_element(self, element_id):
        return self.preprocessor.structural_elements[element_id]

    def get_acoustic_elements(self):
        return self.preprocessor.acoustic_elements 

    def get_acoustic_element(self, element_id):
        return self.preprocessor.acoustic_elements[element_id]
    
    # def load_perforated_plate_by_elements(self, list_elements, perforated_plate, key):
    #     self.preprocessor.set_perforated_plate_by_elements(list_elements, perforated_plate, key)
    #     self.preprocessor.process_elements_to_update_indexes_after_remesh_in_element_info_file(list_elements)
    
    def set_perforated_plate_convergence_dataLog(self, data):
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

    def set_analysis_type(self, ID, analysis_text, method_text = ""):
        self.analysis_id = ID
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_pre_solution_model_checks(self):
        return BeforeRun()

    def get_post_solution_model_checks(self):
        return AfterRun()

    def set_structural_solve(self, structural_solve):
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

    def set_structural_reactions(self, value):
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