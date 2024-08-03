from time import time

import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.preprocessor import  Preprocessor
from pulse.processing.structural_solver import StructuralSolver
from pulse.postprocessing.plot_structural_data import get_structural_frf


# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
preprocessor = Preprocessor()
preprocessor.load_mesh('coord.dat', 'connect.dat')
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', cross_section)
preprocessor.set_prescribed_dofs_bc_by_node([1, 1200, 1325], np.zeros(6))
preprocessor.set_structural_load_bc_by_node([361], np.array([1,0,0,0,0,0]))

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
frequencies = np.arange(0, 202, 2)
modes = 200
solution = StructuralSolver(preprocessor)
direct = solution.direct_method(frequencies)
modal = solution.mode_superposition(frequencies, modes)

# GETTING FRF
node = 711
local_dof = 2
x = frequencies
yd = get_frf(preprocessor, direct, node, local_dof)
ym = get_frf(preprocessor, modal, node, local_dof)

# PLOTTING RESULTS
plt.semilogy(x, yd)
plt.semilogy(x, ym)
plt.show()

