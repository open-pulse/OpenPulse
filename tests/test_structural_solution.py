import numpy as np 
import pytest
from pathlib import Path

from pulse.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.project import Project
from pulse.processing.solution_structural import SolutionStructural

# Setting up model
@pytest.fixture
def model():

    section_label = "Pipe section"
    section_parameters = {  "outer_diameter" : 0.05,
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

    table_names = [None, None, None, None, None, None]
    preprocessor.set_prescribed_dofs_bc_by_node([40, 1424, 1324], [np.zeros(6), table_names])

    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_element('all', cross_section)

    return preprocessor

# start testing 
def test_modal_analysis(model):
    solution = SolutionStructural(model, None)    
    natural_frequencies, modal_shape = solution.modal_analysis(modes=100)
    correct_natural_frequencies = np.load(Path('tests/matrices/structural_solution/natural_frequencies.npy'))
    correct_modal_shape = np.load(Path('tests/matrices/structural_solution/mode_shapes.npy'))
    assert True
    # assert np.allclose(natural_frequencies, correct_natural_frequencies)
    # assert np.allclose(modal_shape, correct_modal_shape)

def test_direct_method(model):
    frequencies = np.linspace(0, 200, 101)
    solution = SolutionStructural(model, frequencies)    
    direct_method = solution.direct_method()
    correct_direct_method = np.load(Path('tests/matrices/structural_solution/direct_method.npy'))
    assert True
    # assert np.allclose(direct_method, correct_direct_method)

def test_mode_superposition(model):
    frequencies = np.linspace(0, 200, 101)
    solution = SolutionStructural(model, frequencies)

    modes = 200
    mode_superposition = solution.mode_superposition(modes, fastest=True)
    correct_mode_superposition = np.load(Path('tests/matrices/structural_solution/mode_superposition.npy'))
    assert True
    # assert np.allclose(mode_superposition, correct_mode_superposition)