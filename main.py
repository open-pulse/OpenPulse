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
do = 0.05   # External diameter [m]
t  = 0.008 # Thickness [m]
cross_section = TCS(do, t) 

# Nodal coordinates
coord = np.loadtxt('C:\Kula\Atividades\Petrobras\Out-Git-open-pulse\coord_ord_OK.dat') 

# Connectivity
connect = np.loadtxt('C:\Kula\Atividades\Petrobras\Out-Git-open-pulse\connect_ord_OK.dat', dtype=int)

# Boundary conditions
fixednodes = np.array([1,1200,1325])
fixeddof = np.zeros(6*len(fixednodes))

for i in range(6):
    fixeddof[i] = 6*(fixednodes[0]-1) + i+1
    fixeddof[i+6] = 6*(fixednodes[1]-1) + i+1
fixeddof = fixeddof.astype(int)

# Tube Segment  is totally define
Segm = TB.Segment(coord,connect,fixeddof,mat,tube)

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
