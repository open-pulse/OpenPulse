#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.model.cross_section import CrossSection
from pulse.properties.material import Material
from pulse.properties.fluid import Fluid
from pulse.model.preprocessor import  Preprocessor
from pulse.processing.assembly_structural import AssemblyStructural 
from pulse.processing.structural_solver import StructuralSolver
from pulse.processing.acoustic_solver import AcousticSolver
from pulse.postprocessing.plot_structural_data import get_structural_frf, get_structural_response
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf, get_acoustic_response
from examples.animation.plot_function import plot_results

''' 
    |=============================================================================|
    |  Please, it's necessary to copy and paste main.py script at OpenPulse file  |
    |  then type "python main.py" in the terminal to run the code !               |
    |=============================================================================| 
'''
speed_of_sound = 350.337
density = 24.85
hydrogen = Fluid('hydrogen', density, speed_of_sound)
steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.05, 0.008, offset_y = 0.005, offset_z = 0.005)
# Mesh init
preprocessor = Preprocessor()
run = 2
anechoic_termination = True
if run==1:
    preprocessor.generate('examples/iges_files/tube_2.iges', 0.01)
    preprocessor.set_acoustic_pressure_BC_by_node([50], 1)
    # Anechoic termination
    if anechoic_termination:
        preprocessor.set_specific_impedance_BC_by_node(1086, speed_of_sound * density)
if run==2:
    preprocessor.load_mesh('examples/validation_acoustic/coord.dat', 'examples/validation_acoustic/connect.dat')
    # Acoustic boundary conditions - Prescribe pressure
    preprocessor.set_acoustic_pressure_BC_by_node([1], 1)
    # Anechoic termination
    if anechoic_termination:
        preprocessor.set_specific_impedance_BC_by_node(1047, speed_of_sound*density)

preprocessor.set_element_type('pipe_1')
preprocessor.set_fluid_by_element('all', hydrogen)
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', cross_section)

# Analisys Frequencies
f_max = 250
df = 1
frequencies = np.arange(df, f_max+df, df)

solution_acoustic = AcousticSolver(preprocessor, frequencies)

direct = solution_acoustic.direct_method()
#%% Acoustic validation

if run==1:
    p_out = get_acoustic_frf(preprocessor, direct, 1086)
    p_b1 = get_acoustic_frf(preprocessor, direct, 1136)
    p_b2 = get_acoustic_frf(preprocessor, direct, 1186)
    p_b3 = get_acoustic_frf(preprocessor, direct, 1236)
    text_out = "Node 1086 (output)"
    text_b1 = "Node 1136 (branch 1)"
    text_b2 = "Node 1186 (branch 2)"
    text_b3 = "Node 1236 (branch 3)"

elif run==2:    
    p_out = get_acoustic_frf(preprocessor, direct, 1047)
    p_b1 = get_acoustic_frf(preprocessor, direct, 1087)
    p_b2 = get_acoustic_frf(preprocessor, direct, 1137)
    p_b3 = get_acoustic_frf(preprocessor, direct, 1187)
    text_out = "Node 1047 (output)"
    text_b1 = "Node 1087 (branch 1)"
    text_b2 = "Node 1137 (branch 2)"
    text_b3 = "Node 1187 (branch 3)"

if anechoic_termination:
    f_com=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,0] 
    p_out_b1_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d_Z.txt", comments='%')[:,1:]
    p_out_b2_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch2_out_equal_d_Z.txt", comments='%')[:,1:]
    p_out_b3_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch3_out_equal_d_Z.txt", comments='%')[:,1:] 
    p_out_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_out_equal_d_Z.txt", comments='%')[:,1:]
else:
    f_com=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d.txt", comments='%')[:,0] 
    p_out_b1_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch1_out_equal_d.txt", comments='%')[:,1:]
    p_out_b2_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch2_out_equal_d.txt", comments='%')[:,1:]
    p_out_b3_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_branch3_out_equal_d.txt", comments='%')[:,1:] 
    p_out_com_3d=np.loadtxt("examples/validation_acoustic/test_geom_2_out_equal_d.txt", comments='%')[:,1:]
 
plt.rcParams.update({'font.size': 12})
p_ref = 20e-6

dB = lambda p : 20 * np.log10(np.abs(p / p_ref))
#Axis plots and legends
plt.subplot(2, 2, 1)
plt.title(text_out)
plt.plot(frequencies, p_out)
plt.plot(f_com, dB(p_out_com_3d[:, 0] + 1j *p_out_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 2)
plt.title(text_b1)
plt.plot(frequencies, p_b1)
plt.plot(f_com, dB(p_out_b1_com_3d[:, 0] + 1j *p_out_b1_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 3)
plt.title(text_b2)
plt.plot(frequencies, p_b2)
plt.plot(f_com, dB(p_out_b2_com_3d[:, 0] + 1j *p_out_b2_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.subplot(2, 2, 4)
plt.title(text_b3)
plt.plot(frequencies, p_b3)
plt.plot(f_com, dB(p_out_b3_com_3d[:, 0] + 1j *p_out_b3_com_3d[:, 1]),'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol',],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)

plt.tight_layout()
plt.show()

column = 3

# pressures, _, _, _ = get_acoustic_response(preprocessor, direct, column)

# plot_results( preprocessor,
#               pressures,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = False, 
#               Animate_Mode = True, 
#               Save = False)

#%%
## Structural Coupled ##
preprocessor.set_prescribed_DOFs_BC_by_node([1136, 1236, 1086], np.zeros(6))

preprocessor.add_spring_to_node([427],1*np.array([1e9,1e9,1e9,0,0,0]))
preprocessor.add_mass_to_node([204],0*np.array([80,80,80,0,0,0]))
preprocessor.add_damper_to_node([342],0*np.array([1e3,1e3,1e3,0,0,0]))

solution_structural = StructuralSolver(mesh, acoustic_solution = direct)
modes = 200
natural_frequencies, mode_shapes = solution_structural.modal_analysis(modes=modes, harmonic_analysis=True)

# SOLVING THE PROBLEM BY TWO AVALIABLE METHODS
direct = solution_structural.direct_method(frequencies, is_viscous_lumped=True)
modal = solution_structural.mode_superposition(frequencies, modes, fastest=True)

column = 3

ms_results = np.real(modal)

load_reactions = solution_structural.get_reactions_at_fixed_nodes(frequencies, direct)
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