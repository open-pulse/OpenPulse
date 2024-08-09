from pulse.model.cross_section import CrossSection
from pulse.properties.material import Material
from pulse.model.preprocessor import  Preprocessor
from pulse.processing.assembly_structural import get_global_matrices

# PREPARING MESH
steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
preprocessor = Preprocessor()
preprocessor.generate('tube_1.iges', 0.01)
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', cross_section)

# GETTING ALL MATRICES TOGETHER
K, M, Kr, Mr = get_global_matrices(preprocessor)