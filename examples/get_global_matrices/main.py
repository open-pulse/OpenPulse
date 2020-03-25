from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices

# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
mesh = Mesh()
mesh.generate('tube_1.iges', 0.01)
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)

# GETTING ALL MATRICES TOGETHER
K, M, Kr, Mr = get_global_matrices(mesh)
