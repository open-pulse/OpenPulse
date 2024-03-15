# from pulse.preprocessing.before_run import BeforeRun
from collections import defaultdict
from pulse.interface.user_input.project.print_message import PrintMessageInput
import numpy as np

from pulse import app

window_title_1 = "Error"
window_title_2 = "Warning"

class BeforeRun:
    def __init__(self, **kwargs):

        self.project = app().project
        self.opv = app().main_window.opv_widget

        self.preprocessor = self.project.preprocessor
        self.nodes = self.preprocessor.nodes
        self.structural_elements = self.preprocessor.structural_elements
        self.acoustic_elements = self.preprocessor.acoustic_elements
        self.dict_tag_to_entity = self.preprocessor.dict_tag_to_entity

    def check_modal_analysis_imported_data(self):
        message = ""
        title = "Modal analysis with imported data from tables"
        if len(self.project.file.non_zero_frequency_info)==3:
            [zero_frequency, f_min, table_name] = self.project.file.non_zero_frequency_info
            if not zero_frequency:
                message = "The current project setup has at least one loaded table of values for boundary conditions or external elements. "
                message += f"The first frequency point f={f_min}Hz from '{table_name}' file has been considered in the current analysis, "
                message += "however, it differs from the 0Hz value. Please, take this information into account when checking the obtained results."

        elif self.project.file.zero_frequency:    
            message = "The current project setup has at least one loaded table of values for boundary conditions or external elements. "
            message += "The first frequency point f=0Hz from imported files have been considered in the current analysis. Please, "
            message += "take this information into account when checking the obtained results."
            
        if message != "":
            PrintMessageInput([window_title_2, title, message])

    def check_input_NodeID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Node ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.nodes)

            list_nodes_typed = list(map(int, tokens))

            if len(list_nodes_typed) == 0:
                    message = "An empty input field for the Node ID has been detected. Please, enter a valid Node ID to proceed!"
            
            elif len(list_nodes_typed) >= 1: 
                if single_ID and len(list_nodes_typed) > 1:
                    message = "Multiple Node IDs"
                else:
                    try:
                        for node_ID in list_nodes_typed:
                            self.nodes[node_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Node ID input field. " 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Node ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([window_title_1, title, message])               
            return True, [] 

        if single_ID:
            return False, list_nodes_typed[0]
        else:
            return False, list_nodes_typed


    def check_input_ElementID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Element ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.structural_elements)

            list_elements_typed = list(map(int, tokens))

            if len(list_elements_typed) == 0:
                    message = "An empty input field for the Element ID has been detected. Please, enter a valid Element ID to proceed!"

            elif len(list_elements_typed) >= 1: 
                if single_ID and len(list_elements_typed)>1:
                    message = "Multiple Element IDs"
                else:
                    try:
                        for element_ID in list_elements_typed:
                            self.structural_elements[element_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Element ID input field. " 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Element ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([window_title_1, title, message])               
            return True, [] 

        if single_ID:
            return False, list_elements_typed[0]
        else:
            return False, list_elements_typed


    def check_input_LineID(self, lineEdit, single_ID=False):
        try:

            title = "Invalid entry to the Line ID"
            message = ""
            tokens = lineEdit.strip().split(',')

            try:
                tokens.remove('')
            except:
                pass

            _size = len(self.dict_tag_to_entity)

            list_lines_typed = list(map(int, tokens))

            if len(list_lines_typed) == 0:
                    message = "An empty input field for the Line ID has been detected. Please, enter a valid Line ID to proceed!"

            elif len(list_lines_typed) >= 1: 
                if single_ID and len(list_lines_typed)>1:
                    message = "Multiple Line IDs"
                else:
                    try:
                        for line_ID in list_lines_typed:
                            self.dict_tag_to_entity[line_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Line ID input field. " 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Line ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([window_title_1, title, message])               
            return True, [] 

        if single_ID:
            return False, list_lines_typed[0]
        else:
            return False, list_lines_typed


    def check_material_all_elements(self):
        """
        This method checks if all structural elements have a material object attributed.
        """
        self.check_set_material = False
        self.check_poisson = False
        lines_without_materials = []
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
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
        lines_without_poisson = []
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
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
        lines_without_materials = []
        lines_without_cross_sections = []
        elements_without_cross_sections = defaultdict(list)  
        for element in self.structural_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
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
                    if element.cross_section.area_fluid == 0:
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
        lines_without_fluids = []
        lines_without_cross_sections = []
        elements_without_cross_sections = defaultdict(list)
        for element in self.acoustic_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
            if element.fluid is None:
                if 'pipe_' in self.structural_elements[element.index].element_type:
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
                if self.structural_elements[element.index].element_type == 'expansion_joint':
                    if element.cross_section.area_fluid == 0:
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
        lines_without_fluids = []
        for element in self.acoustic_elements.values():
            line_id = self.preprocessor.elements_to_line[element.index]
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
        self.is_there_acoustic_pressure = False
        self.is_there_volume_velocity = False
        for node in self.nodes.values():
            
            if structural:               
                if self.preprocessor.stress_stiffening_enabled:
                    self.is_there_loads = True
                    return

                if node.there_are_nodal_loads:
                    self.is_there_loads = True
                    return

                if node.there_are_prescribed_dofs:
                    if True in [True if isinstance(value, np.ndarray) else False for value in node.prescribed_dofs]:
                        self.is_there_prescribed_dofs = True
                        return

                    elif sum([value if value is not None else complex(0) for value in node.prescribed_dofs]) != complex(0):
                        self.is_there_prescribed_dofs = True
                        return

            if acoustic or coupled:
                if node.acoustic_pressure is not None:
                    self.is_there_acoustic_pressure = True
                    return

                if node.volume_velocity is not None:
                    self.is_there_volume_velocity = True
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

        list_plane_wave = []
        list_wide_duct = []
        list_lrf_fluid_eq = []
        list_lrf_full = []
        list_max_valid_freq = []
        list_min_valid_freq = []

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
        lists_elements = [list_plane_wave, list_wide_duct, list_lrf_fluid_eq, list_lrf_full, []]

        for index, flag in enumerate(list_flags):
            if flag:
                self.opv.plot_mesh()
                self.opv.opvRenderer.highlight_elements(lists_elements[index])
                PrintMessageInput([window_title, title, list_messages[index]])


    def check_is_there_a_problem(self, analysis_ID):

        title = " Insufficient model inputs "

        cross_section_message = "You should set a Cross-Section to all elements before proceeding with the model solution.!"
        #
        material_message = "You should to set a Material to all elements before trying to run any Analysis!\n\n"
        material_message += "Lines without material assignment: \n{}"
        #
        fluid_message = "You should to set a Fluid to all elements before trying to run any Analysis!\n\n"
        fluid_message += "Lines without fluid assignment: \n{}"
        #
        all_fluid_inputs_message = "You should insert all fluid properties for wide-duct, LRF fluid equivalent and " 
        all_fluid_inputs_message += "LRF full acoustic element types before proceeding with the model solution.\n\n"
        all_fluid_inputs_message += "Lines with incomplete fluid properties: \n{}"
        #
        structural_message = "You should to apply an external load to the model or prescribe a non-null DOF value before trying to solve the Harmonic Analysis!"
        acoustic_message = "You should to insert a 'Volume velocity' or prescribe an 'Acoustic pressure' to a node before trying to solve the Harmonic Analysis!"
    
        if analysis_ID == 2:
            
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                message = material_message.format(lines_without_materials)
                PrintMessageInput([window_title_1, title, message])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}\n"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([window_title_1, title, cross_section_message])
                return True
        
        elif analysis_ID == 4:
            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True
            elif self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([window_title_1, title, cross_section_message])
                return True

        elif analysis_ID == 0 or analysis_ID == 1:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            self.check_nodes_attributes(structural=True)
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([window_title_1, title, cross_section_message])
                return True
            elif not self.is_there_loads:
                if not self.is_there_prescribed_dofs:
                    PrintMessageInput([window_title_1, title, structural_message])
                    return True
    
        elif analysis_ID == 3:

            lines_without_materials = self.check_material_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(acoustic=True)
            if self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True
            elif self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True
            elif self.check_set_crossSection:
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([window_title_1, title, cross_section_message])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([window_title_1, title, acoustic_message])
                    return True

        elif analysis_ID == 5 or analysis_ID == 6:
            lines_without_materials, elements_without_cross_sections = self.check_material_and_cross_section_in_all_elements()
            lines_without_fluids, elements_without_cross_sections = self.check_fluid_and_cross_section_in_all_elements()
            lines_without_all_fluids_inputs = self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(coupled=True)
            if self.check_set_material:
                self.opv.opvRenderer.highlight_lines(lines_without_materials)
                PrintMessageInput([window_title_1, title, material_message.format(lines_without_materials)])
                return True
            elif self.check_set_fluid:
                self.opv.opvRenderer.highlight_lines(lines_without_fluids)
                PrintMessageInput([window_title_1, title, fluid_message.format(lines_without_fluids)])
                return True
            elif self.check_all_fluid_inputs:
                self.opv.opvRenderer.highlight_lines(lines_without_all_fluids_inputs)
                PrintMessageInput([window_title_1, title, all_fluid_inputs_message.format(lines_without_all_fluids_inputs)])
                return True
            elif self.check_set_crossSection:  
                list_lines, list_elements = self.check_cross_section_in_lines_and_elements(elements_without_cross_sections)
                if list_elements == []:  
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"                 
                    self.opv.opvRenderer.highlight_lines(list_lines)
                elif list_lines == []:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}"
                    self.opv.opvRenderer.highlight_elements(list_elements)
                else:
                    cross_section_message += f"Elements without cross-section assignment: \n\n{list_elements}\n\n"
                    cross_section_message += f"Lines without cross-section assignment: \n\n{list_lines}"
                    self.opv.opvRenderer.highlight_lines(list_lines)
                    self.opv.opvRenderer.highlight_elements(list_elements, reset_colors=False)
                PrintMessageInput([window_title_1, title, cross_section_message])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([window_title_1, title, acoustic_message])
                    return True
    
    def check_cross_section_in_lines_and_elements(self, data):
        list_lines = []
        list_elements = []
        for line_id, element_ids in data.items():
            if list(np.sort(element_ids)) == list(np.sort(self.preprocessor.line_to_elements[line_id])):
                list_lines.append(line_id)
            else:
                for element_id in element_ids:
                    list_elements.append(element_id)
        return list_lines, list_elements
    
    def check_beam_theory_criteria(self, criteria=10):
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
                
            if not removed_from_list or len(list_of_neighboor_lines)==0:
                if len(list_of_neighboor_lines) > 0:
                    output_lines = list_of_neighboor_lines[0]
                    index += 1
            
            return output_lines, list_of_neighboor_lines, neighboor_data, index

        self.section_data_lines, _ = self.project.file.get_cross_sections_from_file()

        self.one_section_one_line = {}
        self.one_section_multiple_lines = {}
        for section_id, [element_type, section_parameters, tag_type, tags] in self.section_data_lines.items():

            if (element_type == "pipe_1" and len(section_parameters) == 6) or "beam_1" in element_type:

                if len(tags) == 1:
                    line_ID = tags[0]
                    length_1, edge_nodes_1 = self.preprocessor.get_line_length(line_ID)

                    if element_type == "pipe_1" and len(section_parameters) == 6:
                        parameter = section_parameters[0]
                    elif "beam_1" in element_type:
                        parameter = max(section_parameters)
                
                    ratio_1 = length_1/parameter
                    self.one_section_one_line[section_id] = {   "section parameter" : parameter,
                                                                "length" : length_1,
                                                                "ratio" : ratio_1,
                                                                "line ID" : tags   }
                    
                else:

                    data = {}
                    neighboor_lines = []

                    for i, tag in enumerate(tags):
                        filtered_lines = []                                
                        length_0, edge_nodes_0 = self.preprocessor.get_line_length(tag)
                        lines = self.get_lines_from_nodes(edge_nodes_0)
                        for line in lines:
                            if line in tags and line not in filtered_lines:
                                filtered_lines.append(line)
                        data[tag] = [length_0, edge_nodes_0, filtered_lines]
                        neighboor_lines.append(filtered_lines)
                        
                    index = 1
                    cache_neighboor_lines = neighboor_lines.copy()
                    ref_lines = neighboor_lines[0]
                    max_iter = 0
                    neighboor_data = {}

                    while len(cache_neighboor_lines) > 0 and max_iter < 1000:
                        ref_lines, cache_neighboor_lines, neighboor_data, index = get_neighboors(   ref_lines, 
                                                                                                    cache_neighboor_lines, 
                                                                                                    neighboor_data, 
                                                                                                    index   )
                    
                    aux = {}
                    if len(neighboor_data)>0:
                        for ind, neigh_lines in neighboor_data.items():

                            if element_type == "pipe_1" and len(section_parameters) == 6:
                                parameter = section_parameters[0]
                            elif "beam_1" in element_type:
                                parameter = max(section_parameters)

                            lengths = []
                            for n_line in neigh_lines:
                                length, _ = self.preprocessor.get_line_length(n_line)
                                lengths.append(length)
                            total_length = np.sum(lengths)
                            ratio = total_length/parameter
                            aux[ind] = {"section parameter" : parameter,
                                        "lines" : neigh_lines,
                                        "lengths" : lengths,
                                        "total length" : total_length,
                                        "ratio" : ratio}
                    
                    self.one_section_multiple_lines[section_id] = aux
        
                
    def get_lines_from_nodes(self, edge_nodes):
        """
        """
        lines = []
        if len(edge_nodes) == 2:
            
            node_1 = edge_nodes[0]
            node_2 = edge_nodes[1]

            elements_node_1 = self.preprocessor.elements_connected_to_node[node_1]
            elements_node_2 = self.preprocessor.elements_connected_to_node[node_2]
            
            # if len(elements_node_1) == 2:
            for element in elements_node_1:
                line_1 = self.preprocessor.elements_to_line[element.index]
                lines.append(line_1)

            # if len(elements_node_2) == 2:
            for element in elements_node_2:
                line_2 = self.preprocessor.elements_to_line[element.index]
                lines.append(line_2)
        
        return lines
