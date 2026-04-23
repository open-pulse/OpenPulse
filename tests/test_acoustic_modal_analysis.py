import numpy as np

from pulse.model import AnalysisID


def test_acoustic_modal_analysis(example2_project):
    project, mesher_setup = example2_project
    model = project.model

    analysis_setup = {
        "analysis_id": AnalysisID.ACOUSTIC_MODAL,
        "number_of_modes": 20,
        "sigma_factor": 1e-2,
    }
    model.set_analysis_setup(analysis_setup=analysis_setup)

    project.file.write_line_properties_in_file()
    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)

    project.build_model_and_solve(running_by_script=True)

    natural_frequencies = project.acoustic_solver.natural_frequencies

    assert natural_frequencies is not None, "No acoustic natural frequencies returned"
    assert len(natural_frequencies) > 0, "Acoustic natural frequencies array is empty"
    assert np.all(natural_frequencies >= 0), "Negative acoustic natural frequencies"
    assert np.all(np.isfinite(natural_frequencies)), "Non-finite acoustic natural frequencies"
    assert np.all(np.diff(natural_frequencies) >= 0), "Acoustic natural frequencies not in ascending order"
