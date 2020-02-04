import numpy as np
from math import pi

from scipy.sparse.linalg import eigs, eigsh, spsolve

class Solution:

    def __init__(self, stiffness_matrix, mass_matrix, **kwargs):
        self.stiffness_matrix = stiffness_matrix
        self.mass_matrix = mass_matrix

        self.frequencies = kwargs.get("frequencies", None)
    
    def modal_analysis(self, number_modes = 10, which = 'LM', sigma = 0 ):

        eigen_values, eigen_vectors = eigsh( self.stiffness_matrix,
                                            k = number_modes,
                                            M = self.mass_matrix,
                                            which = which,
                                            sigma = sigma)
        
        natural_frequencies = np.sqrt( np.absolute( np.real(eigen_values) ) ) /(2 * pi)
        modal_shape = np.real( eigen_vectors )

        # idx = natural_frequencies.argsort()[::1]
        # natural_frequencies= natural_frequencies[idx]
        # modal_shape = modal_shape[:,idx]

        # # Normalizing eigen vector
        # aux = np.abs( modal_shape.conj().T @ M @ modal_shape )
        # modal_shape = np.diag( np.divide(1, np.sqrt( aux.diagonal() ) ) ) @ modal_shape

        return natural_frequencies, modal_shape
    
    def direct(self, F):

        frequencies_sorted = np.sort( np.array( self.frequencies ) )
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies_sorted) ])

        for i in range(len(frequencies_sorted)):
            freq = frequencies_sorted[i]
            A = self.stiffness_matrix - (2 * pi * freq)**2 * self.mass_matrix
            x[:,i] = spsolve(A, F)
        
        return x, frequencies_sorted

    def modal(self, F, number_modes = 10, which = 'LM', sigma = 0):

        frequencies_sorted = np.sort( np.array( self.frequencies ) )
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies_sorted) ])

        natural_frequencies, modal_shape = self.modal_analysis( number_modes = number_modes, which = 'LM', sigma = 0 )

        for i in range(len(frequencies_sorted)):
            freq = frequencies_sorted[i]
            aux = np.diag( np.divide(1, (2 * pi * natural_frequencies)**2 - (2 * pi * freq)**2 ) )
            x[:,i] = modal_shape @ aux @ modal_shape.T @ F

        return x, frequencies_sorted, natural_frequencies, modal_shape
