import numpy as np 
import pytest
from pathlib import Path

from pulse.tools.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.project import Project
from pulse.processing.solution_structural import SolutionStructural
from pulse.postprocessing.read_data import ReadData

# Setting up model
@pytest.fixture
def model():

    section_label = "Pipe section"
    section_parameters = {  "outer_diameter" : 0.08,
                            "thickness" : 0.008,
                            "offset_y" : 0,
                            "offset_z" : 0,
                            "insulation_thickness" : 0,
                            "insulation_density" : 0  }

    pipe_section_info = {  "section_type_label" : section_label ,
                            "section_parameters" : section_parameters  }

    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
    
    project = Project()
    preprocessor = Preprocessor(project)
    geometry_path = Path("examples/iges_files/new_geometries/example_2_withBeam.iges")
    preprocessor.generate(geometry_path, 0.01)
    preprocessor.set_structural_damping([1e-3, 1e-6, 0, 0])

    table_names = [None, None, None, None, None, None]
    preprocessor.set_prescribed_dofs_bc_by_node([1223, 10, 665, 921, 796], [np.zeros(6, dtype=complex), table_names])
    preprocessor.set_structural_load_bc_by_node([690], [np.array([1,0,0,0,0,0], dtype=complex), table_names])
    preprocessor.set_structural_load_bc_by_node([1108], [np.array([0,0,1,0,0,0], dtype=complex), table_names])

    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_element('all', cross_section)

    return preprocessor

# start testing 
def test_modal_analysis(model):
    project = model.project
    solution = SolutionStructural(model, None)
    natural_frequencies, eigen_vectors = solution.modal_analysis(modes=40)
    folder_path = "tests/data/structural"
    file_name = "modal_analysis_results.hdf5"
    read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_natural_frequencies = project.natural_frequencies_structural
    correct_eigen_vectors = project.solution_structural
    assert np.allclose(natural_frequencies, correct_natural_frequencies)
    assert np.allclose(eigen_vectors, correct_eigen_vectors)

def test_direct_method(model):
    project = model.project
    frequencies = np.linspace(0, 200, 201)
    solve = SolutionStructural(model, frequencies)    
    solution = solve.direct_method()
    folder_path = "tests/data/structural"
    file_name = "harmonic_analysis_results_direct.hdf5"
    read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_solution = project.solution_structural
    assert np.allclose(solution, correct_solution)

def test_mode_superposition(model, modes=60):
    project = model.project
    frequencies = np.linspace(0, 200, 201)
    solution = SolutionStructural(model, frequencies)
    solution = solution.mode_superposition(modes, fastest=True)
    folder_path = "tests/data/structural"
    file_name = "harmonic_analysis_results_mode_superposition.hdf5"
    read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_solution = project.solution_structural
    assert np.allclose(solution, correct_solution)