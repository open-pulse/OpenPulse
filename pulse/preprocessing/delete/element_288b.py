import numpy as np
from math import pi, sqrt, sin, cos

from pulse.engine.node import Node
from pulse.engine.section_fem import TubeCrossSection as TCS
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
                 cross_section_properties,
                 load,
                 element_type,
                 user_index,
                 **kwargs):
        
        self.node_initial = node_initial
        self.node_final = node_final
        self.material = material
        self.cross_section_properties = cross_section_properties
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

        if L_ > 0.0001*L:
            sine = delta_y/L_
            cossine = delta_x/L_
        else:
            sine = 0
            cossine = 1

        C = np.zeros((3,3))
        if L_ != 0.:
            C[0,] = np.array([ [cossine * L_ / L,
                                sine * L_ / L,
                                delta_z / L] ])

            C[1,] = np.array([ [-cossine * delta_z * sin(gamma) / L - sine * cos(gamma),
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
        A, I1, I2, I12, J, Q1, Q2, RES1, RES2, _, _, _, _, _, _ = self.cross_section_properties

        # Shear coefficiets - Treatment 
        al1 = 1/RES1
        al2 = 1/RES2

        #Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        #Constitutive matrices (element with constant geometry along x-axis)
        #Torsion + shear - Part a
        Dts = mu*np.array([ [J,   -Q1,   Q2],
                            [-Q1, al1*A, 0.],
                            [Q2,  0.,    al2*A]])
        Dab = E*np.array([[A,   Q1, -Q2],
                          [Q1,  I1, -I12],
                          [-Q2,-I12, I2]]) #Axial + Bending

        ## Numerical integration by Gauss Quadracture
        number_integrations_points = 1
        points, weigths = Element.gauss_quadracture( number_integrations_points )
        
        Ke =  np.zeros( (Element.total_degree_freedom ,Element.total_degree_freedom) )
        Kabe = np.zeros_like(Ke)
        Ktse = np.zeros_like(Ke)

        for point, weigth in zip( points, weigths ):

            # Shape function and its derivative
            phi, derivative_phi = Element.shape_function( point )
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
        A, I1, I2, I12, J, Q1, Q2, _, _, _, _, _, _, _, _ = self.cross_section_properties

        #Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
    
        #Inertial matrices
        Ggm = np.zeros([6, 6])
        Ggm[np.diag_indices(6)] = np.array([A, A, A, J, I1, I2]) / 2
        Ggm[0, 4] = Q1
        Ggm[1, 3] = -Q1
        Ggm[2, 3] = Q2
        Ggm[0, 5] = -Q2
        Ggm[4, 5] = -I12
        Ggm = rho*( Ggm + Ggm.T )

        # Numerical integration by Gauss Quadracture
        number_integrations_points = 2
        points, weigths = Element.gauss_quadracture( number_integrations_points )

        Me = 0
        node_dofs = Node.degree_freedom
        N = np.zeros((node_dofs,2 * node_dofs))

        node_dofs = Node.degree_freedom

        for point, weigth in zip(points, weigths):
            phi, _ = Element.shape_function( point )

            N = np.c_[phi[0] * np.identity( node_dofs ), phi[1] * np.identity( node_dofs )] 

            Me += (N.T @ Ggm @ N) * det_jacob * weigth 
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
        N = np.zeros((node_dofs,2 * node_dofs))


        for point, weigth in zip(points, weigths):
            phi, _ = Element.shape_function( point )

            N = np.c_[phi[0] * np.identity( node_dofs ), phi[1] * np.identity( node_dofs )] 

            Fe += (N.T @ self.load) * det_jacob * weigth
        return Fe
    
    def force_vector_gcs(self):
        T = self.rotation_matrix()
        return T.T @ self.force_vector()
    
    def matrices_gcs(self):
        T = self.rotation_matrix()
        Me_gcs = T.T @ self.mass_matrix() @ T
        Ke_gcs = T.T @ self.stiffness_matrix() @ T
        Fe_gcs = T.T @ self.force_vector()
        return Me_gcs.flatten(), Ke_gcs.flatten(), Fe_gcs

if __name__ == '__main__':
    ## Test setup! ##
    young_modulus = 210e9 # Young modulus [Pa]
    poisson_ratio = 0.3   # Poisson ratio[-]
    density = 7860  # Density[kg/m^3]
    material = Material('Steel', density, young_modulus = young_modulus, poisson_ratio = poisson_ratio)

    ## Cross section definition:
    D_external = 0.05   # External diameter [m]
    thickness  = 0.008 # Thickness [m]
    division_number = 64
    offset = [0.005, 0.005]
    cross_section_1 = TCS(D_external, division_number = division_number , offset = offset , thickness = thickness, element_type = '288b')
    cross_section_1_properties = cross_section_1.all_props()

    load = [0, 0, 0, 0, 0, 0]
    element_type = None
    user_index = 1
    node_initial = Node(0, 0, 0, 1, index = 0)
    node_final = Node(0.01, 0, 0, 2, index = 1)

    element = Element(node_initial, 
                      node_final,
                      material,
                      cross_section_1_properties,
                      load,
                      element_type,
                      user_index)

    ke = element.stiffness_matrix_gcs()
    me = element.mass_matrix_gcs()

    print(ke)