import numpy as np
import scipy
from scipy.linalg import eig
from math import pi, sqrt, sin, cos
from scipy import sparse

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


class Node(object):
    def __init__(self, coord, index):
        self.coord = coord
        self.index = index


class Material_isotropic(object):
    def __init__(self, rho, E, nu):
        self.rho    = rho
        self.E      = E
        self.nu     = nu
        self.G      = E / ( 2.0* (1 + nu) )


class Tube(object):
    def __init__(self, Do, t):
        self.Do = Do
        self.t  = t
        self.Di = Do - 2.*t
        self.A  = (Do**2 - self.Di**2) * pi / 4.
        self.I  = (Do**4 - self.Di**4) * pi / 64.
        self.J  = (Do**4 - self.Di**4) * pi / 32.


class Element(object):
    def __init__(self, node_a, node_b, index):
        self.node_a = node_a
        self.node_b = node_b
        self.le     = np.linalg.norm(node_a.coord - node_b.coord)
        self.index  = index


class Segment(object):
    def __init__(self,coord,connect,fixeddof,mat,tube):
        self.coord      = coord
        self.connect    = connect
        self.mat        = mat
        self.fixeddof   = fixeddof # Verificar mais tarde
        self.tube       = tube
        self.nnode      = coord.shape[0]
        self.AssembNd   = [ Node(coord[i,],i+1) for i in range(self.nnode ) ]
        self.ne         = connect.shape[0]
        self.AssembEl   = [ Element( self.AssembNd[ connect[i,1]-1 ], self.AssembNd[ connect[i,2]-1 ], connect[ i,0 ] )
                            for i in range(self.ne) ]


def Elementar_matrices(npel,ngln,e,mat,tube):

    L   = e.le
    # Material properities
    rho = mat.rho
    E   = mat.E
    nu  = mat.nu
    G   = mat.G

    # Tube cross section properties
    Do  = tube.Do
    Di  = tube.Di
    A   = tube.A
    I_2 = tube.I
    J   = tube.J

    # Other constants
    I_3     = I_2
    J_p     = J
    alpha   = Di / Do
    k_2     = 6. * (1 + nu) * (1 + alpha**2)**2 / ((7 + 6*nu) * (1 + alpha**2)**2  + (20 + 12*nu) * alpha**2)
    k_3     = k_2

    # Stiffness Matrix
    Phi_12      = 24. * I_3 * (1 + nu) / (k_2 * A * L**2)
    Phi_13      = 24. * I_2 * (1 + nu) / (k_3 * A * L**2)
    beta_12_a   = E * I_3 / (1. + Phi_12)
    beta_13_a   = E * I_2 / (1. + Phi_13)
    beta_12_b   = (4. + Phi_12) * beta_12_a
    beta_13_b   = (4. + Phi_13) * beta_13_a
    beta_12_c   = (2. - Phi_12) * beta_12_a
    beta_13_c   = (2. - Phi_13) * beta_13_a

    ke = np.zeros((npel*ngln, npel*ngln))

    # ke diagonal definition
    rows, cols = np.diag_indices(npel*ngln)
    ke[[rows], [cols]] = np.array([ E * A / L               ,
                                    12 * beta_12_a / L**3   ,
                                    12 * beta_13_a / L**3   ,
                                    G * J / L               ,
                                    beta_13_b / L           ,
                                    beta_12_b / L           ,
                                    E * A / L               ,
                                    12 * beta_12_a / L**3   ,
                                    12 * beta_13_a / L**3   ,
                                    G * J / L               ,
                                    beta_13_b / L           ,
                                    beta_12_b / L           ])

    ke[ 6   , 0 ] = - E * A / L
    ke[ 9   , 3 ] = - G * J / L
    ke[ 7   , 1 ] = - 12 * beta_12_a / L**3
    ke[ 11  , 5 ] =   beta_12_c / L
    ke[ 8   , 2 ] = - 12 * beta_13_a / L**3
    ke[ 10  , 4 ] =   beta_13_c / L

    ke[[5,11],[1,1]] =   6 * beta_12_a / L**2
    ke[[7,11],[5,7]] = - 6 * beta_12_a / L**2

    ke[[4,10],[2,2]] = - 6 * beta_13_a / L**2
    ke[[8,10],[4,8]] =   6 * beta_13_a / L**2

    # Mass Matrix
    #
    a_12 = 1. / (k_2 * A * G)
    a_13 = 1. / (k_3 * A * G)
    b_12 = 1. / (E * I_3)
    b_13 = 1. / (E * I_2)

    #
    a_12u_1 = 156 * b_12**2 * L**4 + 3528*a_12 * b_12 * L**2 + 20160 * a_12**2
    a_12u_2 = 2 * L * (11 * b_12**2 * L**4 + 231 * a_12 * b_12 * L**2 + 1260 * a_12**2)
    a_12u_3 = 54 * b_12**2 * L**4 + 1512 * a_12 * b_12 * L**2 + 10080 * a_12**2
    a_12u_4 = -L * (13 * b_12**2 * L**4 + 378 * a_12 * b_12 * L**2 + 2520 * a_12**2)
    a_12u_5 = L**2 * (4 * b_12**2 * L**4 + 84 * a_12 * b_12 * L**2 + 504 * a_12**2)
    a_12u_6 = -3 * L**2 * (b_12**2 * L**4 + 28 * a_12 * b_12 * L**2 + 168 * a_12**2)

    a_12t_1 = 36 * b_12**2 * L**2
    a_12t_2 = -3 * L * b_12 * (-b_12 * L**2 + 60 * a_12)
    a_12t_3 = 4 * b_12**2 * L**4 + 60 * a_12 * b_12 * L**2 + 1440 * a_12**2
    a_12t_4 = -b_12**2 * L**4 - 60 * a_12 * b_12 * L**2 + 720 * a_12**2

    #
    a_13u_1 = 156 * b_13**2 * L**4 + 3528*a_13 * b_13 * L**2 + 20160 * a_13**2
    a_13u_2 = -2 * L * (11 * b_13**2 * L**4 + 231 * a_13 * b_13 * L**2 + 1260 * a_13**2)
    a_13u_3 = 54 * b_13**2 * L**4 + 1512 * a_13 * b_13 * L**2 + 10080 * a_13**2
    a_13u_4 = L * (13 * b_13**2 * L**4 + 378 * a_13 * b_13 * L**2 + 2520 * a_13**2)
    a_13u_5 = L**2 * (4 * b_13**2 * L**4 + 84 * a_13 * b_13 * L**2 + 504 * a_13**2)
    a_13u_6 = -3 * L**2 * (b_13**2 * L**4 + 28 * a_13 * b_13 * L**2 + 168 * a_13**2)

    a_13t_1 = 36 * b_13**2 * L**2
    a_13t_2 = 3 * L * b_13 * (-b_13 * L**2 + 60 * a_13)
    a_13t_3 = 4 * b_13**2 * L**4 + 60 * a_13 * b_13 * L**2 + 1440 * a_13**2
    a_13t_4 = -b_13**2 * L**4 - 60 * a_13 * b_13 * L**2 + 720 * a_13**2

    #
    gamma_12 = rho * L / (b_12 * L**2 + 12*a_12)**2
    gamma_13 = rho * L / (b_13 * L**2 + 12*a_13)**2


    me = np.zeros((npel*ngln, npel*ngln))

    # ke diagonal definition
    rows, cols = np.diag_indices(npel*ngln)
    me[[rows], [cols]] = np.array([ rho * A * L / 3,
                                    gamma_12 * (A * a_12u_1 / 420 + I_3 * a_12t_1 / 30),
                                    gamma_13 * (A * a_13u_1 / 420 + I_2 * a_13t_1 / 30),
                                    rho * J_p * L / 3,
                                    gamma_13 * (A * a_13u_5 / 420 + I_2 * a_13t_3 / 30),
                                    gamma_12 * (A * a_12u_5 / 420 + I_3 * a_12t_3 / 30),
                                    rho * A * L / 3,
                                    gamma_12 * (A * a_12u_1 / 420 + I_3 * a_12t_1 / 30),
                                    gamma_13 * (A * a_13u_1 / 420 + I_2 * a_13t_1 / 30),
                                    rho * J_p * L / 3,
                                    gamma_13 * (A * a_13u_5 / 420 + I_2 * a_13t_3 / 30),
                                    gamma_12 * (A * a_12u_5 / 420 + I_3 * a_12t_3 / 30)])

    # Out diagonal elements

    me[9 , 3] =  rho * J_p * L * 6
    me[6 , 0] =  rho * A * L / 6
    me[5 , 1] =  gamma_12 * (A * a_12u_2 / 420 + I_3 * a_12t_2 / 30)
    me[11, 7] = -gamma_12 * (A * a_12u_2 / 420 + I_3 * a_12t_2 / 30)
    me[4 , 2] =  gamma_13 * (A * a_13u_2 / 420 + I_2 * a_13t_2 / 30)
    me[10, 8] = -gamma_13 * (A * a_13u_2 / 420 + I_2 * a_13t_2 / 30)
    me[7 , 1] =  gamma_12 * (A * a_12u_3 / 420 - I_3 * a_12t_1 / 30)
    me[8 , 2] =  gamma_13 * (A * a_13u_3 / 420 - I_2 * a_13t_1 / 30)
    me[11, 1] =  gamma_12 * (A * a_12u_4 / 420 + I_3 * a_12t_2 / 30)
    me[7 , 5] = -gamma_12 * (A * a_12u_4 / 420 + I_3 * a_12t_2 / 30)
    me[10, 2] =  gamma_13 * (A * a_13u_4 / 420 + I_2 * a_13t_2 / 30)
    me[8 , 4] = -gamma_13 * (A * a_13u_4 / 420 + I_2 * a_13t_2 / 30)
    me[11, 5] =  gamma_12 * (A * a_12u_6 / 420 + I_3 * a_12t_4 / 30)
    me[10, 4] =  gamma_13 * (A * a_13u_6 / 420 + I_2 * a_13t_4 / 30)

    # Rotation Matrix
    gamma = 0
    d1 = e.node_b.coord[0] - e.node_a.coord[0]
    d2 = e.node_b.coord[1] - e.node_a.coord[1]
    d3 = e.node_b.coord[2] - e.node_a.coord[2]

    L_ = sqrt(d1**2 + d2**2)
    L  = sqrt(d1**2 + d2**2 + d3**2)

    C = np.zeros((3,3))
    if L_ != 0.:
        C[0,] = np.array([ [d1 / L, d2 / L, d3 / L] ])

        C[1,] = np.array([ [-d1*d3 * sin(gamma) / (L_ * L) - d2 * cos(gamma) / L_,
                            -d2*d3 * sin(gamma) / (L_ * L) + d1 * cos(gamma) / L_,
                            L_ * sin(gamma) / L] ])

        C[2,] = np.array([ [-d1*d3 * cos(gamma) / (L_ * L) + d2 * sin(gamma) / L_,
                            -d2*d3 * cos(gamma) / (L_ * L) - d1 * sin(gamma) / L_,
                            L_ * cos(gamma) / L] ])
    else:
        C[0,0] = 0.
        C[0,1] = 0.
        C[0,2] = d3/np.abs(d3)
        #
        C[1,0] = -(d3/np.abs(d3)) * sin(gamma)
        C[1,1] = cos(gamma)
        C[1,2] = 0.
        #
        C[2,0] = -(d3/np.abs(d3)) * cos(gamma)
        C[2,1] = -sin(gamma)
        C[2,2] = 0.


    T_tild_e = np.zeros((npel*ngln, npel*ngln))

    T_tild_e[0:3, 0:3]      = C
    T_tild_e[3:6, 3:6]      = C
    T_tild_e[6:9, 6:9]      = C
    T_tild_e[9:12, 9:12]    = C

    return ke, me, T_tild_e


def assembly(Segm,npel,ngln):

    # Initiate
    nnode    = Segm.nnode
    connect  = Segm.connect
    AsEl     = Segm.AssembEl
    ne       = Segm.ne
    mat      = Segm.mat
    tube     = Segm.tube
    fixeddof = Segm.fixeddof

    # DOF connectivity matrix
    Connect_DOF = np.zeros((ne,npel*ngln)).astype(int)

    #
    N_DOF = 6*nnode
    K     = np.zeros((N_DOF,N_DOF))
    M     = np.zeros((N_DOF,N_DOF))

    # Global Matrix Assemble
    for e in AsEl:
        index = e.index - 1

        Ke, Me, T = Elementar_matrices(npel,ngln,e,mat,tube)
        Ke  = np.matmul(np.transpose(T),np.matmul(Ke,T))
        Me  = np.matmul(np.transpose(T),np.matmul(Me,T))

        for i in range(npel):
            for k in range(ngln):
                Connect_DOF[index,ngln*i + k] = ngln*(connect[index,i+1]-1) + k+1
                for p in range(int(ngln*i + k) + 1):
                    K[Connect_DOF[index,ngln*i + k]-1,Connect_DOF[index,p]-1]+=Ke[ngln*i + k,p]
                    M[Connect_DOF[index,ngln*i + k]-1,Connect_DOF[index,p]-1]+=Me[ngln*i + k,p]

    M = np.delete(M,fixeddof-1,axis=1)
    M = np.delete(M,fixeddof-1,axis=0)
    K = np.delete(K,fixeddof-1,axis=1)
    K = np.delete(K,fixeddof-1,axis=0)

    return K, M

def assembly(Segm,npel,ngln):

    # Initiate
    nnode    = Segm.nnode
    connect  = Segm.connect
    AsEl     = Segm.AssembEl
    ne       = Segm.ne
    mat      = Segm.mat
    tube     = Segm.tube
    fixeddof = Segm.fixeddof

    # DOF connectivity matrix
    Connect_DOF = np.zeros((ne,npel*ngln)).astype(int)

    #
    N_DOF = 6*nnode
    K     = sparse.lil_matrix((N_DOF,N_DOF))
    M     = sparse.lil_matrix((N_DOF,N_DOF))


    # Global Matrix Assemble
    for e in AsEl:
        index = e.index - 1

        Ke, Me, T = Elementar_matrices(npel,ngln,e,mat,tube)
        Ke  = np.matmul(np.transpose(T),np.matmul(Ke,T))
        Me  = np.matmul(np.transpose(T),np.matmul(Me,T))

        for i in range(npel):
            for k in range(ngln):
                Connect_DOF[index,ngln*i + k] = ngln*(connect[index,i+1]-1) + k+1
                for p in range(int(ngln*i + k) + 1):
                    K[Connect_DOF[index,ngln*i + k]-1,Connect_DOF[index,p]-1]+=Ke[ngln*i + k,p]
                    M[Connect_DOF[index,ngln*i + k]-1,Connect_DOF[index,p]-1]+=Me[ngln*i + k,p]

    # Como deletar linhas de matriz esparsa!!!
    M = np.delete(M,fixeddof-1,axis=1)
    M = np.delete(M,fixeddof-1,axis=0)
    K = np.delete(K,fixeddof-1,axis=1)
    K = np.delete(K,fixeddof-1,axis=0)

    return K.tocsr(), M.tocsr()


def symmetrize(a):
    return a + a.T - np.diag(a.diagonal())


# def modal_analysis(k,ngln,nnode,fixeddof,K,M):

#     eigvals,eigvects = eig(K, M)
#     eigvals=np.absolute(np.real(eigvals))
#     omega=np.sqrt(eigvals)
#     fn=omega/(2.*np.pi)
#     eigvects=np.real(eigvects)

#     idx = fn.argsort()[::1]
#     fn= fn[idx]
#     eigvects = eigvects[:,idx]
#     eigvects = eigvects.real

#     t=0
#     alldof = list(range(1,ngln*nnode+1))
#     eigvects_ = np.zeros((len(alldof),k))
#     for i in alldof:
#         if i in fixeddof:
#             eigvects_[i-1,:] = 0.*eigvects[0,0:k]
#         else:
#             t +=1
#             eigvects_[i-1,:] = eigvects[t-1,0:k]

#     return fn, eigvects_

def modal_analysis(k,ngln,nnode,fixeddof,K,M):

    eigvals,eigvects = eig(K, M)
    eigvals=np.absolute(np.real(eigvals))
    omega=np.sqrt(eigvals)
    fn=omega/(2.*np.pi)
    eigvects=np.real(eigvects)

    idx = fn.argsort()[::1]
    fn= fn[idx]
    eigvects = eigvects[:,idx]
    eigvects = eigvects.real

    t=0
    alldof = list(range(1,ngln*nnode+1))
    eigvects_ = np.zeros((len(alldof),k))
    for i in alldof:
        if i in fixeddof:
            eigvects_[i-1,:] = 0.*eigvects[0,0:k]
        else:
            t +=1
            eigvects_[i-1,:] = eigvects[t-1,0:k]

    return fn, eigvects_


def plot_mode(modo, fn, eigvects, coord, connectivity, scale):
    # Initialize
    le = 0.4
    fact = 0.5*le
    nnode = coord.shape[0]

    # Deformation
    x = np.array([ eigvects[0 + 6*i, modo-1] for i in range(nnode) ])
    y = np.array([ eigvects[1 + 6*i, modo-1] for i in range(nnode) ])
    z = np.array([ eigvects[2 + 6*i, modo-1] for i in range(nnode) ])
    
    # Scale Fator definition and normalization
    r = (x**2 + y**2 + z**2)**(1/2)
    fact = scale * le/ r.max()

    # Adding deformation
    coord_def        = np.empty_like(coord)
    coord_def[:,0]   = coord[:,0] + fact*x
    coord_def[:,1]   = coord[:,1] + fact*y
    coord_def[:,2]   = coord[:,2] + fact*z

    fig = plt.figure(figsize=(15,10))
    ax = fig.add_subplot(1,1,1,projection='3d')

    fontsize_label = 14
    fontsize_title = 18

    ax.set_title(('Forma modal - '+str(modo)+'º modo: '+str(round(fn[modo-1], 2))+' Hz'),fontsize=fontsize_title,fontweight='bold')
    ax.set_xlabel(('Posição x[m]'),fontsize=fontsize_label,fontweight='bold')
    ax.set_ylabel(('Posição y[m]'),fontsize=fontsize_label,fontweight='bold')
    ax.set_zlabel(('Posição z[m]'),fontsize=fontsize_label,fontweight='bold')
    plt.grid(axis='both')

    # Undeformed
    show_lines(ax, coord, connectivity,'blue')
    for point in coord:
        ax.scatter(*point, color='blue')
    # Deformed
    show_lines(ax, coord_def, connectivity,'red')
    for point in coord_def:
        ax.scatter(*point, color='red')
    
    plt.show()

def show_lines(ax, coordinates, connectivity, color):
    for start, end in connectivity:
        # [start - 1] é uma gambiarra temporária porque o arquivo de conectividade não tá indexado em zero.
        # funciona, só não é muito elegante 
        # outra opção seria colocar o 'nome' do vértice no arquivo
        start_x = coordinates[start-1][0]
        start_y = coordinates[start-1][1]
        start_z = coordinates[start-1][2]

        end_x = coordinates[end-1][0]
        end_y = coordinates[end-1][1]
        end_z = coordinates[end-1][2]

        ax.plot([start_x, end_x], [start_y, end_y], [start_z, end_z], color=color)

def show_points(coordinates):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for point in coordinates:
        ax.scatter(*point, color='red')

def get_conectivity(file):
    connect = []
    with open(file) as file:
        lines = file.readlines()
        for line in lines:
            print(line)
            pos, start, end, rest = line.split('.')
            pos = int(pos)
            start = int(start)
            end = int(end)
            connect.append((start, end))
    return connect


def example():
    # Finite Elements Parameters
    npel = 2
    ngln = 6

    # Material definition: steel
    E   = 210e9 #Pa
    nu  = 0.3   #[-]
    rho = 7860  #[kg/m^3]
    mat = Material_isotropic(rho,E,nu)

    # Section definition: 
    do      = 0.1
    t       = 0.005
    tube    = Tube(do, t)

    # Nodal coordenates
    coord = np.loadtxt('coord.dat')

    # Connectivity
    connect = np.loadtxt('connect.dat')
    connect = connect.astype(int)

    # Boundary conditions
    fixednodes = np.array([58,68])
    fixeddof = np.zeros(6*len(fixednodes))
    for i in range(6):
        fixeddof[i] = 6*(fixednodes[0]-1) + i+1
        fixeddof[i+6] = 6*(fixednodes[1]-1) + i+1
    fixeddof = fixeddof.astype(int)

    # Tube Segment  is totally define
    Segm = Segment(coord,connect,fixeddof,mat,tube)

    # Global Assembly
    K, M    = assembly(Segm,npel,ngln)
    K       = symmetrize(K)
    M       = symmetrize(M)

    # Modal Analysis - Full Matrix process
    k = 25
    nnode = Segm.nnode
    fn, eigvects = modal_analysis(k,ngln,nnode,fixeddof,K,M)

    # Plot
    modo = 23
    scale = 0.5
    connectivity = get_conectivity('connect.dat')

    plot_mode(modo, fn, eigvects, coord, connectivity, scale)

if __name__ == '__main__':
    example()
