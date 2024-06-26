from pulse import app

import numpy as np


class ModelInfoText:
    def __init__(self, parent):
        super().__init__()

        self.opvRenderer = parent
        self.project = app().project
        self.preprocessor = self.project.preprocessor
        
    def get_nodes_info_text(self):
        selected_nodes = self.opvRenderer.getListPickedPoints()
        text = ""
        if len(selected_nodes) == 1:

            node = self.project.get_node(selected_nodes[0])
            node_id = selected_nodes[0]
            node_coords = "{:.4f}, {:.4f}, {:.4f}".format(node.x, node.y, node.z)

            text = f"Node ID: {node_id} ({node_coords}) [m]\n"

            if node in self.preprocessor.nodes_with_prescribed_dofs:
                values = node.prescribed_dofs
                labels = np.array(["ux", "uy", "uz", "rx", "ry", "rz"])
                unit_labels = ["m", "rad"]
                text += self.structural_nodal_info(values, labels, "Prescribed dofs", unit_labels, node.loaded_table_for_prescribed_dofs)

            if node in self.preprocessor.nodes_with_nodal_loads:
                values = node.nodal_loads
                labels = np.array(["Fx", "Fy", "Fz", "Mx", "My", "Mz"])
                unit_labels = ["N", "N.m"]
                text += self.structural_nodal_info(values, labels, "Nodal loads", unit_labels, node.loaded_table_for_nodal_loads)

            if node in self.preprocessor.nodes_connected_to_springs:
                values = node.lumped_stiffness
                labels = np.array(["kx", "ky", "kz", "krx", "kry", "krz"])
                unit_labels = ["N/m", "N.m/rad"]
                text += self.structural_nodal_info(values, labels, "Lumped stiffness", unit_labels, node.loaded_table_for_lumped_stiffness)

            if node in self.preprocessor.nodes_connected_to_dampers:
                values = node.lumped_dampings
                labels = np.array(["cx", "cy", "cz", "crx", "cry", "crz"])
                unit_labels = ["N.s/m", "N.m.s/rad"]
                text += self.structural_nodal_info(values, labels, "lumped dampings", unit_labels, node.loaded_table_for_lumped_dampings)

            if node in self.preprocessor.nodes_with_masses:
                values = node.lumped_masses
                labels = np.array(["mx", "my", "mz", "Jx", "Jy", "Jz"])
                unit_labels = ["kg", "N.m²"]
                text += self.structural_nodal_info(values, labels, "lumped masses", unit_labels, node.loaded_table_for_lumped_masses)

            if node.there_are_elastic_nodal_link_stiffness:
                index = node.external_index
                labels = np.array(["kx", "ky", "kz", "krx", "kry", "krz"])
                unit_labels = ["N/m", "N.m/rad"]
                for key, [_, values] in node.elastic_nodal_link_stiffness.items():
                    linked_nodes = [int(node_id) for node_id in key.split("-")]
                    if index in linked_nodes:            
                        text += self.structural_nodal_info(values, labels, f"Stiffness elastic link: [{key}]", unit_labels, node.loaded_table_for_elastic_link_stiffness)

            if node.there_are_elastic_nodal_link_dampings:
                index = node.external_index
                labels = np.array(["cx", "cy", "cz", "crx", "cry", "crz"])
                unit_labels = ["N.s/m", "N.m.s/rad"]
                for key, [_, values] in node.elastic_nodal_link_dampings.items():
                    linked_nodes = [int(node_id) for node_id in key.split("-")]
                    if index in linked_nodes:            
                        text += self.structural_nodal_info(values, labels, f"Damping elastic link: [{key}]", unit_labels, node.loaded_table_for_elastic_link_dampings)
 
            if node in self.preprocessor.nodes_with_acoustic_pressure:
                value = node.acoustic_pressure
                label = "P"
                unit_label = "[Pa]"
                text += self.acoustic_nodal_info(value, label, "Acoustic pressure", unit_label)
   
            if node in self.preprocessor.nodes_with_volume_velocity:
                value = node.volume_velocity
                label = "Q"
                unit_label = "[m³/s]"
                text += self.acoustic_nodal_info(value, label, "Volume velocity", unit_label)

            if node in self.preprocessor.nodes_with_compressor_excitation:
                value = node.volume_velocity
                label = "Q"
                unit_label = "[m³/s]"

                values_connection_info = list(node.dict_index_to_compressor_connection_info.values())         
                if len(values_connection_info) == 1:
                    connection_type = f"  Connection type: {values_connection_info[0]} \n"
                else:
                    if "discharge" in values_connection_info and "suction" in values_connection_info:
                        connection_type = f"  Connections types: discharge ({values_connection_info.count('discharge')}x) & "
                        connection_type += f"suction ({values_connection_info.count('suction')}x) \n"
                    elif "discharge" in values_connection_info:
                        connection_type = f"  Connections types: discharge ({values_connection_info.count('discharge')}x) \n"
                    elif "suction" in values_connection_info:
                        connection_type = f"  Connections types: suction ({values_connection_info.count('suction')}x) \n"    
                        
                bc_label = "Volume velocity - compressor excitation"
                text += self.acoustic_nodal_info(value, label, bc_label, unit_label, aditional_info=connection_type)
            
            if node in self.preprocessor.nodes_with_specific_impedance:
                value = node.specific_impedance
                label = "Zs"
                unit_label = "[kg/m².s]"
                text += self.acoustic_nodal_info(value, label, "Specific impedance", unit_label)

            if node in self.preprocessor.nodes_with_radiation_impedance:
                Z_type = node.radiation_impedance_type
                aux_dict = {0:"anechoic termination", 
                            1:"unflanged pipe", 
                            2:"flanged pipe"}
                label = "Type"
                value = aux_dict[Z_type]
                unit_label = ""
                text += self.acoustic_nodal_info(value, label, "Radiation impedance", unit_label)

        elif len(selected_nodes) > 1:
            text += f"{len(selected_nodes)} nodes in selection\n\n"
            for i, ids in enumerate(selected_nodes):
                if i == 30:
                    text += "..."
                    break
                text += f"{ids} "
                if i ==10 or i==20:
                    text += "\n"
            text += "\n"
        return text

    def structural_nodal_info(self, values, labels, bc_label, unit_labels, isThereTable):

        mask = [True if value is not None else False for value in values]
        indexes = np.arange(6)
        masked_labels = labels[mask]
        masked_indexes = indexes[mask]
        text = f"\n{bc_label}: \n"

        for index, label  in enumerate(masked_labels):
            if isThereTable:
                value = "Table"
                unit = ""
            else:
                value = values[masked_indexes[index]]
                if masked_indexes[index] in [0, 1, 2]:
                    unit = f"[{unit_labels[0]}]"
                else:
                    unit = f"[{unit_labels[1]}]"
            text += f"  {label} = {value} {unit} \n"

        return text

    def acoustic_nodal_info(self, value, label, bc_label, unit_label, aditional_info=None):
        text = f"\n{bc_label}: \n"
        if aditional_info is not None:
            text += aditional_info
        if isinstance(value, np.ndarray):
            text += f"  {label} = Table of values \n"
        else:
            unit = f"{unit_label}"
            text += f"  {label} = {value} {unit} \n"

        return text

    def get_elements_info_text(self):
    
        # selected_elements = self.opvRenderer.getListPickedElements()
        selected_elements = app().main_window.list_selected_elements()

        text = ""

        if len(selected_elements) == 1:

            structural_element = self.project.get_structural_element(selected_elements[0])
            acoustic_element = self.project.get_acoustic_element(selected_elements[0])
    
            first_node_coords = "{:.4f}, {:.4f}, {:.4f}".format(structural_element.first_node.x, 
                                                                structural_element.first_node.y, 
                                                                structural_element.first_node.z)

            last_node_coords = "{:.4f}, {:.4f}, {:.4f}".format(structural_element.last_node.x, 
                                                                structural_element.last_node.y, 
                                                                structural_element.last_node.z)

            structural_element_type = structural_element.element_type
            acoustic_element_type = acoustic_element.element_type

            material = structural_element.material
            fluid = acoustic_element.fluid
            
            if structural_element_type is None:
                structural_element_type = "undefined"

            if acoustic_element_type is None:
                acoustic_element_type = "undefined"

            if material is None:
                material_name = "undefined"
            else:
                material_name = material.name

            if fluid is None:
                fluid_name = "undefined"
            else:
                fluid_name = fluid.name
                fluid_temperature = fluid.temperature
                fluid_pressure = fluid.pressure

            if structural_element.cross_section is None: 
                outer_diameter = "undefined"
                thickness = "undefined"
                offset_y = "undefined"
                offset_z = "undefined"
                insulation_thickness = "undefined"
                insulation_density = "undefined"
            else:
                if structural_element.cross_section is not None:                 
                    if structural_element.element_type == "pipe_1":
                        outer_diameter = structural_element.cross_section.outer_diameter
                        thickness = structural_element.cross_section.thickness
                        offset_y = structural_element.cross_section.offset_y
                        offset_z = structural_element.cross_section.offset_z
                        insulation_thickness = structural_element.cross_section.insulation_thickness
                        insulation_density = structural_element.cross_section.insulation_density
                        structural_element_type = structural_element.element_type
                    
                    elif structural_element.element_type == "beam_1":
                        area = structural_element.cross_section.area
                        Iyy = structural_element.cross_section.second_moment_area_y
                        Izz = structural_element.cross_section.second_moment_area_z
                        Iyz = structural_element.cross_section.second_moment_area_yz
                        section_label = structural_element.cross_section.section_label
                        xaxis_rotation = structural_element.xaxis_beam_rotation

                        structural_element_type = f"{structural_element.element_type} ({section_label.capitalize()})"               

                    elif structural_element_type == "expansion_joint":
                        effective_diameter = structural_element.cross_section.outer_diameter

            # rotations = structural_element.section_rotation_xyz_undeformed
            # str_rotations = "{:.3f}, {:.3f}, {:.3f}".format(rotations[0], rotations[1], rotations[2])

            text += f"Element ID: {selected_elements[0]} \n\n"
            text += f"First Node ID: {structural_element.first_node.external_index} "
            text += f"({first_node_coords}) [m]\n"
            text += f" Last Node ID: {structural_element.last_node.external_index} "
            text += f"({last_node_coords}) [m]\n\n"
            # text += f"Rotations xyz: ({str_rotations})[deg]\n\n"
            text += f"Material: {material_name} \n"
            text += f"Strutural element type: {structural_element_type} \n\n"
            
            if "pipe_" in structural_element_type:        
                text += f"Diameter: {outer_diameter} [m]\n"
                text += f"Thickness: {thickness} [m]\n"
                if offset_y != 0 or offset_z != 0:
                    text += f"Offset y: {offset_y} [m]\n"
                    text += f"Offset z: {offset_z} [m]\n"

                if insulation_thickness != 0 or insulation_density != 0:
                    text += f"Insulation thickness: {insulation_thickness} [m]\n"
                    text += f"Insulation density: {insulation_density} [kg/m³]\n"

                if acoustic_element.fluid is not None:
                    text += f"\nFluid: {fluid_name} \n"
                    if fluid_temperature is not None:
                        text += f"\nTemperature: {fluid_temperature} [K]"
                    if fluid_pressure is not None:
                        text += f"\nPressure: {fluid_pressure} [Pa] \n" 

                if acoustic_element.element_type is not None:
                    text += f"\nAcoustic element type: {acoustic_element_type} \n"
                    if acoustic_element.element_type in ["undamped mean flow", "peters", "howe"]:
                        if acoustic_element.vol_flow:
                            text += f"Volume flow rate: {acoustic_element.vol_flow} [m³/s]\n"
                    elif acoustic_element.element_type in ["proportional"]:
                        if acoustic_element.proportional_damping:
                            text += f"Proportional damping: {acoustic_element.proportional_damping}\n"   
         
            elif "beam_1" in structural_element_type:
                text += f"Area:  {area} [m²]\n"
                text += f"Iyy:  {Iyy} [m^4]\n"
                text += f"Izz:  {Izz} [m^4]\n"
                text += f"Iyz:  {Iyz} [m^4]\n"
                text += f"x-axis rotation: {xaxis_rotation} [deg]\n"

            elif structural_element_type == "expansion_joint":
                text += f"Effective diameter: {effective_diameter} [m]\n"
            
        elif len(selected_elements) > 1:
            text += f"{len(selected_elements)} elements in selection\n\n"
            for i, ids in enumerate(selected_elements):
                if i == 30:
                    text += "..."
                    break
                text += f"{ids} "
                if i ==10 or i==20:
                    text += "\n"
        return text

    def get_entities_info_text(self):
        line_ids = self.opvRenderer.getListPickedLines()
        text = ""
        if len(line_ids) == 0: 
            return

        elif len(line_ids) == 1:

            entity = self.project.get_entity(line_ids[0])
            
            material = entity.material
            fluid = entity.fluid
            structural_element_type = entity.structural_element_type
            acoustic_element_type = entity.acoustic_element_type

            if material is None:
                material_name = "undefined"    
            else:
                material_name = material.name

            if fluid is None:
                fluid_name = "undefined"    
            else:
                fluid_name = fluid.name
                fluid_temperature = fluid.temperature
                fluid_pressure = fluid.pressure

            if entity.structural_element_type is None:
                structural_element_type = "undefined"

            if entity.cross_section is None:
                outer_diameter = "undefined"
                thickness = "undefined"
                offset_y = "undefined"
                offset_z = "undefined"
                insulation_thickness = "undefined"
                insulation_density = "undefined"
  
            if entity.tag in self.project.number_sections_by_line.keys():

                number_cross_sections = self.project.number_sections_by_line[entity.tag]
                text = f"Line ID  {line_ids[0]}\n"
                text += f"Number of cross-sections: {number_cross_sections}\n"
                if entity.tag in self.preprocessor.number_expansion_joints_by_lines.keys():
                    number_expansion_joints = self.preprocessor.number_expansion_joints_by_lines[entity.tag]
                    # text = f"Line ID  {line_ids[0]} ({number_cross_sections} cross-sections & {number_expansion_joints} expansion joints)\n\n"
                    text += f"Number of expansion joints: {number_expansion_joints}\n"
                if entity.tag in self.preprocessor.number_valves_by_lines.keys():
                    number_valves = self.preprocessor.number_valves_by_lines[entity.tag]
                    text += f"Number of valves: {number_valves}\n"
                # else:
                #     text = f"Line ID  {line_ids[0]} ({number_cross_sections} cross-sections)\n\n"              
                text += f"\nMaterial:  {material_name}\n"

                if structural_element_type in ["pipe_1", "valve"]:
                
                    outer_diameter = "multiples"
                    thickness = "multiples"
                    offset_y = "multiples"
                    offset_z = "multiples"
                    insulation_thickness = "multiples"
                    insulation_density = "multiples"

                    text += f"Structural element type:  {structural_element_type}\n"
              
                if entity.fluid is not None:
                    text += f"\nFluid: {fluid_name}" 
                    if fluid_temperature is not None:
                        text += f"\nTemperature: {fluid_temperature} [K]"
                    if fluid_pressure is not None:
                        text += f"\nPressure: {fluid_pressure} [Pa] \n" 

                if entity.acoustic_element_type is not None:
                    text += f"\nAcoustic element type: {acoustic_element_type}"
                if entity.acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                    if entity.vol_flow:
                        text += f"\nVolume flow rate: {entity.vol_flow} [m³/s]"
                elif entity.acoustic_element_type in ["proportional"]:
                    if entity.proportional_damping:
                        text += f"\nProportional damping: {entity.proportional_damping}"        
               
            else:

                text = ""
                text += f"Line ID  {line_ids[0]}\n\n"
                
                if entity.material is not None:
                    text += f"Material:  {entity.material.name}\n"

                text += f"Structural element type:  {structural_element_type}\n\n"

                if entity.cross_section is not None:
                    if entity.structural_element_type == "beam_1":

                        area = entity.cross_section.area
                        Iyy = entity.cross_section.second_moment_area_y
                        Izz = entity.cross_section.second_moment_area_z
                        Iyz = entity.cross_section.second_moment_area_yz
                        section_label = entity.getCrossSection().section_label
                        xaxis_rotation = entity.xaxis_beam_rotation

                        text += f"({section_label.capitalize()})\n\n"

                        text += f"Area:  {area} [m²]\n"
                        text += f"Iyy:  {Iyy} [m^4]\n"
                        text += f"Izz:  {Izz} [m^4]\n"
                        text += f"Iyz:  {Iyz} [m^4]\n"
                        text += f"x-axis rotation: {xaxis_rotation} [deg]\n"

                    elif entity.structural_element_type in ["pipe_1", "valve"]:

                        outer_diameter = entity.cross_section.outer_diameter
                        thickness = entity.cross_section.thickness
                        offset_y = entity.cross_section.offset_y
                        offset_z = entity.cross_section.offset_z
                        insulation_thickness = entity.cross_section.insulation_thickness
                        insulation_density = entity.cross_section.insulation_density
                                            
                        text += f"Outer diameter:  {outer_diameter} [m]\n"
                        text += f"Thickness:  {thickness} [m]\n"
                        if offset_y != 0 or offset_z != 0:
                            text += f"Offset y: {offset_y} [m]\nOffset z: {offset_z} [m]\n"
                        if insulation_thickness != 0 or insulation_density != 0: 
                            text += f"Insulation thickness: {insulation_thickness} [m]\n"
                            text += f"Insulation density: {int(insulation_density)} [kg/m³]\n"
                                                                           
                        if entity.fluid is not None:
                            text += f"\nFluid: {entity.fluid.name}" 
                            if fluid_temperature is not None:
                                text += f"\nTemperature: {fluid_temperature} [K]"
                            if fluid_pressure is not None:
                                text += f"\nPressure: {fluid_pressure} [Pa] \n" 

                        if entity.acoustic_element_type is not None:
                            text += f"\nAcoustic element type: {entity.acoustic_element_type}"

                        if entity.acoustic_element_type in ["undamped mean flow", "peters", "howe"]:
                            if entity.vol_flow:
                                text += f"\nVolume flow rate: {entity.vol_flow} [m³/s]"
                        elif entity.acoustic_element_type in ["proportional"]:
                            if entity.proportional_damping:
                                text += f"\nProportional damping: {entity.proportional_damping}" 
                
                if entity.expansion_joint_parameters is not None:
                    if entity.structural_element_type == "expansion_joint":
                        effective_diameter = entity.expansion_joint_parameters[0][1]
                        text += f"Structural element type:  {structural_element_type}\n\n"
                        text += f"Effective diameter:  {effective_diameter} [m]\n\n"

        else:

            text = f"{len(line_ids)} lines in selection\n\n"
            i = 0
            for ids in line_ids:
                if i == 30:
                    text += "..."

                    break
                elif i == 19: 
                    text += f"{ids}\n"
                elif i == 9:
                    text += f"{ids}\n"
                else:
                    text += f"{ids}  "
                i+=1
                
        return text