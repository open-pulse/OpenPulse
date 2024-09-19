# fmt: off

from pulse.model.node import DOF_PER_NODE_STRUCTURAL
from pulse.model.model import Model
from pulse.model.structural_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

import numpy as np
from scipy.sparse import csr_matrix
from time import time


class AssemblyStructural:
    """ This class creates a structural assembly object from input data.

    Parameters
    ----------
    preprocessor : Preprocessor object
        Acoustic finite element preprocessor.

    frequencies : array
        Frequencies of analysis.

    acoustic_solution : array, optional
        Solution of the acoustic FETM model. This solution is need to solve the coupled problem.
        Default is None.
    """

    def __init__(self, model: Model, **kwargs):

        self.model = model
        self.preprocessor = model.preprocessor
        self.frequencies = model.frequencies
        self.acoustic_solution = kwargs.get('acoustic_solution', None)
        self.no_table = True

        self.prescribed_indexes = self.get_prescribed_indexes()
        self.unprescribed_indexes = self.get_unprescribed_indexes()


    def get_prescribed_indexes(self):
        """
        This method returns all the indexes of the structural degrees of freedom with prescribed structural displacement or rotation boundary conditions.

        Returns
        ----------
        array
            Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        See also
        --------
        get_prescribed_values : Vaslues of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_unprescribed_indexes : Indexes of the structural free degrees of freedom.
        """

        global_prescribed = list()
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "prescribed_dofs":

                node_id = args[0]
                node = self.preprocessor.nodes[node_id]
                values = data["values"]

                starting_position = node.global_index * DOF_PER_NODE_STRUCTURAL
                internal_dofs = [i for i, value in enumerate(values) if value is not None]

                dofs = starting_position + np.array(internal_dofs)
                global_prescribed.extend(dofs)

        return global_prescribed


    def get_prescribed_values(self):
        """
        This method returns all the values of the structural degrees of freedom with prescribed structural displacement or rotation boundary conditions.

        Returns
        ----------
        array
            Values of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        See also
        --------
        get_prescribed_indexes : Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_unprescribed_indexes : Indexes of the structural free degrees of freedom.
        """
    
        global_prescribed = list()
        list_of_arrays = list()
        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)
        
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "prescribed_dofs":
                # node_id = args
                values = data["values"]
                global_prescribed.extend([value for value in values if value is not None])   

        try:

            aux_ones = np.ones(number_frequencies, dtype=complex)
            for value in global_prescribed:
                if isinstance(value, complex):
                    list_of_arrays.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_of_arrays.append(value[0:number_frequencies])

            array_of_values = np.array(list_of_arrays)

        except Exception as _error_log:
            print(str(_error_log))

        return global_prescribed, array_of_values


    def get_unprescribed_indexes(self):
        """
        This method returns all the indexes of the structural free degrees of freedom.

        Returns
        ----------
        array
            Indexes of the structural free degrees of freedom.

        See also
        --------
        get_prescribed_indexes : Indexes of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.

        get_prescribed_values : Values of the structural degrees of freedom with prescribed displacement or rotation boundary conditions.
        """
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)
        all_indexes = np.arange(total_dof)
        return np.delete(all_indexes, self.prescribed_indexes)


    def get_global_matrices(self):
        """
        This method perform the assembly process of the structural FEM matrices.

        Returns
        ----------
        K : list
            List of stiffness matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix.
            
        M : list
            List of mass matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix.

        Kr : list
            List of stiffness matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix.

        Mr : list
            List of mass matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix.
        """
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)
        number_elements = len(self.preprocessor.structural_elements)
        self.expansion_joint_data = dict()

        rows, cols = self.preprocessor.get_global_structural_indexes()
        mat_Ke = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        
        for index, element in enumerate(self.preprocessor.structural_elements.values()):
            if element.element_type == "expansion_joint":
                self.expansion_joint_data[index] = element
            else:
                mat_Ke[index,:,:], mat_Me[index,:,:] = element.matrices_gcs()
  
        full_K = csr_matrix((mat_Ke.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        full_M = csr_matrix((mat_Me.flatten(), (rows, cols)), shape=[total_dof, total_dof])

        K = full_K[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        M = full_M[self.unprescribed_indexes, :][:, self.unprescribed_indexes]
        Kr = full_K[:, self.prescribed_indexes]
        Mr = full_M[:, self.prescribed_indexes]

        return K, M, Kr, Mr


    def get_expansion_joint_global_matrices(self):
        
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)
        number_elements = len(self.expansion_joint_data)
        
        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        if number_elements == 0:

            full_K = [csr_matrix(([], ([], [])), shape=[total_dof, total_dof]) for _ in range(number_frequencies)]
            full_M = csr_matrix(([], ([], [])), shape=[total_dof, total_dof])

        else: 

            rows = list()
            cols = list()

            mat_Ke = np.zeros((number_frequencies, number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
            mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

            for ind, element in enumerate(self.expansion_joint_data.values()):
                
                i, j = element.global_matrix_indexes()
                rows.append(i)
                cols.append(j)
                mat_Ke[:,ind,:,:], mat_Me[ind,:,:] = element.expansion_joint_matrices_gcs(self.frequencies) 
            
            rows = np.array(rows).flatten()
            cols = np.array(cols).flatten()   

            full_K = [csr_matrix((mat_Ke[j,:,:,:].flatten(), (rows, cols)), shape=[total_dof, total_dof]) for j in range(number_frequencies)]
            full_M = csr_matrix((mat_Me.flatten(), (rows, cols)), shape=[total_dof, total_dof])

        K = [sparse_matrix[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for sparse_matrix in full_K]
        M = full_M[self.unprescribed_indexes, :][:, self.unprescribed_indexes]

        Kr = [sparse_matrix[:, self.prescribed_indexes] for sparse_matrix in full_K]
        Mr = full_M[:, self.prescribed_indexes]
 
        return K, M, Kr, Mr
        

    def get_lumped_matrices(self):
        """
        This method perform the assembly process of the structural FEM lumped matrices.

        Returns
        ----------
        K_lump : list
            List of lumped stiffness matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
            
        M_lump : list
            List of mass matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.
            
        C_lump : list
            List of lumped damping matrices of the free degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Kr_lump  : list
            List of lumped stiffness matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Mr_lump  : list
            List of lumped mass matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        Cr_lump  : list
            List of lumped damping matrices of the prescribed degree of freedom. Each item of the list is a sparse csr_matrix that corresponds to one frequency of analysis.

        flag_Clump  : boll
            This flag returns True if the damping matrices are non zero, and False otherwise.
        """
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)
        
        if self.frequencies is None:
            cols = 1
        else:
            cols = len(self.frequencies)
        
        K_data = list()
        M_data = list()
        C_data = list()

        i_indexes_M, j_indexes_M = list(), list()
        i_indexes_K, j_indexes_K = list(), list()
        i_indexes_C, j_indexes_C = list(), list()

        flag_Clump = False

        _properties = [  
                        "lumped_masses",
                        "lumped_stiffness",
                        "lumped_dampings",
                        "psd_structural_links",
                        "structural_stiffness_links",
                        "structural_damping_links"
                       ]

        for (_property, *args), data in self.model.properties.nodal_properties.items():

            if _property not in _properties:
                continue

            if len(args) == 1:
                node_id = args[0]
                position = self.preprocessor.nodes[node_id].global_dof

            elif len(args) == 2:
                node_ids = args

            loaded_table = "table_names" in data.keys()

            # processing lumped masses
            if _property == "lumped_masses":
                i_indexes_M.extend(position)
                j_indexes_M.extend(position)
                values = data["values"]
                M_data.extend(self.get_bc_array_for_all_frequencies(loaded_table, values))

            # processing lumped stiffness
            if _property == "lumped_stiffness":
                i_indexes_K.extend(position)
                j_indexes_K.extend(position)
                values = data["values"]
                K_data.extend(self.get_bc_array_for_all_frequencies(loaded_table, values))

            # processing lumped dampers
            if _property == "lumped_dampings":
                i_indexes_C.extend(position)
                j_indexes_C.extend(position)
                flag_Clump = True
                values = data["values"]
                C_data.extend(self.get_bc_array_for_all_frequencies(loaded_table, values))

            # structural elastic link in PSDs
            if _property == "psd_structural_links":
                psd_link_data = self.preprocessor.get_psd_structural_link_data(node_ids)
                i_indexes_K.extend(psd_link_data["indexes_i"])
                j_indexes_K.extend(psd_link_data["indexes_j"])
                values = psd_link_data["data"]
                K_data.extend(self.get_bc_array_for_all_frequencies(False, values))

            # structural nodal link for stiffness
            if _property == "structural_stiffness_links":
                link_data_K = self.preprocessor.get_structural_links_data(node_ids, data)
                i_indexes_K.extend(link_data_K["indexes_i"])
                j_indexes_K.extend(link_data_K["indexes_j"])
                values = link_data_K["data"]
                K_data.extend(self.get_bc_array_for_all_frequencies(loaded_table, values))

            # structural nodal link for damping
            if _property == "structural_damping_links":
                link_data_C = self.preprocessor.get_structural_links_data(node_ids, data)
                i_indexes_C.extend(link_data_C["indexes_i"])
                j_indexes_C.extend(link_data_C["indexes_j"])
                values = link_data_C["data"]
                C_data.extend(self.get_bc_array_for_all_frequencies(loaded_table, values))

        data_Klump = np.array(K_data).reshape(-1, cols)
        data_Mlump = np.array(M_data).reshape(-1, cols)
        data_Clump = np.array(C_data).reshape(-1, cols)

        i_indexes_K = np.array(i_indexes_K).flatten()
        i_indexes_M = np.array(i_indexes_M).flatten()
        i_indexes_C = np.array(i_indexes_C).flatten()

        j_indexes_K = np.array(j_indexes_K).flatten()
        j_indexes_M = np.array(j_indexes_M).flatten()
        j_indexes_C = np.array(j_indexes_C).flatten()

        full_K = [csr_matrix((data_Klump[:,j], (i_indexes_K, j_indexes_K)), shape=[total_dof, total_dof]) for j in range(cols)]
        full_M = [csr_matrix((data_Mlump[:,j], (i_indexes_M, j_indexes_M)), shape=[total_dof, total_dof]) for j in range(cols)]
        full_C = [csr_matrix((data_Clump[:,j], (i_indexes_C, j_indexes_C)), shape=[total_dof, total_dof]) for j in range(cols)]
                
        K_lump = [sparse_matrix[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for sparse_matrix in full_K]
        M_lump = [sparse_matrix[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for sparse_matrix in full_M]
        C_lump = [sparse_matrix[self.unprescribed_indexes, :][:, self.unprescribed_indexes] for sparse_matrix in full_C]

        Kr_lump = [sparse_matrix[:, self.prescribed_indexes] for sparse_matrix in full_K]
        Mr_lump = [sparse_matrix[:, self.prescribed_indexes] for sparse_matrix in full_M]
        Cr_lump = [sparse_matrix[:, self.prescribed_indexes] for sparse_matrix in full_C]

        return K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump


    def get_global_loads_for_stress_stiffening(self):
        """
        This method perform the assembly process of the structural FEM force and moment loads.

        Parameters
        ----------
        pressure_external : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.

        loads_matrix3D : boll, optional
            
            Default is False.

        Returns
        ----------
        array
            Loads vectors. Each column corresponds to a frequency of analysis.
        """

        cols = 1
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)
        loads = np.zeros((total_dof, cols), dtype=complex)
    
        # stress stiffening loads
        for element in self.preprocessor.structural_elements.values():
            position = element.global_dof
            loads[position] += element.force_vector_stress_stiffening()

        return loads[self.unprescribed_indexes,:]


    def get_global_loads_for_static_analysis(self):
        """
        This method perform the assembly process of the structural FEM force and moment loads.

        Parameters
        ----------
        pressure_external : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.

        loads_matrix3D : boll, optional
            
            Default is False.

        Returns
        ----------
        array
            Loads vectors. Each column corresponds to a frequency of analysis.
        """
        try:

            cols = 1
            total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)

            _frequencies = np.array([0.], dtype=float)
            loads = np.zeros((total_dof, cols), dtype=complex)
        
            # elementary loads - element integration
            for element in self.preprocessor.structural_elements.values():

                position = element.global_dof
                # self-weight loads
                if self.model.weight_load:
                    loads[position] += element.get_self_weighted_load(self.model.gravity_vector)

                # stress stiffening loads
                if self.model.internal_pressure_load:
                    loads[position] += element.force_vector_stress_stiffening()

                # distributed loads
                if self.model.element_distributed_load:
                    loads[position] += element.get_distributed_load()

            if self.model.external_nodal_loads:
                # nodal loads
                for (property, *args), data in self.model.properties.nodal_properties.items():
                    if property == "nodal_loads":

                        node_id = args[0]
                        node = self.preprocessor.nodes[node_id]
                        position = node.global_dof
                        values = data["values"]

                        if "table_names" in data.keys():
                            temp_loads = [_frequencies if bc is None else bc for bc in values]
                        else:
                            temp_loads = [_frequencies if bc is None else np.ones_like(_frequencies)*bc for bc in values]
                        loads[position, :] += temp_loads

        except Exception as _error_log:
            print(str(_error_log))
                  
        return loads[self.unprescribed_indexes,:]


    def get_global_loads(self, pressure_external = 0, loads_matrix3D=False, static_analysis=False):
        """
        This method perform the assembly process of the structural FEM force and moment loads.

        Parameters
        ----------
        pressure_external : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.

        loads_matrix3D : boll, optional
            
            Default is False.

        Returns
        ----------
        array
            Loads vectors. Each column corresponds to a frequency of analysis.
        """
        
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.preprocessor.nodes)

        if self.frequencies is None or static_analysis:
            _frequencies = np.array([0.], dtype=float)
        else:
            _frequencies = self.frequencies

        cols = len(_frequencies)
        loads = np.zeros((total_dof, cols), dtype=complex)
        pressure_loads = np.zeros((total_dof, cols), dtype=complex)

        if static_analysis:
            return self.get_global_loads_for_static_analysis()

        # distributed loads
        for element in self.preprocessor.structural_elements.values():
            position = element.global_dof 
            loads[position] += element.get_distributed_load()
  
        # nodal loads
        for (property, *args), data in self.model.properties.nodal_properties.items():
            if property == "nodal_loads":

                node_id = args[0]
                node = self.preprocessor.nodes[node_id]
                position = node.global_dof
                values = data["values"]

                if "table_names" in data.keys():
                    temp_loads = [np.zeros_like(_frequencies) if bc is None else bc for bc in values]
                else:
                    temp_loads = [np.zeros_like(_frequencies) if bc is None else np.ones_like(_frequencies)*bc for bc in values]

                loads[position, :] += temp_loads

        # for node in self.preprocessor.nodes.values():
        #     if node.there_are_nodal_loads:
        #         position = node.global_dof
        #         if node.loaded_table_for_nodal_loads:
        #             temp_loads = [np.zeros_like(_frequencies) if bc is None else bc for bc in values]
        #         else:
        #             temp_loads = [np.zeros_like(_frequencies) if bc is None else np.ones_like(_frequencies)*bc for bc in values]
        #         loads[position, :] += temp_loads

        loads = loads[self.unprescribed_indexes, :]
        
        # acoustic-structural loads
        if self.acoustic_solution is not None:
            for element in self.preprocessor.structural_elements.values():
                pressure_first = self.acoustic_solution[element.first_node.global_index, :]
                pressure_last = self.acoustic_solution[element.last_node.global_index, :]
                pressure = np.c_[pressure_first, pressure_last].T
                position = element.global_dof
                pressure_loads[position, :] += element.force_vector_acoustic_gcs(   
                                                                                    _frequencies, 
                                                                                    pressure, 
                                                                                    pressure_external
                                                                                 )

        pressure_loads = pressure_loads[self.unprescribed_indexes,:]

        if loads_matrix3D:
            loads = loads.T.reshape((len(_frequencies), loads.shape[0], 1))
            loads += pressure_loads.T.reshape((len(_frequencies), pressure_loads.shape[0],1))
        else:
            loads += pressure_loads

        return loads
    

    def get_bc_array_for_all_frequencies(self, loaded_table, values):
        """
        This method perform the assembly process of the structural FEM force and moment loads.

        Parameters
        ----------
        pressure_external : float, optional
            Static pressure difference between atmosphere and the fluid in the pipeline.
            Default is 0.

        loads_matrix3D : boll, optional
            
            Default is False.

        Returns
        ----------
        array
            Loads vectors. Each column corresponds to a frequency of analysis.
        """
        if self.frequencies is None:
           number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)

        ones = np.ones(number_frequencies, dtype=float)
        zeros = np.zeros(number_frequencies, dtype=float)

        if loaded_table:
            list_arrays = [zeros if value is None else value[0:number_frequencies] for value in values]
            self.no_table = False
        else:
            list_arrays = [zeros if value is None else ones * value for value in values]

        return list_arrays