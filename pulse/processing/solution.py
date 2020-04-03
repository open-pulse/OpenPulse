from time import time

import numpy as np
from scipy.sparse.linalg import eigs, spsolve

from pulse.utils import timer
from pulse.processing.assembly import get_global_matrices, get_global_forces


def modal_analysis(modes, stiffness_matrix, mass_matrix, *args, **kwargs):
    eigen_values, eigen_vectors = eigs(stiffness_matrix, M=mass_matrix, k=modes, *args, **kwargs)

    positive_real = np.absolute(np.real(eigen_values))
    natural_frequencies = np.sqrt(positive_real)/(2*np.pi)
    modal_shape = np.real(eigen_vectors)

    index_order = np.argsort(natural_frequencies)
    natural_frequencies = natural_frequencies[index_order]
    modal_shape = modal_shape[:, index_order]

    return natural_frequencies, modal_shape

def direct_method(forces, frequencies, stiffness_matrix, mass_matrix, **kwargs):
    alpha_v = kwargs.get('alpha_v', 0)
    beta_v = kwargs.get('beta_v', 0)
    alpha_h = kwargs.get('alpha_h', 0)
    beta_h = kwargs.get('beta_h', 0)

    rows = stiffness_matrix.shape[0]
    cols = len(frequencies)
    x = np.zeros((rows, cols), dtype=complex)

    for i, frequency in enumerate(frequencies):
        A = complex(1, frequency*beta_v + beta_h)*stiffness_matrix + complex(-(2*np.pi*frequency)**2, frequency*alpha_v + alpha_h)*mass_matrix
        x[:,i] = spsolve(A, forces)
    return x
 
def modal_superposition(forces, frequencies, natural_frequencies, modal_shape, **kwargs):
    alpha_v = kwargs.get('alpha_v', 0)
    beta_v = kwargs.get('beta_v', 0)
    alpha_h = kwargs.get('alpha_h', 0)
    beta_h = kwargs.get('beta_h', 0)

    shape = (modal_shape.shape[0], len(frequencies))
    x = np.zeros(shape, dtype=complex)

    F_aux = modal_shape.T @ forces.flatten()
    for i, frequency in enumerate(frequencies):        
        data = np.divide(1, (complex(1, beta_v*frequency + beta_h) * (2*np.pi*natural_frequencies)**2 + complex(-(2*np.pi*frequency)**2, frequency*alpha_v + alpha_h)))
        diag = np.diag(data)
        x[:,i] = modal_shape @ (diag @ F_aux)
    return x

######
# TODO: EVERYTHING IS A COMPLETE MESS, SOLVE IT AS SOON AS POSSIBLE

def new_direct_method(mesh, frequencies, dumping, **kwargs):
    K, M, Kr, Mr = get_global_matrices(mesh)
    F = get_global_forces(mesh)
    F_add = get_equivalent_forces(mesh, frequencies, Kr, Mr, dumping)

    rows = K.shape[0]
    cols = len(frequencies)
    solution = np.zeros((rows, cols), dtype=complex)
    alpha_h, beta_h, alpha_v, beta_v = dumping
    F_aux = F.reshape(-1, 1) - F_add

    for i, frequency in enumerate(frequencies):
        K_damp = K * complex(1, frequency*beta_v + beta_h)
        M_damp = M * complex(-(2*np.pi*frequency)**2, frequency*alpha_v + alpha_h)
        A = K_damp + M_damp
        solution[:,i] = spsolve(A, F_aux[:,i])

    prescribed_indexes = mesh.get_prescribed_indexes()
    prescribed_values = mesh.get_prescribed_values()
    solution = reinsert_prescribed_dofs(solution, prescribed_indexes, prescribed_values)

    return solution


def get_equivalent_forces(mesh, frequencies, Kr, Mr, dumping):   
    unprescribed_indexes = mesh.get_unprescribed_indexes()
    prescribed_values = mesh.get_prescribed_values()

    Kr = Kr.toarray()
    Mr = Mr.toarray()
    Kr = Kr[unprescribed_indexes, :]
    Mr = Mr[unprescribed_indexes, :]

    if Kr == [] or Mr == []:
        print('ENTREI AQUi')
        Kr_add = [0]
        Mr_add = [0]
    else:
        Kr_add = np.sum(Kr*prescribed_values, axis=1)
        Mr_add = np.sum(Mr*prescribed_values, axis=1)

    rows = len(Kr_add)
    cols = len(frequencies)
    F_add = np.zeros((rows,cols), dtype=complex)
    alpha_h, beta_h, alpha_v, beta_v = dumping

    for i, frequency in enumerate(frequencies):
        F_K_add = Kr_add * complex(1,frequency*beta_v + beta_h)
        F_M_add = Mr_add * complex(-(2*np.pi*frequency)**2, -frequency*alpha_v - alpha_h)
        F_add[:, i] = F_K_add + F_M_add

    return F_add

def reinsert_prescribed_dofs(solution, prescribed_indexes, prescribed_values):
    rows = solution.shape[0] + len(prescribed_indexes)
    cols = solution.shape[1]
    full_solution = np.zeros((rows, cols), dtype=complex)

    unprescribed_indexes = np.delete(np.arange(rows), prescribed_indexes)
    full_solution[unprescribed_indexes, :] = solution

    for i in range(cols):
        full_solution[prescribed_indexes, i] = prescribed_values 

    return full_solution
