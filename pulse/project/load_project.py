from typing import TYPE_CHECKING

from pulse import VERSION
from pulse.interface import error_title, warning_title
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.c_beam_cross_section import CBeamCrossSection
from pulse.model.cross_sections.circular_beam_cross_section import (
    CircularBeamCrossSection,
)
from pulse.model.cross_sections.generic_beam_cross_section import (
    GenericBeamCrossSection,
)
from pulse.model.cross_sections.i_beam_cross_section import IBeamCrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.cross_sections.rectangular_beam_cross_section import (
    RectangularBeamCrossSection,
)
from pulse.model.cross_sections.t_beam_cross_section import TBeamCrossSection
from pulse.model.perforated_plate import PerforatedPlate
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material

if TYPE_CHECKING:
    from pulse.project.project import Project

import logging
from collections import defaultdict

import numpy as np
from packaging.version import Version


class LoadProject:
    def __init__(self, project: "Project"):
        super().__init__()

        self.project = project
        self.properties = project.model.properties
        self.preprocessor = project.model.preprocessor

        self._initialize()


    def _initialize(self):
        pass


    def reset_model_properties(self):
        self.properties.line_properties.clear()
        self.properties.nodal_properties.clear()
        self.properties.element_properties.clear()


    def load_project_data(self):
        #
        self.reset_model_properties()
        #
        self.load_mesh_setup_from_file()
        self.load_imported_table_data_from_file()
        #
        self.load_fluids_library()
        self.load_materials_library()

        if self.check_line_properties():
            return True

        self.load_cross_sections_from_file()
        #
        self.load_lines_properties()
        self.load_element_properties()
        self.load_nodal_properties()
        #
        self.load_analysis_setup()
        self.load_inertia_load_setup()


    def load_fluids_library(self) -> dict:

        self.fluids_library = dict()
        fluid_library_data = self.project.file.read_fluid_library_from_file()
        if fluid_library_data is None:
            return dict()

        for str_fluid_id, fluid_data in fluid_library_data.items():
            if not isinstance(fluid_data, dict):
                continue

            fluid = Fluid(**fluid_data)
            self.fluids_library[int(str_fluid_id)] = fluid

        self.properties.set_fluids_library(self.fluids_library)

        return self.fluids_library


    def load_materials_library(self):

        self.materials_library = dict()
        material_library_data = self.project.file.read_material_library_from_file()
        if material_library_data is None:
            return

        for str_material_id, material_data in material_library_data.items():
            if not isinstance(material_data, dict):
                continue

            material = Material(**material_data)
            self.materials_library[int(str_material_id)] = material

        self.properties.set_materials_library(self.materials_library)

        return self.materials_library


    def check_line_properties(self):

        line_properties = self.project.file.read_line_properties_from_file()
        if line_properties is None:
            return True
        elif isinstance(line_properties, dict):
            if len(line_properties) == 0:
                return True
            else:
                return False
        else:
            return False


    def load_cross_sections_from_file(self):

        self.cross_sections = dict()
        line_properties = self.project.file.read_line_properties_from_file()
        if line_properties is None:
            return

        for line_id, data in line_properties.items():

            if "section_type_label" in data.keys() and "section_parameters" in data.keys():
                section_type_label = self.fix_data_for_backwards_compatibility(data)

                if data.get("structure_name") in ["pipe", "bend", "arc_bend", "flange"]:

                    pipe_section_info = PipeCrossSection(*data["section_parameters"])

                    self.cross_sections[line_id] = CrossSection(
                        element_type = "pipe_1",
                        pipe_section_info = pipe_section_info,
                    )

                elif "section_properties" in data.keys():

                    section_parameters = data["section_parameters"]
                    match section_type_label:
                        case "circular_beam":
                            beam_section_info = CircularBeamCrossSection(*section_parameters)
                        case "rectangular_beam":
                            beam_section_info = RectangularBeamCrossSection(*section_parameters)
                        case "c_beam":
                            beam_section_info = CBeamCrossSection(*section_parameters)
                        case "i_beam":
                            beam_section_info = IBeamCrossSection(*section_parameters)
                        case "t_beam":
                            beam_section_info = TBeamCrossSection(*section_parameters)
                        case "generic_beam":
                            beam_section_info = GenericBeamCrossSection(*section_parameters)
                        case _:
                            continue

                    self.cross_sections[line_id] = CrossSection(
                        element_type = "beam_1",
                        beam_section_info = beam_section_info,
                    )

    def fix_data_for_backwards_compatibility(self, data: dict):

        sections_types = [
            "Pipe", 
            "Rectangular section", 
            "Circular section", 
            "C-section", 
            "I-section", 
            "T-section", 
            "Generic section",
            "Valve",
            "Expansion joint",
            "Reducer",
            "Flange"
            ]

        if data.get("section_type_label") in sections_types:
            type_label: str = data.get("section_type_label")
            return type_label.lower().replace(" ", "_").replace("-", "_").replace("section", "beam")

        return data.get("section_type_label")


    def load_lines_properties(self):

        line_properties = self.project.file.read_line_properties_from_file()
        if line_properties is None:
            return

        for line_id, data in line_properties.items():

            if line_id in self.cross_sections.keys():
                cross_section = self.cross_sections[line_id]
                self.properties._set_line_property("cross_section", cross_section, line_ids=int(line_id))

            if isinstance(data, dict):
                for property, prop_data in data.items():

                    if property == "fluid_id":
                        fluid_id = prop_data
                        self.properties._set_line_property(property, fluid_id, line_ids=int(line_id))

                        if fluid_id not in self.fluids_library.keys():
                            continue

                        fluid = self.fluids_library[fluid_id]
                        self.properties._set_line_property("fluid", fluid, line_ids=int(line_id))

                    elif property == "material_id":
                        material_id = prop_data
                        self.properties._set_line_property(property, material_id, line_ids=int(line_id))
    
                        if material_id not in self.materials_library.keys():
                            continue

                        material = self.materials_library[material_id]
                        self.properties._set_line_property("material", material, line_ids=int(line_id))
                    
                    else:

                        self.properties._set_line_property(property, prop_data, line_ids=int(line_id))


    def load_element_properties(self):
        element_properties = self.project.file.load_element_properties_from_file()
        for (property, id), prop_data in element_properties.items():
            self.properties._set_element_property(property, prop_data, element_ids=id)


    def load_nodal_properties(self):
        nodal_properties = self.project.file.load_nodal_properties_from_file()
        for (property, *args), prop_data in nodal_properties.items():
            self.properties._set_nodal_property(property, prop_data, node_ids=args)


    def send_lines_properties_to_elements(self):
        for line_id, data in self.properties.line_properties.items():

            # general
            self.load_cross_sections(line_id, data)

            # acoustic
            self.load_fluids(line_id, data)
            self.load_acoustic_element_types(line_id, data)

            # structural
            self.load_materials(line_id, data)
            self.load_structural_element_types(line_id, data)
            self.load_capped_ends(line_id, data)
            self.load_force_offsets(line_id, data)
            self.load_wall_formulations(line_id, data)
            self.load_beam_xaxis_rotations(line_id, data)

            self.load_expansion_joints(line_id, data)
            self.load_valves(line_id, data)
            self.load_stress_stiffening(line_id, data)


    def send_element_properties_to_elements(self):
        for (property, element_id), prop_data in self.properties.element_properties.items():

            if property == "B2P_rotation_decoupling":
                self.preprocessor.set_B2P_rotation_decoupling(element_id, prop_data)

            elif property == "element_length_correction":
                self.preprocessor.set_element_length_correction_by_element(element_id, prop_data)

            elif property == "perforated_plate":
                perforated_plate = PerforatedPlate(prop_data)
                self.preprocessor.set_perforated_plate_by_elements(element_id, perforated_plate)

            elif property == "acoustic_element_turned_off":
                self.preprocessor.set_elements_to_ignore_in_acoustic_analysis(element_id, True)


    def load_mesh_dependent_properties(self):
        """ This methods send properties to elements.
        """
        self.send_lines_properties_to_elements()
        self.update_node_ids_after_mesh_changed()
        self.update_element_ids_after_mesh_changed()
        self.send_element_properties_to_elements()


    def load_expansion_joints(self, line_id: int, data: dict):

        prop_data = data.get("expansion_joint_info")
        if not isinstance(prop_data, dict):
            return

        prop_data["joint_length"] = self.properties.get_line_length(line_id)

        if "effective_diameter" not in prop_data.keys():
            return
    
        self.preprocessor.add_expansion_joint_by_lines(
            line_id, 
            prop_data,
            )

        self.preprocessor.set_cross_sections_to_expansion_joint(
            line_id, 
            prop_data,
            )


    def load_valves(self, line_id: int, data: dict):

        prop_data = data.get("valve_info")
        if not isinstance(prop_data, dict):
            return

        prop_data["valve_length"] = self.properties.get_line_length(line_id)

        self.preprocessor.add_valve_by_lines(line_id, prop_data)
        self.preprocessor.set_cross_sections_to_valve_elements(line_id, data)


    def load_stress_stiffening(self, line_id: list, data: dict):

        prop_data = data.get("stress_stiffening")
        if not isinstance(prop_data, dict):
            return

        self.preprocessor.set_stress_stiffening_by_lines(line_id, prop_data)


    def load_cross_sections(self, line_id: list, data: dict):

        if "cross_section" in data.keys():
            cross_section = data["cross_section"]
            self.preprocessor.set_cross_section_by_lines(line_id, cross_section)

        elif "section_type_label" in data.keys():
            section_type_label = self.fix_data_for_backwards_compatibility(data)
            if section_type_label == "reducer":
                self.preprocessor.set_variable_cross_section_by_line(line_id, data)


    def load_fluids(self, line_id: int, data: dict):
        fluid = data.get("fluid")
        self.preprocessor.set_fluid_by_lines(line_id, fluid)


    def load_acoustic_element_types(self, line_id: int, data: dict):
        acoustic_element_type = data.get("acoustic_element_type", "undamped")
        proportional_damping = data.get("proportional_damping")
        volumetric_flow_rate = data.get("volumetric_flow_rate")
        self.preprocessor.set_acoustic_element_type_by_lines(   
                                                             line_id, 
                                                             acoustic_element_type, 
                                                             proportional_damping = proportional_damping,
                                                             volumetric_flow_rate = volumetric_flow_rate    
                                                             )


    def load_materials(self, line_id: int, data: dict):
        material = data.get("material")
        self.preprocessor.set_material_by_lines(line_id, material)


    def load_structural_element_types(self, line_id: int, data: dict):
        element_type = data.get("structural_element_type")
        self.preprocessor.set_structural_element_type_by_lines(line_id, element_type)


    def load_capped_ends(self, line_id: int, data: dict):
        capped_end = data.get("capped_end", True)
        self.preprocessor.set_capped_end_by_lines(line_id, capped_end)


    def load_force_offsets(self, line_id: int, data: dict):
        force_offset = data.get("force_offset", True)
        self.preprocessor.set_structural_element_force_offset_by_lines(line_id, force_offset)


    def load_wall_formulations(self, line_id: int, data: dict):
        wall_formulation = data.get("wall_formulation", "thin_wall")
        self.preprocessor.set_structural_element_wall_formulation_by_lines(line_id, wall_formulation)


    def load_beam_xaxis_rotations(self, line_id: int, data: dict):
        xaxis_beam_rotation = data.get("beam_xaxis_rotation", 0)
        self.preprocessor.set_beam_xaxis_rotation_by_lines(line_id, xaxis_beam_rotation)


    def load_imported_table_data_from_file(self):
        imported_tables = self.project.file.load_imported_table_data_from_file()
        if "acoustic" in imported_tables.keys():
            self.project.model.properties.acoustic_imported_tables = imported_tables["acoustic"]
        if "structural" in imported_tables.keys():
            self.project.model.properties.structural_imported_tables = imported_tables["structural"]


    def check_file_version(self):

        project_setup = self.project.file.read_project_setup_from_file()
        if project_setup is None:
            title = "There is something wrong with your project"
            message = "The project file is incompatible with the .pulse file structure. "
            message += "As a result, the project data loading will be canceled."
            PrintMessageInput([error_title, title, message])
            return True

        if "version" in project_setup.keys():
            file_version = project_setup["version"]
        else:
            #TODO: remove this as soon as possible
            file_version = VERSION

        software_version = VERSION
        if Version(file_version) > Version(software_version):
            title = "Incorrect file version"
            message = "The project file version is incompatible with the current OpenPulse version. "
            message += "As a result, the project data loading will be canceled."
            PrintMessageInput([error_title, title, message])
            return True


    def load_mesh_setup_from_file(self):

        project_setup = self.project.file.read_project_setup_from_file()
        if project_setup is None:
            return

        if "mesher_setup" in project_setup.keys():
            self.preprocessor.mesh.set_mesher_setup(mesher_setup=project_setup["mesher_setup"])


    def load_inertia_load_setup(self):

        inertia_load = self.project.file.read_inertia_load_from_file()
        if inertia_load is None:
            return

        gravity = np.array(inertia_load["gravity"], dtype=float)
        stiffening_effect = inertia_load["stiffening_effect"]

        self.project.model.set_gravity_vector(gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)


    def load_analysis_setup(self):
        analysis_setup = self.project.file.load_analysis_file()
        if isinstance(analysis_setup, dict):
            self.project.model.set_analysis_setup(analysis_setup)


    def get_psd_related_lines(self):

        psd_lines = defaultdict(list)
        for line_id, data in self.properties.line_properties.items():

            data: dict
            if "psd_label" in data.keys():
                psd_label = data["psd_label"]
                psd_lines[psd_label].append(line_id)

        return psd_lines


    def get_pulsation_damper_related_lines(self):
        pulsation_damper_lines = defaultdict(list)
        for line_id, data in self.properties.line_properties.items():

            data: dict
            if "pulsation_damper_label" in data.keys():
                pulsation_damper_name = data["pulsation_damper_label"]
                pulsation_damper_lines[pulsation_damper_name].append(line_id)

        return pulsation_damper_lines


    def get_cross_sections_from_file(self):
        """ This method returns a dictionary of already applied cross-sections.
        """
        try:

            count_A = 1
            section_info = dict()
            parameters_to_line_id = defaultdict(list)

            for line_id, data in self.properties.line_properties.items():

                data: dict
                if "structural_element_type" in data.keys():
                    element_type = data["structural_element_type"]
                else:
                    continue

                if "section_type_label" in data.keys():
                    section_type = data["section_type_label"]
                else:
                    continue

                if section_type in ["valve", "expansion_joint", "generic_beam"]:
                    continue

                if "section_parameters" in data.keys():
                    section_parameters = data["section_parameters"]
                else:
                    continue

                if str(section_parameters) not in parameters_to_line_id.keys():
                    section_info[count_A] = [element_type, section_parameters, section_type]
                    count_A += 1

                parameters_to_line_id[str(section_parameters)].append(line_id)

            count_B = 0
            section_info_lines = dict()

            for _data in section_info.values():

                _data: list
                _section_parameters = _data[1]

                if str(_section_parameters) in parameters_to_line_id.keys():
                    count_B += 1
                    aux = _data.copy()
                    line_ids = parameters_to_line_id[str(_section_parameters)]
                    aux.append(line_ids)
                    section_info_lines[count_B] = aux

        except Exception as error_log:

            title = "Error while processing cross-sections"
            message = "Error detected while processing the 'get_cross_sections_from_file' method.\n\n"
            message += f"Last line id: {line_id}\n\n"
            message += f"Details: \n\n {str(error_log)}"
            PrintMessageInput([error_title, title, message])

            return dict()

        return section_info_lines

    def update_node_ids_after_mesh_changed(self):

        aux_nodal = dict()
        non_mapped_nodes = list()
        internal_impedances = list()
        property_to_remove = dict()

        for key, data in self.properties.nodal_properties.items():

            (property, *args) = key

            if "coords" not in data.keys():
                continue
        
            coords = np.array(data["coords"], dtype=float)

            # two nodes-related boundary conditions id mapping
            if len(coords) == 6:

                node_id1, node_id2 = args

                coords_1 = coords[:3]
                coords_2 = coords[3:]
                new_node_id1 = self.preprocessor.get_node_id_by_coordinates(coords_1)
                new_node_id2 = self.preprocessor.get_node_id_by_coordinates(coords_2)

                if (new_node_id1, new_node_id2).count(None):
                    property_to_remove[property] = args

                if new_node_id1 is None:
                    non_mapped_nodes.append((node_id1, coords_1))

                if new_node_id2 is None:
                    non_mapped_nodes.append((node_id2, coords_2))

                if (new_node_id1, new_node_id2).count(None):
                    continue

                sorted_indexes = np.sort([new_node_id1, new_node_id2])
                new_key = (property, sorted_indexes[0], sorted_indexes[1])

            # one node-related boundary conditions id mapping
            elif len(coords) == 3:

                node_id = args
                new_node_id = self.preprocessor.get_node_id_by_coordinates(coords)
                new_key = (property, new_node_id)

                if new_node_id is None:
                    non_mapped_nodes.append((node_id, coords))
                    continue

                if property in ["radiation_impedance", "specific_impedance"]:        
                    neigh_elements = self.preprocessor.structural_elements_connected_to_node.get(new_node_id)
                    if isinstance(neigh_elements, list):
                        if len(neigh_elements) != 1:
                            internal_impedances.append((new_node_id, coords))
                            property_to_remove[property] = args                 
                            continue

            aux_nodal[new_key] = data
    
        if aux_nodal == self.properties.nodal_properties:
            return
        
        if property_to_remove:
            for property, node_ids in property_to_remove.items():
                self.properties._remove_nodal_property(property, node_ids)

            self.project.file.write_imported_table_data_in_file()

        # replace all nodal properties if anything has changed
        self.properties.nodal_properties.clear()

        for new_key, data in aux_nodal.items():
            (property, *args) = new_key
            self.properties._set_nodal_property(property, data, args)

        if aux_nodal:
            self.project.file.write_nodal_properties_in_file()

        if non_mapped_nodes:
            title = "Nodal-related model attributions failed"
            message = "Some nodal-related model attributions could not be mapped "
            message += "after the meshing processing. The non-mapped nodes will be "
            message += "removed from nodal properties file."
            message += "\n\nDetails:"

            for (node_id, coords) in non_mapped_nodes:
                x, y, z = coords
                message += f"\nNode #{node_id} -> coordinates: ({x}, {y}, {z}) [m]"

            PrintMessageInput([warning_title, title, message])

        if internal_impedances:
            title = "Internal impedances detected"
            message = "Some acoustic impedances, whether radiation or specific, were detected in "
            message += "internal nodes (outside of termination) after the geometry had been edited. "
            message += "These impedances will be removed from nodal properties."
            message += "\n\nDetails:"

            for (node_id, coords) in internal_impedances:
                x, y, z = coords
                message += f"\nNode #{node_id} -> coordinates: ({x}, {y}, {z}) [m]"

            PrintMessageInput([warning_title, title, message])

    def update_element_ids_after_mesh_changed(self):

        aux_elements = dict()
        non_mapped_elements = list()

        for (property, element_id), data in self.properties.element_properties.items():
            if property in ["element_length_correction", "B2P_rotation_decoupling"]:

                if "coords" in data.keys():
                    coords = np.array(data["coords"], dtype=float)
                    node_id = self.preprocessor.get_node_id_by_coordinates(coords)

                    if isinstance(node_id, int):
                        if property == "B2P_rotation_decoupling":
                            neigh_elements = self.preprocessor.structural_elements_connected_to_node[node_id]
                        else:
                            neigh_elements = self.preprocessor.acoustic_elements_connected_to_node[node_id]

                        for element in neigh_elements:
                            if property == "B2P_rotation_decoupling":
                                if element.element_type != "beam_1":
                                    continue

                            new_key = (property, element.index)
                            aux_elements[new_key] = data

                    else:
                        non_mapped_elements.append((element_id, node_id))

        pp_removed = list()
        for (property, element_id), data in self.properties.element_properties.items():
            if property in ["perforated_plate", "acoustic_element_turned_off"]:

                coords = np.array(data["coords"], dtype=float)

                coords_1 = coords[:3]
                coords_2 = coords[3:]

                node_id1 = self.preprocessor.get_node_id_by_coordinates(coords_1)
                node_id2 = self.preprocessor.get_node_id_by_coordinates(coords_2)

                line_ids = list()
                for node_id in [node_id1, node_id2]:
                    for line_id in self.preprocessor.mesh.lines_from_node[node_id]:
                        if line_id not in line_ids:
                            line_ids.append(line_id)

                elements_from_lines = list()
                for line_id in line_ids:
                    elements = self.preprocessor.mesh.elements_from_line[line_id]
                    elements_from_lines.extend(elements)

                elements_inside_bounds = defaultdict(list)
                length = np.linalg.norm(coords_1 - coords_2)

                for _element_id in elements_from_lines:
                    element = self.preprocessor.structural_elements[_element_id]
                    ecc = element.center_coordinates

                    if np.linalg.norm(coords_1 - ecc) < length:
                        elements_inside_bounds[_element_id].append("first_node")

                    if np.linalg.norm(coords_2 - ecc) < length:
                        elements_inside_bounds[_element_id].append("last_node")

                external_elements = list()
                for _elem_id, node_label in elements_inside_bounds.items():
                    if len(node_label) == 1:
                        external_elements.append(_elem_id)

                # remove the external elements
                for external_element in external_elements:
                    elements_inside_bounds.pop(external_element)

                if property == "perforated_plate":
                    if len(elements_inside_bounds) != 1:
                        pp_removed.append(element_id) 
                        continue
 
                for _elem_id, node_label in elements_inside_bounds.items():
                    if len(node_label) == 2:
                        new_key = (property, _elem_id)
                        aux_elements[new_key] = data

        if aux_elements != self.properties.element_properties:

            self.properties.element_properties.clear()

            for (_property, _element_id), data in aux_elements.items():
                self.properties._set_element_property(_property, data, int(_element_id))

            if aux_elements:
                self.project.file.write_element_properties_in_file()

            if non_mapped_elements:

                title = "Element-related model attributions failed"
                message = "Some element-related model attributions could not be mapped "
                message += "after the meshing processing. \n\nDetails:"

                for (node_id, coords) in non_mapped_elements:
                    message += f"\n{node_id} - {coords}"

                PrintMessageInput([warning_title, title, message])

        if pp_removed:
            title = "Perforated plates removed"
            message = "Some perforated plates could not be mapped after the "
            message += "meshing processing, therefore, they were removed "
            message += "from both the project files and model setup."
            PrintMessageInput([warning_title, title, message])

    def load_analysis_results(self):
    
        act_modal_analysis = False
        str_modal_analysis = False
        act_harmonic_analysis = False
        str_harmonic_analysis = False
        # str_static_analysis = False

        results_data = self.project.file.read_results_data_from_file()

        if results_data:
            logging.info("Loading results [10%]")
            for key, data in results_data.items():

                if key == "modal_acoustic":
                    act_modal_analysis = True
                    if np.iscomplexobj(data["natural_frequencies"]):
                        self.project.complex_natural_frequencies_acoustic = data["natural_frequencies"]
                    else:
                        self.project.natural_frequencies_acoustic = data["natural_frequencies"]
                    self.project.acoustic_solution = data["modal_shape"]

                if key == "modal_structural":
                    str_modal_analysis = True
                    self.project.natural_frequencies_structural = data["natural_frequencies"]
                    self.project.structural_solution = data["modal_shape"]

                if key == "harmonic_acoustic":
                    act_harmonic_analysis = True
                    self.project.model.frequencies = data["frequencies"]
                    self.project.acoustic_solution = data["solution"]

                if key == "harmonic_structural":
                    str_harmonic_analysis = True
                    self.project.model.frequencies = data["frequencies"]
                    self.project.structural_solution = data["solution"]

                if key == "static_structural":
                    # str_static_analysis = True
                    self.project.structural_solution = data["solution"]

            logging.info("Updating analysis render [75%]")
            if act_modal_analysis:
                pass

            elif str_modal_analysis:
                pass

            elif act_harmonic_analysis:
                pass

            elif str_harmonic_analysis:
                return

            else:
                return