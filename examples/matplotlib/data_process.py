import numpy as np

'''
  OpenPulse Graphic interface development 

  >> This script loads nodal solution and calculates absolute value of 
  resultant displacement vector u_sum = norm(u_x, u_y, u_z) for color 
  scalling in VTK. << 

'''

# Select the mode number to be processed (mode < 40)
mode = 7

# connectivity = np.array(np.loadtxt('Ex_02/connect.dat')[:,1:],int)
# coordinates = np.array(np.loadtxt('Ex_02/coord.dat')[:,1:])
eigen_vectors = np.array(np.loadtxt('examples/matplotlib/Ex_02/u_def.dat'))

number_nodes = np.shape(eigen_vectors)[0]
u_xyz = np.zeros((number_nodes, 4))
u_sum = np.zeros((number_nodes, 2))

u_xyz[:,0]    =  eigen_vectors[:,0] 
u_xyz[:,1:4]  =  eigen_vectors[:,1+(mode-1)*3:3+(mode-1)*3+1]

u_sum[:,0]  =  eigen_vectors[:,0]
u_sum[:,1]  =  np.linalg.norm(eigen_vectors[:,1+(mode-1)*3:3+(mode-1)*3+1],axis=1)

np.savetxt('u_sum.dat', u_sum, fmt=['%6i','%1.10e'])