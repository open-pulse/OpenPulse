from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse import app

import numpy as np
from copy import deepcopy
from numbers import Number

DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    density=7860,
    elasticity_modulus=210e9,
    poisson_ratio=0.3,
    thermal_expansion_coefficient=1e-6,
    color=(200, 200, 200),
)

DEFAULT_FLUID = Fluid(
    name="Air",
    identifier=1,
    density=1.215,
    speed_of_sound=343.2021,
    color=(200, 200, 200),
)


class ModelProperties:
    """
    Class that stores all properties of a model.

    All properties can be setted per node, element, entity,
    volume or globally.

    The only functions that deals with data are _set_property,
    _get_property and _reset_property. All the others are just
    wrappers that call these ones.

    I know it may seem a little weird to structure the data this
    way because it would probably be faster to just use one dict
    for each property in each level of the structure.
    But the current approach is (I hope) a lot less error prone.
    It uses few dicts and we do not need to care if the data
    is handled correctly for each case, because few functions
    handles it, reducing the points of failure.

    Also, the speed is only a requirement on the retrieval of
    data (because it is done multiple times by every element),
    and it is pretty fast. The other operations are proportional
    to things that a human can put here manually (and by the real
    world requirements of the model), so of course a computer can
    handle it in fractions of a second.

    """

    def __init__(self, model=None):

        self._reset_variables()

    def _reset_variables(self):

        self.fluids_library = dict()
        self.materials_library = dict()

        self.acoustic_imported_tables = dict()
        self.structural_imported_tables = dict()

        self.global_properties = dict()
        self.line_properties: dict[str, dict] = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.valves_data = dict()
        self.expansion_joint_data = dict()

        self.global_properties["material", "global"] = DEFAULT_MATERIAL
        self.global_properties["fluid", "global"] = DEFAULT_FLUID

    def set_materials_library(self, materials_library: dict):
        self.materials_library = materials_library

    def set_fluids_library(self, fluids_library: dict):
        self.fluids_library = fluids_library

    def get_next_line_id(self):
        line_ids = list(self.line_properties.keys())
        if line_ids:
            return max(line_ids) + 1
        else:
            return 1

    def get_material(self, **kwargs) -> Material:
        return self._get_property("material", **kwargs)

    def get_fluid(self, **kwargs) -> Fluid:
        return self._get_property("fluid", **kwargs)

    def set_material(self, material: Material, line_ids):
        self._set_line_property("material", material, line_ids=line_ids)

    def set_fluid(self, fluid: Fluid, line_ids):
        self._set_line_property("fluid", fluid, line_ids=line_ids)

    def remove_compressor_table_name(self, node_id: int, table_name: str):
        key = ("reciprocating_compressor_excitation", node_id)
        if key in self.nodal_properties.keys():
            if table_name in self.nodal_properties[key]["table_names"]:
                self.nodal_properties[key]["table_names"].remove(table_name)

    def get_data_group_label(self, property : str):

        acoustic_labels = [ 
                            "acoustic_pressure", 
                            "volume_velocity", 
                            "specific_impedance", 
                            "radiation_impedance", 
                            "reciprocating_compressor_excitation",
                            "reciprocating_pump_excitation",
                            "acoustic_transfer_element"
                           ]

        if property in acoustic_labels:
            return "acoustic"
        else:
            return "structural"
        
    def get_table_values(self, property: str, table_names: list[str]) -> list[None | np.ndarray]:
        """
        This method returns all arrays assigned to a particular property.
        """
        tables_values = list()
        group_label = self.get_data_group_label(property)

        if group_label == "acoustic":
            imported_tables = self.acoustic_imported_tables
        else:
            imported_tables = self.structural_imported_tables

        for table_name in table_names:

            if table_name is None:
                tables_values.append(None)
                continue

            if table_name in imported_tables.keys():
                data_array = imported_tables[table_name]
                values = data_array[:, 1] + 1j*data_array[:, 2]
                tables_values.append(values)

        return tables_values

    def _set_nodal_property(self, property: str, data, node_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """

        if node_ids is None:
            return

        if "real_values" in data.keys() and "imag_values" in data.keys():
            values = list()
            for i, a in enumerate(data["real_values"]):
                if a is None:
                    values.append(None)
                else:
                    b = data["imag_values"][i]
                    values.append(a + 1j*b)

            data["values"] = values

        if "table_names" in data.keys():
            table_names = data.get("table_names", list())
            data["values"] = self.get_table_values(property, table_names)

        if isinstance(node_ids, Number):
            self.nodal_properties[property, node_ids] = data

        elif isinstance(node_ids, list | tuple) and len(node_ids) == 1:
            self.nodal_properties[property, node_ids[0]] = data

        elif isinstance(node_ids, list | tuple) and len(node_ids) == 2:
            self.nodal_properties[property, node_ids[0], node_ids[1]] = data

    def _set_element_property(self, property: str, data, element_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by element.

        """
        if element_ids is None:
            return
        
        elif isinstance(element_ids, Number):
            element_ids = [element_ids]

        for element_id in element_ids:
            self.element_properties[property, element_id] = data

    def _set_line_property(self, property: str, data, line_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by line.

        """
        if line_ids is None:
            return
        
        elif isinstance(line_ids, Number):
            line_ids = [line_ids]

        if isinstance(data, dict):
            if "values" not in data.keys():
                if "table_names" in data.keys():
                    table_names = data.get("table_names", list())
                    data["values"] = self.get_table_values(property, table_names)

        for line_id in line_ids:
            if line_id in self.line_properties.keys():
                self.line_properties[line_id][property] = data
            else:
                self.line_properties[line_id] = {property : data}

    def _set_multiple_line_properties(self, section_info: dict, line_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by line.

        """
        if line_ids is None:
            return
        
        elif isinstance(line_ids, Number):
            line_ids = [line_ids]

        for line_id in line_ids:
            for property, data in section_info.items():

                if line_id in self.line_properties.keys():
                        self.line_properties[line_id][property] = data
                else:
                    self.line_properties[line_id] = {property : data}

    def _get_property(self, property: str, node_ids=None, element_id=None, line_id=None):
        """
        Finds the value that corresponds to the property needed.
        Checks node, element, entity, volume and global data by
        this respective order of priority.
        If the any of this is defined returns None.
        """

        if isinstance(node_ids, Number):
            if (property, node_ids) in self.nodal_properties:
                return self.nodal_properties[property, node_ids]

        elif isinstance(node_ids, list) and len(node_ids) == 2:
            if (property, node_ids[0], node_ids[1]) in self.nodal_properties:
                return self.nodal_properties[property, node_ids[0], node_ids[1]]

        if (property, element_id) in self.element_properties:
            return self.element_properties[property, element_id]

        if line_id in self.line_properties.keys():
            if property in self.line_properties[line_id]:
                return self.line_properties[line_id][property]

        return None

    def material_is_applied_to_all_lines(self):
        lines = app().project.model.mesh.lines_from_model
        k = 0
        for line_data in self.line_properties.values():
            if "material" not in line_data.keys():
                return False
            k += 1

        return len(lines) == k

    def fluid_is_applied_to_all_lines(self):
        lines = app().project.model.mesh.lines_from_model
        k = 0
        for line_data in self.line_properties.values():
            if "fluid" not in line_data.keys():
                return False
            k += 1

        return len(lines) == k

    def is_the_property_applied(self, property: str) -> bool:
        if property == "material":
            return self.material_is_applied_to_all_lines()

        if property == "fluid":
            return self.fluid_is_applied_to_all_lines()

        for line_data in self.line_properties.values():
            if property in line_data.keys():
                return True

        for key in self.element_properties:
            if key[0] == property:
                return True

        for key in self.nodal_properties:
            if key[0] == property:
                return True

        return False

    def is_there_an_acoustic_attribute_in_the_node(self, node_id: int):

        acoustic_properties = [
            "acoustic_pressure",
            "volume_velocity",
            "specific_impedance",
            "radiation_impedance",
            "reciprocating_compressor_excitation",
            "reciprocating_pump_excitation",
            "psd_acoustic_link",
            "acoustic_transfer_element",
        ]

        for (property, *args) in self.nodal_properties.keys():
            if property in acoustic_properties and node_id in args:
                return True

        return False

    def check_if_there_are_tables_at_the_model(self):
        """This method checks if there are imported table of values in
        the model. It returns True if exists or False elsewhere.
        """

        data_dicts = [
            self.nodal_properties,
            self.element_properties,
        ]

        for data_dict in data_dicts:
            for data in data_dict.values():
                if isinstance(data, dict):
                    if "table_names" in data.keys():
                        return True

        return False

    def _reset_nodal_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """
        nodal_properties = deepcopy(self.nodal_properties)

        for existing_property, *args in nodal_properties.keys():
            if property != existing_property:
                continue

            self._remove_nodal_property(property, list(args))

    def _reset_element_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """
        element_properties = deepcopy(self.element_properties)

        for existing_property, *args in element_properties.keys():
            if property != existing_property:
                continue

            self._remove_element_property(property, list(args))

    def _remove_nodal_property(self, property: str, node_ids: int | list | tuple):
        """Remove a nodal property at specific nodal_id."""
        if isinstance(node_ids, Number):
            key = (property, node_ids)
        elif isinstance(node_ids, list | tuple) and len(node_ids) == 1:
            key = (property, node_ids[0])
        elif isinstance(node_ids, list | tuple) and len(node_ids) == 2:
            key = (property, node_ids[0], node_ids[1])
        else:
            return

        # remove nodal property-related tables
        prop_data = self.nodal_properties.get(key)
        self.remove_imported_tables_from_property(property, prop_data)

        if key in self.nodal_properties.keys():
            self.nodal_properties.pop(key)

    def _remove_element_property(self, property: str, element_ids: int | list[int]):
        """Remove a element property at specific element_id."""
        if isinstance(element_ids, Number):
            element_ids = [element_ids]

        for element_id in element_ids:
            key = (property, element_id)

            prop_data = self.element_properties.get(key)
            self.remove_imported_tables_from_property(property, prop_data)

            if key in self.element_properties.keys():
                self.element_properties.pop(key)

    def _remove_line_property(self, property: str, line_ids: int | list[int]):
        """Remove a line property at specific line_id."""

        if isinstance(line_ids, Number):
            line_ids = [line_ids]

        for line_id in line_ids:
            line_data =  self.line_properties.get(line_id, dict())
            if not line_data:
                continue

            prop_data = line_data.get(property)
            self.remove_imported_tables_from_property(property, prop_data)
            if prop_data is None:
                continue

            if property in line_data.keys():
                self.line_properties[line_id].pop(property)

    def remove_imported_tables_from_property(self, property: str, prop_data: dict):
        """
        This method removes the tables associated with a 
        particular property.
        """
        if isinstance(prop_data, dict):
            table_names = prop_data.get("table_names", list())

            if not table_names:
                return

            group_label = self.get_data_group_label(property)
            self.remove_imported_tables(group_label, table_names)

    def _remove_line(self, line_id: int | str):
        if isinstance(line_id, str):
            line_id = int(line_id)
        if line_id in self.line_properties.keys():
            self.line_properties.pop(line_id)

    def get_line_length(self, line_id: int):
        line_data = self.line_properties[line_id]
        if "start_coords" in line_data.keys() and "end_coords" in line_data.keys():
            start_coords = np.array(line_data["start_coords"], dtype=float)
            end_coords = np.array(line_data["end_coords"], dtype=float)
            return np.linalg.norm(end_coords - start_coords)
        else:
            return None

    def get_line_edges(self, line_id: int):
        line_data = self.line_properties[line_id]
        if "start_coords" in line_data.keys() and "end_coords" in line_data.keys():
            start_coords = np.array(line_data["start_coords"], dtype=float)
            end_coords = np.array(line_data["end_coords"], dtype=float)
            return start_coords, end_coords
        else:
            return None, None

    def map_line_to_points(self):
        line_to_points = dict()
        for line_id, data in self.line_properties.items():

            data: dict
            aux = dict()
            if "start_coords" in data.keys() and "end_coords" in data.keys():
                start_coords = np.array(data["start_coords"], dtype=float)
                end_coords = np.array(data["end_coords"], dtype=float)
                aux["start_coords"] = start_coords
                aux["end_coords"] = end_coords

            else:
                return dict()

            if "corner_coords" in data.keys():
                corner_coords = np.array(data["corner_coords"], dtype=float)
                aux["corner_coords"] = corner_coords
                line_to_points[line_id, "curve"] = aux
            else:
                line_to_points[line_id, "line"] = aux
            
            return line_to_points

    def get_nodal_related_table_names(self, property : str, node_ids : int | list) -> list:
        """
        """
        if isinstance(node_ids, Number):
            test_key = (property, node_ids)

        elif isinstance(node_ids, list) and len(node_ids) == 2:
            test_key = (property, node_ids[0], node_ids[1])

        else:
            return list()

        data = self.nodal_properties.get(test_key)

        if not isinstance(data, dict):
            return list()

        table_names = list()
        for table_name in data.get("table_names", list()):
            if table_name is not None:
                table_names.append(table_name)

        return table_names

    def get_element_related_table_names(self, property : str, element_ids : list | tuple, equals = False):
        """
        """
        
        table_names = dict()
        for key, data in self.element_properties.items():
            for element_id in element_ids:
                if "table_names" in data.keys():
                    if equals:
                        if key == (property, element_id):
                            table_names[key] = data["table_names"]
                    else:
                        if key == (property, element_id):
                            continue
                        else:
                            if key[1] == element_id:
                                table_names[key] = data["table_names"]
        return table_names

    def add_imported_tables(self, group_label: str, table_name: str, data: np.ndarray | list | tuple):
        """
        """
        if group_label == "acoustic":
            self.acoustic_imported_tables[table_name] = data
        elif group_label == "structural":
            self.structural_imported_tables[table_name] = data

    def remove_imported_tables(self, group_label: str, table_names: str | list[str]):
        """
        This method removes the imported tables data
        from the corresponding attributes.
        """
        if isinstance(table_names, str):
            table_names = [table_names]

        for table_name in table_names:
            if table_name is None:
                continue

            if group_label == "acoustic":
                if table_name in self.acoustic_imported_tables.keys():
                    self.acoustic_imported_tables.pop(table_name)

            elif group_label == "structural":
                if table_name in self.structural_imported_tables.keys():
                    self.structural_imported_tables.pop(table_name)
