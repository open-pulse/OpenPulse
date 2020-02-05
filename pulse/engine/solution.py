import numpy as np
from math import pi

from scipy.sparse.linalg import eigs, eigsh, spsolve

class Solution:

    def __init__(self, stiffness_matrix, mass_matrix, **kwargs):
        self.stiffness_matrix = stiffness_matrix.tocsr()
        self.mass_matrix = mass_matrix.tocsr()

        self.frequencies = kwargs.get("frequencies", None)
        self.minor_freq = kwargs.get("minor_freq", None)
        self.major_freq = kwargs.get("major_freq", None)
        self.df = kwargs.get("df", None)
        self.number_points = kwargs.get("number_points", None)
        

    def modal_analysis(self, number_modes = 10, which = 'LM', sigma = 0.01 ):

        K = self.stiffness_matrix
        M = self.mass_matrix
  
        eigen_values, eigen_vectors = eigs( K,
                                            k = number_modes,
                                            M = M,
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
    

    def freq_vector(self):

        if np.array(self.frequencies).all() == None or self.frequencies==[] :

            if self.minor_freq == None:
                self.minor_freq = float(input('Enter a value to a minor frequency of analysis: '))
            if self.major_freq == None:
                self.major_freq = float(input('Enter a value to a major frequency of analysis: '))
            if self.df == None and self.number_points == None:
                self.df = float(input('Enter a value to frequency resolution: '))
            if self.df == None and self.number_points != None:
                self.df = (self.major_freq - self.minor_freq)/(self.number_points - 1)

            self.frequencies = np.arange(self.minor_freq, self.major_freq + self.df, self.df)

        return self.frequencies
    

    def direct_method(self, F):

        frequencies = self.freq_vector()
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ])

        for i in range(len(frequencies)):
            freq = frequencies[i]
            A = self.stiffness_matrix - (2 * pi * freq)**2 * self.mass_matrix
            x[:,i] = spsolve(A, F)
        
        return x, frequencies

    def mode_superposition(self, F, number_modes = 10, which = 'LM', sigma = 0.01):

        frequencies = self.freq_vector()
                
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ])

        natural_frequencies, modal_shape = self.modal_analysis( number_modes = number_modes, which = 'LM', sigma = sigma )

        for i in range(len(frequencies)):
            freq = frequencies[i]
            aux = np.diag( np.divide(1, (2 * pi * natural_frequencies)**2 - (2 * pi * freq)**2 ) )
            x[:,i] = modal_shape @ aux @ modal_shape.T @ F

        return x, frequencies, natural_frequencies, modal_shape
