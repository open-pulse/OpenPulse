import numpy as np
from math import pi, sqrt, cos, sin
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

class TubeCrossSection:
    """ Tube cross section.
    Class used to create the tube's cross section and define its properties.
    External diameter D_external and internal diameter D_internal or thickness 
    should be provided.
    Parameters
    ----------
    D_external : float
        External diameter [m].
    D_internal : float
        Internal diameter [m].
    thickness : float
        thickness [m].
    Examples
    --------
    poisson_ratio : float
        Poisson's ratio [ ]
    Examples
    --------
    """
    def __init__(self, D_external, division_number = 8, offset = [0, 0], **kwargs):
        #TODO: review this warning
        assert (
            sum([1 if i in ["D_internal", "thickness"] else 0 for i in kwargs]) > 0
        ), "At least 1 arguments from D_internal and thickness should be provided."

        self.D_external = D_external
        self.D_internal = kwargs.get("D_internal", None)
        self.thickness = kwargs.get("thickness", None)
        self.index = kwargs.get("index", None)
        self.division_number = division_number
        self.offset = offset


        if self.D_internal is None:
            self.D_internal = self.D_external - 2 * self.thickness
        elif self.thickness is None:
            self.thickness = ( self.D_external - self.D_internal) / 2

    def area(self):
        """Cross section area [m**2]."""
        return (self.D_external**2 - self.D_internal**2) * pi / 4
        
    def moment_area(self):
        """Cross section second moment of area [m**4]."""
        return (self.D_external**4 - self.D_internal**4) * pi / 64
    
    def polar_moment_area(self):
        """Cross section second polar moment of area [m**4]."""
        return 2 * self.moment_area()

    def shear_form_factor(self,poisson_ratio):
        """Shear form factor for a tube.
        Parameter
        ---------
        poisson_ratio : float
            Poisson's ratio [ ]"""
        return 0.5

    @staticmethod
    def gauss_quadracture2D():
        c = 1/sqrt(3)
        points=np.zeros([4,2])
        points[0,0]=-c
        points[1,0]=c
        points[2,0]=c
        points[3,0]=-c

        points[0,1]=-c
        points[1,1]=-c
        points[2,1]=c
        points[3,1]=c
        weigth = 1
        return points, weigth


    @staticmethod
    def shape_function(ksi,eta):
        """
        - Quadratic shape funtions and its derivatives
        for calculation of section properties.
        - Q9 element.
        """

        # Shape functions
        phi = np.zeros(9) 
        phi[0] = (ksi**2 - ksi) * (eta**2 - eta) / 4
        phi[1] = (ksi**2 + ksi) * (eta**2 - eta) / 4
        phi[2] = (ksi**2 + ksi) * (eta**2 + eta) / 4
        phi[3] = (ksi**2 - ksi) * (eta**2 + eta) / 4
        phi[4] = (1 - ksi**2) * (eta**2 - eta)  / 2
        phi[5] = (ksi**2 + ksi) * (1 - eta**2)  / 2
        phi[6] = (1 - ksi**2.) * (eta**2 + eta)  / 2
        phi[7] = (ksi**2 - ksi) * (1 - eta**2)  / 2
        phi[8] = (1 - ksi**2) * (1 - eta**2)

        # Derivatives
        dphi=np.zeros([2, 9])
        # ksi Derivative
        dphi[0,0] = (2*ksi - 1) * (eta**2 - eta) / 4
        dphi[0,1] = (2*ksi + 1) * (eta**2 - eta) / 4 
        dphi[0,2] = (2*ksi + 1) * (eta**2 + eta) / 4
        dphi[0,3] = (2*ksi - 1) * (eta**2 + eta) / 4
        dphi[0,4] = -ksi * (eta**2 - eta)
        dphi[0,5] = (2*ksi + 1) * (1 - eta**2) / 2
        dphi[0,6] = -ksi * (eta**2 + eta)
        dphi[0,7] = (2*ksi - 1) * (1 - eta**2) / 2
        dphi[0,8] = -2*ksi * (1 - eta**2)
        # eta Derivative
        dphi[1,0] = (ksi**2 - ksi) * (2*eta - 1) / 4
        dphi[1,1] = (ksi**2 + ksi) * (2*eta - 1) / 4
        dphi[1,2] = (ksi**2 + ksi) * (2*eta + 1) / 4
        dphi[1,3] = (ksi**2 - ksi) * (2*eta + 1) / 4
        dphi[1,4] = (1 - ksi**2) * (2*eta - 1) / 2
        dphi[1,5] = (ksi**2 + ksi) * (-2*eta) / 2
        dphi[1,6] = (1 - ksi**2) * (2*eta + 1) / 2
        dphi[1,7] = (ksi**2 - ksi) * (-2*eta) / 2
        dphi[1,8] = (1 - ksi**2) * (-2*eta)
        return phi, dphi
    
    def mesh_coordinate(self, offset = [0, 0]):
        # coordinates of points on the face
        angular_increment = 2 * pi / (2 * self.division_number)
        theta = 0
        r_o = self.D_external / 2
        r_i = self.D_internal / 2

        coordinate = np.zeros([6 * self.division_number, 2])
        for i in range( 2 * self.division_number ):
            coordinate[3*i + 0, 0] = r_o * cos(theta) - offset[0]
            coordinate[3*i + 0, 1] = r_o * sin(theta) - offset[1]
            coordinate[3*i + 1, 0] = (r_o + r_i)/2 * cos(theta) - offset[0]
            coordinate[3*i + 1, 1] = (r_o + r_i)/2 * sin(theta) - offset[1]
            coordinate[3*i + 2, 0] = r_i * cos(theta) - offset[0]
            coordinate[3*i + 2, 1] = r_i * sin(theta) - offset[1]

            theta += angular_increment

        return coordinate
        
    def mesh_connectivity(self):
        connectivity = np.zeros([self.division_number, 9])
        aux = 0
        for i in range(self.division_number - 1):
            connectivity[i,:] = aux + np.array([8,2,0,6,5,1,3,7,4]) 
            aux += 6
        
        connectivity[i + 1,:] = [2,2+aux,aux,0,5+aux,1+aux,3+aux,1,4+aux]

        return connectivity.astype('int')
    
    def properties(self, poisson_ratio, offset):
        points, weigth = TubeCrossSection.gauss_quadracture2D()
        coordinate = self.mesh_coordinate(offset)
        connectivity = self.mesh_connectivity()
        
        # Geometry properties
        A, I2, I3, I23, Q2, Q3 = 0, 0, 0, 0, 0, 0
        for el in range( self.division_number ):
            Ael, I2el, I3el, I23el, Q2el, Q3el = 0, 0, 0, 0, 0, 0
            for p in points:
                ksi, eta  = p
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y, Z = 0, 0
                for i in range(9):
                    index = connectivity[el,i]
                    JAC[0,:] += coordinate[index, :] * dphi[0,i]
                    JAC[1,:] += coordinate[index, :] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                aux = detJAC * weigth
                Ael += aux
                I2el += Z**2 * aux
                I3el += Y**2 * aux
                I23el += Y * Z * aux
                Q2el += Z * aux
                Q3el += Y * aux
            A += Ael
            I2 += I2el
            I3 += I3el
            I23 += I23el
            Q2 += Q2el
            Q3 += Q3el
        ccg = 2 * (1 + poisson_ratio) * (I2*I3 - (I23**2))
        J = I2 + I3

        # Shear Coefficients
        NGL = len(coordinate)
        F2 = np.zeros(NGL)
        F3 = np.zeros(NGL)
        FT = np.zeros(NGL)
        row = []  # list holding row indices
        col = []  # list holding column indices
        data = []
        matr_aux2 =   np.array([[I2, -I23],[I23, I2]])
        matr_aux3 = - np.array([[I23, -I3],[I3, I23]])

        for el in range( self.division_number ):   #loop -> elements
            ke, pe2, pe3, pet =  0, 0, 0, 0
            for p in points:   #loog -> integration points
                ksi, eta  = p
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y=0
                Z=0
                for i in range(9):
                    index = connectivity[el,i]
                    JAC[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                    JAC[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                aux = detJAC * weigth
                invJAC = np.linalg.inv(JAC)
                dphig = invJAC @ dphi
                ke +=  dphig.T @ dphig * aux
                vect_aux = np.array([Y**2 - Z**2, 2*Y * Z])
                d = matr_aux2 @ vect_aux
                h = matr_aux3 @ vect_aux
                vec = np.array([Z, -Y])
                #
                pe2 += ( poisson_ratio/2 * dphig.T @ d + 2*(1 + poisson_ratio)*phi*(I2*Y - I23*Z) ) * aux
                pe3 += ( poisson_ratio/2 * dphig.T @ h + 2*(1 + poisson_ratio)*phi*(I3*Z - I23*Y) ) * aux
                pet += dphig.T @ vec * aux
                #
            indeces = connectivity[el,:]
            F2[indeces] += pe2
            F3[indeces] += pe3
            FT[indeces] += pet
            row = np.hstack((row, np.repeat(indeces, 9) ))
            col = np.hstack((col, np.tile(indeces, 9) ))
            data = np.hstack((data, ke.flatten() ))
        # construct Lagrangian multiplier matrix:
        # Thanks @robbievanleeuwen !!!
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
        #
        K_lg = csc_matrix((data, (row, col)), shape=(NGL+1, NGL+1))
        #
        u2 = spsolve(K_lg, np.append(F2, 0))
        u3 = spsolve(K_lg, np.append(F3, 0))
        PSI2 = u2[:-1]
        PSI3 = u3[:-1]
        #
        ALP2 = 0
        ALP3 = 0
        ALP23 = 0
        matr_aux4 = np.array([[-I23, I3],[I3, -I23]])
        for el in range( self.division_number ):   #loop -> elements
            PSI2e = np.zeros(9)
            PSI3e = np.zeros(9)
            temp2=0
            temp3=0
            temp23=0
            for p in points:   #loog -> integration points
                ksi, eta  = p
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y=0
                Z=0
                for i in range(9):
                    index = connectivity[el,i]
                    JAC[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                    JAC[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                    PSI2e[i] = PSI2[index]
                    PSI3e[i] = PSI3[index]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                aux = detJAC * weigth
                invJAC = np.linalg.inv(JAC)
                dphig = invJAC @ dphi
                vect_aux = np.array([Y**2 - Z**2, 2*Y * Z])
                d = poisson_ratio/2 * matr_aux2 @ vect_aux
                h = poisson_ratio/2 * matr_aux4 @ vect_aux
                dptemp = (dphig @ PSI2e.T) - d.T
                hptemp = (dphig @ PSI3e.T) - h.T
                temp2 += dptemp.T @ dptemp * aux
                temp3 += hptemp.T @ hptemp * aux
                temp23 += dptemp.T @ hptemp * aux
            ALP2 += temp2
            ALP3 += temp3
            ALP23 += temp23
        RES2 = (A/(ccg**2))*(ALP2)
        RES3 = (A/(ccg**2))*(ALP3)
        RES23 = (A/(ccg**2))*(ALP23)
        
        return A, I2, I3, I23, J, Q2, Q3, RES2, RES3, RES23

if __name__ == "__main__":
    D_external = 0.05   # External diameter [m]
    thickness  = 0.008 # Thickness [m]
    division_number = 64
    offset = [1e-3, 2e-3]
    poisson_ratio = 0.3
    cross_section_1 = TubeCrossSection(D_external, division_number = division_number , offset = offset , thickness = thickness) 
    A, I2, I3, I23, J, Q2, Q3, RES2, RES3, RES23 = cross_section_1.properties(poisson_ratio = poisson_ratio, offset = offset)

    print(RES2, RES3, RES23)