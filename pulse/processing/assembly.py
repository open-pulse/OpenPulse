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


    prescribed_dof = mesh.prescribed_dof()
    free_dof = np.delete(np.arange(total_dof), prescribed_dof)

    K = full_K[free_dof, :][:, free_dof]
    M = full_M[free_dof, :][:, free_dof]
    Kr = full_K[prescribed_dof, :]
    Mr = full_M[prescribed_dof, :]

    return K, M, Kr, Mr


def get_global_forces(mesh):
    total_dof = DOF_PER_ELEMENT * len(mesh.nodes)
    F = np.zeros(total_dof)
    for index, element in enumerate(mesh.elements.values()):
        start = index * DOF_PER_ELEMENT
        end = start + DOF_PER_ELEMENT
        F[start:end] = element.force_vector_gcs(np.array([0, 0, 0, 0, 0, 0]))
    return F