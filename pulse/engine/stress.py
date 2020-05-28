import math
import numpy as np
#
# ARBITRARY TEST
#
freq = 100
alpha = 0.
beta = 1e-6
hyst = 0.
#exemplo: 3 elementos, 4 nos
nel=3
nnode=4
connect = np.array([1, 1, 2],[2, 2, 3],[3, 3, 4])
U = np.random.rand(24)
P = np.random.rand(4)

def stressel(el,connect,freq,alpha,beta,hyst,U,P):
    """
Created on Wed Nov 20 10:24:26 2019
@author: Olavo M. Silva
Mean-stress calculation, depending on internal forces and moments.
Calculation at the external surface.
!!!!WITHOUT STRESS INTENSIFICATION FACTORS!!!!

    """
    # Dados vindos de procedimento do elemento el:
    do = 0.03
    di = 0.01
    A = 1e-5
    I = 1e-9
    J = 2e-9
    p0 = 0.
    Ke = np.random.rand(12,12)
    Me = np.random.rand(12,12)
    connect = np.array([1, 1, 2],[2, 2, 3],[3, 3, 4])
    #
    # Calculando: ###################################
    w = 2.0*np.pi*freq
    KD = Ke - (w**2.0)*Me + 1j*w*(alpha*Me + beta*Ke) + 1j*hyst*Ke
    #
    Ue = np.zeros(12)
    Pe = np.zeros(2)
    n1 = connect[el-1,1]
    n2 = connect[el-1,2]
    Ue[0:6] = U[(6*n1-5)-1:(6*n1)] 
    Ue[6:12] = U[(6*n2-5)-1:(6*n2)]
    Pe[0] = P[n1]
    Pe[1] = P[n2]
    Pm = (Pe[0] + Pe[1])/2
    #
    Sh = (2*Pm*(di^2) - p0*(do^2 + di^2))/(do^2 - di^2) 
    #
    Fe = KD @ Ue
    # Fe = [FX1, FY1, FZ1, MX1, MY1, MZ1, FX2, FY2, FZ2, MX2, MY2, MZ2]
    #
    SX1 = (Fe[0]/A) + (np.sqrt(Fe[4]**2 + Fe[5]**2)*(do/2)/I) + Sh
    SX2 = (Fe[6]/A) + (np.sqrt(Fe[10]**2 + Fe[11]**2)*(do/2)/I) + Sh
    #
    SS1 = (Fe[3]*(do/2)/J) + 2*(np.sqrt(Fe[1]**2 + Fe[2]**2))/A
    SS2 = (Fe[9]*(do/2)/J) + 2*(np.sqrt(Fe[7]**2 + Fe[8]**2))/A

    return SX1, SS1, SX2, SS2
    #
SVEC = np.zeros(nnode,2)
a = np.zeros(nnode)
for el in range(nel):
    SX1, SS1, SX2, SS2 = stressel(el,connect,freq,alpha,beta,hyst,U,P)
    #
    n1 = connect[el-1,1]
    a[n1] = 1 #Aqui o 'a' seria um contado de quantas vezes o "nó 1" é chamado! Teria que implementar! Para a média nodal.
    n2 = connect[el-1,2]
    a[n2] = 1 #Aqui o 'a' seria um contado de quantas vezes o "nó 2" é chamado! Teria que implementar! Para a média nodal.
    #
    SVEC[n1,0:2] = SVEC[n1,0:2] + np.array([SX1, SS1])
    SVEC[n2,0:2] = SVEC[n1,0:2] + np.array([SX2, SS2])
for i in range(nel):
    SVEC[i,:]=SVEC[i,:]/a[i]
    #



    #        
   