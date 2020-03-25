from time import time

import numpy as np
from scipy.sparse.linalg import eigs, spsolve


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