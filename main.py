#%% 
import numpy as np
import time
import h5py
import queue
from collections import deque

from pulse.engine.material import Material
from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection as TCS
from pulse.engine.element_288 import Element
from pulse.engine.assembly import Assembly
from pulse.engine.solution import Solution
from pulse.engine.postprocessing import PostProcessing
from pulse.engine.savedata import SaveData
from pulse.engine.readdata import ReadData
from pulse.mesh import Mesh


from pulse.engine.plot_results import modeshape_plot as plot
import matplotlib.pylab as plt

## Material definition:
# steel
young_modulus = 210e9 # Young modulus [Pa]
poisson_ratio = 0.3   # Poisson ratio[-]
density = 7860  # Density[kg/m^3]
material_1 = Material('Steel', density, young_modulus = young_modulus, poisson_ratio = poisson_ratio)

## Cross section definition:
D_external = 0.05   # External diameter [m]
thickness  = 0.008 # Thickness [m]
cross_section_1 = TCS(D_external, thickness = thickness) 



# m = Mesh("C:\\Petro\\OpenPulse\\Examples\\geometry\\tube_1.iges")
# m.generate(0.01,0.01)
# m.reorder_index_bfs()
# nodal_coordinates = np.array(m.nodes)
# connectivity  = np.array(m.edges, dtype=int)


## Nodal coordinates
nodal_coordinates = np.loadtxt('input_data/coord.dat') 

## Connectivity
connectivity = np.loadtxt('input_data/connect.dat', dtype=int)

## Boundary conditions
#TODO: save the rows and collumns deleted.
fixed_nodes = np.array([1, 1200, 1325]) # Which node has some boundary coundition prescribed.
dofs_fixed_node = [[5,3,2,0,4,1],[0,1,2,3,4,5],[0,1,2,3,4,5]] # What are the degree of freedom restricted on those nodes.
dofs_fixed_value = [[0,1,2,3,4,5],[5,4,3,2,1,0],[7,6,5,4,3,2]] # Value prescribed for each degree of freedom

#TODO: determinate how those material, cross section properties and element type will come from mesh.
## Material atribuition for each element
material_list = [1, material_1]
material_dictionary = { i:material_list[1] for i in connectivity[:,0] }

## Cross section properties atribuition for each element
cross_section_list = [1, cross_section_1]
cross_section_dictionary = { i:cross_section_list[1] for i in connectivity[:,0] }

## Element type atribuition
element_type_dictionary = { i:'pipe16' for i in connectivity[:,0] }

## Assembly those informations.
assemble = Assembly(nodal_coordinates,
                    connectivity,
                    fixed_nodes,
                    dofs_fixed_node,
                    dofs_fixed_value,                
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary)

# Global Assembly
start = time.time()
K, M, Kr, Mr, data_K, data_M, I, J, global_dofs_free, global_dofs_presc, total_dof = assemble.global_matrices()
end = time.time()
print('Time to assemble global matrices:' + str(round((end - start),6)) + '[s]')

# plt.spy(K.toarray())

## Solution
# Analysis parameters
freq_max = 200
df = 2
<<<<<<< HEAD
number_modes = 1000
=======
number_modes = 100
>>>>>>> ada818c148bff5a4eda0e7c3988a745fa4bdc03f

load_dof = 157
response_dof = 157

F = np.zeros( total_dof - len(assemble.dofs_fixed()) )
F[load_dof] = 1

# Solution class definition
solu = Solution(K, M, minor_freq = 0, major_freq = freq_max, df = df, alpha_v = 0, beta_v = 0)

# Modal analysis
natural_frequencies, modal_shape = solu.modal_analysis( number_modes = number_modes, timing = True )

# Direct method
xd, frequencies = solu.direct_method(F, timing = True)

# Mode superposition method - Using the previous modal analysis output as input.
xs, frequencies, _ ,_ = solu.mode_superposition(F,
                                                number_modes=number_modes,
                                                natural_frequencies = natural_frequencies,
                                                modal_shape = modal_shape,
                                                timing = True)

# PostProcessing class definition
post = PostProcessing( fixed_nodes = fixed_nodes, 
                      presc_dofs = assemble.dofs_fixed(), 
                      value_prescribed_dofs = assemble.dofs_prescribed_values(),
                      nodal_coordinates = nodal_coordinates, 
                      eigenVectors = modal_shape, 
                      HA_output = xd,
                      log = False )

eigenVectors_Uxyz, eigenVectors_Rxyz, U_out = post.dof_recover()
# exit()
fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.plot(frequencies, np.log10(np.abs(xd[response_dof,:])), color = [0,0,0], linewidth=2)
plt.plot(frequencies, np.log10(np.abs(xs[response_dof,:])), color = [1,0,0], linewidth=2)
ax.set_title(('FRF: Direct and Mode Superposition Methods'), fontsize = 18, fontweight = 'bold')
ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
ax.set_ylabel(("FRF's magnitude [m/N]"), fontsize = 16, fontweight = 'bold')
ax.legend(['Direct - OpenPulse','Mode Superposition - OpenPulse'])
plt.show()

exit()

#%% Entries for plot function 

#Choose EigenVector to be ploted
mode_to_plot = 100

u_def = post.plot_modal_shape(mode_to_plot)[:,1:]
connectivity_plot = connectivity[:,1:]
coordinates = nodal_coordinates[:,1:]

freq_n = natural_frequencies[mode_to_plot-1]

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
                    frequency_analysis = frequencies,
                    U_out = U_out )

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



