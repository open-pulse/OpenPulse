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

t0 = time()
# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
offset = [0.005, 0.005]
cross_section = CrossSection(0.05, 0.008, offset_y = offset[0], offset_z = offset[1])
mesh = Mesh()

run = 2
if run==1:
    mesh.generate('examples/iges_files/tube_1.iges', 0.01)
    mesh.set_prescribed_dofs_bc_by_node([40, 1424, 1324], np.zeros(6))
if run==2:
    mesh.load_mesh('examples/mesh_files/Geometry_01/coord.dat', 'examples/mesh_files/Geometry_01/connect.dat')
    mesh.set_prescribed_dofs_bc_by_node([1, 1200, 1325], np.zeros(6))

mesh.set_element_type('pipe_1')
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)
dt = time()-t0
print('Total elapsed time:', dt,'[s]')

mesh.set_structural_load_bc_by_node([361], np.array([1,0,0,0,0,0]))

solution = SolutionStructural(mesh)
f_max = 200
df = 2
frequencies = np.arange(0, f_max+df, df)
modes = 200
direct = solution.direct_method(frequencies, is_viscous_lumped=True)
modal = solution.mode_superposition(frequencies, modes, fastest=True)


run=2

if run==1:
    # nodal respose (node, dof_corrected)
    nodes_response = 436 # Desired nodal to get response.
    local_dofs_response  = 0 # Get the response at the following degree of freedom
if run==2:
     # nodal respose (node, dof_corrected)
    nodes_response = 187 # Desired nodal to get response.
    local_dofs_response  = 1 # Get the response at the following degree of freedom
if run==3:
     # nodal respose (node, dof_corrected)
    nodes_response = 711 # Desired nodal to get response.
    local_dofs_response  = 2 # Get the response at the following degree of freedom

response_dof = (nodes_response - 1) *  6 + local_dofs_response
Xd = direct[response_dof,:]
Xs = modal[response_dof,:]

test_label = "ey_{}mm_ez_{}mm".format(int(offset[0]*1000),int(offset[1]*1000))

if run==1:
    file1 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_Ux_node_436.csv", "r")
    FRF = np.loadtxt(file1, delimiter=",", skiprows=2)
    file1.close()
elif run==2:
    file2 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_Uy_node_187.csv", "r")
    FRF = np.loadtxt(file2, delimiter=",", skiprows=2)
    file2.close()
elif run==3:
    file3 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_Uz_node_711.csv", "r")
    FRF = np.loadtxt(file3, delimiter=",", skiprows=2)
    file3.close()
else:
    print("Invalid run number entry!")

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