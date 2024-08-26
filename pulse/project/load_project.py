# fmt: off

from pulse import app

from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse.model.perforated_plate import PerforatedPlate

from pulse.interface.user_input.model.setup.structural.expansion_joint_input import get_cross_sections_to_plot_expansion_joint
from pulse.interface.user_input.project.print_message import PrintMessageInput
from pulse.tools.utils import *

from pulse.model.cross_section import CrossSection

from time import time
from collections import defaultdict

window_title_1 = "Error"
window_title_2 = "Warning"

class LoadProject:
    def __init__(self):
        super().__init__()

        self.project = app().project
        self.model = app().project.model
        self.properties = app().project.model.properties
        self.preprocessor = app().project.preprocessor

        self._initialize()
        
    def _initialize(self):
        self.bc_loader = None

    def load_project_data(self):
        #
        self.load_mesh_setup_from_file()
        self.load_imported_table_data_from_file()
        #
        self.load_fluids_library()
        self.load_materials_library()
        self.load_cross_sectionss()
        #
        self.load_lines_properties()
        self.load_element_properties()
        self.load_nodal_properties()
        #
        self.load_analysis_file()
        self.load_inertia_load_setup()

    def load_fluids_library(self):

        self.library_fluids = dict()
        config = app().pulse_file.read_fluid_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            keys = section.keys()

            name = section['name']
            density =  float(section['density'])
            speed_of_sound =  float(section['speed_of_sound'])
            identifier =  int(section['identifier'])
            color =  get_color_rgb(section['color'])

            if len(color) == 4:
                color = color[:3]

            if 'isentropic_exponent' in keys:
                isentropic_exponent = float(section['isentropic_exponent'])
            else:
                isentropic_exponent = ""

            if 'thermal_conductivity' in keys:
                thermal_conductivity = float(section['thermal_conductivity'])
            else:
                thermal_conductivity = ""

            if 'specific_heat_Cp' in keys:
                specific_heat_Cp = float(section['specific_heat_Cp'])
            else:
                specific_heat_Cp = ""

            if 'dynamic_viscosity' in keys:
                dynamic_viscosity = float(section['dynamic_viscosity'])
            else:
                dynamic_viscosity = ""
            
            if 'temperature' in keys:
                temperature = float(section['temperature'])
            else:
                temperature = None

            if 'pressure' in keys:
                pressure = float(section['pressure'])
            else:
                pressure = None

            # if 'key mixture' in keys:
            #     key_mixture = section['key mixture']
            # else:
            #     key_mixture = None

            # if 'molar fractions' in keys:
            #     str_molar_fractions = section['molar fractions']
            #     molar_fractions = get_list_of_values_from_string(str_molar_fractions, int_values=False)
            # else:
            #     molar_fractions = None

            if "molar_mass" in keys:
                if section["molar_mass"] == "None":
                    molar_mass = None
                else:
                    molar_mass = float(section["molar_mass"])
            else:
                molar_mass = None

            fluid = Fluid(  name = name,
                            density = density,
                            speed_of_sound = speed_of_sound,
                            color =  color,
                            identifier = identifier,
                            isentropic_exponent = isentropic_exponent,
                            thermal_conductivity = thermal_conductivity,
                            specific_heat_Cp = specific_heat_Cp,
                            dynamic_viscosity = dynamic_viscosity,
                            temperature = temperature,
                            pressure = pressure,
                            molar_mass = molar_mass  )
            
            self.library_fluids[identifier] = fluid

    def load_materials_library(self):

        self.library_materials = dict()
        config = app().pulse_file.read_material_library_from_file()

        if config is None:
            return

        for tag in config.sections():

            section = config[tag]
            # keys = section.keys()

            name = section['name']
            identifier = int(section['identifier'])
            density = float(section['density'])
            poisson_ratio = float(section['poisson_ratio'])
            elasticity_modulus = float(section['elasticity_modulus']) * 1e9
            thermal_expansion_coefficient = float(section['thermal_expansion_coefficient'])
            color =  get_color_rgb(section['color'])

            if len(color) == 4:
                color = color[:3]

            material = Material(
                                name = name,
                                identifier = identifier, 
                                density = density,
                                poisson_ratio = poisson_ratio,
                                elasticity_modulus = elasticity_modulus,
                                thermal_expansion_coefficient = thermal_expansion_coefficient, 
                                color = color
                                )
            
            self.library_materials[identifier] = material

    def load_cross_sectionss(self):

        self.cross_sections = dict()
        line_properties = app().pulse_file.read_line_properties_from_file()
        if line_properties is None:
            return

        for line_id, data in line_properties.items():

            if "section_type_label" in data.keys() and "section_parameters" in data.keys():
                if data["section_type_label"] in ["Pipe", "Bend"]:

                    pipe_section_info = {   "section_type_label" : data["section_type_label"],
                                            "section_parameters" : data["section_parameters"]   }

                    self.cross_sections[line_id] = CrossSection(pipe_section_info=pipe_section_info) 
       
                elif "section_properties" in data.keys():

                    beam_section_info = {   "section_type_label" : data["section_type_label"],
                                            "section_parameters" : data["section_parameters"],
                                            "section_properties" : data["section_properties"]   }

                    self.cross_sections[line_id] = CrossSection(beam_section_info=beam_section_info)

    def load_lines_properties(self):

        line_properties = app().pulse_file.read_line_properties_from_file()
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

                        if fluid_id not in self.library_fluids.keys():
                            continue

                        fluid = self.library_fluids[fluid_id]
                        self.properties._set_line_property("fluid", fluid, line_ids=int(line_id))

                    elif property == "material_id":
                        material_id = prop_data
                        self.properties._set_line_property(property, material_id, line_ids=int(line_id))
    
                        if material_id not in self.library_materials.keys():
                            continue

                        material = self.library_materials[material_id]
                        self.properties._set_line_property("material", material, line_ids=int(line_id))
                    
                    else:

                        self.properties._set_line_property(property, prop_data, line_ids=int(line_id))
        
        from pprint import pprint
        pprint(line_properties)

    def load_element_properties(self):
        element_properties = app().pulse_file.load_element_properties_from_file()
        for (property, id), prop_data in element_properties.items():
            self.properties._set_element_property(property, prop_data, element_ids=id)

    def load_nodal_properties(self):
        nodal_properties = app().pulse_file.load_nodal_properties_from_file()
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
            if property == "element_length_correction":
                self.preprocessor.set_element_length_correction_by_element(element_id, prop_data)
            if property == "perforated_plate":
                perforated_plate = PerforatedPlate(prop_data)
                self.preprocessor.set_perforated_plate_by_elements(element_id, perforated_plate)

    def load_mesh_dependent_properties(self):
        """ This methods send properties to elements.
        """
        self.send_lines_properties_to_elements()
        self.send_element_properties_to_elements()

    ## line loaders

    def load_expansion_joints(self, line_id: list, data: dict):

        expansion_joint = None
        if "expansion_joint" in data.keys():
            expansion_joint = data["expansion_joint"]

        if isinstance(expansion_joint, dict):

            joint_elements = self.model.mesh.line_to_elements[line_id]
            if "effective_diameter" in expansion_joint.keys():
                effective_diameter = expansion_joint["effective_diameter"]

                cross_sections = get_cross_sections_to_plot_expansion_joint(joint_elements, 
                                                                            effective_diameter)

                self.preprocessor.add_expansion_joint_by_lines(line_id, 
                                                            expansion_joint)

                self.preprocessor.set_cross_section_by_elements(joint_elements, 
                                                                cross_sections)

    def load_valves(self, line_id: list, data: dict):

        valves = None
        if "valves" in data.keys():
            valves = data["valves"]

        if valves is not None:
            self.preprocessor.add_valve_by_lines(line_id, valves)

    def load_stress_stiffening(self, line_id: list, data: dict):

        if "stress_stiffening" in data.keys():

            prop_data = data["stress_stiffening"]
            if isinstance(prop_data, dict):
                self.preprocessor.set_stress_stiffening_by_lines(line_id, prop_data)

    def load_cross_sections(self, line_id: list, data: dict):

        cross_section = None
        if "cross_section" in data.keys():

            cross_section = data["cross_section"]
            if data["section_type_label"] == "Reducer":
                self.preprocessor.set_variable_cross_section_by_line(line_id, cross_section)
                return

        self.preprocessor.set_cross_section_by_lines(line_id, cross_section)

    def load_fluids(self, line_id: int, data: dict):

        fluid = None
        if "fluid" in data.keys():
            fluid = data["fluid"]

        self.preprocessor.set_fluid_by_lines(line_id, fluid)

    def load_acoustic_element_types(self, line_id: int, data: dict):

        element_type = "undamped"
        if "acoustic_element_type" in data.keys():
            element_type = data["acoustic_element_type"]

        proportional_damping = None
        if "proportional_damping" in data.keys():
            proportional_damping = data["proportional_damping"]

        volume_flow = None
        if "volume_flow" in data.keys():
            volume_flow = data["volume_flow"]

        self.preprocessor.set_acoustic_element_type_by_lines(   
                                                             line_id, 
                                                             element_type, 
                                                             proportional_damping = proportional_damping,
                                                             vol_flow = volume_flow    
                                                             )

    def load_materials(self, line_id: int, data: dict):

        material = None
        if "material" in data.keys():
            material = data["material"]

        self.preprocessor.set_material_by_lines(line_id, material)

    def load_structural_element_types(self, line_id: int, data: dict):

        element_type = None
        if "structural_element_type" in data.keys():
            element_type = data["structural_element_type"]

        self.preprocessor.set_structural_element_type_by_lines(   
                                                                line_id, 
                                                                element_type  
                                                               )

    def load_capped_ends(self, line_id: int, data: dict):

        capped_end = None
        if "capped_end" in data.keys():
            capped_end = data["capped_end"]

        self.preprocessor.set_capped_end_by_lines(   
                                                    line_id, 
                                                    capped_end, 
                                                    )

    def load_force_offsets(self, line_id: int, data: dict):

        # force_offset = None
        if "force_offset" in data.keys():
            force_offset = data["force_offset"]

            self.preprocessor.set_structural_element_force_offset_by_lines(   
                                                                            line_id, 
                                                                            force_offset, 
                                                                        )

    def load_wall_formulations(self, line_id: int, data: dict):

        # wall_formulation = None
        if "wall_formulation" in data.keys():
            wall_formulation = data["wall_formulation"]

            self.preprocessor.set_structural_element_wall_formulation_by_lines(   
                                                                                line_id, 
                                                                                wall_formulation, 
                                                                               )

    def load_beam_xaxis_rotations(self, line_id: int, data: dict):

        xaxis_beam_rotation = 0
        if "beam_xaxis_rotation" in data.keys():
            xaxis_beam_rotation = data["beam_xaxis_rotation"]

        self.preprocessor.set_beam_xaxis_rotation_by_lines(   
                                                            line_id, 
                                                            xaxis_beam_rotation, 
                                                            )

    def set_element_properties(self):
        pass

    def load_imported_table_data_from_file(self):
        imported_tables = app().pulse_file.load_imported_table_data_from_file()
        if "acoustic" in imported_tables.keys():
            app().project.model.properties.acoustic_imported_tables = imported_tables["acoustic"]
        if "structural" in imported_tables.keys():
            app().project.model.properties.structural_imported_tables = imported_tables["structural"]

    def load_mesh_setup_from_file(self):

        project_setup = app().pulse_file.read_project_setup_from_file()
        if project_setup is None:
            return

        if "mesher setup" in project_setup.keys():
            self.preprocessor.mesh.set_mesher_setup(mesh_setup=project_setup["mesher setup"])

    def load_inertia_load_setup(self):

        inertia_load = app().pulse_file.read_inertia_load_from_file()
        if inertia_load is None:
            return

        gravity = np.array(inertia_load["gravity"], dtype=float)
        stiffening_effect = inertia_load["stiffening_effect"]

        self.project.model.set_gravity_vector(gravity)
        self.preprocessor.modify_stress_stiffening_effect(stiffening_effect)

    def load_analysis_file(self):

        analysis_setup = app().pulse_file.load_analysis_file()

        if analysis_setup is None:
            return

        self.model.set_frequency_setup(analysis_setup)
        self.model.set_global_damping(analysis_setup)

    def get_psd_related_lines(self):

        psd_lines = defaultdict(list)
        for line_id, data in self.properties.line_properties.items():

            data: dict
            if "psd_label" in data.keys():
                psd_label = data["psd_label"]
                psd_lines[psd_label].append(line_id)

        return psd_lines

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

                if "section_parameters" in data.keys():
                    section_parameters = data["section_parameters"]
                else:
                    continue

                if section_type in ["Valve", "Expansion joint", "Generic beam section"]:
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
            PrintMessageInput([window_title_1, title, message])

            return dict()

        return section_info_lines

# fmt: on