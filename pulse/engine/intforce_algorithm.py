#
import math
import numpy as np
    """
General algorithm for obtaining the additional load vector 'Fadd' when some degrees of
freedom 'R' are prescribed with non-zero values 'V'.

    """
####################### 2-node 6-DOF/node ###########################
# Total Degrees of Freedom = 60 (10 nodes)
#
freq = 100 # Hz   #OBS.: THE ADDITIONAL LOAD VECTOR IS DEPENDENT ON THE FREQUENCY!
omega = 2.*np.pi*freq
#
totaldof = 60
prescdof = 5
freedof = totaldof - prescdof
# Array with Prescribed Degrees of Freedom (Global, internal):
R = np.array([1, 19, 20, 24, 59 ])
# Array with Values for Prescribed Degrees of Freedom:
V = np.array([0.01, 0.002, -0.1, 0.25, 0.01])
#
# Global matrices eliminating constrained dofs:
K = np.random.rand(55,55)
M = np.random.rand(55,55)
C = np.random.rand(55,55) #if damped problem
#
# Matrices of eliminated lines:
KR = np.random.rand(5,55)
MR = np.random.rand(5,55)
CR = np.random.rand(5,55) # if damped problem
#
Fadd = np.zeros((freedof))
FKadd = np.zeros((freedof))
FMadd = np.zeros((freedof))
FCadd = np.zeros((freedof))
# Additional load vector applied to free dofs
for i in range(freedof):  # 'i' runs over the free degrees of freedom
    FKadd[i] = FKadd[i] + KR[:,i].T @ V
    FMadd[i] = FMadd[i] + MR[:,i].T @ V
    FCadd[i] = FCadd[i] + CR[:,i].T @ V
#
Fadd = FKadd - (omega**2.0)*FMadd + omega*FCadd*1j
#
#OBS.: The matrices of eliminated lines 'KR', 'MR' and 'CR' will be used in the postprocessing routine to
#      calculate the reaction forces!!!