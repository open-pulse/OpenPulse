import C0_TB2N_V4 as el
import numpy as np
#
x2=0.01/np.sqrt(3.) 
x1=0.0
y2=0.01/np.sqrt(3.) 
y1=0.0 
z2=0.01/np.sqrt(3.)
z1=0.0
#
gamma =0.
delta_x = x2-x1
delta_y = y2-y1
delta_z = z2-z1
#
do = 0.05
di = do - 2*0.008
nr = 64
E = 210e9
pois = 0.3
rho = 7860.
L  = np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
offset = np.array([0.005,0.005])
#
#Ke,Keb,Kes,A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12 = el.matrices(1,E,pois,rho,do,di,L,nr,offset)
Ke, Me , A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, yc, zc, ys, zs, yc_p, zc_p, ys_p, zs_p, thetap = el.matrices(1,E,pois,rho,do,di,L,nr,offset)

L_ = np.sqrt(delta_x**2 + delta_y**2)

if L_ > 0.0001*L:
    sine = delta_y/L_
    cossine = delta_x/L_
else:
    sine = 0.0
    cossine = 1.0

C = np.zeros((3,3))
C[0,] = np.array([ [cossine * L_ / L,
                    sine * L_ / L,
                    delta_z / L] ])

C[1,] = np.array([ [(-cossine * delta_z * np.sin(gamma) / L) - sine * np.cos(gamma),
                    (-sine * delta_z * np.sin(gamma) / L) + cossine * np.cos(gamma),
                    L_ * np.sin(gamma) / L] ])

C[2,] = np.array([ [(-cossine * delta_z * np.cos(gamma) / L) + sine * np.sin(gamma),
                    (-sine * delta_z * np.cos(gamma) / L) - cossine * np.sin(gamma),
                    L_ * np.cos(gamma) / L] ])

T_tild_e = np.zeros((12, 12))

T_tild_e[0:3, 0:3]      = C
T_tild_e[3:6, 3:6]      = C
T_tild_e[6:9, 6:9]      = C
T_tild_e[9:12, 9:12]    = C

Ke_r = T_tild_e.T @ Ke @ T_tild_e
Me_r = T_tild_e.T @ Me @ T_tild_e
#Keb_r = T_tild_e.T @ Keb @ T_tild_e
#Kes_r = T_tild_e.T @ Kes @ T_tild_e

Key5 = np.loadtxt(open("Kdense_ey_5mm_ez_5mm.csv", "r"), delimiter=",", skiprows=0)
Mey5 = np.loadtxt(open("Mdense_ey_5mm_ez_5mm.csv", "r"), delimiter=",", skiprows=0)

AA = np.divide((Ke_r - Key5),Key5)
AM = np.divide((Me_r - Mey5),Mey5)


