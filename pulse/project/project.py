from pulse.tools.utils import *
#
from pulse.project.load_project_data import LoadProjectData
from pulse.preprocessing.entity import Entity
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.after_run import AfterRun
from pulse.preprocessing.before_run import BeforeRun
from pulse.processing.structural_solver import StructuralSolver
from pulse.processing.acoustic_solver import AcousticSolver
#
from pulse import app
from pulse.editor.pulsation_suppression_device import PulsationSuppressionDevice
from pulse.interface.user_input.project.loading_screen import LoadingScreen
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.interface.user_input.model.setup.structural.expansion_joint_input import *
# from pulse.interface.user_input.project.call_double_confirmation import CallDoubleConfirmationInput
# from pulse.interface.user_input.project.loading_screen import LoadingScreen
#
from opps.model import Pipeline
#
import os
import numpy as np
from shutil import rmtree
from collections import defaultdict

window_title = "Error"

class Project:
    def __init__(self):

        self.file = app().file
        self.pipeline = Pipeline()
        self.preprocessor = Preprocessor(self)        
        self.PSD = PulsationSuppressionDevice(self)

        self.reset()

    def reset(self, reset_all=False):

        if reset_all:
            self.preprocessor.reset_variables()
            self.file.reset() 

        self.analysis_ID = None
        self.analysis_type_label = ""
        self.analysis_method_label = ""
        self.global_damping = [0, 0, 0, 0]
        self.preferences = dict()
        self.modes = 0
        self.frequencies = None
        self.f_min = 0
        self.f_max = 0
        self.f_step = 0
        self.list_frequencies = list()
        self.natural_frequencies_structural = list()
        self.imported_table_frequency_setup = False
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
        self.weight_load = True
        self.internal_pressure_load = True
        self.external_nodal_loads = True
        self.element_distributed_load = True
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

    def initial_load_project_actions(self, project_file_path):
        try:

            self.reset(reset_all=True)
            self.file.load(project_file_path)

            if self.file.check_if_entity_file_is_active():
                self.process_geometry_and_mesh()
                return True
            else:
                return False

        except Exception as log_error:
            title = "Error while processing initial load project actions"
            message = str(log_error)
            PrintMessageInput([window_title, title, message])
            return False

    def update_project_analysis_setup_state(self, _bool):
        self.setup_analysis_complete = _bool

    def new_project(self, *args, **kwargs):
        self.reset(reset_all=True)
        self.file.new(*args, **kwargs)
        self.file.create_backup_geometry_folder()
        self.process_geometry_and_mesh()

    def new_empty_project(self, *args, **kwargs):
        self.reset(reset_all=True)
        self.file.new(*args, **kwargs)
        self.preprocessor._create_gmsh_geometry()

    def copy_project(self, *args, **kwargs):
        self.file.copy(*args, **kwargs)
         
    def load_project(self, project_file_path):
        def callback():
            self.load_project_files()
        
        if self.initial_load_project_actions(project_file_path): 
            LoadingScreen(title = 'Loading Project', 
                        message = "Loading project files",
                        target=callback)
        self.preprocessor.check_disconnected_lines(self.file._element_size)

    def reset_project(self, **kwargs):
        self.reset()
        self.file.remove_all_unnecessary_files(**kwargs)
        self.file.reset_fluid_and_material_files(**kwargs)
        self.file.reset_project_setup(**kwargs)
        self.file.reset_entity_file(**kwargs)
        if self.file.check_if_entity_file_is_active():
            self.process_geometry_and_mesh()
            self.load_project_files()

    def process_geometry_and_mesh(self):
        # t0 = time()
        self.preprocessor.generate( import_type = self.file.get_import_type(),
                                    length_unit = self.file._length_unit,
                                    geometry_path = self.file.geometry_path, 
                                    element_size = self.file.element_size, 
                                    tolerance = self.file.geometry_tolerance )
        self.file.update_node_ids_after_mesh_changed()
        # dt = time()-t0
        # print(f"Time to process_geometry_and_mesh: {dt} [s]")

    def load_project_files(self):
        self.load_structural_bc_file()
        self.load_acoustic_bc_file()
        self.load_entity_file()
        self.load_analysis_file()
        self.load_inertia_load_setup()
        self.PSD.load_psd_data_from_file()

    def update_element_ids_in_entity_file_after_remesh(self, dict_group_elements_to_update_entity_file, 
                                                             dict_non_mapped_subgroups_entity_file):
        self.file.modify_list_of_element_ids_in_entity_file(dict_group_elements_to_update_entity_file, 
                                                            dict_non_mapped_subgroups_entity_file)
    
    def update_element_ids_in_element_info_file_after_remesh(self, dict_group_elements_to_update,
                                                                   dict_non_mapped_subgroups,
                                                                   dict_list_elements_to_subgroups ):
        self.file.modify_element_ids_in_element_info_file(  dict_group_elements_to_update,
                                                            dict_non_mapped_subgroups,
                                                            dict_list_elements_to_subgroups  )

    def create_folders_structural(self, new_folder_name):
        """This method creates the 'imported_data', 'structural' and 'new_folder_name' folders 
            in the project's directory if they do not exist yet.
        """
        if not os.path.exists(self.file._imported_data_folder_path):
            create_new_folder(self.file._project_path, "imported_data")
        if not os.path.exists(self.file._structural_imported_data_folder_path):
            create_new_folder(self.file._imported_data_folder_path, "structural")   
        new_path = get_new_path(self.file._structural_imported_data_folder_path, new_folder_name)
        if not os.path.exists(new_path):
            create_new_folder(self.file._structural_imported_data_folder_path, new_folder_name)

    def create_folders_acoustic(self, new_folder_name):
        """ This method creates the 'imported_data', 'acoustic' and 'new_folder_name' folders 
            in the project's directory if they do not exist yet.
        """
        if not os.path.exists(self.file._imported_data_folder_path):
            create_new_folder(self.file._project_path, "imported_data")
        if not os.path.exists(self.file._acoustic_imported_data_folder_path):
            create_new_folder(self.file._imported_data_folder_path, "acoustic")   
        new_path = get_new_path(self.file._acoustic_imported_data_folder_path, new_folder_name)
        if not os.path.exists(new_path):
            create_new_folder(self.file._acoustic_imported_data_folder_path, new_folder_name)
                    
    def remove_file_or_folder_from_project_directory(self, filename, folder_name=""):
        if folder_name != "":
            path = get_new_path(self.file._imported_data_folder_path, folder_name)
        else:
            path = self.file._imported_data_folder_path
        list_filenames = os.listdir(path).copy()
        if filename in list_filenames:
            file_path = get_new_path(path, filename)
            if os.path.exists(file_path):
                if "." in filename:
                    os.remove(file_path)
                else:
                    rmtree(file_path)

    def remove_structural_table_files_from_folder(self, filename, folder_name, remove_empty_files=True):
        _folder_path = get_new_path(self.file._structural_imported_data_folder_path, folder_name)
        if os.path.exists(_folder_path):
            list_filenames = os.listdir(_folder_path).copy()
            if filename in list_filenames:
                file_path = get_new_path(_folder_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

        if remove_empty_files:
            if os.path.exists(_folder_path):
                list_filenames = os.listdir(_folder_path).copy()
                if len(list_filenames) == 0:
                    rmtree(_folder_path)
                structural_folders = os.listdir(self.file._structural_imported_data_folder_path).copy()
                if len(structural_folders) == 0:
                    rmtree(self.file._structural_imported_data_folder_path)
                base_folders = os.listdir(self.file._imported_data_folder_path).copy()
                if len(base_folders) == 0:
                    rmtree(self.file._imported_data_folder_path)

    def remove_acoustic_table_files_from_folder(self, filename, folder_name, remove_empty_files=True):
        _folder_path = get_new_path(self.file._acoustic_imported_data_folder_path, folder_name)
        if os.path.exists(_folder_path):
            list_filenames = os.listdir(_folder_path).copy()
            if filename in list_filenames:
                file_path = get_new_path(_folder_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

        if remove_empty_files:
            if os.path.exists(_folder_path):
                list_filenames = os.listdir(_folder_path).copy()
                if len(list_filenames) == 0:
                    rmtree(_folder_path)
                acoustic_folders = os.listdir(self.file._acoustic_imported_data_folder_path).copy()
                if len(acoustic_folders) == 0:
                    rmtree(self.file._acoustic_imported_data_folder_path)
                base_folders = os.listdir(self.file._imported_data_folder_path).copy()
                if len(base_folders) == 0:
                    rmtree(self.file._imported_data_folder_path)

    def remove_structural_empty_folders(self, folder_name=""):
        if folder_name != "":
            folder_path = get_new_path(self.file._structural_imported_data_folder_path, folder_name)
        else:
            folder_path = self.file._structural_imported_data_folder_path
        if os.path.exists(folder_path):
            list_filenames = os.listdir(folder_path).copy()
            if len(list_filenames) == 0:
                rmtree(folder_path)
            structural_folders = os.listdir(self.file._structural_imported_data_folder_path).copy()
            if len(structural_folders) == 0:
                rmtree(self.file._structural_imported_data_folder_path)
            base_folders = os.listdir(self.file._imported_data_folder_path).copy()
            if len(base_folders) == 0:
                rmtree(self.file._imported_data_folder_path)

    def remove_acoustic_empty_folders(self, folder_name=""):
        if folder_name != "":
            folder_path = get_new_path(self.file._acoustic_imported_data_folder_path, folder_name)
        else:
            folder_path = self.file._acoustic_imported_data_folder_path
        if os.path.exists(folder_path):
            list_filenames = os.listdir(folder_path).copy()
            if len(list_filenames) == 0:
                rmtree(folder_path)
            acoustic_folders = os.listdir(self.file._acoustic_imported_data_folder_path).copy()
            if len(acoustic_folders) == 0:
                rmtree(self.file._acoustic_imported_data_folder_path)
            base_folders = os.listdir(self.file._imported_data_folder_path).copy()
            if len(base_folders) == 0:
                rmtree(self.file._imported_data_folder_path)

    def set_entity(self, tag):
        return Entity(tag)

    def load_entity_file(self):
        self.loader = LoadProjectData()
        self.loader.load_entity_file()

    def process_cross_sections_mapping(self):  

        label_etypes = ['pipe_1', 'valve']
        indexes = [0, 1]

        dict_etype_index = dict(zip(label_etypes,indexes))
        dict_index_etype = dict(zip(indexes,label_etypes))
        map_cross_section_to_elements = defaultdict(list)

        for index, element in self.preprocessor.structural_elements.items():

            # if None not in [element.first_node.cross_section, element.last_node.cross_section]:
            #     continue

            if element.variable_section:
                continue

            e_type  = element.element_type
            if e_type in ['beam_1', 'expansion_joint']:
                continue

            elif e_type is None:
                e_type = 'pipe_1'
                self.acoustic_analysis = True
        
            index_etype = dict_etype_index[e_type]

            poisson = element.material.poisson_ratio
            if poisson is None:
                poisson = 0

            outer_diameter = element.cross_section.outer_diameter
            thickness = element.cross_section.thickness
            offset_y = element.cross_section.offset_y
            offset_z = element.cross_section.offset_z
            insulation_thickness = element.cross_section.insulation_thickness
            insulation_density = element.cross_section.insulation_density
           
            map_cross_section_to_elements[str([ outer_diameter, thickness, offset_y, offset_z, poisson,
                                                index_etype, insulation_thickness, insulation_density ])].append(index)
            
            if self.preprocessor.stop_processing:
                return

        for key, elements in map_cross_section_to_elements.items():

            cross_strings = key[1:-1].split(',')
            vals = [float(value) for value in cross_strings]
            el_type = dict_index_etype[vals[5]]

            section_parameters = [vals[0], vals[1], vals[2], vals[3], vals[6], vals[7]]

            if el_type == 'pipe_1':
                pipe_section_info = {   "section_type_label" : "Pipe section",
                                        "section_parameters" : section_parameters   }   
                cross_section = CrossSection(pipe_section_info = pipe_section_info)                             

            elif el_type == 'valve':
                valve_section_info = {  "section_type_label" : "Valve section",
                                        "section_parameters" : section_parameters,  
                                        "diameters_to_plot" : [None, None] }
                cross_section = CrossSection(valve_section_info = valve_section_info)            

            if self.preprocessor.stop_processing:
                return

            # if self.analysis_ID in [3, 4]:
            #     self.preprocessor.set_cross_section_by_element(elements, 
            #                                                    cross_section, 
            #                                                    update_cross_section = False, 
            #                                                    update_section_points = False)  
            # else:
            #     self.preprocessor.set_cross_section_by_element(elements, 
            #                                                    cross_section, 
            #                                                    update_cross_section = True, 
            #                                                    update_section_points = False)

            self.preprocessor.set_cross_section_by_element(
                                                            elements, 
                                                            cross_section, 
                                                            update_cross_section = True, 
                                                            update_section_points = False
                                                            )  

    def get_dict_multiple_cross_sections_from_line(self, line_id):
        '''This methods returns a dictionary of multiples cross-sections associated to 
            the line of interest.        
        '''
        label_etypes = ['pipe_1']
        indexes = [0]
        dict_etype_index = dict(zip(label_etypes,indexes))

        dict_multiple_cross_sections = defaultdict(list)
        list_elements_from_line = list(self.preprocessor.line_to_elements[line_id])
        
        elements = self.preprocessor.structural_elements
        count_sections = 0
        single_cross = False

        for element_id in list_elements_from_line:

            element = elements[element_id]
            e_type  = element.element_type
            if e_type in ['beam_1', 'expansion_joint', 'valve', None]:
                continue
            
            index_etype = dict_etype_index[e_type]
            cross_section = elements[element_id].cross_section
            if cross_section:
                outer_diameter = cross_section.outer_diameter
                thickness = cross_section.thickness
                offset_y = cross_section.offset_y
                offset_z = cross_section.offset_z
                insultation_thickness = cross_section.insulation_thickness
                insultation_density = cross_section.insulation_density
                key_string = str([  outer_diameter, 
                                    thickness, 
                                    offset_y, 
                                    offset_z, 
                                    insultation_thickness, 
                                    insultation_density,
                                    index_etype ])

                if key_string not in list(dict_multiple_cross_sections.keys()):
                    count_sections += 1

                dict_multiple_cross_sections[key_string].append(element_id)

        self.number_sections_by_line[line_id] = count_sections

        if len(dict_multiple_cross_sections) == 1:
            if count_sections == 1:
                list_elements_from_cross_section = dict_multiple_cross_sections[key_string]
                if list_elements_from_cross_section == list_elements_from_line:
                    _element_type = elements[element_id].element_type
                    self.set_structural_element_type_by_lines(line_id, _element_type)
                    _cross_section = elements[element_id].cross_section
                    self.set_cross_section_by_lines(line_id, _cross_section)
                    if line_id in self.number_sections_by_line.keys():
                        self.number_sections_by_line.pop(line_id)
                    single_cross = True 

        return dict_multiple_cross_sections, single_cross   

    def load_structural_bc_file(self):

        title = "ERROR WHILE LOADING STRUCTURAL DATA"
        bc_data = self.file.get_structural_bc_data_from_dat_file()

        for key, values_pd in bc_data["prescribed_dofs"].items():
            frequency_setup_pass = True
            [prescribed_dofs, dofs_tables, dofs_list_freq] = values_pd
            if isinstance(prescribed_dofs, list):
                try:
                    for i, dofs_freq in enumerate(dofs_list_freq):
                        if dofs_freq is not None:
                            if self.change_project_frequency_setup(dofs_tables[i], dofs_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_prescribed_dofs_bc_by_node(key, [prescribed_dofs, dofs_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading prescribed dofs data. \n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message])

        for key, values_nl in bc_data["nodal_loads"].items():
            frequency_setup_pass = True
            [nodal_loads, nodal_loads_tables, nodal_loads_list_freq] = values_nl
            if isinstance(nodal_loads, list):
                try:
                    for i, nodal_loads_freq in enumerate(nodal_loads_list_freq):
                        if nodal_loads_freq is not None:
                            if self.change_project_frequency_setup(nodal_loads_tables[i], nodal_loads_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_structural_loads_by_node(key, [nodal_loads, nodal_loads_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading nodal loads data. \n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message])

        for key, values_li in bc_data["lumped_inertia"].items():
            frequency_setup_pass = True
            [lumped_inertia, lumped_inertia_tables, lumped_inertia_list_freq] = values_li
            if isinstance(lumped_inertia, list):
                try:
                    for i, lumped_inertia_freq in enumerate(lumped_inertia_list_freq):
                        if lumped_inertia_freq is not None:
                            if self.change_project_frequency_setup(lumped_inertia_tables[i], lumped_inertia_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_mass_by_node(key, [lumped_inertia, lumped_inertia_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading lumped masses/moments of inertia data.\n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message])
                
        for key, values_ls in bc_data["lumped_stiffness"].items():
            frequency_setup_pass = True
            [lumped_stiffness, lumped_stiffness_tables, lumped_stiffness_list_freq] = values_ls
            if isinstance(lumped_stiffness, list):
                try:
                    for i, lumped_stiffness_freq in enumerate(lumped_stiffness_list_freq):
                        if lumped_stiffness_freq is not None:
                            if self.change_project_frequency_setup(lumped_stiffness_tables[i], lumped_stiffness_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_spring_by_node(key, [lumped_stiffness, lumped_stiffness_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading lumped stiffness data.\n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message])  

        for key, values_ld in bc_data["lumped_damping"].items():
            frequency_setup_pass = True
            [lumped_dampings, lumped_damping_tables, lumped_damping_list_freq] = values_ld
            if isinstance(lumped_dampings, list):
                try:
                    for i, lumped_damping_freq in enumerate(lumped_damping_list_freq):
                        if lumped_damping_freq is not None:
                            if self.change_project_frequency_setup(lumped_damping_tables[i], lumped_damping_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_damper_by_node(key, [lumped_dampings, lumped_damping_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading lumped damping data.\n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message]) 

        for key, values_els in bc_data["elastic_link_stiffness"].items():
            frequency_setup_pass = True
            [stiffness_data, elastic_link_stiffness_tables, connecting_stiffness_list_freq] = values_els
            if isinstance(stiffness_data, list):
                print(key)
                nodes = [int(node) for node in key.split("-")]
                try:
                    for i, connecting_stiffness_freq in enumerate(connecting_stiffness_list_freq):
                        if connecting_stiffness_freq is not None:
                            if self.change_project_frequency_setup(elastic_link_stiffness_tables[i], connecting_stiffness_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_elastic_nodal_link_stiffness(nodes, [stiffness_data, elastic_link_stiffness_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading elastic nodal link stiffness data.\n\n"
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message]) 

        for key, values_eld in bc_data["elastic_link_damping"].items():
            frequency_setup_pass = True
            [damping_data, elastic_link_damping_tables, connecting_damping_list_freq] = values_eld
            if isinstance(damping_data, list):
                nodes = [int(node) for node in key.split("-")]
                try:
                    for i, connecting_damping_freq in enumerate(connecting_damping_list_freq):
                        if connecting_damping_freq is not None:
                            if self.change_project_frequency_setup(elastic_link_damping_tables[i], connecting_damping_freq):
                                frequency_setup_pass = False
                                break
                    if frequency_setup_pass:
                        self.load_elastic_nodal_link_damping(nodes, [damping_data, elastic_link_damping_tables])
                except Exception as log_error:
                    message = "An error has occurred while loading elastic nodal link damping data.\n\n" 
                    message += str(log_error)
                    PrintMessageInput([window_title, title, message]) 

    def load_acoustic_bc_file(self):

        # bc_data = self.file.get_acoustic_bc_data_from_file()
        bc_data = self.file.get_acoustic_bc_data_from_dat_file()

        for key, [ActPres, ActPres_table_name, ActPres_freq] in bc_data["acoustic_pressure"].items():
            if ActPres_table_name is not None:
                if self.change_project_frequency_setup(ActPres_table_name, ActPres_freq):
                    continue
            if ActPres is not None:
                self.load_acoustic_pressure_bc_by_node(key, [ActPres, ActPres_table_name])

        for key, [VelVol, VelVol_table_name, VelVol_freq] in bc_data["volume_velocity"].items():
            if VelVol_table_name is not None:
                if self.change_project_frequency_setup(VelVol_table_name, VelVol_freq):
                    continue  
            if VelVol is not None:
                self.load_volume_velocity_bc_by_node(key, [VelVol, VelVol_table_name])
  
        for key, data in bc_data["compressor_excitation"].items():
            for [CompExcit, CompExcit_table_name, connection_info, CompExcit_freq] in data:
                if CompExcit_table_name is not None:
                    if self.change_project_frequency_setup(CompExcit_table_name, CompExcit_freq):
                        continue 
                if CompExcit is not None:
                    self.load_compressor_excitation_bc_by_node(key, [CompExcit, CompExcit_table_name], connection_info)  

        for key, [SpecImp, SpecImp_table_name, SpecImp_freq] in bc_data["specific_impedance"].items():
            if SpecImp_table_name is not None:
                if self.change_project_frequency_setup(SpecImp_table_name, SpecImp_freq):
                    continue 
            if SpecImp is not None:
                self.load_specific_impedance_bc_by_node(key, [SpecImp, SpecImp_table_name])

        for key, RadImp in bc_data["radiation_impedance"].items():
            if RadImp is not None:
                self.load_radiation_impedance_bc_by_node(key, RadImp)

    def load_analysis_file(self):
        self.f_min, self.f_max, self.f_step, self.global_damping = self.file.load_analysis_file()

    def load_inertia_load_setup(self):
        gravity, stiffening_effect = self.file.load_inertia_load_setup()
        self.preprocessor.set_inertia_load(gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)

    def load_frequencies_from_table(self):
        self.f_min, self.f_max, self.f_step = self.file.f_min, self.file.f_max, self.file.f_step
        self.frequencies = self.file.frequencies 

    def change_project_frequency_setup(self, table_name, frequencies):
        if frequencies is None:
            return False
        if isinstance(frequencies, np.ndarray):
            frequencies = list(frequencies)
        updated = False
        if self.list_frequencies == list() or not self.file.check_if_there_are_tables_at_the_model():
            updated = True
            self.list_frequencies = frequencies
        if self.list_frequencies == frequencies:
            if updated:
                self.frequencies = np.array(frequencies)
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.file.add_frequency_in_file(self.f_min, self.f_max, self.f_step)
                self.imported_table_frequency_setup = True
            return False
        else:
            title = "Project frequency setup cannot be modified"
            message = f"The following imported table of values has a frequency setup\n"
            message += "different from the others already imported ones. The current\n"
            message += "project frequency setup is not going to be modified."
            message += f"\n\n{table_name}"
            PrintMessageInput([window_title, title, message])
            return True

    def set_material_to_all_lines(self, material):
        self.preprocessor.set_material_by_element('all', material)
        self._set_material_to_all_lines(material)
        self.file.add_material_in_file(self.preprocessor.all_lines, material)

    def set_material_by_lines(self, lines, material):
        self.preprocessor.set_material_by_lines(lines, material)
        self._set_material_to_selected_lines(lines, material)
        self.file.add_material_in_file(lines, material)

    def set_variable_cross_section_by_line(self, line_id, section_data):
        """
        This method sets the variable section info by line selection.
        """
        if section_data:

            [   outer_diameter_initial, thickness_initial, offset_y_initial, offset_z_initial,
                outer_diameter_final, thickness_final, offset_y_final, offset_z_final,
                insulation_thickness, insulation_density  ] = section_data["section_parameters"]

            elements_from_line = self.preprocessor.line_to_elements[line_id]
            self.preprocessor.add_expansion_joint_by_line(line_id, None, remove=True)

            first_element = self.preprocessor.structural_elements[elements_from_line[0]]
            last_element = self.preprocessor.structural_elements[elements_from_line[-1]]
            
            coord_first_1 = first_element.first_node.coordinates
            coord_last_1 = last_element.last_node.coordinates
            
            coord_first_2 = last_element.first_node.coordinates
            coord_last_2 = first_element.last_node.coordinates
            
            lines_vertex_coords = self.preprocessor.get_lines_vertex_coordinates(_array=False)
            vertex_coords = lines_vertex_coords[line_id]

            N = len(elements_from_line)
            if list(coord_first_1) in vertex_coords and list(coord_last_1) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_initial, outer_diameter_final, N)
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_initial, thickness_final, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_initial, offset_y_final, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_initial, offset_z_final, N)

            elif list(coord_first_2) in vertex_coords and list(coord_last_2) in vertex_coords:
                outer_diameter_first, outer_diameter_last = get_linear_distribution_for_variable_section(outer_diameter_final, outer_diameter_initial, N)
                thickness_first, thickness_last = get_linear_distribution_for_variable_section(thickness_final, thickness_initial, N)
                offset_y_first, offset_y_last = get_linear_distribution_for_variable_section(offset_y_final, offset_y_initial, N)
                offset_z_first, offset_z_last = get_linear_distribution_for_variable_section(offset_z_final, offset_z_initial, N)
            
            cross_sections_first = list()
            cross_sections_last = list()
            for index, element_id in enumerate(elements_from_line):
                
                element = self.preprocessor.structural_elements[element_id]
                first_node = element.first_node
                last_node = element.last_node
                
                section_parameters_first = [outer_diameter_first[index],
                                            thickness_first[index],
                                            offset_y_first[index],
                                            offset_z_first[index],
                                            insulation_thickness,
                                            insulation_density]
                
                pipe_section_info_first = { "section_type_label" : "Pipe section" ,
                                            "section_parameters" : section_parameters_first }

                section_parameters_last = [outer_diameter_last[index],
                                            thickness_last[index],
                                            offset_y_last[index],
                                            offset_z_last[index],
                                            insulation_thickness,
                                            insulation_density]
                
                pipe_section_info_last = { "section_type_label" : "Pipe section" ,
                                            "section_parameters" : section_parameters_last }

                cross_section_first = CrossSection(pipe_section_info = pipe_section_info_first)
                cross_section_last = CrossSection(pipe_section_info = pipe_section_info_last)

                cross_sections_first.append(cross_section_first)
                # cross_sections_last.append(cross_section_last)

                first_node.cross_section = cross_section_first
                last_node.cross_section = cross_section_last

            self.set_cross_section_by_elements( elements_from_line,
                                                cross_sections_first,
                                                remesh_mapping = False,
                                                variable_section = True )
        
    def set_cross_section_by_lines(self, lines, cross_section):
        """
        """
        self.preprocessor.add_expansion_joint_by_line(lines, None, remove=True)
        self.preprocessor.set_cross_section_by_lines(lines, cross_section)
        self._set_cross_section_to_selected_line(lines, cross_section)
        self.file.add_cross_section_in_file(lines, cross_section)

    def set_cross_section_by_elements(self, list_elements, cross_section, remesh_mapping=True, variable_section=False):
        """
        """
        if remesh_mapping:
            self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(list_elements)
        self.preprocessor.set_cross_section_by_element(list_elements, cross_section, variable_section=variable_section)       
        # for element in list_elements:
        #     line = self.preprocessor.elements_to_line[element]
        #     if line not in self.lines_with_cross_section_by_elements:
        #         self.lines_with_cross_section_by_elements.append(line)

    def reset_number_sections_by_line(self, line_id):
        if line_id in list(self.number_sections_by_line.keys()):
            self.number_sections_by_line.pop(line_id)

    def add_cross_sections_expansion_joints_valves_in_file(self, list_elements):
        list_lines = list()
        for element_id in list_elements:
            line_id = self.preprocessor.elements_to_line[element_id]
            if line_id not in list_lines:
                list_lines.append(line_id)
        for _line_id in list_lines:
            map_expansion_joints_to_elements = dict()
            map_valves_to_elements = dict()
            map_cross_sections_to_elements, single_cross = self.get_dict_multiple_cross_sections_from_line(_line_id)
            if not single_cross:
                  
                map_expansion_joints_to_elements = self.get_map_expansion_joints_to_elements(_line_id)
                map_valves_to_elements = self.get_map_valves_to_elements(_line_id)

                self.file.add_multiple_cross_sections_expansion_joints_valves_in_file(  _line_id, 
                                                                                        map_cross_sections_to_elements, 
                                                                                        map_expansion_joints_to_elements,
                                                                                        map_valves_to_elements )  
                
                for list_elements_mapped in map_cross_sections_to_elements.values():
                    self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(list_elements_mapped)
    
    def set_structural_element_type_to_all(self, element_type):
        self.preprocessor.set_structural_element_type_by_element('all', element_type)
        self._set_structural_element_type_to_all_lines(element_type)
        self.file.modify_structural_element_type_in_file(self.preprocessor.all_lines, element_type)

    def set_structural_element_type_by_lines(self, lines, element_type):
        self.preprocessor.set_structural_element_type_by_lines(lines, element_type)
        self._set_structural_element_type_to_selected_lines(lines, element_type)
        self.file.modify_structural_element_type_in_file(lines, element_type)
        
    def set_acoustic_element_type_by_lines(self, lines, element_type, proportional_damping = None, vol_flow = None):

        self.preprocessor.set_acoustic_element_type_by_lines(lines, element_type, 
                                                             proportional_damping = proportional_damping, 
                                                             vol_flow = vol_flow)

        self._set_acoustic_element_type_to_selected_lines(lines, element_type, 
                                                          proportional_damping = proportional_damping, 
                                                          vol_flow = vol_flow)

        self.file.modify_acoustic_element_type_in_file(lines, element_type, 
                                                       proportional_damping = proportional_damping, 
                                                       vol_flow = vol_flow)

    def set_beam_xaxis_rotation_by_line(self, line_id, delta_angle):
        self.preprocessor.set_beam_xaxis_rotation_by_line(line_id, delta_angle)
        angle = self.preprocessor.dict_lines_to_rotation_angles[line_id]
        self._set_beam_xaxis_rotation_to_selected_lines(line_id, angle)
        self.file.modify_beam_xaxis_rotation_by_lines_in_file(line_id, angle)

    def set_prescribed_dofs_bc_by_node(self, node_id, data, imported_table):
        [values, table_names] = data
        self.preprocessor.set_prescribed_dofs_bc_by_node(node_id, data)
        labels = ["displacements", "rotations"]
        if imported_table:
            values = table_names
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def set_B2PX_rotation_decoupling(self, element_id, node_id, rotations_mask, remove = False):

        self.preprocessor.set_B2PX_rotation_decoupling( element_id,
                                                        node_id,
                                                        rotations_to_decouple = rotations_mask,
                                                        remove = remove )

        count_add, count_remove = 0, 0
        temp_dict = self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.copy()

        for key, elements in temp_dict.items():
            count_add += 1
            section_key = "B2PX ROTATION DECOUPLING || Selection-{}".format(count_add - count_remove)              
            nodes = self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling[key] 

            if elements != list():   
                self.file.modify_B2PX_rotation_decoupling_in_file(elements = elements, 
                                                                  nodes = nodes, 
                                                                  rotations_maks = key, 
                                                                  section = section_key)
                self.preprocessor.dict_B2PX_rotation_decoupling[key] = [elements, nodes, section_key]

            elif elements == list() or rotations_mask==str([False, False, False]):
                count_remove += 1
                self.file.modify_B2PX_rotation_decoupling_in_file(elements = elements, 
                                                                  nodes = nodes, 
                                                                  rotations_maks = key, 
                                                                  section = section_key, 
                                                                  remove = True)
                self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling.pop(key)
                self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.pop(key)
                self.preprocessor.dict_B2PX_rotation_decoupling.pop(key)

    def reset_B2PX_rotation_decoupling(self):
        N = self.preprocessor.DOFS_ELEMENT
        mat_reset = np.ones((N,N), dtype=int)
        for list_elements in self.preprocessor.dict_elements_with_B2PX_rotation_decoupling.values():
            for element_ID in list_elements:
                element = self.preprocessor.structural_elements[element_ID]
                element.decoupling_matrix = mat_reset
                element.decoupling_info = None
        self.preprocessor.dict_nodes_with_B2PX_rotation_decoupling = dict()
        self.preprocessor.dict_elements_with_B2PX_rotation_decoupling = dict()
        self.file.modify_B2PX_rotation_decoupling_in_file(reset = True)

    def set_nodal_loads_by_node(self, node_id, data, imported_table):
        [values, table_names] = data
        self.preprocessor.set_structural_load_bc_by_node(node_id, data)
        labels = ["forces", "moments"]
        if imported_table:
            values = table_names
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_masses_by_node(self, node_id, data, imported_table):
        [values, table_names] = data
        self.preprocessor.add_mass_to_node(node_id, data)
        labels = ["masses", "moments of inertia"]
        if imported_table:
            values = table_names
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_stiffness_by_node(self, node_id, data, imported_table):
        [values, table_names] = data
        self.preprocessor.add_spring_to_node(node_id, data)
        labels = ["spring stiffness", "torsional spring stiffness"]
        if imported_table:
            values = table_names
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_lumped_dampings_by_node(self, node_id, data, imported_table):
        [values, table_names] = data
        self.preprocessor.add_damper_to_node(node_id, data)
        labels = ["damping coefficients", "torsional damping coefficients"]
        if imported_table:
            values = table_names        
        self.file.add_structural_bc_in_file(node_id, values, labels)

    def add_elastic_nodal_link_stiffness(self, nodeID_1, nodeID_2, parameters, imported_table):
        min_node_ID = min(nodeID_1, nodeID_2)
        max_node_ID = max(nodeID_1, nodeID_2)
        self.preprocessor.add_elastic_nodal_link(min_node_ID, max_node_ID, parameters, _stiffness=True)
        labels = ["connecting stiffness", "connecting torsional stiffness"]
        section_string = ["{}-{}".format(min_node_ID, max_node_ID)]
        if imported_table:
            values = parameters[1]
        else:
            values = parameters[0]
        self.file.add_structural_bc_in_file(section_string, values, labels)

    def add_elastic_nodal_link_damping(self, nodeID_1, nodeID_2, parameters, imported_table):
        min_node_ID = min(nodeID_1, nodeID_2)
        max_node_ID = max(nodeID_1, nodeID_2)
        self.preprocessor.add_elastic_nodal_link(min_node_ID, max_node_ID, parameters, _damping=True)
        labels = ["connecting damping", "connecting torsional damping"]
        section_string = ["{}-{}".format(min_node_ID, max_node_ID)]
        if imported_table:
            values = parameters[1]
        else:
            values = parameters[0]
        self.file.add_structural_bc_in_file(section_string, values, labels)

    def add_valve_by_line(self, line_ids, parameters, reset_cross=True):
        if parameters is None:
            remove = True
            capped = False
            etype = "pipe_1"
        else:
            remove = False
            capped = True
            etype = "valve"

        self.preprocessor.add_expansion_joint_by_line(line_ids, None, remove=True)
        self.preprocessor.add_valve_by_line(line_ids, parameters, remove=remove, reset_cross=reset_cross)
        self.set_capped_end_by_lines(line_ids, capped)
        self.set_structural_element_type_by_lines(line_ids, etype)
        self._set_valve_to_selected_lines(line_ids, parameters)
        
        if reset_cross:

            if etype == "pipe_1":
                self.set_cross_section_by_lines(line_ids, None)  
            
            if isinstance(line_ids, int):
                line_ids = [line_ids]
            for line_id in line_ids:
                if line_id in self.number_sections_by_line.keys():
                    self.number_sections_by_line.pop(line_ids)

            self.file.modify_valve_in_file(line_ids, parameters) 

    def add_valve_by_elements(  self, 
                                list_elements, 
                                parameters,
                                update_element_type = True, 
                                reset_cross = True  ):
                                        
        if parameters is None:
            remove = True
            element_type = "pipe_1"
        else:
            remove = False
            element_type = "valve"

        self.preprocessor.add_valve_by_elements(list_elements, 
                                                parameters, 
                                                remove = remove, 
                                                reset_cross = reset_cross)
        
        if update_element_type:
            self.preprocessor.set_structural_element_type_by_element(list_elements, element_type)

        list_lines = list()
        for element in list_elements:
            line_id = self.preprocessor.elements_to_line[element]
            if line_id not in list_lines:
                list_lines.append(line_id)
                            
        for line_id in list_lines:

            dict_multiple_cross_sections, single_cross = self.get_dict_multiple_cross_sections_from_line(line_id)          

            if not single_cross:

                dict_multiple_expansion_joints = self.get_map_expansion_joints_to_elements(line_id)

                for [parameters_exp_joint, _group_elements_2, _] in dict_multiple_expansion_joints.values():    
                    list_subgroup_elements = check_is_there_a_group_of_elements_inside_list_elements(_group_elements_2)

                    for subgroup_elements in list_subgroup_elements:
                        cross_sections = get_list_cross_sections_to_plot_expansion_joint(subgroup_elements, parameters_exp_joint[0][1])
                        self.preprocessor.set_cross_section_by_element(subgroup_elements, cross_sections)

                self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(   list_elements, 
                                                                                                    reset_line = True, 
                                                                                                    line_id = line_id, 
                                                                                                    dict_map_cross = dict_multiple_cross_sections,
                                                                                                    dict_map_expansion_joint = dict_multiple_expansion_joints )

                elements_from_line = self.preprocessor.line_to_elements[line_id]
                self.add_cross_sections_expansion_joints_valves_in_file( elements_from_line )

    def add_expansion_joint_by_line(self, lines_id, parameters):

        if isinstance(lines_id, int):
            lines_id = [lines_id]

        if parameters is None:
            remove = True
            capped = False
            etype = "pipe_1"
        else:
            remove = False
            capped = True
            etype = "expansion_joint"

        self.preprocessor.add_expansion_joint_by_line(lines_id, parameters, remove=remove)
        self.set_capped_end_by_lines(lines_id, capped)
        self.set_structural_element_type_by_lines(lines_id, etype)
        if etype == "pipe_1":
            self.set_cross_section_by_lines(lines_id, None)  
        self._set_expansion_joint_to_selected_lines(lines_id, parameters)

        for line_id in lines_id:
            if line_id in self.number_sections_by_line.keys():
                self.number_sections_by_line.pop(line_id)

        self.file.modify_expansion_joint_in_file(line_id, parameters)   

    def add_expansion_joint_by_elements(self, 
                                        list_elements, 
                                        parameters,
                                        update_element_type=True, 
                                        reset_cross=True):
                                       
        if parameters is None:
            remove = True
            element_type = "pipe_1"
        else:
            remove = False
            element_type = "expansion_joint"

        self.preprocessor.add_expansion_joint_by_elements(  list_elements, 
                                                            parameters, 
                                                            remove=remove, 
                                                            reset_cross=reset_cross  )
        
        if update_element_type:
            self.preprocessor.set_structural_element_type_by_element(list_elements, element_type)

        list_lines = list()
        for element in list_elements:
            line_id = self.preprocessor.elements_to_line[element]
            if line_id not in list_lines:
                list_lines.append(line_id)
                            
        for line_id in list_lines:

            dict_multiple_cross_sections, single_cross = self.get_dict_multiple_cross_sections_from_line(line_id)
            
            if not single_cross:

                dict_multiple_expansion_joints = self.get_map_expansion_joints_to_elements(line_id)
                for [parameters_exp_joint, _group_elements_2, _] in dict_multiple_expansion_joints.values():    
                    list_subgroup_elements = check_is_there_a_group_of_elements_inside_list_elements(_group_elements_2)
                    for subgroup_elements in list_subgroup_elements:
                        cross_sections = get_list_cross_sections_to_plot_expansion_joint(subgroup_elements, parameters_exp_joint[0][1])
                        self.preprocessor.set_cross_section_by_element(subgroup_elements, cross_sections)
                
                self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(   list_elements, 
                                                                                                    reset_line = True, 
                                                                                                    line_id = line_id, 
                                                                                                    dict_map_cross = dict_multiple_cross_sections,
                                                                                                    dict_map_expansion_joint = dict_multiple_expansion_joints )

                elements_from_line = self.preprocessor.line_to_elements[line_id]
                self.add_cross_sections_expansion_joints_valves_in_file( elements_from_line )                                                

    def get_map_expansion_joints_to_elements(self, line_id):
        structural_elements = self.preprocessor.structural_elements
        dict_multiple_expansion_joints = dict()
        dict_exp_joint_key_parameters_to_parameters = dict()
        dict_exp_joint_key_parameters_to_table_names = dict()
        dict_exp_joint_key_parameters_to_elements = defaultdict(list)
        for element_id in self.preprocessor.line_to_elements[line_id]:
            element = structural_elements[element_id]
            if element.expansion_joint_parameters:
                dict_exp_joint_key_parameters_to_elements[str(element.expansion_joint_parameters)].append(element_id)
                dict_exp_joint_key_parameters_to_parameters[str(element.expansion_joint_parameters)] = element.expansion_joint_parameters
                dict_exp_joint_key_parameters_to_table_names[str(element.expansion_joint_parameters)] = element.joint_stiffness_table_names
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
        for element_id in self.preprocessor.line_to_elements[line_id]:
            element = structural_elements[element_id]
            if element.valve_parameters:
                dict_valve_key_parameters_to_elements[str(element.valve_parameters)].append(element_id)
                dict_valve_key_parameters_to_parameters[str(element.valve_parameters)] = element.valve_parameters
        for ind, (key_parameters, _group_elements) in enumerate(dict_valve_key_parameters_to_elements.items()):
            section_key = f"{line_id}-{ind + 1}"
            parameters_valve = dict_valve_key_parameters_to_parameters[key_parameters]
            dict_multiple_valves[section_key] = [parameters_valve, _group_elements]
        return dict_multiple_valves

    def set_stress_stiffening_by_elements(self, elements, parameters, section, remove=False):
        self.preprocessor.set_stress_stiffening_by_elements(elements, parameters, section=section, remove=remove)
        self.file.modify_stress_stiffnening_element_in_file(elements, parameters, section, remove=remove)

    def set_stress_stiffening_by_line(self, lines, parameters, remove=False):
        
        if isinstance(lines, int):
            lines = [lines]
        
        self.preprocessor.set_stress_stiffening_by_line(lines, parameters, remove=remove)          
        if remove:
            self._set_stress_stiffening_to_selected_lines(lines, [None, None, None, None])
            self.file.modify_stress_stiffnening_line_in_file(lines, [], remove=True)
        else:
            self._set_stress_stiffening_to_selected_lines(lines, parameters)
            self.file.modify_stress_stiffnening_line_in_file(lines, parameters)

    def load_material_by_line(self, line_id, material):
        self.preprocessor.set_material_by_lines(line_id, material)
        self._set_material_to_selected_lines(line_id, material)
    
    def load_stress_stiffening_by_elements(self, elements_id, parameters, section=None):
        self.preprocessor.set_stress_stiffening_by_elements(elements_id, parameters, section=section)

    def load_stress_stiffening_by_line(self, line_id, parameters):
        self.preprocessor.set_stress_stiffening_by_line(line_id, parameters)
        self._set_stress_stiffening_to_selected_lines(line_id, parameters)

    def load_fluid_by_line(self, line_id, fluid):
        self.preprocessor.set_fluid_by_lines(line_id, fluid)
        self._set_fluid_to_selected_lines(line_id, fluid)

    def load_compressor_info_by_line(self, line_id, compressor_info):
        self._set_compressor_info_to_selected_lines(line_id, compressor_info=compressor_info)

    def load_cross_section_by_element(self, list_elements, cross_section):
        self.set_cross_section_by_elements(list_elements, cross_section)

    def load_cross_section_by_line(self, line_id, cross_section):
        self.preprocessor.set_cross_section_by_lines(line_id, cross_section)
        self._set_cross_section_to_selected_line(line_id, cross_section)

    def load_variable_cross_section_by_line(self, line_id, data):
        self._set_variable_cross_section_to_selected_line(line_id, data)
        self.set_variable_cross_section_by_line(line_id, data)

    def load_expansion_joint_by_lines(self, line_id, data):
        joint_elements = self.preprocessor.line_to_elements[line_id]
        cross_sections = get_list_cross_sections_to_plot_expansion_joint(joint_elements, data[0][1])
        self._set_cross_section_to_selected_line(line_id, cross_sections[0])
        self.preprocessor.add_expansion_joint_by_line(line_id, data)
        self._set_expansion_joint_to_selected_lines(line_id, data)
        self.preprocessor.set_cross_section_by_element(joint_elements, cross_sections)

    def load_expansion_joint_by_elements(self, joint_elements, data):
        self.preprocessor.add_expansion_joint_by_elements(joint_elements, data)
        self.preprocessor.process_elements_to_update_indexes_after_remesh_in_entity_file(joint_elements)
        cross_sections = get_list_cross_sections_to_plot_expansion_joint(joint_elements, data[0][1])
        self.preprocessor.set_cross_section_by_element(joint_elements, cross_sections)

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

    def load_beam_xaxis_rotation_by_line(self, line_id, angle):
        self.preprocessor.set_beam_xaxis_rotation_by_line(line_id, angle)
        self._set_beam_xaxis_rotation_to_selected_lines(line_id, angle)

    def load_structural_element_type_by_line(self, line_id, element_type):
        self.preprocessor.set_structural_element_type_by_lines(line_id, element_type)
        self._set_structural_element_type_to_selected_lines(line_id, element_type)

    def load_structural_element_type_by_elements(self, list_elements, element_type):
        self.preprocessor.set_structural_element_type_by_element(list_elements, element_type)
        # self._set_structural_element_type_to_selected_lines(line_id, element_type)

    def load_structural_element_force_offset_by_line(self, line_id, force_offset):
        self.preprocessor.set_structural_element_force_offset_by_lines(line_id, force_offset)
        self._set_structural_element_force_offset_to_lines(line_id, force_offset)

    def load_structural_element_force_offset_by_elements(self, list_elements, force_offset):
        self.preprocessor.set_structural_element_force_offset_by_elements(list_elements, force_offset)

    def load_structural_element_wall_formulation_by_line(self, line_id, formulation):
        self.preprocessor.set_structural_element_wall_formulation_by_lines(line_id, formulation)
        self._set_structural_element_wall_formulation_to_lines(line_id, formulation)

    def load_structural_element_wall_formulation_by_elements(self, list_elements, wall_formulation):
        self.preprocessor.set_structural_element_wall_formulation_by_elements(list_elements, wall_formulation)

    def load_acoustic_element_type_by_line(self, line_id, element_type, proportional_damping=None, vol_flow=None):
        self.preprocessor.set_acoustic_element_type_by_lines(line_id, 
                                                             element_type, 
                                                             proportional_damping = proportional_damping, 
                                                             vol_flow = vol_flow)
        self._set_acoustic_element_type_to_selected_lines(line_id, 
                                                          element_type,
                                                          proportional_damping = proportional_damping, 
                                                          vol_flow = vol_flow)

    def load_structural_loads_by_node(self, node_id, data):
        self.preprocessor.set_structural_load_bc_by_node(node_id, data)

    def load_mass_by_node(self, node_id, data):
        self.preprocessor.add_mass_to_node(node_id, data)

    def load_spring_by_node(self, node_id, data):
        self.preprocessor.add_spring_to_node(node_id, data)

    def load_damper_by_node(self, node_id, data):
        self.preprocessor.add_damper_to_node(node_id, data)

    def load_elastic_nodal_link_stiffness(self, nodes, data):
        self.preprocessor.add_elastic_nodal_link(nodes[0], nodes[1], data, _stiffness=True)
    
    def load_elastic_nodal_link_damping(self, nodes, data):
        self.preprocessor.add_elastic_nodal_link(nodes[0], nodes[1], data, _damping=True)

    def load_B2PX_rotation_decoupling(self, element_ID, node_ID, rotations_to_decouple):
        self.preprocessor.set_B2PX_rotation_decoupling(element_ID, node_ID, rotations_to_decouple=rotations_to_decouple)
    
    def load_capped_end_by_elements(self, elements, value, selection):
        self.preprocessor.set_capped_end_by_elements(elements, value, selection)

    def load_capped_end_by_line(self, lines, value):
        self.preprocessor.set_capped_end_by_lines(lines, value)
        self._set_capped_end_to_lines(lines, value)

    def get_nodes_bc(self):
        return self.preprocessor.nodes_with_prescribed_dofs

    def get_structural_elements(self):
        return self.preprocessor.structural_elements
    
    def get_structural_element(self, element_id):
        return self.preprocessor.structural_elements[element_id]

    def get_acoustic_elements(self):
        return self.preprocessor.acoustic_elements 

    def get_acoustic_element(self, element_id):
        return self.preprocessor.acoustic_elements[element_id]

    def set_frequencies(self, frequencies, min_, max_, step_):
        if max_ != 0 and step_ != 0:
            self.f_min, self.f_max, self.f_step = min_, max_, step_
            self.file.add_frequency_in_file(min_, max_, step_)
        self.frequencies = frequencies
    
    def set_static_analysis_setup(self, analysis_setup):
        [self.weight_load, 
         self.internal_pressure_load,
         self.external_nodal_loads,
         self.element_distributed_load] = analysis_setup

    def load_prescribed_dofs_bc_by_node(self, node_id, data):
        self.preprocessor.set_prescribed_dofs_bc_by_node(node_id, data)

    def _set_material_to_selected_lines(self, lines, material):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.material = material

    def _set_material_to_all_lines(self, material):
        for entity in self.preprocessor.dict_tag_to_entity.values():
            entity.material = material

    def _set_fluid_to_selected_lines(self, lines, fluid):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            if entity.structural_element_type in ['beam_1']:
                entity.fluid = None
            else:
                entity.fluid = fluid    

    def _set_compressor_info_to_selected_lines(self, lines, compressor_info={}):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            if compressor_info:
                if entity.structural_element_type in ['beam_1']:
                    entity.compressor_info =  {}
                else:  
                    entity.compressor_info = compressor_info 
            else:
                if entity.compressor_info:
                    node_id = entity.compressor_info['node_id']
                    self.remove_compressor_excitation_table_files([node_id])
                    self.preprocessor.set_compressor_excitation_bc_by_node([node_id], [None, None])
                    entity.compressor_info = dict()

    def _set_fluid_to_all_lines(self, fluid):
        for entity in self.preprocessor.dict_tag_to_entity.values():
            if entity.structural_element_type in ['beam_1']:
                entity.fluid = None
            else:
                entity.fluid = fluid               

    def _set_cross_section_to_selected_line(self, lines, cross):

        if isinstance(lines, int):
            lines = [lines]

        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.cross_section = cross
            entity.valve_parameters = None
            entity.expansion_joint_parameters = None
            entity.variable_cross_section_data = None

    def _set_variable_cross_section_to_selected_line(self, line_id, section_info):
        entity = self.preprocessor.dict_tag_to_entity[line_id]
        entity.cross_section = None
        entity.variable_cross_section_data = section_info

    def _set_structural_element_type_to_selected_lines(self, lines, element_type):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.structural_element_type = element_type

    def _set_structural_element_type_to_all_lines(self, element_type):
        for entity in self.preprocessor.dict_tag_to_entity.values():
            entity.structural_element_type = element_type

    def _set_acoustic_element_type_to_selected_lines(self, lines, element_type, proportional_damping=None, vol_flow=None):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.acoustic_element_type = element_type
            entity.proportional_damping = proportional_damping
            entity.vol_flow = vol_flow

    def _set_acoustic_element_type_to_all_lines(self, element_type, proportional_damping=None):
        for entity in self.preprocessor.dict_tag_to_entity.values(): 
            entity.acoustic_element_type = element_type
            entity.proportional_damping = proportional_damping

    def _set_beam_xaxis_rotation_to_selected_lines(self, line_id, angle):
        entity = self.preprocessor.dict_tag_to_entity[line_id]
        entity.xaxis_beam_rotation = angle

    def _set_stress_stiffening_to_selected_lines(self, lines, pressures):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.stress_stiffening_parameters = pressures
            
    # def _set_stress_stiffening_to_all_entities(self, pressures):
    #     for entity in self.preprocessor.dict_tag_to_entity.values():
    #         entity.external_pressure = pressures[0]
    #         entity.internal_pressure = pressures[1]

    def _set_expansion_joint_to_selected_lines(self, lines, parameters):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.expansion_joint_parameters = parameters

    def _set_valve_to_selected_lines(self, lines, parameters):
        if isinstance(lines, int):
            lines = [lines]
        for line_id in lines:
            entity = self.preprocessor.dict_tag_to_entity[line_id]
            entity.valve_parameters = parameters

    def get_nodes_with_prescribed_dofs_bc(self):
        return self.preprocessor.nodes_with_prescribed_dofs

    def set_fluid_by_lines(self, lines, fluid):
        self.preprocessor.set_fluid_by_lines(lines, fluid)
        self._set_fluid_to_selected_lines(lines, fluid)
        self.file.add_fluid_in_file(lines, fluid)

    def set_compressor_info_by_lines(self, lines, compressor_info={}):
        self.file.modify_compressor_info_in_file(lines, compressor_info=compressor_info)
        self._set_compressor_info_to_selected_lines(lines, compressor_info=compressor_info)

    def reset_compressor_info_by_node(self, node_id):
        line_id = self.preprocessor.get_line_from_node_id(node_id)
        self.set_compressor_info_by_lines(line_id, compressor_info={})

    def set_fluid_to_all_lines(self, fluid):
        self.preprocessor.set_fluid_by_element('all', fluid)
        self._set_fluid_to_all_lines(fluid)
        for line in self.preprocessor.all_lines:
            self.file.add_fluid_in_file(line, fluid)

    def set_acoustic_pressure_bc_by_node(self, node_ids, data):
        label = ["acoustic pressure"]
        if self.preprocessor.set_acoustic_pressure_bc_by_node(node_ids, data):
            return
        self.file.add_acoustic_bc_in_file(node_ids, data, label) 

    def set_volume_velocity_bc_by_node(self, node_ids, data):
        label = ["volume velocity"]
        if self.preprocessor.set_volume_velocity_bc_by_node(node_ids, data):
            return True
        self.file.add_acoustic_bc_in_file(node_ids, data, label)
    
    def set_specific_impedance_bc_by_node(self, node_ids, data):
        label = ["specific impedance"]
        if self.preprocessor.set_specific_impedance_bc_by_node(node_ids, data):
            return
        self.file.add_acoustic_bc_in_file(node_ids, data, label) 

    def set_radiation_impedance_bc_by_node(self, node_ids, data):
        label = ["radiation impedance"] 
        if self.preprocessor.set_radiation_impedance_bc_by_node(node_ids, data):
            return
        self.file.add_acoustic_bc_in_file(node_ids, [data, None], label)
    
    def set_compressor_excitation_bc_by_node(self, node_ids, data, table_index, connection_info):
        label = [f"compressor excitation - {table_index}"]
        for node_id in node_ids:
            if self.preprocessor.set_compressor_excitation_bc_by_node([node_id], data, connection_info):
                return True
            self.file.add_acoustic_bc_in_file([node_id], data, label)
        return False

    def remove_acoustic_pressure_table_files(self, node_ids):
        str_key = "acoustic pressure"
        folder_table_name = "acoustic_pressure_files"
        if isinstance(node_ids, int):
            node_ids = [node_ids]
        for node_id in node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.acoustic_pressure_table_name is not None:
                table_name = node.acoustic_pressure_table_name
                if self.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                str_key,
                                                                                table_name, 
                                                                                folder_table_name   ):
                    self.remove_acoustic_table_files_from_folder(table_name, "acoustic_pressure_files")
            # remove_bc_from_file(node_id, self.file._node_acoustic_path, [str_key], None, equals_keys=True)
        self.file.filter_bc_data_from_dat_file(node_ids, [str_key], self.file._node_acoustic_path)

    def remove_volume_velocity_table_files(self, node_ids):
        str_key = "volume velocity"
        folder_table_name = "volume_velocity_files"
        if isinstance(node_ids, int):
            node_ids = [node_ids]
        for node_id in node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.volume_velocity_table_name is not None:
                table_name = node.volume_velocity_table_name        
                if self.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                str_key,
                                                                                table_name, 
                                                                                folder_table_name   ):
                    self.remove_acoustic_table_files_from_folder(table_name, "volume_velocity_files")    
            # remove_bc_from_file(node_id, self.file._node_acoustic_path, [str_key], None, equals_keys=True)
        self.file.filter_bc_data_from_dat_file(node_ids, [str_key], self.file._node_acoustic_path)             

    def remove_compressor_excitation_table_files(self, node_ids):
        str_key = "compressor excitation -"
        folder_table_name = "compressor_excitation_files"
        if isinstance(node_ids, int):
            node_ids = [node_ids]
        for node_id in node_ids:
            node = self.preprocessor.nodes[node_id]
            for table_name in node.compressor_excitation_table_names:
                if table_name is not None:
                    if self.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                    str_key,
                                                                                    table_name, 
                                                                                    folder_table_name   ):
                        self.remove_acoustic_table_files_from_folder(table_name, "compressor_excitation_files")
            # remove_bc_from_file(node_id, self.file._node_acoustic_path, [str_key], None)
        self.file.filter_bc_data_from_dat_file(node_ids, [str_key], self.file._node_acoustic_path)

    def remove_specific_impedance_table_files(self, node_ids):
        str_key = "specific impedance"
        folder_table_name = "specific_impedance_files"
        if isinstance(node_ids, int):
            node_ids = [node_ids]
        for node_id in node_ids:
            node = self.preprocessor.nodes[node_id]
            if node.specific_impedance_table_name is not None:
                table_name = node.acoustic_pressure_table_name
                if self.file.check_if_table_can_be_removed_in_acoustic_model(   node_id, 
                                                                                str_key,
                                                                                table_name, 
                                                                                folder_table_name   ):
                    self.remove_acoustic_table_files_from_folder(table_name, "acoustic_pressure_files")  
            # remove_bc_from_file(node_id, self.file._node_acoustic_path, [str_key], None, equals_keys=True)
        self.file.filter_bc_data_from_dat_file(node_ids, [str_key], self.file._node_acoustic_path)

    def set_element_length_correction_by_elements(self, elements, value, section, psd_label=""):
        # label = ["acoustic element length correction"] 
        self.preprocessor.set_length_correction_by_element(elements, value, section)
        self.file.add_length_correction_in_file(elements, value, section, psd_label=psd_label)
    
    def set_perforated_plate_by_elements(self, list_elements, perforated_plate, section):
        self.preprocessor.set_perforated_plate_by_elements(list_elements, perforated_plate, section)
        self.preprocessor.process_elements_to_update_indexes_after_remesh_in_element_info_file(list_elements)
        self.file.add_perforated_plate_in_file(list_elements, perforated_plate, section)

    def set_capped_end_by_elements(self, elements, value, selection):
        self.preprocessor.set_capped_end_by_elements(elements, value, selection)
        self.file.modify_capped_end_elements_in_file(elements, value, selection)

    def set_capped_end_by_lines(self, lines, value):
        if isinstance(lines, int):
            lines = [lines]
        self.preprocessor.set_capped_end_by_lines(lines, value)
        self._set_capped_end_to_lines(lines, value)
        self.file.modify_capped_end_lines_in_file(lines, value)      

    def set_structural_element_wall_formulation_by_lines(self, lines, formulation):
        if isinstance(lines, int):
            lines = [lines]
        self.preprocessor.set_structural_element_wall_formulation_by_lines(lines, formulation)
        self._set_structural_element_wall_formulation_to_lines(lines, formulation)
        self.file.modify_structural_element_wall_formulation_in_file(lines, formulation)  

    def set_structural_element_force_offset_by_lines(self, lines, force_offset):
        if isinstance(lines, int):
            lines = [lines]
        self.preprocessor.set_structural_element_force_offset_by_lines(lines, force_offset)
        self._set_structural_element_force_offset_to_lines(lines, force_offset)
        self.file.modify_structural_element_force_offset_in_file(lines, force_offset)

    def set_inertia_load_setup(self, gravity, stiffening_effect=False):
        self.preprocessor.set_inertia_load(gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)
        self.file.add_inertia_load_setup_to_file(gravity, stiffening_effect)

    def _set_structural_element_wall_formulation_to_lines(self, lines, formulation):
        if isinstance(lines, int):
            lines = [lines]
        for line in lines:
            entity = self.preprocessor.dict_tag_to_entity[line] 
            entity.structural_element_wall_formulation = formulation

    def _set_structural_element_force_offset_to_lines(self, lines, force_offset):
        if isinstance(lines, int):
            lines = [lines]
        for line in lines:
            entity = self.preprocessor.dict_tag_to_entity[line] 
            entity.force_offset = force_offset

    def _set_capped_end_to_lines(self, lines, value):
        if isinstance(lines, int):
            lines = [lines]
        for line in lines:
            entity = self.preprocessor.dict_tag_to_entity[line] 
            entity.capped_end = value

    def get_nodes_with_acoustic_pressure_bc(self):
        return self.preprocessor.nodesAcousticBC

    def load_acoustic_pressure_bc_by_node(self, node_id, data):
        self.preprocessor.set_acoustic_pressure_bc_by_node(node_id, data)

    def load_volume_velocity_bc_by_node(self, node_id, data):
        self.preprocessor.set_volume_velocity_bc_by_node(node_id, data)

    def load_specific_impedance_bc_by_node(self, node_id, data):
        self.preprocessor.set_specific_impedance_bc_by_node(node_id, data)

    def load_radiation_impedance_bc_by_node(self, node_id, value):
        self.preprocessor.set_radiation_impedance_bc_by_node(node_id, value)

    def load_compressor_excitation_bc_by_node(self, node_id, data, connection_info):
        self.preprocessor.set_compressor_excitation_bc_by_node(node_id, data, connection_info)

    def load_length_correction_by_elements(self, list_elements, value, key):
        self.preprocessor.set_length_correction_by_element(list_elements, value, key)
        self.preprocessor.process_elements_to_update_indexes_after_remesh_in_element_info_file(list_elements)
    
    def load_perforated_plate_by_elements(self, list_elements, perforated_plate, key):
        self.preprocessor.set_perforated_plate_by_elements(list_elements, perforated_plate, key)
        self.preprocessor.process_elements_to_update_indexes_after_remesh_in_element_info_file(list_elements)
    
    def set_perforated_plate_convergence_dataLog(self, data):
        self.perforated_plate_data_log = data

    def set_color_scale_setup(self, color_scale_setup):
        self.color_scale_setup = color_scale_setup

    def get_map_nodes(self):
        return self.preprocessor.map_nodes

    def get_map_elements(self):
        return self.preprocessor.map_elements

    def get_preprocess(self):
        return self.preprocessor

    def get_nodes_color(self):
        return self.preprocessor.nodes_color

    def get_nodes(self):
        return self.preprocessor.nodes

    # def get_entities(self):
    #     return self.preprocessor.entities

    def get_node(self, node_id):
        return self.preprocessor.nodes[node_id]

    def get_entity(self, line_id):
        self.preprocessor.dict_tag_to_entity[line_id]
        return self.preprocessor.dict_tag_to_entity[line_id]

    def get_element_size(self):
        return self.file.element_size

    def set_modes_sigma(self, modes, sigma=1e-2):
        self.modes = modes
        self.sigma = sigma

    def get_frequencies(self):
        return self.frequencies

    def get_frequency_setup(self):
        return self.f_min, self.f_max, self.f_step

    def get_modes(self):
        return self.modes

    def get_material_list_path(self):
        return self.file.material_list_path
    
    def get_fluid_list_path(self):
        return self.file._fluid_list_path

    def set_analysis_type(self, ID, analysis_text, method_text = ""):
        self.analysis_ID = ID
        self.analysis_type_label = analysis_text
        self.analysis_method_label = method_text

    def get_analysis_id(self): 
        return self.analysis_ID

    def get_analysis_type_label(self):
        return self.analysis_type_label

    def get_analysis_method_label(self):
        return self.analysis_method_label

    def get_pre_solution_model_checks(self):
        return BeforeRun()

    def get_post_solution_model_checks(self):
        return AfterRun()

    def set_structural_damping(self, value):
        self.global_damping = value
        self.preprocessor.set_structural_damping(value)
        self.file.add_damping_in_file(value)

    def get_damping(self):
        return self.global_damping

    def set_structural_solve(self, structural_solve):
        self.structural_solve = structural_solve

    def get_structural_solve(self):

        if self.analysis_ID in [5, 6]:
            results = StructuralSolver(self.preprocessor, self.frequencies, acoustic_solution=self.solution_acoustic)

        else:

            if self.analysis_ID in [2, 4]:
                results = StructuralSolver(self.preprocessor, None)
            else:
                results = StructuralSolver(self.preprocessor, self.frequencies)

        return results

    def set_structural_solution(self, value):
        self.solution_structural = value

    def get_structural_solution(self):
        return self.solution_structural

    def get_acoustic_solve(self):
        return AcousticSolver(self.preprocessor, self.frequencies)

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
        if self.analysis_ID is None:
            return self.analysis_ID
        analysis = self.analysis_ID
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