#%%
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.solution_acoustic import SolutionAcoustic

from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf, get_acoustic_response
from pulse.animation.plot_function import plot_results

start = time()
# Fluid setup
sound_velocity = 343.21
density = 1.2041
hydrogen = Fluid('air', density, sound_velocity)
# Tube setup
cross_section = CrossSection(0.05, 0.008)
# Mesh init
mesh = Mesh()
run = 2
if run==1:
    mesh.generate('examples/iges_files/tube_2.iges', 0.01)
    mesh.set_acoustic_pressure_BC_by_node([50], [1])
    # Anechoic termination
    mesh.add_impedance_specific_to_node(1086, 343 * 1.2)
    # Rigid termination on nodes
    # mesh.set_volume_velocity_by_node([1087, 1137, 1187], [0])
if run==2:
    mesh.load_mesh('examples/validation_acoustic/coord.dat', 'examples/validation_acoustic/connect.dat')
    # Acoustic boundary conditions - Prescribe pressure
    mesh.set_acoustic_pressure_BC_by_node([1], [1])
    # Anechoic termination
    mesh.add_impedance_specific_to_node(1047, 343 * 1.2)
    # Rigid termination on nodes
    # mesh.set_volume_velocity_by_node([1087, 1137, 1187], [0])

mesh.set_fluid_by_element('all', hydrogen)
mesh.set_cross_section_by_element('all', cross_section)

# Analisys Frequencies
f_max = 200
df = 2
frequencies = np.arange(df, f_max+df, df)

# ACT = AssemblyAcoustic(mesh)
# %timeit ACT.get_global_matrices(frequencies)

solution = SolutionAcoustic(mesh, frequencies)

direct = solution.direct_method()
end = time()

print("Time:", end-start)
#%% Validation
p_ref = 20e-6

dB = lambda p : 20 * np.log10(np.abs(p / p_ref))
if run==1:
    p_out = get_acoustic_frf(mesh, direct, 1086)
    p_b1 = get_acoustic_frf(mesh, direct, 1136)
    p_b2 = get_acoustic_frf(mesh, direct, 1186)
    p_b3 = get_acoustic_frf(mesh, direct, 1236)

    text_out = "Node 1086 (output)"
    text_b1 = "Node 1136 (branch 1)"
    text_b2 = "Node 1186 (branch 2)"
    text_b3 = "Node 1236 (branch 3)"

elif run==2:    
    p_out = get_acoustic_frf(mesh, direct, 1047)
    p_b1 = get_acoustic_frf(mesh, direct, 1087)
    p_b2 = get_acoustic_frf(mesh, direct, 1137)
    p_b3 = get_acoustic_frf(mesh, direct, 1187)

    text_out = "Node 1047 (output)"
    text_b1 = "Node 1087 (branch 1)"
    text_b2 = "Node 1137 (branch 2)"
    text_b3 = "Node 1187 (branch 3)"

f_com=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,0] 
p_out_b1_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,1:]
p_out_b2_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch2_out_equal_d_Z.txt", comments='%')[:,1:]
p_out_b3_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch3_out_equal_d_Z.txt", comments='%')[:,1:] 
p_out_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_out_equal_d_Z.txt", comments='%')[:,1:]
 
plt.rcParams.update({'font.size': 12})

#Axis plots and legends
plt.subplot(2, 2, 1)
plt.title(text_out)
plt.plot(frequencies, dB(p_out))
plt.plot(f_com, dB(p_out_com_3d[:, 0] + 1j *p_out_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 2)
plt.title(text_b1)
plt.plot(frequencies, dB(p_b1))
plt.plot(f_com, dB(p_out_b1_com_3d[:, 0] + 1j *p_out_b1_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 3)
plt.title(text_b2)
plt.plot(frequencies, dB(p_b2))
plt.plot(f_com, dB(p_out_b2_com_3d[:, 0] + 1j *p_out_b2_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 4)
plt.title(text_b3)
plt.plot(frequencies, dB(p_b3))
plt.plot(f_com, dB(p_out_b3_com_3d[:, 0] + 1j *p_out_b3_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol',],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.tight_layout()
plt.show()

column = 48

pressures, _, _, _ = get_acoustic_response(mesh, direct, column)

plot_results( mesh,
              pressures,
              out_OpenPulse = True,
              Acoustic = True, 
              Show_nodes = True, 
              Undeformed = False, 
              Deformed = False, 
              Animate_Mode = True, 
              Save = False)
