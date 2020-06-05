select = 1

if select == 1:
    import numpy as np
    from math import pi, sqrt, cos, sin, atan
    from numpy.linalg import inv, pinv, norm
    from scipy.sparse import csc_matrix

    def gauss_quadrature2D():
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
        weight = 1
        return points, weight

    def shape_function(ksi,eta):
        """
        - Quadratic shape functions and its derivatives
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

    class CrossSection:
        def __init__(self, external_diameter, thickness, offset_y = 0, offset_z = 0, division_number = 64):
            self.external_diameter = external_diameter
            self.thickness = thickness
            self.offset = np.array([offset_y, offset_z])
            self.offset_virtual = None
            self.division_number = division_number

            self.external_radius = external_diameter/2
            self.internal_diameter = external_diameter - 2*thickness

            # Area properties
            self.area = 0
            self.first_moment_area_y = 0
            self.first_moment_area_z = 0
            self.second_moment_area_y = 0
            self.second_moment_area_z = 0
            self.second_moment_area_yz = 0
            self.polar_moment_area = 0
            self.y_centroid = 0
            self.z_centroid = 0

            # Shear properties
            self.y_shear = 0
            self.z_shear = 0
            self.res_y = 0
            self.res_z = 0
            self.res_yz = 0

            # Principal Bending Axis Rotation
            self.principal_axis = None

        @property
        def area_fluid(self):
            return (self.internal_diameter**2) * pi / 4

        def getExternalDiameter(self):
            return self.external_diameter
        
        def getExternalRadius(self):
            return self.external_radius

        def getThickness(self):
            return self.thickness

        def getInternalDiameter(self):
            return self.internal_diameter

        def mesh_connectivity(self):
            connectivity = np.zeros([self.division_number, 9], dtype = int)
            aux = 0
            for i in range(self.division_number - 1):
                connectivity[i,:] = aux + np.array([8,2,0,6,5,1,3,7,4]) 
                aux += 6
            
            connectivity[i + 1,:] = [2,2+aux,aux,0,5+aux,1+aux,3+aux,1,4+aux]

            return connectivity
        
        def mesh_coordinate(self):
            # coordinates of points on the face
            angular_increment = 2 * pi / (2 * self.division_number)
            theta = 0
            r_o = self.external_diameter / 2
            r_i = self.internal_diameter / 2

            if self.offset_virtual is None:
                offset = self.offset
            else:
                offset = self.offset_virtual # used in element_type = 'pipe_1'

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
        
        def area_properties(self):
            coordinate = self.mesh_coordinate()
            points, weight = gauss_quadrature2D()
            connectivity = self.mesh_connectivity()
            
            # Geometry properties
            A = Iy = Iz = Iyz = Qy = Qz = 0
            for el in range( self.division_number ): # Integration over each element
                for ksi, eta in points: # integration points
                    phi, dphi = shape_function(ksi,eta)
                    jacobian = np.zeros((2,2))
                    y = z = 0
                    for i, index in enumerate(connectivity[el,:]):
                        jacobian[0,:] += coordinate[index, :] * dphi[0,i]
                        jacobian[1,:] += coordinate[index, :] * dphi[1,i]
                        y += coordinate[index, 0] * phi[i]
                        z += coordinate[index, 1] * phi[i]
                    det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
                    dA = det_jacobian * weight
                    A += dA
                    Iy += z**2 * dA
                    Iz += y**2 * dA
                    Iyz += y * z * dA
                    Qy += z * dA
                    Qz += y * dA

            self.area = A
            self.first_moment_area_y = Qy
            self.first_moment_area_z = Qz
            self.second_moment_area_y = Iy
            self.second_moment_area_z = Iz
            self.second_moment_area_yz = Iyz
            self.polar_moment_area = Iy + Iz
            self.y_centroid = Qz/A
            self.z_centroid = Qy/A
        

        def shear_properties(self, poisson_ratio = 0, element_type = 'pipe_1'):
            coordinate = self.mesh_coordinate()
            points, weight = gauss_quadrature2D()
            connectivity = self.mesh_connectivity()
            

            if element_type == 'pipe_1':
                # for the pipe_1 element, offset and its dependence need to be updated as below
                self.offset_virtual = self.offset + np.array([self.y_centroid, self.z_centroid]) 
                coordinate = self.mesh_coordinate()
                self.area_properties()

            Iy = self.second_moment_area_y 
            Iz = self.second_moment_area_z
            Iyz = self.second_moment_area_yz

            # Shear Coefficients
            NGL = len(coordinate)
            Fy = np.zeros(NGL)
            Fz = np.zeros(NGL)
            FT = np.zeros(NGL)

            # Initializing  Lagrangian multiplier matrix construction
            row = np.r_[ np.arange(NGL), np.repeat(NGL, NGL)]  # list holding row indices
            col = np.r_[ np.repeat(NGL, NGL), np.arange(NGL)]  # list holding column indices
            data = np.r_[np.repeat(1, NGL), np.repeat(1, NGL)] 

            matrix_aux2 =   np.array([[Iy, -Iyz],[Iyz, Iy]])
            matrix_aux3 = - np.array([[Iyz, -Iz],[Iz, Iyz]])

            for el in range( self.division_number ): # Integration over each cross sections element
                ke =  0
                indexes = connectivity[el,:]
                for ksi, eta in points:   # integration points
                    phi, dphi = shape_function(ksi,eta)
                    jacobian = np.zeros((2,2))
                    y, z = 0, 0
                    for i, index in enumerate(connectivity[el,:]):
                        jacobian[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                        jacobian[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                        y += coordinate[index, 0] * phi[i]
                        z += coordinate[index, 1] * phi[i]
                    det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
                    dA = det_jacobian * weight
                    inv_jacobian = np.linalg.inv(jacobian)
                    dphig = inv_jacobian @ dphi
                    ke +=  dphig.T @ dphig * dA
                    vector_aux = np.array([y**2 - z**2, 2*y * z])
                    d = matrix_aux2 @ vector_aux
                    h = matrix_aux3 @ vector_aux
                    vec = np.array([z, -y])
                    #
                    Fy[indexes] += ( poisson_ratio/2 * dphig.T @ d + 2*(1 + poisson_ratio)*phi*(Iy*y - Iyz*z) ) * dA
                    Fz[indexes] += ( poisson_ratio/2 * dphig.T @ h + 2*(1 + poisson_ratio)*phi*(Iz*z - Iyz*y) ) * dA
                    FT[indexes] += (dphig.T @ vec) * dA
                # Appending new elements to the Lagrangian Mult Matrix
                row = np.r_[row, np.repeat(indexes, 9) ]
                col = np.r_[col, np.tile(indexes, 9) ]
                data = np.r_[data, ke.flatten() ]
            #
            K_lg = csc_matrix((data, (row, col)), shape=(NGL+1, NGL+1))
            # Pseudo inverse used to remedy numerical instability
            inv_K_lg = pinv(K_lg.toarray()) 

            u2 = inv_K_lg @ np.append(Fy, 0)
            u3 = inv_K_lg @ np.append(Fz, 0)
            psi_y = u2[:-1]
            psi_z = u3[:-1]
            #
            alpha_y = alpha_z = alpha_yz = 0
            for el in range( self.division_number ): # Integration over each cross 
                psi_ye = np.zeros(9)
                psi_ze = np.zeros(9)
                for ksi, eta in points:   # integration points
                    phi, dphi = shape_function(ksi,eta)
                    jacobian = np.zeros((2,2))
                    y, z = 0, 0
                    for i, index in enumerate(connectivity[el,:]):
                        jacobian[0,:] += coordinate[index, [0, 1]] * dphi[0,i]
                        jacobian[1,:] += coordinate[index, [0, 1]] * dphi[1,i]
                        y += coordinate[index, 0] * phi[i]
                        z += coordinate[index, 1] * phi[i]
                        psi_ye[i] = psi_y[index]
                        psi_ze[i] = psi_z[index]
                    det_jacobian = jacobian[0,0]*jacobian[1,1] - jacobian[0,1]*jacobian[1,0]
                    dA = det_jacobian * weight
                    inv_jacobian = inv(jacobian)
                    dphig = inv_jacobian @ dphi
                    vector_aux = np.array([y**2 - z**2, 2*y * z])
                    d = poisson_ratio/2 * matrix_aux2 @ vector_aux
                    h = poisson_ratio/2 * matrix_aux3 @ vector_aux
                    dptemp = (dphig @ psi_ye) - d
                    hptemp = (dphig @ psi_ze) - h
                    alpha_y += dptemp @ dptemp * dA
                    alpha_z += hptemp @ hptemp * dA
                    alpha_yz += dptemp @ hptemp * dA
            
            A = self.area
            ccg = 2 * (1 + poisson_ratio) * (Iy*Iz - (Iyz**2))
            self.res_y = (A/(ccg**2))*(alpha_y)
            self.res_z = (A/(ccg**2))*(alpha_z)
            self.res_yz = (A/(ccg**2))*(alpha_yz)

            # shear center
            self.y_shear = -(psi_z.T @ FT)/ccg
            self.z_shear = (psi_y.T @ FT)/ccg

        def offset_rotation(self, element_type = 'pipe_1'):
            if element_type is 'pipe_2':
                self.principal_axis = np.eye(12)
            else:
                y_c = self.y_centroid
                z_c = self.z_centroid
                y_s = self.y_shear
                z_s = self.z_shear
                if norm(self.offset) > 0:
                    Iy = self.second_moment_area_y 
                    Iz = self.second_moment_area_z
                    Iyz = self.second_moment_area_yz
                    angle = atan(2*Iyz/(Iz-Iy))/2
                    # Rotational part of transformation matrix
                    rotation = np.array([[ 1. ,      0.   ,    0.    ],
                                        [ 0. ,cos(angle) ,sin(angle)],
                                        [ 0. ,-sin(angle),cos(angle)]])
                    # Translational part of transformation matrix
                    translation = np.array([[ 0  , z_c,-y_c],
                                            [-z_s,  0 , 0  ],
                                            [y_s ,  0 , 0  ]])
                    T = np.eye(12)
                    T[0:3,3:6]   = translation
                    T[6:9,9:12]  = translation
                    #
                    R = np.zeros([12, 12])
                    R[0:3, 0:3]  = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = rotation
                    self.principal_axis = R @ T
                else:
                    translation = np.array([[ 0  , z_c,-y_c],
                                            [-z_s,  0 , 0  ],
                                            [y_s ,  0 , 0  ]])
                    T = np.eye(12)
                    T[0:3,3:6]   = translation
                    T[6:9,9:12]  = translation
                    self.principal_axis = T
        
        def update_properties(self, poisson_ratio = 0, element_type = 'pipe_1'):
            self.area_properties()

            if element_type == 'pipe_1':
                self.shear_properties(poisson_ratio = 0, element_type = None)
                self.offset_rotation(element_type = 'pipe_1')
                self.shear_properties(poisson_ratio = 0, element_type = element_type)
            else:
                self.shear_properties(poisson_ratio = poisson_ratio, element_type = element_type)

elif select == 2:
        
    from math import pi

    class CrossSection:
        def __init__(self, external_diameter, thickness):
            self.external_diameter = external_diameter
            self.thickness = thickness

            self.external_radius = external_diameter/2
            self.internal_diameter = external_diameter - 2*thickness

        @property
        def area_fluid(self):
            return (self.internal_diameter**2) * pi / 4

        @property
        def area(self):
            return ((self.external_diameter**2) - (self.internal_diameter**2)) * pi / 4
        
        @property
        def moment_area(self):
            return ((self.external_diameter**4) - (self.internal_diameter**4)) * pi / 64
        
        @property
        def polar_moment_area(self):
            return 2 * self.moment_area

        @property
        def shear_form_factor(self):
            alpha = self.internal_diameter / self.external_diameter
            auxiliar = alpha / (1 + alpha**2)
            return 6 / (7 + 20 * auxiliar**2)
        
        def shear_area(self, element_length, young_modulus):
            temp = self.area * self.shear_form_factor
            return 1 / (( 1 / temp) + (element_length**2 / (12 * young_modulus * self.moment_area)))

        def getExternalDiameter(self):
            return self.external_diameter
        
        def getExternalRadius(self):
            return self.external_radius

        def getThickness(self):
            return self.thickness

        def getInternalDiameter(self):
            return self.internal_diameter