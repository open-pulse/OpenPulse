import numpy as np
from math import pi, sqrt, sin, cos

from node import Node
from tube import TubeCrossSection
from material import Material


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
        return self.node_initial.distance(self.node_final)

    def global_degree_freedom(self, fixed_nodes):
        """Return the degrees of freedom related to the element in a array with 12 integers.
        If the index of the initial node or final node are in 'fixed_nodes', its degree of
        freedom are not considered."""
        if self.node_initial.user_index in fixed_nodes:
            index_global_initial = []
        elif self.node_final.user_index in fixed_nodes:
            index_global_final = []
        else:
            index_global_initial = self.node_initial.global_dof()
            index_global_final = self.node_final.global_dof()
            
        return index_global_initial.tolist() + index_global_final.tolist()

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

    def stiffness_matrix(self):
        """ Element striffness matrix in the element coordinate system."""

        # Element length
        L   = self.length()

        # Material properities
        E   = self.material.young_modulus
        nu  = self.material.poisson_ratio
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area()
        I_2 = self.cross_section.moment_area()
        J   = self.cross_section.polar_moment_area()
        k_2 = self.cross_section.shear_form_factor( self.material.poisson_ratio )

        # Others constitutive properties
        I_3     = I_2
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

        
        ke = np.zeros((self.total_degree_freedom, self.total_degree_freedom))

        # stiffness matrix diagonal construction
        rows, cols = np.diag_indices(self.total_degree_freedom)
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

        return Element.symmetrize(ke)

    def stiffness_matrix_global(self):
        """ Element striffness matrix in the global coordinate system."""
        T = self.rotation_matrix()
        return T.T @ self.stiffness_matrix() @ T

    def mass_matrix(self):
        """ Element mass matrix in the element coordinate system."""

        # Element length
        L   = self.length()

        # Material properities
        rho = self.material.density
        E   = self.material.young_modulus
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area()
        I_2 = self.cross_section.moment_area()
        J   = self.cross_section.polar_moment_area()
        k_2 = self.cross_section.shear_form_factor( self.material.poisson_ratio )

        # Others constitutive constants
        I_3     = I_2
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


        me = np.zeros((self.total_degree_freedom, self.total_degree_freedom))

        # Mass matrix diagonal construction
        rows, cols = np.diag_indices(self.total_degree_freedom)
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

        return Element.symmetrize(me)
    
    def mass_matrix_global(self):
        """ Element mass matrix in the global coordinate system."""
        T = self.rotation_matrix()
        return T.T @ self.mass_matrix() @ T
    


