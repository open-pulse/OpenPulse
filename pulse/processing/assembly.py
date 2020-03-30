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
    Kr = full_K[prescribed_indexes, :]
    Mr = full_M[prescribed_indexes, :]

    return K, M, Kr, Mr

def get_global_forces(mesh):
    total_dof = DOF_PER_NODE * len(mesh.nodes)
    forces = np.zeros(total_dof)

    # distributed forces
    for element in mesh.elements.values():
        position = element.global_dof
        forces[position] += element.force_vector_gcs()

    # nodal forces
    for node in mesh.nodes.values():
        position = node.global_dof
        forces[position] += node.forces
    
    prescribed_indexes = mesh.get_prescribed_indexes()
    forces = np.delete(forces, prescribed_indexes)

    return forces
    
def new_get_global_matrices(mesh):
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

    K = csr_matrix((data_k, (rows, cols)), shape=[total_dof, total_dof])
    M = csr_matrix((data_m, (rows, cols)), shape=[total_dof, total_dof])

    return K, M

def new_get_global_forces(mesh):
    total_dof = DOF_PER_NODE * len(mesh.nodes)
    forces = np.zeros(total_dof)

    # distributed forces
    for element in mesh.elements.values():
        position = element.global_dof
        forces[position] += element.force_vector_gcs()

    # nodal forces
    for node in mesh.nodes.values():
        position = node.global_dof
        forces[position] += node.forces

    return forces