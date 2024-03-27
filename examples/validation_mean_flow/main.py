#%%
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.preprocessor import Preprocessor
from pulse.preprocessing.perforated_plate import PerforatedPlate
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

# Fluid setup
speed_of_sound = 347.21
density = 1.1614
air = Fluid('air', density, speed_of_sound)
air.isentropic_exponent = 1.400
air.thermal_conductivity = 0.0263
air.specific_heat_Cp = 1007
air.dynamic_viscosity = 1.846e-05

steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
# Tube setup

section_parameters = [0.04859, 0.003, 0, 0, 0, 0]
pipe_section_info = {  "section_type_label" : "Pipe section" ,
                        "section_parameters" : section_parameters  }

cross_section1 = CrossSection(pipe_section_info=pipe_section_info)
cross_section1.update_properties()

section_parameters = [0.04044, 0.003, 0, 0, 0, 0]
pipe_section_info = {  "section_type_label" : "Pipe section" ,
                        "section_parameters" : section_parameters  }

cross_section2 = CrossSection(pipe_section_info=pipe_section_info)
cross_section2.update_properties()

# preprocessor init

preprocessor = Preprocessor()
preprocessor.generate('examples/validation_mean_flow/side_branch.iges', 0.01)
preprocessor.set_material_by_element('all', steel)
# preprocessor.set_volume_velocity_bc_by_node(51, 1.8543e-5 + 0j)
preprocessor.set_acoustic_pressure_bc_by_node(51, [1 + 0j,''])
preprocessor.set_radiation_impedance_bc_by_node(103 , 0)

# element_type = 'undamped mean flow'
element_type = 'peters'
# element_type = 'howe'
preprocessor.set_acoustic_element_type_by_element('all', element_type, proportional_damping=None)

preprocessor.set_fluid_by_element('all', air)
preprocessor.set_cross_section_by_line([1, 2], cross_section1)
preprocessor.set_cross_section_by_line([3, 4], cross_section2)

mach = 0.1
mean_velocity = mach * air.speed_of_sound
preprocessor.set_mean_velocity_by_element('all', mean_velocity)

# Frequencies of analysis
f_max = 1000
df = 1
frequencies = np.arange(df, f_max+df, df)
solution = SolutionAcoustic(preprocessor, frequencies)

direct = solution.direct_method()

f_fem=np.loadtxt("examples/validation_mean_flow/dataM0p1_peters.txt", delimiter=',')[:,0] 
p_fem=np.loadtxt("examples/validation_mean_flow/dataM0p1_peters.txt", delimiter=',')[:,1:3] 
p_fem = p_fem[:,0] +1j*p_fem[:,1]

p_ref = 20e-6
p_fem_dB = 20*np.log10(np.abs(p_fem)/(np.sqrt(2)*p_ref))
p_out = get_acoustic_frf(preprocessor, direct, 103, dB=True)

plt.rcParams.update({'font.size': 12})
plt.figure()
#Axis plots and legends
plt.title('Node 51. Model: '+ str(element_type) + '. Mach: '+ str(mach))
plt.plot(frequencies, p_out)
plt.plot(f_fem, p_fem_dB,':')
plt.legend(['FETM - OpenPulse','FETM - Martin'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(df, f_max) 
plt.grid(True)
plt.show()
