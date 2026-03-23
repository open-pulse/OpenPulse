import numpy as np 
import pytest
from pathlib import Path

from examples.example_file_helper import get_example_file_path
from pulse.model import AnalysisID
from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.postprocessing.plot_structural_data import get_structural_frf
from pulse.project.project import Project

# Setting up model
@pytest.fixture
def current_model(datadir: Path):
    section_parameters = [0.01, 0.001, 0, 0, 0, 0]
    pipe_section_info = {  "section_type_label" : "pipe" ,
                            "section_parameters" : section_parameters  }

    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    steel = Material('Steel', 7850, elasticity_modulus=200e9, poisson_ratio=0.3, identifier=1)
    
    # Initialize project
    project = Project()
    project.initialize_pulse_file_and_loader(dir_path=str(datadir))
    
    model = project.model
    mesh = model.mesh
    preprocessor = model.preprocessor

    geometry_path = get_example_file_path("iges_files/new_geometries/simple_L_pipe.iges")

    mesher_setup = { 
                    "element_size" : 0.01,
                    "geometry_tolerance" : 1e-6,
                    "length_unit" : "meter",
                    "import_type" : 0,
                    "geometry_path" : str(geometry_path)
                    }

    project.reset(reset_all=True)
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    preprocessor.generate()

    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_elements('all', cross_section)

    # Apply prescribed 
    node_id = 103
    coords = preprocessor.nodes[node_id].coordinates
    prescribed_dofs = [0j, 0j, 0j, 0j, 0j, 0j]
    real_values = [value if value is None else np.real(value) for value in prescribed_dofs]
    imag_values = [value if value is None else np.imag(value) for value in prescribed_dofs]
    
    data = {
            "coords" : list(coords),
            "values" : prescribed_dofs,
            "real_values" : real_values,
            "imag_values" : imag_values
            }
    
    model.properties._set_nodal_property("prescribed_dofs", data, node_id)
    
    # Apply nodal loads
    node_id = 152
    load_values = [1+0j, 0j, 0j, 0j, 0j, 0j]
    
    coords = preprocessor.nodes[node_id].coordinates
    nodal_loads = load_values
    real_values = [value if value is None else np.real(value) for value in nodal_loads]
    imag_values = [value if value is None else np.imag(value) for value in nodal_loads]
    
    data = {
            "coords" : list(coords),
            "values" : nodal_loads,
            "real_values" : real_values,
            "imag_values" : imag_values
            }
    
    model.properties._set_nodal_property("nodal_loads", data, node_id)

    # Write properties to file
    project.file.write_nodal_properties_in_file()
    project.file.write_project_setup_in_file(mesher_setup)

    return project


def test_modal_analysis(current_model, num_regression):
    project = current_model
    model = project.model
    
    # Analysis setup for structural modal analysis
    analysis_setup = {
                      "analysis_id" : AnalysisID.STRUCTURAL_MODAL,
                      "number_of_modes" : 40,
                      "sigma_factor" : 1e-2
                      }
    
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)
    
    # Build and solve the model
    project.build_model_and_solve(running_by_script=True)
    
    # Get the results
    natural_frequencies = project.natural_frequencies_structural
    eigen_vectors = project.structural_solution
    
    # Verify results exist and have correct shape
    assert natural_frequencies is not None
    assert eigen_vectors is not None
    assert len(natural_frequencies) == 40
    assert eigen_vectors.shape[1] == 40
    
    # Regression tests - compare against stored baseline
    # Store natural frequencies as array
    num_regression.check(
        {
            "natural_frequencies": natural_frequencies,
        },
        default_tolerance=dict(atol=1e-6, rtol=1e-6)
    )


def test_direct_method(current_model, num_regression):
    project = current_model
    model = project.model
    
    # Analysis setup for structural harmonic analysis
    analysis_setup = {
                      "analysis_id" : AnalysisID.STRUCTURAL_HARMONIC,
                      "f_min" : 0,
                      "f_max" : 200,
                      "f_step" : 1,
                      "global_damping" : [1e-3, 1e-5, 0.],
                      "analysis_method" : "direct"
                      }
    
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)
    
    # Build and solve the model
    project.build_model_and_solve(running_by_script=True)
    
    # Get the results
    solution = project.structural_solution
    
    # Verify results exist and have correct shape
    assert solution is not None
    assert len(solution.shape) == 2  # Should be 2D array
    assert solution.shape[1] == 201  # 0 to 200 Hz with 1 Hz step

    response = get_structural_frf(model.preprocessor, solution, 152, 0, absolute=True)

    # Regression tests - compare against stored baseline
    num_regression.check(
        {
            "frequencies": model.frequencies,
            "response": response
        },
        default_tolerance=dict(atol=1e-6, rtol=1e-6)
    )



def test_mode_superposition(current_model, num_regression):
    project = current_model
    model = project.model
    
    # Analysis setup for structural harmonic analysis with mode superposition
    analysis_setup = {
                      "analysis_id" : AnalysisID.STRUCTURAL_HARMONIC,
                      "f_min" : 0,
                      "f_max" : 200,
                      "f_step" : 1,
                      "global_damping" : [1e-3, 1e-5, 0.],
                      "analysis_method" : "mode_superposition",
                      "number_of_modes" : 60
                      }
    
    model.set_analysis_setup(analysis_setup=analysis_setup)
    project.file.write_analysis_setup_in_file(analysis_setup)
    
    # Build and solve the model
    project.build_model_and_solve(running_by_script=True)
    
    # Get the results
    solution = project.structural_solution
    
    # Verify results exist and have correct shape
    assert solution is not None
    assert len(solution.shape) == 2  # Should be 2D array
    assert solution.shape[1] == 201  # 0 to 200 Hz with 1 Hz step

    response = get_structural_frf(model.preprocessor, solution, 152, 0, absolute=True)

    # Regression tests - compare against stored baseline
    num_regression.check(
        {
            "frequencies": model.frequencies,
            "response": response
        },
        default_tolerance=dict(atol=1e-6, rtol=1e-6)
    )
