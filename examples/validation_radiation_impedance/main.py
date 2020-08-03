from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.fluid import Fluid
from pulse.preprocessing.mesh import Mesh
from pulse.processing.assembly_acoustic import AssemblyAcoustic
from pulse.processing.solution_acoustic import SolutionAcoustic
from pulse.postprocessing.plot_acoustic_data import get_acoustic_frf

# Fluid setup
speed_of_sound = 343.21
density = 1.2041
air = Fluid('air', density, speed_of_sound)
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
# Tube setup
cross_section = CrossSection(0.05, 0.008, offset_y=0, offset_z=0)
cross_section.update_properties()
cross_section_expansion = CrossSection(0.288, 0.008, offset_y=0, offset_z=0)
cross_section_expansion.update_properties()
cross_section_branch = CrossSection(0.025, 0.004, offset_y=0, offset_z=0)
cross_section_branch.update_properties()

# Mesh init
mesh = Mesh()
mesh.generate('examples/iges_files/tube_2.iges', 0.01)
mesh.set_material_by_element('all', steel)
mesh.set_acoustic_pressure_bc_by_node(50, 1 + 0j)

unflanged = True
flanged = False
if unflanged:
    mesh.set_radiation_impedance_bc_by_node(1086 , 1)
elif flanged:
    mesh.set_radiation_impedance_bc_by_node(1086 , 2)

mesh.set_fluid_by_element('all', air)
mesh.set_cross_section_by_element('all', cross_section)
# Analisys Frequencies
f_max = 2500
df = 1
frequencies = np.arange(df, f_max+df, df)

solution = SolutionAcoustic(mesh, frequencies)

direct = solution.direct_method()

pressure = get_acoustic_frf(mesh, direct, 1086, dB=True)
p_ref = 20e-6
 
plt.rcParams.update({'font.size': 12})

if unflanged:
    fem=np.loadtxt("examples/validation_radiation_impedance/pout_fem_unflanged.dat", delimiter = ',')
    title = "Pressure out - Unflanged pipe"
elif flanged:
    fem=np.loadtxt("examples/validation_radiation_impedance/pout_fem_flanged.dat", delimiter = ',')
    title = "Pressure out - Flanged pipe"

fem_dB = 20*np.log10(np.abs((fem[:, 3])/p_ref))

#Axis plots and legends
plt.title(title)
plt.plot(frequencies, pressure)
plt.plot(fem[:,0], fem_dB,'-.')
plt.legend(['FETM - OpenPulse','FEM 3D - Comsol'],loc='best')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Pressure [dB]')
plt.xlim(0, 250) 
plt.grid(True)
plt.show()

