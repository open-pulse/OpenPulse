from typing import TYPE_CHECKING

import numpy as np

from pulse.model.node import NodePosition
from pulse.model.elements.structural_element import DOF_PER_ELEMENT, StructuralElement, symmetrize

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


class BeamStructuralElement(StructuralElement):
    def __init__(self, element_attributes: "ElementAttributes", **kwargs):
        super().__init__(element_attributes, **kwargs)


    def matrices_gcs(self):
        """
        This method returns the element stiffness and mass matrices for beam analytic
        formulation in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.

        mass : array
            Element mass matrix in the global coordinate system.

        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        stiffness = Rt @ self.stiffness_matrix_beam() @ R
        mass = Rt @ self.mass_matrix_beam() @ R

        return stiffness, mass


    def stiffness_matrix_beam(self):
        """
        This method returns the beam element stiffness matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is suitable for any beam cross section data.

        Returns
        -------
        stiffness : array
            Beam element stiffness matrix in the local coordinate system.

        See also
        --------
        stiffness_matrix_pipes : Pipe element stiffness matrix in the local coordinate system.
        """

        # Element length
        L   = self.length

        material = self.material
        cross_section = self.cross_section

        # Material properities
        E   = material.elasticity_modulus
        nu  = material.poisson_ratio
        G   = material.shear_modulus

        # Tube cross section properties
        A   = cross_section.area
        I_2 = cross_section.second_moment_area_y
        I_3 = cross_section.second_moment_area_z
        J   = cross_section._polar_moment_area()

        # Process cross-section offset
        cross_section.offset_rotation(el_type = 'beam_1')
        principal_axis = cross_section.principal_axis

        # alpha = self.get_shear_coefficient(cross_section.additional_section_info, material.poisson_ratio)
        # k_2 = alpha

        # Note: the shear coefficient is currently disabled, as a consequence, the shear deflection will be disabled on the beam_1 element 
        k_2 = 0

        # Others constitutive properties
        k_3     = k_2

        # Auxiliar constants
        if k_2 == 0:
            Phi_12 = 0
            Phi_13 = 0
        else:
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
        ke[[rows], [cols]] = np.array([ 
            E * A / L               ,
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
            beta_12_b / L           ,
            ], dtype=float)

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

        if self.element_attributes.decoupling_info is None:
            Ke = symmetrize(ke)

        else:
            # print(self.index, element_attributes.decoupling_info)
            # [_, _, node_position, decouple_mask] = element_attributes.decoupling_info
            # Ke_decoup = self.decouple_rotations(ke, node_position, decouple_mask)
            # Ke = symmetrize(Ke_decoup)

            Ke = symmetrize(ke) * self.element_attributes.decoupling_matrix

        return principal_axis.T @ Ke @ principal_axis


    def mass_matrix_beam(self):
        """
        This method returns the beam element mass matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is suitable for any beam cross section data.

        Returns
        -------
        mass : array
            Beam element mass matrix in the local coordinate system.

        See also
        --------
        mass_matrix_pipes : Pipe element mass matrix in the local coordinate system.
        """

        material = self.material
        cross_section = self.cross_section

        # Element length
        L   = self.length

        # Material properities
        rho = material.density
        # nu = material.poisson_ratio
        E   = material.elasticity_modulus
        G   = material.shear_modulus

        # Tube cross section properties
        A   = cross_section.area
        I_2 = cross_section.second_moment_area_y
        I_3 = cross_section.second_moment_area_z
        J   = cross_section._polar_moment_area()

        # Process cross-section offset
        cross_section.offset_rotation(el_type = 'beam_1')
        principal_axis = cross_section.principal_axis

        # alpha = self.get_shear_coefficient(element_attributes)
        # k_2 = alpha

        # Note: the shear coefficient is currently disabled, as a consequence, the shear deflection will be disabled on the beam_1 element 
        k_2 = 0
        
        # Others constitutive constants
        J_p     = J
        k_3     = k_2

        # Auxiliar constants
        # 1st group
        if k_2 == 0:
            a_12 = 0
            a_13 = 0
        else:
            a_12 = 1. / (k_2 * A * G)
            a_13 = 1. / (k_3 * A * G)

        b_12 = 1. / (E * I_3)
        b_13 = 1. / (E * I_2)

        # 2nd group
        a_12u_1 = 156 * b_12**2 * L**4 + 3528 * a_12 * b_12 * L**2 + 20160 * a_12**2
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
        gamma_12 = rho * L / (b_12 * L**2 + 12 * a_12)**2
        gamma_13 = rho * L / (b_13 * L**2 + 12 * a_13)**2

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

        Me = symmetrize(me) * self.element_attributes.decoupling_matrix

        return principal_axis.T @ Me @ principal_axis


    def decouple_rotations(self, Ke: np.ndarray, node_position: NodePosition, decouple_mask: list[bool, bool, bool]):
        """
        This method processes the modified elementary stiffness matrix considering the rotation dofs decoupling.

        Parameters
        ----------
        Ke: np.ndarray
            The elementary stiffness matrix.

        node_position: NodePosition | int
            An integer used to represent the node position (use 0 for first node and 1 for last node).
        
        decouple_mask: list[bool]
            A list of three boolean values used to decouple rotations x, y, and z, respectively.
            If the value is True, the corresponding rotation will be decoupled.
        
        Return
        ------
        K_mod: np.ndarray
            The modified elementary stiffness matrix.

        """

        first_node = node_position == NodePosition.FIRST
        rotation_indices = [3, 4, 5] if first_node else [9, 10, 11]

        decouple_indices = list()
        for i, ind in enumerate(rotation_indices):
            if decouple_mask[i]:
                decouple_indices.append(ind)

        all_indices = np.arange(DOF_PER_ELEMENT, dtype=int)
        kept_indices = np.delete(all_indices, decouple_indices)

        K_aa = Ke[np.ix_(kept_indices, kept_indices)]
        K_ab = Ke[np.ix_(kept_indices, decouple_indices)]
        K_ba = Ke[np.ix_(decouple_indices, kept_indices)]
        K_bb = Ke[np.ix_(decouple_indices, decouple_indices)]

        # compute the condensed matrix
        K_cond = K_aa - K_ab @ np.linalg.inv(K_bb) @ K_ba

        # initialize the modified elementary stiffness matrix
        K_mod = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        # fill out the modified elementary stiffness matrix
        K_mod[np.ix_(kept_indices, kept_indices)] = K_cond

        # np.savetxt("K_mod_matrix.dat", K_mod, delimiter=",")

        return K_mod


    def get_shear_coefficient(self):
        """
        This method returns the shear coefficient according to the beam cross section. This coefficient is traditionally introduced in the Timoshenko beam theory.

        Parameters
        -------
        section_info : 
            Beam cross section data.

        poisson : float
            Material Poisson's ratio.

        Returns
        -------
        shear_coefficient : float
            shear coefficient
        """

        cross_section = self.cross_section
        poisson = self.material.poisson_ratio

        section_info = cross_section.section_info

        section_label = section_info[0]
        parameters = section_info[1]
 
        if section_label == "rectangular_beam":

            b, h, b_in, _, _, _ = parameters

            m = (b_in)/h
            n = b_in/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + ((3 + poisson)*m + 3*m**2)*(10*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "circular_beam":

            d_out, d_in, _, _ = parameters
            
            m = d_in/d_out
            numerator = 6*(1 + poisson)*((1 + m**2)**2)
            denominator = (7 + 6*poisson)*((1 + m**2)**2) + ((20 + 12*poisson)*m**2)
            shear_coefficient = numerator/denominator

        elif section_label == "c_beam":

            h, w1, t1, w2, t2, tw, _, _, _ = parameters
            
            tf = (t1+t2)/2
            b = (w1+w2)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (30*n**2)*(m + m**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = 0.93*numerator/denominator

        elif section_label == "i_beam":

            h, w1, t1, w2, t2, tw, _, _, _ = parameters
            
            tf = (t1+t2)/2
            b = (w1+w2)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (30*n**2)*(m + m**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "i_beam":

            h, w1, t1, tw, _, _, _ = parameters
            tf, b = t1, w1
      
            m = (2*b*tf)/(h*tw)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 4*m)**2)
            denominator = (12 + 96*m + 278*m**2 + 192*m**3) + poisson*(11 + 88*m + 248*m**2 + 216*m**3) + (30*n**2)*(m + m**2) + (10*poisson*n**2)*(4*m + 5*m**2 + m**3)
            shear_coefficient = numerator/denominator

        elif section_label == "generic_beam":
            shear_coefficient = cross_section.shear_coefficient

        return shear_coefficient