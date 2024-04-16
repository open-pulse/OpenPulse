#%%
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.preprocessor import  Preprocessor
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

# Fluid setup
speed_of_sound = 343.21
density = 1.2041
air = Fluid('air', density, speed_of_sound)
air.isentropic_exponent = 1.400
air.thermal_conductivity = 0.0263
air.specific_heat_Cp = 1007
air.dynamic_viscosity = 184.6e-7    

steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.05, 0.008, offset_y=0, offset_z=0)
cross_section.update_properties()
cross_section_expansion = CrossSection(0.288, 0.008, offset_y=0, offset_z=0)
cross_section_expansion.update_properties()
cross_section_branch = CrossSection(0.025, 0.004, offset_y=0, offset_z=0)
cross_section_branch.update_properties()

# Preprocessor init
preprocessor = Preprocessor()
preprocessor.generate('examples/validation_length_correction/tube_2_expasion.iges', 0.01)
preprocessor.set_material_by_element('all', steel)
preprocessor.set_acoustic_pressure_bc_by_node(10, 1 + 0j)
preprocessor.set_radiation_impedance_bc_by_node(1047 , 0)

element_type = 'LRF full'
preprocessor.set_acoustic_element_type_by_element('all', element_type, proportional_damping=None)

preprocessor.set_fluid_by_element('all', air)
preprocessor.set_cross_section_by_element('all', cross_section)
preprocessor.set_cross_section_by_lines(40, cross_section_expansion)
preprocessor.set_cross_section_by_lines([37, 38, 39], cross_section_branch)
preprocessor.set_cross_section_by_lines([21, 22, 23, 24, 25, 27, 28], cross_section_branch)

preprocessor.set_length_correction_by_element([9, 10, 11, 12, 13, 659, 660, 661, 662, 663, 711, 712, 885, 886, 1197, 1198, 1225, 1226, 1227, 1228, 1235, 1236], 0, "section") # Expansion correction
preprocessor.set_length_correction_by_element([608, 609, 610, 967, 968, 984, 985, 986, 987, 988, 1004, 1005, 1006, 1007, 1008, 1009, 1047, 1048, 1097, 1098, 1147, 1148, 1149], 1, "section") # Side branch correction
# Analisys Frequencies
f_max = 250
df = 1
frequencies = np.arange(df, f_max+df, df)

solution = SolutionAcoustic(mesh, frequencies)

direct = solution.direct_method()
#%% Validation

pressure = get_acoustic_frf(mesh, direct, 1047, dB=True)
p_ref = 20e-6
 
plt.rcParams.update({'font.size': 12})

f_fem=np.loadtxt("examples/validation_length_correction/tube_2_expasion.dat")[:,0] 
p_fem=np.loadtxt("examples/validation_length_correction/tube_2_expasion.dat")[:,1:]
p_fem_dB = 20*np.log10(np.abs((p_fem[:, 0] + 1j *p_fem[:, 1])/p_ref))

#Axis plots and legends
plt.title("Node 1047")
plt.plot(frequencies, pressure)
plt.plot(f_fem, p_fem_dB,'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.ylim(0, 120) 
plt.grid(True)
plt.show()

