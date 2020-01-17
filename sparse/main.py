import numpy as np
import TB_Matrices as TB
import MS_Animation as MS


# Finite Elements Parameters
npel = 2 # Nodes Per ELements
ngln = 6 # Numero de Graus de Liberdade por Nó

# Material definition: steel
E   = 210e9 # Young modulus [Pa]
nu  = 0.3   # Poisson ratio[-]
rho = 7860  # Density[kg/m^3]
mat = TB.Material_isotropic(rho,E,nu)

# Section definition: 
do      = 0.1   # External diameter [m]
t       = 0.005 # Thickness [m]
tube    = TB.Tube(do, t) 

# Nodal coordinates
coord = np.loadtxt('coord.dat') 

# Connectivity
connect = np.loadtxt('connect.dat')
connect = connect.astype(int)

# Boundary conditions
fixednodes = np.array([58,68])
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
MS.anima(coord, connect, eigvects, mode)
