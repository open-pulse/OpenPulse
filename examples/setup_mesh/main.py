from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices

# create materials
steel = Material('Steel', density=7860, young_modulus=210e9, poisson_ratio=0.3)
alloy_steel = Material('AISI4140', density=7850, young_modulus=203200000000, poisson_ratio=0.27)

# create cross sections
large_tube = CrossSection(0.05, 0.034)
thin_tube = CrossSection(0.01, 0.005)

# create mesh
mesh = Mesh()

# define mesh file and element size
mesh.generate('tube_2.iges', 0.01)

# set properties to all elements
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', large_tube)

# set properties for specific lines
mesh.set_cross_section_by_line([37, 38, 39], thin_tube)
mesh.set_material_by_line([37, 38, 39], alloy_steel)