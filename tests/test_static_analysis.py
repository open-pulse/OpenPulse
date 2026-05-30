from pathlib import Path

import numpy as np
import pytest

from examples.example_file_helper import get_example_file_path
from pulse.model import AnalysisID
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.properties.material import Material
from pulse.project.project import Project


@pytest.fixture
def structural_model(datadir: Path):
    steel = Material(
        name="Steel",
        identifier=1,
        density=7850,
        elasticity_modulus=200e9,
        poisson_ratio=0.3,
    )

    section_parameters = [0.01, 0.001, 0, 0, 0, 0]
    cross_section = CrossSection(pipe_section_info=PipeCrossSection(*section_parameters))
    cross_section.update_properties()

    project = Project()
    project.initialize_pulse_file_and_loader(dir_path=datadir)
    model = project.model
    preprocessor = model.preprocessor

    geometry_path = get_example_file_path("iges_files/new_geometries/simple_L_pipe.iges")
    mesher_setup = {
        "element_size": 0.01,
        "geometry_tolerance": 1e-6,
        "length_unit": "meter",
        "import_type": 0,
        "geometry_path": str(geometry_path),
    }

    project.reset(reset_all=True)
    model.mesh.set_mesher_setup(mesher_setup=mesher_setup)
    preprocessor.generate()

    preprocessor.set_material_by_element("all", steel)
    preprocessor.set_cross_section_by_elements("all", cross_section)

    # Fix one end (node 103 is a boundary node in simple_L_pipe.iges)
    fixed_node_id = 103
    coords = preprocessor.nodes[fixed_node_id].coordinates
    prescribed_dofs = [0j, 0j, 0j, 0j, 0j, 0j]
    data = {
        "coords": list(coords),
        "values": prescribed_dofs,
        "real_values": [np.real(v) for v in prescribed_dofs],
        "imag_values": [np.imag(v) for v in prescribed_dofs],
    }
    model.properties._set_nodal_property("prescribed_dofs", data, fixed_node_id)

    # Apply unit force at node 152
    load_node_id = 152
    coords = preprocessor.nodes[load_node_id].coordinates
    nodal_loads = [1 + 0j, 0j, 0j, 0j, 0j, 0j]
    data = {
        "coords": list(coords),
        "values": nodal_loads,
        "real_values": [np.real(v) for v in nodal_loads],
        "imag_values": [np.imag(v) for v in nodal_loads],
    }
    model.properties._set_nodal_property("nodal_loads", data, load_node_id)

    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)

    return project


def test_structural_static(structural_model):
    project = structural_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.STRUCTURAL_STATIC,
    }

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    solution = project.structural_solver.solution
    assert solution is not None
    assert solution.ndim == 2
    assert solution.shape[1] == 1

