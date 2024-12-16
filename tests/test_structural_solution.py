import numpy as np 
import pytest
from pathlib import Path
from os.path import basename

from pulse.utils.common_utils import sparse_is_equal
from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.model import Model
from pulse.model.preprocessor import Preprocessor
from pulse.project.project import Project
from pulse.processing.structural_solver import StructuralSolver
# from pulse.postprocessing.read_data import ReadData

# Setting up model
@pytest.fixture
def current_model():
    return

    section_parameters = [0.08, 0.008, 0, 0, 0, 0]
    pipe_section_info = {  "section_type_label" : "Pipe" ,
                            "section_parameters" : section_parameters  }

    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
    
    project = Project()
    model = Model(project)
    preprocessor = model.preprocessor
    mesh = preprocessor.mesh

    geometry_path = Path("examples/iges_files/new_geometries/example_2_withBeam.iges")

    mesher_setup = { 
                    "length_unit" : "meter",
                    "element_size" : 0.01,
                    "geometry_tolerance" : 1e-6,
                    "import_type" : 0,
                    "geometry_filename" : basename(str(geometry_path)),
                    "geometry_path" : str(geometry_path)
                    }

    mesh.set_mesher_setup(mesher_setup = mesher_setup)

    preprocessor.generate()

    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_elements('all', cross_section)

    # preprocessor.set_structural_damping([1e-3, 1e-6, 0, 0])
    table_names = [None, None, None, None, None, None]
    preprocessor.set_prescribed_dofs([1223, 10, 665, 921, 796], [np.zeros(6, dtype=complex), table_names])
    preprocessor.set_structural_loads([690], [np.array([1,0,0,0,0,0], dtype=complex), table_names])
    preprocessor.set_structural_loads([1108], [np.array([0,0,1,0,0,0], dtype=complex), table_names])

    return preprocessor

# start testing 
def test_modal_analysis(current_model):
    #TODO: update this test
    return
    project = current_model.project
    model = current_model.model
    solution = StructuralSolver(model, None)
    natural_frequencies, eigen_vectors = solution.modal_analysis(modes=40)
    folder_path = "tests/data/structural"
    file_name = "modal_analysis_results.hdf5"
    read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_natural_frequencies = project.natural_frequencies_structural
    correct_eigen_vectors = project.solution_structural
    assert np.allclose(natural_frequencies, correct_natural_frequencies)
    assert np.allclose(eigen_vectors, correct_eigen_vectors)

def test_direct_method(current_model):
    #TODO: update this test
    return
    project = current_model.project
    model = current_model.model
    frequencies = np.linspace(0, 200, 201)
    solve = StructuralSolver(model, frequencies)    
    solution = solve.direct_method()
    folder_path = "tests/data/structural"
    file_name = "harmonic_analysis_results_direct.hdf5"
    # read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_solution = project.solution_structural
    assert np.allclose(solution, correct_solution)

def test_mode_superposition(current_model, modes=60):
    #TODO: update this test
    return
    project = current_model.project
    model = current_model.model
    frequencies = np.linspace(0, 200, 201)
    solution = StructuralSolver(model, frequencies)
    solution = solution.mode_superposition(modes, fastest=True)
    folder_path = "tests/data/structural"
    file_name = "harmonic_analysis_results_mode_superposition.hdf5"
    # read = ReadData(project, file_name=file_name, folder_path=folder_path)
    correct_solution = project.solution_structural
    assert np.allclose(solution, correct_solution)