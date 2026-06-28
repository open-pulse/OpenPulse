
import numpy as np
from scipy.sparse import csr_matrix

from pulse.model import AnalysisID
from pulse.model.elements.acoustic.acoustic_calculator import (
    AcousticCalculator,
    RadiationImpedanceType,
    length_correction_for_branches,
    length_correction_for_expansions,
)
from pulse.model.elements.acoustic.acoustic_element import DOF_PER_ELEMENT, ENTRIES_PER_ELEMENT, ElementLengthCorrection
from pulse.model.elements.element_attributes import ElementAttributes
from pulse.model.elements.elements_builder import build_acoustic_element
from pulse.model.model import Model
from pulse.model.node import DOF_PER_NODE_ACOUSTIC


class AssemblyAcoustic:
    """ This class creates a acoustic assembly object from input data.

    Parameters
    ----------
    model : Model object
        An object containing all the information required for the acoustic assembler.

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

    def get_length_corretion(self, element_attributes: ElementAttributes):
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

        length_correction_data = element_attributes.length_correction_data
        if not length_correction_data:
            return 0.

        correction_type = length_correction_data.get("correction_type")
        if correction_type is None:
            print("Invalid element length correction type detected")
            return 0.

        first_node = element_attributes.first_node
        last_node = element_attributes.last_node
        di_actual = element_attributes.cross_section.inner_diameter

        diameters_first = np.array(self.neighbor_diameters[first_node.global_index])
        diameters_last = np.array(self.neighbor_diameters[last_node.global_index])

        def get_element_correction(di_actual: float, di: float, diameters: list):

            correction = None
            if correction_type in [ElementLengthCorrection.EXPANSION, ElementLengthCorrection.LOOP]:
                correction = length_correction_for_expansions(di_actual, di)

            elif correction_type == ElementLengthCorrection.SIDE_BRANCH:
                correction = length_correction_for_branches(di_actual, di)
                if len(diameters) == 2:
                    message = "Warning: Expansion identified in acoustic "
                    message += "domain is being corrected as side branch."
                    print(message)

            else:
                print(f"The correction type {correction_type} is invalid")

            return correction

        corrections_first = [0]

        for _, _, di in diameters_first:
            if di_actual >= di:
                continue

            correction = get_element_correction(di_actual, di, diameters_first)
            if correction is None:
                continue

            corrections_first.append(correction)

        corrections_last = [0]

        for _, _, di in diameters_last:
            if di_actual >= di:
                continue

            correction = get_element_correction(di_actual, di, diameters_last)
            if correction is None:
                continue

            corrections_last.append(correction)

        length_correction = max(corrections_first) + max(corrections_last)

        return length_correction

    def get_length_correction_for_acoustic_link(self, diameters: list[float, float]):
        d_minor, d_major = diameters
        return length_correction_for_expansions(d_minor, d_major)

    def get_global_matrices_for_harmonic_analysis(self):
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
        number_elements = len(self.preprocessor.elements_attributes)
        total_entries = number_elements * ENTRIES_PER_ELEMENT

        rows, cols = self.preprocessor.get_global_acoustic_indexes()
        data_Kd = np.zeros([len(self.frequencies), total_entries], dtype = complex)
        # data_Kd = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=complex)

        for k, (index, element_attributes) in enumerate(self.preprocessor.elements_attributes.items()):

            if element_attributes.structural_element_type in ["beam_1", "rigid_element"]:
                continue

            start = (index - 1) * ENTRIES_PER_ELEMENT
            end = start + ENTRIES_PER_ELEMENT

            element_attributes.acoustic_element_formulation = "FETM"
            length_correction = self.get_length_corretion(element_attributes)

            element = build_acoustic_element(element_attributes)
            data_Kd[:, start:end] = element.fetm_admittance_matrix(self.frequencies, length_correction = length_correction)
            # data_Kd[k, :, :] = element.fetm_admittance_matrix(self.frequencies, length_correction = length_correction)

        full_K = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof], dtype=complex) for data in data_Kd]
        # full_K = [csr_matrix((data_Kde.flatten(), (rows, cols)), shape=[total_dof, total_dof], dtype=complex) for data_Kde in data_Kd]

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

            if _property != "psd_acoustic_link":
                continue

            psd_link_data = self.preprocessor.get_psd_acoustic_link_data(args)
            if psd_link_data is None:
                continue

            rows.extend(psd_link_data.indexes_rows)
            cols.extend(psd_link_data.indexes_cols)

            length = psd_link_data.length
            element_attributes = psd_link_data.element_attributes
            length_correction = self.get_length_correction_for_acoustic_link(psd_link_data.diameters)

            element = build_acoustic_element(element_attributes)
            data_Ke = element.fetm_admittance_link_matrix(self.frequencies, length, length_correction=length_correction)

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

    def get_fetm_transfer_matrices(self):

        """
        This method perform the assembly process of the acoustic FETM transfer matrices.

        Returns
        ----------
        T_link : list
            List of linked admittance matrices of the free degree of freedom. Each item of the list is a 
            sparse csr_matrix that corresponds to one frequency of analysis.

        Tr_link : list
            List of linked admittance matrices of the prescribed degree of freedom. Each item of the list 
            is a sparse csr_matrix that corresponds to one frequency of analysis.
        """

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        rows = list()
        cols = list()
        data_T = list()

        for (_property, *args), data in self.model.properties.nodal_properties.items():

            if _property != "acoustic_transfer_element":
                continue

            et_data = self.preprocessor.get_acoustic_transfer_element_data(args, data)
            rows.extend(et_data["indexes_i"])
            cols.extend(et_data["indexes_j"])
            data_Te = et_data["data_Te"]

            if len(data_T):
                data_T = np.c_[data_T, data_Te]
            else:
                data_T = data_Te

        if len(data_T):
            full_T_link = [csr_matrix((data, (rows, cols)), shape=[total_dof, total_dof]) for data in data_T]
        else:
            full_T_link = [csr_matrix((total_dof, total_dof)) for _ in self.frequencies]

        T_link = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_T_link]
        Tr_link = [full[:, self.prescribed_indexes] for full in full_T_link]

        return T_link, Tr_link 

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
        
        data_Klump = list()
        ind_Klump = list()
        area_fluid = None

        # processing external elements by node
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property not in ["specific_impedance", "radiation_impedance"]:
                continue

            if not isinstance(data, dict):
                continue

            node_id = args[0]
            node = self.preprocessor.nodes[node_id]
            position = node.global_index

            element_ids = self.preprocessor.elements_connected_to_node.get(node_id)
            if len(element_ids) != 1:
                continue

            structural_element_type = self.preprocessor.get_structural_element_type(element_ids[0])
            if structural_element_type in ["beam_1", "rigid_element"]:
                continue

            cross_section = self.preprocessor.get_element_cross_section(element_ids[0])
            area_fluid = cross_section.area_fluid

            if property == "specific_impedance":
                impedance = data["values"][0]

            elif property == "radiation_impedance":
                impedance_type = data.get("impedance_type")
                element_attributes = self.preprocessor.elements_attributes.get(element_ids[0])

                act_calculator = AcousticCalculator(element_attributes)
                impedance = act_calculator.get_radiation_impedance(impedance_type, self.frequencies)

            ind_Klump.append(position)
            admittance = self.get_nodal_admittance(impedance, area_fluid, self.frequencies)

            if len(data_Klump):
                data_Klump = np.c_[data_Klump, admittance]
            else:
                data_Klump = admittance

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
                    raise TypeError("The Specific Impedance array and frequencies array must have the same length.")
                admittance = np.divide(1, Z)
        
        return admittance.reshape(-1, 1)#([len(frequencies),1])

    def get_array_of_values(self, value: (None | complex | np.ndarray), frequencies: np.ndarray) -> np.ndarray:

        if frequencies is not None:
            values = np.zeros(len(frequencies), dtype=complex)

        if value is not None:
            if isinstance(value, complex):
                values = value * np.ones_like(frequencies, dtype=complex)

            elif isinstance(value, np.ndarray):
                if frequencies is None:
                    values = np.array(value, dtype=complex)
                elif len(values) != len(frequencies):
                    raise TypeError("The Specific Impedance array and frequencies array must have the same length.")
                else:
                    values = value
        
        return values.reshape(-1, 1)#([len(frequencies),1])

    def get_lumped_matrices_for_FEM(self):
        """
        This method perform the assembly process of the acoustic FETM lumped matrices.

        Returns
        ----------
        K_lump : list
            List of lumped admittance matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Kr_lump : list
            List of lumped admittance matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
        """

        area_fluid = None
        ind_Clump = list()
        data_Clump = list()
        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        # processing external elements by node
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property not in ["specific_impedance", "radiation_impedance"]:
                continue

            if not isinstance(data, dict):
                continue

            node_id = args[0]
            node = self.preprocessor.nodes[node_id]
            position = node.global_index

            element_ids = self.preprocessor.elements_connected_to_node.get(node_id)
            if len(element_ids) != 1:
                continue

            cross_section = self.preprocessor.get_element_cross_section(element_ids[0])
            area_fluid = cross_section.area_fluid

            if property == "specific_impedance":
                impedance = data["values"][0]

            elif property == "radiation_impedance":

                impedance_type = data.get("impedance_type")
                if impedance_type != RadiationImpedanceType.ANECHOIC:
                    if not AnalysisID(self.model.analysis_id).is_modal():
                        continue

                element_attributes = self.preprocessor.elements_attributes.get(element_ids[0])

                act_calculator = AcousticCalculator(element_attributes)
                impedance = act_calculator.get_radiation_impedance(impedance_type, self.frequencies)

            ind_Clump.append(position)
            Z = self.get_array_of_values(impedance, self.frequencies)

            Ce = area_fluid / Z

            if len(data_Clump):
                data_Clump = np.c_[data_Clump, Ce]
            else:
                data_Clump = Ce

        if area_fluid is None:
            if self.frequencies is None:
                full_C = [csr_matrix((total_dof, total_dof), dtype=complex)]
            else:
                full_C = [csr_matrix((total_dof, total_dof), dtype=complex) for _ in self.frequencies]

        else:
            full_C = [csr_matrix((data, (ind_Clump, ind_Clump)), shape=[total_dof, total_dof], dtype=complex) for data in data_Clump]

        C_lump = [full[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for full in full_C]
        Cr_lump = [full[:, self.prescribed_indexes] for full in full_C]

        return C_lump, Cr_lump

    def get_global_matrices_for_modal_analysis(self):
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
        number_elements = len(self.preprocessor.elements_attributes)

        rows, cols = self.preprocessor.get_global_acoustic_indexes()
        mat_Ke = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=complex)
        mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=complex)

        for k, element_attributes in enumerate(self.preprocessor.elements_attributes.values()):

            if element_attributes.structural_element_type in ["beam_1", "rigid_element"]:
                continue

            element_attributes.acoustic_element_formulation = "FEM"
            length_correction = self.get_length_corretion(element_attributes)

            # build the acoustic element
            element = build_acoustic_element(element_attributes)

            mat_Ke[k, :, :], mat_Me[k, :, :] = element.fem_elementary_matrices(length_correction=length_correction)

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

        K_link = 0.
        M_link = 0.

        rows = list()
        cols = list()
        data_Klink = list()
        data_Mlink = list()

        total_dof = DOF_PER_NODE_ACOUSTIC * len(self.preprocessor.nodes)

        for (_property, *args), data in self.model.properties.nodal_properties.items():

            if _property != "psd_acoustic_link":
                continue

            psd_link_data = self.preprocessor.get_psd_acoustic_link_data(args)
            if psd_link_data is None:
                continue

            rows.extend(psd_link_data.indexes_rows)
            cols.extend(psd_link_data.indexes_cols)

            length = psd_link_data.length
            element_attributes = psd_link_data.element_attributes
            length_correction = self.get_length_correction_for_acoustic_link(psd_link_data.diameters)

            element = build_acoustic_element(element_attributes)
            data_Ke, data_Me = element.fem_elementary_link_matrices(length, length_correction = length_correction)

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
            if property not in ["volume_velocity", "reciprocating_compressor_excitation", "reciprocating_pump_excitation"]:
                continue

            node_id = args[0]
            node = self.preprocessor.nodes[node_id]
            position = node.global_index
            values = data["values"][0]

            if isinstance(values, complex):
                aux_ones = np.ones_like(self.frequencies)
                volume_velocity[:, position] = values * aux_ones

            elif isinstance(values, np.ndarray):
                volume_velocity[:, position] = values

        volume_velocity = volume_velocity[:, self.unprescribed_indexes]

        return volume_velocity