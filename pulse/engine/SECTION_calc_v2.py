import math
import numpy as np
from scipy.sparse import csc_matrix, coo_matrix, linalg
from scipy.sparse.linalg import spsolve
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
    #####################################################
    ########### SECTION MESH #### HOLLOW CIRCLE #########
    ############### GEOMETRY PROPERTIES  ################
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
    NGL = len(coordface)
    #####################################
    #####################################
    #####################################
    A = 0.
    I2 = 0.
    I3 = 0.
    I23 = 0.
    vI2el = np.zeros(nr)
    vI3el = np.zeros(nr)
    for el in range(nr):   #loop -> elements
        Ael = 0.
        I2el = 0.
        I3el = 0.
        I23el = 0.
        #phi = np.zeros((9,1))
        #dphi=np.zeros((2,9))
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
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dxdeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]        
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            Ael = Ael + detJAC*wint
            I2el = I2el + (Z**2.)*detJAC*wint
            I3el = I3el + (Y**2.)*detJAC*wint
            I23el = I23el + Y*Z*detJAC*wint
        vI2el[el] = I2el
        vI3el[el] = I3el
        A = A + Ael
        I2 = I2 + I2el
        I3 = I3 + I3el
        I23 = I23 + I23el
    CSec = 1./(I2*I3)
    #########################################################
    #                                                       #
    #        !!!!!!NÂO DELETAR COMENTARIOS!!!!!!!           #
    #                                                       #
    # #######################################################
    # ########### SECTION MESH #### HOLLOW CIRCLE ###########
    # ####################### STRESS ########################
    # #
    # div = nr
    # nnodeface = 6*div
    # ang = 360./div
    # coordface = np.zeros((nnodeface,3))
    # tt = 0
    # for i in range(div):
    #     coordface[3*i + 0,0] = 3*i + 1
    #     coordface[3*i + 0,1] = (do/2.)*math.cos(math.radians(tt))
    #     coordface[3*i + 0,2] = (do/2.)*math.sin(math.radians(tt))
    #     coordface[3*i + 1,0] = 3*i + 2
    #     coordface[3*i + 1,1] = ((do+di)/4.)*math.cos(math.radians(tt))
    #     coordface[3*i + 1,2] = ((do+di)/4.)*math.sin(math.radians(tt))
    #     coordface[3*i + 2,0] = 3*i + 3
    #     coordface[3*i + 2,1] = (di/2.)*math.cos(math.radians(tt))
    #     coordface[3*i + 2,2] = (di/2.)*math.sin(math.radians(tt))
    #     tt = tt + ang
    # aux = 3*nr
    # tt = 0
    # for i in range(div-1):
    #     coordface[aux + 3*i + 0,0] = 3*i + aux + 1
    #     coordface[aux + 3*i + 0,1] = (coordface[3*i + 0,1] + coordface[3*(i+1) + 0,1])/2.
    #     coordface[aux + 3*i + 0,2] = (coordface[3*i + 0,2] + coordface[3*(i+1) + 0,2])/2.
    #     coordface[aux + 3*i + 1,0] = 3*i + aux + 2
    #     coordface[aux + 3*i + 1,1] = (coordface[3*i + 1,1] + coordface[3*(i+1) + 1,1])/2.
    #     coordface[aux + 3*i + 1,2] = (coordface[3*i + 1,2] + coordface[3*(i+1) + 1,2])/2.
    #     coordface[aux + 3*i + 2,0] = 3*i + aux + 3
    #     coordface[aux + 3*i + 2,1] = (coordface[3*i + 2,1] + coordface[3*(i+1) + 2,1])/2.
    #     coordface[aux + 3*i + 2,2] = (coordface[3*i + 2,2] + coordface[3*(i+1) + 2,2])/2.
    #     tt = tt + 3
    # aux2 = aux + tt
    # coordface[aux2+2,0] = aux2 + 3
    # coordface[aux2+2,1] = (coordface[aux - 1,1] + coordface[2,1])/2.
    # coordface[aux2+2,2] = (coordface[aux - 1,2] + coordface[2,2])/2.
    # coordface[aux2+1,0] = aux2 + 2
    # coordface[aux2+1,1] = (coordface[aux - 2,1] + coordface[1,1])/2.
    # coordface[aux2+1,2] = (coordface[aux - 2,2] + coordface[1,2])/2.
    # coordface[aux2+0,0] = aux2 + 1
    # coordface[aux2+0,1] = (coordface[aux - 3,1] + coordface[0,1])/2.
    # coordface[aux2+0,2] = (coordface[aux - 3,2] + coordface[0,2])/2.
    # #
    # connectface = np.zeros((nr,10))
    # connectface = connectface.astype(int)
    # aux = 0
    # for i in range(nr):
    #     connectface[i,0] = i + 1
    #     connectface[i,1:10] = [6+aux,3+aux,1+aux,4+aux,(3*nr+3)+aux,2+aux,(3*nr+1)+aux,5+aux,(3*nr+2)+aux] 
    #     if i == nr-1:
    #         connectface[i,1:10] = [3,3+aux,1+aux,1,(3*nr+3)+aux,2+aux,(3*nr+1)+aux,2,(3*nr+2)+aux]
    #     aux = aux + 3
    # NGL = len(coordface)
    ###################################################
    ###################################################
    #NGL = len(coordface)
    #K = np.zeros((NGL,NGL))
    #F = np.zeros((NGL,1))
    #PSI = np.zeros((NGL,1))
    #CAP = 0.
    #DDe = 0.
    #pe = np.zeros((9,nr))
    F = np.zeros(NGL)
    row = []  # list holding row indices
    col = []  # list holding column indices
    data = [] 
    for el in range(nr):   #loop -> elements
        ke = np.zeros((9,9))
        pe1 = np.zeros(9)
        #ue = np.zeros((9,1))
        #te = 0.
        #phi = np.zeros((1,9))
        #dphi=np.zeros((2,9))
        #de = np.zeros((2,1))
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
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dxdeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]        
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            invJAC = np.linalg.inv(JAC)
            dphig = np.dot(invJAC, dphi)
            ke = ke + np.dot(dphig.T, dphig)*detJAC*wint
            #r = Y**2. - Z**2.
            #q = 2.*Y*Z
            #de[0,0] = I2*r
            #de[1,0] = I2*q
            #pe1 = pe1 + np.matmul(dphig.T, de)*detJAC*wint
            pe1 = pe1 + phi*(2.*I2*Y)*detJAC*wint
            #te = te + np.matmul(de.T, de)*detJAC*wint
            # end loop Nint    
        # for i in range(9):
        #     ss = connectface[el,i+1] - 1
        #     for j in range(9):
        #         tt = connectface[el,j+1] - 1
        #         K[ss,tt] += ke[i,j]
        #     F[ss] += pe1[i]
        node_ids = connectface[el,1:10]-1
        F[node_ids] += pe1
        rrr = np.repeat(node_ids, 9)
        ccc = np.tile(node_ids, 9)
        k = ke.flatten()
        row = np.hstack((row, rrr))
        col = np.hstack((col, ccc))
        data = np.hstack((data, k))
    #K = coo_matrix((data, (row, col)), shape=(NGL, NGL))
    # construct Lagrangian multiplier matrix:
    # column vector of ones
    row = np.hstack((row, range(NGL)))
    col = np.hstack((col, np.repeat(NGL, NGL)))
    data = np.hstack((data, np.repeat(1, NGL)))

    # row vector of ones
    row = np.hstack((row, np.repeat(NGL, NGL)))
    col = np.hstack((col, range(NGL)))
    data = np.hstack((data, np.repeat(1, NGL)))

    # zero in bottom right corner
    row = np.hstack((row, NGL))
    col = np.hstack((col, NGL))
    data = np.hstack((data, 0))

    K_lg = coo_matrix((data, (row, col)), shape=(NGL+1, NGL+1))

    # K_lg_precond = linalg.LinearOperator(
    #             (NGL + 1, NGL + 1),
    #             linalg.spilu(K_lg).solve)
    #PSI = spsolve(k,F)
    #PSI = np.dot(np.linalg.inv(K),F)
    u = spsolve(K_lg, np.append(F, 0))
    err = u[-1] / max(np.absolute(u))
    PSI = u[:-1]
    
    ALP = 0.
    for el in range(nr):
        PSIe = np.zeros(9)
        temp=0.
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
                JAC[1,1] = JAC[1,1] + coordface[ii,2]*dphi[1,i] #dxdeta
                Y = Y + coordface[ii,1]*phi[i]
                Z = Z + coordface[ii,2]*phi[i]     
                PSIe[i] = PSI[ii]
            detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
            invJAC = np.linalg.inv(JAC)
            dphig = np.dot(invJAC, dphi)
            #temp = temp + np.dot(np.dot(PSIe.T, dphig.T), np.dot(dphig, PSIe))*detJAC*wint
            temp = temp + (np.dot(PSIe.T, dphig[0,:])**2. + np.dot(dphig[1,:], PSIe.T)**2.)*detJAC*wint
            #temp = temp + np.dot(phi,PSIe)*Y*detJAC*wint
        ALP = ALP + temp
    RES = A*ALP/((2*I2*I3)**2.)  
    #RES = (A*(CSec**2.)*I3/2.)*ALP

    return A,I2,I3,RES
   


            