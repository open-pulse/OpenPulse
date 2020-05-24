import numpy as np 
import pytest

from pulse.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution import Solution


# Setting up model
@pytest.fixture
def mesh_():
    steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
    cross_section = CrossSection(0.05, 0.008)
    mesh = Mesh()
    mesh.generate('iges_files\\tube_1.iges', 0.01)

    mesh.set_structural_boundary_condition_by_node([40, 1424, 1324], np.zeros(6))
    mesh.set_material_by_element('all', steel)
    mesh.set_cross_section_by_element('all', cross_section)

    return mesh

# start testing 
def test_modal_analysis(mesh_):
    solution = Solution(mesh_)
    natural_frequencies, modal_shape = solution.modal_analysis(modes=200, harmonic_analysis=True)
    correct_natural_frequencies = np.load('matrices\\structural_solution\\natural_frequencies.npy')
    correct_modal_shape = np.load('matrices\\structural_solution\\modal_shape.npy')
    
    assert np.allclose(natural_frequencies, correct_natural_frequencies)
    assert np.allclose(modal_shape, correct_modal_shape)

def test_direct_method(mesh_):
    solution = Solution(mesh_)
    frequencies = np.arange(0, 200+1, 2)
    
    direct_method = solution.direct_method(frequencies, is_viscous_lumped=True)
    correct_direct_method = np.load('matrices\\structural_solution\\direct_method.npy')

    assert np.allclose(direct_method, correct_direct_method)

def test_modal_superposition(mesh_):
    solution = Solution(mesh_)
    frequencies = np.arange(0, 200+1, 2)
    modes = 200

    modal_superposition = solution.modal_superposition(frequencies, modes, fastest=True)
    correct_modal_superposition = np.load('matrices\\structural_solution\\modal_superposition.npy')

    assert np.allclose(modal_superposition, correct_modal_superposition)
