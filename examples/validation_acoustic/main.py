#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.preprocessor import  Preprocessor
from pulse.processing.acoustic_solver import AcousticSolver
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
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.05, 0.008, offset_y = 0.005, offset_z = 0.005)
#  Preprocessor init
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