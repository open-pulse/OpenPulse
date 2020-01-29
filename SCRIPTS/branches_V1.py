# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 10:28:40 2020

@author: Martin Tuozzo
"""

#%%
import pandas as pd

import matplotlib as mpl

import matplotlib.pyplot as plt

import numpy as np

import math 

import sympy as sym

import scipy.sparse.linalg

import scipy.sparse

#%% - Branch geometrical properties

"Number of branches"
n_branches=3
"Element node number"
nn=6
"Total node number"
ntn=n_branches*nn

"Volume velocity source index node number"
nnq=1
"Pressure source index node number"
nnp=2

"Branch 1 length"
L_b1=0.4
"Branch 2 length"
L_b2=0.4
"Branch 3 length"
L_b3=0.4
"Branch 4 length"
L_b4=0.4
"Duct branch exterior diameter 1 [m]"
d_b1=0.154 
"Duct branch exterior diameter 2 [m]"
d_b2=0.154 #%% 0.205
"Duct branch exterior diameter 3 [m]"
d_b3=0.154
"Duct branch exterior diameter 4 [m]"
d_b4=0.154
"Duct branch 1 thickness [m]"
e_b1=0.01
"Duct branch 2 thickness [m]"
e_b2=0.01 #%%0.012
"Duct branch 3 thickness [m]"
e_b3=0.01
"Duct branch 4 thickness [m]"
e_b4=0.01

#%% - Pressures and velocities applied to node 1

pn1=100 # [Pa]
qn1=0  # [m3/s] 

#%% variaveis fisicas

f=np.arange(1,251,1)
w=2*math.pi*np.transpose(f)
c=1149.4/3.281 #350.337 sond velocity in the gas m/s
rho_std=(0.00183)/0.00194 #standard density kg/m3
rho=0.0482/0.00194 #density kg/m3
rho_vec=np.array([rho_std,rho])
k1=(w/c)

#%% variaveis da geometria do duto

d_b1i=d_b1-(2*e_b1)
d_b2i=d_b2-(2*e_b2)
d_b3i=d_b3-(2*e_b3)
d_b4i=d_b4-(2*e_b4)

r_b1i=d_b1i/2
r_b2i=d_b2i/2
r_b3i=d_b3i/2
r_b4i=d_b4i/2

S_b1=math.pi*r_b1i**2
S_b2=math.pi*r_b2i**2
S_b3=math.pi*r_b3i**2
S_b4=math.pi*r_b4i**2

r_vec=np.array([r_b1i,r_b2i,r_b3i,r_b4i])
S_vec=math.pi*(r_vec**2)
L_vec=np.array([L_b1,L_b2,L_b3,L_b4])

deltaL=0.6133*r_vec
#%% definições de impedancia
Z0=rho_vec[1]*c

Z1=Z0/S_b1
Z2=Z0/S_b2
Z3=Z0/S_b3
Z4=Z0/S_b4

Zin=np.zeros((len(f),1),  dtype=int) #+1j*1*10**6
#Zin=np.ones((len(f),1),  dtype=int)*1*10**6 #%1j*0.04 #%1j*1*10**6
#Zin=np.ones((len(f),1),  dtype=int)*1j*0.04

Zrad_nf=np.zeros((len(f),n_branches),  dtype=complex)
for i in range(n_branches):
    Zrad_nf[:,i]=Z0*(0.25*((k1*(r_vec[i]))**2) + 1j*k1*deltaL[i]) 

Z_branches=np.concatenate((Zin,Zrad_nf[:,1:4]),axis=1)
#%% Matrix initialization


Z_vec=((rho_vec[1]*c)*np.ones((n_branches)))/S_vec[0:n_branches]

conec_matrix=np.matrix([[1,0,-1,0],[0,1,0,-1]])
element_matrix=np.zeros((2,4),  dtype=complex)
TM=np.zeros((nn*n_branches +1,nn*n_branches +1), dtype=complex)
#qp_vec=np.array([])
qp_vec=np.zeros((nn*n_branches +1,1),  dtype=complex)
solution_qp=[]
solution_qp_freq=[]
p0_2=[]
pL_2=[]
q0_2=[]
qL_2=[]
TM_all=[]
qp_vec[nnp]=-pn1
qp_vec[nnq]=-qn1
    
#%%Assembly process

for i in range(len(f)):
    for n in range(n_branches):
            TM[nn*n +5, nn*n +5]=1
            TM[nn*n +5, ntn]=-1
            TM[ntn, nn*0 +4]=1  #%% volume velocity sense for the n branches - branch 1 - 1 into the junction -1 out to the junction
            TM[ntn, nn*1 +4]=-1  #%% volume velocity sense for the n branches - branch 2
            TM[ntn, nn*2 +4]=-1  #%% volume velocity sense for the n branches - branch 3
#            TM[ntn, nn*3 +4]=-1  #%% volume velocity sense for the n branches - branch 4
            TM[nn*n , (nn*n):(nn*n +2)]=[-Z_branches[i,n], -1]
            element_matrix=np.matrix([[np.cos(k1[i]*L_vec[n]), -1j*np.sin(k1[i]*L_vec[n])/Z_vec[n],-1,0],[-1j*Z_vec[n]*np.sin(k1[i]*L_vec[n]) , np.cos(k1[i]*L_vec[n]), 0, -1]])
            TM[(nn*n +3):(nn*n +5) , (nn*n +2):(nn*n +6)]= element_matrix
            TM[(nn*n +1) : (nn*n +3) , (nn*n) : (nn*n + 4)]= conec_matrix

    solution_qp=np.linalg.solve(TM, qp_vec)
    solution_qp_freq.append(solution_qp)
    TM_all.append(TM)
    "aqui-pode-se escolher o nó onde quer-se pegar os dados de p e q"    
    q0_2.append(solution_qp[2]) #%% node numbers for q/p of branch 1 - constant for calculate the H_q/p functions between two diferent branches
    qL_2.append(solution_qp[14]) #%% b2=8/9 - b3=14/15 - b4=20/21 - node number for q/p branches out nodes
    p0_2.append(solution_qp[3])
    pL_2.append(solution_qp[15])
    
    Hp_TMM_2=20*np.log10(np.abs(pL_2)/np.abs(p0_2))
    Hq_TMM_2=20*np.log10((np.abs(qL_2)/S_vec[3])/(np.abs(q0_2)/S_vec[0]))
            
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in TM]))


#%% PLOTS
# for in line plots
#get_ipython().run_line_magic('matplotlib', 'inline')
#matplotlib qt - to show the figures in a new window
# get_ipython().run_line_magic('matplotlib', 'qt')
plt.rcParams.update({'font.size': 20})

fig = plt.figure(figsize=[12,8])
plt.subplot(211)
#plt.plot(f,Hp,'o',f,Hp_TMM_1,'-')
plt.plot(f,Hp_TMM_2,'-')
plt.ylabel('H$_{p,b3/b1}$ [Pa/Pa]')
#plt.legend(['H$_{p_{branch 3}/p_{branch 1}}$','TMM H$_{p_{branch 3}/p_{branch 1}}$'],loc='best')
plt.legend(['TMM H$_{p_{branch 3}/p_{branch 1}}$','H$_{p_{branch 3}/p_{branch 1}}$'],loc='best')
plt.subplot(212)
#plt.plot(f,Hu,'o',f,Hq_TMM_1,'-')
plt.plot(f,Hq_TMM_2,'-')
plt.xlabel('Frequency [Hz]')
plt.ylabel('H$_{u, b3/b1}$ [m/s / m/s]')
#plt.legend(['H$_{u_{branch 3}/u_{branch 1}}$','TMM H$_{u_{branch 3}/u_{branch 1}}$'],loc='best')
plt.legend(['TMM H$_{u_{branch 3}/u_{branch 1}}$'],loc='best')
plt.show()