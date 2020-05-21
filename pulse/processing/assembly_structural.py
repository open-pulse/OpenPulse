from time import time
import numpy as np
from scipy.sparse import csr_matrix

from pulse.utils import timer
from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL
from pulse.preprocessing.element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT


class AssemblyStructural:
    def __init__(self, mesh):
        self.mesh = mesh

    def get_prescribed_indexes(self):
        global_prescribed = []
        for node in self.mesh.nodes.values():
            # print(node.global_index)
            starting_position = node.global_index * DOF_PER_NODE_STRUCTURAL
            dofs = np.array(node.get_structural_boundary_condition_indexes()) + starting_position
            global_prescribed.extend(dofs)
        return global_prescribed

    def get_prescribed_values(self):
        global_prescribed = []
        for node in self.mesh.nodes.values():
            global_prescribed.extend(node.get_structural_boundary_condition_values())
        return global_prescribed

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

        data_Mlump = []
        data_Klump = []
        data_Clump = []

        ind_Mlump = []
        ind_Klump = []
        ind_Clump = []

        flag_Clump = False

        # processing external elements by node
        for node in self.mesh.nodes.values():
            # processing mass added
            if np.sum(node.spring) == 0:
                continue
            else:
                position = node.global_dof
                data_Klump.append(node.spring)
                ind_Klump.append(position)
            # processing mass added
            if np.sum(node.mass) == 0:
                continue
            else:
                position = node.global_dof
                data_Mlump.append(node.mass)
                ind_Mlump.append(position)
            # processing damper added
            if np.sum(node.damper) == 0:
                continue
            else:
                position = node.global_dof
                data_Clump.append(node.damper)
                ind_Clump.append(position)
                flag_Clump = True
            
        data_Klump = np.array(data_Klump).flatten()
        data_Mlump = np.array(data_Mlump).flatten()
        data_Clump = np.array(data_Clump).flatten()
        
        ind_Klump = np.array(ind_Klump).flatten()
        ind_Mlump = np.array(ind_Mlump).flatten()
        ind_Clump = np.array(ind_Clump).flatten()
        
        full_K = csr_matrix((data_Klump, (ind_Klump, ind_Klump)), shape=[total_dof, total_dof])
        full_M = csr_matrix((data_Mlump, (ind_Mlump, ind_Mlump)), shape=[total_dof, total_dof])
        full_C = csr_matrix((data_Clump, (ind_Clump, ind_Clump)), shape=[total_dof, total_dof])

        prescribed_indexes = self.get_prescribed_indexes()
        unprescribed_indexes = self.get_unprescribed_indexes()

        K_lump = full_K[unprescribed_indexes, :][:, unprescribed_indexes]
        M_lump = full_M[unprescribed_indexes, :][:, unprescribed_indexes]
        C_lump = full_C[unprescribed_indexes, :][:, unprescribed_indexes]

        Kr_lump = full_K[:, prescribed_indexes]
        Mr_lump = full_M[:, prescribed_indexes]
        Cr_lump = full_C[:, prescribed_indexes]

        return K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump
        
    def get_all_matrices(self):
        
        K, M, Kr, Mr = self.get_global_matrices()
        K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump = self.get_lumped_matrices()
        
        Kadd_lump = K + K_lump
        Madd_lump = M + M_lump

        return Kadd_lump, Madd_lump, K, M, Kr, Mr, K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump

    def get_global_loads(self, frequencies, loads_matrix3D=False):

        total_dof = DOF_PER_NODE_STRUCTURAL * len(self.mesh.nodes)
        loads = np.zeros(total_dof)

        # distributed loads
        for element in self.mesh.structural_elements.values():
            if np.sum(element.loaded_forces) == 0:
                continue
            position = element.global_dof
            loads[position] += element.force_vector_gcs()

        # nodal loads
        for node in self.mesh.nodes.values():
            if np.sum(node.forces) == 0:
                continue
            position = node.global_dof
            loads[position] += node.forces
            
        unprescribed_indexes = self.get_unprescribed_indexes()
        loads = loads[unprescribed_indexes]

        if loads_matrix3D:
            loads = loads.reshape(-1, 1)*np.ones((len(frequencies),1,1))
        else:
            loads = loads.reshape(-1, 1)@np.ones((1, len(frequencies)))

        return loads