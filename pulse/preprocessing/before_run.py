# from pulse.preprocessing.before_run import BeforeRun
from data.user_input.project.printMessageInput import PrintMessageInput
import numpy as np

window_title_1 = "ERROR"
window_title_2 = "WARNING"

class BeforeRun:
    def __init__(self, mesh, **kwargs):
        self.mesh = mesh
        self.nodes = mesh.nodes
        self.structural_elements = mesh.structural_elements
        self.acoustic_elements = mesh.acoustic_elements
        self.dict_tag_to_entity = mesh.dict_tag_to_entity


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
                    message = "An empty input field for the Node ID has been detected. \n\nPlease, enter a valid Node ID to proceed!"
            
            elif len(list_nodes_typed) >= 1: 
                if single_ID and len(list_nodes_typed) > 1:
                    message = "Multiple Node IDs"
                else:
                    try:
                        for node_ID in list_nodes_typed:
                            self.nodes[node_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Node ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Node ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
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
                    message = "An empty input field for the Element ID has been detected. \n\nPlease, enter a valid Element ID to proceed!"

            elif len(list_elements_typed) >= 1: 
                if single_ID and len(list_elements_typed)>1:
                    message = "Multiple Element IDs"
                else:
                    try:
                        for element_ID in list_elements_typed:
                            self.structural_elements[element_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Element ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Element ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
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
                    message = "An empty input field for the Line ID has been detected. \n\nPlease, enter a valid Line ID to proceed!"

            elif len(list_lines_typed) >= 1: 
                if single_ID and len(list_lines_typed)>1:
                    message = "Multiple Line IDs"
                else:
                    try:
                        for line_ID in list_lines_typed:
                            self.dict_tag_to_entity[line_ID]
                    except:
                        message = "Dear user, you have typed an invalid entry at the Line ID input field.\n\n" 
                        message += f"The input value(s) must be integer(s) number(s) greater than 1 and\n less than {_size}."

        except Exception as log_error:
            message = f"Wrong input for the Line ID's! \n\n{str(log_error)}"

        if message != "":
            PrintMessageInput([title, message, window_title_1])               
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
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return

    def check_poisson_all_elements(self):
        """
        This method checks if all structural elements have a Poisson ratio attributed.
        """
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material.poisson_ratio == 0:
                self.check_poisson = True
                return


    def check_material_and_cross_section_in_all_elements(self):
        """
        This method checks if all structural elements have a material object and a cross section object attributed.
        """
        self.check_set_material = False
        self.check_set_crossSection = False
        self.check_poisson = False
        for element in self.structural_elements.values():
            if element.material is None:
                self.check_set_material = True
                return
            if element.cross_section is None:
                if element.element_type:
                    self.check_set_crossSection = True
                    return
            else:        

                if element.element_type == 'expansion_joint':
                    if element.cross_section.area_fluid == 0:
                        self.check_set_crossSection = True
                        return
                else:
                    if element.cross_section.thickness == 0:
                        if element.cross_section.area == 0:
                            self.check_set_crossSection = True
                            return


    def check_fluid_and_cross_section_in_all_elements(self):
        """
        This method checks if all acoustic elements have a fluid object and a cross section object attributed.
        """
        self.check_set_fluid = False
        self.check_set_crossSection = False
        for element in self.acoustic_elements.values():
            
            if element.fluid is None:
                if 'pipe_' in self.structural_elements[element.index].element_type:
                    self.check_set_fluid = True
                    return

            if element.cross_section is None:
                self.check_set_crossSection = True
                return

            if self.structural_elements[element.index].element_type == 'expansion_joint':
                if element.cross_section.area_fluid == 0:
                    self.check_set_crossSection = True
                    return
            else:    
                if element.cross_section.thickness == 0:
                    if element.cross_section.area == 0:
                        self.check_set_crossSection = True
                        return


    def check_fluid_inputs_in_all_elements(self):
        """
        This method checks if each acoustic element has the necessary fluid data to evaluate the analysis according to its element type.
        """
        self.check_all_fluid_inputs = False
        for element in self.acoustic_elements.values():
            if element.element_type in ['wide-duct', 'LRF fluid equivalent', 'LRF full']:
                if 'pipe_' in self.structural_elements[element.index].element_type:
                    _list = [   element.fluid.isentropic_exponent, element.fluid.thermal_conductivity, 
                                element.fluid.specific_heat_Cp, element.fluid.dynamic_viscosity   ]
                    if None in _list:
                        self.check_all_fluid_inputs = True
                        return


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
        
        message_plane_wave = "flag_plane_wave"
        message_wide_duct = "flag_wide_duct"
        message_lrf_fluid_eq = "flag_lrf_fluid_eq"
        message_lrf_full = "flag_lrf_full"
        message_unflanged_radiation_impedance  = "The unflanged radiation impedance model is out of its validity frequency range. It is recommended to check the results carefully."

        for element in self.acoustic_elements.values():

            if element.flag_plane_wave and not flag_plane_wave:
                flag_plane_wave = True
                
            if element.flag_wide_duct and not flag_wide_duct:
                flag_wide_duct = True
                
            if element.flag_lrf_fluid_eq and not flag_lrf_fluid_eq:
                flag_lrf_fluid_eq = True
                
            if element.flag_lrf_full and not flag_lrf_full:
                flag_lrf_full = True
                
            if element.flag_unflanged_radiation_impedance and not flag_unflanged_radiation_impedance:
                flag_unflanged_radiation_impedance = True

        list_flags = [flag_plane_wave, flag_wide_duct, flag_lrf_fluid_eq, flag_lrf_full, flag_unflanged_radiation_impedance]
        list_messages = [message_plane_wave, message_wide_duct, message_lrf_fluid_eq, message_lrf_full, message_unflanged_radiation_impedance]

        for index, flag in enumerate(list_flags):
            if flag:
                PrintMessageInput([title, list_messages[index], window_title])


    def check_is_there_a_problem(self, analysis_ID):

        title = " Insufficient model inputs "

        cross_section_message = "You should to set a Cross-Section to all\n elements before trying to run any Analysis!"
        material_message = "You should to set a Material to all elements\n before trying to run any Analysis!"
        fluid_message = "You should to set a Fluid to all elements\n before trying to run any Analysis!"
        all_fluid_inputs_message = "You should insert all fluid properties for wide-duct, LRF \nfluid equivalent and LRF full acoustic element types."
        structural_message = "You should to apply an external load to the model or prescribe a \nnon-null DOF value before trying to solve the Harmonic Analysis!"
        acoustic_message = "You should to insert a Volume Velocity or prescribe an Acoustic \nPressure to a node before trying to solve the Harmonic Analysis!"
    
        if analysis_ID == 2:
            self.check_material_and_cross_section_in_all_elements()
            if self.check_set_material:
                PrintMessageInput([title, material_message, window_title_1])
                return True
            elif self.check_set_crossSection:
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
        
        elif analysis_ID == 4:
            self.check_material_all_elements()
            self.check_fluid_and_cross_section_in_all_elements()
            self.check_fluid_inputs_in_all_elements()
            if self.check_set_material:
                PrintMessageInput([title, material_message, window_title_1])
                return True
            elif self.check_set_fluid:
                PrintMessageInput([title, fluid_message, window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                PrintMessageInput([title, all_fluid_inputs_message, window_title_1])
                return True
            elif self.check_set_crossSection:
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True

        elif analysis_ID == 0 or analysis_ID == 1:
            self.check_material_and_cross_section_in_all_elements()
            self.check_nodes_attributes(structural=True)
            if self.check_set_material:
                PrintMessageInput([title, material_message, window_title_1])
                return True
            elif self.check_set_crossSection:
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_loads:
                if not self.is_there_prescribed_dofs:
                    PrintMessageInput([title, structural_message, window_title_1])
                    return True
    
        elif analysis_ID == 3:
            self.check_material_all_elements()
            self.check_fluid_and_cross_section_in_all_elements()
            self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(acoustic=True)
            if self.check_set_fluid:
                PrintMessageInput([title, fluid_message, window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                PrintMessageInput([title, all_fluid_inputs_message, window_title_1])
                return True
            elif self.check_set_material:
                PrintMessageInput([title, material_message, window_title_1])
                return True
            elif self.check_set_crossSection:
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([title, acoustic_message, window_title_1])
                    return True

        elif analysis_ID == 5 or analysis_ID == 6:
            self.check_material_and_cross_section_in_all_elements()
            self.check_fluid_and_cross_section_in_all_elements()
            self.check_fluid_inputs_in_all_elements()
            self.check_nodes_attributes(coupled=True)
            if self.check_set_material:
                PrintMessageInput([title, material_message, window_title_1])
                return True
            elif self.check_set_fluid:
                PrintMessageInput([title, fluid_message, window_title_1])
                return True
            elif self.check_all_fluid_inputs:
                PrintMessageInput([title, all_fluid_inputs_message, window_title_1])
                return True
            elif self.check_set_crossSection:
                PrintMessageInput([title, cross_section_message, window_title_1])
                return True
            elif not self.is_there_volume_velocity:
                if not self.is_there_acoustic_pressure:
                    PrintMessageInput([title, acoustic_message, window_title_1])
                    return True