# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:32:54 2019

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

#%% Variables to insert

"Duct 1 Length [m]"
L1=2
"Duct 2 Length [m]"
L2=2
"Duct exterior diameter 1 [m]"
d1=0.154
"Duct exterior diameter 2 [m]"
d2=0.205
"Duct 1 thickness [m]"
e1=0.01
"Duct 2 thickness [m]"
e2=0.012
"number of ducts elements - duct 1"
nde1=10
"number of ducts elements - duct 2"
nde2=10

"Pressures and velocities apllied to node n"
pn1=100 # [Pa]

#%% variaveis fisicas

f=np.arange(1,251,1)
w=2*math.pi*np.transpose(f)
c=1149.4/3.281 #350.337 sond velocity in the gas m/s
rho_std=(0.0183)/0.00194 #standard density kg/m3
rho=0.0482/0.00194 #density kg/m3
rho_vec=np.array([rho_std,rho])
k1=(w/c)


qn1=0  # [m3/s] 
"source position - x times element size example- if xtps is 0 - pressure source is located at x=0, if is 1 the source is located at x= element size [m]"
xtps=0 
xtqs=0
#%% variaveis da geometria do duto

"Duct total length [m]"
L=L1+L2

"Total number of elements [m]"
nde=nde1+nde2

"Inner diameters and radius [m]"
d1i=d1-(2*e1)
d2i=d2-(2*e2)
r1i=d1i/2
r2i=d2i/2

"Cross-sections [m2]"
S1=math.pi*r1i**2
S2=math.pi*r2i**2

"Radius vector"
r_vec_1=r1i*np.ones((nde//2))
r_vec_2=r2i*np.ones((nde//2))
r_vec=np.concatenate((r_vec_1,r_vec_2),axis=0)

#%% definições de impedancia
"Fluid impedance"
Z0=rho_vec[1]*c
Z1=Z0/S1
Z2=Z0/S2

"End length correction"
deltaL=0.6133*r_vec[nde-1]

"Outer impedance tube 2"
Zrad_nf=Z0*(0.25*((k1*r_vec[nde-1])**2) + 1j*k1*deltaL)
"Inlet impedance tube 1"
Zin=0#+1j*1*10**6

#%% Elements and nodes number
"source position "
xps=xtps*(L//nde)
xqs=xtqs*(L//nde)
"Pressure source"
Pn1=pn1
"velocity volumetric source (u*S= m^3/S)"
Qn1=qn1
"Node pressure source - xtps+1 is the element number associated to the"
"source position (in times of the size element) - the source is located always in"
"the corresponding node at the begining of the element"
nnp=4*xtps + 2
"velocity node source"
nnq=4*xtqs + 1
"number of conections"
nce= nde+1
"number of total nodes"
conec_nod=2
element_nod=4 
nn=nde*element_nod + nce*conec_nod - (nde-1)*(element_nod//2)

#%% Matrix initialization
L_vec_1=(L1/nde1)*np.ones((nde1))
L_vec_2=(L2/nde2)*np.ones((nde2))
L_vec=np.concatenate((L_vec_1,L_vec_2),axis=0)
#L_vec=(L/nde)*np.ones((nde))

S_vec=math.pi*(r_vec**2)
Z_vec=((rho_vec[1]*c)*np.ones((nde)))/S_vec
conec_matrix=np.matrix([[1,0,-1,0],[0,1,0,-1]])
element_matrix=np.zeros((2,4),  dtype=complex)
TM=np.zeros((nn,nn), dtype=complex)
#qp_vec=np.array([])
qp_vec=np.zeros((nn,1),  dtype=complex)
solution_qp=[]
solution_qp_freq=[]
p0_2=[]
pL_2=[]
q0_2=[]
qL_2=[]
TM_all=[]
qp_vec[nnp]=-Pn1
qp_vec[nnq]=-qn1
#qp_vec=np.array([0 , -un1, -pn1, 0, 0,0, 0,0,0,0,0,0])
    
#%%Assembly process

for i in range(len(f)):
    TM[0,0:2]=[Zin , -1]
    TM[nn-1,nn-2:nn]=[-Zrad_nf[i]/S_vec[nde-1], -1]
    for n in range(nde):
        element_matrix=np.matrix([[np.cos(k1[i]*L_vec[n]), -1j*np.sin(k1[i]*L_vec[n])/Z_vec[n],-1,0],[-1j*Z_vec[n]*np.sin(k1[i]*L_vec[n]) , np.cos(k1[i]*L_vec[n]), 0, -1]])
        TM[(4*n +3):(4*n +5) , (4*n +2):(4*n +6)]= element_matrix
        for n2 in range(nde+1):
            TM[(4*n2 + 1) : (4*n2 +3), (n2 + 3*n2) : (4*n2 + 4)]= conec_matrix
    solution_qp=np.linalg.solve(TM, qp_vec)
    solution_qp_freq.append(solution_qp)
    TM_all.append(TM)
    "aqui-pode-se escolher o nó onde quer-se pegar os dados de p e q"    
    q0_2.append(solution_qp[2])
    qL_2.append(solution_qp[nn-4])
    p0_2.append(solution_qp[3])
    pL_2.append(solution_qp[nn-3])
    
    "Tranfer functions for the pressure and the velocity between x=0 and x=L"
    Hp_TMM_2=20*np.log10(np.abs(pL_2)/np.abs(p0_2))
    Hq_TMM_2=20*np.log10((np.abs(qL_2)/S2)/(np.abs(q0_2)/S1))
            
#print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in TM]))

#%% PLOTS
plt.rcParams.update({'font.size': 20})

#Analitical plots for pressure and velocity field expressions and TMM comparison (1 duct constant section)
plt.figure(1)
plt.subplot(211)
#plt.plot(f,p_1.real,'o',f,p_2.real,'*',f,np.real(p0),'-',f,np.real(pL),'--')
plt.plot(f,np.real(p0_2),'-',f,np.real(pL_2),'--')
plt.legend(['Real P(x=0)','Real P(x=L)','TMM Real P(x=0)','TMM Real P(x=L)'],loc='best')
plt.ylabel('Pressure [Pa]')
plt.subplot(212)
#plt.plot(f,u_1.real,'o',f,u_2.real,'*',f,np.real(q0)/S1,'-',f,np.real(qL)/S1,'--')
plt.plot(f,np.real(q0_2)/S1,'-',f,np.real(qL_2)/S2,'--')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Velocity [m/s]')
plt.legend(['Real u(x=0)','Real u(x=L)','TMM Real u(x=0)','TMM Real u(x=L)'],loc='best')
plt.show()

plt.figure(2)
plt.subplot(211)
#plt.plot(f,Hp,'o',f,Hp_TMM_1,'-')
plt.plot(f,Hp_TMM_2,'-')
plt.ylabel('H$_{21}$ [Pa/Pa]')
plt.legend(['H$_{p2/p1}$','TMM H$_{p2/p1}$'],loc='best')
plt.subplot(212)
#plt.plot(f,Hu,'o',f,Hq_TMM_1,'-')
plt.plot(f,Hq_TMM_2,'-')
plt.xlabel('Frequency [Hz]')
plt.ylabel('H$_{21}$ [m/s / m/s]')
plt.legend(['H$_{u2/u1}$','TMM H$_{u2/u1}$'],loc='best')
plt.show()