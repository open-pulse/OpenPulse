#%% 
from time import time
import numpy as np 
import matplotlib.pyplot as plt 

from pulse.preprocessing.cross_section import CrossSection
from pulse.preprocessing.material import Material
from pulse.preprocessing.mesh import Mesh
from pulse.processing.solution_structural import SolutionStructural
from pulse.postprocessing.plot_acoustic_data import get_acoustic_response
from pulse.postprocessing.plot_structural_data import get_structural_response
from pulse.postprocessing.stress import Stress
from pulse.animation.plot_function import plot_results


''' 
    |=============================================================================|
    |  Please, it's necessary to copy and paste main.py script at OpenPulse file  |
    |  then type "python main.py" in the terminal to run the code !               |
    |=============================================================================| 
'''

t0 = time()
# PREPARING MESH
steel = Material('Steel', 7860, young_modulus=210e9, poisson_ratio=0.3)
offset = [0.005, 0.005]
element_type = 'pipe_1'
cross_section = CrossSection(0.05, 0.008, offset_y = offset[0], offset_z = offset[1], poisson_ratio=steel.poisson_ratio)
mesh = Mesh()

mesh.generate('examples/iges_files/tube_2.iges', 0.01)
mesh.set_prescribed_dofs_bc_by_node([1136, 1236], np.zeros(6))

mesh.set_element_type_by_element('all', element_type)
mesh.set_material_by_element('all', steel)
mesh.set_cross_section_by_element('all', cross_section)

mesh.set_structural_load_bc_by_node([50], np.array([1,1,1,0,0,0]))

solution = SolutionStructural(mesh)
f_max = 200
df = 2
frequencies = np.arange(0, f_max+df, df)
modes = 200
direct = solution.direct_method(frequencies, is_viscous_lumped=True)
tf = time()
print('Structural direct solution time:', (tf-t0),'[s]')
column = 50

_, coord_def, _, _ = get_structural_response(mesh, direct, column, Normalize=False)

# plot_results( mesh,
#               coord_def,
#               scf = 0.5,
#               out_OpenPulse = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = False, 
#               Animate_Mode = True, 
#               Save = False)

# Stress
acoustic_solution = np.zeros([len(mesh.nodes.keys()), len(frequencies)], dtype=complex)
stress = Stress(mesh, frequencies, direct, acoustic_solution = acoustic_solution)
start = time()
stress.get3()
end = time()

print("Stress calculation time:", end - start,'[s]')
# plot stress
stress_plot, _, _, _ = get_acoustic_response(mesh, stress.normal_axial, column)
print("Normal axial")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)

stress_plot, _, _, _ = get_acoustic_response(mesh, stress.normal_bending_y, column)
print("Normal bending y")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)

stress_plot, _, _, _ = get_acoustic_response(mesh, stress.normal_bending_z, column)
print("Normal bending z")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)

stress_plot, _, _, _ = get_acoustic_response(mesh, stress.shear_torsion, column)
print("Shear Torsion")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)

stress_plot, _, _, _ = get_acoustic_response(mesh, stress.shear_transversal_xy, column)
print("Shear Transversal xy")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)

stress_plot, _, _, _ = get_acoustic_response(mesh, stress.shear_transversal_xz, column)
print("Shear Transversal xz")
print("Value min: ", np.min(stress_plot[:,1]),"\nValue max: ", np.max(stress_plot[:,1]))

# plot_results( mesh,
#               stress_plot,
#               out_OpenPulse = True,
#               Acoustic = True, 
#               Show_nodes = True, 
#               Undeformed = False, 
#               Deformed = True, 
#               Animate_Mode = False, 
#               Save = False)