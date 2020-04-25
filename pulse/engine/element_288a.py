import numpy as np
from math import pi, sqrt, sin, cos

from pulse.engine.node import Node
from pulse.engine.tube import TubeCrossSection
from pulse.engine.material import Material


class Element:
    """ Element  

    Parameters
    ----------
    node_initial : Node
        Initial element former node.
    node_final : Node
        Final element former node.
    material : Material
        Element's material.
    cross_section : TubeCrossSection
        Element's cross section.
    element_type : pipe16, pipe288
        Element type identifier.
    index_user : int
        User element identifier.
    Examples
    --------

    """
    nodes_per_element = 2
    total_degree_freedom = nodes_per_element * Node.degree_freedom

    def __init__(self,
                 node_initial, 
                 node_final,
                 material,
                 cross_section,
                 load,
                 element_type,
                 user_index,
                 **kwargs):
        
        self.node_initial = node_initial
        self.node_final = node_final
        self.material = material
        self.cross_section = cross_section
        self.load = load
        self.element_type = element_type
        self.user_index = user_index  

    def length(self):
        """Define the element length."""
        return self.node_initial.distance( self.node_final )
   
    def dofs(self):
        """Return the degrees of freedom related to the element in a array with 12 integers.
        If the index of the initial node or final node are in 'fixed_nodes', its degree of
        freedom are not considered."""

        global_dof_ni = self.node_initial.dofs_node( )
        global_dof_nf = self.node_final.dofs_node( )

        # Concatenating vectors
        a, b = len( global_dof_ni ), len( global_dof_nf )
        global_dof = np.zeros(a+b,dtype = int)
        global_dof[0:a], global_dof[a:a+b] = global_dof_ni, global_dof_nf

        mat_I = global_dof.reshape( a+b, 1) @ np.ones(( 1, a+b ))
        mat_J = mat_I.T
        mat_If = mat_I[:,0]

        return mat_I.flatten(), mat_J.flatten(), mat_If.flatten()

    def rotation_matrix(self):
        """ Make the rotation from the element coordinate system to the global doordinate system."""
        # Rotation Matrix
        gamma = 0
        delta_x = self.node_final.x - self.node_initial.x
        delta_y = self.node_final.y - self.node_initial.y
        delta_z = self.node_final.z - self.node_initial.z

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


        T_tild_e = np.zeros((self.total_degree_freedom, self.total_degree_freedom))

        T_tild_e[0:3, 0:3]      = C
        T_tild_e[3:6, 3:6]      = C
        T_tild_e[6:9, 6:9]      = C
        T_tild_e[9:12, 9:12]    = C

        return T_tild_e
    
    @staticmethod
    def symmetrize(a):
        """ Take a matrix a and symmetrize it."""
        return a + a.T - np.diag(a.diagonal())

    @staticmethod
    def gauss_quadracture(n):
        if n == 1:
            points = [0]
            weigths = [2]
            return points, weigths
        if n == 2:
            points = [-1/sqrt(3), 1/sqrt(3)]
            weigths = [1, 1]
            return points, weigths
        if n == 3:
            points = [-sqrt(3/5), 0, sqrt(3/5)]
            weigths = [5/9, 8/9, 5/9]
            return points, weigths
        else:
            #warning: n must be 1, 2 or 3.
            pass
    
    @staticmethod
    def shape_function(ksi):
        """
        Created on Wed Nov 20 10:24:26 2019
        @author: Olavo M. Silva
        Linear shape functions and derivatives for 2-node topology

        """
        phi = np.array( [(1 - ksi)/2, (1 + ksi)/2] )
        derivative_phi = np.array( [-0.5, 0.5] )
        return phi, derivative_phi

    def stiffness_matrix(self):
        """ Element striffness matrix in the element coordinate system."""

        # Element length
        L   = self.length()

        # Material properities
        E = self.material.young_modulus
        mu = self.material.mu_parameter()

        # Tube cross section properties
        A = self.cross_section.area()
        I1 = self.cross_section.moment_area()
        J = self.cross_section.polar_moment_area()
        shear_area_1 = self.cross_section.shear_area(L, E)

        # Others constitutive properties
        I2 = I1
        shear_area_2 = shear_area_1

        #Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        #Constitutive matrices (element with constant geometry along x-axis)
        D_shear = np.diag([mu * shear_area_1, mu * shear_area_2])
        D_bend = np.diag([E * I1, E * I2])

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 1
        points, weigths = Element.gauss_quadracture( number_integrations_points )
        
        Ke=0.
        B_bend = np.zeros((2,12))
        B_shear = np.zeros((2,12))
        B_axial = np.zeros((1,12))
        B_tors = np.zeros((1,12))

        for point, weigth in zip( points, weigths ):

            # Shape function and its derivative
            phi, derivative_phi = Element.shape_function( point )
            dphi = inv_jacob * derivative_phi
            
            B_bend[[0,1],[4,5]] = dphi[0]
            B_bend[[0,1],[10,11]] = dphi[1]
            
            B_shear[[0,1],[1,2]] = dphi[0]
            B_shear[0,5] = -phi[0]
            B_shear[[0,1],[7,8]] = dphi[1]
            B_shear[0,11] = -phi[1]
            B_shear[1,4] = phi[0]
            B_shear[1,10] = phi[1]

            B_axial[0,0] = dphi[0]
            B_axial[0,6] = dphi[1]
            
            B_tors[0,3] = dphi[0]
            B_tors[0,9] = dphi[1] 

            Ke += ((B_bend.T @ D_bend @ B_bend)+(B_shear.T @ D_shear @ B_shear)+E * A * (B_axial.T @ B_axial)+mu * J * (B_tors.T @ B_tors)) * det_jacob * weigth

        return Ke

    def stiffness_matrix_gcs(self):
        """ Element striffness matrix in the global coordinate system."""
        T = self.rotation_matrix()
        return T.T @ self.stiffness_matrix() @ T

    def mass_matrix(self):
        """ Element mass matrix in the element coordinate system."""

        # Element length
        L   = self.length()

        # Material properities
        rho = self.material.density

        # Tube cross section properties
        A = self.cross_section.area()
        I1 = self.cross_section.moment_area()
        J = self.cross_section.polar_moment_area()

        # Others constitutive constants
        I2 = I1

        #Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
    
        #Inertial matrices (element with constant geometry along x-axis)
        G_tr = rho * A * np.eye(3)
        G_rot = rho * np.diag([J, I1, I2])

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 2
        points, weigths = Element.gauss_quadracture( number_integrations_points )

        Me=0.
        N_tr = np.zeros((3,12))
        N_rot = np.zeros((3,12))

        for point, weigth in zip(points, weigths):
            phi, _ = Element.shape_function( point )
            
            N_tr[[0,1,2],[0,1,2]] = phi[0]
            N_tr[[0,1,2],[6,7,8]] = phi[1]

            N_rot[[0,1,2],[3,4,5]] = phi[0]
            N_rot[[0,1,2],[9,10,11]] = phi[1]
            
            Me += ((N_tr.T @ G_tr @ N_tr) + (N_rot.T @ G_rot @ N_rot))*det_jacob*weigth 
        return Me
    
    def mass_matrix_gcs(self):
        """ Element mass matrix in the global coordinate system."""
        T = self.rotation_matrix()
        return T.T @ self.mass_matrix() @ T

    def force_vector(self):
        ## Numerical integration by Gauss Quadracture
        L   = self.length()
        number_integrations_points = 2
        points, weigths = Element.gauss_quadracture( number_integrations_points )

        #Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2

        node_dofs = Node.degree_freedom
        Fe = np.zeros(( Element.total_degree_freedom))
        NN = np.zeros((node_dofs,2 * node_dofs))


        for point, weigth in zip(points, weigths):
            phi, _ = Element.shape_function( point )

            NN[0:node_dofs, 0:node_dofs            ] = phi[0] * np.identity( node_dofs )
            NN[0:node_dofs, node_dofs:2 * node_dofs] = phi[1] * np.identity( node_dofs )

            Fe += (NN.T @ self.load) * det_jacob * weigth
        return Fe
    
    def force_vector_gcs(self):
        T = self.rotation_matrix()
        return T.T @ self.force_vector()
    
    def matrices_gcs(self):
        T = self.rotation_matrix()
        T_trp = T.T
        Me_gcs = T_trp @ self.mass_matrix() @ T
        Ke_gcs = T_trp @ self.stiffness_matrix() @ T
        Fe_gcs = T_trp @ self.force_vector()
        return Me_gcs.flatten(), Ke_gcs.flatten(), Fe_gcs


