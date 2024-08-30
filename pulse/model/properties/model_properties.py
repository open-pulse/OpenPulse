
from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid

import numpy as np


DEFAULT_MATERIAL = Material(
    name="Steel",
    identifier=1,
    color=(200, 200, 200),
    density=7860,
    elasticity_modulus=210e9,
    poisson_ratio=0.3,
)

DEFAULT_FLUID = Fluid(
    name="Air",
    identifier=1,
    color=(200, 200, 200),
    density=1.215,
    speed_of_sound=343.2021,
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

        self.acoustic_imported_tables = dict()
        self.structural_imported_tables = dict()

        self.global_properties = dict()
        self.line_properties = dict()
        self.element_properties = dict()
        self.nodal_properties = dict()

        self.valves_data = dict()
        self.expansion_joint_data = dict()

        self.global_properties["material", "global"] = DEFAULT_MATERIAL
        self.global_properties["fluid", "global"] = DEFAULT_FLUID

    def get_material(self, **kwargs) -> Material:
        return self._get_property("material", **kwargs)

    def get_fluid(self, **kwargs) -> Fluid:
        return self._get_property("fluid", **kwargs)

    def set_material(self, material: Material, line_ids):
        self._set_line_property("material", material, line_ids=line_ids)

    def set_fluid(self, fluid: Fluid, line_ids):
        self._set_line_property("fluid", fluid, line_ids=line_ids)

    def remove_compressor_table_name(self, node_id: int, table_name: str):
        key = ("compressor_excitation", node_id)
        if key in self.nodal_properties.keys():
            if table_name in self.nodal_properties[key]["table_names"]:
                self.nodal_properties[key]["table_names"].remove(table_name)

    def get_data_group_label(self, property : str):

        acoustic_labels = [ 
                            "acoustic_pressure", 
                            "volume_velocity", 
                            "specific_impedance", 
                            "radiation_impedance", 
                            "compressor_excitation"
                           ]

        if property in acoustic_labels:
            return "acoustic"
        else:
            return "structural"

    def _set_nodal_property(self, property: str, data, node_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by node, element, line, surface or volume
        if any of these exists. Otherwise sets the property as global.

        """

        if node_ids is None:
            return

        group_label = self.get_data_group_label(property)

        tables_values = list()
        if "real_values" in data.keys() and "imag_values" in data.keys():
            for i, a in enumerate(data["real_values"]):
                if a is None:
                    tables_values.append(None)
                else:
                    b = data["imag_values"][i]
                    tables_values.append(a + 1j*b)

        if "table_names" in data.keys():

            if group_label == "acoustic":
                imported_tables = self.acoustic_imported_tables
            else:
                imported_tables = self.structural_imported_tables

            for i, table_name in enumerate(data["table_names"]):

                if table_name is None:
                    tables_values.append(None)
                    continue

                if table_name in imported_tables.keys():
                    data_array = imported_tables[table_name]
                    values = data_array[:, 1] + 1j*data_array[:, 2]
                    tables_values.append(values)

        data["values"] = tables_values

        if isinstance(node_ids, int):
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
        
        elif isinstance(element_ids, int):
            element_ids = [element_ids]

        for element_id in element_ids:
            self.element_properties[property, element_id] = data

    def _set_line_property(self, property: str, data, line_ids: (int | list | tuple | None)):
        """
        Sets a data to a property by line.

        """
        if line_ids is None:
            return
        
        elif isinstance(line_ids, int):
            line_ids = [line_ids]

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
        
        elif isinstance(line_ids, int):
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

        if isinstance(node_ids, int):
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

        keys_to_remove = list()

        for key in self.nodal_properties.keys():
            if len(key) == 2:
                existing_property, _ = key
            else:
                existing_property = key

            if property == existing_property:
                if key not in keys_to_remove:
                    keys_to_remove.append(key)

        for _key in keys_to_remove:
            self.nodal_properties.pop(_key)

    def _reset_element_property(self, property: str):
        """
        Clears all instances of a specific property from the structure.
        """

        keys_to_remove = list()

        for key in self.element_properties.keys():
            if len(key) == 2:
                existing_property, _ = key
            else:
                existing_property = key

            if property == existing_property:
                if key not in keys_to_remove:
                    keys_to_remove.append(key)

        for _key in keys_to_remove:
            self.element_properties.pop(_key)

    def _remove_nodal_property(self, property: str, node_ids: int | list | tuple):
        """Remove a nodal property at specific nodal_id."""
        if isinstance(node_ids, int):
            key = (property, node_ids)
        elif isinstance(node_ids, list | tuple) and len(node_ids) == 1:
            key = (property, node_ids[0])
        elif isinstance(node_ids, list | tuple) and len(node_ids) == 2:
            key = (property, node_ids[0], node_ids[1])
        else:
            return
        if key in self.nodal_properties.keys():
            self.nodal_properties.pop(key)

    def _remove_element_property(self, property: str, element_ids: int | list):
        """Remove a element property at specific element_id."""
        if isinstance(element_ids, int):
            element_ids = [element_ids]
        for element_id in element_ids:
            key = (property, element_id)
            if key in self.element_properties.keys():
                self.element_properties.pop(key)

    def _remove_line_property(self, property: str, line_ids: int | list):
        """Remove a line property at specific line_id."""
        if isinstance(line_ids, int):
            line_ids = [line_ids]
        for line_id in line_ids:
            if line_id in self.line_properties.keys():
                if property in self.line_properties[line_id].keys():
                    self.line_properties[line_id].pop(property)

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

    def get_nodal_related_table_names(self, property : str, node_ids : int | list) -> list:
        """
        """
        table_names = list()
        if isinstance(node_ids, int):
            test_key = (property, node_ids)

        elif isinstance(node_ids, list) and len(node_ids) == 2:
            test_key = (property, node_ids[0], node_ids[1])

        else:
            return table_names

        if test_key in self.nodal_properties.keys():
            data = self.nodal_properties[test_key]

            if "table_names" in data.keys():
                for table_name in data["table_names"]:
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

    def remove_imported_tables(self, group_label: str, table_name: str):
        """
        """
        if group_label == "acoustic":
            if table_name in self.acoustic_imported_tables.keys():
                self.acoustic_imported_tables.pop(table_name)

        elif group_label == "structural":
            if table_name in self.structural_imported_tables.keys():
                self.structural_imported_tables.pop(table_name)