from time import time

import numpy as np 
import matplotlib.pyplot as plt 

from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.preprocessor import  Preprocessor
from pulse.processing.assemblers.structural_assembler import StructuralAssembler
from pulse.processing.solvers.harmonic_solver import HarmonicSolver
from pulse.processing.solvers.modal_solver import ModalSolver
from pulse.postprocessing.plot_structural_data import get_structural_frf


# PREPARING MESH
steel = Material(name='Steel', identifier=1, density=7860, elasticity_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
preprocessor = Preprocessor()
preprocessor.load_mesh('coord.dat', 'connect.dat')
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', cross_section)
preprocessor.set_prescribed_dof([1, 1200, 1325], np.zeros(6))
preprocessor.set_structural_loads([361], np.array([1,0,0,0,0,0]))

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
frequencies = np.arange(0, 202, 2)
modes = 200
assembler = StructuralAssembler(preprocessor)
direct_solver = HarmonicSolver(assembler)
direct_solver.direct_method(frequencies)
direct = direct_solver.solution
modal_solver = HarmonicSolver(assembler)
modal_solver.mode_superposition(frequencies, n_modes=modes)
modal = modal_solver.solution

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

