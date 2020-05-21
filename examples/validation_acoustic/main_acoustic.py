#%%
from time import time

import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_acoustic import SolutionAcoustic

from pulse.postprocessing.plot_data import get_frf, get_displacement_matrix

# Fluid setup
sound_velocity = 350.337
density = 24.85
hydrogen = Fluid('hydrogen', density, sound_velocity)
# Tube setup
cross_section = CrossSection(0.05, 0.008)
# Mesh init
mesh = Mesh()
run = 2
if run==1:
    mesh.generate('examples/iges_files/tube_2.iges', 0.01)
    mesh.set_acoustic_boundary_condition_by_node([1], [1])
if run==2:
    mesh.load_mesh('coord.dat', 'connect.dat')
    # Acoustic boundary conditions - Prescribe pressure
    mesh.set_acoustic_boundary_condition_by_node([1], [1])

mesh.set_fluid_by_element('all', hydrogen)
mesh.set_cross_section_by_element('all', cross_section)

# Rigid termination on nodes
mesh.set_volume_velocity_by_node([1087, 1137, 1187], [0])

# Anechoic termination
z = 343 * 1.2
mesh.add_impedance_specific_to_node(1047, z)

# Analisys Frequencies
f_max = 250
df = 1
frequencies = np.arange(df, f_max+df, df)

solution = SolutionAcoustic(mesh, frequencies)
start = time()
direct = solution.direct_method()
end = time()

print("Time:", end-start)
#%% Validation
p_ref = 20e-6

dB = lambda p : 20 * np.log10(np.abs(p / p_ref))

p_1047 = direct[1047-1, :]
p_1087 = direct[1087-1, :]
p_1137 = direct[1137-1, :]
p_1187 = direct[1187-1, :]


f_com=np.loadtxt("test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,0] 
p_out_b1_com_3d=np.loadtxt("test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,1:]
p_out_b2_com_3d=np.loadtxt("test_geom_2_branch2_out_equal_d_Z.txt", comments='%')[:,1:]
p_out_b3_com_3d=np.loadtxt("test_geom_2_branch3_out_equal_d_Z.txt", comments='%')[:,1:] 
p_out_com_3d=np.loadtxt("test_geom_2_out_equal_d_Z.txt", comments='%')[:,1:]
 
plt.rcParams.update({'font.size': 12})

#Axis plots and legends
plt.subplot(2, 2, 1)
plt.title('Node 1047')
plt.plot(frequencies, dB(p_1047))
plt.plot(f_com, dB(p_out_com_3d[:, 0] + 1j *p_out_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 2)
plt.title('Node 1087')
plt.plot(frequencies, dB(p_1087))
plt.plot(f_com, dB(p_out_b1_com_3d[:, 0] + 1j *p_out_b1_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 3)
plt.title('Node 1137')
plt.plot(frequencies, dB(p_1137))
plt.plot(f_com, dB(p_out_b2_com_3d[:, 0] + 1j *p_out_b2_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 4)
plt.title('Node 1187')
plt.plot(frequencies, dB(p_1187))
plt.plot(f_com, dB(p_out_b3_com_3d[:, 0] + 1j *p_out_b3_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol',],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.tight_layout()
plt.show()

