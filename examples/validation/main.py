#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly_structural import AssemblyStructural 
from pulse.processing.solution_structural import SolutionStructural
from pulse.postprocessing.plot_structural_data import get_structural_frf, get_structural_response
from pulse.animation.plot_function import plot_results

''' 
    |=============================================================================|
    |  Please, it's necessary to copy and paste main.py script at OpenPulse file  |
    |  then type "python main.py" in the terminal to run the code !               |
    |=============================================================================| 
'''

# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
cross_section = CrossSection(0.05, 0.008)
mesh = Mesh()
# connect = mesh.connectivity_matrix
# coord = mesh.nodal_coordinates_matrix 

run = 2
if run==1:
    mesh.generate('examples/iges_files/tube_1.iges', 0.01)
    mesh.set_prescribed_dofs_bc_by_node([40, 1424, 1324], np.zeros(6))
if run==2:
    mesh.load_mesh('examples/mesh_files/Geometry_01/coord.dat', 'examples/mesh_files/Geometry_01/connect.dat')
    mesh.set_prescribed_dofs_bc_by_node([1, 1200, 1325], np.zeros(6))

mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)

# mesh.set_boundary_condition_by_node([361], np.array([0.1,None,None,None,None,None]))
mesh.set_load_bc_by_node([361], np.array([1,0,0,0,0,0]))

mesh.add_spring_to_node([427],1*np.array([1e9,1e9,1e9,0,0,0]))
mesh.add_mass_to_node([204],0*np.array([80,80,80,0,0,0]))
mesh.add_damper_to_node([342],0*np.array([1e3,1e3,1e3,0,0,0]))

# assemble = Assembly(mesh)
# K, M, Kr, Mr = assemble.get_global_matrices()

solu = SolutionStructural(mesh)
natural_frequencies, mode_shapes = solu.modal_analysis(modes=200, harmonic_analysis=True)

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
f_max = 200
df = 2
frequencies = np.arange(0, f_max+df, df)
modes = 200
direct = solu.direct_method(frequencies, is_viscous_lumped=True)
modal = solu.mode_superposition(frequencies, modes, fastest=True)

column = 85

ms_results = np.real(modal)

load_reactions = solu.get_reactions_at_fixed_nodes(frequencies, direct)
load_reactions = np.real(load_reactions)
_, coord_def, _, _ = get_structural_response(mesh, modal, column, Normalize=False)

plot_results( mesh,
              coord_def,
              scf = 0.5,
              out_OpenPulse = True, 
              Show_nodes = True, 
              Undeformed = False, 
              Deformed = False, 
              Animate_Mode = True, 
              Save = False)

#%%
# GETTING FRF
response_node = 361
local_DOF = 0
response_DM = get_structural_frf(mesh, direct, response_node, local_DOF)
response_MS = get_structural_frf(mesh, modal, response_node, local_DOF)

DOF_label = dict(zip(np.arange(6), ["Ux", "Uy", "Uz", "Rx", "Ry", "Rz"]))
Unit_label = dict(zip(np.arange(6), ["[m]", "[m]", "[m]", "[rad]", "[rad]", "[rad]"]))

# PLOTTING RESULTS
fig = plt.figure(figsize=[10,6])
ax = fig.add_subplot(1,1,1)

first_legend_label = "Direct"
second_legend_label = "Mode superposition"

if response_DM.all()==0 or response_MS.all()==0:
    first_plot, = plt.plot(frequencies, response_DM, color=[0,0,0], linewidth=3, label=first_legend_label)
    second_plot, = plt.plot(frequencies, response_MS, color=[1,0,0], linewidth=1, label=second_legend_label)
else:
    first_plot, = plt.semilogy(frequencies, response_DM, color=[0,0,0], linewidth=3, label=first_legend_label)    
    second_plot, = plt.semilogy(frequencies, response_MS, color=[1,0,0], linewidth=1, label=second_legend_label)

first_legend = plt.legend(handles=[first_plot, second_plot], loc='upper right')
plt.gca().add_artist(first_legend)

ax.set_title(("FRF - Response {} at node {}").format(DOF_label[local_DOF], response_node), fontsize = 18, fontweight = 'bold')
ax.set_xlabel(("Frequency [Hz]"), fontsize = 16, fontweight = 'bold')
ax.set_ylabel(("FRF's magnitude {}").format(Unit_label[local_DOF]), fontsize = 16, fontweight = 'bold')
plt.show()