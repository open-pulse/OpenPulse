#%%
from time import time

import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly import get_global_matrices
from pulse.processing.solution import direct_method, modal_superposition, modal_analysis
from pulse.postprocessing.plot_data import get_frf, get_displacement_matrix


# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.034)
mesh = Mesh()

run = 2
if run==1:
    mesh.generate('examples/iges_files/tube_1.iges', 0.01)
    mesh.set_boundary_condition_by_node([1, 24, 26], np.zeros(6))
if run==2:
    mesh.load_mesh('coord.dat', 'connect.dat')
    mesh.set_boundary_condition_by_node([1, 1200, 1325], np.zeros(6))

mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)

# mesh.set_boundary_condition_by_node([361], np.array([0.001,None,None,None,None,None]))
mesh.set_force_by_node([361], np.array([1,0,0,0,0,0]))

mesh.add_spring_to_node([427],0*np.array([1e9,1e9,1e9,0,0,0]))
mesh.add_mass_to_node([204],0*np.array([80,80,80,0,0,0]))
mesh.add_damper_to_node([342],0*np.array([1e3,1e3,1e3,0,0,0]))

connect = mesh.get_connectivity_matrix(reordering=True)
coord = mesh.get_nodal_coordinates_matrix(reordering=True) 

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
f_max = 200
df = 2
frequencies = np.arange(0, f_max+df, df)
modes = 200
direct = direct_method(mesh, frequencies, is_viscous_lumped=True)
modal = modal_superposition(mesh, frequencies, modes)
natural_frequencies, mode_shapes = modal_analysis(mesh,modes=200)
column = 100
# _, data, r_res = get_displacement_matrix(mesh, direct, column, scf=0.4)

#%%
# GETTING FRF
node = 187
local_dof = 1
yd = get_frf(mesh, direct, node, local_dof)
ym = get_frf(mesh, modal, node, local_dof)

data = np.zeros((len(frequencies),2))
data[:,0] = frequencies
data[:,1] = yd
np.savetxt("FRF_newCode_RP_n436x_direct.dat",data)

data = np.zeros((len(frequencies),2))
data[:,0] = frequencies
data[:,1] = ym
np.savetxt("FRF_newCode_RP_n436x_modesup.dat",data)

# PLOTTING RESULTS
plt.semilogy(frequencies, yd)
plt.semilogy(frequencies, ym)
plt.show()



# %%
