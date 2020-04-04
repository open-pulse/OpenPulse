from time import time

import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices
from pulse.processing.solution import direct_method, modal_superposition
from pulse.postprocessing.plot_data import get_frf


# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
mesh = Mesh()
mesh.load_mesh('coord.dat', 'connect.dat')
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)
mesh.set_boundary_condition_by_node([1, 1200, 1325], np.zeros(6))
mesh.set_force_by_node([361, 230], np.array([1,0,0,0,0,0]))

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
frequencies = np.arange(0, 201, 2)
modes = 200
direct = direct_method(mesh, frequencies)
modal = modal_superposition(mesh, frequencies, modes)

# GETTING FRF
node = 27
local_dof = 3
x = frequencies
yd = get_frf(mesh, direct, node, local_dof)
ym = get_frf(mesh, modal, node, local_dof)

# PLOTTING RESULTS
plt.semilogy(x, yd)
plt.semilogy(x, ym)
plt.show()

