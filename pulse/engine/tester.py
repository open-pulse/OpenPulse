import C0_TB2N as el
#
do = 0.09
di = 0.04
nr = 256
E = 210e9
pois = 0.3
rho = 7860.
le = 0.01
#
ke,me,fe,A, I1, I2, I12, J, RES1, RES2 = el.matrices(1,E,pois,rho,do,di,le,nr)
