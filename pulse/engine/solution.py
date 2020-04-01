import numpy as np
from math import pi
from time import time
from scipy.sparse.linalg import eigs, eigsh, spsolve, lobpcg

class Solution:

    def __init__(self, assemble, **kwargs):
        
        self.K, self.M, self.F, self.Kr, self.Mr = assemble.rows_columns_drops(timing=True)
        self.global_dofs_free, self.global_dofs_prescribed, self.global_dofs_values = assemble.solution_dofs_info()
        self.K_lump, self.M_lump, self.C_lump, self.Kr_lump, self.Mr_lump, self.Cr_lump, self.flagK, self.flagM, self.flagC = assemble.rows_columns_drops_lumped()
        self.Kadd_lump, self.Madd_lump = assemble.add_lumped_matrices()
        self.external_elements = assemble.is_there_lumped_info()
        
        self.frequencies = kwargs.get("frequencies", None)
        self.minor_freq = kwargs.get("minor_freq", None)
        self.major_freq = kwargs.get("major_freq", None)
        self.df = kwargs.get("df", None)
        self.number_points = kwargs.get("number_points", None)

        self.damping = kwargs.get("damping", [0,0,0,0]) # entries => [alpha_h, beta_h, alpha_v, beta_v]
        self.lump_damping = kwargs.get("lumped_damping", [0,0,0,0]) # entries => [alpha_h_lump, beta_h_lump, alpha_v_lump, beta_v_lump]

    def modal_analysis(self, number_modes = 10, which = 'LM', sigma = 0.01, timing = False ):
        """ Perform a modal analysis and returns the natural frequencies and the respective modal shapes 
            normalized with respect to generalized mass coordinates..
        """
        start = time()  
        eigen_values, eigen_vectors = eigs( self.Kadd_lump,
                                            k = number_modes,
                                            M = self.Madd_lump,
                                            which = which,
                                            sigma = sigma)

        end = time()
        if timing:
            print('Time to perform modal analysis :' + str(round((end - start),6)) + '[s]')
        
        natural_frequencies = np.sqrt( np.absolute( np.real(eigen_values) ) ) /(2 * pi)
        ind_ord = np.argsort(  natural_frequencies )
        natural_frequencies = natural_frequencies[ ind_ord ]
        modal_shape = np.real( eigen_vectors[ :, ind_ord ] )

        return natural_frequencies, modal_shape
    
    def freq_vector(self):

        if np.array(self.frequencies).all() == None:
        
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
    
    def F_add(self, viscous_damping_lumped = False, proportional_damping = True):
        """ This method calculates the equivalent load resultant of the prescription 
            of degrees of freedom.
        """

        if viscous_damping_lumped:
            proportional_damping = False

        Kr = self.Kr
        Mr = self.Mr
        frequencies = self.freq_vector()  
        alphaH, betaH, alphaV, betaV = self.damping
        alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = self.lump_damping

        if self.flagK:
            Kr_lump = self.Kr_lump.toarray()
            Kr_lump = Kr_lump[ self.global_dofs_free, : ]
            Kr_lump_temp = np.zeros(Kr_lump.shape)

        if self.flagM:
            Mr_lump = self.Mr_lump.toarray()
            Mr_lump = Mr_lump[ self.global_dofs_free, : ]
            Mr_lump_temp = np.zeros(Mr_lump.shape)

        if self.flagC:
            Cr_lump = self.Cr_lump.toarray()
            Cr_lump = Cr_lump[ self.global_dofs_free, : ]
            Cr_lump_temp = np.zeros(Cr_lump.shape)

        if Kr == [] or Mr == []:

            Kr_add, Mr_add = 0, 0

        else:

            Kr = (self.Kr.toarray())[ self.global_dofs_free, : ]
            Mr = (self.Mr.toarray())[ self.global_dofs_free, : ]
            Kr_temp = np.zeros(Kr.shape)
            Mr_temp = np.zeros(Mr.shape)
            
            for ind, value in enumerate(self.global_dofs_values):
                
                Kr_temp[ :, ind ] = value*Kr[ :, ind ]
                Mr_temp[ :, ind ] = value*Mr[ :, ind ]

                if self.flagK:
                    Kr_lump_temp[ :, ind ] = value*Kr_lump[ :, ind ]
                if self.flagM:
                    Mr_lump_temp[ :, ind ] = value*Mr_lump[ :, ind ]
                if self.flagC:
                    Cr_lump_temp[ :, ind ] = value*Cr_lump[ :, ind ]
            
            Kr_add = np.sum( Kr_temp, axis=1 )
            Mr_add = np.sum( Mr_temp, axis=1 )

            if self.flagK:
                Kr_add_lump = np.sum( Kr_lump_temp, axis=1 )
            else:
                Kr_add_lump = 0

            if self.flagM:
                Mr_add_lump = np.sum( Mr_lump_temp, axis=1 )
            else:
                Mr_add_lump = 0

            if self.flagC:
                Cr_add_lump = np.sum( Cr_lump_temp, axis=1 )
            else:
                Cr_add_lump = 0
        
        rows = len(Kr_add) 
        columns = len(frequencies)

        F_add = np.zeros([ rows , columns ], dtype=complex)

        for i, freq in enumerate(frequencies):

            omega = 2*pi*freq

            F_Kadd = Kr_add + Kr_add_lump
            F_Madd = (-(omega**2))*(Mr_add + Mr_add_lump) 
            F_Cadd = 1j*((betaH + omega*betaV)*Kr_add + (alphaH + omega*alphaV)*Mr_add)

            if proportional_damping:
                F_Cadd_lump = 1j*((betaH_lump + omega*betaV_lump)*Kr_add_lump + (alphaH_lump + omega*alphaV_lump)*Mr_add_lump)
            else:
                F_Cadd_lump = 1j*omega*Cr_add_lump

            F_add[:, i] = F_Kadd + F_Madd + F_Cadd + F_Cadd_lump

        return F_add

    def direct_method(self, timing = False, viscous_damping_lumped=False, proportional_damping_lumped=True):
        """ 
            Perform an harmonic analysis through direct method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """
        if viscous_damping_lumped:
            proportional_damping_lumped = False
        
        alphaH, betaH, alphaV, betaV = self.damping
        alphaH_lump, betaH_lump, alphaV_lump, betaV_lump = self.lump_damping

        K = self.K
        M = self.M        
        K_sum = self.Kadd_lump
        M_sum = self.Madd_lump

        K_lump = self.K_lump
        M_lump = self.M_lump
        C_lump = self.C_lump

        F = self.F.reshape(len(self.global_dofs_free),1)
        F_add = self.F_add(viscous_damping_lumped=viscous_damping_lumped)
        frequencies = self.freq_vector()
        x = np.zeros([ self.K.shape[0], len(frequencies) ], dtype=complex )
        
        start = time()
        
        F_aux = F - F_add
        
        for i, freq in enumerate(frequencies):

            omega = 2*pi*freq
            
            F_K = K_sum
            F_M =  (-(omega**2))*M_sum
            F_C = 1j*(( betaH + omega*betaV )*K + ( alphaH + omega*alphaV )*M)

            if viscous_damping_lumped:
                F_Clump = 1j*omega*C_lump
            
            if proportional_damping_lumped:
                F_Clump = 1j*(( betaH_lump + omega*betaV_lump )*K_lump + ( alphaH_lump + omega*alphaV_lump )*M_lump)

            A = F_K + F_M + F_C + F_Clump
            x[:,i] = spsolve(A, F_aux[:,i])
        
        if timing:
            end = time()
            print('Time to solve harmonic analisys problem through direct method:' + str(round((end - start),6)) + '[s]')

        return x, frequencies

    def mode_superposition(self, number_modes = 10, which = 'LM', sigma = 0.01, timing = False, **kwargs):
        """ 
            Perform an harmonic analysis through superposition method and returns the response of
            all nodes due the external or internal equivalent load. It has been implemented two
            different damping models: Viscous Proportional and Hysteretic Proportional
            Entries for Viscous Proportional Model Damping: (alpha_v, beta_v)
            Entries for Hyteretic Proportional Model Damping: (alpha_h, beta_h)
        """

        alphaH, betaH, alphaV, betaV = self.damping
        
        F = self.F.reshape(len(self.global_dofs_free),1)
        F_add = self.F_add()
        
        modal_shape = kwargs.get("modal_shape", None)
        natural_frequencies = kwargs.get("natural_frequencies", None)

        frequencies = self.freq_vector()
        x = np.zeros([ self.K.shape[0], len(frequencies) ], dtype=complex)

        start = time()
        if np.array(modal_shape).all() == None or modal_shape.shape[1] != number_modes:
            natural_frequencies, modal_shape = self.modal_analysis( number_modes = number_modes, which = 'LM', sigma = sigma )            

        F_aux = modal_shape.T @ (F - F_add)

        for i, freq in enumerate(frequencies):

            omega = 2*pi*freq
            omega_n = 2*pi*natural_frequencies

            F_kg = (omega_n**2)
            F_mg =  - (omega**2)
            F_cg = 1j*((betaH + betaV*omega)*(omega_n**2) + (alphaH + omega*alphaV)) 

            data = np.divide(1, (F_kg + F_mg + F_cg))
            diag = np.diag(data)

            x[:,i] = modal_shape @ (diag @ F_aux[:,i])
            
        end = time()

        if timing:
            print('Time to solve harmonic analisys problem through mode superposition method:' + str(round((end - start),6)) + '[s]')
        
        if self.external_elements:
            print("WARNING: There are external elements like lumped springs or masses in the model.\n         It's recommended to solve the harmonic analysis through direct method if you want to get more accurate results.")

        return x, frequencies, natural_frequencies, modal_shape
