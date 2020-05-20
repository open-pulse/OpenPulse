import sys 
import os 
sys.path.append('..')

import numpy as np 
from scipy.sparse import save_npz, load_npz

from pulse.utils import sparse_is_equal
from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import Assembly 


# Setting up model
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.008)
mesh = Mesh()
mesh.generate('iges_files\\tube_1.iges', 0.01)

mesh.set_structural_boundary_condition_by_node([40, 1424, 1324], np.zeros(6))
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)
assembly = Assembly(mesh)

# We can do better, i swear
Kadd_lump, Madd_lump, K, M, Kr, Mr, K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump = assembly.get_all_matrices()

def save_correct_matrices():
    save_npz('matrices\\assembly\\Kadd_lump', Kadd_lump)
    save_npz('matrices\\assembly\\Madd_lump', Madd_lump)
    save_npz('matrices\\assembly\\K', K)
    save_npz('matrices\\assembly\\M', M)
    save_npz('matrices\\assembly\\Kr', Kr)
    save_npz('matrices\\assembly\\Mr', Mr)
    save_npz('matrices\\assembly\\K_lump', K_lump)
    save_npz('matrices\\assembly\\M_lump', M_lump)
    save_npz('matrices\\assembly\\C_lump', C_lump)
    save_npz('matrices\\assembly\\Kr_lump', Kr_lump)
    save_npz('matrices\\assembly\\Mr_lump', Mr_lump)
    save_npz('matrices\\assembly\\Cr_lump', Cr_lump)


# we need a better way to test similarity 
# sparse matrix operands are ridiculous

# start testing 
def test_Kadd_lump(): 
    correct_Kadd_lump = load_npz('matrices\\assembly\\Kadd_lump.npz')
    assert sparse_is_equal(correct_Kadd_lump, Kadd_lump)

def test_Madd_lump(): 
    correct_Madd_lump = load_npz('matrices\\assembly\\Madd_lump.npz')
    assert sparse_is_equal(correct_Madd_lump, Madd_lump)

def test_K(): 
    correct_K = load_npz('matrices\\assembly\\K.npz')
    assert sparse_is_equal(correct_K, K)

def test_M(): 
    correct_M = load_npz('matrices\\assembly\\M.npz')
    assert sparse_is_equal(correct_M, M)

def test_Kr(): 
    correct_Kr = load_npz('matrices\\assembly\\Kr.npz')
    assert sparse_is_equal(correct_Kr, Kr)

def test_Mr(): 
    correct_Mr = load_npz('matrices\\assembly\\Mr.npz')
    assert sparse_is_equal(correct_Mr, Mr)

def test_K_lump(): 
    correct_K_lump = load_npz('matrices\\assembly\\K_lump.npz')
    assert sparse_is_equal(correct_K_lump, K_lump)

def test_M_lump(): 
    correct_M_lump = load_npz('matrices\\assembly\\M_lump.npz')
    assert sparse_is_equal(correct_M_lump, M_lump)

def test_C_lump(): 
    correct_C_lump = load_npz('matrices\\assembly\\C_lump.npz')
    assert sparse_is_equal(correct_C_lump, C_lump)

def test_Kr_lump(): 
    correct_Kr_lump = load_npz('matrices\\assembly\\Kr_lump.npz')
    assert sparse_is_equal(correct_Kr_lump, Kr_lump)

def test_Mr_lump(): 
    correct_Mr_lump = load_npz('matrices\\assembly\\Mr_lump.npz')
    assert sparse_is_equal(correct_Mr_lump, Mr_lump)

def test_Cr_lump(): 
    correct_Cr_lump = load_npz('matrices\\assembly\\Cr_lump.npz')
    assert sparse_is_equal(correct_Cr_lump, Cr_lump)
