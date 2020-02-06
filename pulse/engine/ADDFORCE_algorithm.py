#
import math
import numpy as np
"""
General algorithm for obtaining the additional load vector 'Fadd' when some degrees of
freedom 'R' are prescribed with zero or non-zero values, 'V'.

Matrices and vectors randomly produced to build the algorithm.

THE HARMONIC PROBLEM HAS NOT YET BEEN SOLVED.

"""
####################### 2-node 6-DOF/node ###########################
# Total Degrees of Freedom = 60 (10 nodes)
#
freq = 100 # Hz   #OBS.: THE ADDITIONAL LOAD VECTOR IS DEPENDENT ON THE FREQUENCY!
omega = 2.*np.pi*freq
#
#############
#
totaldof = 60
prescdof = 6
freedof = totaldof - prescdof
# Array with ALL Degrees of Freedom (Global, internal):
DOFS = np.arange(60) + 1
# Array with PRESCRIBED Degrees of Freedom (Global, internal):
R = np.array([1, 15, 19, 20, 24, 59 ])
# Array with FREE Degrees of Freedom (Global, internal):
D = np.delete(DOFS, [R-1] , None)
# Array with Values for Prescribed Degrees of Freedom:
V = np.array([0.01, 0., 0.002, -0.1, 0.25, 0.01])
#
# Global matrices eliminating prescribed dofs:
K = np.random.rand(54,54)
M = np.random.rand(54,54)
C = np.random.rand(54,54) #if damped problem
#
# Matrices of eliminated lines:
KR = np.random.rand(6,60)
MR = np.random.rand(6,60)
CR = np.random.rand(6,60) # if damped problem
#
Fadd = np.zeros((freedof))
FKadd = np.zeros((freedof))
FMadd = np.zeros((freedof))
FCadd = np.zeros((freedof))
# Additional load vector applied to free dofs
for i in range(freedof):  # 'i' runs over the free degrees of freedom
    j = D[i]-1
    FKadd[i] = FKadd[i] + KR[:,j].T @ V
    FMadd[i] = FMadd[i] + MR[:,j].T @ V
    FCadd[i] = FCadd[i] + CR[:,j].T @ V
#
Fadd = FKadd - (omega**2.0)*FMadd + omega*FCadd*1j
#
#OBS.: The matrices of eliminated lines 'KR', 'MR' and 'CR' will be used in ]
#      the postprocessing routines to calculate the reaction forces!!!