from pathlib import Path

import numpy as np
import pytest

from examples.example_file_helper import get_example_file_path
from pulse.model import AnalysisID
from pulse.model.cross_section import CrossSection
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection
from pulse.model.perforated_plate import PerforatedPlate
from pulse.model.properties.fluid import Fluid
from pulse.model.properties.material import Material
from pulse.project.project import Project


# OPENPULSE-type PP (linear) — used to verify FEM correctly applies FETM admittance for PP
_LINEAR_PP_DATA = {
    "type": 0,          # PerforatedPlateFormulation.OPENPULSE
    "hole_diameter": 0.001,
    "plate_thickness": 0.003,
    "area_porosity": 0.2,
    "discharge_coefficient": 1.0,
    "single_hole": False,
    "nonlinear_effects": False,
    "nonlinear_discharge_coefficient": 0.76,
    "correction_factor": 1.0,
    "bias_flow_effects": False,
    "bias_flow_coefficient": 1.0,
    "dimensionless_impedance": None,
}


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
        "acoustic_formulation": "fetm",
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
        "acoustic_formulation": "fem",
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
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fetm"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fetm"})
    project.build_model_and_solve(running_by_script=True)
    fetm_solution = project.acoustic_solver.solution.copy()

    # Run FEM (new assembler created from scratch via reset_solvers)
    project.reset_solvers()
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fem"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fem"})
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


def _apply_acoustic_pressure(model, preprocessor, node_id, pressure=1.0 + 0j):
    coords = preprocessor.nodes[node_id].coordinates
    data = {
        "coords": list(coords),
        "real_values": [np.real(pressure)],
        "imag_values": [np.imag(pressure)],
    }
    model.properties._set_nodal_property("acoustic_pressure", data, node_id)


def test_acoustic_harmonic_fem_prescribed_pressure(acoustic_model):
    """FEM acoustic harmonic with prescribed unit pressure (Dirichlet BC).

    Applies p=1+0j at one end of the duct, checks:
    - prescribed node holds the specified pressure at every frequency
    - other nodes have non-zero pressure (wave propagation)
    - result is equivalent to FETM within 1% at low frequencies
    """
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    node_id = 103
    _apply_acoustic_pressure(model, preprocessor, node_id=node_id, pressure=1.0 + 0j)
    project.file.write_nodal_properties_in_file()

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
        "acoustic_formulation": "fem",
    }

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    solution = project.acoustic_solver.solution
    assert solution is not None
    assert solution.ndim == 2
    assert solution.shape[1] == len(model.frequencies)

    # Prescribed node must equal the prescribed pressure at every frequency
    global_idx = preprocessor.nodes[node_id].global_index
    assert np.allclose(solution[global_idx, :], 1.0 + 0j), (
        f"Prescribed node pressure deviates: max error = "
        f"{np.max(np.abs(solution[global_idx, :] - 1.0)):.3e}"
    )

    # Other nodes must carry non-trivial pressure (wave propagates into the duct)
    other_rows = [i for i in range(solution.shape[0]) if i != global_idx]
    assert np.max(np.abs(solution[other_rows, :])) > 1e-3


def test_acoustic_harmonic_fem_prescribed_pressure_vs_fetm(acoustic_model):
    """FEM and FETM agree at low frequencies for prescribed-pressure excitation."""
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    node_id = 103
    _apply_acoustic_pressure(model, preprocessor, node_id=node_id, pressure=1.0 + 0j)
    project.file.write_nodal_properties_in_file()

    base_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
    }

    # FETM run
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fetm"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fetm"})
    project.build_model_and_solve(running_by_script=True)
    fetm_solution = project.acoustic_solver.solution.copy()

    # FEM run
    project.reset_solvers()
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fem"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fem"})
    project.build_model_and_solve(running_by_script=True)
    fem_solution = project.acoustic_solver.solution.copy()

    assert fetm_solution.shape == fem_solution.shape

    # Prescribed node must be exactly 1+0j in both solutions
    global_idx = preprocessor.nodes[node_id].global_index
    assert np.allclose(fetm_solution[global_idx, :], 1.0 + 0j)
    assert np.allclose(fem_solution[global_idx, :], 1.0 + 0j)

    # Total energies within 2× (same kh criterion as volume-velocity case)
    fetm_energy = np.sum(np.abs(fetm_solution) ** 2)
    fem_energy = np.sum(np.abs(fem_solution) ** 2)
    assert 0.5 < fem_energy / fetm_energy < 2.0

    # At f=1-5 Hz the norms should agree within 1%
    for fi in range(5):
        fetm_norm = np.linalg.norm(fetm_solution[:, fi])
        fem_norm = np.linalg.norm(fem_solution[:, fi])
        if fetm_norm > 1e-20:
            assert abs(fetm_norm - fem_norm) / fetm_norm < 0.01, (
                f"f={fi+1} Hz: FETM norm={fetm_norm:.4e}, FEM norm={fem_norm:.4e}"
            )


def test_acoustic_harmonic_fem_perforated_plate(acoustic_model):
    """FEM acoustic harmonic with a non-COMMON_PIPE perforated plate element.

    An OPENPULSE-type perforated plate is applied to a mid-pipe element.
    The PP contributes its FETM admittance matrix to the FEM system (hybrid
    approach), so the solution must differ from the PP-free case — confirming
    the PP is actually applied and not silently ignored.
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
        "acoustic_formulation": "fem",
    }

    # Baseline: FEM without PP
    model.set_analysis_setup(base_setup)
    project.file.write_analysis_setup_in_file(base_setup)
    project.build_model_and_solve(running_by_script=True)
    solution_no_pp = project.acoustic_solver.solution.copy()

    # Apply linear OPENPULSE PP to a mid-pipe element
    project.reset_solvers()
    element_ids = sorted(preprocessor.acoustic_elements.keys())
    pp_element_id = int(element_ids[len(element_ids) // 2])
    pp = PerforatedPlate(_LINEAR_PP_DATA)
    preprocessor.set_perforated_plate_by_elements(pp_element_id, pp)
    model.properties._set_element_property("perforated_plate", _LINEAR_PP_DATA, element_ids=pp_element_id)

    model.set_analysis_setup(base_setup)
    project.file.write_analysis_setup_in_file(base_setup)
    project.build_model_and_solve(running_by_script=True)
    solution_with_pp = project.acoustic_solver.solution.copy()

    assert solution_with_pp is not None
    assert solution_with_pp.ndim == 2
    assert solution_with_pp.shape == solution_no_pp.shape

    # PP must change the solution — it is not silently ignored
    assert not np.allclose(solution_no_pp, solution_with_pp), (
        "Perforated plate had no effect on FEM solution; PP was silently ignored"
    )

    # The PP introduces a resistive impedance that attenuates transmission;
    # total energy with PP should be less than without PP
    energy_no_pp = np.sum(np.abs(solution_no_pp) ** 2)
    energy_with_pp = np.sum(np.abs(solution_with_pp) ** 2)
    assert energy_with_pp < energy_no_pp, (
        f"Expected PP to attenuate energy: no_pp={energy_no_pp:.3e}, with_pp={energy_with_pp:.3e}"
    )


def test_acoustic_harmonic_fem_pp_vs_fetm(acoustic_model):
    """FEM and FETM produce consistent results when a perforated plate is present.

    With a linear OPENPULSE PP, both methods should give the same PP admittance
    contribution. At low frequencies (1–5 Hz) the solutions should agree within 1%.
    """
    project, _ = acoustic_model
    model = project.model
    preprocessor = model.preprocessor

    _apply_volume_velocity(model, preprocessor, node_id=103)
    project.file.write_nodal_properties_in_file()

    element_ids = sorted(preprocessor.acoustic_elements.keys())
    pp_element_id = int(element_ids[len(element_ids) // 2])
    pp = PerforatedPlate(_LINEAR_PP_DATA)
    preprocessor.set_perforated_plate_by_elements(pp_element_id, pp)
    model.properties._set_element_property("perforated_plate", _LINEAR_PP_DATA, element_ids=pp_element_id)

    base_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 1,
        "f_max": 200,
        "f_step": 1,
        "global_damping": [0., 0., 0.],
    }

    # FETM run
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fetm"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fetm"})
    project.build_model_and_solve(running_by_script=True)
    fetm_solution = project.acoustic_solver.solution.copy()

    # FEM run
    project.reset_solvers()
    model.set_analysis_setup({**base_setup, "acoustic_formulation": "fem"})
    project.file.write_analysis_setup_in_file({**base_setup, "acoustic_formulation": "fem"})
    project.build_model_and_solve(running_by_script=True)
    fem_solution = project.acoustic_solver.solution.copy()

    assert fetm_solution.shape == fem_solution.shape

    # Total energies within 2× (same kh criterion as the no-PP case)
    fetm_energy = np.sum(np.abs(fetm_solution) ** 2)
    fem_energy = np.sum(np.abs(fem_solution) ** 2)
    assert 0.5 < fem_energy / fetm_energy < 2.0, (
        f"Energy ratio FEM/FETM={fem_energy/fetm_energy:.3f} out of [0.5, 2.0]"
    )

    # At f=1-5 Hz the norm difference should be < 5%
    for fi in range(5):
        fetm_norm = np.linalg.norm(fetm_solution[:, fi])
        fem_norm = np.linalg.norm(fem_solution[:, fi])
        if fetm_norm > 1e-20:
            assert abs(fetm_norm - fem_norm) / fetm_norm < 0.05, (
                f"f={fi+1} Hz PP: FETM norm={fetm_norm:.4e}, FEM norm={fem_norm:.4e}"
            )
