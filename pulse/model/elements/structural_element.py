from typing import TYPE_CHECKING

import numpy as np

from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.model.properties.fluid import Fluid
from pulse.utils.rotations import rotation_matrix_3x3_by_deltas

NODES_PER_ELEMENT = 2
DOF_PER_ELEMENT = DOF_PER_NODE_STRUCTURAL * NODES_PER_ELEMENT
ENTRIES_PER_ELEMENT = DOF_PER_ELEMENT ** 2

zeros_3x3 = np.zeros((3,3), dtype=float)

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


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

    element_type : str, ['pipe_1', 'beam_1', 'expansion_joint', 'valve'], optional
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
    def __init__(self, element_attributes: "ElementAttributes", **kwargs):

        self.element_attributes = element_attributes

        self.first_node = element_attributes.first_node
        self.last_node = element_attributes.last_node
        self.index = element_attributes.index

        self._initialize()

    def _initialize(self):

        self._Dab = None
        self._Bab = None
        self._Dts = None
        self._Bts = None

        self.transf_mat = None
        self.transf_matrix_offset_shear_left = None
        self.transf_matrix_offset_shear_right = None


    @ property
    def delta_x(self) -> np.ndarray:
        return self.element_attributes.delta_x


    @ property
    def delta_y(self) -> np.ndarray:
        return self.element_attributes.delta_y


    @ property
    def delta_z(self) -> np.ndarray:
        return self.element_attributes.delta_z


    @ property
    def length(self) -> float:
        return self.element_attributes.length


    @ property
    def cross_section(self):
        return self.element_attributes.cross_section


    @ property
    def material(self):
        return self.element_attributes.material


    @ property
    def fluid(self):
        return self.element_attributes.fluid


    @property
    def global_dof(self) -> np.ndarray:
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


    @ property
    def element_rotation_matrix(self) -> np.ndarray:
        return self.element_attributes.element_rotation_matrix


    @property
    def element_rotation_matrix_inverse(self) -> np.ndarray:
        return self.element_attributes.element_rotation_matrix_inverse


    def matrices_gcs(self):
        pass


    def compute_transf_submatrix(self) -> np.ndarray:
        xaxis_rotation_angle = 0
        if self.element_attributes is not None:
            xaxis_rotation_angle = self.element_attributes.xaxis_rotation_angle

        return rotation_matrix_3x3_by_deltas(self.delta_x, self.delta_y, self.delta_z, xaxis_rotation_angle)


    def element_results_gcs(self) -> np.ndarray:
        return self.element_attributes.element_results_gcs()


    def element_results_lcs(self):
        return self.element_attributes.element_results_lcs()


    def static_element_results_gcs(self) -> np.ndarray:
        values = np.zeros(DOF_PER_ELEMENT, dtype=float)
        values[:DOF_PER_NODE_STRUCTURAL] = self.first_node.static_nodal_solution_gcs
        values[DOF_PER_NODE_STRUCTURAL:] = self.last_node.static_nodal_solution_gcs
        return values


    def static_element_results_lcs(self) -> np.ndarray:
        return self.element_rotation_matrix @ self.static_element_results_gcs()


    def mean_element_results(self) -> np.ndarray:
        results_gcs = self.element_results_gcs()
        results_first_node = results_gcs[:DOF_PER_NODE_STRUCTURAL]
        results_last_node = results_gcs[DOF_PER_NODE_STRUCTURAL:]
        return (results_first_node + results_last_node) / 2
        # u_x = (results_gcs[0] + results_gcs[-6])/2
        # u_y = (results_gcs[1] + results_gcs[-5])/2
        # u_z = (results_gcs[2] + results_gcs[-4])/2
        # theta_x = (results_gcs[3] + results_gcs[-3])/2
        # theta_y = (results_gcs[4] + results_gcs[-2])/2
        # theta_z = (results_gcs[5] + results_gcs[-1])/2
        # return np.array([u_x, u_y, u_z, theta_x, theta_y, theta_z], dtype=float)


    def mean_rotations_at_global_coordinate_system(self) -> np.ndarray:
        results_gcs = self.element_results_gcs()
        theta_x = (results_gcs[3] + results_gcs[-3])/2
        theta_y = (results_gcs[4] + results_gcs[-2])/2
        theta_z = (results_gcs[5] + results_gcs[-1])/2
        return np.array([theta_x, theta_y, theta_z], dtype=float)


    def deformed_element_length(self, deltas: np.ndarray) -> float:
        return np.linalg.norm(deltas)


    def global_matrix_indexes(self) -> np.ndarray:
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


    def force_vector_gcs(self) -> np.ndarray:
        """
        This method returns the element force vector in the global coordinate system.

        Returns
        -------
        array
            Force vector in the global coordinate system.
        """
        Rt = self.element_rotation_matrix_inverse
        return Rt @ self.get_distributed_load()


    def get_distributed_load(self) -> np.ndarray:
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

        cross_section = self.cross_section
        loaded_forces = self.element_attributes.loaded_forces

        R = self.element_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]

        # convert the loads to the local coordinates
        eload_lcs =  R @ loaded_forces @ R.T
        eload_lcs = eload_lcs.reshape(-1, 1)

        ## Numerical integration by Gauss quadrature
        L = self.element_attributes.length
        integrations_points = 2
        points, weigths = gauss_quadrature(integrations_points)

        #Determinant of Jacobian (linear 1D trasform)
        det_jacobian = L / 2

        Fe = 0
        aux_eyes = np.eye( DOF_PER_NODE_STRUCTURAL, dtype=float)
        for point, weigth in zip(points, weigths):
            phi, _ = shape_function(point)
            N = np.c_[phi[0] * aux_eyes, phi[1] * aux_eyes]
            Fe += (N.T @ eload_lcs) * det_jacobian * weigth

        if self.element_type != "pipe_1":
            return np.zeros((DOF_PER_ELEMENT, 1), dtype=float)

        principal_axis = cross_section.principal_axis

        if self.element_attributes.force_offset:
            if self.element_attributes.is_section_variable:
                if self.transf_matrix_offset_shear_left is None:
                    self.process_offset_transformation_matrices()
                return self.transf_matrix_offset_shear_left @ Fe

            return principal_axis.T @ Fe

        return Fe


    def force_vector_acoustic_gcs(self, frequencies: np.ndarray, pressures: np.ndarray, pressure_external: float) -> np.ndarray:
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

        material = self.material
        cross_section = self.cross_section

        rows = DOF_PER_ELEMENT
        cols = len(frequencies)
        Do = cross_section.outer_diameter
        Di = cross_section.inner_diameter

        nu = material.poisson_ratio
        A = cross_section.area

        # p_avg = (pressures[0] + pressures[1])/2
        if self.element_attributes.capped_end:
            capped_end = 1 if self.element_attributes.capped_end else 0

        if self.element_attributes.structural_element_type == 'pipe_1':
            stress_axial = (pressures * Di**2 - pressure_external * Do**2) / (Do**2 - Di**2)
            if self.element_attributes.wall_formulation == "thick_wall":
                force = A * (capped_end - 2 * nu) * stress_axial

            elif self.element_attributes.wall_formulation == "thin_wall":
                force = A * (capped_end * stress_axial - nu * pressures * (Do / (Do - Di) - 1))

            else:
                raise TypeError('Only thin and thick wall formulation types are allowable.')

        elif self.element_attributes.structural_element_type in ['expansion_joint','valve']:
            nu = 0
            force = A * (capped_end - 2*nu) * pressures

        else:
            return np.zeros((rows, cols))

        aux = np.zeros((rows, cols), dtype=complex)
        aux[0,:] = -force[0,:]
        aux[6,:] =  force[1,:]

        R = self.element_rotation_matrix

        if self.element_attributes.structural_element_type == 'pipe_1':
            principal_axis = cross_section.principal_axis
        elif self.element_attributes.structural_element_type in ['expansion_joint', 'valve']:
            principal_axis = np.eye(DOF_PER_ELEMENT)
        else:
            raise TypeError(f'Invalid element type: {self.element_attributes.structural_element_type}')

        if self.element_attributes.force_offset:
            if self.element_attributes.is_section_variable:
                if self.transf_matrix_offset_shear_left is None:
                    self.process_offset_transformation_matrices()
                return R.T @ self.transf_matrix_offset_shear_left @ aux

            return R.T @ principal_axis.T @ aux

        return R.T @ aux


    def force_vector_stress_stiffening(self, vector_gcs: bool = True) -> np.ndarray:
        """
        This method returns description
        Returns
        -------
        S : array
            Load vector in the global coordinate system.
        """

        material = self.material
        cross_section = self.cross_section

        rows = DOF_PER_ELEMENT
        aux = np.zeros([rows, 1])

        D_out = cross_section.outer_diameter
        D_in = cross_section.inner_diameter
        A = cross_section.area
        nu = material.poisson_ratio

        P_in = self.element_attributes.internal_pressure
        P_out = self.element_attributes.external_pressure

        if self.element_type in ['pipe_1', 'valve']:
            axial_stress = (P_in*(D_in**2) - P_out*(D_out**2))/((D_out**2) - (D_in**2))
        else:
            return aux

        capped_end = 1 if self.element_attributes.capped_end else 0

        if self.element_type in ['pipe_1', 'valve']:
            principal_axis = cross_section.principal_axis
        else:
            raise TypeError(f'Invalid element type: {self.element_type}')

        aux[0], aux[6] = -1, 1
        R = self.element_rotation_matrix

        if vector_gcs:
            if self.element_attributes.force_offset:
                aux = R.T @ (principal_axis.T @ aux)
            else:
                aux = R.T @ aux
        else:
            aux = 1
            capped_end = 0

        if self.element_attributes.wall_formulation == "thick_wall":
            return (capped_end - 2*nu) * axial_stress * A * aux
        elif self.element_attributes.wall_formulation == "thin_wall":
            return (capped_end*axial_stress - nu*((P_in*D_out/(D_out-D_in))-P_in)) * A * aux
        else:
            raise TypeError('Only thin and thick wall formulation types are allowable.')


    def get_self_weighted_load(self, gravity_vector: np.ndarray) -> np.ndarray:
        """
        This method returns the self-weighted loads for static analysis.
        Returns
        -------
        Fe_sw : array
            Load vector due to self-weight in the global coordinate system.
        """
 
        if np.sum(gravity_vector) == 0:
            return np.zeros((12,1), dtype=float)

        material = self.material
        cross_section = self.cross_section
        fluid = self.fluid

        rho = material.density
        A = cross_section.area

        A_fluid = A_ins = 0.
        rho_fluid = rho_ins = 0.
        g = gravity_vector

        if self.element_type in ["pipe_1", "valve"]:
            A_ins = cross_section.area_insulation
            rho_ins = cross_section.insulation_density
            if isinstance(fluid, Fluid) and self.element_attributes.adding_mass_effect:
                rho_fluid = fluid.density
                A_fluid = cross_section.area_fluid

        eload = (rho * A + rho_fluid * A_fluid + rho_ins * A_ins) * g

        R = self.element_rotation_matrix[0:DOF_PER_NODE_STRUCTURAL, 0:DOF_PER_NODE_STRUCTURAL]

        # convert the loads to the local coordinates
        eload_lcs =  R @ eload @ R.T               
        eload_lcs = eload_lcs.reshape(-1, 1)

        ## Numerical integration by Gauss quadrature
        L = self.element_attributes.length
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

        if self.element_attributes.structural_element_type == 'pipe_1':
            principal_axis = cross_section.principal_axis
        else:
            principal_axis = np.eye(DOF_PER_ELEMENT)

        if self.element_attributes.force_offset:
            if self.element_attributes.is_section_variable:
                return self.transf_matrix_offset_shear_left @ Fe_sw

            return principal_axis.T @ Fe_sw

        return Fe_sw


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
        Le = self.element_attributes.length
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


def gauss_quadrature(integration_points: int) -> tuple[list, list]:
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

def shape_function(ksi: float) -> tuple[np.ndarray, np.ndarray]:
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

def symmetrize(A: np.ndarray) -> np.ndarray:
    """ This function receives matrix and makes it symmetric.

    Parameters
    ----------
    A: np.ndarray
        Matrix.

    Returns
    -------
    np.ndarray
        Symmetric matrix.    
    """
    return A + A.T - np.diag(A.diagonal())
