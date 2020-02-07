import math
import numpy as np
#######################################################
def shapesect(ksi,eta):
    """
    - Quadratic shape funtions and its derivatives
    for calculation of section properties.
    - Q9 element.
    """
    ##### SHAPE FUNCTIONS ######################
    phi = np.zeros(9) 
    phi[0] = 0.25*(ksi**2. - ksi)*(eta**2. - eta) 
    phi[1] = 0.25*(ksi**2. + ksi)*(eta**2. - eta)
    phi[2] = 0.25*(ksi**2. + ksi)*(eta**2. + eta)
    phi[3] = 0.25*(ksi**2. - ksi)*(eta**2. + eta)
    phi[4] = 0.50*(1.0 - ksi**2.)*(eta**2. - eta)
    phi[5] = 0.50*(ksi**2. + ksi)*(1.0 - eta**2.)
    phi[6] = 0.50*(1.0 - ksi**2.)*(eta**2. + eta)
    phi[7] = 0.50*(ksi**2. - ksi)*(1.0 - eta**2.)
    phi[8] = (1.0 - ksi**2.)*(1.0 - eta**2)
    #
    #### DERIVATIVES ############################
    dphi=np.zeros((2,9))
    ## Dski ##  
    dphi[0,0] = 0.25*(2.*ksi - 1.0)*(eta**2. - eta) 
    dphi[0,1] = 0.25*(2.*ksi + 1.0)*(eta**2. - eta) 
    dphi[0,2] = 0.25*(2.*ksi + 1.0)*(eta**2. + eta)
    dphi[0,3] = 0.25*(2.*ksi - 1.0)*(eta**2. + eta)
    dphi[0,4] = 0.50*(-2.*ksi)*(eta**2. - eta)
    dphi[0,5] = 0.50*(2*ksi + 1.0)*(1.0 - eta**2.)
    dphi[0,6] = 0.50*(-2.*ksi)*(eta**2. + eta)
    dphi[0,7] = 0.50*(2.*ksi - 1.0)*(1.0 - eta**2.)       
    dphi[0,8] = (-2.*ksi)*(1.0 - eta**2)
    ## Deta ##
    dphi[1,0] = 0.25*(ksi**2. - ksi)*(2.*eta - 1.0)
    dphi[1,1] = 0.25*(ksi**2. + ksi)*(2.*eta - 1.0)
    dphi[1,2] = 0.25*(ksi**2. + ksi)*(2.*eta + 1.0)
    dphi[1,3] = 0.25*(ksi**2. - ksi)*(2.*eta + 1.0)
    dphi[1,4] = 0.50*(1.0 - ksi**2.)*(2*eta - 1.0)
    dphi[1,5] = 0.50*(ksi**2. + ksi)*(-2.*eta)
    dphi[1,6] = 0.50*(1.0 - ksi**2.)*(2.*eta + 1.0)
    dphi[1,7] = 0.50*(ksi**2. - ksi)*(-2.*eta)
    dphi[1,8] = (1.0 - ksi**2.)*(-2.*eta)
    #
    return phi, dphi
    #
def sectcalc(do,di,nr):
    """
    Section Properties calculation
    """
    do=0.05
    di=0.04
    nr=8
    #
    ### Integration points ###
    Nint = 4
    c = 1./np.sqrt(3.)
    pint=np.zeros((4,2))
    pint[0,0]=-c
    pint[0,1]=-c
    pint[1,0]=c
    pint[1,1]=-c
    pint[2,0]=c
    pint[2,1]=c
    pint[3,0]=-c
    pint[3,1]=c
    #
    wint = 1.
    #
    ########### SECTION MESH #### HOLLOW CIRCLE #######
    #
    div = 2*nr
    nnodeface = 3*div
    ang = 360./div
    coordface = np.zeros((nnodeface,3))
    tt = 0
    for i in range(div):
        coordface[3*i + 0,0] = 3*i + 0
        coordface[3*i + 0,1] = (do/2.)*math.cos(math.radians(tt))
        coordface[3*i + 0,2] = (do/2.)*math.sin(math.radians(tt))
        coordface[3*i + 1,0] = 3*i + 1
        coordface[3*i + 1,1] = ((do+di)/4.)*math.cos(math.radians(tt))
        coordface[3*i + 1,2] = ((do+di)/4.)*math.sin(math.radians(tt))
        coordface[3*i + 2,0] = 3*i + 2
        coordface[3*i + 2,1] = (di/2.)*math.cos(math.radians(tt))
        coordface[3*i + 2,2] = (di/2.)*math.sin(math.radians(tt))
        tt = tt + ang
    connectface = np.zeros((nr,10))
    connectface = connectface.astype(int)
    aux = 0
    for i in range(nr):
        connectface[i,0] = i + 1
        connectface[i,1:10] = [9+aux,3+aux,1+aux,7+aux,6+aux,2+aux,4+aux,8+aux,5+aux] 
        if i == nr-1:
            connectface[i,1:10] = [3,3+aux,1+aux,1,6+aux,2+aux,4+aux,2,5+aux]
        aux = aux + 6
    #####################################
    #####################################
    A = 0.
    I2 = 0.
    I3 = 0.
    for el in range(nr):   #loop -> elements
        Ael = 0.
        I2el = 0.
        I3el = 0.
        for p in range(Nint):   #loog -> integration points
            ksi = pint[p,0] 
            eta = pint[p,1]
            phi, dphi = shapesect(ksi,eta)
            #
            JAC = np.zeros((2,2))
            X=0.
            Y=0.
            ii=0
            for i in range(9):
                ii = connectface[el,i+1] -1
                JAC[0,0] = JAC[0,0] + coordface[ii,1]*dphi[0,i] #dxdksi
                JAC[0,1] = JAC[0,1] + coordface[ii,2]*dphi[0,i] #dydksi
                JAC[1,0] = JAC[1,0] + coordface[ii,1]*dphi[1,i] #dxdeta
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dxdeta
                X = X + coordface[ii,1]*phi[i]
                Y = Y + coordface[ii,2]*phi[i]
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            #
            Ael = Ael + detJAC*wint
            I2el = I2el + (Y**2.)*detJAC*wint
            I3el = I3el + (X**2.)*detJAC*wint
        A = A + Ael
        I2 = I2 + I2el
        I3 = I3 + I3el
    #

    
