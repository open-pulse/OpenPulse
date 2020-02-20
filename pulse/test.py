# from pulse.engine.element_288 import Element as oldElement
# from pulse.engine.node import Node as oldNode
# from pulse.engine.material import Material as oldMaterial
# from pulse.engine.tube import TubeCrossSection as oldCrossSection

# from pulse.geometry.element import Element as newElement
# from pulse.geometry.node import Node as newNode
# from pulse.setup.material import Material as newMaterial
# from pulse.setup.cross_section import CrossSection as newCrossSection


# ofs = oldNode(1,1,1, 9)
# oln = oldNode(2,2,2, 9)
# om = oldMaterial('s', density=7860, young_modulus=210e9, poisson_ratio=0.3)
# ocs = oldCrossSection(D_external=0.05, D_internal=0.038)
# oe = oldElement(ofs, oln, om, ocs, '', '')

# nfn = newNode(1,1,1)
# nln = newNode(2,2,2)
# nm = newMaterial('s', density=7860, young_modulus=210e9, poisson_ratio=0.3)
# ncs = newCrossSection(external_diameter=0.05, internal_diameter=0.038)
# ne = newElement(first_node=nfn, last_node=nln, material=nm, cross_section=ncs)

# Ko = oe.stiffness_matrix_gcs()
# Kn = ne.stiffness_matrix_gcs()

# Mo = oe.mass_matrix_gcs()
# Mn = ne.mass_matrix_gcs()

# print((Ko == Kn).all())
# print((Mo == Mn).all())

#######################

from pulse.setup.cross_section import CrossSection
from pulse.setup.material import Material
from pulse.geometry.mesh import Mesh
from pulse.solver.assembly import get_global_matrices


steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)

mesh = Mesh()
mesh.generate('Examples\\geometry\\tube_1.iges', 0.01)
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)

# K, M, Kr, Mr = get_global_matrices(mesh)

#############################

# from pulse.geometry.mesh import Mesh
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt

# mesh = Mesh()
# mesh.generate('Examples\\geometry\\tube_1.iges', 0.01)

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# x = [node.x for node in mesh.nodes.values()]
# y = [node.y for node in mesh.nodes.values()]
# z = [node.z for node in mesh.nodes.values()]
# ax.scatter(x, y, z)

# for element in mesh.elements.values():
#     x = [element.first_node.x, element.last_node.x]
#     y = [element.first_node.y, element.last_node.y]
#     z = [element.first_node.z, element.last_node.z]
#     ax.plot(x,y,z)

# plt.show()