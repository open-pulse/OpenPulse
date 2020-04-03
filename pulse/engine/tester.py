import C0_TB2N_V3 as el
import numpy as np
#
do = 0.05
di = do - 2*0.008
nr = 64
E = 210e9
pois = 0.3
rho = 7860.
le = 0.01
offset = np.array([1e-3,2e-3])
#
ke,me,fe,A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12 = el.matrices(1,E,pois,rho,do,di,le,nr,offset)
