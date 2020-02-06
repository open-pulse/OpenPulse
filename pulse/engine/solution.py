import numpy as np
from math import pi
import time

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
        

    def modal_analysis(self, number_modes = 10, which = 'LM', sigma = 0.01, timing = False ):
  
        start = time.time()  
        eigen_values, eigen_vectors = eigs( self.stiffness_matrix,
                                            k = number_modes,
                                            M = self.mass_matrix,
                                            which = which,
                                            sigma = sigma)

        end = time.time()
        if timing:
            print('Time to perform modal analysis :' + str(round((end - start),6)) + '[s]')
        
        modal_shape = np.real( eigen_vectors )
        natural_frequencies = np.sqrt( np.absolute( np.real(eigen_values) ) ) /(2 * pi)

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
    

    def direct_method(self, F, timing = False):

        frequencies = self.freq_vector()
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ])
        
        start = time.time()
        for i in range(len(frequencies)):
            freq = frequencies[i]
            A = self.stiffness_matrix - (2 * pi * freq)**2 * self.mass_matrix
            x[:,i] = spsolve(A, F)
        
        if timing:
            end = time.time()
            print('Time to solve harmonic analisys problem through direct method:' + str(round((end - start),6)) + '[s]')

        return x, frequencies

    def mode_superposition(self, F, number_modes = 10, which = 'LM', sigma = 0.01, timing = False, **kwargs):
        
        frequencies = self.freq_vector()
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ])

        modal_shape = kwargs.get("modal_shape", None)
        natural_frequencies = kwargs.get("natural_frequencies", None)
        
        start = time.time()
        if np.array(modal_shape).all() == None or modal_shape.shape[1] != number_modes:
            natural_frequencies, modal_shape = self.modal_analysis( number_modes = number_modes, which = 'LM', sigma = sigma )            

        F_aux = modal_shape.T @ F
        for i in range(len(frequencies)):
            freq = frequencies[i]
            aux = np.diag( np.divide(1, (2 * pi * natural_frequencies)**2 - (2 * pi * freq)**2 ) )
            x[:,i] = modal_shape @ aux @ F_aux
        
        end = time.time()
        if timing:
            print('Time to solve harmonic analisys problem through mode superposition method:' + str(round((end - start),6)) + '[s]')


        return x, frequencies, natural_frequencies, modal_shape
