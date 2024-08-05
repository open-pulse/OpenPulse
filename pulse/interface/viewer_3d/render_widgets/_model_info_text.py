import numpy as np
from molde.utils import TreeInfo, format_long_sequence

from pulse import app


def nodes_info_text() -> str:
    nodes = app().main_window.list_selected_nodes()
    project = app().project
    preprocessor = app().project.preprocessor
    info_text = ""

    if len(nodes) > 1:
        info_text += (
            f"{len(nodes)} NODES IN SELECTION\n"
            f"{format_long_sequence(nodes)}\n\n"
        )
    elif len(nodes) == 1:
        _id, *_ = nodes
        node = project.get_node(_id)
        tree = TreeInfo(f"Node {_id}")
        tree.add_item(
            f"Position",
            "[{:.3f}, {:.3f}, {:.3f}]".format(*node.coordinates),
            "m",
        )
        info_text += str(tree)
        info_text += _structural_format(
            "Prescribed dofs",
            node.prescribed_dofs,
            ("u", "r"),
            ("m", "rad"),
            node.loaded_table_for_prescribed_dofs
        )
        info_text += _structural_format(
            "Nodal loads",
            node.nodal_loads,
            ("F", "M"),
            ("N", "N.m"),
            node.loaded_table_for_nodal_loads
        )
        info_text += _structural_format(
            "Lumped stiffness",
            node.lumped_stiffness,
            ("k", "kr"),
            ("N/m", "N.m/rad"),
            node.loaded_table_for_lumped_stiffness
        )
        info_text += _structural_format(
            "Lumped dampings",
            node.lumped_dampings,
            ("c", "cr"),
            ("N.s/m", "N.m.s/rad"),
            node.loaded_table_for_lumped_dampings
        )
        info_text += _structural_format(
            "Lumped masses",
            node.lumped_masses,
            ("m", "J"),
            ("kg", "N.m²"),
            node.loaded_table_for_lumped_masses
        )
        if node.there_are_elastic_nodal_link_stiffness:
            for key, [_, values] in node.elastic_nodal_link_stiffness.items():
                info_text += _structural_format(
                    f"Stiffness elastic link: {key}",
                    values,
                    ("k", "kr"),
                    ("N/m", "N.m/rad"),
                    node.loaded_table_for_elastic_link_stiffness
                )
        if node.there_are_elastic_nodal_link_dampings:
            for key, [_, values] in node.elastic_nodal_link_dampings.items():
                info_text += _structural_format(
                    f"Stiffness elastic link: {key}",
                    values,
                    ("k", "kr"),
                    ("N/m", "N.m/rad"),
                    node.loaded_table_for_elastic_link_stiffness
                )
        if node in preprocessor.nodes_with_acoustic_pressure:
            info_text += _acoustic_format(
                "Acoustic pressure",
                node.acoustic_pressure,
                "P",
                "Pa"
            )
        if node in preprocessor.nodes_with_volume_velocity:
            info_text += _acoustic_format(
                "Volume velocity",
                node.volume_velocity,
                "Q",
                "m³/s"
            )
        if node in preprocessor.nodes_with_specific_impedance:
            info_text += _acoustic_format(
                "Specific impedance",
                node.specific_impedance,
                "Zs",
                "kg/m².s"
            )
        if node in preprocessor.nodes_with_radiation_impedance:
            aux_dict = {
                0:"anechoic termination", 
                1:"unflanged pipe", 
                2:"flanged pipe"
            }

            info_text += _acoustic_format(
                "Radiation impedance",
                aux_dict[node.radiation_impedance_type],
                "Type",
                ""
            )
        if node in preprocessor.nodes_with_compressor_excitation:
            info_text += compressor_excitation_info_text(node)

    return info_text

def elements_info_text() -> str:
    elements = app().main_window.list_selected_elements()
    info_text = ""
    project = app().project

    if len(elements) > 1:
        info_text += (
            f"{len(elements)} ELEMENTS IN SELECTION\n"
            f"{format_long_sequence(elements)}\n\n"
        )
    elif len(elements) == 1:
        _id, *_ = elements
        structural_element = project.get_structural_element(_id)
        acoustic_element = project.get_acoustic_element(_id)

        first_node = structural_element.first_node
        last_node = structural_element.last_node

        tree = TreeInfo(f"ELEMENT {_id}")
        tree.add_item(
            f"First Node - {first_node.external_index:>5}",
            "[{:.3f}, {:.3f}, {:.3f}]".format(*first_node.coordinates),
            "m",
        )
        tree.add_item(
            f"Last Node  - {last_node.external_index:>5}",
            "[{:.3f}, {:.3f}, {:.3f}]".format(*last_node.coordinates),
            "m",
        )
        info_text += str(tree)

        if structural_element.material:
            info_text += material_info_text(structural_element.material)

        if acoustic_element.fluid:
            info_text += fluid_info_text(acoustic_element.fluid)

        info_text += cross_section_info_text(
            structural_element.cross_section, structural_element.element_type
        )

    return info_text

def entity_info_text() -> str:
    lines = app().main_window.list_selected_lines()
    info_text = ""
    project = app().project

    if len(lines) > 1:
        info_text += (
            f"{len(lines)} LINES IN SELECTION\n"
            f"{format_long_sequence(lines)}\n\n"
        )
    elif len(lines) == 1:

        _id, *_ = lines
        entity = project.get_entity(_id)

        info_text += f"LINE {_id}\n\n"

        if entity.material:
            info_text += material_info_text(entity.material)

        if entity.fluid:
            info_text += fluid_info_text(entity.fluid)

        info_text += cross_section_info_text(
            entity.cross_section, entity.structural_element_type
        )

    return info_text

def material_info_text(material) -> str:
    tree = TreeInfo("Material")
    tree.add_item("Name", material.name)
    return str(tree)

def fluid_info_text(fluid) -> str:
    tree = TreeInfo("fluid")
    tree.add_item("Name", fluid.name)
    if fluid.temperature:
        tree.add_item("Temperature", round(fluid.temperature, 4), "K")
    if fluid.pressure:
        tree.add_item("Pressure", round(fluid.pressure, 4), "Pa")
    return str(tree)

def cross_section_info_text(cross_section, element_type) -> str:
    info_text = ""

    if cross_section is None:
        tree = TreeInfo("cross section")
        tree.add_item("Info", "Undefined")
        info_text += str(tree)

    elif element_type == "beam_1":
        tree = TreeInfo("cross section")
        tree.add_item("Area", round(cross_section.area, 2), "m²")
        tree.add_item("Iyy", round(cross_section.second_moment_area_y, 4), "m⁴")
        tree.add_item("Izz", round(cross_section.second_moment_area_z, 4), "m⁴")
        tree.add_item("Iyz", round(cross_section.second_moment_area_yz, 4), "m⁴")
        tree.add_item(
            "x-axis rotation", round(cross_section.second_moment_area_yz, 4), "m⁴"
        )
        info_text += str(tree)

    elif element_type in ["pipe_1", "valve"]:
        tree = TreeInfo("cross section")
        tree.add_item("Outer Diameter", round(cross_section.outer_diameter, 4), "m")
        tree.add_item("Thickness", round(cross_section.thickness, 4), "m")
        tree.add_separator()
        if cross_section.offset_y or cross_section.offset_z:
            tree.add_item("Offset Y", round(cross_section.offset_y, 4), "m")
            tree.add_item("Offset Z", round(cross_section.offset_z, 4), "m")
            tree.add_separator()
        if cross_section.insulation_thickness or cross_section.insulation_density:
            tree.add_item(
                "Insulation Thickness",
                round(cross_section.insulation_thickness, 4),
                "m",
            )
            tree.add_item(
                "Insulation Density",
                round(cross_section.insulation_density, 4),
                "kg/m³",
            )
        info_text += str(tree)

    return info_text

def analysis_info_text(frequency_index):
    project = app().project

    tree = TreeInfo(project.analysis_type_label)
    if project.analysis_ID in [2, 4]:
        if project.analysis_type_label == "Structural Modal Analysis":
            frequencies = project.get_structural_natural_frequencies()
        
        if project.analysis_type_label == "Acoustic Modal Analysis":
            frequencies = project.get_acoustic_natural_frequencies()
        
        if frequencies is None:
            return ""

        mode = frequency_index + 1
        frequency = frequencies[frequency_index]
        tree.add_item("Mode", mode)
        tree.add_item("Natural Frequency", f"{frequency:.2f}", "Hz")
    else:
        frequencies = project.get_frequencies()
        if frequencies is None:
            return ""

        if project.analysis_method_label is not None:
            tree.add_item("Method", project.analysis_method_label)

        frequency = frequencies[frequency_index]
        tree.add_item("Frequency", f"{frequency:.2f}", "Hz")

    return str(tree)

def compressor_excitation_info_text(node) -> str:
    tree = TreeInfo("Volume velocity - compressor excitation")
    if isinstance(node.volume_velocity, np.ndarray):
        tree.add_item("Q", "Table of values")
    else:
        tree.add_item("Q", node.volume_velocity, "m³/s")

    values_connection_info = list(node.dict_index_to_compressor_connection_info.values())
    if len(values_connection_info) == 1:
        tree.add_item("Connection type", values_connection_info[0])
    elif "discharge" in values_connection_info and "suction" in values_connection_info:
        tree.add_item(
            "Connection types", 
            f"discharge ({values_connection_info[0]}x)"
            + "& suction ({values_connection_info.count('suction')}x)"
        )
    elif "discharge" in values_connection_info:
        tree.add_item("Connection types", f"discharge ({values_connection_info.count('discharge')}x)")
    elif "suction" in values_connection_info:
        tree.add_item("Connection types", f"suction ({values_connection_info.count('suction')}x)")

    return str(tree)

def _pretty_sequence(sequence) -> str:
    str_sequence = [("Ø" if i is None else str(i)) for i in sequence]
    return "[" + ", ".join(str_sequence) + "]"

def _all_none(sequence) -> bool:
    return all(i is None for i in sequence)

def _structural_format(property_name, values, labels, units, has_table):
    if _all_none(values):
        return ""

    u = values[:3]
    r = values[3:]
    u_labels = ", ".join([labels[0] + i for i in "xyz"])
    r_labels = ", ".join([labels[1] + i for i in "xyz"])

    tree = TreeInfo(property_name)
    if has_table:
        tree.add_item(u_labels, "Loaded from table")
        tree.add_item(r_labels, "Loaded from table")
    else:
        if not _all_none(u):
            tree.add_item(u_labels, _pretty_sequence(u), units[0])
        if not _all_none(r):
            tree.add_item(r_labels, _pretty_sequence(r), units[1])
    return str(tree)

def _acoustic_format(property_name, value, label, unit):
    tree = TreeInfo(property_name)
    if isinstance(value, np.ndarray):
        tree.add_item(label, "Table of values")
    else:
        tree.add_item(label, value, unit)
    return str(tree)
