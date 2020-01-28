import numpy as np

from material import Material
from node import Node
from tube import TubeCrossSection as TCS
from element import Element
from assembly import Assembly

import Animate.MS_Animation as Anima


# Material definition: steel
young_modulus = 210e9 # Young modulus [Pa]
poisson_ratio = 0.3   # Poisson ratio[-]
density = 7860  # Density[kg/m^3]
mat1 = Material('Steel', density, young_modulus = young_modulus, poisson_ratio = poisson_ratio)

# Cross section definition:
D_external = 0.05   # External diameter [m]
thickness  = 0.008 # Thickness [m]
cross_section = TCS(D_external, thickness = thickness) 

# Nodal coordinates
nodal_coordinates = np.loadtxt('C:\Kula\Atividades\Petrobras\Out-Git-open-pulse\coord_ord_OK.dat') 

# Connectivity
connectivity = np.loadtxt('C:\Kula\Atividades\Petrobras\Out-Git-open-pulse\connect_ord_OK.dat', dtype=int)

# Boundary conditions
fixed_nodes = np.array([1,1200,1325])

# Tube Segment  is totally define
Segm = Assembly(nodal_coordinates,
                connectivity,
                fixed_nodes,
                material_list,
                material_dictionary,
                cross_section_list,
                cross_section_dictionary,
                element_type_dictionary)

# Global Assembly
K, M    = TB.assembly(Segm,npel,ngln)

# Modal Analysis - Full Matrix process
k = 25
nnode = Segm.nnode
fn, eigvects = TB.modal_analysis(k,ngln,nnode,fixeddof,K,M)

# Modal Shape Animation
mode = 10 # Mode to be animated
Anima.MS_animation(coord, connect, eigvects, mode)

# Direct solver
frequencies = range(100)
F = np.zeros([ K.shape[0],1 ])
F[6*15] = 1 

x = TB.solver_direct(frequencies, F, ngln,nnode,fixeddof, K, M)

print(x) 
