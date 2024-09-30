from time import time
import numpy as np
from math import pi
from numpy.linalg import norm
from scipy.sparse import csr_matrix, csc_matrix

from pulse.model.model import Model
from pulse.model.node import DOF_PER_NODE_ACOUSTIC
from pulse.model.acoustic_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

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
    def __init__(self, model: Model):

        self.model = model
        self.preprocessor = model.preprocessor
        self.frequencies = model.frequencies

        self.total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        self.neighbor_diameters = self.preprocessor.neighbor_elements_diameter_global()
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

        global_prescribed = list()

        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "acoustic_pressure":

                node_id = args[0]
                node = self.preprocessor.nodes[node_id]
                values = data["values"]

                starting_position = node.global_index * DOF_PER_NODE_ACOUSTIC
                internal_dofs = [i for i, value in enumerate(values) if value is not None]

                dofs = starting_position + np.array(internal_dofs)
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

        global_prescribed = list()

        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "acoustic_pressure":
                values = data["values"]
                global_prescribed.extend([value for value in values if value is not None])   
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
        beam_gdofs, _ = self.preprocessor.get_beam_and_non_beam_elements_global_dofs()

        for dof in list(beam_gdofs):
            indexes_to_remove.append(dof)

        indexes_to_remove = list(np.sort(indexes_to_remove))
        unprescribed_pipe_indexes = np.delete(all_indexes, indexes_to_remove)
        self.preprocessor.set_unprescribed_pipe_indexes(unprescribed_pipe_indexes)

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
        if element.length_correction_data is not None:

            correction_type = element.length_correction_data["correction_type"]

            first = element.first_node.global_index
            last = element.last_node.global_index

            di_actual = element.cross_section.inner_diameter

            diameters_first = np.array(self.neighbor_diameters[first])
            diameters_last = np.array(self.neighbor_diameters[last])

            corrections_first = [0]
            corrections_last = [0]

            for _, _, di in diameters_first:
                if di_actual < di:

                    if correction_type in [0, 2]:
                        correction = length_correction_expansion(di_actual, di)

                    elif correction_type == 1:
                        correction = length_correction_branch(di_actual, di)
                        if len(diameters_first) == 2:
                            message = "Warning: Expansion identified in acoustic "
                            message += "domain is being corrected as side branch."
                            print(message)

                    else:
                        print("Datatype not understood")

                    corrections_first.append(correction)

            for _, _, di in diameters_last:
                if di_actual < di:

                    if correction_type in [0, 2]:
                        correction = length_correction_expansion(di_actual, di)

                    elif correction_type == 1:
                        correction = length_correction_branch(di_actual, di)
                        if len(diameters_last) == 2:
                            message = "Warning: Expansion identified in acoustic "
                            message += "domain is being corrected as side branch."
                            print(message)

                    else:
                        print("Datatype not understood")

                    corrections_last.append(correction)

            length_correction = max(corrections_first) + max(corrections_last)

        return length_correction

    def get_length_correction_for_acoustic_link(self, diameters):
        d_minor, d_major = diameters
        return length_correction_expansion(d_minor, d_major)

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

        for element in self.preprocessor.get_acoustic_elements():

            index = element.index
            start = (index - 1) * ENTRIES_PER_ELEMENT
            end = start + ENTRIES_PER_ELEMENT

            if element.acoustic_link_diameters:
                length_correction = self.get_length_correction_for_acoustic_link(element.acoustic_link_diameters)
            else:
                length_correction = self.get_length_corretion(element)

            data_k[:, start:end] = element.matrix(self.frequencies, length_correction = length_correction)

        full_K = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof], dtype=complex) for data in data_k]

        K = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_K]
        Kr = [full[:, self.prescribed_indexes] for full in full_K]

        return K, Kr

    def get_fetm_link_matrices(self):

        """
        This method perform the assembly process of the acoustic FETM link matrices.

        Returns
        ----------
        K_link : list
            List of linked admittance matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Kr_link : list
            List of linked admittance matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        rows = list()
        cols = list()
        data_Klink = list()

        for (_property, *args) in self.model.properties.nodal_properties.keys():

            if _property == "psd_acoustic_link":

                psd_link_data = self.preprocessor.get_psd_acoustic_link_data(args)
                rows.extend(psd_link_data["indexes_i"])
                cols.extend(psd_link_data["indexes_j"])

                element = psd_link_data["element_pipe"]

                data_Ke = element.fetm_link_matrix(self.frequencies)

                if len(data_Klink):
                    data_Klink = np.c_[data_Klink, data_Ke]
                else:
                    data_Klink = data_Ke

        if len(data_Klink):
            full_K_link = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof]) for data in data_Klink]
        else:
            full_K_link = [csr_matrix((total_dof, total_dof)) for _ in self.frequencies]
        
        K_link = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_K_link]
        Kr_link = [full[:, self.prescribed_indexes] for full in full_K_link]

        return K_link, Kr_link  

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

        elements = self.preprocessor.get_acoustic_elements()

        # processing external elements by node
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property in ["specific_impedance", "radiation_impedance"]:

                node_id = args[0]
                node = self.preprocessor.nodes[node_id]
                position = node.global_index

                if property == "specific_impedance":
    
                    impedance = data["values"]

                    for element in elements:
                        if element.first_node.global_index == position or element.last_node.global_index == position:
                            area_fluid = element.cross_section.area_fluid

                elif property == "radiation_impedance":

                    impedance_type = data["impedance_type"]
                    elements = self.preprocessor.acoustic_elements_connected_to_node[node_id]

                    if len(elements) == 1:
                        element = elements[0]
                        area_fluid = element.cross_section.area_fluid
                        impedance = element.get_radiation_impedance(impedance_type, self.frequencies)

                ind_Klump.append(position)
                admittance = self.get_nodal_admittance(impedance, area_fluid, self.frequencies)

                if data_Klump == []:
                    data_Klump = admittance
                else:
                    data_Klump = np.c_[data_Klump, admittance]

        if area_fluid is None:
            full_K = [csr_matrix((total_dof, total_dof)) for _ in self.frequencies]
        else:
            full_K = [csr_matrix((data, (ind_Klump, ind_Klump)), shape=[total_dof, total_dof]) for data in data_Klump]
        
        K_lump = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_K]
        Kr_lump = [full[:, self.prescribed_indexes] for full in full_K]

        return K_lump, Kr_lump  

    def get_nodal_admittance(self, impedance: (None | complex | np.ndarray), area_fluid: float, frequencies: np.ndarray) -> np.ndarray:
        
        admittance = np.zeros(len(frequencies), dtype=complex)

        if impedance is not None:
            Z = impedance / area_fluid
            
            if isinstance(impedance, complex):
                admittance = (1 / Z) * np.ones_like(frequencies)

            elif isinstance(impedance, np.ndarray):
                if len(impedance) != len(frequencies):
                    raise TypeError("The Specific Impedance array and frequencies array must have \nthe same length.")
                admittance = np.divide(1, Z)
        
        return admittance.reshape(-1, 1)#([len(frequencies),1])

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
        for element in self.preprocessor.get_acoustic_elements():

            index = element.index - 1
            if element.acoustic_link_diameters:
                length_correction = self.get_length_correction_for_acoustic_link(element.acoustic_link_diameters)
            else:
                length_correction = self.get_length_corretion(element)
            
            mat_Ke[index,:,:], mat_Me[index,:,:] = element.fem_1d_matrix(length_correction)

        full_K = csr_matrix((mat_Ke.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        full_M = csr_matrix((mat_Me.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        
        K = full_K[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        M = full_M[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

        return K, M

    def get_link_global_matrices_modal(self):
        """
        This method perform the assembly process of the acoustic link FEM matrices.

        Returns
        ----------
        K : sparse csr_matrix
            Acoustic stiffness matrix.

        M : sparse csr_matrix
            Acoustic inertia matrix.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        rows = list()
        cols = list()
        data_Klink = list()
        data_Mlink = list()

        K_link = 0.
        M_link = 0.

        for (_property, *args), data in self.model.properties.nodal_properties.items():

            data: dict
            if _property == "psd_acoustic_link":

                if "link_data" in data.keys():
                    rows.extend(data["link_data"]["indexes_i"])
                    cols.extend(data["link_data"]["indexes_j"])

                    element = data["element_pipe"]

                    data_Ke, data_Me = element.fem_1d_link_matrix()

                    data_Klink.extend(list(data_Ke))
                    data_Mlink.extend(list(data_Me))

        if len(data_Klink):
            full_K_link = csr_matrix((data_Klink, (rows, cols)), shape=[total_dof, total_dof])
            full_M_link = csr_matrix((data_Mlink, (rows, cols)), shape=[total_dof, total_dof])
            
            K_link = full_K_link[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
            M_link = full_M_link[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

        return K_link, M_link

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

        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property in ["volume_velocity", "compressor_excitation"]:

                node_id = args[0]
                node = self.preprocessor.nodes[node_id]
                position = node.global_index
                values = data["values"][0]

                if isinstance(values, complex):
                    volume_velocity[:, position] = values*np.ones_like(self.frequencies)
                elif isinstance(values, np.ndarray):
                    volume_velocity[:, position] = values

        volume_velocity = volume_velocity[:, self.unprescribed_indexes]

        return volume_velocity