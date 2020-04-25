#%% 
import numpy as np
from time import time
import h5py

from pulse.engine.material import Material
from pulse.engine.node import Node
from pulse.engine.preprocessing import PreProcessing
from pulse.engine.assembly import Assembly
from pulse.engine.solution import Solution
from pulse.engine.postprocessing import PostProcessing
from pulse.engine.savedata import SaveData
from pulse.engine.readdata import ReadData
from pulse.mesh import Mesh
from pulse.engine.section_fem import TubeCrossSection as TCS

from pulse.engine.plot_results import modeshape_plot as plot
import matplotlib.pylab as plt

t0 = time()

## Nodal coordinates
nodal_coordinates = np.loadtxt('input_data/coord.dat')

## Connectivity
connectivity = np.loadtxt('input_data/connect.dat', dtype=int)

## Material definition:
young_modulus = 210e9 # Young modulus [Pa]
poisson_ratio = 0.3   # Poisson ratio[-]
density = 7860  # Density[kg/m^3]
material_1 = Material('Steel', density, young_modulus = young_modulus, poisson_ratio = poisson_ratio)

## Cross section definition:
D_external = 0.05   # External diameter [m]
thickness  = 0.008 # Thickness [m]
division_number = 64 
offset = [0.005, 0.005] # Offsets: (ey, ez) [m]

## Element type selection: 
# Enter 1 for Element288a
# Enter 2 for Element288b
# Enter 3 for Element288c

Element_type_selector = 3

if Element_type_selector==1:
    from pulse.engine.element_288a import Element
    cross_section = TCS(D_external, thickness = thickness, element_type = '288a')
    cross_section_properties = cross_section
    element_type_dictionary = { i:'288a' for i in connectivity[:,0] }

if Element_type_selector==2:
    from pulse.engine.element_288b import Element
    cross_section = TCS(D_external, division_number = division_number , offset = offset , thickness = thickness, element_type = '288b')
    cross_section_properties = cross_section.all_props()
    element_type_dictionary = { i:'288b' for i in connectivity[:,0] }

if Element_type_selector==3:
    from pulse.engine.element_288c import Element
    cross_section = TCS(D_external, division_number = division_number , offset = offset , thickness = thickness, element_type = '288c')
    cross_section_properties = cross_section.all_props()
    element_type_dictionary = { i:'288c' for i in connectivity[:,0] }
   
## Cross section properties atribuition for each element
cross_section_list = [1, cross_section_properties]
cross_section_dictionary = { i:cross_section_list[1] for i in connectivity[:,0] }

#TODO: determinate how those material, cross section properties and element type will come from mesh.
## Material atribuition for each element
material_list = [1, material_1]
material_dictionary = { i:material_list[1] for i in connectivity[:,0] }

# distributed load over element
load_dictionary = {i:np.array([0, 0, 0, 0, 0, 0]) for i in connectivity[:,0]}

#
##
### BEGIN OF NODAL/DOF INPUTS FOR PRESCRIBED DOFS, LOADS AND RESPONSE
# Note: all entries refer to the global coordinate system

# dofs prescribed (nodes, dof<=>values)
nodes_prescribed_dofs = [1, 1200, 1325] # Which node has some boundary coundition prescribed.
local_dofs_prescribed  = [[0,1,2,3,4,5],[0,1,2,3,4,5],[0,1,2,3,4,5]] # What are the degree of freedom restricted on those nodes.
prescribed_dofs_values = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]] # prescribed values for each degree of freedom

# external nodal load prescribed (nodes, dof<=>values)
nodes_prescribed_load = [361] # Which node has some nodal load prescribed.
local_dofs_prescribed_load  = [[0]]# What are the local degree of freedom with external load.
prescribed_load_values      = [[1]] # Whats are the prescribed values for external nodal load

run=1

if run==1:
    # nodal respose (node, dof_corrected)
    nodes_response = [436] # Desired nodal to get response.
    local_dofs_response  = [[0]] # Get the response at the following degree of freedom
if run==2:
     # nodal respose (node, dof_corrected)
    nodes_response = [187] # Desired nodal to get response.
    local_dofs_response  = [[1]] # Get the response at the following degree of freedom
if run==3:
     # nodal respose (node, dof_corrected)
    nodes_response = [711] # Desired nodal to get response.
    local_dofs_response  = [[2]] # Get the response at the following degree of freedom


### END OF NODAL/DOF INPUTS FOR PRESCRIBED DOFS, LOADS AND RESPONSE
##

## 
### ENTRIES FOR LUMPED PARAMETERS
## LUMPED STIFFNESS
nodes_lumped_stiffness = [427]
local_lumped_stiffness = [[0,1,2]]
lumped_stiffness_values = [[1e9*0,1e9*0,1e9*0]]

## LUMPED MASS
nodes_lumped_mass = [204]
local_lumped_mass = [[0,1,2]]
lumped_mass_values = [[1000*0,1000*0,1000*0]]

## LUMPED DAMPING
# proportional hysteretic and viscous
alpha_h_lumped = 0 # hysteretic constant of mass matrix
beta_h_lumped = 0 # hysteretic constant of stiffenss matrix
alpha_v_lumped = 0 # viscous constant of mass matrix
beta_v_lumped = 0 # viscous constant of stiffenss matrix
lumped_damping = [alpha_h_lumped, beta_h_lumped, alpha_v_lumped, beta_v_lumped]

# viscous non-proportional model 
nodes_lumped_damping = [427]
local_lumped_damping = [[0,1,2]]
lumped_damping_values = [[1000*0,1000*0,1000*0]]
###
##

# SET ANALYSIS PARAMETERS FOR MODAL ANALYSIS AND HARMONIC ANALYSIS
number_modes = 200
freq_max = 200
df = 2

# Preprocessing data:
preprocessor = PreProcessing(   nodal_coordinates, 
                                connectivity,
                                material_dictionary,
                                cross_section_dictionary,
                                load_dictionary,
                                Element,
                                element_type_dictionary,
                                nodes_prescribed_dofs = nodes_prescribed_dofs,
                                local_dofs_prescribed = local_dofs_prescribed,
                                prescribed_dofs_values = prescribed_dofs_values,
                                nodes_prescribed_load = nodes_prescribed_load,
                                local_dofs_prescribed_load = local_dofs_prescribed_load,
                                prescribed_load_values = prescribed_load_values,
                                nodes_response = nodes_response,
                                local_dofs_response = local_dofs_response,
                                nodes_lumped_stiffness = nodes_lumped_stiffness,
                                local_lumped_stiffness = local_lumped_stiffness,
                                lumped_stiffness_values = lumped_stiffness_values,
                                nodes_lumped_mass = nodes_lumped_mass,
                                local_lumped_mass = local_lumped_mass,
                                lumped_mass_values = lumped_mass_values,
                                nodes_lumped_damping = nodes_lumped_damping,
                                local_lumped_damping = local_lumped_damping,
                                lumped_damping_values = lumped_damping_values
                                )
#%%
## Call Assembly class.
assemble = Assembly( preprocessor, Element )

# Entries for Solution class definition
damping = [0, 0, 0, 0] # [alpha_h, beta_h, alpha_v, beta_v]
solu = Solution( assemble, 
                minor_freq = 0, major_freq = freq_max, df = df, damping=damping, lumped_damping=lumped_damping)

# Modal analysis
natural_frequencies, modal_shape = solu.modal_analysis( number_modes = number_modes, timing = True )
# print(natural_frequencies)

# Direct method
xd, frequencies = solu.direct_method(timing = True, viscous_damping_lumped = True)

# Mode superposition method - Using the previous modal analysis output as input.
xs, frequencies, _ ,_ = solu.mode_superposition( number_modes = number_modes,
                                                 natural_frequencies = natural_frequencies,
                                                 modal_shape = modal_shape,
                                                 timing = True )

# PostProcessing class definition
post = PostProcessing( assemble,
                       eigenVectors = modal_shape,
                       HA_output = xd, 
                       frequencies = frequencies,
                       free_dofs = preprocessor.free_dofs,
                       damping = damping,
                       log = False )

R = np.real(post.load_reactions(xd))
# np.savetxt("OpenPulse_Reactions.dat", R)
response_dof = preprocessor.response_info()[0,0].astype(int)
Xd = (post.harmonic_response(xd)[response_dof,:])
Xs = (post.harmonic_response(xs)[response_dof,:])

tf = time()
print('Total elapsed time:', (tf-t0),'[s]')

test_label = "ey_{}mm_ez_{}mm".format(int(offset[0]*1000),int(offset[1]*1000))

#TODO DO NOT DELETE THESE LINES
## FRFs obtained through Ansys (Harmonic Response - Full)
file1 = open("Examples/Validation/Element288c/" + test_label + "/FRF_Fx_1N_Ux_node_436.csv", "r")
file2 = open("Examples/Validation/Element288c/" + test_label + "/FRF_Fx_1N_Uy_node_187.csv", "r")
file3 = open("Examples/Validation/Element288c/" + test_label + "/FRF_Fx_1N_Uz_node_711.csv", "r")
FRF_Ux = np.loadtxt(file1, delimiter=",", skiprows=2)
FRF_Uy = np.loadtxt(file2, delimiter=",", skiprows=2)
FRF_Uz = np.loadtxt(file3, delimiter=",", skiprows=2)
file1.close()
file2.close()
file3.close()

if run==1:
    FRF = FRF_Ux
elif run==2:
    FRF = FRF_Uy
elif run==3:
    FRF = FRF_Uz
else:
    print("Invalid run number entry!")
#%%
fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.semilogy(frequencies, np.abs(Xd), color = [0,0,0], linewidth=3)
plt.semilogy(frequencies, np.abs(Xs), color = [1,0,0], linewidth=1.5)
plt.semilogy(FRF[:,0], np.abs(FRF[:,1] + 1j*FRF[:,2]), color = [0,0,1], linewidth=1)
ax.set_title(('FRF: Direct and Mode Superposition Methods'), fontsize = 18, fontweight = 'bold')
ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
ax.set_ylabel(("FRF's magnitude [m]"), fontsize = 16, fontweight = 'bold')
plt.legend(['Direct - OpenPulse','Mode Superposition - OpenPulse', 'Direct - Ansys'], loc="best")
plt.show()
#%%
exit()
# Entries for plot function 
#Choose EigenVector to be ploted
mode_to_plot = 31

# u_def = post.plot_modal_shape(mode_to_plot)
u_def = post.plot_harmonic_response(20, xd)
connectivity_plot = preprocessor.connectivity_remaped()
coordinates = preprocessor.nodal_coordinates_remaped()

freq_n = natural_frequencies[mode_to_plot-1]
freq_n = None

# Choose the information to plot/animate
Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, False, False, True, False

# Amplitude scalling factor
scf=0.4

# Call function to plot nodal results [dynamic]
plot(coordinates, connectivity_plot, u_def, freq_n, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)

exit()

# #%% Save important results using HDF5 format

# data_K, data_M, data_F, I, J, I_f, global_dofs_free, global_dofs_presc, total_dofs = assemble.matrices_data_to_save()
# eigenVectors_Uxyz, eigenVectors_Rxyz = post.dof_recover()

# # Defines wdata as an object of SaveData Class
# wdata = SaveData( connectivity, 
#                     nodal_coordinates,  
#                     data_K, 
#                     data_M, 
#                     I, 
#                     J,
#                     I_f,
#                     global_dofs_free,
#                     dofs_prescribed = global_dofs_presc,
#                     eigenVectors = modal_shape,
#                     eigenVectors_Uxyz = eigenVectors_Uxyz,
#                     natural_frequencies = natural_frequencies, 
#                     frequency_analysis = frequencies )

# # Call store_data method to save the output results 
# wdata.store_data()
# #%%
# # Defines rdata as an object of ReadData Class
# rdata = ReadData()

# # Call read_data method and return all variable saved in file
# var_name, data, flag = rdata.read_data()
# if flag:
#     for i, name in enumerate(var_name):
#         vars()[name[0]+"_"] = data[i]