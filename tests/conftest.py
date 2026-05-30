import pytest
import numpy as np

from examples.example_file_helper import get_example_file_path
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.cross_sections.i_beam_cross_section import IBeamCrossSection
from pulse.project.project import Project

from tests.helpers import (
    create_air_fluid,
    create_stainless_steel_material,
    create_temporary_fluid_library,
    create_temporary_material_library,
)


@pytest.fixture
def example2_project(tmp_path):
    """Project pre-loaded with example_2_withBeam.iges geometry, air fluid,
    stainless steel material, standard cross-sections, and 5-point DOF prescriptions.

    Returns (project, mesher_setup) so each test can append its analysis-specific
    boundary conditions and then solve.
    """
    project = Project()
    project.initialize_pulse_file_and_loader(dir_path=tmp_path)
    model = project.model
    mesh = model.mesh
    preprocessor = model.preprocessor

    geometry_path = get_example_file_path("iges_files/new_geometries/example_2_withBeam.iges")
    mesher_setup = {
        "element_size": 0.01,
        "geometry_tolerance": 1e-6,
        "length_unit": "meter",
        "import_type": 0,
        "geometry_path": str(geometry_path),
    }

    project.reset(reset_all=True)
    mesh.set_mesher_setup(mesher_setup=mesher_setup)
    preprocessor.generate()

    mesher_setup["import_type"] = 1
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    all_lines = model.mesh.lines_from_model
    beam_lines = [20, 23, 24]
    branch_lines = [31, 32, 33]
    main_lines = [line_id for line_id in all_lines if line_id not in beam_lines + branch_lines]

    # Fluid
    fluids = create_air_fluid()
    create_temporary_fluid_library(project, fluids)
    preprocessor.set_fluid_by_lines(all_lines, fluids[1])
    model.properties._set_line_property("fluid_id", fluids[1].identifier, all_lines)
    model.properties._set_line_property("fluid", fluids[1], all_lines)

    # Material
    materials = create_stainless_steel_material()
    create_temporary_material_library(project, materials)
    preprocessor.set_material_by_lines(all_lines, materials[1])
    model.properties._set_line_property("material_id", materials[1].identifier, all_lines)
    model.properties._set_line_property("material", materials[1], all_lines)

    # Cross-sections
    main_section_info = PipeCrossSection(0.100, 0.008, 0, 0, 0, 0)
    branch_section_info = PipeCrossSection(0.050, 0.008, 0, 0, 0, 0)
    beam_section_info = IBeamCrossSection(0.16, 0.12, 0.01, 0.12, 0.01, 0.01, 0.0, 0.0)

    cross_section_main = CrossSection(pipe_section_info=main_section_info)
    cross_section_branch = CrossSection(pipe_section_info=branch_section_info)
    cross_section_beam = CrossSection(beam_section_info=beam_section_info)

    for line_id in main_lines:
        center_coords = model.properties._get_property("center_coords", line_id=line_id)
        corner_coords = model.properties._get_property("corner_coords", line_id=line_id)
        label = main_section_info.section_type_label if (center_coords, corner_coords).count(None) == 2 else "bend"
        model.properties._set_line_property("structure_name", label, line_id)

    model.properties._set_multiple_line_properties(main_section_info.as_dict(), main_lines)
    model.properties._set_line_property("cross_section", cross_section_main, main_lines)
    model.properties._set_line_property("structural_element_type", "pipe_1", main_lines)
    preprocessor.set_cross_section_by_lines(main_lines, cross_section_main)
    preprocessor.set_structural_element_type_by_lines(main_lines, "pipe_1")

    for line_id in branch_lines:
        center_coords = model.properties._get_property("center_coords", line_id=line_id)
        corner_coords = model.properties._get_property("corner_coords", line_id=line_id)
        label = branch_section_info.section_type_label if (center_coords, corner_coords).count(None) == 2 else "bend"
        model.properties._set_line_property("structure_name", label, line_id)

    model.properties._set_multiple_line_properties(branch_section_info.as_dict(), branch_lines)
    model.properties._set_line_property("cross_section", cross_section_branch, branch_lines)
    model.properties._set_line_property("structural_element_type", "pipe_1", branch_lines)
    preprocessor.set_cross_section_by_lines(branch_lines, cross_section_branch)
    preprocessor.set_structural_element_type_by_lines(branch_lines, "pipe_1")

    model.properties._set_line_property("structure_name", beam_section_info.section_type_label, beam_lines)
    model.properties._set_multiple_line_properties(beam_section_info.as_dict(), beam_lines)
    model.properties._set_line_property("cross_section", cross_section_beam, beam_lines)
    model.properties._set_line_property("structural_element_type", "beam_1", beam_lines)
    preprocessor.set_cross_section_by_lines(beam_lines, cross_section_beam)
    preprocessor.set_structural_element_type_by_lines(beam_lines, "beam_1")

    # DOF prescriptions — 5 support nodes
    support_coords = np.array([
        [0.000,  0.000,  0.000],
        [2.000, -0.250,  1.250],
        [0.850,  1.000, -0.750],
        [1.350,  1.250,  0.500],
        [0.850,  0.000,  0.500],
    ], dtype=float)

    for coords in support_coords:
        node_id = preprocessor.get_node_id_by_coordinates(coords)
        prescribed_dofs = [0j, 0j, 0j, 0j, 0j, 0j]
        data = {
            "coords": list(coords),
            "values": prescribed_dofs,
            "real_values": [np.real(v) for v in prescribed_dofs],
            "imag_values": [np.imag(v) for v in prescribed_dofs],
        }
        model.properties._set_nodal_property("prescribed_dofs", data, node_id)

    return project, mesher_setup
"""
Global pytest configuration and fixtures.

The ``no_qt_in_solver`` fixture suppresses GUI-related side effects that
originate inside the non-linear harmonic solver during headless (CI/script)
runs:

* ``_build_convergence_plot`` – tries to create a PySide6 ``XYPlot`` widget.
  When no display is available Qt calls ``abort()`` at the C level, which
  cannot be caught by Python's ``except Exception``.  Returning ``None`` is
  the expected headless behaviour and is already documented in the docstring
  of that helper.

* ``time.sleep`` inside ``process_analysis`` – a 1-second UI-update pause
  injected after every nonlinear acoustic solve.  Skipped in tests.
"""

from unittest.mock import patch


@pytest.fixture(autouse=True)
def no_qt_in_solver():
    with (
        patch(
            "pulse.processing.solvers.harmonic_solver._build_convergence_plot",
            return_value=None,
        ),
        patch("time.sleep"),
    ):
        yield
