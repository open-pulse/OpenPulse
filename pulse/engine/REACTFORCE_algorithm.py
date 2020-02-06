#
import math
import numpy as np
"""
General algorithm for obtaining the reaction forces 'Freact' when some degrees of
freedom 'R' are prescribed with zero or non-zero values, 'V'.
THIS IS A POST-PROCESSING PROCEDURE. It is assumed that the solution U is already obtained.

Matrices and vectors randomly produced to build the algorithm.

THE HARMONIC PROBLEM WAS SOLVED AND WE HAVE THE SOLUTION.

"""
####################### 2-node 6-DOF/node ###########################
# Total Degrees of Freedom = 60 (10 nodes)
#
freq = 100 # Hz   #OBS.: THE REACTION FORCES ARE DEPENDENT ON THE FREQUENCY!
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
#############
# Global matrices eliminating constrained dofs:
K = np.random.rand(54,54)
M = np.random.rand(54,54)
C = np.random.rand(54,54) #if damped problem
#
# Matrices of eliminated lines:
KR = np.random.rand(6,60)
MR = np.random.rand(6,60)
CR = np.random.rand(6,60) # if damped problem
#
# Here, the vector U_T_omega is obtained from R and D. However, the code
# must be implemented to "deliver" U_T_omega.
#
# Solution of harmonic problem:
U_omega = np.random.rand(freedof)  #U(omega)  --- U IS DEPENDENT ON OMEGA!
# Global U_T vector, with all degrees of freedom, including constrained ones
U_T_omega = np.zeros(totaldof)
for i in range(freedof):
    U_T_omega[D[i]-1]=U_omega[i]
for i in range(prescdof):
    U_T_omega[R[i]-1]=V[i]
#
Freact = np.zeros((prescdof))
FKreact = np.zeros((prescdof))
FMreact = np.zeros((prescdof))
FCreact = np.zeros((prescdof))
# Additional load vector applied to free dofs
for i in range(prescdof):  # 'i' runs over the prescribed degrees of freedom
    FKreact[i] = FKreact[i] + KR[i,:] @ U_T_omega
    FMreact[i] = FMreact[i] + MR[i,:] @ U_T_omega
    FCreact[i] = FCreact[i] + CR[i,:] @ U_T_omega
#
Freact = FKreact - (omega**2.0)*FMreact + omega*FCreact*1j
#
#OBS.: The matrices of eliminated lines 'KR', 'MR' and 'CR' will be used in 
#      the postprocessing routines in order to calculate the reaction forces!!!