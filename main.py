#%% 
import numpy as np
import time

from material import Material
from node import Node
from tube import TubeCrossSection as TCS
from element import Element
from assembly import Assembly

import Animate.MS_Animation as Anima
import matplotlib.pylab as plt
from scipy.sparse.linalg import eigs, eigsh, lobpcg



# Material definition: steel
young_modulus = 210e9 # Young modulus [Pa]
poisson_ratio = 0.3   # Poisson ratio[-]
density = 7860  # Density[kg/m^3]
material_1 = Material('Steel', density, young_modulus = young_modulus, poisson_ratio = poisson_ratio)

# Cross section definition:
D_external = 0.05   # External diameter [m]
thickness  = 0.008 # Thickness [m]
cross_section_1 = TCS(D_external, thickness = thickness) 

# Nodal coordinates
nodal_coordinates = np.loadtxt('coord_ord_OK.dat') 

# Connectivity
connectivity = np.loadtxt('connect_ord_OK.dat', dtype=int)

# Boundary conditions
fixed_nodes = np.array([1,1200,1325])

# Material atribuition for each element
material_list = [1, material_1]
material_dictionary = { i:material_list[1] for i in connectivity[:,0] }

# Cross section properties atribuition for each element
cross_section_list = [1, cross_section_1]
cross_section_dictionary = { i:cross_section_list[1] for i in connectivity[:,0] }

# Element type atribuition
element_type_dictionary = { i:'pipe16' for i in connectivity[:,0] }


# Tube Segment  is totally define
assemble = Assembly(nodal_coordinates,
                connectivity,
                fixed_nodes,
                material_list,
                material_dictionary,
                cross_section_list,
                cross_section_dictionary,
                element_type_dictionary)

# Global Assembly
start = time.time()
K, M, I, J, coo_K, coo_M, total_dof  = assemble.global_matrices( delete_line = False )
end = time.time()

print(end - start)

plt.spy(K.toarray(), markersize=5)
plt.show()

# plt.spy(K.toarray()[7150:7250,7150:7250], markersize=1)
# plt.show()

# plt.spy(K.toarray()[7850:8000,7850:8000], markersize=1)
# plt.show()

#%%


# # Modal Analysis - Full Matrix process

N_modes = 100

M = M.tocsr()
K = K.tocsr()

eigenValues, eigenVectors = eigs(K, N_modes, M, sigma = 1, which ='LM')
# eigenValues, eigenVectors = eigsh(sK, N_modes, sM, sigma=1e-8, which='LM')
# eigenValues, eigenVectors = np.linalg.eig( (K.toarray(), M.toarray()) )

idx = eigenValues.argsort()
eigenValues = ((np.real(eigenValues[idx]))**(1/2))/(2*np.pi)
eigenVectors = np.real(eigenVectors[:,idx])

# # Modal Analysis - Full Matrix process
# k = 25
# nnode = Segm.nnode
# fn, eigvects = TB.modal_analysis(k,ngln,nnode,fixeddof,K,M)

# # Modal Shape Animation
# mode = 10 # Mode to be animated
# Anima.MS_animation(coord, connect, eigvects, mode)

# # Direct solver
# frequencies = range(100)
# F = np.zeros([ K.shape[0],1 ])
# F[6*15] = 1 

# x = TB.solver_direct(frequencies, F, ngln,nnode,fixeddof, K, M)

# print(x) 


#%%
