#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 
# import seaborn as sns

from pulse.model.cross_section import CrossSection
from pulse.model.properties.material import Material
from pulse.model.properties.fluid import Fluid
from pulse.model.preprocessor import Preprocessor
from pulse.processing.assemblers.acoustic_assembler import AcousticAssembler
from pulse.processing.assemblers.structural_assembler import StructuralAssembler
from pulse.processing.solvers.harmonic_solver import HarmonicSolver
from pulse.postprocessing.structural_post_processor import StructuralPostProcessor
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response
from pulse.postprocessing.plot_structural_data import get_structural_response, get_stress_data
from examples.animation.plot_function import plot_results


''' 
    |=============================================================================|
    |  Please, it's necessary to copy and paste main.py script at OpenPulse file  |
    |  then type "python main.py" in the terminal to run the code !               |
    |=============================================================================| 
'''

t0 = time()
# PREPARING MESH
speed_of_sound = 331.2 # speed of sound at 0ºC
density = 1.204
air = Fluid('air', density, speed_of_sound)
steel = Material(name='Steel', identifier=1, density=7860, elasticity_modulus=210e9, poisson_ratio=0.3)
offset = [0.005, 0.005]
element_type = 'pipe_1'
cross_section = CrossSection(0.05, 0.008, offset_y = offset[0], offset_z = offset[1], poisson_ratio=steel.poisson_ratio)
cross_section.update_properties()
preprocessor = Preprocessor()

preprocessor.generate('examples/iges_files/tube_2.iges', 0.01)
# preprocessor.set_acoustic_pressure_bc_by_node([50], 1e5 + 0j)
# preprocessor.set_specific_impedance_bc_by_node(1086, speed_of_sound * density+ 0j)
preprocessor.set_prescribed_dof([1136, 1236], np.zeros(6)+ 0j)

preprocessor.set_element_type_by_element('all', element_type)
preprocessor.set_fluid_by_element('all', air)
preprocessor.set_material_by_element('all', steel)
preprocessor.set_cross_section_by_element('all', cross_section)
preprocessor.set_structural_loads([50], np.array([1,1,1,0,0,0])+ 0j)

f_max = 200
df = 2
frequencies = np.arange(0.001, f_max+df, df)
modes = 200

# acoustic_assembler = AcousticAssembler(mesh)
# acoustic_solver = HarmonicSolver(acoustic_assembler)
# acoustic_solver.direct_method(frequencies)

struct_assembler = StructuralAssembler(preprocessor)  # acoustic_solution=acoustic_solver.solution
solver = HarmonicSolver(struct_assembler)
solver.direct_method(frequencies)
direct_structural = solver.solution
tf = time()
print('Structural direct solution time:', (tf-t0),'[s]')
column = 50

_, coord_def, _, _ = get_structural_response(preprocessor, direct_structural, column, Normalize=False)

post = StructuralPostProcessor(solver)
post.stress_calculate(external_pressure=0, damping=False)
stress_data = get_stress_data(preprocessor, column, real=True)
stress_plot = stress_data[:,[0,2]]

print("Value min: ", np.min(stress_plot[:,1]))
print("Value max: ", np.max(stress_plot[:,1]))
plot_results( preprocessor,
              coord_def,
              data_stress = stress_plot,
              scf = 0.20,
              out_OpenPulse = True, 
              Show_nodes = False, 
              Undeformed = False, 
              Deformed = True, 
              Animate_Mode = False, 
              Save = False)
