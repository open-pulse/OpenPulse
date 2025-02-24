#fmt: off

from pulse import app
from pulse.utils.unit_conversion import mm_to_m

from molde.utils import TreeInfo, format_long_sequence

import numpy as np
from numbers import Number


def nodes_info_text() -> str:

    nodes = app().main_window.list_selected_nodes()
    preprocessor = app().project.model.preprocessor
    properties = app().project.model.properties

    info_text = ""

    if len(nodes) > 1:
        info_text += (f"{len(nodes)} NODES IN SELECTION\n" f"{format_long_sequence(nodes)}\n\n")

    elif len(nodes) == 1:

        node_id, *_ = nodes
        node = preprocessor.nodes[node_id]
        tree = TreeInfo(f"Node {node_id}")
        tree.add_item(f"Position", "[{:.3f}, {:.3f}, {:.3f}]".format(*node.coordinates), "m")
        info_text += str(tree)

        key = ("prescribed_dofs", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            values = data["values"]
            loaded_table = "table_names" in data.keys()
            info_text += _structural_format("Prescribed dofs",  values, ("u", "r"), ("m", "rad"), loaded_table)

        key = ("nodal_loads", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            values = data["values"]
            loaded_table = "table_names" in data.keys()
            info_text += _structural_format("Nodal loads", values, ("F", "M"), ("N", "N.m"), loaded_table)

        key = ("lumped_stiffness", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            values = data["values"]
            loaded_table = "table_names" in data.keys()
            info_text += _structural_format("Lumped stiffness", values, ("k", "kr"), ("N/m", "N.m/rad"), loaded_table)

        key = ("lumped_dampings", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            values = data["values"]
            loaded_table = "table_names" in data.keys()
            info_text += _structural_format("Lumped dampings", values, ("c", "cr"), ("N.s/m", "N.m.s/rad"), loaded_table)        

        key = ("lumped_masses", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            values = data["values"]   
            loaded_table = "table_names" in data.keys()
            info_text += _structural_format("Lumped masses", values, ("m", "J"), ("kg", "N.m²"), loaded_table)

        for (property, *args), data in properties.nodal_properties.items():
            if property == "stiffness_elastic_link" and node_id in args:
                values = data["values"]
                loaded_table = "table_names" in data.keys()
                info_text += _structural_format(f"Stiffness elastic link: {key}", values, ("k", "kr"), ("N/m", "N.m/rad"), loaded_table)

        for (property, *args), data in properties.nodal_properties.items():
            if property == "dampings_elastic_link" and node_id in args:
                values = data["values"]
                loaded_table = "table_names" in data.keys()
                info_text += _structural_format(f"Damping elastic link: {key}", values, ("k", "kr"), ("N.s/m", "N.m.s/rad"), loaded_table)

        key = ("acoustic_pressure", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            ap_values = data["values"][0]
            loaded_table = "table_names" in data.keys()
            info_text += _acoustic_format("Acoustic pressure", ap_values, "P", "Pa")

        key = ("volume_velocity", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            vv_values = data["values"][0]
            loaded_table = "table_names" in data.keys()
            info_text += _acoustic_format("Volume velocity", vv_values, "Q", "m³/s")

        key = ("specific_impedance", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            si_values = data["values"][0]
            loaded_table = "table_names" in data.keys()
            info_text += _acoustic_format("Specific impedance", si_values, "Zs", "kg/m².s")

        key = ("radiation_impedance", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            impedance_type = data["impedance_type"]
            labels = ["anechoic termination", "flanged pipe", "unflanged pipe"]
            info_text += _acoustic_format("Radiation impedance", labels[impedance_type], "Type", "")

        key = ("reciprocating_compressor_excitation", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            info_text += compressor_excitation_info_text(data)

        key = ("reciprocating_pump_excitation", node_id)
        if key in properties.nodal_properties.keys():
            data = properties.nodal_properties[key]
            info_text += pump_excitation_info_text(data)

    return info_text

def elements_info_text() -> str:

    elements = app().main_window.list_selected_elements()
    info_text = ""
    project = app().project

    if len(elements) > 1:
        info_text += ( f"{len(elements)} ELEMENTS IN SELECTION\n"
                        f"{format_long_sequence(elements)}\n\n" )

    elif len(elements) == 1:
        _id, *_ = elements
        structural_element = project.get_structural_element(_id)
        acoustic_element = project.get_acoustic_element(_id)

        first_node = structural_element.first_node
        last_node = structural_element.last_node

        tree = TreeInfo(f"ELEMENT {_id}")
        tree.add_item( f"First Node - {first_node.external_index:>5}",
                        "[{:.3f}, {:.3f}, {:.3f}]".format(*first_node.coordinates),
                        "m" )

        tree.add_item( f"Last Node  - {last_node.external_index:>5}",
                        "[{:.3f}, {:.3f}, {:.3f}]".format(*last_node.coordinates),
                        "m" )

        info_text += str(tree)

        if structural_element.material:
            info_text += material_info_text(structural_element.material)

        if acoustic_element.fluid:
            info_text += fluid_info_text(acoustic_element.fluid)

        valve_name = structural_element.valve_data.get("valve_name", "")

        info_text += cross_section_info_text(
                                             structural_element.cross_section, 
                                             structural_element.element_type,
                                             structural_element.beam_xaxis_rotation,
                                             valve_name
                                             )

    return info_text

def lines_info_text() -> str:

    info_text = ""

    project = app().project
    lines = app().main_window.list_selected_lines()

    if len(lines) > 1:
        info_text += (
            f"{len(lines)} LINES IN SELECTION\n" f"{format_long_sequence(lines)}\n\n"
        )

    elif len(lines) == 1:

        line_id, *_ = lines

        properties = project.model.properties
        length = mm_to_m(project.model.mesh.curve_length[line_id])

        # info_text += f"LINE {line_id}\n"
        # info_text += f"Length: {length : .3f} [m]\n\n"

        info_text += line_info_text(line_id, length)

        material = properties._get_property("material", line_id=line_id)
        if material is not None:
            info_text += material_info_text(material)

        fluid = properties._get_property("fluid", line_id=line_id)
        if fluid is not None:
            info_text += fluid_info_text(fluid)

        cross_section = properties._get_property("cross_section", line_id=line_id)
        structural_element_type = properties._get_property("structural_element_type", line_id=line_id)
        beam_xaxis_rotation = properties._get_property("beam_xaxis_rotation", line_id=line_id)

        valve_name = ""
        valve_info = properties._get_property("valve_info", line_id=line_id)
        if isinstance(valve_info, dict):
            valve_name = valve_info.get("valve_name", "")

        info_text += cross_section_info_text(
                                             cross_section, 
                                             structural_element_type, 
                                             beam_xaxis_rotation, 
                                             valve_name
                                             )
        
        info_text += strucural_element_info_text()

    return info_text

def line_info_text(line_id, length):
    tree = TreeInfo("Line")
    tree.add_item("Identifier", line_id)
    tree.add_item("Length", f"{length : .4f}", "m")
    return str(tree)

def material_info_text(material) -> str:
    tree = TreeInfo("Material")
    tree.add_item("Name", material.name)
    tree.add_item("Density", material.density, "kg/m³")
    tree.add_item("Elasticity modulus", round(material.elasticity_modulus / 1e9, 2), "GPa")
    tree.add_item("Poisson ratio", material.poisson_ratio, "")
    return str(tree)

def fluid_info_text(fluid) -> str:
    tree = TreeInfo("fluid")
    tree.add_item("Name", fluid.name)
    if fluid.temperature:
        tree.add_item("Temperature", round(fluid.temperature, 4), "K")
    if fluid.pressure:
        tree.add_item("Pressure", f"{fluid.pressure : .8e}", "Pa")
    if fluid.density:
        tree.add_item("Density", round(fluid.density, 4), "kg/m³")
    if fluid.speed_of_sound:
        tree.add_item("Speed of sound", round(fluid.speed_of_sound, 4), "m/s")
    if fluid.bulk_modulus:
        tree.add_item("Bulk modulus", f"{fluid.bulk_modulus : .8e}", "Pa")
    if fluid.molar_mass:
        tree.add_item("Molar mass", round(fluid.molar_mass, 4), "kg/kmol")
    return str(tree)

def cross_section_info_text(cross_section, structural_element_type, beam_xaxis_rotation, valve_name) -> str:

    info_text = ""

    if cross_section is None:
        tree = TreeInfo("cross section")
        tree.add_item("Info", "Undefined")
        info_text += str(tree)

    elif structural_element_type == "beam_1":
        tree = TreeInfo("cross section")

        area = cross_section.area
        I_yy = cross_section.second_moment_area_y
        I_zz = cross_section.second_moment_area_z
        I_yz = cross_section.second_moment_area_yz

        tree.add_item("Section type", cross_section.section_type_label, "")
        tree.add_item("Area", f"{area : .6e}", "m²")
        tree.add_item("Iyy", f"{I_yy : .6e}", "m⁴")
        tree.add_item("Izz", f"{I_zz : .6e}", "m⁴")
        tree.add_item("Iyz", f"{I_yz : .6e}", "m⁴")

        if isinstance(beam_xaxis_rotation, float):
            tree.add_item("x-axis rotation", round(beam_xaxis_rotation, 4), "deg")

        info_text += str(tree)

    elif structural_element_type in ["pipe_1", "valve"]:

        tree = TreeInfo("cross section")
        tree.add_item("Section type", cross_section.section_type_label, "")
        if structural_element_type == "valve":
            tree.add_item("Valve name", valve_name, "")

        tree.add_item("Outer diameter", round(cross_section.outer_diameter, 4), "m")
        tree.add_item("Thickness", round(cross_section.thickness, 4), "m")
        tree.add_separator()

        if cross_section.offset_y or cross_section.offset_z:
            tree.add_item("Offset y", round(cross_section.offset_y, 4), "m")
            tree.add_item("Offset z", round(cross_section.offset_z, 4), "m")
            tree.add_separator()

        if cross_section.insulation_thickness or cross_section.insulation_density:
            tree.add_item("Insulation thickness", round(cross_section.insulation_thickness, 4),"m")
            tree.add_item("Insulation density", round(cross_section.insulation_density, 4), "kg/m³")

        info_text += str(tree)

    return info_text

def strucural_element_info_text():

    line_ids = app().main_window.list_selected_lines()
    if len(line_ids) == 1:

        tree = TreeInfo("structural element")

        structural_element_type = app().project.model.properties._get_property("structural_element_type", line_id=line_ids[0])
        if strucural_element_info_text is None:
            label = "Pipe_1"
        else:
            label = structural_element_type
        tree.add_item("Strucural element type", label)

        if structural_element_type in ["Pipe_1", "pipe_1"]:

            capped_end = app().project.model.properties._get_property("capped_end", line_id=line_ids[0])
            if capped_end is not None:
                label = "Active" if capped_end else "Inactive"
            else:
                label = "Active"
            tree.add_item("Capped end", label)

            force_offset = app().project.model.properties._get_property("force_offset", line_id=line_ids[0])
            if force_offset is not None:
                label = "Active" if force_offset else "Inactive"
            else:
                label = "Active"
            tree.add_item("Force offset", label)

            wall_formulation = app().project.model.properties._get_property("wall_formulation", line_id=line_ids[0])
            if wall_formulation is not None:
                label = wall_formulation.replace("_", " ").capitalize()
            else:
                label = "Thin wall"
            tree.add_item("Wall formulation", label)

    return str(tree)

def analysis_info_text(frequency_index: int):

    project = app().project
    tree = TreeInfo(project.analysis_type_label)

    if project.analysis_id in [2, 4]:
        if project.analysis_type_label == "Structural Modal Analysis":
            frequencies = list(project.natural_frequencies_structural)

        if project.analysis_type_label == "Acoustic Modal Analysis":
            if isinstance(project.complex_natural_frequencies_acoustic, np.ndarray):
                frequencies = list(project.complex_natural_frequencies_acoustic)
            else:
                frequencies = list(project.natural_frequencies_acoustic)

        if frequencies is None:
            return ""

        if frequency_index >= len(frequencies):
            return ""

        mode = frequency_index + 1
        tree.add_item("Mode", mode)

        if isinstance(project.complex_natural_frequencies_acoustic, np.ndarray):
            value = frequencies[frequency_index]
            damping_ratio = -np.real(value) / np.abs(value)
            damped_frequency = np.abs(value) * np.sqrt(1 - damping_ratio**2)
            tree.add_item("Damped Natural Frequency", f"{damped_frequency : .4f}", "Hz")
            tree.add_item("Damping Ratio", f"{damping_ratio : .4e}", "--")

        else:
            frequency = frequencies[frequency_index]
            tree.add_item("Natural Frequency", f"{frequency : .4f}", "Hz")

    else:

        frequencies = project.model.frequencies
        if frequencies is None:
            return ""

        if frequency_index >= len(frequencies):
            return ""

        if project.analysis_method_label is not None:
            tree.add_item("Method", project.analysis_method_label)

        frequency = frequencies[frequency_index]
        tree.add_item("Frequency", f"{frequency:.2f}", "Hz")

    return str(tree)

def compressor_excitation_info_text(compressor_data: dict) -> str:
    tree = TreeInfo("Volume velocity due compressor excitation")
    tree.add_item("Q", "Table of values")

    connection_type = compressor_data["connection_type"]
    tree.add_item("Connection type", connection_type)

    return str(tree)

def pump_excitation_info_text(pump_data: dict) -> str:
    tree = TreeInfo("Volume velocity due pump excitation")
    tree.add_item("Q", "Table of values")

    connection_type = pump_data["connection_type"]
    tree.add_item("Connection type", connection_type)

    return str(tree)

def min_max_stresses_info_text():
    min_stress = np.round(app().project.min_stress, 2)
    max_stress = np.round(app().project.max_stress, 2)
    tree = TreeInfo("Stress info")
    tree.add_item("Min stress", min_stress, "Pa")
    tree.add_item("Max stress", max_stress, "Pa")
    return str(tree)

def _all_none(sequence) -> bool:
    return all(i is None for i in sequence)

def _structural_format(property_name, values, labels, units, has_table):
    if _all_none(values):
        return ""

    u_values = []
    u_labels = []
    for val, label in zip(values[:3], "xyz"):
        if val is not None:
            u_values.append(val)
            u_labels.append(labels[0] + label)

    r_values = []
    r_labels = []
    for val, label in zip(values[3:], "xyz"):
        if val is None:
            continue

        if not isinstance(val, Number | str):
            val = "table"

        r_values.append(val)
        r_labels.append(labels[1] + label)

    tree = TreeInfo(property_name)
    if has_table:
        tree.add_item(u_labels, "Table of values")
        tree.add_item(r_labels, "Table of values")
    else:
        if u_values:
            tree.add_item(", ".join(u_labels), u_values, units[0])
        if r_values:
            tree.add_item(", ".join(r_labels), r_values, units[1])
    return str(tree)

def _acoustic_format(property_name, value, label, unit):
    tree = TreeInfo(property_name)
    if isinstance(value, Number | str):
        tree.add_item(label, value, unit)
    else:
        tree.add_item(label, "Table of values")
    return str(tree)

#fmt: on