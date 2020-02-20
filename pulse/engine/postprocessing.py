import numpy as np

from pulse.engine.assembly import Assembly
from pulse.engine.node import Node

class PostProcessing:

    def __init__(self, prescribed_info, nodal_coordinates, **kwargs):
        
        self.prescribed_info = prescribed_info
        self.nodal_coordinates = nodal_coordinates
        self.fn = kwargs.get("fn", None)
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.HA_output = kwargs.get("HA_output", None)
        self.log = kwargs.get("log", None)


    def dof_recover(self):
        """ 
        This method returns eigenVectors with all prescribed dofs values recovered.
        Similarly, it returns final dofs response U_out considering already prescribed dofs values.

        """
        if 
        global_dofs = np.array(self.prescribed_info[1][:,0], dtype='int32')
            
        aux_eigenVectors = self.eigenVectors
        for row in global_dofs:
            aux_eigenVectors = np.insert( aux_eigenVectors, row, [0], axis=0 )
        
        if self.log:
            print('Dofs before recovering:',self.eigenVectors.shape[0])
            print('Dofs after recovering:',aux_eigenVectors.shape[0])

        eigenVectors_Uxyz = np.zeros(( self.nodal_coordinates.shape[0], int(1 + (Node.degree_freedom/2)*aux_eigenVectors.shape[1]) ))
        eigenVectors_Rxyz = np.zeros(( self.nodal_coordinates.shape[0], int(1 + (Node.degree_freedom/2)*aux_eigenVectors.shape[1]) ))
        eigenVectors_Uxyz[:,0] = np.arange( 1, self.nodal_coordinates.shape[0] + 1, 1 )
        eigenVectors_Rxyz[:,0] = np.arange( 1, self.nodal_coordinates.shape[0] + 1, 1 )

        ind = np.arange( 0, aux_eigenVectors.shape[0], Node.degree_freedom )

        for j in range( self.eigenVectors.shape[1] ):
                
            eigenVectors_Uxyz[ :, 1+3*j ] = aux_eigenVectors[ ind+0, j ]
            eigenVectors_Uxyz[ :, 2+3*j ] = aux_eigenVectors[ ind+1, j ]
            eigenVectors_Uxyz[ :, 3+3*j ] = aux_eigenVectors[ ind+2, j ]
            
            eigenVectors_Rxyz[ :, 1+3*j ] = aux_eigenVectors[ ind+3, j ]
            eigenVectors_Rxyz[ :, 2+3*j ] = aux_eigenVectors[ ind+4, j ]
            eigenVectors_Rxyz[ :, 3+3*j ] = aux_eigenVectors[ ind+5, j ]
    
        if self.HA_output.all() != None:
            U_out = self.HA_output
            for i in range(len(global_dofs)):
                    U_out = np.insert( U_out, int(self.prescribed_info[1][i,0]), self.prescribed_info[1][i,2], axis=0 )
        else:
            U_out = []
            print("Please, it's necessary to solve an Harmonic Analysis if you intend recover information about prescribed dofs.")

        return eigenVectors_Uxyz, eigenVectors_Rxyz, U_out


    def plot_modal_shape(self, mode):
        
        eigen_Uxyz_plot = []
        eigen_Uxyz, _, _ = self.dof_recover()
        eigen_Uxyz_plot.append(eigen_Uxyz)
        eigen_Uxyz_plot = np.asarray(eigen_Uxyz_plot[0])
        Uxyz_mode = np.zeros((eigen_Uxyz_plot.shape[0], 4))
        Uxyz_mode[:,0] = eigen_Uxyz_plot[:,0]
        Uxyz_mode[:,1:4] = eigen_Uxyz_plot[:,(1+3*(mode-1)):(4+3*(mode-1))]

        return Uxyz_mode