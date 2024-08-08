from pulse.preprocessing.cross_section import CrossSection
from pulse.properties.material import Material
from pulse.preprocessing.preprocessor import  Preprocessor
from pulse.processing.assembly_structural import get_global_matrices

# create materials
steel = Material('Steel', density=7860, elasticity_modulus=210e9, poisson_ratio=0.3)
alloy_steel = Material('AISI4140', density=7850, elasticity_modulus=203200000000, poisson_ratio=0.27)

# create cross sections
large_tube = CrossSection(0.05, 0.034)
thin_tube = CrossSection(0.01, 0.005)

# create preprocessor
preprocessor = Preprocessor()

# define mesh file and element size
preprocessor.generate('tube_2.iges', 0.01)

# set properties to all elements
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', large_tube)

# set properties for specific lines
preprocessor.set_cross_section_by_lines([37, 38, 39], thin_tube)
preprocessor.set_material_by_lines([37, 38, 39], alloy_steel)