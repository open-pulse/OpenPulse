from typing import TYPE_CHECKING

import numpy as np

from pulse.model.elements.structural_element import DOF_PER_ELEMENT, DOF_PER_NODE_STRUCTURAL, StructuralElement

if TYPE_CHECKING:
    from pulse.model.elements.element_attributes import ElementAttributes


class ExpansionJointStructuralElement(StructuralElement):
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
        super().__init__(element_attributes, **kwargs)

        self.expansion_joint_data = element_attributes.expansion_joint_data


    def matrices_gcs(self, frequencies: np.ndarray | None = None):
        """
        This method returns the expansion joint element stiffness and mass matrices in the global coordinate system.

        Returns
        -------
        stiffness : array
            Element stiffness matrix in the global coordinate system.
            
        mass : array
            Element mass matrix in the global coordinate system.

        """

        R = self.element_rotation_matrix
        Rt = self.element_rotation_matrix_inverse

        stiffness = Rt @ self.stiffness_matrix_expansion_joint_harmonic(frequencies=frequencies) @ R
        mass = Rt @ self.mass_matrix_expansion_joint() @ R  

        return stiffness, mass


    def stiffness_matrix_expansion_joint_harmonic(self, frequencies: np.ndarray | None = None):

        L_e = self.expansion_joint_data.ejoint_length / self.length
        n_freq = 1 if frequencies is None else frequencies.size

        K_matrix = np.zeros((n_freq, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=complex)

        kx, kyz, krx, kryz = self.expansion_joint_data.values

        K1 = kx * L_e
        K2 = K3 = kyz / L_e
        K4 = krx * L_e
        K5 = K6 = kryz / L_e

        K1 = get_array_values(K1, n_freq)
        K2 = get_array_values(K2, n_freq)
        K3 = K2
        K4 = get_array_values(K4, n_freq)
        K5 = get_array_values(K5, n_freq)
        K6 = K5   

        Ks = np.array([K1, K2, K3, K4, K5, K6], dtype=complex).T.reshape(n_freq, DOF_PER_NODE_STRUCTURAL)
        indexes_1 = np.arange(DOF_PER_NODE_STRUCTURAL, dtype=int)
        indexes_2 = indexes_1 + DOF_PER_NODE_STRUCTURAL

        K_matrix[:,indexes_1,indexes_1] = K_matrix[:,indexes_2,indexes_2] = Ks
        K_matrix[:,indexes_1,indexes_2] = K_matrix[:,indexes_2,indexes_1] = -Ks

        return K_matrix


    def mass_matrix_expansion_joint(self):

        L_e = self.expansion_joint_data.ejoint_length / self.length
        M_matrix = np.zeros((DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        M1 = M2 = M3 = self.expansion_joint_data.ejoint_mass / (2 * L_e)
        indexes = np.array([0, 1, 2, 6, 7, 8], dtype=int)

        M_matrix[indexes,indexes] = [M1, M2, M3, M1, M2, M3]

        return M_matrix


def get_array_values(values: np.ndarray | float, number_frequencies: int):
    if isinstance(values, np.ndarray):
        if number_frequencies == 1:
            return values[0]
        else:
            return values

    return values * np.ones(number_frequencies, dtype = float)