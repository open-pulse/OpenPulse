import numpy as np
from math import pi

from pulse.engine.node import Node

class PostProcessing:

    def __init__(self, assemble, **kwargs):

        _, _, _, self.Kr, self.Mr = assemble.rows_columns_drops(timing=False)
        
        self.global_dofs_free, self.global_dofs_prescribed, self.prescribed_dofs_values = assemble.solution_dofs_info()
        self.number_nodes = int((len(self.global_dofs_free) + len(self.global_dofs_prescribed))/Node.degree_freedom)
        self.number_dofs = int(len(self.global_dofs_free) + len(self.global_dofs_prescribed))
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.HA_output = kwargs.get("HA_output", None)
        self.frequencies = kwargs.get("frequencies", None)
        self.free_dofs = kwargs.get("free_dofs", None)
        self.damping = kwargs.get("damping", [0,0,0,0])

    def get_Uxyz_Rxyz(self, data, dtype):
        """ This method returns: 
            Uxyz = [ Ux[:,0+n], Uy[:,0+n], Uz[:,0+n] ]
            Rxyz = [ Rx[:,0+n], Ry[:,0+n], Rz[:,0+n] ].
        """
        ind = np.arange( 0, data.shape[0], Node.degree_freedom )
        Uxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*data.shape[1]) ), dtype=dtype)
        Rxyz = np.zeros(( self.number_nodes, int(1 + (Node.degree_freedom/2)*data.shape[1]) ), dtype=dtype)
        Uxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )
        Rxyz[:,0] = np.arange( 0, self.number_nodes + 0, 1 )

        for j in range( data.shape[1] ):
                
            Uxyz[:, 1+3*j], Uxyz[:, 2+3*j], Uxyz[:, 3+3*j] = data[ind+0, j], data[ind+1, j], data[ind+2, j]
            Rxyz[:, 1+3*j], Rxyz[:, 2+3*j], Rxyz[:, 3+3*j] = data[ind+3, j], data[ind+4, j], data[ind+5, j]
    
        return Uxyz, Rxyz

    def modal_response(self):
        """ This method returns eigenVectors with all prescribed dofs values recovered."""
        aux_eigenVectors = self.eigenVectors.copy()
        if not self.global_dofs_prescribed == []:
            global_dofs = np.array(self.global_dofs_prescribed, dtype=int)
            
            for row in global_dofs:
                aux_eigenVectors = np.insert( aux_eigenVectors, row, [0], axis=0 )

        return aux_eigenVectors

    def plot_modal_shape(self, mode):
        '''This method returns modal shape to plot.'''
        data = self.modal_response()
        eigenUxyz, _ = self.get_Uxyz_Rxyz(data, dtype=float)
    
        Uxyz_mode = np.zeros((self.number_nodes, 4))
        Uxyz_mode[:,0] = eigenUxyz[:,0]
        Uxyz_mode[:,1:4] = eigenUxyz[:,(1+3*(mode-1)):(4+3*(mode-1))]

        return Uxyz_mode
    
    def harmonic_response (self, data):
        """ This method returns U_out with all prescribed dofs values recovered."""

        if not data == []:
            U_out = data
            if not self.global_dofs_prescribed == []:
                global_dofs = np.array(self.global_dofs_prescribed, dtype=int)
                value = self.prescribed_dofs_values

            for i, gdof in enumerate(global_dofs):
                    U_out = np.insert( U_out, gdof, value[i], axis=0 )
        else:
            U_out = []
            print("Please, it's necessary to solve an Harmonic Analysis if you intend recover information about prescribed dofs.")

        return U_out

    def plot_harmonic_response(self, column, data):
        '''This method returns harmonic response to plot.'''
        U = self.harmonic_response(data)
        HR_Uxyz, _ = self.get_Uxyz_Rxyz(U, dtype=complex)

        HR_f = np.zeros((self.number_nodes, 4), dtype=float)
        HR_f[:,0] = np.real(HR_Uxyz[:,0])
        HR_f[:,1:4] = np.real(HR_Uxyz[:,(1+3*(column-1)):(4+3*(column-1))])

        return HR_f

    def load_reactions(self, data):
        '''This method returns reaction forces at fixed points.'''

        alpha_h, beta_h, alpha_v, beta_v = self.damping
        U = self.harmonic_response(data)

        if not U==[]:    

            if self.Kr == [] or self.Mr == []:

                Kr_U, Mr_U = 0, 0

            else:
    
                Kr = (self.Kr.toarray())
                Mr = (self.Mr.toarray())

                rows = U.shape[1]
                cols = Kr.shape[1] 
                            
                Kr_U    = np.zeros( (rows, cols), dtype = complex )
                Mr_U    = np.zeros( (rows, cols), dtype = complex )
                F_react = np.zeros( (rows, cols+1), dtype = complex )
                F_react[:,0] = self.frequencies
                U_t = U.T

                for ind in range(cols):

                    Kr_U[ :, ind ] = U_t @ Kr[ :, ind ]
                    Mr_U[ :, ind ] = U_t @ Mr[ :, ind ]
            
            for k in range(cols):
                for ind, freq in enumerate(self.frequencies):

                    omega = 2*pi*freq

                    F_Kdamp = (1 + 1j*( beta_h + omega*beta_v ))*Kr_U[ind,k]
                    F_Mdamp = ( -(omega**2) + 1j*( alpha_h + omega*alpha_v ))*Mr_U[ind,k]
                    F_react[ind,k+1] = F_Kdamp +  F_Mdamp

        else:
            F_react = []
        return F_react        