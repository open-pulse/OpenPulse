import numpy as np
import matplotlib

# Load nodal results from different files 

mode = 32 

connectivity = np.array(np.loadtxt('Ex_02/connect.dat')[:,1:],int)
coordinates = np.array(np.loadtxt('Ex_02/coord.dat')[:,1:])
eigen_vectors = np.array(np.loadtxt('Ex_02/u_def.dat')

number_nodes = np.shape(eigen_vectors)[0]
u_sum = np.zeros((number_nodes, 2))

u_def[:,0]   =  eigen_vectors[:,0]
u_def[:,1:4] =  A = eigen_vectors[:,1+(mode-1)*3:3+(mode-1)*3+1]

u_sum[:,0]  =  eigen_vectors[:,0] 
u_sum[:,1]  =  np.linalg.norm(eigen_vectors[:,1+(mode-1)*3:3+(mode-1)*3+1],axis=1)