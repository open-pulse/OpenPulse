import numpy as np 
from scipy.sparse import save_npz, load_npz
import pytest 

from pulse.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import Assembly 

# Setting up model
@pytest.fixture
def model():
    steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
    cross_section = CrossSection(0.05, 0.008)
    mesh = Mesh()
    mesh.generate('iges_files\\tube_1.iges', 0.01)

    mesh.set_structural_boundary_condition_by_node([40, 1424, 1324], np.zeros(6))
    mesh.set_material_by_element('all', steel)
    mesh.set_cross_section_by_element('all', cross_section)
    assembly = Assembly(mesh)

    # We need to separate it in multiple atribute or functions as soon as possible. 
    names = ['Kadd_lump', 'Madd_lump', 'K', 'M', 'Kr', 'Mr', 'K_lump', 'M_lump', 'C_lump', 'Kr_lump', 'Mr_lump', 'Cr_lump']
    answer = assembly.get_all_matrices()

    return dict(zip(names, answer))


# we need a better way to test similarity 
# sparse matrix operands are ridiculous

# start testing 
def test_matrices(model):
    names = ['Kadd_lump', 'Madd_lump', 'K', 'M', 'Kr', 'Mr', 'K_lump', 'M_lump', 'C_lump', 'Kr_lump', 'Mr_lump', 'Cr_lump']
    for name in names:
        correct_matrix = load_npz(f'matrices\\assembly\\{name}.npz')
        testing_matrix = model[name]
        assert sparse_is_equal(correct_matrix, testing_matrix)


