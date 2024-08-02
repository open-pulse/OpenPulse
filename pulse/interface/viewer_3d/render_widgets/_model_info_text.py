from molde.utils import TreeInfo, format_long_sequence

from pulse import app


def nodes_info_text() -> str:
    nodes = app().main_window.list_selected_nodes()
    project = app().project

    info_text = ""

    if len(nodes) == 1:
        _id, *_ = nodes
        node = project.get_node(_id)
        tree = TreeInfo(f"Node {_id}")
        tree.add_item(
            f"Position",
            "({:.3f}, {:.3f}, {:.3f})".format(*node.coordinates),
            "m",
        )
        info_text += str(tree)

    elif len(nodes) > 1:
        info_text += (
            f"{len(nodes)} NODES IN SELECTION\n"
            f"{format_long_sequence(nodes)}\n\n"
        )
    return info_text

def elements_info_text() -> str:
    elements = app().main_window.list_selected_elements()
    info_text = ""
    project = app().project

    if len(elements) == 1:
        _id, *_ = elements
        structural_element = project.get_structural_element(_id)
        acoustic_element = project.get_acoustic_element(_id)

        first_node = structural_element.first_node
        last_node = structural_element.last_node

        tree = TreeInfo(f"ELEMENT {_id}")
        tree.add_item(
            f"First Node - {first_node.external_index:>5}",
            "({:.3f}, {:.3f}, {:.3f})".format(*first_node.coordinates),
            "m",
        )
        tree.add_item(
            f"Last Node  - {last_node.external_index:>5}",
            "({:.3f}, {:.3f}, {:.3f})".format(*last_node.coordinates),
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

    elif len(elements) > 1:
        info_text += (
            f"{len(elements)} ELEMENTS IN SELECTION\n"
            f"{format_long_sequence(elements)}\n\n"
        )
    return info_text

def entity_info_text() -> str:
    entities = app().main_window.list_selected_entities()
    info_text = ""
    project = app().project

    if len(entities) == 1:
        _id, *_ = entities
        entity = project.get_entity(_id)

        info_text += f"LINE {_id}\n\n"

        if entity.material:
            info_text += material_info_text(entity.material)

        if entity.fluid:
            info_text += fluid_info_text(entity.fluid)

        info_text += cross_section_info_text(
            entity.cross_section, entity.structural_element_type
        )

    elif len(entities) > 1:
        info_text += (
            f"{len(entities)} LINES IN SELECTION\n"
            f"{format_long_sequence(entities)}\n\n"
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
