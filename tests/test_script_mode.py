import pytest
import numpy as np 
from pathlib import Path
from scipy.sparse import save_npz, load_npz

from pulse.utils.common_utils import sparse_is_equal
from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.model import Model
from pulse.model.preprocessor import Preprocessor
from pulse.project.project import Project
from pulse.processing.assembly_structural import AssemblyStructural 

# Setting up model
# @pytest.fixture
def model():

    project = Project()
    model = Model(project)

    mesh = model.mesh
    preprocessor = model.preprocessor

    # load geometry file
    geometry_path = Path("examples/iges_files/new_geometries/example_2_withBeam.iges")

    mesher_setup = {"element_size" : 0.01,
                    "geometry_tolerance" : 1e-6,
                    "length_unit" : "meter",
                    "import_type" : 0,
                    "geometry_path" : geometry_path}

    project.reset(reset_all=True)
    mesh.set_mesher_setup(mesher_setup=mesher_setup)

    # create the geometry
    preprocessor.generate()

    # section_parameters = [0.05, 0.008, 0, 0, 0, 0]
    # pipe_section_info = {  "section_type_label" : "Pipe" ,
    #                         "section_parameters" : section_parameters  }

    # steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
    # cross_section = CrossSection(pipe_section_info=pipe_section_info)
    # cross_section.update_properties()

    # table_names = [None, None, None, None, None, None]
    # preprocessor.set_prescribed_dofs([40, 1424, 1324], [np.zeros(6), table_names])

    # preprocessor.set_material_by_element('all', steel)
    # preprocessor.set_cross_section_by_element('all', cross_section)

    # frequencies = np.linspace(0, 200, 101)
    # assembly = AssemblyStructural(model, frequencies)

if __name__ == "__main__":
    model()