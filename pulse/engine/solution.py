import numpy as np
from math import pi
import time
from scipy.sparse.linalg import eigs, eigsh, spsolve, lobpcg

class Solution:

    def __init__(self, stiffness_matrix, mass_matrix, **kwargs):
        self.stiffness_matrix = stiffness_matrix.tocsc()
        self.mass_matrix = mass_matrix.tocsc()

        self.Kr = kwargs.get("Kr", None)
        self.Mr = kwargs.get("Mr", None)
        self.presc_dofs_info = kwargs.get("presc_dofs_info", None)
        self.free_dofs = kwargs.get("free_dofs", None)
        
        self.frequencies = kwargs.get("frequencies", None)
        self.minor_freq = kwargs.get("minor_freq", None)
        self.major_freq = kwargs.get("major_freq", None)
        self.df = kwargs.get("df", None)
        self.number_points = kwargs.get("number_points", None)
        self.alpha_v = kwargs.get("alpha_v", None)
        self.beta_v = kwargs.get("beta_v", None)
        self.alpha_h = kwargs.get("alpha_h", None)
        self.beta_h = kwargs.get("beta_h", None)      

    def modal_analysis(self, number_modes = 10, which = 'LM', sigma = 0.01, timing = False ):
        """ Perform a modal analysis and returns natural frequencies and modal shapes normalized 
            with respect to generalized mass coordinates.
        """
  
        start = time.time()  
        eigen_values, eigen_vectors = eigs( self.stiffness_matrix,
                                            k = number_modes,
                                            M = self.mass_matrix,
                                            which = which,
                                            sigma = sigma)


        end = time.time()
        if timing:
            print('Time to perform modal analysis :' + str(round((end - start),6)) + '[s]')
        
        natural_frequencies = np.sqrt( np.absolute( np.real(eigen_values) ) ) /(2 * pi)
        ind_ord = np.argsort(  natural_frequencies )
        natural_frequencies = natural_frequencies[ ind_ord ]
        modal_shape = np.real( eigen_vectors[ :, ind_ord ] )
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
        """ 
            Perform an harmonic analysis through direct method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        
        if self.alpha_v == None: 
            self.alpha_v = 0
        if self.beta_v == None:
            self.beta_v = 0

        if self.alpha_h == None: 
            self.alpha_h = 0
        if self.beta_h == None:
            self.beta_h = 0

        if self.Kr == None or self.Mr == None:
            Kr_v, Mr_v = 0, 0
        else:

            Kr = (self.Kr.toarray())[ :, self.free_dofs ]
            Mr = (self.Mr.toarray())[ :, self.free_dofs ]

            Kr_temp = np.zeros(( Kr.shape[1], Kr.shape[0] ))
            Mr_temp = np.zeros(( Mr.shape[1], Mr.shape[0] ))

            for ind, value in enumerate(self.presc_dofs_info[:,2]):
                
                Kr_temp[ :, ind ] = value*Kr[ ind, : ]
                Mr_temp[ :, ind ] = value*Mr[ ind, : ]
            
            Kr_v = np.sum( Kr_temp, axis=1 )
            Mr_v = np.sum( Mr_temp, axis=1 )
        
        M = self.mass_matrix
        K = self.stiffness_matrix

        frequencies = self.freq_vector()
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ], dtype=complex )
        
        start = time.time()
        for i, freq in enumerate(frequencies):

            F_add = (1 + 1j*freq*self.beta_v + 1j*self.beta_h)*Kr_v - ( ((2 * pi * freq)**2) - 1j*freq*self.alpha_v - 1j*self.alpha_h)*Mr_v
            
            K_damp = ( 1 + 1j*freq*self.beta_v + 1j*self.beta_h )*K
            M_damp = ( -((2 * pi * freq)**2) + 1j*freq*self.alpha_v + 1j*self.alpha_h)*M
            
            A = K_damp + M_damp
            x[:,i] = spsolve(A, F - F_add)
        
        if timing:
            end = time.time()
            print('Time to solve harmonic analisys problem through direct method:' + str(round((end - start),6)) + '[s]')

        return x, frequencies

    def mode_superposition(self, F, number_modes = 10, which = 'LM', sigma = 0.01, timing = False, **kwargs):
        """ 
            Perform an harmonic analysis through superposition method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        
        if self.alpha_v == None: 
            self.alpha_v = 0
        elif self.beta_v == None:
            self.beta_v = 0

        if self.alpha_h == None: 
            self.alpha_h = 0
        elif self.beta_h == None:
            self.beta_h = 0

        if self.Kr == None or self.Mr == None:
            Kr_v, Mr_v = 0, 0
        else:

            Kr = (self.Kr.toarray())[ :, self.free_dofs ]
            Mr = (self.Mr.toarray())[ :, self.free_dofs ]

            Kr_temp = np.zeros(( Kr.shape[1], Kr.shape[0] ))
            Mr_temp = np.zeros(( Mr.shape[1], Mr.shape[0] ))

            for ind, value in enumerate(self.presc_dofs_info[:,2]):
                
                Kr_temp[ :, ind ] = value*Kr[ ind, : ]
                Mr_temp[ :, ind ] = value*Mr[ ind, : ]
            
            Kr_v = np.sum( Kr_temp, axis=1 )
            Mr_v = np.sum( Mr_temp, axis=1 )

        frequencies = self.freq_vector()
        x = np.zeros([ self.stiffness_matrix.shape[0], len(frequencies) ], dtype=complex)

        modal_shape = kwargs.get("modal_shape", None)
        natural_frequencies = kwargs.get("natural_frequencies", None)

        start = time.time()
        if np.array(modal_shape).all() == None or modal_shape.shape[1] != number_modes:
            natural_frequencies, modal_shape = self.modal_analysis( number_modes = number_modes, which = 'LM', sigma = sigma )            

        #F_aux = modal_shape.T @ F

        for i, freq in enumerate(frequencies):

            Kg_damp = (1 + 1j*self.beta_v*freq + 1j*self.beta_h)*((2 * pi * natural_frequencies)**2)
            Mg_damp = (1j*freq*self.alpha_v + 1j*self.alpha_h) - ((2 * pi * freq)**2)

            data = np.divide(1, (Kg_damp + Mg_damp))
            diag = np.diag(data)

            F_add = (1 + 1j*freq*self.beta_v + 1j*self.beta_h)*Kr_v - ( ((2 * pi * freq)**2) - 1j*freq*self.alpha_v - 1j*self.alpha_h)*Mr_v
            F_aux = modal_shape.T @ (F - F_add)

            x[:,i] = modal_shape @ (diag @ F_aux)
            
        end = time.time()
        if timing:
            print('Time to solve harmonic analisys problem through mode superposition method:' + str(round((end - start),6)) + '[s]')

        return x, frequencies, natural_frequencies, modal_shape
