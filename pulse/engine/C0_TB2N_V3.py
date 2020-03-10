#
import math
import numpy as np
import SECTION_GEOM as sec
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
def matrices(ee,E,pois,rho,do,di,le,nr):
    """
Created on Wed Jan 20 11:36:09 2019
@author: Olavo M. Silva
Implementation of element matrices based on pipe288 (Ansys) - Timoshenko Beam.
Ref.: Hughes, T.J.R., The Finite Element Method - Linear Static 
      and Dynamic Finite Element Analysis, Dover, 1987.
      Sec. 5.4
Notes:
- The kinematic conditions do not include warping.
- The elementary matrices are not rotated.
- Hughes2Ansys convention -> x1:x2, x2:x3, x3:x1, tet1:tet2, tet2:tet3, tet3:tet1.
- The shear correction factor ks used in the calculation of [Ke] was adapted from: 
E. Oñate, Structural Analysis with the Finite Element Method. Linear Statics.
Volume 2: Beams, Plates and Shells, CIMNE, 2013. Sec. 2.2.3.1.
This is different from what is used in Ansys, which performs a numerical integration 
over the cross-section to obtain ks. The cross-sectional area is considered as a sum 
of "N" divisions (default: N=8). However, the equation considered in this work is a 
very good approximation for thin and thick walled pipes. Ansys' ks converges to
analytical ks when N->inf.
- Ansys pipe288 element has some "tricks" that make hard to compare matrices entries.  
It can be made with N>100, but with some differences. 
    """
    #Material
    #pois = 0.
    #E = 210e9
    #pois = 0.3
    #G = E/(2.0*(1.0 + pois)) #Nao deletar!!!
    #lame parameters
    #lamb = pois*E/((1.0 + pois)*(1.0 -2.0*pois)) #Nao deletar!!!
    mu = E/(2.0*(1.0 + pois))
    #
    #Geometry properties of cross-section
    I1d = math.pi*(do**4 - di**4)/64.0   # I1 = I2
    I2d = math.pi*(do**4 - di**4)/64.0
    # J =  I1 + I2   
    # A =  math.pi*(do**2 - di**2)/4.0
    #do = 0.05
    #di = 0.04
    #nr = 64
    offset = np.array([0.003,0.00])
    A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12 = sec.sectcalc(do,di,nr,offset,0.)
    Jm = I1 + I2
    #
    #Mp = np.array([[mu, 0., 0.], [0., (1./RES1)*mu, (1./RES12)*mu], [0., (1./RES12)*mu, (1./RES2)*mu]])
    #Shear form factor
    # alpha = di/do
    # kk = alpha/(1+(alpha**2.))
    # ks =  6./(7. + 20.*(kk**2.)) 
    # As_ = ks*A  
    # Residual bending flexibility
    #As1 = 1./((1./(As_)) + ((le)**2.)/(12.*E*I1))
    #As2 = 1./((1./(As_)) + ((le)**2.)/(12.*E*I2))
    al1=(1/RES1)
    al2=(1/RES2)
    #al12 = (RES12)
    #ddt = al1*al2 - (al12**2.)
    al = np.min([al1,al2])
    # Residual bending flexibility
    #As1 = 1./((1./(As1)) + ((le)**2.)/(12.*E*I1))
    #As2 = 1./((1./(As2)) + ((le)**2.)/(12.*E*I2))
    #
    #Determinant of Jacobian (linear 1D trasform)
    detJac = le/2.0
    invJac = 1./detJac
    #s
    #Constitutive matrices (element with constant geometry along x-axis)
    #Dts = mu*np.array([[J,-Q1/2,Q2/2],[-Q1/2,al*A,0.],[Q2/2,0.,al*A]])
    Dts = mu*np.array([[J,-Q1,Q2],[-Q1,al*A,0.],[Q2,0.,al*A]]) 
    #Dab = E*np.array([[A,Q1,-Q2],[Q1,I1,-I12],[-Q2,-I12,I2]])
    #Dts = mu*np.array([[J, -(al2*Q1+al12*Q2)/ddt, (al12*Q1+al1*Q2)/ddt],[-Q1,al2*A/ddt,-al12*A/ddt],[Q2,-al12*A/ddt,al1*A/ddt] ])
    #Dts = mu*np.array([[J, -Q1, Q2],[-Q1,al2*A/dt,-al12*A/dt],[Q2,-al12*A/dt,al1*A/dt] ])
    #Dts = mu*np.array([[J,0.,0.],[0.,As1,0.],[0.,0.,As2]])
    #Dts = Mp @ Dts
    Dab = E*np.array([[A,Q1,-Q2],[Q1,I1,-I12],[-Q2,-I12,I2]])
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
        Kabe += (Bab.T @ Dab @ Bab)*detJac*wfact_k[i]
        Ktse += (Bts.T @ Dts @ Bts)*detJac*wfact_k[i]
        ##########
        #
    Ke = Kabe + Ktse
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
    return Ke, Me, Fe, A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12