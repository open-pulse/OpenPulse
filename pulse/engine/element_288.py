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
                 element_type,
                 user_index,
                 **kwargs):
        
        self.node_initial = node_initial
        self.node_final = node_final
        self.material = material
        self.cross_section = cross_section
        self.element_type = element_type
        self.user_index = user_index  

    def length(self):
        """Define the element length."""
        return self.node_initial.distance( self.node_final )
   
    def dofs(self):
        """Return the degrees of freedom related to the element in a array with 12 integers.
        If the index of the initial node or final node are in 'fixed_nodes', its degree of
        freedom are not considered."""

        # Initial node global, local, global boundary and local boundary degrees of freedom
        global_dof_ni, local_dof_ni, global_boundary_ni, boundary_ni = self.node_initial.dofs( )

        # Final node global degrees of freedom, global boundary, local degree od freedom emended and boundary emended
        global_dof_nf, local_dof_nf, global_boundary_nf, boundary_nf  = self.node_final.dofs( )
        local_dof_nf = local_dof_nf + Node.degree_freedom

        if boundary_nf != []:
            boundary_nf = np.array(boundary_nf) + Node.degree_freedom
        
        # Concatenating vectors
        a, b = len( global_dof_ni ), len( global_dof_nf )
        c, d = Node.degree_freedom - a, Node.degree_freedom - b
        global_dof = np.zeros(a+b,dtype = int)
        local_dof = np.zeros(a+b,dtype = int)
        global_boundary = np.zeros(c+d,dtype = int)
        boundary = np.zeros(c+d,dtype = int)

        global_dof[0:a], global_dof[a:a+b] = global_dof_ni, global_dof_nf
        local_dof[0:a], local_dof[a:a+b] = local_dof_ni, local_dof_nf
        global_boundary[0:c], global_boundary[c:c+d] = global_boundary_ni, global_boundary_nf
        boundary[0:c], boundary[c:c+d] = boundary_ni, boundary_nf
     

        return global_dof, local_dof, global_boundary, boundary

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
        nu = self.material.poisson_ratio
        G = self.material.shear_modulus
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
        det_jacobian = L / 2
        inv_jacobian = 1 / det_jacobian

        #Constitutive matrices (element with constant geometry along x-axis)
        D_shear = np.diag([mu * shear_area_1, mu * shear_area_2])
        D_bending = np.diag([E * I1, E * I2])

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 1
        points, weigths = Element.gauss_quadracture( number_integrations_points )

        # Memory alocation
        element_dofs = Element.total_degree_freedom
        Kbe = np.zeros((element_dofs,element_dofs))
        Kse = np.zeros((element_dofs,element_dofs))
        Kae = np.zeros((element_dofs,element_dofs))
        Kte = np.zeros((element_dofs,element_dofs))

        for point, weigth in zip( points, weigths ):

            # Shape function and its derivative
            phi, derivative_phi = Element.shape_function( point )
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

        return Kbe + Kse + Kae + Kte 

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
        mu = self.material.mu_parameter()

        # Tube cross section properties
        A = self.cross_section.area()
        I1 = self.cross_section.moment_area()
        J = self.cross_section.polar_moment_area()

        # Others constitutive constants
        I2 = I1

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2
    
        #Inertial matrices (element with constant geometry along x-axis)
        G_translation = rho * A * np.eye(3)
        G_rotation = rho * np.diag([J, I1, I2])

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 2
        points, weigths = Element.gauss_quadracture( number_integrations_points )
        
        #
        element_dofs = Element.total_degree_freedom
        Me = np.zeros((element_dofs, element_dofs))
        Mass_translation = np.zeros((element_dofs, element_dofs))
        Mass_rotation = np.zeros((element_dofs, element_dofs))
        for point, weigth in zip(points, weigths):
            phi, dphi = Element.shape_function( point )

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
    
    def mass_matrix_gcs(self):
        """ Element mass matrix in the global coordinate system."""
        T = self.rotation_matrix()
        return T.T @ self.mass_matrix() @ T

    def force_vector(self, load):
        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 2
        points, weigths = Element.gauss_quadracture( number_integrations_points )

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        node_dofs = Node.degree_freedom
        Fe = np.zeros(( Element.total_degree_freedom, 1))
        NN = np.zeros((node_dofs,2 * node_dofs))


        for point, weigth in zip(points, weigths):
            phi, _ = Element.shape_function( point )

            NN[0:node_dofs,0:node_dofs] = phi[0] * np.identity( node_dofs )
            NN[0:node_dofs,node_dofs:2 * node_dofs] = phi[1] * np.identity( node_dofs )

            Fe += (NN.T @ load.T) * det_jacobian * weigth
        return Fe
    
    def force_vector_gcs(self, load):
        T = self.rotation_matrix()
        # I'm not sure how to rotate this vector
        return T.T @ self.force_vector( load )
    