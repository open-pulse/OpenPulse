import math
import scipy
import numpy as np
from scipy.sparse import csc_matrix, coo_matrix, linalg
from scipy.sparse.linalg import spsolve
from scipy.sparse.linalg import cgs
from scipy.sparse.linalg import LinearOperator, spilu
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
def sectcalc(do,di,nr,secoffset,pois):
    """
    Section Properties calculation
    """
    #
    #Geometry properties of cross-section
    ### Integration points ###
  
    Nint = 4
    #c = 1./np.sqrt(3.)
    c = np.sqrt(3.)/3.
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
    ###################################################################
    ################### SECTION MESH #### HOLLOW CIRCLE ###############
    ###################################################################
    #
    div = 2*nr
    nnodeface = 3*div
    ang = 360./div
    coordface = np.zeros((nnodeface,3))
    tt = 0
    for i in range(div):
        coordface[3*i + 0,0] = 3*i + 1
        coordface[3*i + 0,1] = (do/2.)*math.cos(math.radians(tt)) - secoffset[0]
        coordface[3*i + 0,2] = (do/2.)*math.sin(math.radians(tt)) - secoffset[1]
        coordface[3*i + 1,0] = 3*i + 2
        coordface[3*i + 1,1] = ((do+di)/4.)*math.cos(math.radians(tt)) - secoffset[0]
        coordface[3*i + 1,2] = ((do+di)/4.)*math.sin(math.radians(tt)) - secoffset[1]
        coordface[3*i + 2,0] = 3*i + 3
        coordface[3*i + 2,1] = (di/2.)*math.cos(math.radians(tt)) - secoffset[0]
        coordface[3*i + 2,2] = (di/2.)*math.sin(math.radians(tt)) - secoffset[1]
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
    NGL = len(coordface)
    ##################################################
    ####################################################################
    ####################### GEOMETRY PROPERTIES  #######################
    ####################################################################
    A = 0.
    I2 = 0.
    I3 = 0.
    I23 = 0.
    Q2 = 0.
    Q3 = 0.
    vI2el = np.zeros(nr)
    vI3el = np.zeros(nr)
    for el in range(nr):   #loop -> elements
        Ael = 0.
        I2el = 0.
        I3el = 0.
        I23el = 0.
        Q2el = 0.
        Q3el = 0.
        for p in range(Nint):   #loog -> integration points
            ksi = pint[p,0] 
            eta = pint[p,1]
            phi, dphi = shapesect(ksi,eta)
            #
            JAC = np.zeros((2,2))
            Y=0.
            Z=0.
            ii=0
            for i in range(9):
                ii = connectface[el,i+1] - 1
                JAC[0,0] = JAC[0,0] + coordface[ii,1]*dphi[0,i] #dxdksi
                JAC[0,1] = JAC[0,1] + coordface[ii,2]*dphi[0,i] #dydksi
                JAC[1,0] = JAC[1,0] + coordface[ii,1]*dphi[1,i] #dxdeta
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dydeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]        
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            Ael = Ael + detJAC*wint
            I2el = I2el + (Z**2.)*detJAC*wint
            I3el = I3el + (Y**2.)*detJAC*wint
            I23el = I23el + Y*Z*detJAC*wint
            Q2el = Q2el + Z*detJAC*wint
            Q3el = Q3el + Y*detJAC*wint
        vI2el[el] = I2el
        vI3el[el] = I3el
        A = A + Ael
        I2 = I2 + I2el
        I3 = I3 + I3el
        I23 = I23 + I23el
        Q2 = Q2 + Q2el
        Q3 = Q3 + Q3el
    ccg = 2.*(1.+pois)*(I2*I3 - (I23**2))
    yc = Q3/A
    zc = Q2/A
    ####################################################################
    ####################### SHEAR COEFFICIENTS #########################
    ####################################################################
    F2 = np.zeros(NGL)
    u2 = np.zeros(NGL)
    F3 = np.zeros(NGL)
    FT = np.zeros(NGL)
    row = []  # list holding row indices
    col = []  # list holding column indices
    data = [] 
    for el in range(nr):   #loop -> elements
        ke = np.zeros((9,9))
        pe2 = np.zeros(9)
        pe3 = np.zeros(9)
        pet = np.zeros(9)
        for p in range(Nint):   #loog -> integration points
            ksi = pint[p,0] 
            eta = pint[p,1]
            phi, dphi = shapesect(ksi,eta)
            #
            JAC = np.zeros((2,2))
            invJAC = np.zeros((2,2))
            Y=0.
            Z=0.
            ii=0
            for i in range(9):
                ii = connectface[el,i+1] - 1
                JAC[0,0] = JAC[0,0] + coordface[ii,1]*dphi[0,i] #dxdksi
                JAC[0,1] = JAC[0,1] + coordface[ii,2]*dphi[0,i] #dydksi
                JAC[1,0] = JAC[1,0] + coordface[ii,1]*dphi[1,i] #dxdeta
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dydeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]    
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            invJAC = np.linalg.inv(JAC)
            dphig = invJAC @ dphi
            ke = ke + (dphig.T @ dphig)*detJAC*wint
            r = Y**2. - Z**2.     
            q = 2.*Y*Z
            # d = [d1, d2] neq. d_ = [dy, dz] !!!!!
            d1 = I2*r - I23*q
            d2 = I23*r + I2*q
            h1 = -I23*r + I3*q
            h2 = -I3*r - I23*q
            d = np.array([d1,d2])
            h = np.array([h1,h2])
            vec = np.array([Z, -Y])
            #
            pe2 += ((pois/2.)*(dphig.T @ d) + 2.*(1+pois)*phi*(I2*Y - I23*Z))*detJAC*wint
            pe3 += ((pois/2.)*(dphig.T @ h) + 2.*(1+pois)*phi*(I3*Z - I23*Y))*detJAC*wint
            pet += (dphig.T @ vec)*detJAC*wint
            #
        node_ids = connectface[el,1:10]-1
        F2[node_ids] += pe2
        F3[node_ids] += pe3
        FT[node_ids] += pet
        rrr = np.repeat(node_ids, 9)
        ccc = np.tile(node_ids, 9)
        k = ke.flatten()
        row = np.hstack((row, rrr))
        col = np.hstack((col, ccc))
        data = np.hstack((data, k))
    #construct Lagrangian multiplier matrix:
    #Thanks @robbievanleeuwen !!!
    #column vector of ones
    row = np.hstack((row, range(NGL)))
    col = np.hstack((col, np.repeat(NGL, NGL)))
    data = np.hstack((data, np.repeat(1, NGL)))
    #row vector of ones
    row = np.hstack((row, np.repeat(NGL, NGL)))
    col = np.hstack((col, range(NGL)))
    data = np.hstack((data, np.repeat(1, NGL)))
    #zero in bottom right corner
    row = np.hstack((row, NGL))
    col = np.hstack((col, NGL))
    data = np.hstack((data, 0))
    
    K_lg = csc_matrix((data, (row, col)), shape=(NGL+1, NGL+1))

    Kd = K_lg.toarray()
    KK = np.linalg.pinv(Kd)

    u2 = KK @ np.append(F2, 0)
    u3 = KK @ np.append(F3, 0)
    #ut = KK @ np.append(FT, 0)
    
    #
    # norm_A = scipy.sparse.linalg.norm(K_lg)
    # norm_invA = scipy.sparse.linalg.norm(scipy.sparse.linalg.inv(K_lg))
    # cond = norm_A*norm_invA
    # #
    # u2 = spsolve(K_lg, np.append(F2, 0))
    # u3 = spsolve(K_lg, np.append(F3, 0))
    # ut = spsolve(K_lg, np.append(FT, 0))
    #
    #
    # err2 = u2[-1] / max(np.absolute(u2)) # if needed
    # err3 = u3[-1] / max(np.absolute(u3)) # if needed
    # errt = ut[-1] / max(np.absolute(ut)) # if needed
    PSI2 = u2[:-1]
    PSI3 = u3[:-1]
    #PSIT = ut[:-1]
    #
    #PSI2 = u2
    #PSI3 = u3
    #JX = np.dot(PSIT.T,FT) # if needed
    #JX = np.dot(ut.T,FT) # if needed
    J = I2 + I3  #- JX
    #
    ys = -(PSI3.T @ FT)/ccg
    zs = (PSI2.T @ FT)/ccg
    #
    ALP2 = 0.
    ALP3 = 0.
    ALP23 = 0.
    for el in range(nr):
        PSI2e = np.zeros(9)
        PSI3e = np.zeros(9)
        temp2=0.
        temp3=0.
        temp23=0.
        for p in range(Nint):   #loop -> integration points
            ksi = pint[p,0] 
            eta = pint[p,1]
            phi, dphi = shapesect(ksi,eta)
            #
            JAC = np.zeros((2,2))
            invJAC = np.zeros((2,2))
            Y=0.
            Z=0.
            ii=0
            for i in range(9):
                ii = connectface[el,i+1] - 1
                JAC[0,0] = JAC[0,0] + coordface[ii,1]*dphi[0,i] #dxdksi
                JAC[0,1] = JAC[0,1] + coordface[ii,2]*dphi[0,i] #dydksi
                JAC[1,0] = JAC[1,0] + coordface[ii,1]*dphi[1,i] #dxdeta
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dydeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]     
                PSI2e[i] = PSI2[ii]
                PSI3e[i] = PSI3[ii]
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            invJAC = np.linalg.inv(JAC)
            dphig = invJAC @ dphi
            r = (Y**2.) - (Z**2.)     
            q = 2.*Y*Z
            # d = [d1, d2] neq. d_ = [dy, dz] !!!!!
            dy = pois*((I2*r/2.) - (I23*q/2.))
            dz = pois*((I2*q/2.) + (I23*r/2.))
            #
            hy = pois*((I3*q/2.) - (I23*r/2.))
            hz = pois*(-(I23*q/2.) - (I3*r/2.))
            #
            d_ = np.array([dy,dz])
            h_ = np.array([hy,hz])
            dptemp = (dphig @ PSI2e.T) - d_.T
            hptemp = (dphig @ PSI3e.T) - h_.T
            temp2 = temp2 + (dptemp.T @ dptemp)*detJAC*wint
            temp3 = temp3 + (hptemp.T @ hptemp)*detJAC*wint
            temp23 = temp23 + (dptemp.T @ hptemp)*detJAC*wint
        ALP2 = ALP2 + temp2
        ALP3 = ALP3 + temp3
        ALP23 = ALP23 + temp23
    RES2 = (A/(ccg**2.))*(ALP2)
    RES3 = (A/(ccg**2.))*(ALP3)
    RES23 = (A/(ccg**2.))*(ALP23)

    return A, I2, I3, I23, J, Q2, Q3, RES2, RES3, RES23, yc, zc, ys, zs