#%% 
import numpy as np
import time
import h5py

from pulse.engine.material import Material
from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection as TCS
from pulse.engine.element import Element
from pulse.engine.assembly import Assembly
from pulse.engine.solution import Solution

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
dofs_fixed_node = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]] # What are the degree of freedom restricted on those nodes.

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
                    material_list,
                    material_dictionary,
                    cross_section_list,
                    cross_section_dictionary,
                    element_type_dictionary)

# Global Assembly
start = time.time()
K, M, Kb, Mb, total_dof, Ib, Jb = assemble.global_matrices()
end = time.time()
print('Time to assemble global matrices:' + str(round((end - start),6)) + '[s]')

## Solution
# Analysis parameters
freq_max = 50
df = 1
number_modes = 20

load_dof = 157
response_dof = 157

F = np.zeros( total_dof )
F[load_dof] = 1

# Solution class definition
solu = Solution(K, M, minor_freq = 0, major_freq = freq_max, df = df)

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

fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.plot(frequencies, np.log10(np.abs(xd[response_dof,:])))
plt.plot(frequencies, np.log10(np.abs(xs[response_dof,:])))
ax.legend(['Direct - OpenPulse','Superposition - OpenPulse'])
plt.show()

#%% Rebuild of EigenVectors adding fixed DOFs information (all DOFs fixed)

def results(mode_to_plot):

  u_xyz = np.zeros((nodal_coordinates.shape[0]-fixed_nodes.shape[0],1+3))
  ind_u = np.arange(0,modal_shape.shape[0],6)

  u_xyz[:,1] = modal_shape[ind_u  ,mode_to_plot-1]
  u_xyz[:,2] = modal_shape[ind_u+1,mode_to_plot-1]
  u_xyz[:,3] = modal_shape[ind_u+2,mode_to_plot-1]

  for i in fixed_nodes:
    u_xyz = np.insert(u_xyz,i-1,[0],axis=0)

  u_xyz[:,0] = np.arange(1,nodal_coordinates.shape[0]+1,1)

  return u_xyz

#% Entries for plot function 

#Choose EigenVector to be ploted
mode_to_plot = 24

connectivity_plot = connectivity[:,1:]
coordinates = nodal_coordinates[:,1:]
u_def = results(mode_to_plot)[:,1:]
freq_n = frequencies[mode_to_plot-1]

# Choose the information to plot/animate
Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, False, False, True, False

# Amplitude scalling factor
scf=0.4

# Call function to plot nodal results [dynamic]
plot(coordinates, connectivity_plot, u_def, freq_n, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)

#%% Save important results using HDF5 format

save_results = False

if save_results:
    
  # np.savetxt('M_globalmatrix.txt',M.toarray(),fmt='%.18e')
  # np.savetxt('K_globalmatrix.txt',K.toarray(),fmt='%.18e')

  f = h5py.File('output_data.hdf5', 'w')
  f.create_dataset('/input/nodal_coordinates', data = nodal_coordinates, dtype='float64')
  f.create_dataset('/input/connectivity', data = connectivity, dtype='int')
  f.create_dataset('/global_matrices/I', data = I, dtype='int')
  f.create_dataset('/global_matrices/J', data = J, dtype='int')
  f.create_dataset('/global_matrices/coo_K', data = coo_K, dtype='float64')
  f.create_dataset('/global_matrices/coo_M', data = coo_M, dtype='float64')
  f.create_dataset('/results/eigenVectors', data = eigenVectors, dtype='float64')
  f.create_dataset('/results/natural_frequencies', data = fn, dtype='float64')
  f.close()

## Example how to read files in HDF5 format

# f = h5py.File('output_data.hdf5', 'r')
# list(f.keys())
# K = f['/global_matrices/coo_K']
# # f.close()
