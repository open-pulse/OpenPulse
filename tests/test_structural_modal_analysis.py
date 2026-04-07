import numpy as np

from pulse.model import AnalysisID


def test_structural_modal_analysis(example2_project, num_regression):
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

    analysis_setup = {
        "analysis_id": AnalysisID.STRUCTURAL_MODAL,
        "number_of_modes": 40,
        "sigma_factor": 1e-2,
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)

    project.file.write_line_properties_in_file()
    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    natural_frequencies = project.natural_frequencies_structural
    # natural_frequencies = project.natural_frequencies_acoustic
    print(f"Natural frequencies: \n {natural_frequencies.reshape(-1, 1)}")

    assert natural_frequencies is not None, "No natural frequencies returned"
    assert len(natural_frequencies) == 40, f"Expected 40 modes, got {len(natural_frequencies)}"
    assert np.all(natural_frequencies >= 0), "Negative natural frequencies"
    assert np.all(np.isfinite(natural_frequencies)), "Non-finite natural frequencies"
    assert np.all(np.diff(natural_frequencies) >= 0), "Natural frequencies not in ascending order"

    num_regression.check(
        {"natural_frequencies": natural_frequencies},
        default_tolerance=dict(atol=1e-4, rtol=1e-4),
    )
