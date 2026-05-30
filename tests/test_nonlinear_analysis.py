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


# ── Perforated plate configuration ───────────────────────────────────────────

_PP_DATA = {
    "type": 0,
    "hole_diameter": 0.001,
    "plate_thickness": 0.003,
    "area_porosity": 0.2,
    "discharge_coefficient": 1.0,
    "single_hole": False,
    "nonlinear_effects": True,
    "nonlinear_discharge_coefficient": 0.76,
    "correction_factor": 1.0,
    "bias_flow_effects": False,
    "bias_flow_coefficient": 1.0,
    "dimensionless_impedance": None,
}


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def nonlinear_model(datadir: Path):
    """
    Acoustic model with a nonlinear perforated plate element.

    Sets up the same L-pipe geometry used in the acoustic tests, adds a
    perforated plate with ``nonlinear_effects=True`` to a mid-pipe element,
    and applies a volume velocity excitation at a boundary node.
    """
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

    # Pick a mid-pipe element for the perforated plate (avoid boundary elements).
    # Cast to Python int: numpy int64 from dict keys fails isinstance(x, int) in
    # numpy >= 2.0, which breaks the slicer utility used by set_perforated_plate_*.
    element_ids = sorted(preprocessor.acoustic_elements.keys())
    pp_element_id = int(element_ids[len(element_ids) // 2])

    pp = PerforatedPlate(_PP_DATA)
    preprocessor.set_perforated_plate_by_elements(pp_element_id, pp)
    model.properties._set_element_property("perforated_plate", _PP_DATA, element_ids=pp_element_id)

    # Apply volume velocity excitation at a boundary node
    excitation_node_id = 103
    coords = preprocessor.nodes[excitation_node_id].coordinates
    volume_velocity = [0.001 + 0j]
    data = {
        "coords": list(coords),
        "values": volume_velocity,
        "real_values": [np.real(v) for v in volume_velocity],
        "imag_values": [np.imag(v) for v in volume_velocity],
    }
    model.properties._set_nodal_property("volume_velocity", data, excitation_node_id)

    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)

    return project, pp_element_id


# ── Integration tests ─────────────────────────────────────────────────────────


def test_nl_elements_detected(nonlinear_model):
    """AcousticAssembler must detect the nonlinear perforated plate element."""
    project, pp_element_id = nonlinear_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 50,
        "f_max": 150,
        "f_step": 50,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    # initialize_solver creates acoustic_assembler but does NOT solve yet
    project.model.preprocessor.process_cross_sections_mapping()
    project.initialize_solver()

    assembler = project.acoustic_assembler
    assert len(assembler.nl_elements) == 1
    detected_ids = {el.index for el in assembler.nl_elements}
    assert pp_element_id in detected_ids


def test_nonlinear_direct_method_solution_shape(nonlinear_model):
    """Nonlinear solver must produce a 2-D complex solution with one column per frequency."""
    project, _ = nonlinear_model
    model = project.model

    f_min, f_max, f_step = 50, 150, 50
    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": f_min,
        "f_max": f_max,
        "f_step": f_step,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    solution = project.acoustic_solver.solution
    assert solution is not None
    assert solution.ndim == 2
    assert solution.shape[1] == len(model.frequencies)
    assert np.iscomplexobj(solution)


def test_nonlinear_convergence_data_log(nonlinear_model):
    """Convergence data log must be populated after a successful nonlinear solve."""
    project, _ = nonlinear_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 50,
        "f_max": 150,
        "f_step": 50,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    log = project.perforated_plate_data_log
    assert log is not None

    iterations, pressure_residues, delta_residues, target_pct = log
    assert len(iterations) > 0
    assert len(pressure_residues) == len(iterations)
    assert len(delta_residues) == len(iterations)
    assert target_pct == pytest.approx(10.0)  # default 10 %
    assert all(r >= 0 for r in pressure_residues)
    assert all(r >= 0 for r in delta_residues)


def test_nonlinear_pressure_residues_decrease(nonlinear_model):
    """
    After convergence, the last recorded pressure residue must be below the
    convergence target (10 %).
    """
    project, _ = nonlinear_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 50,
        "f_max": 150,
        "f_step": 50,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    log = project.perforated_plate_data_log
    assert log is not None

    _, pressure_residues, _, target_pct = log
    assert pressure_residues[-1] < target_pct


def test_nonlinear_solver_frequencies_stored(nonlinear_model):
    """Solver must record the frequency vector used during the nonlinear solve."""
    project, _ = nonlinear_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 50,
        "f_max": 150,
        "f_step": 50,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    solver = project.acoustic_solver
    assert solver.frequencies is not None
    np.testing.assert_array_equal(solver.frequencies, model.frequencies)


def test_nonlinear_differs_from_linear(nonlinear_model, datadir: Path):
    """
    The nonlinear solution must differ from a linear solution on the same model,
    since the perforated plate changes the system impedance.
    """
    project, pp_element_id = nonlinear_model
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_HARMONIC,
        "f_min": 50,
        "f_max": 150,
        "f_step": 50,
        "global_damping": [0.0, 0.0, 0.0],
        "analysis_method": "direct",
    }

    # ── Nonlinear solve ───────────────────────────────────────────────────
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)
    project.build_model_and_solve(running_by_script=True)
    nl_solution = project.acoustic_solver.solution.copy()

    # ── Linear solve: same model, nonlinear_effects disabled ─────────────
    preprocessor = model.preprocessor
    linear_pp_data = {**_PP_DATA, "nonlinear_effects": False}
    linear_pp = PerforatedPlate(linear_pp_data)
    preprocessor.set_perforated_plate_by_elements(pp_element_id, linear_pp)
    model.properties._set_element_property("perforated_plate", linear_pp_data, element_ids=pp_element_id)

    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.build_model_and_solve(running_by_script=True)
    linear_solution = project.acoustic_solver.solution.copy()

    # The two solutions must not be identical
    assert not np.allclose(nl_solution, linear_solution), (
        "Nonlinear and linear solutions are identical — nonlinear effects had no impact."
    )
