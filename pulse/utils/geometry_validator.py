from dataclasses import dataclass, field
from pathlib import Path

import gmsh


SUPPORTED_LINE_TYPES = {"Line", "Circle"}

DIMENSION_LABELS = {
    0: "point",
    1: "curve",
    2: "surface",
    3: "solid",
}


@dataclass
class ValidationResult:
    is_valid: bool = True
    parse_error: bool = False
    parse_error_message: str = ""
    entity_counts: dict = field(default_factory=dict)
    unsupported_line_types: list = field(default_factory=list)
    has_surfaces_or_solids: bool = False


def validate_geometry_file(geometry_path: Path) -> ValidationResult:
    result = ValidationResult()

    was_initialized = gmsh.is_initialized()
    if was_initialized:
        gmsh.finalize()

    try:
        # A try except is needed here in case gmsh itself crashes while opening the geometry. In this case,
        # OP won't crash and the gmsh error is treated in the Exception.
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(str(geometry_path))

        entities = gmsh.model.get_entities()

        surfaces = [e for e in entities if e[0] == 2]
        solids = [e for e in entities if e[0] == 3]

        if surfaces or solids:
            result.has_surfaces_or_solids = True
            result.is_valid = False
            result.entity_counts["surface"] = len(surfaces)
            result.entity_counts["solid"] = len(solids)

        lines = [e for e in entities if e[0] == 1]
        unsupported_types = set()
        for line in lines:
            line_type = gmsh.model.get_type(*line)
            if line_type not in SUPPORTED_LINE_TYPES:
                unsupported_types.add(line_type)

        if unsupported_types:
            result.is_valid = False
            result.unsupported_line_types = sorted(unsupported_types)

    except Exception as e:
        result.is_valid = False
        result.parse_error = True
        result.parse_error_message = str(e)

    finally:
        gmsh.finalize()
        if was_initialized:
            gmsh.initialize("", False)

    return result


def format_validation_error(result: ValidationResult) -> str:
    if result.parse_error:
        return f"Failed to read geometry file.\n\nError: {result.parse_error_message}\n\nPlease verify the file is a valid STEP or IGES format."

    lines = ["OpenPulse only supports straight lines and circular arcs.\n"]

    if result.has_surfaces_or_solids:
        counts = []
        if "surface" in result.entity_counts:
            counts.append(f"{result.entity_counts['surface']} surface entity(ies)")
        if "solid" in result.entity_counts:
            counts.append(f"{result.entity_counts['solid']} solid entity(ies)")
        lines.append(f"Found unsupported geometry: {', '.join(counts)}.")

    if result.unsupported_line_types:
        types_str = ", ".join(result.unsupported_line_types)
        lines.append(f"Found unsupported curve types: {types_str}.")

    lines.append("\nPlease provide a wireframe geometry containing only lines and arcs.")
    return "\n".join(lines)
