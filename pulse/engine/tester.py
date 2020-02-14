import C0_TB2N as el
#
do = 0.15
di = 0.14
nr = 32
E = 210e9
pois = 0.3
rho = 7860.
le = 0.01
#
ke,me,fe = el.matrices(1,E,pois,rho,do,di,le,nr)
