#
import math
import numpy as np
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
def matrices(ee,E,pois,rho,do,di,le,eload):
    """
Created on Wed Jan 20 11:36:09 2019
@author: Olavo M. Silva
Implementation of element matrices based on pipe288 (Ansys) - Timoshenko Beam.
Ref.: Hughes, T.J.R., The Finite Element Method - Linear Static 
      and Dynamic Finite Element Analysis, Dover, 1987.
      Sec. 5.4
Notes:
- The kinematic conditions do not include warping, i.e, plane sections remain plane.
- The elementary matrices are not rotated.
- Hughes2Ansys convention -> x1:x2, x2:x3, x3:x1, tet1:tet2, tet2:tet3, tet3:tet1.
- The shear correction factor ks used in the calculation of [Ke] was adapted from: 
E. Oñate, Structural Analysis with the Finite Element Method. Linear Statics.
Volume 2: Beams, Plates and Shells, CIMNE, 2013. Sec. 2.2.3.1.
This is different from what is used in Ansys, which performs a numerical integration 
over the cross-section to obtain ks. The cross-sectional area is considered as a sum 
of "N" divisions (default: N=8). However, the equation considered in this work is a 
very good approximation for thin and thick walled pipes.
    """
    #Geometry properties of cross-section
    I1 = math.pi*(do**4 - di**4)/64.0   # I1 = I2
    I2 = math.pi*(do**4 - di**4)/64.0
    J =  I1 + I2      #pg 367 Hughes
    A = math.pi*(do**2 - di**2)/4.0
    #
    #Shear form factor
    alpha = di/do
    kk = alpha/(1+(alpha**2.))
    ks = 6./(7. + 20.*(kk**2.))
    As_ = ks*A  
    # Residual bending flexibility - Hughes, pg. 378 and ANSYS FACT
    As1 = 0.9971445*1./((1./(As_)) + ((le)**2.)/(12.*E*I1))
    As2 = 0.9971445*1./((1./(As_)) + ((le)**2.)/(12.*E*I2))
    #
    #Material
    #G = E/(2.0*(1.0 + pois)) #Nao deletar!!!
    #lame parameters
    #lamb = pois*E/((1.0 + pois)*(1.0 -2.0*pois)) #Nao deletar!!!
    mu = E/(2.0*(1.0 + pois))
    #
    #Determinant of Jacobian (linear 1D trasform)
    detJac = le/2.0
    invJac = 1./detJac
    #
    #Constitutive matrices (element with constant geometry along x-axis)
    Ds = np.array([[mu*As1, 0.],[0., mu*As2]])
    Db = np.array([[E*I1, 0.],[0., E*I2]])
    #
    #Inertial matrices (element with constant geometry along x-axis)
    Gt = np.array([[rho*A, 0., 0.], [0, rho*A, 0.], [0., 0., rho*A]])
    Gr = np.array([[rho*J, 0., 0.], [0, rho*I1, 0.], [0., 0., rho*I2]])
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
    Kbe = np.zeros((npel*ngln,npel*ngln))
    Kse = np.zeros((npel*ngln,npel*ngln))
    Kae = np.zeros((npel*ngln,npel*ngln))
    Kte = np.zeros((npel*ngln,npel*ngln))
    #
    Me = np.zeros((npel*ngln,npel*ngln))
    Mt = np.zeros((npel*ngln,npel*ngln))
    Mr = np.zeros((npel*ngln,npel*ngln))
    #
    NN = np.zeros((ngln,2*ngln)) #2-node element
    #
    ############################## STIFFNESS MATRIX ###################################
    for i in range(nint_k):
        pksi = pint_k[i]
        phi, dphi = shape(pksi)
        #
        dphi = invJac*dphi
        #
        ##### Bending B ######
        Bb = np.array([[0.,0.,0.,0.,dphi[0],0.,0.,0.,0.,0.,dphi[1],0.],[0.,0.,0.,0.,0.,dphi[0],0.,0.,0.,0.,0.,dphi[1]]]) 
        ##### Shear B #####
        Bs =  np.array([[0.,dphi[0],0.,0.,0.,-phi[0],0.,dphi[1],0.,0.,0.,-phi[1]],[0.,0.,dphi[0],0.,phi[0],0.,0.,0.,dphi[1],0.,phi[1],0.]])   
        ##### Axial B #####
        Ba = np.array([[dphi[0],0.,0.,0.,0.,0.,dphi[1],0.,0.,0.,0.,0.]])
        ##### Torsional B #####
        Bt = np.array([[0.,0.,0.,dphi[0],0.,0.,0.,0.,0.,dphi[1],0.,0.]])
        #       
        ########## 
        Kbe = Kbe + np.matmul(np.transpose(Bb),np.matmul(Db,Bb))*(detJac)*wfact_k[i]
        Kse = Kse + np.matmul(np.transpose(Bs),np.matmul(Ds,Bs))*(detJac)*wfact_k[i]
        Kae = Kae + E*A*np.matmul(np.transpose(Ba),Ba)*(detJac)*wfact_k[i]
        Kte = Kte + mu*J*np.matmul(np.transpose(Bt),Bt)*(detJac)*wfact_k[i]
        ##########
        #
    Ke = Kbe + Kse + Kae + Kte 
    #
    ############################## MASS MATRIX ########################################
    for i in range(nint_m):
        pksi = pint_m[i]
        phi, dphi = shape(pksi)
        #
        Nt = np.array([[phi[0],0.,0.,0.,0.,0.,phi[1],0.,0.,0.,0.,0.],[0.,phi[0],0.,0.,0.,0.,0.,phi[1],0.,0.,0.,0.],[0.,0.,phi[0],0.,0.,0.,0.,0.,phi[1],0.,0.,0.]])
        Nr = np.array([[0.,0.,0.,phi[0],0.,0.,0.,0.,0.,phi[1],0.,0.],[0.,0.,0.,0.,phi[0],0.,0.,0.,0.,0.,phi[1],0.],[0.,0.,0.,0.,0.,phi[0],0.,0.,0.,0.,0.,phi[1]]])
        #
        ###########
        Mt = Mt + np.matmul(np.transpose(Nt),np.matmul(Gt,Nt))*(detJac)*wfact_m[i]
        Mr = Mr + np.matmul(np.transpose(Nr),np.matmul(Gr,Nr))*(detJac)*wfact_m[i]
        ###########
    Me = Mt + Mr  
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
        Fe = Fe + np.matmul(np.transpose(NN),np.transpose(eload))*(detJac)*wfact_m[i]
    #
    return Ke, Me, Fe