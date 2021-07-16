from time import time
import numpy as np
from math import pi
from numpy.linalg import norm
from scipy.sparse import csr_matrix, csc_matrix
from pulse.utils import timer, error

from pulse.preprocessing.node import DOF_PER_NODE_ACOUSTIC
from pulse.preprocessing.acoustic_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

def length_correction_expansion(smaller_diameter, larger_diameter):
    """ This function returns the acoustic length correction due to expansion in the acoustic domain. This discontinuity is characterized by two elements in line with different diameters.

    Parameters
    ----------
    smaller_diameter: float
        Smaller diameter between the two elements diameters.

    larger_diameter: float
        Larger diameter between the two elements diameters.

    Returns
    -------
    float
        Length correction due to expansion.

    See also
    --------
    length_correction_branch : Length correction due to sidebranch in the acoustic domain.
    """
    xi = smaller_diameter / larger_diameter
    if xi <= 0.5:
        factor = 8 / (3 * pi) * (1 - 1.238 * xi)
    else:
        factor = 8 / (3 * pi) * (0.875 * (1 - xi) * (1.371 - xi))
    return smaller_diameter * factor / 2

def length_correction_branch(branch_diameter, principal_diameter):
    """ This function returns the acoustic length correction due to sidebranch in the acoustic domain. This discontinuity is characterized by three elements, two with the same diameters in line, and the other with different diameter connected to these two.

    Parameters
    ----------
    smaller_diameter: float
        Smaller diameter between the two elements diameters.

    larger_diameter: float
        Larger diameter between the two elements diameters.

    Returns
    -------
    float
        Length correction due to side branch.

    See also
    --------
    length_correction_expansion : Length correction due to expansion in the acoustic domain.
    """
    xi = branch_diameter / principal_diameter
    if xi <= 0.4:
        factor = 0.8216 - 0.0644 * xi - 0.694 * xi**2
    elif xi > 0.4:
        factor = 0.9326 - 0.6196 * xi
    return branch_diameter * factor / 2

class AssemblyAcoustic:
    """ This class creates a acoustic assembly object from input data.

    Parameters
    ----------
    mesh : Mesh object
        Acoustic finite element preprocessor.

    frequencies : array
        Frequencies of analysis.
    """
    def __init__(self, preprocessor, frequencies):
        self.preprocessor = preprocessor
        self.frequencies = frequencies
        if preprocessor.beam_gdofs is None:
            self.beam_gdofs, self.pipe_gdofs = preprocessor.get_beam_and_pipe_elements_global_dofs()
        else:
            self.beam_gdofs, self.pipe_gdofs = preprocessor.beam_gdofs, preprocessor.pipe_gdofs
        self.acoustic_elements = preprocessor.get_pipe_elements()
        self.total_dof = DOF_PER_NODE_ACOUSTIC * len(preprocessor.nodes)
        self.neighbor_diameters = preprocessor.neighbor_elements_diameter_global()
        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_pipe_and_unprescribed_indexes()

    def get_prescribed_indexes(self):
        """
        This method returns all the indexes of the acoustic degrees of freedom with prescribed pressure boundary condition.

        Returns
        ----------
        array
            Indexes of the acoustic degrees with prescribed pressure boundary conditions.

        See also
        --------
        get_prescribed_values : Values of the prescribed pressure boundary condition.

        get_unprescribed_indexes : Indexes of the free acoustic degrees of freedom.
        """
        global_prescribed = []
        for node in self.preprocessor.nodes.values():
            starting_position = node.global_index * DOF_PER_NODE_ACOUSTIC
            dofs = np.array(node.get_acoustic_boundary_condition_indexes()) + starting_position
            global_prescribed.extend(dofs)
        return global_prescribed

    def get_prescribed_values(self):
        """
        This method returns all the values of the prescribed pressure boundary condition.

        Returns
        ----------
        array
            Values of the prescribed pressure boundary condition.

        See also
        --------
        get_prescribed_indexes : Indexes of the acoustic degrees with prescribed pressure boundary conditions.

        get_unprescribed_indexes : Indexes of the free acoustic degrees of freedom.
        """
        global_prescribed = []
        for node in self.preprocessor.nodes.values():
            if node.acoustic_pressure is not None:
                global_prescribed.extend([node.acoustic_pressure])
        return global_prescribed

    def get_unprescribed_indexes(self):
        """
        This method returns all the indexes of the free acoustic degrees of freedom.

        Returns
        ----------
        array
            Indexes of the free acoustic degrees of freedom.

        See also
        --------
        get_prescribed_values : Values of the prescribed pressure boundary condition.

        get_prescribed_indexes : Indexes of the acoustic degrees with prescribed pressure boundary conditions.
        """
        all_indexes = np.arange(self.total_dof)
        unprescribed_indexes = np.delete(all_indexes, self.prescribed_indexes)
        return unprescribed_indexes

    def get_pipe_and_unprescribed_indexes(self):
        """
        This method returns all the indexes of the free acoustic degrees of freedom.

        Returns
        ----------
        array
            Indexes of the free acoustic degrees of freedom.

        See also
        --------
        get_prescribed_values : Values of the prescribed pressure boundary condition.

        get_prescribed_indexes : Indexes of the acoustic degrees with prescribed pressure boundary conditions.
        """
        all_indexes = np.arange(self.total_dof)
        indexes_to_remove = self.prescribed_indexes.copy()
        for dof in list(self.beam_gdofs):
            indexes_to_remove.append(dof)
        indexes_to_remove = list(np.sort(indexes_to_remove))
        unprescribed_pipe_indexes = np.delete(all_indexes, indexes_to_remove)
        return unprescribed_pipe_indexes

    def get_length_corretion(self, element):
        """
        This method evaluate the acoustic length correction for an element. The necessary conditions and the type of correction are checked.

        Parameters
        ----------
        element: Acoustic element object
            Acoustic element.

        Returns
        ----------
        float
            Length correction.
        """
        length_correction = 0
        if element.acoustic_length_correction is not None:
            first = element.first_node.global_index
            last = element.last_node.global_index

            di_actual = element.cross_section.inner_diameter

            diameters_first = np.array(self.neighbor_diameters[first])
            diameters_last = np.array(self.neighbor_diameters[last])

            corrections_first = [0]
            corrections_last = [0]

            for _,_,di in diameters_first:
                if di_actual < di:
                    if element.acoustic_length_correction == 0 or element.acoustic_length_correction == 2:
                        correction = length_correction_expansion(di_actual, di)
                    elif element.acoustic_length_correction == 1:
                        correction = length_correction_branch(di_actual, di)
                        if len(diameters_first) == 2:
                            print("Warning: Expansion identified in acoustic \ndomain is being corrected as side branch.")
                    else:
                        print("Datatype not understood")
                    corrections_first.append(correction)

            for _,_,di in diameters_last:
                if di_actual < di:
                    if element.acoustic_length_correction == 0 or element.acoustic_length_correction == 2:
                        correction = length_correction_expansion(di_actual, di)
                    elif element.acoustic_length_correction == 1:
                        correction = length_correction_branch(di_actual, di)
                        if len(diameters_last) == 2:
                            print("Warning: Expansion identified in acoustic \ndomain is being corrected as side branch.")
                    else:
                        print("Datatype not understood")
                    corrections_last.append(correction)
            length_correction = max(corrections_first) + max(corrections_last)
        return length_correction

    def get_global_matrices(self):
        """
        This method perform the assembly process of the acoustic FETM matrices.

        Returns
        ----------
        K : list
            List of admittance matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Kr : list
            List of admittance matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)
        total_entries = ENTRIES_PER_ELEMENT * len(self.preprocessor.acoustic_elements)

        rows, cols = self.preprocessor.get_global_acoustic_indexes()
        data_k = np.zeros([len(self.frequencies), total_entries], dtype = complex)
        for element in self.acoustic_elements:
            
            index = element.index

            start = (index-1) * ENTRIES_PER_ELEMENT
            end = start + ENTRIES_PER_ELEMENT

            length_correction = self.get_length_corretion(element)
            data_k[:, start:end] = element.matrix(self.frequencies, length_correction = length_correction)
            
        full_K = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof], dtype=complex) for data in data_k]

        K = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_K]
        Kr = [full[:, self.prescribed_indexes] for full in full_K]

        return K, Kr
            
    def get_lumped_matrices(self):
        """
        This method perform the assembly process of the acoustic FETM lumped matrices.

        Returns
        ----------
        K_lump : list
            List of lumped admittance matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Kr_lump : list
            List of lumped admittance matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)
        
        data_Klump = []
        ind_Klump = []
        area_fluid = None

        elements = self.acoustic_elements

        # processing external elements by node
        for node in self.preprocessor.nodes.values():

            if node.specific_impedance is None:
                node_specific_impedance = 0
            else:
                node_specific_impedance = node.specific_impedance

            if node.radiation_impedance is None:
                node_radiation_impedance = 0
            else:
                node_radiation_impedance = node.radiation_impedance

            if np.sum(node_specific_impedance + node_radiation_impedance) != 0:
                position = node.global_index

                for element in elements:
                    if element.first_node.global_index == position or element.last_node.global_index == position:
                        area_fluid = element.cross_section.area_fluid

                ind_Klump.append(position)
                if data_Klump == []:
                    data_Klump = node.admittance(area_fluid, self.frequencies)
                else:
                    data_Klump = np.c_[data_Klump, node.admittance(area_fluid, self.frequencies)]

        if area_fluid is None:
            full_K = [csr_matrix((total_dof, total_dof)) for _ in self.frequencies]
        else:
            full_K = [csr_matrix((data, (ind_Klump, ind_Klump)), shape=[total_dof, total_dof]) for data in data_Klump]
        
        K_lump = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_K]
        Kr_lump = [full[:, self.prescribed_indexes] for full in full_K]

        return K_lump, Kr_lump  

    def get_global_matrices_modal(self):
        """
        This method perform the assembly process of the acoustic FEM matrices.

        Returns
        ----------
        K : sparse csr_matrix
            Acoustic stiffness matrix.

        M : sparse csr_matrix
            Acoustic inertia matrix.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)
        number_elements = len(self.preprocessor.acoustic_elements)

        rows, cols = self.preprocessor.get_global_acoustic_indexes()
        mat_Ke = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        # for index, element in enumerate(self.preprocessor.acoustic_elements.values()):
        for element in self.acoustic_elements:
            index = element.index - 1
            length_correction = self.get_length_corretion(element)
            mat_Ke[index,:,:], mat_Me[index,:,:] = element.fem_1d_matrix(length_correction)            

        full_K = csr_matrix((mat_Ke.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        full_M = csr_matrix((mat_Me.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        
        K = full_K[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        M = full_M[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

        return K, M

    def get_global_volume_velocity(self):
        """
        This method perform the assembly process of the acoustic load, volume velocity.

        Returns
        ----------
        volume_velocity : array
            Volume velocity load.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)
        volume_velocity = np.zeros([len(self.frequencies), total_dof], dtype=complex)

        for node in self.preprocessor.nodes.values():
            if node.volume_velocity is not None:
                position = node.global_index
                volume_velocity[:, position] += node.get_volume_velocity(self.frequencies)
        
        volume_velocity = volume_velocity[:, self.unprescribed_indexes]

        return volume_velocity