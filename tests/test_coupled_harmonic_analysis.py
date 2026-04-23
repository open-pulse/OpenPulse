import numpy as np

from pulse.model import AnalysisID


def test_coupled_harmonic_analysis(example2_project):
    project, mesher_setup = example2_project
    model = project.model
    preprocessor = model.preprocessor

    ## Apply nodal loads
    load_coords = np.array([
        [0.500,  0.000,  0.000],
        [1.200, -0.250,  1.250],
    ], dtype=float)

    for coords in load_coords:
        node_id = preprocessor.get_node_id_by_coordinates(coords)
        nodal_loads = [None, None, 1 + 0j, None, None, None]
        data = {
            "coords": list(coords),
            "values": nodal_loads,
            "real_values": [v if v is None else np.real(v) for v in nodal_loads],
            "imag_values": [v if v is None else np.imag(v) for v in nodal_loads],
        }
        model.properties._set_nodal_property("nodal_loads", data, node_id)

    ## Apply volume velocity excitation
    coords = np.array([0.000, 0.000, 0.000])
    node_id = preprocessor.get_node_id_by_coordinates(coords)
    volume_velocity = [0.01 + 0j]
    data = {
        "coords": list(coords),
        "values": volume_velocity,
        "real_values": [np.real(v) for v in volume_velocity],
        "imag_values": [np.imag(v) for v in volume_velocity],
    }
    model.properties._set_nodal_property("volume_velocity", data, node_id)

    ## Apply radiation impedance
    coords = np.array([2.000, -0.250, 1.250])
    node_id = preprocessor.get_node_id_by_coordinates(coords)
    model.properties._set_nodal_property(
        "radiation_impedance",
        {"coords": list(coords), "impedance_type": "flanged"},
        node_id,
    )

    analysis_setup = {
        "analysis_id": AnalysisID.COUPLED_HARMONIC,
        "f_min": 1,
        "f_max": 300,
        "f_step": 1,
        "global_damping": [1e-3, 1e-5, 0.],
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)

    project.file.write_line_properties_in_file()
    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    structural_solution = project.structural_solution
    acoustic_solution = project.acoustic_solution

    assert structural_solution is not None, "No structural solution returned"
    assert acoustic_solution is not None, "No acoustic solution returned"
    assert structural_solution.ndim == 2, "Structural solution must be 2D"
    assert acoustic_solution.ndim == 2, "Acoustic solution must be 2D"
    assert structural_solution.shape[1] == 300, f"Expected 300 freq points, got {structural_solution.shape[1]}"
    assert acoustic_solution.shape[1] == 300, f"Expected 300 freq points, got {acoustic_solution.shape[1]}"
    assert np.any(np.abs(structural_solution) > 0), "Acoustic solution is all zeros"
    assert np.any(np.abs(acoustic_solution) > 0), "Acoustic solution is all zeros"
    assert np.all(np.isfinite(structural_solution)), "Non-finite values in structural solution"
    assert np.all(np.isfinite(acoustic_solution)), "Non-finite values in acoustic solution"
