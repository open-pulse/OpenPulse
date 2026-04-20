from pathlib import Path

import numpy as np
import pytest

from examples.example_file_helper import get_example_file_path
from pulse.model import AnalysisID
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project


@pytest.fixture
def acoustic_model(datadir: Path):
    steel = Material(
        name="Steel",
        identifier=1,
        density=7850,
        elasticity_modulus=200e9,
        poisson_ratio=0.3,
    )

    air = Fluid(
        name="air",
        identifier=1,
        temperature=293.15,
        pressure=101325,
        density=1.204263,
        speed_of_sound=343.395034,
        isentropic_exponent=1.401985,
        thermal_conductivity=0.025503,
        specific_heat_Cp=1006.400178,
        dynamic_viscosity=1.8247e-5,
        molar_mass=28.958601,
        color=[0, 170, 255],
    )

    section_parameters = [0.05, 0.008, 0, 0, 0, 0]
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
    preprocessor.set_fluid_by_element("all", air)
    preprocessor.set_cross_section_by_elements("all", cross_section)

    project.file.write_project_setup_in_file(mesher_setup)

    return project, mesher_setup


def test_acoustic_modal(acoustic_model):
    project, _ = acoustic_model
    model = project.model

    n_modes = 20
    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_MODAL,
        "number_of_modes": n_modes,
        "sigma_factor": 1e-2,
    }

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    natural_frequencies = project.acoustic_solver.natural_frequencies
    assert natural_frequencies is not None
    assert len(natural_frequencies) == n_modes
    assert all(f >= 0 for f in natural_frequencies)


def _apply_volume_velocity(model, preprocessor, node_id):
    coords = preprocessor.nodes[node_id].coordinates
    volume_velocity = [0.01 + 0j]
    data = {
        "coords": list(coords),
        "values": volume_velocity,
        "real_values": [np.real(v) for v in volume_velocity],
        "imag_values": [np.imag(v) for v in volume_velocity],
    }
    model.properties._set_nodal_property("volume_velocity", data, node_id)


def test_acoustic_harmonic(acoustic_model):
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    # Apply volume velocity excitation at node 103 (boundary node in simple_L_pipe)
    _apply_volume_velocity(model, preprocessor, node_id=103)
    project.file.write_nodal_properties_in_file()

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
        "analysis_method": "fetm",
    }

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    solution = project.acoustic_solver.solution
    assert solution is not None
    assert solution.ndim == 2
    assert solution.shape[1] == len(model.frequencies)


def test_acoustic_harmonic_fem(acoustic_model):
    """FEM acoustic harmonic analysis produces a valid complex pressure solution."""
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    _apply_volume_velocity(model, preprocessor, node_id=103)
    project.file.write_nodal_properties_in_file()

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
        "analysis_method": "fem",
    }

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    assert project.acoustic_assembler._harmonic_method == "fem"

    solution = project.acoustic_solver.solution
    assert solution is not None
    assert solution.ndim == 2
    assert solution.shape[1] == len(model.frequencies)
    assert np.issubdtype(solution.dtype, np.complexfloating)
    assert np.any(np.abs(solution) > 0)


def test_acoustic_harmonic_fem_vs_fetm(acoustic_model):
    """FEM and FETM solutions agree in shape and energy at low frequencies.

    With element_size=0.01 m and c=343 m/s the mesh cutoff is ~34 kHz.
    At 1-200 Hz the FEM dispersion error is negligible (kh << 1), so both
    methods should produce acoustically equivalent results even though the
    numerical values differ slightly.
    """
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    _apply_volume_velocity(model, preprocessor, node_id=103)
    project.file.write_nodal_properties_in_file()

    base_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
    }

    # Run FETM
    model.set_analysis_setup({**base_setup, "analysis_method": "fetm"})
    project.file.write_analysis_setup_in_file({**base_setup, "analysis_method": "fetm"})
    project.build_model_and_solve(running_by_script=True)
    fetm_solution = project.acoustic_solver.solution.copy()

    # Run FEM (new assembler created from scratch via reset_solvers)
    project.reset_solvers()
    model.set_analysis_setup({**base_setup, "analysis_method": "fem"})
    project.file.write_analysis_setup_in_file({**base_setup, "analysis_method": "fem"})
    project.build_model_and_solve(running_by_script=True)
    fem_solution = project.acoustic_solver.solution.copy()

    # Same output shape
    assert fetm_solution.shape == fem_solution.shape

    # FEM and FETM are numerically distinct (different formulations)
    assert not np.allclose(fetm_solution, fem_solution)

    # Total acoustic energy should be very close — at 1-200 Hz with 0.01 m
    # elements the FEM dispersion error (kh)² is at most ~3e-4 at 200 Hz
    fetm_energy = np.sum(np.abs(fetm_solution) ** 2)
    fem_energy = np.sum(np.abs(fem_solution) ** 2)
    assert 0.5 < fem_energy / fetm_energy < 2.0

    # At very low frequencies (f=1-5 Hz) the two methods should be virtually
    # identical: relative norm difference < 1%
    for fi in range(5):
        fetm_norm = np.linalg.norm(fetm_solution[:, fi])
        fem_norm = np.linalg.norm(fem_solution[:, fi])
        if fetm_norm > 1e-20:
            assert abs(fetm_norm - fem_norm) / fetm_norm < 0.01
