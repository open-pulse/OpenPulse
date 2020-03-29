from time import time

import numpy as np
from scipy.sparse.linalg import eigs, spsolve

from pulse.utils import timer
from pulse.processing.assembly import new_get_global_matrices, get_global_forces


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

    shape = (stiffness_matrix.shape[0], len(frequencies))
    x = np.zeros(shape, dtype=complex)

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

# TODO: this code seens terible, solve it as soon as possible 

def new_direct_method(mesh, frequencies, **kwargs):
    alpha_v = kwargs.get('alpha_v', 0)
    beta_v = kwargs.get('beta_v', 0)
    alpha_h = kwargs.get('alpha_h', 0)
    beta_h = kwargs.get('beta_h', 0)

    # get matrices
    K, M = new_get_global_matrices(mesh)
    F = get_global_forces(mesh)
    F_add = get_equivalent_forces(mesh, frequencies, stiffness=K, mass=M, **kwargs)
 
    # get dofs
    all_dofs = np.arange(K.shape[0])
    prescribed_dofs_index = mesh.get_prescribed_dofs_index()
    free_dofs_index = np.delete(all_dofs, prescribed_dofs_index)

    # slice matrices
    K_free = K[free_dofs_index, :][:, free_dofs_index]
    M_free = M[free_dofs_index, :][:, free_dofs_index]
    F = F.reshape(-1, 1)
                           
    # create x
    shape = (K_free.shape[0], len(frequencies))
    x = np.zeros(shape, dtype=complex)
    # calculate x
    F_aux = F - F_add
    for i, frequency in enumerate(frequencies):
        K_damp = complex(1, frequency*beta_v + beta_h)*K_free
        M_damp = complex(-(2*np.pi*frequency)**2, frequency*alpha_v + alpha_h)*M_free
        A = K_damp + M_damp
        x[:,i] = spsolve(A, F_aux[:, i])
    return x

def get_equivalent_forces(mesh, frequencies, stiffness, mass, **kwargs):
    alpha_v = kwargs.get('alpha_v', 0)
    beta_v = kwargs.get('beta_v', 0)
    alpha_h = kwargs.get('alpha_h', 0)
    beta_h = kwargs.get('beta_h', 0)    

    # get dofs
    all_dofs = np.arange(stiffness.shape[0])
    prescribed_dofs_index = mesh.get_prescribed_dofs_index()
    prescribed_dofs_values = mesh.get_prescribed_dofs_values()
    free_dofs_index = np.delete(all_dofs, prescribed_dofs_index)

    Kr = stiffness[free_dofs_index, :][:, prescribed_dofs_index]
    Mr = mass[free_dofs_index, :][:, prescribed_dofs_index]
    Kr = Kr.toarray()
    Mr = Mr.toarray()

    if Kr == [] or Mr == []:
        Kr_add = [0]
        Mr_add = [0]
    else:
        Kr_temp = np.zeros(Kr.shape)
        Mr_temp = np.zeros(Mr.shape)

        for ind, value in enumerate(prescribed_dofs_values):
            Kr_temp[:, ind] = value*Kr[:, ind]
            Mr_temp[:, ind] = value*Mr[:, ind]

        Kr_add = np.sum(Kr_temp, axis=1)
        Mr_add = np.sum(Mr_temp, axis=1)

    rows = len(Kr_add)
    cols = len(frequencies)
    
    F_add = np.zeros((rows,cols), dtype=complex)   
    for i, freq in enumerate(frequencies):
        F_Kadd = (1 + 1j*freq*beta_v + 1j*beta_h)*Kr_add 
        F_Madd = (- ( ((2 * np.pi * freq)**2) - 1j*freq*alpha_v - 1j*alpha_h))*Mr_add
        F_add[:, i] = F_Kadd + F_Madd
    return F_add