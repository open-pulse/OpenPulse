# fmt: off

from pulse import app
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import mm_to_m

import numpy as np
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class BeforeRun:
    def __init__(self):

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties
        self.preprocessor = app().project.preprocessor

        self.nodes = self.preprocessor.nodes
        self.acoustic_elements = self.preprocessor.acoustic_elements

        self.structural_elements = self.preprocessor.structural_elements

    def check_modal_analysis_imported_data(self):
        message = ""
        title = "Modal analysis with imported data from tables"
        if self.properties.check_if_there_are_tables_at_the_model():
            message = "The current project setup has at least one loaded table of values for boundary conditions or external elements. "
            message += "The first frequency point near to 0 Hz from imported files have been considered in the current analysis. Please, "
            message += "take this information into account when checking the obtained results."
            
        if message != "":
            PrintMessageInput([window_title_2, title, message])

    def check_selected_ids(self, selected_ids : str, selection_type : str, single_id = False):
        try:


            title = "Invalid entry to the Line ID"
            message = ""

            tokens = selected_ids.strip().split(',')
            label = selection_type.replace("s", "")

            try:
                tokens.remove('')
            except:
                pass

            if selection_type == "lines":
                _size = len(self.model.mesh.lines_from_model)

            elif selection_type == "elements":
                _size = len(self.structural_elements)

            elif selection_type == "nodes":
                _size = len(self.nodes)
    
            typed_ids = list(map(int, tokens))
            
            if len(typed_ids) == 0:
                    message = f"An empty input field for the {label.capitalize()} ID has been detected." 
                    message += f"You should to enter a valid  {label.capitalize()} ID to proceed!"

            elif len(typed_ids) >= 1:

                if single_id and len(typed_ids)>1:
                    message = f"Multiple {label.capitalize()} IDs"

                else:
                    try:
                        for typed_id in typed_ids:

                            if selection_type == "lines":
                                self.model.mesh.elements_from_line[typed_id]

                            elif selection_type == "elements":
                                self.structural_elements[typed_id]

                            elif selection_type == "nodes":
                                self.nodes[typed_id]

                            else:
                                continue

                    except:
                        message = f"Dear user, you have typed an invalid entry at the {label.capitalize()} ID input field. " 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the {label.capitalize()} IDs! \n\n"
            message += str(log_error)

        if message != "":
            PrintMessageInput([window_title_1, title, message])               
            return True, list() 

        if single_id:
            return False, typed_ids[0]
        else:
            return False, typed_ids

    def check_material_all_elements(self):
        """
        This method checks if all structural elements have a material object attributed.
        """
        self.check_set_material = False
        self.check_poisson = False
        lines_without_materials = list()
        for element in self.structural_elements.values():
            line_id = self.model.mesh.line_from_element[element.index]
            if element.material is None:
                self.check_set_material = True
                if line_id not in lines_without_materials:
                    lines_without_materials.append(line_id)
                
        return lines_without_materials

    def check_poisson_all_elements(self):
        """
        This method checks if all structural elements have a Poisson ratio attributed.
        """
        self.check_poisson = False
        lines_without_poisson = list()
        for element in self.structural_elements.values():
            line_id = self.model.mesh.line_from_element[element.index]
            if element.material.poisson_ratio == 0:
                self.check_poisson = True
                if line_id not in lines_without_poisson:
                    lines_without_poisson.append(line_id)
                
        return lines_without_poisson

    def check_material_and_cross_section_in_all_elements(self):
        """
        This method checks if all structural elements have a material object and a cross section object attributed.
        """
        self.check_set_material = False
        self.check_set_crossSection = False
        self.check_poisson = False
        lines_without_materials = list()
        lines_without_cross_sections = list()
        elements_without_cross_sections = defaultdict(list)  
        for element in self.structural_elements.values():
            line_id = self.model.mesh.line_from_element[element.index]
            if element.material is None:
                self.check_set_material = True
                if line_id not in lines_without_materials:
                    lines_without_materials.append(line_id)

            if element.cross_section is None:
                if element.element_type:
                    self.check_set_crossSection = True
                    if element.index not in elements_without_cross_sections[line_id]:
                        elements_without_cross_sections[line_id].append(element.index)
                    if line_id not in lines_without_cross_sections:
                        lines_without_cross_sections.append(line_id)
                    
            else:        

                if element.element_type == 'expansion_joint':
                    if element.expansion_joint_data is None:
                        self.check_set_crossSection = True
                        if element.index not in elements_without_cross_sections[line_id]:
                            elements_without_cross_sections[line_id].append(element.index)
                        if line_id not in lines_without_cross_sections:
                            lines_without_cross_sections.append(line_id)

                else:

                    if element.cross_section.thickness == 0:
                        if element.cross_section.area == 0:
                            self.check_set_crossSection = True
                            if element.index not in elements_without_cross_sections[line_id]:
                                elements_without_cross_sections[line_id].append(element.index)
                            if line_id not in lines_without_cross_sections:
                                lines_without_cross_sections.append(line_id)

        return lines_without_materials, elements_without_cross_sections

    def check_fluid_and_cross_section_in_all_elements(self):
        """
        This method checks if all acoustic elements have a fluid object and a cross section object attributed.
        """

        self.check_set_fluid = False
        self.check_set_crossSection = False
        lines_without_fluids = list()
        lines_without_cross_sections = list()
        elements_without_cross_sections = defaultdict(list)

        for element in self.acoustic_elements.values():

            structural_element = self.structural_elements[element.index]

            line_id = self.model.mesh.line_from_element[element.index]
            if element.fluid is None:
                if structural_element.element_type in ["pipe_1", "valve", "expansion_joint"]:
                    self.check_set_fluid = True
                    if line_id not in lines_without_fluids:
                        lines_without_fluids.append(line_id)

            if element.cross_section is None:

                self.check_set_crossSection = True
                if element.index not in elements_without_cross_sections[line_id]:
                    elements_without_cross_sections[line_id].append(element.index)
                if line_id not in lines_without_cross_sections:
                        lines_without_cross_sections.append(line_id)

            else:

                if structural_element.element_type == 'expansion_joint':
                    if structural_element.expansion_joint_data is None:
                        self.check_set_crossSection = True
                        if element.index not in elements_without_cross_sections[line_id]:
                            elements_without_cross_sections[line_id].append(element.index)
                        if line_id not in lines_without_cross_sections:
                            lines_without_cross_sections.append(line_id)     

                else:    

                    if element.cross_section.thickness == 0:
                        if element.cross_section.area == 0:
                            self.check_set_crossSection = True
                            if element.index not in elements_without_cross_sections[line_id]:
                                elements_without_cross_sections[line_id].append(element.index)
                            if line_id not in lines_without_cross_sections:
                                lines_without_cross_sections.append(line_id)
                        
        return lines_without_fluids, elements_without_cross_sections

    def check_fluid_inputs_in_all_elements(self):
        """
        This method checks if each acoustic element has the necessary fluid data to evaluate the analysis according to its element type.
        """
        self.check_all_fluid_inputs = False
        lines_without_fluids = list()
        for element in self.acoustic_elements.values():
            line_id = self.model.mesh.line_from_element[element.index]
            if element.element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                if 'pipe_' in self.structural_elements[element.index].element_type:
                    _list = [   element.fluid.isentropic_exponent, element.fluid.thermal_conductivity, 
                                element.fluid.specific_heat_Cp, element.fluid.dynamic_viscosity   ]
                    if None in _list:
                        self.check_all_fluid_inputs = True
                        if line_id not in lines_without_fluids:
                            lines_without_fluids.append(line_id)
                        
        return lines_without_fluids


    def check_nodes_attributes(self, acoustic=False, structural=False, coupled=False):
        """
        This method checks if there is the necessary nodal input data to evaluate the analysis according to its type.

        Parameters
        ----------
        acoustic : boll, optional
            True if a acoustic analysis will be performed. False otherwise.
            Default is False.

        structural : boll, optional
            True if a structural analysis will be performed. False otherwise.
            Default is False.

        coupled : boll, optional
            True if a coupled analysis will be performed. False otherwise.
            Default is False.
        """

        self.is_there_loads = False
        self.is_there_prescribed_dofs = False
        self.acoustic_pressure = False
        self.volume_velocity = False
        self.compressor_excitation = False
            
        if structural:               
            if self.preprocessor.stress_stiffening_enabled:
                self.is_there_loads = True
                return

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "nodal_loads":
                    self.is_there_loads = True
                    return

            for (property, *args), data in self.properties.nodal_properties.items():
                data: dict
                if property == "prescribed_dofs":
                    if "table_names" in data.keys():
                        self.is_there_prescribed_dofs = True

                    elif "values" in data.keys():
                        values = data["values"]
                        if sum([complex(0) if value is None else value for value in values]) != complex(0):
                            self.is_there_prescribed_dofs = True
                            return

        if acoustic or coupled:
            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "acoustic_pressure":
                    self.acoustic_pressure = True
                    return

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "volume_velocity":
                    self.volume_velocity = True
                    return

            for (property, *args) in self.properties.nodal_properties.keys():
                if property == "compressor_excitation":
                    self.compressor_excitation = True
                    return

    def check_all_acoustic_criteria(self):
        window_title = "WARNING"
        title = "Acoustic criteria not satisfied"
        
        flag_plane_wave = False
        flag_wide_duct = False
        flag_lrf_fluid_eq = False
        flag_lrf_full = False
        flag_unflanged_radiation_impedance = False
        
        message_plane_wave = "The acoustic model is out of the plane wave validity frequency range. It is recommended to check the high frequency results carefully."
        message_wide_duct = "The wide-duct acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_lrf_fluid_eq = "The Low Reduced Frequency (LRF fluid equivalent) acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_lrf_full = "The Low Reduced Frequency (LRF) acoustic damping model is out of its validity frequency range. It is recommended to check the results carefully."
        message_unflanged_radiation_impedance  = "The unflanged radiation impedance model is out of its validity frequency range. It is recommended to check the results carefully."

        list_plane_wave = list()
        list_wide_duct = list()
        list_lrf_fluid_eq = list()
        list_lrf_full = list()
        list_max_valid_freq = list()
        list_min_valid_freq = list()

        for element in self.acoustic_elements.values():
            if element.flag_plane_wave:
                list_plane_wave.append(element.index)
            if element.flag_wide_duct:
                list_wide_duct.append(element.index)
            if element.flag_lrf_fluid_eq:
                list_lrf_fluid_eq.append(element.index)
            if element.flag_lrf_full:
                list_lrf_full.append(element.index)
            list_max_valid_freq.append(element.max_valid_freq) 
            list_min_valid_freq.append(element.min_valid_freq)
                
            if element.flag_unflanged_radiation_impedance and not flag_unflanged_radiation_impedance:
                flag_unflanged_radiation_impedance = True

        self.dict_criterias = {}

        if len(list_plane_wave)>=1:
            flag_plane_wave = True
            self.dict_criterias['Plane wave'] = list_plane_wave
        if len(list_wide_duct)>=1:
            flag_wide_duct = True
            self.dict_criterias['Wide duct'] = list_wide_duct
        if len(list_lrf_fluid_eq)>=1:
            flag_lrf_fluid_eq = True
            self.dict_criterias['LRF fluid eq'] = list_lrf_fluid_eq
        if len(list_lrf_full)>=1:
            flag_lrf_full = True
            self.dict_criterias['LRF full'] = list_lrf_full
        
        self.max_valid_freq = np.array(list_max_valid_freq)[np.array(list_max_valid_freq)!=None]
        self.min_valid_freq = np.array(list_min_valid_freq)[np.array(list_min_valid_freq)!=None]

        self.max_valid_freq = np.min(self.max_valid_freq)
        self.min_valid_freq = np.max(self.min_valid_freq)

        list_flags = [flag_plane_wave, flag_wide_duct, flag_lrf_fluid_eq, flag_lrf_full, flag_unflanged_radiation_impedance]
        list_messages = [message_plane_wave, message_wide_duct, message_lrf_fluid_eq, message_lrf_full, message_unflanged_radiation_impedance]
        lists_elements = [list_plane_wave, list_wide_duct, list_lrf_fluid_eq, list_lrf_full, list()]

        for index, flag in enumerate(list_flags):
            if flag:
                app().main_window.plot_mesh()
                app().main_window.set_selection(elements = lists_elements[index])
                PrintMessageInput([window_title, title, list_messages[index]])


    def check_is_there_a_problem(self, analysis_id):

        title = " Insufficient model inputs "

        cross_section_message = "You should set a Cross-Section to all elements before proceeding with the model solution.\n\n"
        #
        material_message = "You should to set a Material to all elements before trying to run any Analysis.\n\n"
        material_message += "Lines without material assignment: \n{}"
        #
        fluid_message = "You should to set a Fluid to all elements before trying to run any Analysis.\n\n"
        fluid_message += "Lines without fluid assignment: \n{}"
        #
        all_fluid_inputs_message = "You should insert all fluid properties for wide-duct, LRF fluid equivalent and " 
        all_fluid_inputs_message += "LRF full acoustic element types before proceeding with the model solution.\n\n"
        all_fluid_inputs_message += "Lines with incomplete fluid properties: \n{}"
        #
        structural_message = "You should to apply an external load to the model or prescribe a non-null DOF value before trying to solve the Harmonic Analysis."
        #
        acoustic_message = "Enter a nodal acoustic excitation to proceed with the Harmonic Analysis processing. "
        acoustic_message += "\n\nAvailable acoustic excitations: acoustic pressure; compressor excitation; volume velocity."

        if analysis_id == 2:

            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            if self.check_set_material:
                app().main_window.set_selection(lines = lines_without_materials)
                message = material_message.format(lines_without_materials)
                PrintMessageInput([window_title_1, title, message])
                return True

            elif self.check_set_crossSection:

                line_ids, element_ids = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if element_ids == list():  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}\n"                 
                    app().main_window.set_selection(lines = line_ids)

                elif line_ids == list():
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n"
                    app().main_window.set_selection(elements = element_ids)

                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"
                    app().main_window.set_selection(lines = line_ids)
                    app().main_window.set_selection(elements = element_ids)

                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

        elif analysis_id == 4:
            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()

            if self.check_set_material:
                app().main_window.set_selection(lines = lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True

            elif self.check_set_fluid:
                app().main_window.set_selection(lines = lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True

            elif self.check_all_fluid_inputs:
                app().main_window.set_selection(lines = lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True

            elif self.check_set_crossSection:

                line_ids, element_ids = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if element_ids == list():  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"                 
                    app().main_window.set_selection(lines = line_ids)

                elif line_ids == list():
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}"
                    app().main_window.set_selection(lines = element_ids)

                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"
                    app().main_window.set_selection(lines = line_ids)
                    app().main_window.set_selection(elements = element_ids)

                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

        elif analysis_id == 0 or analysis_id == 1:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            self.check_nodes_attributes(structural=True)

            if self.check_set_material:
                app().main_window.set_selection(lines = lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True

            elif self.check_set_crossSection:

                line_ids, element_ids = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if element_ids == list():  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"                 
                    app().main_window.set_selection(lines = line_ids)

                elif line_ids == list():
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}"
                    app().main_window.set_selection(elements = element_ids)

                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"
                    app().main_window.set_selection(lines = line_ids)
                    app().main_window.set_selection(elements = element_ids)

                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

            elif not self.is_there_loads:
                if not self.is_there_prescribed_dofs:
                    PrintMessageInput([window_title_1, title, structural_message])
                    return True

        elif analysis_id == 3:

            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(acoustic=True)

            if self.check_set_fluid:
                app().main_window.set_selection(lines =lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True

            elif self.check_all_fluid_inputs:
                app().main_window.set_selection(lines =lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True

            elif self.check_set_material:
                app().main_window.set_selection(lines =lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True

            elif self.check_set_crossSection:

                line_ids, element_ids = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)

                if element_ids == list():  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"                 
                    app().main_window.set_selection(lines =line_ids)

                elif line_ids == list():
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}"
                    app().main_window.set_selection(elements = element_ids)

                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"
                    app().main_window.set_selection(lines = line_ids)
                    app().main_window.set_selection(elements = element_ids)

                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

            elif sum([  self.acoustic_pressure, 
                        self.volume_velocity, 
                        self.compressor_excitation  ]) == 0:

                PrintMessageInput([window_title_1, title, acoustic_message])
                return True

        elif analysis_id == 5 or analysis_id == 6:

            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(coupled=True)

            if self.check_set_material:
                app().main_window.set_selection(lines = lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True

            elif self.check_set_fluid:
                app().main_window.set_selection(lines = lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True

            elif self.check_all_fluid_inputs:
                app().main_window.set_selection(lines = lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True

            elif self.check_set_crossSection:

                line_ids, element_ids = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)

                if element_ids == list():  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"                 
                    app().main_window.set_selection(lines = line_ids)

                elif line_ids == list():

                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}"
                    app().main_window.set_selection(elements = element_ids)
                else:

                    cross_section_message += f"Elements without cross-section assignment: \n\n{element_ids}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{line_ids}"
                    app().main_window.set_selection(lines = line_ids)
                    app().main_window.set_selection(elements = element_ids)

                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

            elif sum([  self.acoustic_pressure, 
                        self.volume_velocity, 
                        self.compressor_excitation  ]) == 0:

                PrintMessageInput([window_title_1, title, acoustic_message])
                return True
    
    def check_cross_section_in_lines_and_elements(self, data):

        line_ids = list()
        element_ids = list()

        for line_id, _element_ids in data.items():
            if list(np.sort(element_ids)) == list(np.sort(self.model.mesh.elements_from_line[line_id])):
                line_ids.append(line_id)
            else:
                for _element_id in _element_ids:
                    element_ids.append(_element_id)

        return line_ids, element_ids
    
    def check_beam_theory_criteria(self):
        """
        """
        
        def get_neighboors(input_lines, list_of_neighboor_lines, neighboor_data, index):

            stop = False
            removed_from_list = False
            output_lines = input_lines.copy()

            if input_lines in list_of_neighboor_lines:
                list_of_neighboor_lines.remove(input_lines)

            for neighboor_lines in list_of_neighboor_lines:
                if stop:
                    break
                for line_id in neighboor_lines:
                    if line_id in input_lines:
                        cache_neighboor_lines = neighboor_lines.copy()
                        stop=True
                        break

            if stop:
                for line in cache_neighboor_lines:
                    if line not in output_lines:
                        output_lines.append(line)

                if cache_neighboor_lines in list_of_neighboor_lines:
                    list_of_neighboor_lines.remove(cache_neighboor_lines)
                    removed_from_list = True

            neighboor_data[index] = output_lines

            if not removed_from_list or len(list_of_neighboor_lines) == 0:
                if len(list_of_neighboor_lines) > 0:
                    output_lines = list_of_neighboor_lines[0]
                    index += 1

            return output_lines, list_of_neighboor_lines, neighboor_data, index

        section_data_lines = app().loader.get_cross_sections_from_file()

        self.one_section_one_line = dict()
        self.one_section_multiple_lines = dict()
        for section_id, [element_type, section_parameters, tag_type, line_ids] in section_data_lines.items():

            if (element_type == "pipe_1" and len(section_parameters) == 6) or "beam_1" in element_type:

                if len(line_ids) == 1:

                    line_id = line_ids[0]
                    length_mm = self.preprocessor.mesh.curve_length[line_id]
                    length_m = mm_to_m(length_mm)

                    if element_type == "pipe_1" and len(section_parameters) == 6:
                        parameter = section_parameters[0]

                    elif "beam_1" in element_type:
                        parameter = max(section_parameters)
                
                    ratio_1 = length_m / parameter
                    self.one_section_one_line[section_id] = {
                                                            "section parameter" : parameter,
                                                            "length" : length_m,
                                                            "ratio" : ratio_1,
                                                            "line ID" : line_ids
                                                            }

                else:

                    # data = dict()
                    neighboor_lines = list()

                    for i, line_id in enumerate(line_ids):

                        edge_nodes = list()
                        line_edges = self.properties.get_line_edges(line_id)

                        filtered_lines = list()                

                        for coords in line_edges:

                            node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                            edge_nodes.append(node_id)

                            for line in self.preprocessor.mesh.lines_from_node[node_id]:
                                if (line in line_ids) and (line not in filtered_lines):
                                    filtered_lines.append(line)

                        if filtered_lines:  
                            # data[line_id] = [length_m, edge_nodes, filtered_lines]
                            neighboor_lines.append(filtered_lines)

                    cache_neighboor_lines = neighboor_lines.copy()
                    ref_lines = neighboor_lines[0]

                    index = 1
                    max_iter = 0
                    neighboor_data = dict()

                    while len(cache_neighboor_lines) > 0 and max_iter < 1000:
                        # print("\nAntes:", (ref_lines, cache_neighboor_lines, neighboor_data, index))
                        neigh_data = get_neighboors(ref_lines, cache_neighboor_lines, neighboor_data, index)
                        ref_lines, cache_neighboor_lines, neighboor_data, index = neigh_data
                        # print("Depois:", (ref_lines, cache_neighboor_lines, neighboor_data, index))

                    # print(f"antes -> {neighboor_data}")
                    # neighboor_data = self.filter_braches_with_equal_section(neighboor_data)
                    # print(f"depois -> {neighboor_data}")

                    aux = dict()
                    if neighboor_data:
                        for ind, neigh_lines in neighboor_data.items():

                            if element_type == "pipe_1" and len(section_parameters) == 6:
                                parameter = section_parameters[0]
                            elif "beam_1" in element_type:
                                parameter = max(section_parameters)

                            lengths = list()
                            for _line_id in neigh_lines:
                                length_mm = self.preprocessor.mesh.curve_length[_line_id]
                                length_m = mm_to_m(length_mm)
                                lengths.append(length_m)

                            total_length = np.sum(lengths)
                            ratio = total_length / parameter

                            aux[ind] = {
                                        "section parameter" : parameter,
                                        "lines" : neigh_lines,
                                        "lengths" : lengths,
                                        "total length" : total_length,
                                        "ratio" : ratio
                                        }

                    self.one_section_multiple_lines[section_id] = aux

    def filter_braches_with_equal_section(self, data: dict):
        index = 0
        aux = dict()
        for _, line_ids in data.items():

            main_lines = line_ids.copy()

            for line_id in line_ids:

                # main_lines = list()
                # branch_lines = list()
                selected_element = None

                edge_nodes = list()
                line_edges = self.properties.get_line_edges(line_id)
                for coords in line_edges:

                    node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                    edge_nodes.append(node_id)

                    if len(self.preprocessor.mesh.lines_from_node[node_id]) > 2:

                        elements = self.preprocessor.structural_elements_connected_to_node[node_id]
                        for element in elements:
                            if self.preprocessor.mesh.line_from_element[element.index] == line_id:
                                selected_element = element
                                break

                        list_elements = elements.copy()
                        list_elements.remove(selected_element)

                        u = selected_element.directional_vector
                        for element in list_elements:

                            v = selected_element.directional_vector

                            if round(np.dot(u, v), 6) == 1:

                                line_0 = self.preprocessor.mesh.line_from_element[selected_element.index]
                                line_1 = self.preprocessor.mesh.line_from_element[element.index]

                                if line_0 not in main_lines:
                                    main_lines.append(line_0)

                                if line_1 not in main_lines:
                                    main_lines.append(line_1)

                                break

                if main_lines:
                    index += 1
                    aux[index] = main_lines

                elif selected_element is not None:
                    index += 1
                    aux[index] = [self.preprocessor.mesh.line_from_element[selected_element.index]]

        return aux

# fmt: on