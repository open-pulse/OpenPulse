import numpy as np 
import pytest

from pulse.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.processing.solution_structural import SolutionStructural


# Setting up model
@pytest.fixture
def mesh_():
    steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
    cross_section = CrossSection(0.05, 0.008)
    preprocessor = Preprocessor()
    preprocessor.generate('iges_files\\tube_1.iges', 0.01)

    preprocessor.set_prescribed_dofs_bc_by_node([40, 1424, 1324], np.zeros(6))
    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_element('all', cross_section)

    return mesh

# start testing 
def test_modal_analysis(preprocessor):
    solution = SolutionStructural(preprocessor)
    natural_frequencies, modal_shape = solution.modal_analysis(modes=200, harmonic_analysis=True)
    correct_natural_frequencies = np.load('matrices\\structural_solution\\natural_frequencies.npy')
    correct_modal_shape = np.load('matrices\\structural_solution\\mode_shapes.npy')
    
    assert np.allclose(natural_frequencies, correct_natural_frequencies)
    assert np.allclose(modal_shape, correct_modal_shape)

def test_direct_method(preprocessor):
    solution = SolutionStructural(preprocessor)
    frequencies = np.arange(0, 200+1, 2)
    
    direct_method = solution.direct_method(frequencies, is_viscous_lumped=True)
    correct_direct_method = np.load('matrices\\structural_solution\\direct_method.npy')

    assert np.allclose(direct_method, correct_direct_method)

def test_mode_superposition(preprocessor):
    solution = SolutionStructural(preprocessor)
    frequencies = np.arange(0, 200+1, 2)
    modes = 200

    mode_superposition = solution.mode_superposition(frequencies, modes, fastest=True)
    correct_mode_superposition = np.load('matrices\\structural_solution\\mode_superposition.npy')

    assert np.allclose(mode_superposition, correct_mode_superposition)
