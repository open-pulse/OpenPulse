from math import pi, sqrt, sin, cos
import numpy as np

from pulse.preprocessing.node import Node, distance, DOF_PER_NODE_STRUCTURAL

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


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


class Element:
    def __init__(self, first_node, last_node, **kwargs):
        self.first_node = first_node
        self.last_node = last_node
        self.material = kwargs.get('material', None)
        self.cross_section = kwargs.get('cross_section', None)
        self.loaded_forces = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))
        self.element_type = kwargs.get('element_type', 'pipe1')

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
        R = self.rotation_matrix()
        Rt = R.T
        stiffness = Rt @ self.stiffness_matrix() @ R
        mass = Rt @ self.mass_matrix() @ R
        return stiffness, mass

    def stiffness_matrix_gcs(self):
        """ Element striffness matrix in the global coordinate system."""
        R = self.rotation_matrix()
        return R.T @ self.stiffness_matrix() @ R

    def mass_matrix_gcs(self):
        """ Element mass matrix in the global coordinate system."""
        R = self.rotation_matrix()
        return R.T @ self.mass_matrix() @ R
    
    def force_vector_gcs(self):
        R = self.rotation_matrix()
        return R.T @ self.force_vector()

    def rotation_matrix(self):
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
    
    def stiffness_matrix(self):
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
        
        if self.element_type == 'pipe1':
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe2':
            Qy = self.cross_section.first_moment_area_y
            Qz = self.cross_section.first_moment_area_z
            Iyz = self.cross_section.second_moment_area_yz
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe1 and pipe2 element types are allowed.')
            pass
            
        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        # Constitutive matrices (element with constant geometry along x-axis)
        # Torsion and shear
        Dts = mu*np.array([[J,   -Qy,   Qz],
                           [-Qy, aly*A,  0  ],
                           [Qz,   0,  alz*A]])
        # Axial and Bending
        Dab = E*np.array([[A,  Qy , -Qz],
                          [Qy, Iy , -Iyz],
                          [-Qz,-Iyz, Iz]])

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

            # Torsional and Shear B-matrix
            Bts = np.zeros((3,12))
            Bts[[0,1,2],[3,1,2]] = dphi[0] # 1st node
            Bts[[1],[5]] = -phi[0]
            Bts[[2],[4]] = phi[0]
            Bts[[0,1,2],[9,7,8]] = dphi[1] # 2nd node
            Bts[[1],[11]] = -phi[1]
            Bts[[2],[10]] = phi[1]

            Kabe += Bab.T @ Dab @ Bab * det_jacob * weigth
            Ktse += Bts.T @ Dts @ Bts * det_jacob * weigth
            
        Ke = Kabe + Ktse

        return principal_axis.T @ Ke @ principal_axis

    def mass_matrix(self):
        """ Element mass matrix in the element coordinate system."""
        L   = self.length
        rho = self.material.density

        # Area properties
        A = self.cross_section.area
        Iy = self.cross_section.second_moment_area_y
        Iz = self.cross_section.second_moment_area_z
        J = self.cross_section.polar_moment_area

        if self.element_type == 'pipe1':
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe2':
            Qy = self.cross_section.first_moment_area_y
            Qz = self.cross_section.first_moment_area_z
            Iyz = self.cross_section.second_moment_area_yz
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe1 and pipe2 element types are allowed.')
            pass

        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
    
        # Inertial matrices
        Ggm = np.zeros([6, 6])
        Ggm[np.diag_indices(6)] = np.array([A, A, A, J, Iy, Iz]) / 2
        Ggm[0, 4] = Qy
        Ggm[1, 3] = -Qy
        Ggm[2, 3] = Qz
        Ggm[0, 5] = -Qz
        Ggm[4, 5] = -Iyz
        Ggm = rho*( Ggm + Ggm.T )

        # Numerical integration by Gauss Quadracture
        integrations_points = 2
        points, weigths = gauss_quadracture( integrations_points )

        Me = 0
        N = np.zeros((DOF_PER_NODE_STRUCTURAL, 2 * DOF_PER_NODE_STRUCTURAL))

        for point, weigth in zip(points, weigths):
            phi, _ = shape_function( point )

            N = np.c_[phi[0] * np.eye( DOF_PER_NODE_STRUCTURAL ), phi[1] * np.eye( DOF_PER_NODE_STRUCTURAL )] 

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
        
        if self.element_type == 'pipe1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe1 and pipe2 element types are allowed.')
            pass
        
        return principal_axis.T @ Fe

    def force_vector_acoustic_gcs(self, frequencies, pressure_avg, pressure_external):

        A = self.cross_section.area
        Do = self.cross_section.external_diameter
        Di = self.cross_section.internal_diameter
        stress_axial = (pressure_avg * Di**2 - pressure_external * Do**2) / (Do**2 - Di**2)
        aux = np.zeros([DOF_PER_ELEMENT, 1])
        aux[0], aux[6] = 1, -1
        R = self.rotation_matrix()

        if self.element_type == 'pipe1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            print('Only pipe1 and pipe2 element types are allowed.')
            pass

        aux = R.T @ principal_axis.T @ aux
        F_p = (1 - 2*self.material.poisson_ratio)* A * aux @ stress_axial.reshape([1,-1])

        return F_p