import numpy as np
from math import pi

from pulse.engine.assembly import Assembly
from pulse.engine.node import Node

class PostProcessing:

    def __init__(self, preprocessor, **kwargs):
        
        self.prescbribed_dofs_info = preprocessor.prescbribed_dofs_info()
        self.number_nodes = preprocessor.number_nodes()
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.HA_output = kwargs.get("HA_output", None)
        self.frequencies = kwargs.get("frequencies", None)
        self.Kr = kwargs.get("Kr", None)
        self.Mr = kwargs.get("Mr", None)
        self.free_dofs = kwargs.get("free_dofs", None)
        self.alpha_v = kwargs.get("alpha_v", None)
        self.beta_v = kwargs.get("beta_v", None)
        self.alpha_h = kwargs.get("alpha_h", None)
        self.beta_h = kwargs.get("beta_h", None)    
        self.log = kwargs.get("log", None)

    def dof_recover(self):
        """ 
        This method returns eigenVectors with all prescribed dofs values recovered.
        
        """
        aux_eigenVectors = self.eigenVectors.copy()
        if self.prescbribed_dofs_info.any():
            global_dofs = np.array(self.prescbribed_dofs_info[:,0], dtype='int32')
            
            for row in global_dofs:
                aux_eigenVectors = np.insert( aux_eigenVectors, row, [0], axis=0 )
            
        if self.log:
            print('Dofs before recovering:',self.eigenVectors.shape[0])
            print('Dofs after recovering:',aux_eigenVectors.shape[0])

        eigenVectors_Uxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*aux_eigenVectors.shape[1]) ))
        eigenVectors_Rxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*aux_eigenVectors.shape[1]) ))
        eigenVectors_Uxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )
        eigenVectors_Rxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )

        ind = np.arange( 0, aux_eigenVectors.shape[0], Node.degree_freedom )

        for j in range( self.eigenVectors.shape[1] ):
                
            eigenVectors_Uxyz[ :, 1+3*j ] = aux_eigenVectors[ ind+0, j ]
            eigenVectors_Uxyz[ :, 2+3*j ] = aux_eigenVectors[ ind+1, j ]
            eigenVectors_Uxyz[ :, 3+3*j ] = aux_eigenVectors[ ind+2, j ]
            
            eigenVectors_Rxyz[ :, 1+3*j ] = aux_eigenVectors[ ind+3, j ]
            eigenVectors_Rxyz[ :, 2+3*j ] = aux_eigenVectors[ ind+4, j ]
            eigenVectors_Rxyz[ :, 3+3*j ] = aux_eigenVectors[ ind+5, j ]
    
        return eigenVectors_Uxyz, eigenVectors_Rxyz
    
    def harmonic_response (self, data):
        '''This method returns final dofs response U_out considering the loads and the prescribed dofs values.'''

        if data.any():
            U_out = data
            if self.prescbribed_dofs_info.any():
                global_dofs = np.array(self.prescbribed_dofs_info[:,0], dtype=int)
                value = self.prescbribed_dofs_info[:,2]

            for i, gdof in enumerate(global_dofs):
                    U_out = np.insert( U_out, gdof, value[i], axis=0 )
        else:
            U_out = []
            print("Please, it's necessary to solve an Harmonic Analysis if you intend recover information about prescribed dofs.")
        
        return U_out

    def plot_modal_shape(self, mode):
        
        eigen_Uxyz_plot = []
        eigen_Uxyz, _ = self.dof_recover()
        eigen_Uxyz_plot.append(eigen_Uxyz)
        eigen_Uxyz_plot = np.asarray(eigen_Uxyz_plot[0])
        Uxyz_mode = np.zeros((eigen_Uxyz_plot.shape[0], 4))
        Uxyz_mode[:,0] = eigen_Uxyz_plot[:,0]
        Uxyz_mode[:,1:4] = eigen_Uxyz_plot[:,(1+3*(mode-1)):(4+3*(mode-1))]

        return Uxyz_mode

    def plot_harmonic_response(self, freq, data):
        
        HR_Uxyz_plot = []
        Uout = self.harmonic_response(data)

        ind = np.arange( 0, Uout.shape[0], Node.degree_freedom )

        HR_Uxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*Uout.shape[1]) ), dtype=complex)
        HR_Rxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*Uout.shape[1]) ), dtype=complex)
        HR_Uxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )
        HR_Rxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )

        for j in range( Uout.shape[1] ):
                
            HR_Uxyz[ :, 1+3*j ] = Uout[ ind+0, j ]
            HR_Uxyz[ :, 2+3*j ] = Uout[ ind+1, j ]
            HR_Uxyz[ :, 3+3*j ] = Uout[ ind+2, j ]
            
            HR_Rxyz[ :, 1+3*j ] = Uout[ ind+3, j ]
            HR_Rxyz[ :, 2+3*j ] = Uout[ ind+4, j ]
            HR_Rxyz[ :, 3+3*j ] = Uout[ ind+5, j ]

        HR_Uxyz_plot.append(HR_Uxyz)
        HR_Uxyz_plot = np.asarray(HR_Uxyz_plot[0])
        HR_f = np.zeros((HR_Uxyz_plot.shape[0], 4), dtype=float)
        HR_f[:,0] = np.real(HR_Uxyz_plot[:,0])
        HR_f[:,1:4] = np.real(HR_Uxyz_plot[:,(1+3*(freq-1)):(4+3*(freq-1))])

        return HR_f

    def load_reactions(self, data):

        if self.alpha_v == None: 
            self.alpha_v = 0
        if self.beta_v == None:
            self.beta_v = 0

        if self.alpha_h == None: 
            self.alpha_h = 0
        if self.beta_h == None:
            self.beta_h = 0

        U = self.harmonic_response(data)

        if self.Kr == None or self.Mr == None:

            Kr_U, Mr_U = 0, 0

        else:
   
            Kr = (self.Kr.toarray())
            Mr = (self.Mr.toarray())

            Kr_U = np.zeros( (U.shape[1], Kr.shape[0]), dtype = complex )
            Mr_U = np.zeros( (U.shape[1], Mr.shape[0]), dtype = complex )
            F_react = np.zeros( (U.shape[1], Mr.shape[0]), dtype = complex )
            U_t = U.T

            for ind in range(Kr.shape[0]):

                Kr_U[ :, ind ] = U_t @ Kr[ ind, : ]
                Mr_U[ :, ind ] = U_t @ Mr[ ind, : ]
        
        for k in range(Kr.shape[0]):
            for ind, freq in enumerate(self.frequencies):

                F_Kdamp = (1 + 1j*freq*self.beta_v + 1j*self.beta_h)*Kr_U[ind,k]
                F_Mdamp = ( ((2 * pi * freq)**2) - 1j*freq*self.alpha_v - 1j*self.alpha_h)*Mr_U[ind,k]
                F_react[ind,k] = F_Kdamp -  F_Mdamp

        return F_react        