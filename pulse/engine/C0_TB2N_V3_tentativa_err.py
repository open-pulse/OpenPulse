#
import math
import numpy as np
import SECTION_GEOM3 as sec
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
- The elementary matrices are not rotated.
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
    vec1 = np.array([offset[0],0.0])
    A, I1, I2, I12, Ja, Q1a, Q2a, RES1a, RES2a, RES12, ys, zs = sec.sectcalc(do,di,nr,vec1,0.)
    vec2 = np.array([0.0,offset[1]])
    A, I1, I2, I12, Jb, Q1b, Q2b, RES1b, RES2b, RES12, ys, zs = sec.sectcalc(do,di,nr,vec2,0.)
    # Axial + Bending
    A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, ys, zs = sec.sectcalc(do,di,nr,offset,0.)
    ddt = RES1*RES2 - (RES12**2.) #if needed
    # Torsional -> mass
    Jm = I1 + I2
    #
    ###############################
    yc = -0.005 #Q2/A
    zc = -0.00 #Q1/A
    ys = -0.005 #Q2/A
    zs = -0.00 #Q1/A
    meas = np.linalg.norm(offset)
    if meas>0.:
        thetap = 0.5*np.arctan(2*I12/(I2-I1))
    else:
        thetap = 0.
    thetap = -np.pi
    print(thetap)
    Iyp = 0.5*(I1+I2) + 0.5*(I1+I2)*np.cos(2*thetap) - I12*np.sin(2*thetap)
    Izp = I1 + I2 - Iyp

    lam = np.array([[1.,0.,0.],[0.,np.cos(thetap),np.sin(thetap)],[0.,-np.sin(thetap),np.cos(thetap)]])
    
    tam  = -np.array([[0.,-zc,yc],[zs,0.,0.],[-ys,0.,0.]])
    II = np.identity(3)

    T = np.zeros((12, 12))
    R = np.zeros((12, 12))

    T[0:3, 0:3]      = II
    T[3:6, 3:6]      = II
    T[6:9, 6:9]      = II
    T[9:12, 9:12]    = II
    T[0:3,3:6]       = tam
    T[6:9,9:12]      = tam

    R[0:3, 0:3]      = lam
    R[3:6, 3:6]      = lam
    R[6:9, 6:9]      = lam
    R[9:12, 9:12]    = lam

    ALPHA = np.array([[RES1,RES12],[RES12, RES2]])
    print(ALPHA)
    VRES,DUMP = np.linalg.eig(ALPHA)
    print(VRES)

    O = R @ T

    ##############################
    # Shear coefficiets - Treatment 
    ala = 0*np.min([1./RES1a,1./RES2a])
    alb = 0*np.min([1./RES1b,1./RES2b])
    #al1 = 1./VRES[0] #np.min([1./RES1a,1./RES1b])
    #al2 = 1./VRES[1] #np.min([1./RES2a,1./RES2b])
    Q1m = (Q1a + Q1b)/2
    Q2m = (Q2a + Q2b)/2
    al1 = 1./RES1
    al2 = 1./RES2
    al12 = 1./RES12
    al = np.min([1./RES1,1./RES2])
    # Residual bending flexibility
    #As1 = 1./((1./(As1)) + ((le)**2.)/(12.*E*I1)) #if needed
    #As2 = 1./((1./(As2)) + ((le)**2.)/(12.*E*I2)) #if needed
    #
    #Determinant of Jacobian (linear 1D trasform)
    detJac = le/2.0
    invJac = 1./detJac
    #s
    #Constitutive matrices (element with constant geometry along x-axis)
    Dts = mu*np.array([[J,-Q1,Q2],[-Q1,al1*A,0.],[Q2,0.,al2*A]]) #Theoretical (common shear)
    #Dts = mu*np.array([[J, -(RES1*Q1+RES12*Q2)/ddt, (RES12*Q1+RES1*Q2)/ddt],[-Q1,RES2*A/ddt,-RES12*A/ddt],[Q2,-RES12*A/ddt,RES1*A/ddt]]) #Theoretical, Pilkey shear -> asymmetric
    
    #Dts_a = mu*np.array([[J,-Q1a,Q2a],[-Q1a,ala*A,0.],[Q2a,0.,ala*A]]) #Torsion + shear (Ansys) - Part a
    #Dts_b = mu*np.array([[J,-Q1b,Q2b],[-Q1b,alb*A,0.],[Q2b,0.,alb*A]]) #Torsion + shear (Ansys) - Part b
    #Dab = E*np.array([[A,Q1,-Q2],[Q1,I1,-I12],[-Q2,-I12,I2]]) #Axial + Bending
    Dab = E*np.array([[A,Q1,-Q2],[Q1,I1,-I12],[-Q2,-I12,I2]]) #Axial + Bending

    #Dts = mu*np.array([[J,0,0],[0,al*A,0.],[0,0.,al*A]]) #Torsion + shear (Ansys) - Part a
    #Dab = E*np.array([[A,0,0],[0,Iyp,0],[0,0,Izp]]) #Axial + Bending

    #
    #Inertial matrices (element with constant geometry along x-axis)
    Ggm = np.zeros((6,6))
    Ggm[0,0:6] = np.array([A, 0., 0., 0., Q1, -Q2]) 
    Ggm[1,0:6] = np.array([0., A, 0., -Q1, 0., 0.])
    Ggm[2,0:6] = np.array([0., 0., A, Q2, 0., 0.])
    Ggm[3,0:6] = np.array([0., -Q1, Q2, Jm, 0., 0.])
    Ggm[4,0:6] = np.array([Q1, 0., 0., 0., I1, -I12])
    Ggm[5,0:6] = np.array([-Q2, 0., 0., 0., -I12, I2])
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
    Ktse_a = np.zeros((npel*ngln,npel*ngln))
    Ktse_b = np.zeros((npel*ngln,npel*ngln))
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
        #Ktse_a += (Bts.T @ (Dts_a @ Bts))*detJac*wfact_k[i]
        #Ktse_b += (Bts.T @ (Dts_b @ Bts))*detJac*wfact_k[i]
        Ktse += (Bts.T @ (Dts @ Bts))*detJac*wfact_k[i] 

        ##########
        #
    ##Keb = 1.*Kabe + 0.*(Ktse_a + Ktse_b)/2.
    ##Kes = 0.*Kabe + 1.*(Ktse_a + Ktse_b)/2.
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
    #
    #return Ke, Keb, Kes, A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12
    return Ke, yc,zc,A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, ys, zs