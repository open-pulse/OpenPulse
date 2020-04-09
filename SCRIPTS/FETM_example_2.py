import pandas as pd

import matplotlib as mpl

import matplotlib.pyplot as plt

import numpy as np

import math 

import sympy as sym

import scipy.sparse as sp

from scipy.sparse.linalg import spsolve

#%%
import time
start_time = time.time()
#%%
connect_g2 = np.loadtxt("connect_example_2.dat", dtype=int)
coord_g2 = np.loadtxt("coord_example_2.dat")

"Pressure node 1"
Pn1=1
"dof number per node"
ngl_node=1
"element numbers"
nel = len(connect_g2)
el_numb = np.arange(0,nel)
"node numbers"
nnode=  np.int(np.max(coord_g2[:,0]))
nnode_v = np.arange(0,nnode) 
"DOF's"
NGL = ngl_node*(nnode)
"node 1 conectivity"
n1_conect = connect_g2[:,1]
"node 2 conectivity"
n2_conect = connect_g2[:,2]
"Length elements vector"
node_diff=[]
Le_v=np.zeros([nel])
#for i,ii,iii in zip(n1_conect-1,n2_conect-1,el_numb):
#    node_dif= (coord_g2[i][1:]) - (coord_g2[ii][1:])
#    node_diff.append(node_dif)
#    Le=np.linalg.norm(node_diff[iii])
#    Le_v[iii]=Le
#Le_v=np.zeros([len(node_diff)])
#for j in range(len(node_diff)):
#    Le=np.linalg.norm(node_diff[j])
#    Le_v[j]=Le
#%% Frequency range
"sound gas velocity m/s"
c0=350.337
"Gas density"
rho0=24.85
"Fluid diameter [m]"
d=0.034
"Fluid branch diameter [m]"
d_b=0.022
"Fluid area"
S=np.pi*(d/2)**2
"Bend duct angle [radians]"
theta=np.deg2rad(90)
"Bend duct curvature ratio [m]"
cr_bd=0.05
cr_bd_2=0.1
"Bend duct arc length"
al_bd=theta*cr_bd
al_bd_2=theta*cr_bd_2
"Acoustic impedance"
Z=(rho0*c0)/S
step_f=1
f=np.arange(1,250+step_f,step_f)
k=((2*np.pi*f)/c0)
w=2*np.pi*f

"Fluid diameters vector [m]"
d_v=np.repeat(d, nel)

"Fluid cross-section surfaces vector"
S_v=np.pi*(d_v/2)**2
"Acoustic impedances vector"
Z_v=(rho0*c0)/S_v

#%%
"Anechoic termination"
z_nod= np.array([1047-1]) #%%levar em consideração que insert aumenta o tamano do array
S_adm=S_v[-1] #%last element section
A=S_adm/(1.2*343)
A_v=np.zeros([nel-len(z_nod),1])
#for aa in range(len(z_nod)):
A_v=np.insert(A_v,z_nod,A)
#%%
"Variables initialization"
KG = np.zeros([NGL,NGL],dtype=complex)
#KG = sp.csr_matrix((NGL,NGL), dtype=complex)
q=np.zeros([NGL]) 

p_nodes=np.array([0],dtype=int)
p_values=np.array([0],dtype=int)

p_all=[]
p_nodes=np.zeros([nnode-1,len(f)],dtype=complex)
p_b1_out=np.zeros([len(f)])
p_b2_out=np.zeros([len(f)])
p_b3_out=np.zeros([len(f)])
p_out=np.zeros([len(f)])

Ks_e=np.zeros([2,2])
KG_all=[]       
#%%
for i in range(len(f)):
    KG = np.zeros([NGL,NGL],dtype=complex)
    for l,m,ll,lll in zip(n1_conect-1,n2_conect-1,el_numb,nnode_v):
        node_dif= (coord_g2[l][1:]) - (coord_g2[m][1:])
        node_diff.append(node_dif)
        Le=np.linalg.norm(node_diff[ll])
        Le_v[ll]=Le
        Ks_e= np.array([[(-1j*np.cos(k[i]*Le_v[ll]))/(Z_v[ll]*np.sin(k[i]*Le_v[ll])), 1j/(Z_v[ll]*np.sin(k[i]*Le_v[ll]))],
                         [1j/(Z_v[ll]*np.sin(k[i]*Le_v[ll])), (-1j*np.cos(k[i]*Le_v[ll]))/(Z_v[ll]*np.sin(k[i]*Le_v[ll]))]])
        KG[l,m] += Ks_e[0,1]
        KG[m,l] += Ks_e[1,0]
        KG[l,l] += Ks_e[0,0]
        KG[m,m] += Ks_e[1,1]
        KG[lll,lll] += A_v[lll]           
    KG_all.append(KG)
    KG1=np.delete(KG,0,0)
    KG2=np.delete(KG1,0,1)
    KGc1p=KG[:,0]*Pn1
    q1=q-KGc1p
    q2=np.delete(q1,0,0)
    p=np.linalg.solve(KG2,q2)
    p_all.append(p)
    p_b1_out[i]=np.real(p_all[i][1087-2])
    p_b2_out[i]=np.real(p_all[i][1137-2])
    p_b3_out[i]=np.real(p_all[i][1187-2])
    p_out[i]=np.real(p_all[i][1047-2])
    p_nodes[:,i]=p
    #%%
p_nodes_all=np.insert(p_nodes,0,1,0)
#np.savetxt("pressure_all_nodes.dat",np.real(p_nodes_all),fmt='%24.22e')    

#%% LOAD AND PLOTS

f_com=np.loadtxt("test_geom_2_branch1_out_equal_d_Z.txt")[:,0] 
p_out_b1_com_3d=np.loadtxt("test_geom_2_branch1_out_equal_d_Z.txt")[:,1]
p_out_b2_com_3d=np.loadtxt("test_geom_2_branch2_out_equal_d_Z.txt")[:,1]
p_out_b3_com_3d=np.loadtxt("test_geom_2_branch3_out_equal_d_Z.txt")[:,1] 
p_out_com_3d=np.loadtxt("test_geom_2_pout_equal_d_Z.txt")[:,1]
 
plt.rcParams.update({'font.size': 12})

fig = plt.figure(1)
#get_ipython().run_line_magic('matplotlib', 'qt')
ax = fig.add_subplot(111)    # The big subplot
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top=False, bottom=False, left=False, right=False)

#Axis plots and legends
ax1.plot(f,p_b1_out,'-',f_com,np.real(p_out_b1_com_3d),'-.')
ax1.legend(['Branch 1 out FETM','Branch 1 out FEM 3D','Branch out FEM 3D'],loc='best')
ax1.set_xticklabels([])

ax2.plot(f,p_b2_out,'-',f_com,np.real(p_out_b2_com_3d),'-.')
ax2.legend(['Branch 2 out FETM','Branch 2 out FEM 3D','Bend out FEM 3D'],loc='best')
ax2.set_xticklabels([])
    
ax3.plot(f,p_b3_out,'-',f_com,np.real(p_out_b3_com_3d),'-.')
ax3.legend(['Branch 3 out FETM','Branch 3 out FEM 3D',],loc='best')

ax4.plot(f,p_out,'-',f_com,np.real(p_out_com_3d),'-.')
ax4.legend(['Out FETM','Out FEM 3D','Bend out FEM 3D'],loc=2)

# Set common labels
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Pressure [Pa]')

plt.show()

print("--- The executing total time of program is: %s seconds ---" % (time.time() - start_time))
                       
                
                
                
                
                
                
                
                
                
                
                


# %%
