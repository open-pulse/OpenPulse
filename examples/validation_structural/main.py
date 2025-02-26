#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.model.cross_section import CrossSection
from pulse.properties.material import Material
from pulse.model.preprocessor import Preprocessor
from pulse.processing.assembly_structural import AssemblyStructural 
from pulse.processing.structural_solver import StructuralSolver
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
element_type = 'beam_1'
steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
preprocessor = Preprocessor()

load_file = 1
if load_file==1:
    preprocessor.generate('examples/iges_files/tube_1.iges', 0.01)
    preprocessor.set_prescribed_dofs([40, 1424, 1324], np.zeros(6, dtype=complex))
    preprocessor.set_structural_loads([359], np.array([1,0,0,0,0,0], dtype=complex))
if load_file==2:
    preprocessor.load_mesh('examples/mesh_files/Geometry_01/coord.dat', 'examples/mesh_files/Geometry_01/connect.dat')
    preprocessor.set_prescribed_dofs([1, 1200, 1325], np.zeros(6, dtype=complex))
    preprocessor.set_structural_loads([361], np.array([1,0,0,0,0,0], dtype=complex))

mat_out = preprocessor.set_B2P_rotation_decoupling(1316, 425, rotations_to_decouple=[True, True, False])

preprocessor.set_structural_element_type_by_element('all', element_type)
preprocessor.set_material_by_element('all', steel)


d_out = 0.05
d_in = 0.034
area = np.pi*((d_out**2)-(d_in**2))/4
Iyy =  np.pi*((d_out**4)-(d_in**4))/64
Izz = np.pi*((d_out**4)-(d_in**4))/64
Iyz = 0

section_info = ["generic_beam", None]

cross_section = CrossSection(d_out, 0, 0, 0, steel.poisson_ratio, element_type=element_type, area=area, Iyy=Iyy, Izz=Izz, Iyz=Iyz, additional_section_info=section_info) 

# offset = [0.005, 0.005]
# cross_section = CrossSection(0.05, 0.008, offset[0], offset[1], steel.poisson_ratio, element_type=element_type, division_number=64)

preprocessor.set_cross_section_by_element('all', cross_section)

f_max = 200
df = 2
frequencies = np.arange(0, f_max+df, df)

solution = StructuralSolver(preprocessor, frequencies)

modes = 200
global_damping = [0, 0, 0, 0]
direct = solution.direct_method(global_damping)
modal = solution.mode_superposition(modes, global_damping, fastest=True)
# natural_frequencies, modal_shape = solution.modal_analysis(modes=20)
dt = time()-t0
print('Total elapsed time:', dt,'[s]')

######################################################################################
##                       POST-PROCESSING THE RESULTS                                ##
######################################################################################

run=1

if load_file==1:   

    if run==1:
        # nodal response (node, dof_corrected)
        node_response = 435 # Desired node to get response.
        local_dof_response  = 0 # Get the response at the following degree of freedom
    if run==2:
        # nodal response (node, dof_corrected)
        node_response = 185 # Desired node to get response.
        local_dof_response  = 1 # Get the response at the following degree of freedom
    if run==3:
        # nodal response (node, dof_corrected)
        node_response = 709 # Desired node to get response.
        local_dof_response  = 2 # Get the response at the following degree of freedom

elif load_file==2:

    if run==1:
        # nodal response (node, dof_corrected)
        node_response = 436 # Desired node to get response.
        local_dof_response  = 0 # Get the response at the following degree of freedom
    if run==2:
        # nodal response (node, dof_corrected)
        node_response = 187 # Desired node to get response.
        local_dof_response  = 1 # Get the response at the following degree of freedom
    if run==3:
        # nodal response (node, dof_corrected)
        node_response = 711 # Desired node to get response.
        local_dof_response  = 2 # Get the response at the following degree of freedom


Xd = get_structural_frf(preprocessor, direct, node_response, local_dof_response, absolute=True)
Xs = get_structural_frf(preprocessor, modal, node_response, local_dof_response, absolute=True)

# test_label = "ey_{}mm_ez_{}mm".format(int(offset[0]*1000),int(offset[1]*1000))

# if run==1:
#     # file1 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_n361_Ux_n436.csv", "r")
#     file1 = "C:/Users/"
#     FRF = np.loadtxt(file1, delimiter=",", skiprows=2)
#     # file1.close()
# elif run==2:
#     # file2 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_n361_Uy_n187.csv", "r")
#     file2 = "C:/Users/"
#     FRF = np.loadtxt(file2, delimiter=",", skiprows=2)
#     # file2.close()
# elif run==3:
#     # file3 = open("examples/validation_structural/data/" + test_label + "/FRF_Fx_1N_n361_Uz_n711.csv", "r")
#     file3 = "C:/Users/"
#     FRF = np.loadtxt(file3, delimiter=",", skiprows=2)
#     # file3.close()
# else:
#     print("Invalid run number entry!")

fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(1,1,1)
plt.semilogy(frequencies, np.abs(Xd), color = [0,0,0], linewidth=3)
plt.semilogy(frequencies, np.abs(Xs), color = [1,0,0], linewidth=1.5)
# plt.semilogy(FRF[:,0], np.abs(FRF[:,1] + 1j*FRF[:,2]), color = [0,0,1], linewidth=1)
ax.set_title(('FRF: Direct and Mode Superposition Methods'), fontsize = 18, fontweight = 'bold')
ax.set_xlabel(('Frequency [Hz]'), fontsize = 16, fontweight = 'bold')
ax.set_ylabel(("FRF's magnitude [m]"), fontsize = 16, fontweight = 'bold')
plt.legend(['Direct - OpenPulse','Mode Superposition - OpenPulse', 'Direct - Ansys'], loc="best")
plt.show()

# %%
