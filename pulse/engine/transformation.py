#
import math
import numpy as np
#######################################################
def transformation():

    x1,y1,z1,x2,y2,z2 = coordenadas_dos_dois_nós_de_acordo_com_connectividade
    theta = 0.0 #isso será zero, mas manter ele vivo no programa
    L = tamanho_do_elemento

    L_xy = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    d = 0.0001*L

    if L_xy > d:
        S1 = (y2 - y1)/L_xy
        else:
        S1 = 0.0
    
    S2 = (z2 - z1)/L
    S3 = np.sin(theta)
    
    if L_xy > d:
        C1 = (x2 - x1)/L_xy
        else:
        C1 = 1.0
    
    C2 = L_xy/L
    C3 = np.cos(theta)

    T = np.array[[C1*C2,S1*C2,S2], [(-C1*S2*S3-S1*C3),(-S1*S2*S3+C1*C3),S3*C2],[(-C1*S2*C3+S1*S3),(-S1*S2*C3-C1*S3),C3*C2]]

    TR = [[T,0,0,0],[0,T,0,0],[0,0,T,0],[0,0,0,T]]  #Fiz um esquema. Seria preencher uma matriz zero 12x12 com o T
                                                    #na diagonal, como se fosse uma pseudo 4x4, jogando as T 3x3 nos
                                                    #elementos da diagonal
                                