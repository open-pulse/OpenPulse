from math import pi, sqrt, sin, cos
from pulse.preprocessing.acoustic_element import DOF_PER_NODE
import numpy as np

from pulse.preprocessing.node import Node, distance, DOF_PER_NODE_STRUCTURAL

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

decoupling_matrix = np.ones((DOF_PER_ELEMENT,DOF_PER_ELEMENT), dtype=int)
zeros_3x3 = np.zeros((3,3), dtype=float)

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
        points = [-1/sqrt(3), 1/sqrt(3)]
        weigths = [1, 1]
    elif integration_points == 3:
        points = [-sqrt(3/5), 0, sqrt(3/5)]
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

def symmetrize(a):
    """ This function receives matrix and makes it symmetric.

    Parameters
    ----------
    array
        Matrix.

    Returns
    -------
    array
        Symmetric matrix.    
    """
    return a + a.T - np.diag(a.diagonal())
class StructuralElement:
    """A structural element.
    This class creates a structural element from input data.

    Parameters
    ----------
    first_node : Node object
        Fist node of element.

    last_node : Node object
        Last node of element.

    index : int
        Element index.

    element_type : str, ['pipe_1', 'pipe_2', 'beam_1', 'expansion_joint', 'valve'], optional
        Element type
        Default is 'pipe_1'.

    material : Material object, optional
        Element structural material.
        Default is 'None'.

    fluid : Fluid object, optional
        Element acoustic fluid.
        Default is 'None'.

    cross_section : CrossSection object, optional
        Element cross section.
        Default is 'None'.

    loaded_forces : array, optional
        Structural forces and moments on the nodes.
        Default is zeros(12).
    """
    def __init__(self, first_node, last_node, index, **kwargs):

        self.first_node = first_node
        self.last_node = last_node
        self.index = index

        self.element_type = kwargs.get('element_type', 'pipe_1')
        self.wall_formulation = kwargs.get('wall_formulation', 'thick_wall')
        self.material = kwargs.get('material', None)
        self.cross_section = kwargs.get('cross_section', None)
        self.cross_section_points = kwargs.get('cross_section_points', None)
        self.loaded_forces = kwargs.get('loaded_forces', np.zeros(DOF_PER_NODE_STRUCTURAL))
        self.fluid = kwargs.get('fluid', None)
        self.adding_mass_effect = kwargs.get('adding_mass_effect', False)
        self.decoupling_matrix = kwargs.get('decoupling_matrix', decoupling_matrix)
        self.decoupling_info = kwargs.get('decoupling_info', None)

        self.capped_end = kwargs.get('capped_end', False)
        self.stress_intensification = kwargs.get('stress_intensification', True)
        self.wall_formutation_type = kwargs.get('wall_formutation_type', "thick wall")
        self.force_offset = True

        self.section_rotation_xyz_undeformed = None
        self.deformed_rotation_xyz = None
        self.deformed_length = None
        self.xaxis_beam_rotation = 0
        
        self.internal_pressure = 0
        self.external_pressure = 0
        self.reset_expansion_joint_parameters()
        self.reset_valve_parameters()

        self.delta_x = self.last_node.x - self.first_node.x
        self.delta_y = self.last_node.y - self.first_node.y
        self.delta_z = self.last_node.z - self.first_node.z

        self.element_center_coordinates = np.array([(self.last_node.x + self.first_node.x)/2, 
                                                    (self.last_node.y + self.first_node.y)/2,
                                                    (self.last_node.z + self.first_node.z)/2], dtype=float)

        self._Dab = None
        self._Bab = None
        self._Dts = None
        self._Bts = None
        self._rot = None

        self.sub_transformation_matrix = None
        self.sub_inverse_rotation_matrix = None
        self.section_directional_vectors = None
        self.mean_rotation_results = None
        self.rotation_matrix_results_at_lcs = None

        self.results_at_global_coordinate_system = None

        self.stress = None
        self.internal_load = None
        self.static_analysis_evaluated = False
        self.perforated_plate = None
        self.valve_parameters = None
        self.variable_section = False

    @property
    def length(self):
        """
        This method returns the element length.

        Returns
        -------
        float
            Element length.
        """
        return distance(self.first_node, self.last_node) 

    @property
    def global_dof(self):
        """
        This method returns the element global degrees of freedom. The 3D Timoshenko beam theory implemented takes into account the three node's translations and the three node's rotations.

        Returns
        -------
        list
            Element global degrees of freedom.
        """
        global_dof = np.zeros(DOF_PER_ELEMENT, dtype=int)
        global_dof[:DOF_PER_NODE_STRUCTURAL] = self.first_node.global_dof
        global_dof[DOF_PER_NODE_STRUCTURAL:] = self.last_node.global_dof
        return global_dof

    # @property
    # def local_dof(self):
    #     return np.arange(DOF_PER_ELEMENT, dtype=int)

    def element_results_gcs(self):
        values = np.zeros(DOF_PER_ELEMENT, dtype=float)
        values[:DOF_PER_NODE_STRUCTURAL] = self.first_node.nodal_solution_gcs
        values[DOF_PER_NODE_STRUCTURAL:] = self.last_node.nodal_solution_gcs
        return values

    def element_results_lcs(self):
        return self.element_rotation_matrix@self.element_results_gcs()
    
    def static_element_results_gcs(self):
        values = np.zeros(DOF_PER_ELEMENT, dtype=float)
        values[:DOF_PER_NODE_STRUCTURAL] = self.first_node.static_nodal_solution_gcs
        values[DOF_PER_NODE_STRUCTURAL:] = self.last_node.static_nodal_solution_gcs
        return values

    def static_element_results_lcs(self):
        return self.element_rotation_matrix@self.static_element_results_gcs()

    def mean_element_results(self):
        results_gcs = self.element_results_gcs()
        results_first_node = results_gcs[:DOF_PER_NODE_STRUCTURAL]
        results_last_node = results_gcs[DOF_PER_NODE_STRUCTURAL:]
        return (results_first_node+results_last_node)/2
        # u_x = (results_gcs[0] + results_gcs[-6])/2
        # u_y = (results_gcs[1] + results_gcs[-5])/2
        # u_z = (results_gcs[2] + results_gcs[-4])/2       
        # theta_x = (results_gcs[3] + results_gcs[-3])/2
        # tehta_y = (results_gcs[4] + results_gcs[-2])/2
        # tehta_z = (results_gcs[5] + results_gcs[-1])/2
        # return np.array([u_x, u_y, u_z, theta_x, tehta_y, tehta_z], dtype=float)

    def mean_rotations_at_global_coordinate_system(self):
        results_gcs = self.element_results_gcs()
        theta_x = (results_gcs[3] + results_gcs[-3])/2
        tehta_y = (results_gcs[4] + results_gcs[-2])/2
        tehta_z = (results_gcs[5] + results_gcs[-1])/2
        return np.array([theta_x, tehta_y, tehta_z], dtype=float)

    def mean_rotations_at_local_coordinate_system(self):
        results_lcs = self.element_results_lcs()
        theta_x = (results_lcs[3] + results_lcs[-3])/2
        tehta_y = (results_lcs[4] + results_lcs[-2])/2
        tehta_z = (results_lcs[5] + results_lcs[-1])/2
        return np.array([theta_x, tehta_y, tehta_z], dtype=float)

    def section_normal_vectors_at_lcs(self):
        theta_x, theta_y, theta_z = self.mean_rotations_at_local_coordinate_system()
        L_ = np.sqrt(1-(np.sin(theta_y)**2))
        L = 1
        dx = L_*np.cos(theta_z)
        dy = L_*np.sin(theta_z)
        dz = -L*np.sin(theta_y)
        uvw = np.array([dx, dy*np.cos(theta_x) - dz*np.sin(theta_x), dy*np.sin(theta_x) + dz*np.cos(theta_x)], dtype=float)   
        return uvw

    def deformed_element_length(self, delta):
        self.deformed_length = (delta[0]**2 + delta[1]**2 + delta[2]**2)**(1/2)
        
    def global_matrix_indexes(self):
        """
        This method returns the indexes of the rows and columns that place the element matrices into the global matrices according to the element global degrees of freedom.

        Returns
        -------
        rows : array
            Indexes of the rows. It's a matrix with dimension 12 by 12 constant through the rows.
            
        cols : array
            Indexes of the columns. It's a matrix with dimension 12 by 12 constant through the columns.
        """
        rows = self.global_dof.reshape(DOF_PER_ELEMENT, 1) @ np.ones((1, DOF_PER_ELEMENT))
        cols = rows.T
        return rows.reshape(-1), cols.reshape(-1)

    def matrices_gcs(self):
        """
        This method returns the element stiffness and mass matrices according to the 3D Timoshenko beam theory in the global coordinate system.

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
        self._rot = R = self.element_rotation_matrix = self._element_rotation_matrix()
        Rt = self.transpose_rotation_matrix = self.element_rotation_matrix.T
        if self.element_type in ['pipe_1','pipe_2']:
            if self.variable_section:
                stiffness = Rt @ self.stiffness_matrix_pipes_variable_section() @ R
                mass = Rt @ self.mass_matrix_pipes_variable_section() @ R
            else:
                stiffness = Rt @ self.stiffness_matrix_pipes() @ R
                mass = Rt @ self.mass_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            stiffness = Rt @ self.stiffness_matrix_beam() @ R
            mass = Rt @ self.mass_matrix_beam() @ R
        elif self.element_type in ['valve']:
            stiffness = Rt @ self.stiffness_matrix_pipes()*self.valve_stiffening_factor @ R
            mass = Rt @ self.mass_matrix_valve() @ R   
        # elif self.element_type == "expansion_joint":
        #     stiffness = Rt @ self.stiffness_matrix_expansion_joint() @ R
        #     mass = Rt @ self.mass_matrix_expansion_joint() @ R            
        return stiffness, mass

    def expansion_joint_matrices_gcs(self, frequencies=None):
        """
        This method returns the element stiffness and mass matrices according to the 3D Timoshenko beam theory in the global coordinate system.

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
        self._rot = R = self.element_rotation_matrix = self._element_rotation_matrix()
        Rt = self.transpose_rotation_matrix = self.element_rotation_matrix.T
        if self.element_type == "expansion_joint":
            stiffness = Rt @ self.stiffness_matrix_expansion_joint_harmonic(frequencies=frequencies) @ R
            mass = Rt @ self.mass_matrix_expansion_joint() @ R            
        return stiffness, mass

    def stiffness_matrix_gcs(self, frequencies=None):
        """
        This method returns the element stiffness matrix according to the 3D Timoshenko beam theory in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.

        See also
        --------
        matrices_gcs : Element stiffness and mass matrices in the global coordinate system.
        
        mass_matrix_gcs : Element mass matrix in the global coordinate system.

        stiffness_matrix_pipes : Pipe element stiffness matrix in the local coordinate system.

        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """
        R = self.element_rotation_matrix
        Rt = self.transpose_rotation_matrix
        if self.element_type in ['pipe_1','pipe_2']:
            if self.variable_section:
                return Rt @ self.stiffness_matrix_pipes_variable_section() @ R
            else:
                return Rt @ self.stiffness_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            return Rt @ self.stiffness_matrix_beam() @ R
        elif self.element_type in ['valve']:
            return Rt @ self.stiffness_matrix_pipes()*self.valve_stiffening_factor @ R
        elif self.element_type == "expansion_joint":
            return Rt @ self.stiffness_matrix_expansion_joint_harmonic(frequencies=frequencies) @ R
            
    def mass_matrix_gcs(self):
        """
        This method returns the element mass matrix according to the 3D Timoshenko beam theory in the global coordinate system.

        Returns
        -------
        mass : array
            Element mass matrix in the global coordinate system.

        See also
        --------
        matrices_gcs : Element stiffness and mass matrices in the global coordinate system.

        stiffness_matrix_gcs : Element stiffness matrix in the global coordinate system.
        """
        R = self.element_rotation_matrix
        Rt = self.transpose_rotation_matrix
        if self.element_type in ['pipe_1','pipe_2']:
            if self.variable_section:
                return Rt @ self.mass_matrix_pipes_variable_section() @ R
            else:
                return Rt @ self.mass_matrix_pipes() @ R
        elif self.element_type in ['beam_1']:
            return Rt @ self.mass_matrix_beam() @ R
        elif self.element_type in ['valve']:
            return Rt @ self.mass_matrix_valve() @ R
        elif self.element_type == "expansion_joint":
            return Rt @ self.mass_matrix_expansion_joint() @ R  

    def force_vector_gcs(self):
        """
        This method returns the element force vector in the global coordinate system.

        Returns
        -------
        array
            Force vector in the global coordinate system.
        """
        Rt = self.transpose_rotation_matrix
        return Rt @ self.force_vector()

    def _element_rotation_matrix(self):
        """
        This method returns the transformation matrix that perform a rotation from the element's local coordinate system to the global coordinate system.

        Returns
        -------
        array
            Rotation matrix
        """
        R = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        # self.sub_transformation_matrix = _rotation_matrix(self.delta_x, self.delta_y, self.delta_z)
        R[0:3, 0:3] = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = self.sub_transformation_matrix
        return R
    
    def _inverse_element_rotation_matrix(self):
        R = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        R[0:3, 0:3] = R[3:6, 3:6] = R[6:9, 6:9] = R[9:12, 9:12] = self.sub_inverse_rotation_matrix
        return R

    def get_local_coordinate_system_info(self):
        """
        This method returns the coordinates of the element center and its local coordinate system.

        Returns
        -------
        element_center_coordinates: array
            Coordinates of element center.

        directional_vectors: array
            Element local coordinate system.
        """
        # invR = np.linalg.inv(self.sub_transformation_matrix)
        # u = invR@np.array([1,0,0])
        # v = invR@np.array([0,1,0])
        # w = invR@np.array([0,0,1])
        # invR = inverse_matrix_3x3(self.sub_transformation_matrix)
        # u ,v, w = invR.T
        # self.section_directional_vectors = [u, v, w]
        return self.element_center_coordinates, self.section_directional_vectors 

    def stiffness_matrix_pipes(self):
        """
        This method returns the pipe element stiffness matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        stiffness : array
            Pipe element stiffness matrix in the local coordinate system.

        See also
        --------
        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """
        L = self.length

        E = self.material.young_modulus
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
        aly = 1/res_y
        alz = 1/res_z
        
        if self.element_type in ['pipe_1', 'valve']:
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
        points, weigths = gauss_quadrature( integrations_points )

        Kabe = 0.
        Ktse = 0.

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
        This method returns the pipe element mass matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is optimized for pipe cross section data.

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

        # Numerical integration by Gauss quadrature
        integrations_points = 2
        points, weigths = gauss_quadrature( integrations_points )

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
        This method returns the pipe element stiffness matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is optimized for pipe cross section data.

        Returns
        -------
        stiffness : array
            Pipe element stiffness matrix in the local coordinate system.

        See also
        --------
        stiffness_matrix_beam : Beam element stiffness matrix in the local coordinate system.
        """
        L = self.length

        E = self.material.young_modulus
        mu = self.material.mu_parameter
        G = self.material.shear_modulus
        
        self.process_offset_transformation_matrices()
                            
        ## Numerical integration by Gauss quadrature
        integrations_points = 1
        points, weigths = gauss_quadrature( integrations_points )

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
            elif self.element_type == 'pipe_2':
                Qy = section.first_moment_area_y
                Qz = section.first_moment_area_z
                Iyz = section.second_moment_area_yz
                # principal_axis = np.eye(DOF_PER_ELEMENT)
            else:
                print('Only pipe_1 and pipe_2 element types are allowed.')
                pass
                
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

        return self.transf_mat_OffsetShear_left @ Ke @ self.transf_mat_OffsetShear_right


    def mass_matrix_pipes_variable_section(self):
        """
        This method returns the pipe element mass matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is optimized for pipe cross section data.

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
        points, weigths = gauss_quadrature( integrations_points )
        
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
            elif self.element_type == 'pipe_2':
                Qy = section.first_moment_area_y
                Qz = section.first_moment_area_z
                Iyz = section.second_moment_area_yz
                # principal_axis = np.eye(DOF_PER_ELEMENT)
            else:
                print('Only pipe_1 and pipe_2 element types are allowed.')
                pass
            
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


    def process_offset_transformation_matrices(self):
        """
        """

        N_dof = DOF_PER_NODE_STRUCTURAL
        E_dof = DOF_PER_ELEMENT

        cross_section_first = self.first_node.cross_section
        cross_section_last = self.last_node.cross_section
        
        yc_1, zc_1, ys_1, zs_1 = cross_section_first.get_centroide_and_shear_center()
        yc_2, zc_2, ys_2, zs_2  = cross_section_last.get_centroide_and_shear_center()        

        delta_yc = yc_2 - yc_1
        delta_zc = zc_2 - zc_1
        delta_ys = ys_2 - ys_1
        delta_zs = zs_2 - zs_1

        offset_first = cross_section_first.offset
        offset_last = cross_section_last.offset

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
        # L_ = sqrt(delta_x**2 + delta_yo**2)
        # L = sqrt(delta_x**2 + delta_yo**2 + delta_zo**2)

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
        Of[0:N_dof, 0:N_dof] = To_I@Ro
        Of[N_dof:, N_dof:] = To_J@Ro

        self.transf_mat_Offset = Of
        self.transf_mat_OffsetShear_left = Of.T@Sc.T
        self.transf_mat_OffsetShear_right = Sc@Of


    def force_vector(self):
        """
        This method returns the element load vector in the local coordinate system. The loads are forces and moments according to the degree of freedom.

        Returns
        -------
        force : array
            Load in the local coordinate system.

        Raises
        ------
        TypeError
            Only pipe_1 and pipe_2 element types are allowed.
        """
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
            Fe += (N.T @ self.loaded_forces.T) * det_jacobian * weigth
        
        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            raise TypeError('Only pipe_1 and pipe_2 element types are allowed.')
        
        if self.force_offset:
            if self.variable_section:
                return self.transf_mat_OffsetShear_left @ Fe
            else:
                return principal_axis.T @ Fe
        else:
            return Fe

    def force_vector_acoustic_gcs(self, frequencies, pressures, pressure_external):
        """
        This method returns the element load vector due to the internal acoustic pressure field in the global coordinate system. The loads are forces and moments according to the degree of freedom. 

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

        if self.element_type in ['pipe_1', 'pipe_2']:
            stress_axial = (pressures * Di**2 - pressure_external * Do**2) / (Do**2 - Di**2)
            if self.wall_formutation_type == "thick wall": 
                force = A * (capped_end - 2*nu)* stress_axial
            elif self.wall_formutation_type == "thin wall":
                force = A * (capped_end*stress_axial - nu*pressures*(Do/(Do-Di) - 1))
        elif self.element_type in ['expansion_joint','valve']:
            nu = 0
            force = (capped_end - 2*nu)* A *pressures
        else:
            return np.zeros((rows, cols))

        aux = np.zeros((rows, cols), dtype=complex)
        aux[0,:] = -force[0,:]
        aux[6,:] =  force[1,:]
        R = self.element_rotation_matrix
        
        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type in ['pipe_2', 'expansion_joint', 'valve']:
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            raise TypeError('Only pipe_1 and pipe_2 element types are allowed.')
        
        if self.force_offset:
            if self.variable_section:
                return R.T @ self.transf_mat_OffsetShear_left @ aux
            else:
                return R.T @ principal_axis.T @ aux
        else:
            return R.T @ aux


    def force_vector_stress_stiffening(self, vector_gcs=True):
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
        
        if self.element_type in ['pipe_1', 'pipe_2', 'valve']:
            axial_stress = (P_in*(D_in**2) - P_out*(D_out**2))/((D_out**2) - (D_in**2))
        else:
            return aux
        
        if self.capped_end:
            capped_end = 1
        else:
            capped_end = 0

        if self.element_type == 'pipe_1':
            principal_axis = self.cross_section.principal_axis
        elif self.element_type == 'pipe_2':
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            raise TypeError('Only pipe_1 and pipe_2 element types are allowed.')

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

        if self.wall_formutation_type == "thick wall":
            return (capped_end - 2*nu) * axial_stress * A * aux
        elif self.wall_formutation_type == "thin wall":
            return (capped_end*axial_stress - nu*((P_in*D_out/(D_out-D_in))-P_in)) * A * aux
    

    def get_self_weighted_load(self, gravity_vector):
        """
        This method returns the self-weighted loads for static analysis.
        Returns
        -------
        Fe_sw : array
            Load vector due to self-weight in the global coordinate system.
        """
 
        g = gravity_vector
        #
        rho = self.material.density
        A = self.cross_section.area
        #
        A_fluid = A_ins = 0.
        rho_fluid = rho_ins = 0.
        if self.element_type in ["pipe_1", "valve"]:
            A_ins = self.cross_section.area_insulation
            rho_ins = self.cross_section.insulation_density
            if self.fluid is not None and self.adding_mass_effect:
                rho_fluid = self.fluid.density
                A_fluid = self.cross_section.area_fluid
        
        eload = (rho*A + rho_fluid*A_fluid + rho_ins*A_ins)*g

        _R = self.element_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]
        _Rt = self.transpose_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]
        
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
                return self.transf_mat_OffsetShear_left @ Fe_sw
            else:
                return principal_axis.T @ Fe_sw
        else:
            return Fe_sw

        
    def stiffness_matrix_beam(self):
        """
        This method returns the beam element stiffness matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is suitable for any beam cross section data.

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

        # Material properities
        E   = self.material.young_modulus
        nu  = self.material.poisson_ratio
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area
        I_2 = self.cross_section.second_moment_area_y
        I_3 = self.cross_section.second_moment_area_z
        J   = self.cross_section._polar_moment_area()

        # Process cross-section offset
        self.cross_section.offset_rotation(el_type = 'beam_1')
        principal_axis = self.cross_section.principal_axis

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

        Ke = symmetrize(ke)*self.decoupling_matrix

        return principal_axis.T @ Ke @ principal_axis

    def mass_matrix_beam(self):
        """
        This method returns the beam element mass matrix according to the 3D Timoshenko beam theory in the local coordinate system. This formulation is suitable for any beam cross section data.

        Returns
        -------
        mass : array
            Beam element mass matrix in the local coordinate system.

        See also
        --------
        mass_matrix_pipes : Pipe element mass matrix in the local coordinate system.
        """

        # Element length
        L   = self.length

        # Material properities
        rho = self.material.density
        # nu = self.material.poisson_ratio
        E   = self.material.young_modulus
        G   = self.material.shear_modulus

        # Tube cross section properties
        A   = self.cross_section.area
        I_2 = self.cross_section.second_moment_area_y
        I_3 = self.cross_section.second_moment_area_z
        J   = self.cross_section._polar_moment_area()

        # Process cross-section offset
        self.cross_section.offset_rotation(el_type = 'beam_1')
        principal_axis = self.cross_section.principal_axis

        # alpha = self.get_shear_coefficient(self.cross_section.section_info, self.material.poisson_ratio)
        # k_2 = alpha
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
        
        Me = symmetrize(me)*self.decoupling_matrix

        return principal_axis.T @ Me @ principal_axis

    def get_shear_coefficient(self, section_info, poisson):
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

            h, w1, t1, w2, t2, tw, _, _, _ = parameters
            
            tf = (t1+t2)/2
            b = (w1+w2)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (m + m**2)*(30*n**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = 0.93*numerator/denominator

        elif section_label == "I-section":

            h, w1, t1, w2, t2, tw, _, _, _ = parameters
            
            tf = (t1+t2)/2
            b = (w1+w2)/2

            m = (2*b*tf)/(h*w2)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 3*m)**2)
            denominator = (12 + 72*m + 150*m**2 + 90*m**3) + poisson*(11 + 66*m + 135*m**2 + 90*m**3) + (m + m**2)*(30*n**2) + (8*m + 9*m**2)*(5*poisson*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "T-section":

            h, w1, t1, tw, _, _, _ = parameters
            tf, b = t1, w1
      
            m = (2*b*tf)/(h*tw)
            n = b/h
            numerator = 10*(1 + poisson)*((1 + 4*m)**2)
            denominator = (12 + 96*m + 278*m**2 + 192*m**3) + poisson*(11 + 88*m + 248*m**2 + 216*m**3) + (m + m**2)*(30*n**2) + (4*m + 5*m**2 + m**3)*(10*poisson*n**2)
            shear_coefficient = numerator/denominator

        elif section_label == "Generic section":
            shear_coefficient = self.cross_section.shear_coefficient

        return shear_coefficient

    def stiffness_matrix_expansion_joint(self, frequencies=None):
        L_e = self.joint_length/self.length
        K_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        
        K1 = self.joint_axial_stiffness*L_e
        K2 = K3 = self.joint_transversal_stiffness/L_e
        K4 = self.joint_torsional_stiffness*L_e
        K5 = K6 = self.joint_angular_stiffness/L_e  

        Ks = np.array([K1, K2, K3, K4, K5, K6], dtype=float)
        indexes_1 = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)
        indexes_2 = indexes_1 + 6

        K_matrix[indexes_1,indexes_1] = K_matrix[indexes_2,indexes_2] = Ks
        K_matrix[indexes_1,indexes_2] = K_matrix[indexes_2,indexes_1] = -Ks
 
        return K_matrix

    def stiffness_matrix_expansion_joint_harmonic(self, frequencies=None):
        L_e = self.joint_length/self.length
        if frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(frequencies)
         
        K_matrix = np.zeros((number_frequencies, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
            
        K1 = self.joint_axial_stiffness*L_e
        K2 = K3 = self.joint_transversal_stiffness/L_e
        K4 = self.joint_torsional_stiffness*L_e
        K5 = K6 = self.joint_angular_stiffness/L_e  

        K1 = self.get_array_values(K1, number_frequencies)
        K2 = self.get_array_values(K2, number_frequencies)
        K3 = K2
        K4 = self.get_array_values(K4, number_frequencies)
        K5 = self.get_array_values(K5, number_frequencies)
        K6 = K5   

        Ks = np.array([K1, K2, K3, K4, K5, K6], dtype=float).T.reshape(number_frequencies, DOF_PER_NODE_STRUCTURAL)
        indexes_1 = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)
        indexes_2 = indexes_1 + DOF_PER_NODE_STRUCTURAL

        K_matrix[:,indexes_1,indexes_1] = K_matrix[:,indexes_2,indexes_2] = Ks
        K_matrix[:,indexes_1,indexes_2] = K_matrix[:,indexes_2,indexes_1] = -Ks

        return K_matrix

    def mass_matrix_expansion_joint(self):
        L_e = self.joint_length/self.length
        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        M1 = M2 = M3 = self.joint_mass/(2*L_e)
        indexes = np.array([0,1,2,6,7,8], dtype=int)

        M_matrix[indexes,indexes] = [M1, M2, M3, M1, M2, M3]
        return M_matrix

    def mass_matrix_valve(self):
        L_e = self.valve_length/self.length
        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        M1 = M2 = M3 = self.valve_mass/(2*L_e)
        indexes = np.array([0,1,2,6,7,8], dtype=int)

        M_matrix[indexes,indexes] = [M1, M2, M3, M1, M2, M3]
        return M_matrix

    def reset_expansion_joint_parameters(self):
        self.expansion_joint_parameters = None
        self.joint_length = 0
        self.joint_effective_diameter = 0
        self.joint_mass = 0  
        self.joint_axial_locking_criteria = 0
        self.joint_rods_included = False
        self.joint_axial_stiffness = 0
        self.joint_transversal_stiffness = 0
        self.joint_torsional_stiffness = 0
        self.joint_angular_stiffness = 0
        self.joint_stiffness_table_names = []

    def reset_valve_parameters(self):
        self.valve_parameters = None
        self.valve_elements = []
        self.flange_elements = []
        self.valve_section_parameters = {}
        self.valve_length = 0
        self.valve_stiffening_factor = 10
        self.valve_mass = 0
        self.valve_center_coordinates = None
        self.flange_parameters = {}  
        self.valve_diameters = {}        

    def get_array_values(self, value, number_frequencies):
        if isinstance(value, np.ndarray):
            if number_frequencies == 1:
                return value[0]
            else:
                return value
        else:
            return value*np.ones(number_frequencies)

    # def __str__(self):
    #     text = ''
    #     text += f'Element ID: {self.index} \n'
    #     text += f'First Node ID: {self.first_node.external_index} -- Coordinates: ({self.first_node.coordinates}) [m]\n'
    #     text += f'Last Node ID: {self.last_node.external_index} -- Coordinates: ({self.first_node.coordinates}) [m]\n'
    #     text += f'Material: {self.material.name} \n'
    #     text += f'Strutural element type: {self.element_type} \n'
    #     return text