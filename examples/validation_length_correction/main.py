from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf, get_acoustic_response
from pulse.animation.plot_function import plot_results

# Fluid setup
speed_of_sound = 343.21
density = 1.2041
air = Fluid('air', density, speed_of_sound)
hysteretic_damping = 0.01
air.dynamic_viscosity = 1.846e-5
air.specific_heat_Cp = 1.0049e3
air.isentropic_exponent = 1.400
air.thermal_conductivity = 0.02587

steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.05, 0.008, 0, 0)
cross_section.update_properties()
cross_section_expansion = CrossSection(0.288, 0.008, 0, 0)
cross_section_expansion.update_properties()
cross_section_branch = CrossSection(0.033, 0.008, 0, 0)
cross_section_branch.update_properties()

# Mesh init
mesh = Mesh()
mesh.generate('examples/validation_length_correction/tube_2_expasion.iges', 0.01)
mesh.set_material_by_element('all', steel)

element_type = 0
#0 - Dampingless
#1 - Hysteretic
#2 - Wide-duct
#3 - LRF fluid equivalent
#4 - LRF full

radiation_impedance = 1

mesh.set_acoustic_element_type_by_line('all', element_type, hysteretic_damping = hysteretic_damping)

mesh.set_acoustic_pressure_bc_by_node(10, 1 + 0j)

mesh.set_fluid_by_element('all', air)
mesh.set_cross_section_by_element('all', cross_section)
mesh.set_cross_section_by_line(40, cross_section_expansion)
mesh.set_cross_section_by_line([37, 38, 39], cross_section_branch)
mesh.set_cross_section_by_line([21, 22, 23, 24, 25, 27, 28], cross_section_branch)

mesh.set_length_correction_by_element([10, 1227], 0, 'In code') # Expansion correction
mesh.set_length_correction_by_element([711, 886], 2, 'In code') # Loop correction
mesh.set_length_correction_by_element([1097, 1147, 1047], 1, 'In code') # Side branch correction

mesh.set_radiation_impedance_bc_by_node([1047], radiation_impedance)
# Analisys Frequencies
f_max = 250
df = 1
frequencies = np.arange(df, f_max+df, df)

solution = SolutionAcoustic(mesh, frequencies)

direct = solution.direct_method()
pressure = get_acoustic_frf(mesh, direct, 1047, dB=True)

 
plt.rcParams.update({'font.size': 12})
#Axis plots and legends
plt.title("Node 1047")
plt.plot(frequencies, pressure)
plt.legend(['FETM - OpenPulse'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.ylim(0, 120) 
plt.grid(True)
plt.show()