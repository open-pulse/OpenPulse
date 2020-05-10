import time

import numpy as np
from scipy.sparse import csr_matrix

from pulse.utils import timer
from pulse.preprocessing.node import DOF_PER_NODE
from pulse.preprocessing.element import ENTRIES_PER_ELEMENT, DOF_PER_ELEMENT


def get_global_matrices(mesh):

    total_dof = DOF_PER_NODE * len(mesh.nodes)
    total_entries = ENTRIES_PER_ELEMENT * len(mesh.elements)

    rows = np.zeros(total_entries)
    cols = np.zeros(total_entries)
    data_k = np.zeros(total_entries)
    data_m = np.zeros(total_entries)

    for index, element in enumerate(mesh.elements.values()):

        start = index * ENTRIES_PER_ELEMENT
        end = start + ENTRIES_PER_ELEMENT 

        i, j = element.global_matrix_indexes()
        Ke, Me = element.matrices_gcs()
        
        rows[start:end] = i.flatten()
        cols[start:end] = j.flatten()
        data_k[start:end] = Ke.flatten()
        data_m[start:end] = Me.flatten()

    full_K = csr_matrix((data_k, (rows, cols)), shape=[total_dof, total_dof])
    full_M = csr_matrix((data_m, (rows, cols)), shape=[total_dof, total_dof])

    prescribed_indexes = mesh.get_prescribed_indexes()
    unprescribed_indexes = mesh.get_unprescribed_indexes()

    K = full_K[unprescribed_indexes, :][:, unprescribed_indexes]
    M = full_M[unprescribed_indexes, :][:, unprescribed_indexes]
    Kr = full_K[:, prescribed_indexes]
    Mr = full_M[:, prescribed_indexes]

    return K, M, Kr, Mr
    
def get_lumped_matrices(mesh):

    total_dof = DOF_PER_NODE * len(mesh.nodes)
    
    data_Mlump = np.zeros(total_dof)
    data_Klump = np.zeros(total_dof)
    data_Clump = np.zeros(total_dof)
    
    ind_Mlump = np.zeros(total_dof)
    ind_Klump = np.zeros(total_dof)
    ind_Clump = np.zeros(total_dof)

    flag_Clump = False

    # processing external elements by node
    for index, node in enumerate(mesh.nodes.values()):
        if np.sum(node.spring) == 0:
            continue
        start = index * DOF_PER_NODE
        # print(start)
        end = start + DOF_PER_NODE 
        # print(end)
        position = node.global_dof
        # print(position)
        # print(node.spring)

        data_Klump[start:end] = node.spring
        ind_Klump[start:end] = position
  
    for index, node in enumerate(mesh.nodes.values()):
        if np.sum(node.mass) == 0:
            continue
        start = index * DOF_PER_NODE
        # print(start)
        end = start + DOF_PER_NODE 
        # print(end)
        position = node.global_dof
        # print(position)
        # print(node.mass)

        data_Mlump[start:end] = node.mass
        ind_Mlump[start:end] = position

    for index, node in enumerate(mesh.nodes.values()):
        if np.sum(node.damper) == 0:
            continue
        start = index * DOF_PER_NODE
        # print(start)
        end = start + DOF_PER_NODE 
        # print(end)
        position = node.global_dof
        # print(position)
        # print(node.damper)

        data_Clump[start:end] = node.damper
        ind_Clump[start:end] = position
        flag_Clump = True


    full_K = csr_matrix((data_Klump, (ind_Klump, ind_Klump)), shape=[total_dof, total_dof])
    full_M = csr_matrix((data_Mlump, (ind_Mlump, ind_Mlump)), shape=[total_dof, total_dof])
    full_C = csr_matrix((data_Clump, (ind_Clump, ind_Clump)), shape=[total_dof, total_dof])

    prescribed_indexes = mesh.get_prescribed_indexes()
    unprescribed_indexes = mesh.get_unprescribed_indexes()

    K_lump = full_K[unprescribed_indexes, :][:, unprescribed_indexes]
    M_lump = full_M[unprescribed_indexes, :][:, unprescribed_indexes]
    C_lump = full_C[unprescribed_indexes, :][:, unprescribed_indexes]

    Kr_lump = full_K[:, prescribed_indexes]
    Mr_lump = full_M[:, prescribed_indexes]
    Cr_lump = full_C[:, prescribed_indexes]

    return K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump
    
def get_all_matrices(mesh):
    
    K, M, Kr, Mr = get_global_matrices(mesh)
    K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump = get_lumped_matrices(mesh)
    
    Kadd_lump = K + K_lump
    Madd_lump = M + M_lump

    return Kadd_lump, Madd_lump, K, M, Kr, Mr, K_lump, M_lump, C_lump, Kr_lump, Mr_lump, Cr_lump, flag_Clump


def get_global_forces(mesh):

    total_dof = DOF_PER_NODE * len(mesh.nodes)
    forces = np.zeros(total_dof)

    # distributed loads
    for element in mesh.elements.values():
        if np.sum(element.loaded_forces) == 0:
            continue
        position = element.global_dof
        forces[position] += element.force_vector_gcs()

    # nodal loads
    for node in mesh.nodes.values():
        if np.sum(node.forces) == 0:
            continue
        position = node.global_dof
        forces[position] += node.forces
    
    # prescribed_indexes = mesh.get_prescribed_indexes()
    # forces = np.delete(forces, prescribed_indexes)
    
    unprescribed_indexes = mesh.get_unprescribed_indexes()
    forces = forces[unprescribed_indexes]

    return forces