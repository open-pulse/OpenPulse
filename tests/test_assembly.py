import pytest
import numpy as np 
from pathlib import Path
from scipy.sparse import save_npz, load_npz

from examples.example_file_helper import get_example_file_path
from pulse.utils.common_utils import sparse_is_equal
from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.model import Model
from pulse.model.preprocessor import Preprocessor
from pulse.project.project import Project
from pulse.processing.assembly_structural import AssemblyStructural
from pulse.model.cross_sections.pipe_cross_section import PipeCrossSection

# Setting up model
@pytest.fixture
def model():

    # create a material object
    steel = Material(
        name = 'Steel', 
        identifier = 1,
        density = 7850, 
        elasticity_modulus = 200e9, 
        poisson_ratio = 0.3,
        )

    section_parameters = [0.05, 0.008, 0, 0, 0, 0]
    pipe_section_info = PipeCrossSection(*section_parameters)

    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    project = Project()
    model = Model(project)
    preprocessor = model.preprocessor
    geometry_path = get_example_file_path("iges_files/new_geometries/example_2_withBeam.iges")
    preprocessor.generate(geometry_path, 0.01)

    table_names = [None, None, None, None, None, None]
    preprocessor.set_prescribed_dof([40, 1424, 1324], [np.zeros(6), table_names])

    preprocessor.set_material_by_element('all', steel)
    preprocessor.set_cross_section_by_element('all', cross_section)

    frequencies = np.linspace(0, 200, 101)
    assembly = AssemblyStructural(model, frequencies)

    # We need to separate it in multiple atribute or functions as soon as possible. 
    # names = ['Kadd_lump', 'Madd_lump', 'K', 'M', 'Kr', 'Mr', 'K_lump', 'M_lump', 'C_lump', 'Kr_lump', 'Mr_lump', 'Cr_lump']
    names = ['K', 'M', 'Kr', 'Mr']
    answer = assembly.get_global_matrices()

    return dict(zip(names, answer))


# we need a better way to test similarity 
# sparse matrix operands are ridiculous

# # start testing 
# def test_matrices(model):
#     names = ['Kadd_lump', 'Madd_lump', 'K', 'M', 'Kr', 'Mr', 'K_lump', 'M_lump', 'C_lump', 'Kr_lump', 'Mr_lump', 'Cr_lump']
#     for name in names:
#         correct_matrix = load_npz(f'matrices\\assembly\\{name}.npz')
#         testing_matrix = model[name]
#         assert sparse_is_equal(correct_matrix, testing_matrix)


