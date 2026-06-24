import numpy as np

from pulse.model.node import DOF_PER_NODE_STRUCTURAL, Node
from pulse.model.properties.fluid import Fluid
from pulse.model.structural_element import StructuralElement  #, decoupling_matrix

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


class PipeStructuralElement(StructuralElement):
    def __init__(self, first_node: Node, last_node: Node, index: int, **kwargs):
        super().__init__(first_node, last_node, index, **kwargs)

        self.element_type = "pipe_1"
        self.wall_formulation: str = kwargs.get('wall_formulation', 'thin_wall')

        self.loaded_forces: np.ndarray = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))

        self.capped_end: bool = kwargs.get('capped_end', True)
        self.stress_intensification: bool = kwargs.get('stress_intensification', True)


    def stiffness_matrix_pipes(self):
        """
        This method returns the pipe element stiffness matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        stiffness : array
            Pipe element stiffness matrix in the local coordinate system.

        See also
        --------
        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """
        L = self.length

        E = self.material.elasticity_modulus
        mu = self.material.mu_parameter
        G = self.material.shear_modulus
                   
        # Area properties - constant section along x-axis
        A = self.cross_section.area
        Iy = self.cross_section.second_moment_area_y
        Iz = self.cross_section.second_moment_area_z
        J = self.cross_section.polar_moment_area
        res_y = self.cross_section.res_y
        res_z = self.cross_section.res_z
    
        # Shear coefficiets
        aly = 1 / res_y
        alz = 1 / res_z

        if self.element_type in ['pipe_1', 'valve']:
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = self.cross_section.principal_axis
        else:
            print('Only pipe_1 element types are allowed.')
            
        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        # Constitutive matrices (element with constant geometry along x-axis)
        # Torsion and shear
        Dts = mu*np.array([ [J  ,   -Qy,    Qz],
                            [-Qy, aly*A,     0],
                            [Qz ,     0, alz*A] ])
        self._Dts = Dts
        # Axial and Bending
        Dab = E*np.array([  [A  ,   Qy,  -Qz],
                            [Qy ,   Iy, -Iyz],
                            [-Qz, -Iyz,   Iz]  ])
        self._Dab = Dab

        key = 1

        # Variables related to prestress effect
        self.Phi_y = key*(12*E*Iz)/(G*aly*A*L**2)
        self.Phi_z = key*(12*E*Iy)/(G*alz*A*L**2)
        self.Jx_Ax = key*J/A

        ## Numerical integration by Gauss quadrature
        integrations_points = 1
        points, weigths = gauss_quadrature(integrations_points)

        Kabe = 0.
        Ktse = 0.

        Ue = np.zeros(DOF_PER_ELEMENT, dtype=float)
        K_geo = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        if self.static_analysis_evaluated:

            self.static_analysis_evaluated = False
            Ue = self.static_element_results_lcs()
            mat_K_geo = self.get_Te_matrix()
            Fp_x = self.force_vector_stress_stiffening(vector_gcs=False)
            Te = (E*A/L) * (Ue[6] - Ue[0]) - Fp_x
            K_geo = (Te/L) * mat_K_geo

        for point, weigth in zip(points, weigths):

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

        Ke = Kabe + Ktse + K_geo

        return principal_axis.T @ Ke @ principal_axis


    def mass_matrix_pipes(self):
        """
        This method returns the pipe element mass matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        mass : array
            Pipe element mass matrix in the local coordinate system.

        See also
        --------
        mass_matrix_beam : Beam element mass matrix in the local coordinate system.
        """
        L   = self.length
        rho = self.material.density

        # Area properties - constant section along x-axis
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
        else:
            print('Only pipe_1 element types are allowed.')

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

        # Numerical integration by Gauss quadrature
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)

        Me = 0
        N = np.zeros((DOF_PER_NODE_STRUCTURAL, 2 * DOF_PER_NODE_STRUCTURAL))
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL )
        
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function( point )
            N = np.c_[phi[0]*aux_eyes, phi[1]*aux_eyes] 
            Me += (N.T @ Ggm @ N) * det_jacob * weigth

        return principal_axis.T @ Me @ principal_axis
    

    def get_Te_matrix(self):
        """
        """
               
        L = self.length    
        den_y = (1 + self.Phi_y)**2
        den_z = (1 + self.Phi_z)**2

        mat_K_geo = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        
        mat_K_geo[[1,2,7,8],[1,2,7,8]] = [  (6/5 + 2*self.Phi_y + self.Phi_y**2)/den_y, 
                                            (6/5 + 2*self.Phi_z + self.Phi_z**2)/den_z,
                                            (6/5 + 2*self.Phi_y + self.Phi_y**2)/den_y,
                                            (6/5 + 2*self.Phi_z + self.Phi_z**2)/den_z  ]

        mat_K_geo[[1,2,7,8],[7,8,1,2]] = [  -(6/5 + 2*self.Phi_y + self.Phi_y**2)/den_y, 
                                            -(6/5 + 2*self.Phi_z + self.Phi_z**2)/den_z,
                                            -(6/5 + 2*self.Phi_y + self.Phi_y**2)/den_y,
                                            -(6/5 + 2*self.Phi_z + self.Phi_z**2)/den_z   ]

        mat_K_geo[[3,3,9,9],[3,9,3,9]] =  [  self.Jx_Ax, -self.Jx_Ax, -self.Jx_Ax, self.Jx_Ax  ]

        mat_K_geo[[4,5,10,11],[4,5,10,11]] = [  (L**2)*((2/15) + (self.Phi_z/6) + ((self.Phi_z**2)/12))/den_z,
                                                (L**2)*((2/15) + (self.Phi_y/6) + ((self.Phi_y**2)/12))/den_y,
                                                (L**2)*((2/15) + (self.Phi_z/6) + ((self.Phi_z**2)/12))/den_z,
                                                (L**2)*((2/15) + (self.Phi_y/6) + ((self.Phi_y**2)/12))/den_y   ]

        mat_K_geo[[4,5,10,11],[10,11,4,5]] = [  -(L**2)*((1/30) + (self.Phi_z/6) + ((self.Phi_z**2)/12))/den_z,
                                                -(L**2)*((1/30) + (self.Phi_y/6) + ((self.Phi_y**2)/12))/den_y,
                                                -(L**2)*((1/30) + (self.Phi_z/6) + ((self.Phi_z**2)/12))/den_z,
                                                -(L**2)*((1/30) + (self.Phi_y/6) + ((self.Phi_y**2)/12))/den_y   ]

        mat_K_geo[[1,1,5,11],[5,11,1,1]] =  [   L/(10*den_y), L/(10*den_y), L/(10*den_y), L/(10*den_y)  ]

        mat_K_geo[[4,8,8,10],[8,4,10,8]] =  [   L/(10*den_z), L/(10*den_z), L/(10*den_z), L/(10*den_z)  ]

        mat_K_geo[[5,7,7,11],[7,5,11,7]] =  [   -L/(10*den_y), -L/(10*den_y), -L/(10*den_y), -L/(10*den_y)  ]

        mat_K_geo[[2,2,4,10],[4,10,2,2]] =  [   -L/(10*den_z), -L/(10*den_z), -L/(10*den_z), -L/(10*den_z)  ]
        
        return mat_K_geo


    def stiffness_matrix_pipes_variable_section(self):
        """
        This method returns the pipe element stiffness matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        stiffness : array
            Pipe element stiffness matrix in the local coordinate system.

        See also
        --------
        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """
        L = self.length

        E = self.material.elasticity_modulus
        mu = self.material.mu_parameter
        G = self.material.shear_modulus
        
        self.process_offset_transformation_matrices()
                            
        ## Numerical integration by Gauss quadrature
        integrations_points = 1
        points, weigths = gauss_quadrature(integrations_points)

        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        index = 0
        Kabe = 0.
        Ktse = 0.

        sections = [self.first_node.cross_section, self.last_node.cross_section]
        prop_1 = [sections[0].outer_diameter, sections[1].outer_diameter]
        prop_2 = [sections[0].thickness, sections[1].thickness]

        for point, weigth in zip( points, weigths ):

            # Shape function and its derivative
            phi, derivative_phi = shape_function( point )
            dphi = inv_jacob * derivative_phi

            outer_diameter = point*((prop_1[1] - prop_1[0])/2) + ((prop_1[1] + prop_1[0])/2)
            thickness = point*((prop_2[1] - prop_2[0])/2) + ((prop_2[1] + prop_2[0])/2)

            section = sections[index]
            section.set_section_parameters([outer_diameter, thickness])
            section.update_properties()

            # Area properties - constant section along x-axis
            A = section.area
            Iy = section.second_moment_area_y
            Iz = section.second_moment_area_z
            J = section.polar_moment_area
            res_y = section.res_y
            res_z = section.res_z
        
            # Shear coefficiets
            aly = 1/res_y
            alz = 1/res_z
            
            if self.element_type in ['pipe_1', 'valve']:
                Qy = 0
                Qz = 0
                Iyz = 0
                # principal_axis = section.principal_axis
            else:
                print('Only pipe_1 element types are allowed.')
                
            key = 1
            # Variables related to prestress effect
            self.Phi_y = key*(12*E*Iz)/(G*aly*A*L**2)
            self.Phi_z = key*(12*E*Iy)/(G*alz*A*L**2)
            self.Jx_Ax = key*J/A

            Ue = np.zeros(DOF_PER_ELEMENT, dtype=float)
            K_geo = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

            if self.static_analysis_evaluated:

                self.static_analysis_evaluated = False
                Ue = self.static_element_results_lcs()
                mat_K_geo = self.get_Te_matrix()
                Fp_x = self.force_vector_stress_stiffening(vector_gcs=False)
                Te = (E*A/L)*(Ue[6] - Ue[0]) - Fp_x
                K_geo = (Te/L)*mat_K_geo

            # if self.index in [12]:
            #     # print("\nElement 12:")
            #     # print("UX(11):", self.first_node.static_nodal_solution_gcs[0])
            #     # print("UX(12):", self.last_node.static_nodal_solution_gcs[0])
            #     print(f"Te: {Te}")

            # Constitutive matrices (element with constant geometry along x-axis)
            # Torsion and shear
            Dts = mu*np.array([ [J  ,   -Qy,    Qz],
                                [-Qy, aly*A,     0],
                                [Qz ,     0, alz*A] ])
            self._Dts = Dts
            # Axial and Bending
            Dab = E*np.array([  [A  ,   Qy,  -Qz],
                                [Qy ,   Iy, -Iyz],
                                [-Qz, -Iyz,   Iz]  ])
            self._Dab = Dab

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

            index += 1

        Ke = Kabe + Ktse + K_geo

        return self.transf_matrix_offset_shear_left @ Ke @ self.transf_matrix_offset_shear_right


    def mass_matrix_pipes_variable_section(self):
        """
        This method returns the pipe element mass matrix according to the 3D Timoshenko beam theory 
        in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        mass : array
            Pipe element mass matrix in the local coordinate system.

        See also
        --------
        mass_matrix_beam : Beam element mass matrix in the local coordinate system.
        """
        L   = self.length
        rho = self.material.density

        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2

        # Numerical integration by Gauss quadrature
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)
        
        sections = [self.first_node.cross_section, self.last_node.cross_section]
        prop_1 = [sections[0].outer_diameter, sections[1].outer_diameter]
        prop_2 = [sections[0].thickness, sections[1].thickness]

        Me = 0
        index = 0
        N = np.zeros((DOF_PER_NODE_STRUCTURAL, 2 * DOF_PER_NODE_STRUCTURAL))
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL )

        for point, weigth in zip(points, weigths):
    
            phi, _ = shape_function( point )
            N = np.c_[phi[0]*aux_eyes, phi[1]*aux_eyes]

            outer_diameter = point*((prop_1[1] - prop_1[0])/2) + ((prop_1[1] + prop_1[0])/2)
            thickness = point*((prop_2[1] - prop_2[0])/2) + ((prop_2[1] + prop_2[0])/2)

            section = sections[index]
            section.set_section_parameters([outer_diameter, thickness])
            section.update_properties()

            # Area properties - constant section along x-axis
            A = section.area
            Iy = section.second_moment_area_y
            Iz = section.second_moment_area_z
            J = section.polar_moment_area
            Ais = section.area_insulation

            rho_insulation = section.insulation_density
            if self.fluid is not None and self.adding_mass_effect:
                rho_fluid = self.fluid.density
                Ai = section.area_fluid
                Gfl = rho_fluid*np.array([[Ai, 0, 0],[0, Ai, 0],[0, 0, Ai]], dtype='float64') 
            else:
                Gfl = np.zeros((3,3), dtype='float64') 

            if self.element_type == 'pipe_1':
                Qy = 0
                Qz = 0
                Iyz = 0
                # principal_axis = section.principal_axis
            else:
                print('Only pipe_1 element types are allowed.')
            
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

            # Ggm[[0,1,2,0,4], [4,3,3,5,5]] = [Qy, -Qy, Qz, -Qz, -Iyz]
            Ggm = rho*( Ggm + Ggm.T )
            Ggm[0:3,0:3] = Ggm[0:3,0:3] + Gfl + Gis

            Me += (N.T @ Ggm @ N) * det_jacob * weigth
            index += 1
            
        return self.transf_mat_Offset.T @ Me @ self.transf_mat_Offset


    def matrices_gcs(self):
        """
        This method returns the element stiffness and mass matrices according to the 
        3D Timoshenko beam theory in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.
            
        mass : array
            Element mass matrix in the global coordinate system.

        See also
        --------
        stiffness_matrix_gcs : Element stiffness matrix in the global coordinate system.
        
        mass_matrix_gcs : Element mass matrix in the global coordinate system.
        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        if self.variable_section:
            stiffness = Rt @ self.stiffness_matrix_pipes_variable_section() @ R
            mass = Rt @ self.mass_matrix_pipes_variable_section() @ R

        else:
            stiffness = Rt @ self.stiffness_matrix_pipes() @ R
            mass = Rt @ self.mass_matrix_pipes() @ R

        return stiffness, mass


    def process_offset_transformation_matrices(self):
        """
        """
        N_dof = DOF_PER_NODE_STRUCTURAL
        E_dof = DOF_PER_ELEMENT

        cross_section_first = self.first_node.cross_section
        cross_section_last = self.last_node.cross_section
        
        yc_1, zc_1, ys_1, zs_1 = cross_section_first.get_centroide_and_shear_center()
        yc_2, zc_2, ys_2, zs_2  = cross_section_last.get_centroide_and_shear_center()        

        # delta_yc = yc_2 - yc_1
        # delta_zc = zc_2 - zc_1
        delta_ys = ys_2 - ys_1
        delta_zs = zs_2 - zs_1

        offset_first = cross_section_first.offsets
        offset_last = cross_section_last.offsets

        y1_offset, z1_offset = offset_first
        y2_offset, z2_offset = offset_last

        delta_yo = y2_offset - y1_offset
        delta_zo = z2_offset- z1_offset
        # delta_yo *= -1
        # delta_zo *= -1

        # process matrix transformation to account the shear center differences effect
        Le = self.length
        delta_xo = 0
        L_A = np.sqrt(Le**2 + delta_yo**2 + delta_zo**2)
        L_G = L_A - delta_xo
        
        L_N = Le
        # L_A = Le
        # L_G = Le
        L_B = np.sqrt(Le**2 + delta_yo**2)
        
        L_SB = np.sqrt(L_G**2 + delta_ys**2)
        L_SC = np.sqrt(L_G**2 + delta_ys**2 + delta_zs**2)

        C1 = L_SC/L_G
        C2 = -(delta_ys*L_SC)/(L_SB*L_G)
        C3 = -delta_zs/L_SB

        Rs = np.eye(N_dof, dtype=float)
        Ts_1 = np.eye(N_dof, dtype=float)
        Ts_2 = np.eye(N_dof, dtype=float)

        Rs[[3,4,5],[3,3,3]] = [C1, C2, C3]
        Ts_1[[1,2],[3,3]] = [-zs_1, ys_1]
        Ts_2[[1,2],[3,3]] = [-zs_2, ys_2]

        Sc = np.zeros((E_dof, E_dof), dtype=float)
        Sc[0:N_dof, 0:N_dof] = Rs@Ts_1
        Sc[N_dof:, N_dof:] = Rs@Ts_2

        # process matrix transformation to account the offset effect
        ro = np.array([ [      L_A/L_N, delta_yo/L_B,       (L_A*delta_zo)/(L_N*L_B)],
                        [-delta_yo/L_N,      L_A/L_B, -(delta_yo*delta_zo)/(L_N*L_B)],
                        [-delta_zo/L_N,            0,                        L_B/L_N] ])
        
        # delta_x = sqrt(Le**2 - delta_yo**2 - delta_zo**2)
        # L_ = np.sqrt(delta_x**2 + delta_yo**2)
        # L = np.sqrt(delta_x**2 + delta_yo**2 + delta_zo**2)

        # sin_delta = delta_yo / L_
        # cos_delta = delta_x / L_
        # sin_epsilon = -delta_zo / L
        # cos_epsilon = L_ / L

        # ro = np.array([ [cos_delta*cos_epsilon, -sin_delta, cos_delta*sin_epsilon],
        #                 [sin_delta*cos_epsilon,  cos_delta, sin_delta*sin_epsilon],
        #                 [         -sin_epsilon,          0,           cos_epsilon] ])
        
        # print(ro@np.array([Le,0,0]), delta_yo, delta_zo)

        Ro = np.zeros((N_dof,N_dof), dtype=float)
        Ro[0:int(N_dof/2), 0:int(N_dof/2)] = ro
        Ro[ int(N_dof/2):,  int(N_dof/2):] = ro

        To_I = np.eye(N_dof, dtype=float)
        To_J = np.eye(N_dof, dtype=float)
        To_I[[0,0,1,2],[4,5,3,3]] = [z1_offset, -y1_offset, -z1_offset, y1_offset]
        To_J[[0,0,1,2],[4,5,3,3]] = [z2_offset, -y2_offset, -z2_offset, y2_offset]

        Of = np.zeros((E_dof, E_dof), dtype=float)
        Of[0:N_dof, 0:N_dof] = To_I @ Ro
        Of[N_dof:, N_dof:] = To_J @ Ro

        self.transf_mat_Offset = Of
        self.transf_matrix_offset_shear_left = Of.T @ Sc.T
        self.transf_matrix_offset_shear_right = Sc @ Of


    def get_self_weighted_load(self, gravity_vector):
        """
        This method returns the self-weighted loads for static analysis.
        Returns
        -------
        Fe_sw : array
            Load vector due to self-weight in the global coordinate system.
        """
 
        if np.sum(gravity_vector) == 0:
            return np.zeros((12,1), dtype=float)
        #
        g = gravity_vector
        rho = self.material.density
        A = self.cross_section.area
        #
        A_fluid = A_ins = 0.
        rho_fluid = rho_ins = 0.
        if self.element_type in ["pipe_1", "valve"]:
            A_ins = self.cross_section.area_insulation
            rho_ins = self.cross_section.insulation_density
            if isinstance(self.fluid, Fluid) and self.adding_mass_effect:
                rho_fluid = self.fluid.density
                A_fluid = self.cross_section.area_fluid

        eload = (rho * A + rho_fluid * A_fluid + rho_ins * A_ins) * g

        _R = self.element_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]
        _Rt = self.element_rotation_matrix_inverse[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]

        # convert the loads to the local coordinates
        eload_lcs =  _R @ eload @ _Rt               
        eload_lcs = eload_lcs.reshape(-1, 1)

        ## Numerical integration by Gauss quadrature
        L = self.length
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        Fe_sw = 0.
        aux_eyes = np.eye(DOF_PER_NODE_STRUCTURAL, dtype=float)

        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)
            N = np.c_[phi[0] * aux_eyes, phi[1] * aux_eyes]
            Fe_sw += (N.T @ eload_lcs) * det_jacobian * weigth
        
        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        else:
            principal_axis = np.eye(DOF_PER_ELEMENT)

        if self.force_offset:
            if self.variable_section:
                return self.transf_matrix_offset_shear_left @ Fe_sw
            else:
                return principal_axis.T @ Fe_sw
        else:
            return Fe_sw


    def get_distributed_load(self, rot_matrix: np.ndarray):
        """
        This method returns the element load vector in the local coordinate system. The loads are forces and moments according to the degree of freedom.

        Returns
        -------
        force : array
            Load in the local coordinate system.

        Raises
        ------
        TypeError
            Only pipe_1 element type is allowed.
        """

        _R = self.element_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]
        _Rt = self.element_rotation_matrix_inverse[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]
        
        # convert the loads to the local coordinates
        eload_lcs =  _R @ self.loaded_forces @ _Rt               
        eload_lcs = eload_lcs.reshape(-1, 1)

        ## Numerical integration by Gauss quadrature
        L = self.length
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        Fe = 0
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL, dtype=float)
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)
            N = np.c_[phi[0]*aux_eyes, phi[1]*aux_eyes] 
            Fe += (N.T @ eload_lcs) * det_jacobian * weigth
        
        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        else:
            return np.zeros((DOF_PER_ELEMENT, 1), dtype=float)
        
        if self.force_offset:
            if self.variable_section:
                return self.transf_matrix_offset_shear_left @ Fe
            else:
                return principal_axis.T @ Fe
        else:
            return Fe


    def force_vector_acoustic_gcs(self, frequencies, pressures, pressure_external):
        """
        This method returns the element load vector due to the internal acoustic pressure field in the global 
        coordinate system. The loads are forces and moments according to the degree of freedom. 

        Parameters
        ----------
        frequencies : array
            Frequencies of analysis in Hertz.
        
        pressure_avg : array
            The average between the pressure at the first node and last node of the element. 

        Returns
        -------
        force : array
            Load vector in the global coordinate system.
        """
        rows = DOF_PER_ELEMENT
        cols = len(frequencies)
        Do = self.cross_section.outer_diameter
        Di = self.cross_section.inner_diameter

        nu = self.material.poisson_ratio
        A = self.cross_section.area

        # p_avg = (pressures[0]+pressures[1])/2
        if self.capped_end:
            capped_end = 1
        else:
            capped_end = 0

        # print(f"-> capped_end [{self.index}]: {self.capped_end} / {capped_end}")

        if self.element_type == 'pipe_1':

            stress_axial = (pressures * Di**2 - pressure_external * Do**2) / (Do**2 - Di**2)
            if self.wall_formulation == "thick_wall": 
                force = A * (capped_end - 2*nu) * stress_axial
            elif self.wall_formulation == "thin_wall":
                force = A * (capped_end*stress_axial - nu*pressures*(Do/(Do-Di) - 1))
            else:
                raise TypeError('Only thin and thick wall formulation types are allowable.')

        elif self.element_type in ['expansion_joint','valve']:
            nu = 0
            force = A * (capped_end - 2*nu) * pressures

        else:
            return np.zeros((rows, cols))

        aux = np.zeros((rows, cols), dtype=complex)
        aux[0,:] = -force[0,:]
        aux[6,:] =  force[1,:]

        R = self.element_rotation_matrix

        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type in ['expansion_joint', 'valve']:
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            raise TypeError(f'Invalid element type: {self.element_type}')

        if self.force_offset:
            if self.variable_section:
                if self.transf_matrix_offset_shear_left is None:
                    self.process_offset_transformation_matrices()
                return R.T @ self.transf_matrix_offset_shear_left @ aux
            else:
                return R.T @ principal_axis.T @ aux
        else:
            return R.T @ aux


    def force_vector_stress_stiffening(self, vector_gcs: bool = True):
        """
        This method returns description
        Returns
        -------
        S : array
            Load vector in the global coordinate system.
        """

        rows = DOF_PER_ELEMENT
        aux = np.zeros([rows, 1])

        D_out = self.cross_section.outer_diameter
        D_in = self.cross_section.inner_diameter
        A = self.cross_section.area
        nu = self.material.poisson_ratio

        P_in = self.internal_pressure
        P_out = self.external_pressure

        if self.element_type in ['pipe_1', 'valve']:
            axial_stress = (P_in*(D_in**2) - P_out*(D_out**2))/((D_out**2) - (D_in**2))
        else:
            return aux

        if self.capped_end:
            capped_end = 1
        else:
            capped_end = 0

        if self.element_type in ['pipe_1', 'valve']:
            principal_axis = self.cross_section.principal_axis
        else:
            raise TypeError(f'Invalid element type: {self.element_type}')

        aux[0], aux[6] = -1, 1
        R = self.element_rotation_matrix

        if vector_gcs:
            if self.force_offset:
                aux = R.T @ (principal_axis.T @ aux)
            else:
                aux = R.T @ aux
        else:
            aux = 1
            capped_end = 0

        if self.wall_formulation == "thick_wall":
            return (capped_end - 2*nu) * axial_stress * A * aux
        elif self.wall_formulation == "thin_wall":
            return (capped_end*axial_stress - nu*((P_in*D_out/(D_out-D_in))-P_in)) * A * aux
        else:
            raise TypeError('Only thin and thick wall formulation types are allowable.')


def gauss_quadrature(integration_points):
    """
    This method returns the Gauss quadrature data.  

    Parameters
    -------
    integration_points : int
        Number of integration points.

    Returns
    -------
    points : array
        Integration points in the normalized domain [-1,1].

    weigths : array
        Weigths of the respective integration points in the sum approximation.

    Raises
    ------
    TypeError
        Only 1, 2, and 3 integration points are supported.
    """
    if integration_points == 1:
        points = [0]
        weigths = [2]
    elif integration_points == 2:
        points = [-1/np.sqrt(3), 1/np.sqrt(3)]
        weigths = [1, 1]
    elif integration_points == 3:
        points = [-np.sqrt(3/5), 0, np.sqrt(3/5)]
        weigths = [5/9, 8/9, 5/9]
    else:
        raise TypeError('You must provide 1, 2, or 3 integration points')
    return points, weigths

def shape_function(ksi):
    """ This function returns the one dimensional linear shape function and its derivative.

    Parameters
    ----------
    float in [-1,1]
        Dimensionless coordinate.

    Returns
    -------
    phi : array
        One dimensional linear shape function.

    derivative_phi : array
        Shape function derivative.
    """
    phi = np.array([(1 - ksi)/2, (1 + ksi)/2])
    derivative_phi = np.array([-0.5, 0.5])
    return phi, derivative_phi
