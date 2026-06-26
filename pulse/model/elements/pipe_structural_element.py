from typing import TYPE_CHECKING

import numpy as np

from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.model.properties.fluid import Fluid
from pulse.model.elements.structural_element import StructuralElement, gauss_quadrature, shape_function

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2


class PipeStructuralElement(StructuralElement):
    def __init__(self, element_attributes: ElementAttributes, **kwargs):
        super().__init__(element_attributes, **kwargs)


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

        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        if self.element_attributes.is_section_variable:
            stiffness = Rt @ self.stiffness_matrix_pipes_variable_section() @ R
            mass = Rt @ self.mass_matrix_pipes_variable_section() @ R

        else:
            stiffness = Rt @ self.stiffness_matrix_pipes() @ R
            mass = Rt @ self.mass_matrix_pipes() @ R

        return stiffness, mass


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

        material = self.material
        cross_section = self.cross_section

        E = material.elasticity_modulus
        mu = material.mu_parameter
                   
        # Area properties - constant section along x-axis
        A = cross_section.area
        Iy = cross_section.second_moment_area_y
        Iz = cross_section.second_moment_area_z
        J = cross_section.polar_moment_area
        res_y = cross_section.res_y
        res_z = cross_section.res_z
    
        # Shear coefficiets
        aly = 1 / res_y
        alz = 1 / res_z

        if self.structural_element_type in ['pipe_1', 'valve']:
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = cross_section.principal_axis
        else:
            print('Only pipe_1 element types are allowed.')
            
        # Determinant of Jacobian (linear 1D trasform)
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        # Constitutive matrices (element with constant geometry along x-axis)
        # Torsion and shear
        Dts = mu*np.array([ 
            [J  ,   -Qy,    Qz],
            [-Qy, aly*A,     0],
            [Qz ,     0, alz*A],
            ], dtype=float)

        self._Dts = Dts

        # Axial and Bending
        Dab = E*np.array([  
            [A  ,   Qy,  -Qz],
            [Qy ,   Iy, -Iyz],
            [-Qz, -Iyz,   Iz],
            ], dtype=float)

        self._Dab = Dab

        ## Numerical integration by Gauss quadrature
        integrations_points = 1
        points, weigths = gauss_quadrature(integrations_points)

        Kabe = 0.
        Ktse = 0.

        Ue = np.zeros(DOF_PER_ELEMENT, dtype=float)
        K_geo = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        if self.element_attributes.static_analysis_evaluated:
            self.element_attributes.static_analysis_evaluated = False
            Ue = self.static_element_results_lcs()
            Te = self.compute_Te_matrix()
            Fp_x = self.force_vector_stress_stiffening(vector_gcs=False)
            Te = (E * A / L) * (Ue[6] - Ue[0]) - Fp_x
            K_geo = (Te / L) * Te

        for point, weigth in zip(points, weigths):

            # Shape function and its derivative
            phi, derivative_phi = shape_function( point )
            dphi = inv_jacob * derivative_phi

            # Axial and Bending B-matrix
            Bab = np.zeros([3, 12])
            Bab[[0, 1, 2], [0, 4, 5]] = dphi[0]  # 1st node
            Bab[[0, 1, 2], [6, 10, 11]] = dphi[1]  # 2nd node
            self._Bab = Bab

            # Torsional and Shear B-matrix
            Bts = np.zeros((3, 12))
            Bts[[0, 1, 2], [3, 1, 2]] = dphi[0]  # 1st node
            Bts[[1], [5]] = -phi[0]
            Bts[[2], [4]] = phi[0]
            Bts[[0, 1, 2], [9, 7, 8]] = dphi[1]  # 2nd node
            Bts[[1], [11]] = -phi[1]
            Bts[[2], [10]] = phi[1]
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

        fluid = self.fluid
        material = self.material
        cross_section = self.cross_section

        rho = material.density

        # Area properties - constant section along x-axis
        A = cross_section.area
        Iy = cross_section.second_moment_area_y
        Iz = cross_section.second_moment_area_z
        J = cross_section.polar_moment_area
        Ais = cross_section.area_insulation

        if isinstance(fluid, Fluid) and self.element_attributes.adding_mass_effect:
            rho_fluid = fluid.density
            Ai = cross_section.area_fluid
            Gfl = rho_fluid * np.array([
                [Ai, 0, 0],
                [0, Ai, 0],
                [0, 0, Ai]
                ], dtype='float64')

        else:
            Gfl = np.zeros((3, 3), dtype='float64') 

        if self.structural_element_type == 'pipe_1':
            Qy = 0
            Qz = 0
            Iyz = 0
            principal_axis = cross_section.principal_axis
        else:
            print('Only pipe_1 element types are allowed.')

        # Determinant of Jacobian (linear 1D trasform)
        L = self.length
        det_jacob = L / 2

        #Fluid/Insulation inertia effects
        rho_insulation = cross_section.insulation_density
        Gis = rho_insulation * np.array([
            [Ais, 0, 0],
            [0, Ais, 0],
            [0, 0, Ais]
            ], dtype='float64')

        # Inertial matrices
        Ggm = np.zeros((6, 6), dtype=float)
        Ggm[np.diag_indices(6)] = np.array([A, A, A, J, Iy, Iz]) / 2
        Ggm[0, 4] = Qy
        Ggm[1, 3] = -Qy
        Ggm[2, 3] = Qz
        Ggm[0, 5] = -Qz
        Ggm[4, 5] = -Iyz
        Ggm = rho * (Ggm + Ggm.T)

        # Ggm = rho * np.array([
        #     [  A,   0,   0,   0,   Qy,  -Qz],
        #     [  0,   A,   0, -Qy,    0,    0],
        #     [  0,   0,   A,  Qz,    0,    0],
        #     [  0, -Qy,  Qz,   J,    0,    0],
        #     [ Qy,   0,   0,   0,   Iy, -Iyz],
        #     [-Qz,   0,   0,   0, -Iyz,   Iz],
        #     ], dtype=float)
        # Ggm[0:3,0:3] += Gfl + Gis

        Ggm[0:3,0:3] = Ggm[0:3,0:3] + Gfl + Gis

        # Numerical integration by Gauss quadrature
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)

        Me = 0
        N = np.zeros((DOF_PER_NODE_STRUCTURAL, 2 * DOF_PER_NODE_STRUCTURAL))
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL )
        
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)
            N = np.c_[phi[0] * aux_eyes, phi[1] * aux_eyes]
            Me += (N.T @ Ggm @ N) * det_jacob * weigth

        return principal_axis.T @ Me @ principal_axis
    

    def compute_Te_matrix(self):
        """
        This method computes the Te matrix for stress stiffening updating.
        """

        L = self.length

        material = self.material
        cross_section = self.cross_section

        E = material.elasticity_modulus
        G = material.shear_modulus
                   
        # Area properties - constant section along x-axis
        A = cross_section.area
        Iy = cross_section.second_moment_area_y
        Iz = cross_section.second_moment_area_z
        J = cross_section.polar_moment_area
        res_y = cross_section.res_y
        res_z = cross_section.res_z
    
        # Shear coefficiets
        aly = 1 / res_y
        alz = 1 / res_z

        key = 1

        # Variables related to prestress effect
        Phi_y = key * (12 * E * Iz) / (G * aly * A * L**2)
        Phi_z = key * (12 * E * Iy) / (G * alz * A * L**2)
        Jx_Ax = key * J / A
               
        den_y = (1 + Phi_y)**2
        den_z = (1 + Phi_z)**2

        Te_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        Te_matrix[[1, 2, 7, 8], [1, 2, 7, 8]] = [
            (6 / 5 + 2 * Phi_y + Phi_y**2) / den_y,
            (6 / 5 + 2 * Phi_z + Phi_z**2) / den_z,
            (6 / 5 + 2 * Phi_y + Phi_y**2) / den_y,
            (6 / 5 + 2 * Phi_z + Phi_z**2) / den_z,
        ]

        Te_matrix[[1, 2, 7, 8], [7, 8, 1, 2]] = [
            -(6 / 5 + 2 * Phi_y + Phi_y**2) / den_y,
            -(6 / 5 + 2 * Phi_z + Phi_z**2) / den_z,
            -(6 / 5 + 2 * Phi_y + Phi_y**2) / den_y,
            -(6 / 5 + 2 * Phi_z + Phi_z**2) / den_z,
        ]

        Te_matrix[[3, 3, 9, 9], [3, 9, 3, 9]] = [Jx_Ax, -Jx_Ax, -Jx_Ax, Jx_Ax]

        Te_matrix[[4, 5, 10, 11], [4, 5, 10, 11]] = [
            (L**2) * ((2 / 15) + (Phi_z / 6) + ((Phi_z**2) / 12)) / den_z,
            (L**2) * ((2 / 15) + (Phi_y / 6) + ((Phi_y**2) / 12)) / den_y,
            (L**2) * ((2 / 15) + (Phi_z / 6) + ((Phi_z**2) / 12)) / den_z,
            (L**2) * ((2 / 15) + (Phi_y / 6) + ((Phi_y**2) / 12)) / den_y,
        ]

        Te_matrix[[4, 5, 10, 11], [10, 11, 4, 5]] = [
            -(L**2) * ((1 / 30) + (Phi_z / 6) + ((Phi_z**2) / 12)) / den_z,
            -(L**2) * ((1 / 30) + (Phi_y / 6) + ((Phi_y**2) / 12)) / den_y,
            -(L**2) * ((1 / 30) + (Phi_z / 6) + ((Phi_z**2) / 12)) / den_z,
            -(L**2) * ((1 / 30) + (Phi_y / 6) + ((Phi_y**2) / 12)) / den_y,
        ]

        Te_matrix[[1, 1, 5, 11], [5, 11, 1, 1]] = [L / (10 * den_y), L / (10 * den_y), L / (10 * den_y), L / (10 * den_y)]

        Te_matrix[[4, 8, 8, 10], [8, 4, 10, 8]] = [L / (10 * den_z), L / (10 * den_z), L / (10 * den_z), L / (10 * den_z)]

        Te_matrix[[5, 7, 7, 11], [7, 5, 11, 7]] = [-L / (10 * den_y), -L / (10 * den_y), -L / (10 * den_y), -L / (10 * den_y)]

        Te_matrix[[2, 2, 4, 10], [4, 10, 2, 2]] = [-L / (10 * den_z), -L / (10 * den_z), -L / (10 * den_z), -L / (10 * den_z)]
        
        return Te_matrix


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

        material = self.material
        # cross_section = self.cross_section

        E = material.elasticity_modulus
        mu = material.mu_parameter

        self.process_offset_transformation_matrices()

        ## Numerical integration by Gauss quadrature
        integrations_points = 1
        points, weigths = gauss_quadrature(integrations_points)

        # Determinant of Jacobian (linear 1D trasform)
        L = self.length
        det_jacob = L / 2
        inv_jacob = 1 / det_jacob

        index = 0
        Kabe = 0.
        Ktse = 0.

        sections = [self.first_node.cross_section, self.last_node.cross_section]
        prop_1 = [sections[0].outer_diameter, sections[1].outer_diameter]
        prop_2 = [sections[0].thickness, sections[1].thickness]

        for point, weigth in zip(points, weigths):

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
            aly = 1 / res_y
            alz = 1 / res_z
            
            if self.structural_element_type in ['pipe_1', 'valve']:
                Qy = 0
                Qz = 0
                Iyz = 0
                # principal_axis = section.principal_axis

            else:
                print('Only pipe_1 element types are allowed.')

            Ue = np.zeros(DOF_PER_ELEMENT, dtype=float)
            K_geo = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

            if self.element_attributes.static_analysis_evaluated:
                self.element_attributes.static_analysis_evaluated = False
                Ue = self.static_element_results_lcs()
                mat_K_geo = self.compute_Te_matrix()
                Fp_x = self.force_vector_stress_stiffening(vector_gcs=False)
                Te = (E * A / L) * (Ue[6] - Ue[0]) - Fp_x
                K_geo = (Te / L) * mat_K_geo

            # if self.index in [12]:
            #     # print("\nElement 12:")
            #     # print("UX(11):", self.first_node.static_nodal_solution_gcs[0])
            #     # print("UX(12):", self.last_node.static_nodal_solution_gcs[0])
            #     print(f"Te: {Te}")

            # Constitutive matrices (element with constant geometry along x-axis)
            # Torsion and shear
            Dts = mu * np.array([ 
                [  J,   -Qy,    Qz],
                [-Qy, aly*A,     0],
                [ Qz,     0, alz*A],
                ], dtype=float)
            
            self._Dts = Dts

            # Axial and Bending
            Dab = E*np.array([  
                [A  ,   Qy,  -Qz],
                [Qy ,   Iy, -Iyz],
                [-Qz, -Iyz,   Iz],
                ], dtype=float)

            self._Dab = Dab

            # Axial and Bending B-matrix
            Bab = np.zeros([3, 12], dtype=float)
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


    def mass_matrix_pipes_variable_section(self, element_attributes):
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
        L = self.length

        fluid = self.fluid
        material = self.material
        # cross_section = self.cross_section

        rho = material.density

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
            if isinstance(fluid, Fluid) and element_attributes.adding_mass_effect:
                rho_fluid = fluid.density
                Ai = section.area_fluid
                Gfl = rho_fluid*np.array([
                    [Ai, 0, 0],
                    [0, Ai, 0],
                    [0, 0, Ai]
                    ], dtype='float64')

            else:
                Gfl = np.zeros((3,3), dtype='float64') 

            if self.structural_element_type == 'pipe_1':
                Qy = 0
                Qz = 0
                Iyz = 0
                # principal_axis = section.principal_axis
            else:
                print('Only pipe_1 element types are allowed.')
            
            #Fluid/Insulation inertia effects
            Gis = rho_insulation * np.array([
                [Ais, 0, 0],
                [0, Ais, 0],
                [0, 0, Ais]
                ], dtype='float64')

            # Inertial matrices
            Ggm = np.zeros([6, 6])
            Ggm[np.diag_indices(6)] = np.array([A, A, A, J, Iy, Iz]) / 2
            
            Ggm[0, 4] = Qy
            Ggm[1, 3] = -Qy
            Ggm[2, 3] = Qz
            Ggm[0, 5] = -Qz
            Ggm[4, 5] = -Iyz

            # Ggm[[0,1,2,0,4], [4,3,3,5,5]] = [Qy, -Qy, Qz, -Qz, -Iyz]
            Ggm = rho * ( Ggm + Ggm.T )
            Ggm[0:3,0:3] = Ggm[0:3,0:3] + Gfl + Gis

            Me += (N.T @ Ggm @ N) * det_jacob * weigth
            index += 1
            
        return self.transf_mat_Offset.T @ Me @ self.transf_mat_Offset