import numpy as np
from numpy.linalg import norm
from math import pi, sqrt, cos, sin, atan
from scipy.sparse import csc_matrix

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
    def __init__(self, D_external, division_number = 8, offset = [0, 0], element_type = '288b', **kwargs):
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
        self.element_type = element_type


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

    def shear_form_factor(self):
        """Shear form factor for a tube.
        Parameter
        ---------
        poisson_ratio : float
            Poisson's ratio [ ]"""
        alpha = self.D_internal / self.D_external
        # auxiliar = alpha / (1 + (alpha**2))
        return 6 / (7 + 20 * ((alpha / (1 + (alpha**2)))**2))
    
    def shear_area(self, element_length, young_modulus):
        shear_area = self.area() * self.shear_form_factor()
        return 1 / (( 1 / shear_area) + element_length**2/(12 * young_modulus * self.moment_area()))



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
    
    def mesh_coordinate(self, offset):
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
    
    def area_properties(self, **kwargs):
        '''
        Parameters: possion_ratio: float
                        Material propertie.
                    offset: [2,1] array
                        Deviation from the coordinate system axis Y and Z, respectively.
        Returns:    A: float
                        Cross section area.
                    I2: float
                        Cross section second moment of area relative to Y axis.
                    I3: float
                        Cross section second moment of area relative to Z axis.
                    I23: float
                        Cross section product moment of area relative to YZ axis.
                    J: float
                        Cross section second polar moment of area.
                    Q2: float
                        Cross section first moment of area relative to Y axis.
                    Q3: float
                        Cross section first moment of area relative to Z axis.

        '''

        offset = kwargs.get("offset", self.offset)
        coordinate = kwargs.get("coordinate", self.mesh_coordinate(offset))

        points, weigth = TubeCrossSection.gauss_quadracture2D()
        connectivity = self.mesh_connectivity()
        
        # Geometry properties
        A, I1, I2, I12, Q1, Q2 = 0, 0, 0, 0, 0, 0
        for el in range( self.division_number ): # Integration over each cross sections element
            for ksi, eta in points: # integration points
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y, Z = 0, 0
                for i, index in enumerate(connectivity[el,:]):
                    JAC[0,:] += coordinate[index, :] * dphi[0,i]
                    JAC[1,:] += coordinate[index, :] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                dA = detJAC * weigth
                A += dA
                I1 += Z**2 * dA
                I2 += Y**2 * dA
                I12 += Y * Z * dA
                Q1 += Z * dA
                Q2 += Y * dA
        J = I1 + I2
        # Centroid position
        y_centroid = Q2/A
        z_centroid = Q1/A

        return A, I1, I2, I12, J, Q1, Q2, y_centroid, z_centroid

    def shear_properties(self, poisson_ratio = 0, **kwargs):
        offset = self.offset
        coordinate = self.mesh_coordinate(offset)
        points, weigth = TubeCrossSection.gauss_quadracture2D()
        connectivity = self.mesh_connectivity()
        A, I1, I2, I12, J, Q1, Q2, y_centroid, z_centroid = self.area_properties()

        element_type = kwargs.get("element_type", self.element_type)

        if element_type == '288c':
            offset += np.array([y_centroid, z_centroid]) # for the 288c element, offset and its dependence need to be updated as below
            coordinate = self.mesh_coordinate(offset)
            A, I1, I2, I12, J, Q1, Q2, y_centroid, z_centroid = self.area_properties(offset = offset, coordinate = coordinate)

        # Shear Coefficients
        NGL = len(coordinate)
        F2 = np.zeros(NGL)
        F3 = np.zeros(NGL)
        FT = np.zeros(NGL)

        # Initializing  Lagrangian multiplier matrix construction
        row = np.r_[ np.arange(NGL), np.repeat(NGL, NGL)]  # list holding row indices
        col = np.r_[ np.repeat(NGL, NGL), np.arange(NGL)]  # list holding column indices
        data = np.r_[np.repeat(1, NGL), np.repeat(1, NGL)] 

        matr_aux2 =   np.array([[I1, -I12],[I12, I1]])
        matr_aux3 = - np.array([[I12, -I2],[I2, I12]])

        for el in range( self.division_number ): # Integration over each cross sections element
            ke =  0
            indeces = connectivity[el,:]
            for ksi, eta in points:   # integration points
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y, Z = 0, 0
                for i, index in enumerate(connectivity[el,:]):
                    JAC[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                    JAC[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                dA = detJAC * weigth
                invJAC = np.linalg.inv(JAC)
                dphig = invJAC @ dphi
                ke +=  dphig.T @ dphig * dA
                vect_aux = np.array([Y**2 - Z**2, 2*Y * Z])
                d = matr_aux2 @ vect_aux
                h = matr_aux3 @ vect_aux
                vec = np.array([Z, -Y])
                #
                F2[indeces] += ( poisson_ratio/2 * dphig.T @ d + 2*(1 + poisson_ratio)*phi*(I1*Y - I12*Z) ) * dA
                F3[indeces] += ( poisson_ratio/2 * dphig.T @ h + 2*(1 + poisson_ratio)*phi*(I2*Z - I12*Y) ) * dA
                FT[indeces] += (dphig.T @ vec) * dA
            # Appending new elements to the Lagrangian Mult Matrix
            row = np.r_[row, np.repeat(indeces, 9) ]
            col = np.r_[col, np.tile(indeces, 9) ]
            data = np.r_[data, ke.flatten() ]
        #
        K_lg = csc_matrix((data, (row, col)), shape=(NGL+1, NGL+1))
        # Pseudo inverse used to remedy numerical instability
        inv_K_lg = np.linalg.pinv(K_lg.toarray()) 

        u2 = inv_K_lg @ np.append(F2, 0)
        u3 = inv_K_lg @ np.append(F3, 0)
        PSI2 = u2[:-1]
        PSI3 = u3[:-1]
        #
        ALP1, ALP2, ALP12 = 0, 0, 0
        for el in range( self.division_number ): # Integration over each cross 
            PSI2e = np.zeros(9)
            PSI3e = np.zeros(9)
            for ksi, eta in points:   # integration points
                phi, dphi = TubeCrossSection.shape_function(ksi,eta)
                JAC = np.zeros((2,2))
                Y, Z = 0, 0
                for i, index in enumerate(connectivity[el,:]):
                    JAC[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                    JAC[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                    Y += coordinate[index, 0] * phi[i]
                    Z += coordinate[index, 1] * phi[i]
                    PSI2e[i] = PSI2[index]
                    PSI3e[i] = PSI3[index]
                detJAC = JAC[0,0]*JAC[1,1] - JAC[0,1]*JAC[1,0]
                dA = detJAC * weigth
                invJAC = np.linalg.inv(JAC)
                dphig = invJAC @ dphi
                vect_aux = np.array([Y**2 - Z**2, 2*Y * Z])
                d = poisson_ratio/2 * matr_aux2 @ vect_aux
                h = poisson_ratio/2 * matr_aux3 @ vect_aux
                dptemp = (dphig @ PSI2e) - d
                hptemp = (dphig @ PSI3e) - h
                ALP1 += dptemp @ dptemp * dA
                ALP2 += hptemp @ hptemp * dA
                ALP12 += dptemp @ hptemp * dA
        
        ccg = 2 * (1 + poisson_ratio) * (I1*I2 - (I12**2))
        RES1 = (A/(ccg**2))*(ALP1)
        RES2 = (A/(ccg**2))*(ALP2)
        RES12 = (A/(ccg**2))*(ALP12)

        # shear center
        y_shear = -(PSI3.T @ FT)/ccg
        z_shear = (PSI2.T @ FT)/ccg
        return A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, y_centroid, z_centroid, y_shear, z_shear

    @property
    def offset_rotation(self):
        # Principal bending axis
        _, I1, I2, I12, _, _, _, _, _, _, y_centroid, z_centroid, y_shear, z_shear = self.shear_properties( element_type = 'None')

        if norm(self.offset) > 0:
            angle = atan(2*I12/(I2-I1))/2
        else:
            angle = 0.
        # Rotational part of transformation matrix
        rotate = np.array([[ 1. ,      0.   ,    0.    ],
                           [ 0. ,cos(angle) ,sin(angle)],
                           [ 0. ,-sin(angle),cos(angle)]])
        # Translational part of transformation matrix
        translation = np.array([[   0.   ,z_centroid,-y_centroid],
                                [-z_shear,    0.    ,     0.    ],
                                [y_shear ,    0.    ,     0.    ]])
        T = np.eye(12)
        T[0:3,3:6]   = translation
        T[6:9,9:12]  = translation
        #
        R = np.zeros([12, 12])
        R[0:3, 0:3]  = rotate
        R[3:6, 3:6]  = rotate
        R[6:9, 6:9]  = rotate
        R[9:12, 9:12]= rotate
        #
        # Transformation based on the Principal Bending Axis
        O = R @ T

        return O

    def all_props(self, poisson_ratio = 0):
        A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, y_centroid, z_centroid, y_shear, z_shear = self.shear_properties(poisson_ratio = poisson_ratio)

        if self.element_type == '288c':
            O = self.offset_rotation
        else:
            O = []
        
        return A, I1, I2, I12, J, Q1, Q2, RES1, RES2, RES12, y_centroid, z_centroid, y_shear, z_shear, O


if __name__ == '__main__':

    poisson_ratio = 0.3   # Poisson ratio[-]
    D_external = 0.05   # External diameter [m]
    thickness  = 0.008 # Thickness [m]
    division_number = 64
    offset = [2e-3, 2e-3]
    cross_section_1 = TubeCrossSection(D_external, division_number = division_number , offset = offset , thickness = thickness)
    cross_section_1_properties = cross_section_1.shear_properties(poisson_ratio = 0 )

    for i in cross_section_1_properties:
        print(i)
