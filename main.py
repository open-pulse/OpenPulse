#%% 
import numpy as np
import time
import h5py
import queue
from collections import deque

from pulse.engine.material import Material
from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection as TCS
from pulse.engine.element import Element
from pulse.engine.assembly import Assembly
from pulse.engine.solution import Solution
from pulse.engine.postprocessing import PostProcessing
from pulse.engine.savedata import SaveData

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

## Nodal coordinates
nodal_coordinates = np.loadtxt('Input/coord.dat') 

## Connectivity
connectivity = np.loadtxt('Input/connect.dat', dtype=int)

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
K, M, Kr, Mr, data_K, data_M, I, J, global_dofs_not_presc, global_dofs_presc, total_dof = assemble.global_matrices()
end = time.time()
print('Time to assemble global matrices:' + str(round((end - start),6)) + '[s]')

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
solu = Solution(K, M, minor_freq = 0, major_freq = freq_max, df = df, alpha = 0, beta = 1e-4)

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

#%

post = PostProcessing( fixed_nodes = fixed_nodes, presc_dofs = assemble.dofs_fixed(), value_prescribed_dofs = assemble.dofs_prescribed_values(), eigenVectors = modal_shape, HA_output = xd, nodal_coordinates = nodal_coordinates )

# eigenVectors_Uxyz, eigenVectors_Rxyz, U_out = post.dof_recover()

fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.plot(frequencies, np.log10(np.abs(xd[response_dof,:])))
plt.plot(frequencies, np.log10(np.abs(xs[response_dof,:])))
ax.legend(['Direct - OpenPulse','Superposition - OpenPulse'])
plt.show()

# exit()

#%% Entries for plot function 

#Choose EigenVector to be ploted
mode_to_plot = 3

u_def = post.plot_modal_shape(mode_to_plot)[:,1:]

connectivity_plot = connectivity[:,1:]
coordinates = nodal_coordinates[:,1:]
# u_def = results(mode_to_plot)[:,1:]
freq_n = natural_frequencies[mode_to_plot-1]

# Choose the information to plot/animate
Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, False, False, True, False

# Amplitude scalling factor
scf=0.4

# Call function to plot nodal results [dynamic]
plot(coordinates, connectivity_plot, u_def, freq_n, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)

exit()


#%% Save important results using HDF5 format

save_results = False

save = SaveData(save_results, data_K, data_M, I, J, connectivity, nodal_coordinates, dofs_not_presc = dofs_not_presc, dofs_presc = dofs_presc  )

if save_results:
    
  # np.savetxt('M_globalmatrix.txt',M.toarray(),fmt='%.18e')
  # np.savetxt('K_globalmatrix.txt',K.toarray(),fmt='%.18e')

  f = h5py.File('new_output_data.hdf5', 'w')
  f.create_dataset('/input/nodal_coordinates', data = nodal_coordinates, dtype='float64')
  f.create_dataset('/input/connectivity', data = connectivity, dtype='int')
  f.create_dataset('/global_matrices/I', data = I, dtype='int')
  f.create_dataset('/global_matrices/J', data = J, dtype='int')
  f.create_dataset('/global_matrices/data_K', data = data_K, dtype='float64')
  f.create_dataset('/global_matrices/data_M', data = data_M, dtype='float64')
  f.create_dataset('/results/eigenVectors', data = eigenVectors, dtype='float64')
  f.create_dataset('/results/natural_frequencies', data = fn, dtype='float64')
  f.close()

# Example how to read files in HDF5 format

f = h5py.File('output_data.hdf5', 'r')
list(f.keys())
K = f.get('/global_matrices/coo_K').value
f.close()


f = h5py.File('new_output_data.hdf5', 'r')
list(f.keys())
K_new = f.get('/global_matrices/coo_K').value
f.close()

