from time import time
import numpy as np
from scipy.sparse import csr_matrix

from pulse.utils import timer, error
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL
from pulse.preprocessing.structural_element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT

class AssemblyStructural:
    def __init__(self, mesh, frequencies, **kwargs):
        self.mesh = mesh
        self.frequencies = frequencies
        self.acoustic_solution = kwargs.get('acoustic_solution', None)
        self.no_table = True

    def get_prescribed_indexes(self):
        global_prescribed = []
        for node in self.mesh.nodes.values():
            if node.there_are_prescribed_dofs:
                starting_position = node.global_index * DOF_PER_NODE_STRUCTURAL
                dofs = np.array(node.get_prescribed_dofs_bc_indexes()) + starting_position
                global_prescribed.extend(dofs)
        return global_prescribed

    def get_prescribed_values(self):
    
        global_prescribed = []
        list_prescribed_dofs = []
        if self.frequencies is None:
            cols = 1
        else:
            cols = len(self.frequencies)
        
        for node in self.mesh.nodes.values():
            if node.there_are_prescribed_dofs:
                global_prescribed.extend(node.get_prescribed_dofs_bc_values())      

        try:    
            aux_ones = np.ones(cols, dtype=complex)
            for value in global_prescribed:
                if isinstance(value, complex):
                    list_prescribed_dofs.append(aux_ones*value)
                elif isinstance(value, np.ndarray):
                    list_prescribed_dofs.append(value)
            array_prescribed_values = np.array(list_prescribed_dofs)
        except Exception as e:
            error(str(e))

        return global_prescribed, array_prescribed_values

    def get_unprescribed_indexes(self):
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.mesh.nodes)
        all_indexes = np.arange(total_dof)
        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = np.delete(all_indexes, prescribed_indexes)
        return unprescribed_indexes

    def get_global_matrices(self):
 
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.mesh.nodes)
        number_elements = len(self.mesh.structural_elements)

        rows, cols = self.mesh.get_global_structural_indexes()
        mat_Ke = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)
        mat_Me = np.zeros((number_elements, DOF_PER_ELEMENT, DOF_PER_ELEMENT), dtype=float)

        for index, element in enumerate(self.mesh.structural_elements.values()):
            mat_Ke[index,:,:], mat_Me[index,:,:] = element.matrices_gcs() 

        # np.savetxt('Me.csv', mat_Me[0,:,:], delimiter=",")
        # np.savetxt('Ke.csv', mat_Ke[0,:,:], delimiter=",")

        full_K = csr_matrix((mat_Ke.flatten(), (rows, cols)), shape=[total_dof, total_dof])
        full_M = csr_matrix((mat_Me.flatten(), (rows, cols)), shape=[total_dof, total_dof])

        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = self.get_unprescribed_indexes()

        K = full_K[unprescribed_indexes, :][:, unprescribed_indexes]
        M = full_M[unprescribed_indexes, :][:, unprescribed_indexes]
        Kr = full_K[:, prescribed_indexes]
        Mr = full_M[:, prescribed_indexes]

        return K, M, Kr, Mr
        
    def get_lumped_matrices(self):

        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.mesh.nodes)
        
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
        self.nodes_with_nodal_elastic_links = []

        flag_Clump = False

        # processing external elements by node
        for node in self.mesh.nodes.values():

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
        
        for cluster_data in self.mesh.dict_nodes_with_elastic_link_stiffness.values():
            for indexes_i, indexes_j, data, in cluster_data:
                for i in range(2):
                    i_indexes_K.append(indexes_i[i])
                    j_indexes_K.append(indexes_j[i])
                    list_Kdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_elastic_link_stiffness, data[i]))

        for cluster_data in self.mesh.dict_nodes_with_elastic_link_damping.values():
            for indexes_i, indexes_j, data, in cluster_data:
                for i in range(2):
                    i_indexes_C.append(indexes_i[i])
                    j_indexes_C.append(indexes_j[i])
                    list_Cdata.append(self.get_bc_array_for_all_frequencies(node.loaded_table_for_elastic_link_damping, data[i]))

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

        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = self.get_unprescribed_indexes()

        K_lump = [sparse_matrix[unprescribed_indexes, :][:, unprescribed_indexes] for sparse_matrix in full_K]
        M_lump = [sparse_matrix[unprescribed_indexes, :][:, unprescribed_indexes] for sparse_matrix in full_M]
        C_lump = [sparse_matrix[unprescribed_indexes, :][:, unprescribed_indexes] for sparse_matrix in full_C]

        Kr_lump = [sparse_matrix[:, prescribed_indexes] for sparse_matrix in full_K]
        Mr_lump = [sparse_matrix[:, prescribed_indexes] for sparse_matrix in full_M]
        Cr_lump = [sparse_matrix[:, prescribed_indexes] for sparse_matrix in full_C]

        return K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump
        
    def get_global_loads(self, pressure_external = 0, loads_matrix3D=False):
        
        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.mesh.nodes)
        cols = len(self.frequencies)
        loads = np.zeros((total_dof, cols), dtype=complex)
        pressure_loads = np.zeros((total_dof, cols), dtype=complex)

        # distributed loads
        for element in self.mesh.structural_elements.values():
            if np.sum(element.loaded_forces) != 0:
                position = element.global_dof
                loads[position] += element.force_vector_gcs()      

        # nodal loads
        for node in self.mesh.nodes.values():
            if node.there_are_nodal_loads:
                position = node.global_dof
                if node.loaded_table_for_nodal_loads:
                    temp_loads = [np.zeros_like(self.frequencies) if bc is None else bc for bc in node.nodal_loads]
                else:
                    temp_loads = [np.zeros_like(self.frequencies) if bc is None else np.ones_like(self.frequencies)*bc for bc in node.nodal_loads]
                loads[position, :] += temp_loads
           
        unprescribed_indexes = self.get_unprescribed_indexes()
        loads = loads[unprescribed_indexes,:]
        
        if self.acoustic_solution is not None:
            for element in self.mesh.structural_elements.values():
                pressure_first = self.acoustic_solution[element.first_node.global_index, :]
                pressure_last = self.acoustic_solution[element.last_node.global_index, :]
                pressure_avg = (pressure_first + pressure_last) / 2
                position = element.global_dof
                pressure_loads[position, :] += element.force_vector_acoustic_gcs(self.frequencies, pressure_avg, pressure_external)
        
        pressure_loads = pressure_loads[unprescribed_indexes,:]

        if loads_matrix3D:
            loads = loads.T.reshape((len(self.frequencies), loads.shape[0], 1))
            loads += pressure_loads.T.reshape((len(self.frequencies), pressure_loads.shape[0],1))
        else:
            loads += pressure_loads

        return loads
    
    def get_bc_array_for_all_frequencies(self, there_are_table, boundary_condition):
       
        if there_are_table:
            list_arrays = [np.zeros_like(self.frequencies) if bc is None else bc for bc in boundary_condition]
            self.no_table = False
        else:
            if self.frequencies is None:
                frequencies = 1
            else:
                frequencies = self.frequencies
            list_arrays = [np.zeros_like(frequencies) if bc is None else np.ones_like(frequencies)*bc for bc in boundary_condition]
        return list_arrays
