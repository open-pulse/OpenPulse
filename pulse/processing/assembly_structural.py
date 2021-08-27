from time import time
import numpy as np
from scipy.sparse import csr_matrix

from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL
from pulse.preprocessing.structural_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

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
    def __init__(self, preprocessor, frequencies, **kwargs):
        self.preprocessor = preprocessor
        self.frequencies = frequencies
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
        global_prescribed = []
        for node in self.preprocessor.nodes.values():
            if node.there_are_prescribed_dofs:
                starting_position = node.global_index * DOF_PER_NODE_STRUCTURAL
                dofs = np.array(node.get_prescribed_dofs_bc_indexes()) + starting_position
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
    
        global_prescribed = []
        list_prescribed_dofs = []
        if self.frequencies is None:
            number_frequencies = 1
        else:
            number_frequencies = len(self.frequencies)
        
        for node in self.preprocessor.nodes.values():
            if node.there_are_prescribed_dofs:
                global_prescribed.extend(node.get_prescribed_dofs_bc_values())      

        try:    
            aux_ones = np.ones(number_frequencies, dtype=complex)
            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_dofs.append(value[0:number_frequencies])
            array_prescribed_values = np.array(list_prescribed_dofs)
        except Exception as log_error:
            print(str(log_error))

        return global_prescribed, array_prescribed_values

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
        self.expansion_joint_data = {}

        rows, cols = self.preprocessor.get_global_structural_indexes()
        mat_Ke = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        
        for index, element in enumerate(self.preprocessor.structural_elements.values()):
            # mat_Ke[index,:,:], mat_Me[index,:,:] = element.matrices_gcs()
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

            rows = []
            cols = []  
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
        
        list_Kdata = []
        list_Mdata = []
        list_Cdata = []

        i_indexes_M, j_indexes_M = [], []
        i_indexes_K, j_indexes_K = [], []
        i_indexes_C, j_indexes_C = [], []
        
        self.nodes_with_lumped_masses = []
        self.nodes_connected_to_springs = []
        self.nodes_connected_to_dampers = []
        # self.nodes_with_nodal_elastic_links = []

        flag_Clump = False

        # processing external elements by node
        for node in self.preprocessor.nodes.values():

            # processing mass added
            if node.there_are_lumped_stiffness:
                position = node.global_dof
                self.nodes_connected_to_springs.append(node)
                list_Kdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_lumped_stiffness, node.lumped_stiffness))
                i_indexes_K.append(position)
                j_indexes_K.append(position)

            # processing mass added
            if node.there_are_lumped_masses:
                position = node.global_dof
                self.nodes_with_lumped_masses.append(node)
                list_Mdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_lumped_masses, node.lumped_masses))
                i_indexes_M.append(position)
                j_indexes_M.append(position)

            # processing damper added
            if node.there_are_lumped_dampings:
                position = node.global_dof
                self.nodes_connected_to_dampers.append(node)
                list_Cdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_lumped_dampings, node.lumped_dampings))
                i_indexes_C.append(position)
                j_indexes_C.append(position)
                flag_Clump = True
        
        for key, cluster_data in self.preprocessor.nodes_with_elastic_link_stiffness.items():
            node = self.preprocessor.nodes[int(key.split("-")[0])]
            for indexes_i, indexes_j, data, in cluster_data:
                for i in range(2):
                    i_indexes_K.append(indexes_i[i])
                    j_indexes_K.append(indexes_j[i])
                    list_Kdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_elastic_link_stiffness, data[i]))
        
        for key, cluster_data in self.preprocessor.nodes_with_elastic_link_dampings.items():
            node = self.preprocessor.nodes[int(key.split("-")[0])]
            for indexes_i, indexes_j, data, in cluster_data:
                for i in range(2):
                    i_indexes_C.append(indexes_i[i])
                    j_indexes_C.append(indexes_j[i])
                    list_Cdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_elastic_link_dampings, data[i]))

        data_Klump = np.array(list_Kdata).reshape(-1, cols)
        data_Mlump = np.array(list_Mdata).reshape(-1, cols)
        data_Clump = np.array(list_Cdata).reshape(-1, cols)
       
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
            cols = 1
        else:
            cols = len(self.frequencies)

        loads = np.zeros((total_dof, cols), dtype=complex)
        pressure_loads = np.zeros((total_dof, cols), dtype=complex)
    
        # stress stiffening loads
        if static_analysis:
            for element in self.preprocessor.structural_elements.values():
                position = element.global_dof
                loads[position] += element.force_vector_stress_stiffening() 
            return loads[self.unprescribed_indexes,:]

        # distributed loads
        for element in self.preprocessor.structural_elements.values():
            if np.sum(element.loaded_forces) != 0:
                position = element.global_dof
                loads[position] += element.force_vector_gcs()      

        # nodal loads
        for node in self.preprocessor.nodes.values():
            if node.there_are_nodal_loads:
                position = node.global_dof
                if node.loaded_table_for_nodal_loads:
                    temp_loads = [np.zeros_like(self.frequencies) if bc is None else bc for bc in node.nodal_loads]
                else:
                    temp_loads = [np.zeros_like(self.frequencies) if bc is None else np.ones_like(self.frequencies)*bc for bc in node.nodal_loads]
                loads[position, :] += temp_loads
           
        loads = loads[self.unprescribed_indexes,:]
        
        if self.acoustic_solution is not None:
            for element in self.preprocessor.structural_elements.values():
                pressure_first = self.acoustic_solution[element.first_node.global_index, :]
                pressure_last = self.acoustic_solution[element.last_node.global_index, :]
                pressure_avg = (pressure_first + pressure_last) / 2
                position = element.global_dof
                pressure_loads[position, :] += element.force_vector_acoustic_gcs(self.frequencies, pressure_avg, pressure_external)
        
        pressure_loads = pressure_loads[self.unprescribed_indexes,:]

        if loads_matrix3D:
            loads = loads.T.reshape((len(self.frequencies), loads.shape[0], 1))
            loads += pressure_loads.T.reshape((len(self.frequencies), pressure_loads.shape[0],1))
        else:
            loads += pressure_loads

        return loads
    
    def get_bc_array_for_all_frequencies(self, loaded_table, boundary_condition):
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

        if loaded_table:
            list_arrays = [np.zeros(number_frequencies, dtype=float) if bc is None else bc[0:number_frequencies] for bc in boundary_condition]
            self.no_table = False
        else:
            list_arrays = [np.zeros(number_frequencies, dtype=float) if bc is None else np.ones(number_frequencies, dtype=float)*bc for bc in boundary_condition]

        return list_arrays
