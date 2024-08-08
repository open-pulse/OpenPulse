#%% 
import numpy as np
from time import time
import h5py
import pandas
# import queue
# from collections import deque

from pulse.engine.material import Material
from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection as TCS
from pulse.engine.preprocessing import PreProcessing
from pulse.engine.assembly import Assembly
from pulse.engine.solution import Solution
from pulse.engine.postprocessing import PostProcessing
from pulse.engine.savedata import SaveData
from pulse.engine.readdata import ReadData
from pulse.preprocessor import Preprocessor

from pulse.engine.plot_results import modeshape_plot as plot
import matplotlib.pylab as plt

t0 = time()

## Material definition:
# steel
elasticity_modulus = 210e9 # Young modulus [Pa]
poisson_ratio = 0.3   # Poisson ratio[-]
density = 7860  # Density[kg/m^3]
material_1 = Material('Steel', density, elasticity_modulus = elasticity_modulus, poisson_ratio = poisson_ratio)

## Cross section definition:
outer_diameter = 0.05   # Outer diameter [m]
thickness  = 0.008 # Thickness [m]
cross_section_1 = TCS(outer_diameter, thickness = thickness) 

# m = Preprocessor("C:\\Petro\\OpenPulse\\Examples\\geometry\\tube_1.iges")
# m.generate(0.01,0.01)
# # m.reorder_index_bfs()
# nodal_coordinates = np.array(m.nodes)
# connectivity  = np.array(m.edges, dtype=int)

## Nodal coordinates
nodal_coordinates = np.loadtxt('input_data/coord.dat')

## Connectivity
connectivity = np.loadtxt('input_data/connect.dat', dtype=int)

#TODO: determinate how those material, cross section properties and element type will come from preprocessor.
## Material atribuition for each element
material_list = [1, material_1]
material_dictionary = { i:material_list[1] for i in connectivity[:,0] }

## Cross section properties atribuition for each element
cross_section_list = [1, cross_section_1]
cross_section_dictionary = { i:cross_section_list[1] for i in connectivity[:,0] }

load_dictionary = {i:np.array([0, 0, 0, 0, 0, 0]) for i in connectivity[:,0]}

## Element type atribuition
element_type_dictionary = { i:'pipe16' for i in connectivity[:,0] }

##
### BEGIN OF NODAL/DOF INPUTS FOR PRESCRIBED DOFS, LOADS AND RESPONSE

# dofs prescribed (nodes, dof<=>values)
nodes_prescribed_dofs = [1, 1200, 1325] # Which node has some boundary coundition prescribed.
local_dofs_prescribed   = [[0,1,2],[0,1,2],[0,1,2]] # What are the degree of freedom restricted on those nodes.
# prescribed_dofs_values = [[0.01,0.01,0.01],[0.01,0.01,0.01],[0.01,0.01,0.01]] # prescribed values for each degree of freedom
prescribed_dofs_values = [[0,0,0],[0,0,0],[0,0,0]] # prescribed values for each degree of freedom

# external nodal load prescribed (nodes, dof<=>values)
nodes_prescribed_load = [27,230] # Which node has some nodal load prescribed.
local_dofs_prescribed_load  = [[1],[2]] # What are the local degree of freedom with external load.
prescribed_load_values      = [[1],[1]] # Whats are the prescribed values for external nodal load

# nodal response (node, dof_corrected)
nodes_response = [27] # Desired nodal response.
local_dofs_response  = [[1]] # Get the response at the following degree of freedom

### END OF NODAL/DOF INPUTS FOR PRESCRIBED DOFS, LOADS AND RESPONSE
##

# Preprocessing data:
preprocessor = PreProcessing(   nodal_coordinates, 
                                connectivity,
                                material_dictionary,
                                cross_section_dictionary,
                                load_dictionary,
                                element_type_dictionary,
                                nodes_prescribed_dofs,
                                local_dofs_prescribed,
                                prescribed_dofs_values,
                                nodes_prescribed_load,
                                local_dofs_prescribed_load,
                                prescribed_load_values,
                                nodes_response,
                                local_dofs_response )

## Assembly those informations.
assemble = Assembly( preprocessor )

# Global Assembly
K, M, F, Kr, Mr, data_K, data_M, data_F, I, J, I_f, global_dofs_free, global_dofs_presc, total_dof = assemble.global_matrices()

## Solution
# Analysis parameters
freq_max = 200
df = 2
number_modes = 100

load_dof = 157
response_dof = 157

F = np.zeros( total_dof - len(assemble.dofs_fixed()) )
F[load_dof] = 1

# Solution class definition

presc_dofs_info = preprocessor.prescbribed_dofs_info()
free_dofs = preprocessor.free_dofs()

solu = Solution(K, M, 
                Kr=Kr, Mr=Mr, presc_dofs_info = presc_dofs_info, free_dofs = free_dofs,
                minor_freq = 0, major_freq = freq_max, df = df, alpha_v = 0, beta_v = 0)
#%%
# Modal analysis
natural_frequencies, modal_shape = solu.modal_analysis( number_modes = number_modes, timing = True )
# print(natural_frequencies)

# Direct method
xd, frequencies = solu.direct_method(F, timing = True)

# Mode superposition method - Using the previous modal analysis output as input.
xs, frequencies, _ ,_ = solu.mode_superposition(F,
                                                number_modes=number_modes,
                                                natural_frequencies = natural_frequencies,
                                                modal_shape = modal_shape,
                                                timing = True)

# PostProcessing class definition
post = PostProcessing( preprocessor,
                       eigenVectors = modal_shape,
                       HA_output = xd, 
                       frequencies = frequencies,
                       Kr = Kr,
                       Mr = Mr,
                       free_dofs = free_dofs,
                       log = False )


R = np.real(post.load_reactions(xd))

eigenVectors_Uxyz, eigenVectors_Rxyz = post.dof_recover()

response_dof = preprocessor.response_info()[0,0].astype(int)
Xd = (post.harmonic_response(xd)[response_dof,:])
Xs = (post.harmonic_response(xs)[response_dof,:])

tf = time()
print('Total elapsed time:', (tf-t0),'[s]')

fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.semilogy(frequencies, np.abs(Xd), color = [0,0,0], linewidth=2)
plt.semilogy(frequencies, np.abs(Xs), color = [1,0,0], linewidth=2)
ax.set_title(('FRF: Direct and Mode Superposition Methods'), fontsize = 18, fontweight = 'bold')
ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
ax.set_ylabel(("FRF's magnitude [m/N]"), fontsize = 16, fontweight = 'bold')
ax.legend(['Direct - OpenPulse','Mode Superposition - OpenPulse'])
plt.show()

# Entries for plot function 
#Choose EigenVector to be ploted
mode_to_plot = 10

# u_def = post.plot_modal_shape(mode_to_plot)
u_def = post.plot_harmonic_response(20, xd)
connectivity_plot = preprocessor.connectivity_remaped()
coordinates = preprocessor.nodal_coordinates_remaped()

freq_n = natural_frequencies[mode_to_plot-1]
freq_n = None
#%%
# Choose the information to plot/animate
Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, False, False, True, False

# Amplitude scalling factor
scf=0.4

# Call function to plot nodal results [dynamic]
plot(coordinates, connectivity_plot, u_def, freq_n, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)

exit()

#%% Save important results using HDF5 format

# Defines wdata as an object of SaveData Class
wdata = SaveData( connectivity, 
                    nodal_coordinates,  
                    data_K, 
                    data_M, 
                    I, 
                    J,
                    global_dofs_free,
                    dofs_prescribed = global_dofs_presc,
                    eigenVectors = modal_shape,
                    eigenVectors_Uxyz = eigenVectors_Uxyz,
                    natural_frequencies = natural_frequencies, 
                    frequency_analysis = frequencies )

# Call store_data method to save the output results 
wdata.store_data()
#%%
# Defines rdata as an object of ReadData Class
rdata = ReadData()

# Call read_data method and return all variable saved in file
var_name, data, flag = rdata.read_data()
if flag:
    for i, name in enumerate(var_name):
        vars()[name[0]+"_"] = data[i]
