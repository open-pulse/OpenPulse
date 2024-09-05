import pytest
import numpy as np 
from pathlib import Path
from scipy.sparse import save_npz, load_npz

from pulse.tools.utils import sparse_is_equal
from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.model import Model
from pulse.model.preprocessor import Preprocessor
from pulse.project.project import Project
from pulse.processing.assembly_structural import AssemblyStructural 

# Setting up model
@pytest.fixture
def model():

    section_parameters = [0.05, 0.008, 0, 0, 0, 0]
    pipe_section_info = {  "section_type_label" : "Pipe" ,
                            "section_parameters" : section_parameters  }

    steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
    cross_section = CrossSection(pipe_section_info=pipe_section_info)
    cross_section.update_properties()

    project = Project()
    model = Model(project)
    preprocessor = model.preprocessor
    geometry_path = Path("examples/iges_files/new_geometries/example_2_withBeam.iges")
    preprocessor.generate(geometry_path, 0.01)

    table_names = [None, None, None, None, None, None]
    preprocessor.set_prescribed_dofs([40, 1424, 1324], [np.zeros(6), table_names])

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


