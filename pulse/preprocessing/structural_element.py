
from math import pi, sqrt, sin, cos
import numpy as np

from pulse.preprocessing.node import Node, distance, DOF_PER_NODE_STRUCTURAL

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

decoupling_matrix = np.ones((DOF_PER_ELEMENT,DOF_PER_ELEMENT), dtype=int)

def gauss_quadracture(integration_points):
    if integration_points == 1:
        points = [0]
        weigths = [2]
    elif integration_points == 2:
        points = [-1/sqrt(3), 1/sqrt(3)]
        weigths = [1, 1]
    elif integration_points == 3:
        points = [-sqrt(3/5), 0, sqrt(3/5)]
        weigths = [5/9, 8/9, 5/9]
    else:
        raise TypeError('You must provide 1, 2, or 3 integration points')
    return points, weigths

def shape_function(ksi):
    phi = np.array([(1 - ksi)/2, (1 + ksi)/2])
    derivative_phi = np.array([-0.5, 0.5])
    return phi, derivative_phi

class StructuralElement:
    def __init__(self, first_node, last_node, index, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.index = index
        self.material = kwargs.get('material', None)
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_forces = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))
        self.element_type = kwargs.get('element_type', 'pipe_1')
        self.fluid = kwargs.get('fluid', None)
        self.adding_mass_effect = kwargs.get('adding_mass_effect', False)
        self.decoupling_matrix = kwargs.get('decoupling_matrix', decoupling_matrix)
        self.decoupling_info = kwargs.get('decoupling_info', None)

        self.caped_end = kwargs.get('caped_end', False)
        self.stress_intensification = kwargs.get('stress_intensification', True)

        self._Dab = None
        self._Bab = None
        self._Dts = None
        self._Bts = None
        self._rot = None

        self.stress = None
        self.internal_load = None

        self.rotation_matrix = self._rotation_matrix()
        self.transpose_rotation_matrix = self.rotation_matrix.T

    @property
    def length(self):
        return distance(self.first_node, self.last_node) 

    @property
    def global_dof(self):
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE_STRUCTURAL] = self.first_node.global_dof
        global_dof[DOF_PER_NODE_STRUCTURAL:] = self.last_node.global_dof
        return global_dof

    def global_matrix_indexes(self):
        ''' Returns two matrixes size 12 by 12, filled with rows indexes and column indexes. It may be usefull to construct the global matrix.'''
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows, cols

    def matrices_gcs(self):
        """ Element striffness and mass matrix in the global coordinate system."""
        R = self.rotation_matrix
        Rt = self.transpose_rotation_matrix
        if self.element_type in ['pipe_1','pipe_2']:
            stiffness = Rt @ self.stiffness_matrix_pipes() @ R
            mass = Rt @ self.mass_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            stiffness = Rt @ self.stiffness_matrix_beam() @ R
            mass = Rt @ self.mass_matrix_beam() @ R
        return stiffness, mass

    def stiffness_matrix_gcs(self):
        """ Element striffness matrix in the global coordinate system."""
        R = self.rotation_matrix
        Rt = self.transpose_rotation_matrix
        if self.element_type in ['pipe_1','pipe_2']:
            return Rt @ self.stiffness_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            return Rt @ self.stiffness_matrix_beam() @ R

    def mass_matrix_gcs(self):
        """ Element mass matrix in the global coordinate system."""
        R = self.rotation_matrix
        Rt = self.transpose_rotation_matrix
        if self.element_type in ['pipe_1','pipe_2']:
            return Rt @ self.mass_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            return Rt @ self.mass_matrix_beam() @ R
    
    def force_vector_gcs(self):
        Rt = self.transpose_rotation_matrix
        return Rt @ self.force_vector()

    def _rotation_matrix(self):
        """ Make the rotation from the element coordinate system to the global doordinate system."""
        # Rotation Matrix
        gamma = 0
        delta_x = self.last_node.x - self.first_node.x
        delta_y = self.last_node.y - self.first_node.y
        delta_z = self.last_node.z - self.first_node.z

        L_ = sqrt(delta_x**2 + delta_y**2)
        L  = sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        if L_ > 0.0001*L:
            sine = delta_y/L_
            cossine = delta_x/L_
        else:
            sine = 0
            cossine = 1

        C = np.zeros((3,3))
        if L_ != 0.:
            C[0,] = np.array([[cossine * L_ / L,
                            sine * L_ / L,
                            delta_z / L] ])

            C[1,] = np.array([[-cossine * delta_z * sin(gamma) / L - sine * cos(gamma),
                            -sine * delta_z * sin(gamma) / L + cossine * cos(gamma),
                            L_ * sin(gamma) / L] ])

            C[2,] = np.array([ [-cossine * delta_z * cos(gamma) / L + sine * sin(gamma),
                                -sine * delta_z * cos(gamma) / L - cossine * sin(gamma),
                                L_ * cos(gamma) / L] ])
        else:
            C[0,0] = 0.
            C[0,1] = 0.
            C[0,2] = delta_z/np.abs(delta_z)
            #
            C[1,0] = -(delta_z/np.abs(delta_z)) * sin(gamma)
            C[1,1] = cos(gamma)
            C[1,2] = 0.
            #
            C[2,0] = -(delta_z/np.abs(delta_z)) * cos(gamma)
            C[2,1] = -sin(gamma)
            C[2,2] = 0.

        R = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        R[0:3, 0:3] = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = C

        return R
    
    def stiffness_matrix_pipes(self):
        """ Element striffness matrix in the element coordinate system."""
        L = self.length

        E = self.material.young_modulus
        mu = self.material.mu_parameter

        # Area properties
        A = self.cross_section.area
        Iy = self.cross_section.second_moment_area_y
        Iz = self.cross_section.second_moment_area_z
        J = self.cross_section.polar_moment_area
        res_y = self.cross_section.res_y
        res_z = self.cross_section.res_z

        # Shear coefficiets
        aly = 1/res_y
        alz = 1/res_z
        
        if self.element_type == 'pipe_1':
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            Qy = self.cross_section.first_moment_area_y
            Qz = self.cross_section.first_moment_area_z
            Iyz = self.cross_section.second_moment_area_yz
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe_1 and pipe_2 element types are allowed.')
            pass
            
        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        # Constitutive matrices (element with constant geometry along x-axis)
        # Torsion and shear
        Dts = mu*np.array([[J,   -Qy,   Qz],
                        [-Qy, aly*A,  0  ],
                        [Qz,   0,  alz*A]])
        self._Dts = Dts
        # Axial and Bending
        Dab = E*np.array([[A,  Qy , -Qz],
                        [Qy, Iy , -Iyz],
                        [-Qz,-Iyz, Iz]])
        self._Dab = Dab

        ## Numerical integration by Gauss Quadracture
        integrations_points = 1
        points, weigths = gauss_quadracture( integrations_points )

        Kabe = 0
        Ktse = 0

        for point, weigth in zip( points, weigths ):

            # Shape function and its derivative
            phi, derivative_phi = shape_function( point )
            dphi = inv_jacob * derivative_phi

            # Axial and Bending B-matrix
            Bab = np.zeros([3, 12])
            Bab[[0,1,2],[0,4,5]] = dphi[0] # 1st node
            Bab[[0,1,2],[6,10,11]] = dphi[1] # 2nd node
            self._Bab = Bab

            # Torsional and Shear B-matrix
            Bts = np.zeros((3,12))
            Bts[[0,1,2],[3,1,2]] = dphi[0] # 1st node
            Bts[[1],[5]] = -phi[0]
            Bts[[2],[4]] = phi[0]
            Bts[[0,1,2],[9,7,8]] = dphi[1] # 2nd node
            Bts[[1],[11]] = -phi[1]
            Bts[[2],[10]] = phi[1]
            self._Bts = Bts

            Kabe += Bab.T @ Dab @ Bab * det_jacob * weigth
            Ktse += Bts.T @ Dts @ Bts * det_jacob * weigth
            
        Ke = Kabe + Ktse

        return principal_axis.T @ Ke @ principal_axis

    def mass_matrix_pipes(self):
        """ Element mass matrix in the element coordinate system."""
        L   = self.length
        rho = self.material.density

        # Area properties
        A = self.cross_section.area
        Iy = self.cross_section.second_moment_area_y
        Iz = self.cross_section.second_moment_area_z
        J = self.cross_section.polar_moment_area
        Ais = self.cross_section.area_insulation
        rho_insulation = self.cross_section.insulation_density
                    
        if self.fluid is not None and self.adding_mass_effect:
            rho_fluid = self.fluid.density
            Ai = self.cross_section.area_fluid
            Gfl = rho_fluid*np.array([[Ai, 0, 0],[0, Ai, 0],[0, 0, Ai]], dtype='float64') 
        else:
            Gfl = np.zeros((3,3), dtype='float64') 

        if self.element_type == 'pipe_1':
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            Qy = self.cross_section.first_moment_area_y
            Qz = self.cross_section.first_moment_area_z
            Iyz = self.cross_section.second_moment_area_yz
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe_1 and pipe_2 element types are allowed.')
            pass

        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        
        #Fluid/Insulation inertia effects
        Gis = rho_insulation*np.array([[Ais, 0, 0],[0, Ais, 0],[0, 0, Ais]], dtype='float64') 

        # Inertial matrices
        Ggm = np.zeros([6, 6])
        Ggm[np.diag_indices(6)] = np.array([A, A, A, J, Iy, Iz]) / 2
        Ggm[0, 4] = Qy
        Ggm[1, 3] = -Qy
        Ggm[2, 3] = Qz
        Ggm[0, 5] = -Qz
        Ggm[4, 5] = -Iyz
        Ggm = rho*( Ggm + Ggm.T )
        Ggm[0:3,0:3] = Ggm[0:3,0:3] + Gfl + Gis

        # Numerical integration by Gauss Quadracture
        integrations_points = 2
        points, weigths = gauss_quadracture( integrations_points )

        Me = 0
        N = np.zeros((DOF_PER_NODE_STRUCTURAL, 2 * DOF_PER_NODE_STRUCTURAL))
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL )
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function( point )

            N = np.c_[phi[0]*aux_eyes, phi[1]*aux_eyes] 

            Me += (N.T @ Ggm @ N) * det_jacob * weigth

        return principal_axis.T @ Me @ principal_axis
    
    def force_vector(self):
        ## Numerical integration by Gauss Quadracture
        L = self.length
        integrations_points = 2
        points, weigths = gauss_quadracture(integrations_points)

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        Fe = 0
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)

            N = np.c_[phi[0] * np.eye( DOF_PER_NODE_STRUCTURAL ), phi[1] * np.eye( DOF_PER_NODE_STRUCTURAL )] 

            Fe += (N.T @ self.loaded_forces.T) * det_jacobian * weigth
        
        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe_1 and pipe_2 element types are allowed.')
            pass
        
        return principal_axis.T @ Fe

    def force_vector_acoustic_gcs(self, frequencies, pressure_avg, pressure_external):

        A = self.cross_section.area
        Do = self.cross_section.external_diameter
        Di = self.cross_section.internal_diameter
        stress_axial = (pressure_avg * Di**2 - pressure_external * Do**2) / (Do**2 - Di**2)
        aux = np.zeros([DOF_PER_ELEMENT, 1])
        aux[0], aux[6] = 1, -1
        R = self.rotation_matrix

        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe_1 and pipe_2 element types are allowed.')
            pass

        if self.caped_end:
            caped_end = 1
        else:
            caped_end = 0

        aux = R.T @ principal_axis.T @ aux
        F_p = (caped_end - 2*self.material.poisson_ratio)* A * aux @ stress_axial.reshape([1,-1])

        return F_p

    ##
    #@staticmethod
    def symmetrize(self, a):
        """ Take a matrix a and symmetrize it."""
        return a + a.T - np.diag(a.diagonal())

    def stiffness_matrix_beam(self):
        """ Element striffness matrix in the element coordinate system."""

        # Element length
        L   = self.length

        # Material properities
        E   = self.material.young_modulus
        nu  = self.material.poisson_ratio
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area
        I_2 = self.cross_section.second_moment_area_y
        I_3 = self.cross_section.second_moment_area_z
        J   = self.cross_section._polar_moment_area()
 
        # alpha = self.get_shear_coefficient(self.cross_section.additional_section_info, self.material.poisson_ratio)
        # k_2 = alpha
        k_2 = 1

        # Others constitutive properties
        # I_3     = I_2
        k_3     = k_2

        # Auxiliar constantes
        Phi_12      = 24. * I_3 * (1 + nu) / (k_2 * A * L**2)
        Phi_13      = 24. * I_2 * (1 + nu) / (k_3 * A * L**2)
        beta_12_a   = E * I_3 / (1. + Phi_12)
        beta_13_a   = E * I_2 / (1. + Phi_13)
        beta_12_b   = (4. + Phi_12) * beta_12_a
        beta_13_b   = (4. + Phi_13) * beta_13_a
        beta_12_c   = (2. - Phi_12) * beta_12_a
        beta_13_c   = (2. - Phi_13) * beta_13_a

        
        ke = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        # stiffness matrix diagonal construction
        rows, cols = np.diag_indices(DOF_PER_ELEMENT)
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

        # stiffness matrix out diagonal construction
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

        # if decoupling_matrix is None:
        #     Ke = self.symmetrize(me)
        # else:
        #     Ke = self.symmetrize(me)*decoupling_matrix

        Ke = self.symmetrize(ke)*self.decoupling_matrix

        return Ke

    def mass_matrix_beam(self):
        """ Element mass matrix in the element coordinate system."""

        # Element length
        L   = self.length

        # Material properities
        rho = self.material.density
        nu = self.material.poisson_ratio
        E   = self.material.young_modulus
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area
        I_2 = self.cross_section.second_moment_area_y
        I_3 = self.cross_section.second_moment_area_z
        J   = self.cross_section._polar_moment_area()

        alpha = self.get_shear_coefficient(self.cross_section.additional_section_info, self.material.poisson_ratio)
        k_2 = alpha
        k_2 = 1
        
        # Others constitutive constants
        # I_3     = I_2
        J_p     = J
        k_3     = k_2

        # Auxiliar constantes
        # 1st group
        a_12 = 1. / (k_2 * A * G)
        a_13 = 1. / (k_3 * A * G)
        b_12 = 1. / (E * I_3)
        b_13 = 1. / (E * I_2)

        # 2nd group
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

        # 3rd group
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

        # 4th group
        gamma_12 = rho * L / (b_12 * L**2 + 12*a_12)**2
        gamma_13 = rho * L / (b_13 * L**2 + 12*a_13)**2


        me = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        # Mass matrix diagonal construction
        rows, cols = np.diag_indices(DOF_PER_ELEMENT)
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

        # Mass matrix out diagonal construction
        me[9 , 3] =  rho * J_p * L / 6
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

        # if decoupling_matrix is None:
        #     Me = self.symmetrize(me)
        # else:
        #     Me = self.symmetrize(me)*decoupling_matrix

        # if np.sum(self.decoupling_matrix) != 144:
        #     print(self.index)
        
        Me = self.symmetrize(me)*self.decoupling_matrix

        return Me

    def get_shear_coefficient(self, section_info, poisson):

        section_label = section_info[0]
        parameters = section_info[1]
 
        if section_label == "Rectangular section":

            b, h, b_in, _, _, _ = parameters

            m = (b_in)/h
            n = b_in/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + ((3 + poisson)*m + 3*m**2)*(10*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "Circular section":

            d_out, d_in, _, _ = parameters
            
            m = d_in/d_out
            numerator = 6*(1 + poisson)*((1 + m**2)**2)
            denominator = (7 + 6*poisson)*((1 + m**2)**2) + ((20 + 12*poisson)*m**2)
            shear_coefficient = numerator/denominator

        elif section_label == "C-section":

            h, w1, w2, w3, t1, _, t3, _, _, _ = parameters
            
            tf = (t1+t3)/2
            b = (w1+w3)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (m + m**2)*(30*n**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = 0.93*numerator/denominator

        elif section_label == "I-section":

            h, w1, w2, w3, t1, _, t3, _, _, _ = parameters
            
            tf = (t1+t3)/2
            b = (w1+w3)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (m + m**2)*(30*n**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "T-section":

            h, w1, w2, t1, _, _, _, _ = parameters
            tf, b = t1, w1
      
            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 4*m)**2)
            denominator = (12 + 96*m + 278*m**2 + 192*m**3) + poisson*(11 + 88*m + 248*m**2 + 216*m**3) + (m + m**2)*(30*n**2) + (4*m + 5*m**2 + m**3)*(10*poisson*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "Generic section":
            shear_coefficient = self.cross_section.shear_coefficient

        # print(section_label, parameters, shear_coefficient)

        return shear_coefficient