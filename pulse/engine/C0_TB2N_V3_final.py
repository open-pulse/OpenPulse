#
import math
import numpy as np
import SECTION_GEOM4 as sec
#######################################################
def shape(ksi):
    """
Created on Wed Nov 20 10:24:26 2019
@author: Olavo M. Silva
Linear shape functions and derivatives for 2-node topology

    """
    phi = np.array( [0.5*(1.0-ksi),0.5*(1.0+ksi)] )
    dphi = np.array( [-0.5, 0.5] )
    #       
    return phi, dphi
######################################################  
def matrices(ee,E,pois,rho,do,di,le,nr,offset):
    """
Created on Wed Mar 11 11:36:09 2019
@author: Olavo M. Silva
Implementation of element matrices based on pipe288 (Ansys) - Timoshenko Beam.
Ref.:1) Hughes, T.J.R., The Finite Element Method - Linear Static 
      and Dynamic Finite Element Analysis, Dover, 1987.
     2) Pilkey, W. D., Analysis and Design of Elastic Beam - Computational Methods, John Wiley & Son, 2002.
Notes:
- The kinematic conditions do not include warping.
- The elementary matrices are rotated.
- Hughes2Ansys convention -> x1:x2, x2:x3, x3:x1, tet1:tet2, tet2:tet3, tet3:tet1.
- The shear correction factor 'al' used in the calculation of [Ke] was adapted from Pilkey's book. 
It is performed numerical integration over the cross-section to obtain the section's constants and the
shear correction factors. The cross-sectional area is composed of 'N' elements (default for 
calculations: N=64). However, the simplified equation found in techinical literature is a very good 
approximation for thin and thick walled pipes. Ansys' ks converges to analytical 'al' when N->inf.
- Ansys pipe288 element has some "tricks" that make hard to compare matrices entries.  
It can be made with N>100, but with some differences. 
    """
    #Material
    mu = E/(2.0*(1.0 + pois))
    #
    #Geometry properties of cross-section
    # Shear + Torsion
    A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, yc, zc, ys, zs = sec.sectcalc(do,di,nr,offset,0.)
    vec = offset + np.array([yc,zc])
    _, I1p, I2p, _, Jp, _, _, RES1p, RES2p, _, yc_p, zc_p, ys_p, zs_p = sec.sectcalc(do,di,nr,vec,0.)
    #
    ###############################
    # Principal bending axis
    meas = np.linalg.norm(offset)
    if meas>0.:
        thetap = 0.5*np.arctan(2*I12/(I2-I1))
    else:
        thetap = 0.
    # Rotational part of transformation matrix
    lam = np.array([[1.,0.,0.],[0.,np.cos(thetap),np.sin(thetap)],[0.,-np.sin(thetap),np.cos(thetap)]])
    # Translational part of transformation matrix
    tam  = np.array([[0.,zc,-yc],[-zs,0.,0.],[ys,0.,0.]])
    II = np.identity(3)
    # Obtaining of transformation matrix O
    T = np.zeros((12, 12))
    R = np.zeros((12, 12))
    #
    T[0:3, 0:3]      = II
    T[3:6, 3:6]      = II
    T[6:9, 6:9]      = II
    T[9:12, 9:12]    = II
    T[0:3,3:6]       = tam
    T[6:9,9:12]      = tam
    #
    R[0:3, 0:3]      = lam
    R[3:6, 3:6]      = lam
    R[6:9, 6:9]      = lam
    R[9:12, 9:12]    = lam
    # Principal values of RES -> VRES  #if necessary in the future
    if meas>0.:
        gammap = 0.5*np.arctan(2*RES12/(RES2-RES1))
    else:
        gammap = 0.
    RES1x = 0.5*(RES1+RES2) + 0.5*(RES1+RES2)*np.cos(2*gammap) - RES12*np.sin(2*gammap)
    RES2x = RES1 + RES2 - RES1p
    #
    # Transformation based on the Principal Bending Axis
    O = R @ T
    #
    ##############################
    # Shear coefficiets
    al1 = 1./RES1p
    al2 = 1./RES2p
    # Geometry properties: principal bending axis
    Q1p = 0.
    Q2p = 0.
    I12p = 0.
    #Determinant of Jacobian (linear 1D trasform)
    detJac = le/2.0
    invJac = 1./detJac
    #
    #Constitutive matrices (element with constant geometry along x-axis)
    Dts = mu*np.array([[Jp,-Q1p,Q2p],[-Q1p,al1*A,0.],[Q2p,0.,al2*A]]) #Theoretical (common shear)
    Dab = E*np.array([[A,Q1p,-Q2p],[Q1p,I1p,-I12p],[-Q2p,-I12p,I2p]]) #Axial + Bending
    #
    #Inertial matrices (element with constant geometry along x-axis)
    Ggm = np.zeros((6,6))
    Ggm[0,0:6] = np.array([A, 0., 0., 0., Q1p, -Q2p]) 
    Ggm[1,0:6] = np.array([0., A, 0., -Q1p, 0., 0.])
    Ggm[2,0:6] = np.array([0., 0., A, Q2p, 0., 0.])
    Ggm[3,0:6] = np.array([0., -Q1p, Q2p, Jp, 0., 0.])
    Ggm[4,0:6] = np.array([Q1p, 0., 0., 0., I1p, -I12p])
    Ggm[5,0:6] = np.array([-Q2p, 0., 0., 0., -I12p, I2p])
    Ggm = rho*Ggm
    #
    #Preparing for numeric integration
    npel = 2
    ngln = 6
    nint_k = 1 #Stiffness: Reduced integration to avoid shear locking
    pint_k = np.array([0.])
    wfact_k = np.array([2.])
    nint_m = 2 #Mass: Full integration #Distributed external load: Full integration
    pint_m = np.array([-0.577350269189626,0.577350269189626])
    wfact_m = np.array([1.0,1.0])
    #
    Ke =  np.zeros((npel*ngln,npel*ngln))
    Kabe = np.zeros((npel*ngln,npel*ngln))
    Ktse = np.zeros((npel*ngln,npel*ngln))
    #
    Me = np.zeros((npel*ngln,npel*ngln))
    #
    N = np.zeros((ngln,2*ngln))
    NN = np.zeros((ngln,2*ngln)) #2-node element
    #
    ############################## STIFFNESS MATRIX ###################################
    for i in range(nint_k):
        pksi = pint_k[i]
        phi, dphi = shape(pksi)
        dphi = invJac*dphi
        #
        ##### Axial and Bending B-matrix #########
        Bab = np.zeros((3,12))
        Bab_n1 = np.zeros((3,6))
        Bab_n1[0,0:6] = np.array([dphi[0],0.,0.,0.,0.,0.]) 
        Bab_n1[1,0:6] = np.array([0.,0.,0.,0.,dphi[0],0.])
        Bab_n1[2,0:6] = np.array([0.,0.,0.,0.,0.,dphi[0]])
        Bab_n2 = np.zeros((3,6))
        Bab_n2[0,0:6] = np.array([dphi[1],0.,0.,0.,0.,0.]) 
        Bab_n2[1,0:6] = np.array([0.,0.,0.,0.,dphi[1],0.])
        Bab_n2[2,0:6] = np.array([0.,0.,0.,0.,0.,dphi[1]])
        Bab[0:3,0:6], Bab[0:3,6:12] = Bab_n1, Bab_n2 
        #       
        ##### Torsional and Shear B-matrix #####
        Bts = np.zeros((3,12))
        Bts_n1 = np.zeros((3,6))
        Bts_n1[0,0:6] = np.array([0., 0., 0., dphi[0], 0., 0.])
        Bts_n1[1,0:6] = np.array([0., dphi[0], 0., 0., 0., -phi[0]])
        Bts_n1[2,0:6] = np.array([0., 0., dphi[0], 0., phi[0], 0.])
        Bts_n2 = np.zeros((3,6))
        Bts_n2[0,0:6] = np.array([0., 0., 0., dphi[1], 0., 0.])
        Bts_n2[1,0:6] = np.array([0., dphi[1], 0., 0., 0., -phi[1]])
        Bts_n2[2,0:6] = np.array([0., 0., dphi[1], 0., phi[1], 0.])
        Bts[0:3,0:6], Bts[0:3,6:12] = Bts_n1, Bts_n2  
        ##### 
        Kabe += (Bab.T @ (Dab @ Bab))*detJac*wfact_k[i]
        Ktse += (Bts.T @ (Dts @ Bts))*detJac*wfact_k[i] 
        ##########
    Ke = Kabe + Ktse
    Ke = O.T @ Ke @ O
    #
    ############################## MASS MATRIX ########################################
    for i in range(nint_m):
        pksi = pint_m[i]
        phi, dphi = shape(pksi)
        #
        N[0:6,0:6]=phi[0]*np.identity(6)
        N[0:ngln,(ngln):(2*ngln)]=phi[1]*np.identity(6)
        ###########
        Me += (N.T @ Ggm @ N)*detJac*wfact_m[i]
    Me = O.T @ Me @ O
    #
    ############################## LOAD VECTOR ########################################
    #
    #Linear shape functions
    #Each element has information about EXTERNAL DISTRIBUTED LOAD along its length: put it in "element class"
    eload = np.array([[0.,-1000.,0.,0.,0.,0.]]) #[N/m, N/m, N/m, Nm/m, Nm/m, Nm/m]                
    #
    Fe = np.zeros((2*ngln,1))
    for i in range(nint_m):
        pksi = pint_m[i]
        phi, dphi = shape(pksi)
        NN[0:ngln,0:ngln]=phi[0]*np.identity(ngln)
        NN[0:ngln,(ngln):(2*ngln)]=phi[1]*np.identity(ngln)
        #
        Fe = Fe + (NN.T @ eload.T)*detJac*wfact_m[i]
        Fe = O.T @ Fe
    #
    #return Ke, Keb, Kes, A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12
    return Ke, Me ,A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, yc, zc, ys, zs, yc_p, zc_p, ys_p, zs_p, thetap
