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
        gamma = 0
        delta_x = self.last_node.x - self.first_node.x
        delta_y = self.last_node.y - self.first_node.y
        delta_z = self.last_node.z - self.first_node.z

        L_ = sqrt(delta_x**2 + delta_y**2)
        L  = sqrt(delta_x**2 + delta_y**2 + delta_z**2)

        C = np.zeros((3,3))
        if L_ != 0.:
            C[0,] = np.array([ [delta_x / L, delta_y / L, delta_z / L] ])

            C[1,] = np.array([ [-delta_x*delta_z * sin(gamma) / (L_ * L) - delta_y * cos(gamma) / L_,
                                -delta_y*delta_z * sin(gamma) / (L_ * L) + delta_x * cos(gamma) / L_,
                                L_ * sin(gamma) / L] ])

            C[2,] = np.array([ [-delta_x*delta_z * cos(gamma) / (L_ * L) + delta_y * sin(gamma) / L_,
                                -delta_y*delta_z * cos(gamma) / (L_ * L) - delta_x * sin(gamma) / L_,
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

        T_tild_e = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        T_tild_e[0:3, 0:3] = C
        T_tild_e[3:6, 3:6] = C
        T_tild_e[6:9, 6:9] = C
        T_tild_e[9:12, 9:12] = C

        return T_tild_e
    
    def stiffness_matrix(self):
        """ Element striffness matrix in the element coordinate system."""
        L   = self.length

        E = self.material.young_modulus
        mu = self.material.mu_parameter

        A = self.cross_section.area
        I1 = self.cross_section.moment_area
        J = self.cross_section.polar_moment_area
        shear_area_1 = self.cross_section.shear_area(L, E)

        I2 = I1
        shear_area_2 = shear_area_1

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2
        inv_jacobian = 1 / det_jacobian

        #Constitutive matrices (element with constant geometry along x-axis)
        D_shear = np.diag([mu * shear_area_1, mu * shear_area_2])
        D_bending = np.diag([E * I1, E * I2])

        # Numerical integration by Gauss Quadracture
        number_integrations_points = 1
        points, weigths = gauss_quadracture(number_integrations_points)

        Kbe = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))
        Kse = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))
        Kae = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))
        Kte = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        for point, weigth in zip( points, weigths ):
            # Shape function and its derivative
            phi, derivative_phi = shape_function(point)
            dphi = inv_jacobian * derivative_phi

            B_bending = np.zeros((2,12))
            B_bending[[0,1],[4,5]] = dphi[0]
            B_bending[[0,1],[10,11]] = dphi[1]

            B_shear = np.zeros((2,12))
            B_shear[[0,1],[1,2]] = dphi[0]
            B_shear[0,5] = -phi[0]
            B_shear[[0,1],[7,8]] = dphi[1]
            B_shear[0,11] = -phi[1]
            B_shear[1,4] = phi[0]
            B_shear[1,10] = phi[1]

            B_axial = np.zeros((1,12))
            B_axial[0,0] = dphi[0]
            B_axial[0,6] = dphi[1]

            B_torsional = np.zeros((1,12))
            B_torsional[0,3] = dphi[0]
            B_torsional[0,9] = dphi[1] 
            
            Kbe += (B_bending.T @ D_bending @ B_bending) * det_jacobian * weigth
            Kse += (B_shear.T @ D_shear @ B_shear) * det_jacobian * weigth
            Kae += E * A * (B_axial.T @ B_axial) * det_jacobian * weigth
            Kte += mu * J * (B_torsional.T @ B_torsional) * det_jacobian * weigth

        Ke = Kbe + Kse + Kae + Kte 

        return Ke

    def mass_matrix(self):
        """ Element mass matrix in the element coordinate system."""
        L   = self.length

        rho = self.material.density

        A = self.cross_section.area
        I1 = self.cross_section.moment_area
        J = self.cross_section.polar_moment_area

        I2 = I1

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2
    
        #Inertial matrices (element with constant geometry along x-axis)
        G_translation = rho * A * np.eye(3)
        G_rotation = rho * np.diag([J, I1, I2])

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 2
        points, weigths = gauss_quadracture(number_integrations_points)
        
        #
        Me = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))
        Mass_rotation = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))
        Mass_translation = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT))

        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)

            N_translation = np.zeros((3,12))
            N_translation[[0,1,2],[0,1,2]] = phi[0]
            N_translation[[0,1,2],[6,7,8]] = phi[1]

            N_rotation = np.zeros((3,12))
            N_rotation[[0,1,2],[3,4,5]] = phi[0]
            N_rotation[[0,1,2],[9,10,11]] = phi[1]
            
            Mass_translation += (N_translation.T @ G_translation @ N_translation) * det_jacobian * weigth
            Mass_rotation += N_rotation.T @ G_rotation @ N_rotation * det_jacobian * weigth

        Me = Mass_translation + Mass_rotation

        return Me
    
    def force_vector(self):
        ## Numerical integration by Gauss Quadracture
        L = self.length
        number_integrations_points = 2
        points, weigths = gauss_quadracture(number_integrations_points)

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        Fe = np.zeros((DOF_PER_ELEMENT))
        NN = np.zeros((DOF_PER_NODE_STRUCTURAL, 2*DOF_PER_NODE_STRUCTURAL))

        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)

            NN[0 : DOF_PER_NODE_STRUCTURAL, 0 : DOF_PER_NODE_STRUCTURAL] = phi[0] * np.identity(DOF_PER_NODE_STRUCTURAL)
            NN[0 : DOF_PER_NODE_STRUCTURAL, DOF_PER_NODE_STRUCTURAL: 2*DOF_PER_NODE_STRUCTURAL] = phi[1] * np.identity(DOF_PER_NODE_STRUCTURAL)

            Fe += (NN.T @ self.loaded_forces.T) * det_jacobian * weigth

        return Fe