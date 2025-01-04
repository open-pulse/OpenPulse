#%%
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse.model.preprocessor import Preprocessor
from pulse.model.perforated_plate import PerforatedPlate
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.acoustic_solver import AcousticSolver
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

# Fluid setup
speed_of_sound = 347.21
density = 1.1614
air = Fluid('air', density, speed_of_sound)
air.isentropic_exponent = 1.400
air.thermal_conductivity = 0.0263
air.specific_heat_Cp = 1007
air.dynamic_viscosity = 1.846e-05

steel = Material('Steel', 7860, elasticity_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.273, 0.00927, offset_y=0, offset_z=0)
cross_section.update_properties()
cross_section_expansion = CrossSection(0.56, 0.00475, offset_y=0, offset_z=0)
cross_section_expansion.update_properties()

# preprocessor init
preprocessor = Preprocessor()
preprocessor.generate('examples/validation_perforated_plate/silencer_wpp.iges', 0.01)
preprocessor.set_material_by_element('all', steel)
preprocessor.set_acoustic_pressure_bc_by_node(188, 2 + 0j)
preprocessor.set_radiation_impedance_bc_by_node(234 , 0)

element_type = 'undamped'
preprocessor.set_acoustic_element_type_by_element('all', element_type, proportional_damping=None)

preprocessor.set_fluid_by_element('all', air)
preprocessor.set_cross_section_by_element('all', cross_section)
preprocessor.set_cross_section_by_lines([1, 2, 3, 4], cross_section_expansion)

# Frequencies of analysis
f_max = 400
df = 1
frequencies = np.arange(df, f_max+df, df)
solution = AcousticSolver(preprocessor, frequencies)

direct = solution.direct_method()

# Perforated plate setup
hole_diameter = 1e-3
thickness = 0.002
porosity = 0.01
pp = PerforatedPlate(hole_diameter, thickness, porosity)
preprocessor.set_perforated_plate(86, pp)

solution = AcousticSolver(preprocessor, frequencies)
direct_pp = solution.direct_method()

f_fem=np.loadtxt("examples/validation_perforated_plate/FEM.txt", delimiter=',')[:,0] 
p_fem=np.loadtxt("examples/validation_perforated_plate/FEM.txt", delimiter=',')[:,1:4] 

p_ref = 20e-6
p_fem_dB = 20*np.log10(p_fem[:,2]/(np.sqrt(2)*p_ref))
 
plt.rcParams.update({'font.size': 12})
plt.figure()
#Axis plots and legends
plt.title("Node 234")
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct, 234, dB=True))
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct_pp, 234, dB=True),'-.')
plt.plot(f_fem, p_fem_dB,':')
# plt.plot(f_fem, p_fem_zlin[:,2],':')
plt.legend(['FETM - OpenPulse','FETM - OpenPulse w/ Perforated Plate','FEM - w/ Perforated Plate'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 400) 
# plt.ylim(40, 120) 
plt.grid(True)
plt.show()

plt.figure()
#Axis plots and legends
plt.title("Node 234")
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct, 234, real=True))
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct_pp, 234, real=True),'-.')
plt.plot(f_fem, p_fem[:,0],':')
plt.legend(['FETM - OpenPulse','FETM - OpenPulse w/ Perforated Plate','FEM - w/ Perforated Plate'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [Pa]')
plt.xlim(0, 400) 
plt.grid(True)
plt.show()

plt.figure()
#Axis plots and legends
plt.title("Node 234")
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct, 234, imag=True))
plt.plot(frequencies, get_acoustic_frf(preprocessor, direct_pp, 234, imag=True),'-.')
plt.plot(f_fem, p_fem[:,1],':')
plt.legend(['FETM - OpenPulse','FETM - OpenPulse w/ Perforated Plate','FEM - w/ Perforated Plate'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [Pa]')
plt.xlim(0, 400) 
plt.grid(True)
plt.show()
