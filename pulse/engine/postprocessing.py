import numpy as np

from pulse.engine.assembly import Assembly
from pulse.engine.node import Node

class PostProcessing:

    def __init__(self, fixed_nodes, presc_dofs, value_prescribed_dofs, nodal_coordinates, **kwargs):

        self.fixed_nodes = fixed_nodes
        self.presc_dofs = presc_dofs
        self.value_prescribed_dofs = value_prescribed_dofs 
        self.nodal_coordinates = nodal_coordinates
        self.fn = kwargs.get("fn", None)
        # self.dofs_fixed = kwargs.get("dofs_fixed", None)
        self.eigenVectors = kwargs.get("eigenVectors", None)
        self.HA_output = kwargs.get("HA_output", None)


    def dof_recover(self):
        """ 
        This method returns eigenVectors with all prescribed dofs values recovered.
        Similarly, it returns final dofs response U considering already prescribed dofs values.

        """

        global_dofs = np.sort( self.presc_dofs )
        print('Dofs before recovering:',self.eigenVectors.shape[0])

        for row in global_dofs:
            print(row)
            self.eigenVectors = np.insert( self.eigenVectors, row, [0], axis=0 )
        print('Dofs after recovering:',self.eigenVectors.shape[0])

        eigenVectors_Uxyz = np.zeros(( self.nodal_coordinates.shape[0], int(1 + (Node.degree_freedom/2)*self.eigenVectors.shape[1]) ))
        eigenVectors_Rxyz = np.zeros(( self.nodal_coordinates.shape[0], int(1 + (Node.degree_freedom/2)*self.eigenVectors.shape[1]) ))
        eigenVectors_Uxyz[:,0] = np.arange( 1, self.nodal_coordinates.shape[0] + 1, 1 )
        eigenVectors_Rxyz[:,0] = np.arange( 1, self.nodal_coordinates.shape[0] + 1, 1 )

        ind = np.arange( 0, self.eigenVectors.shape[0], Node.degree_freedom )

        for j in range( self.eigenVectors.shape[1] ):
                
            eigenVectors_Uxyz[ :, 1+3*j ] = self.eigenVectors[ ind+0, j ]
            eigenVectors_Uxyz[ :, 2+3*j ] = self.eigenVectors[ ind+1, j ]
            eigenVectors_Uxyz[ :, 3+3*j ] = self.eigenVectors[ ind+2, j ]
            
            eigenVectors_Rxyz[ :, 1+3*j ] = self.eigenVectors[ ind+3, j ]
            eigenVectors_Rxyz[ :, 2+3*j ] = self.eigenVectors[ ind+4, j ]
            eigenVectors_Rxyz[ :, 3+3*j ] = self.eigenVectors[ ind+5, j ]
    
        if self.HA_output.all() != None:
            U_out = self.HA_output
            count = int(0)

            for i in range(self.fixed_nodes.shape[0]):

                values = np.array(self.value_prescribed_dofs[i]).shape[0]
                print(values)

                for j in range(values):

                    U_out = np.insert( U_out, self.presc_dofs[count], self.value_prescribed_dofs[i][j], axis=0 )
                   
                    print(self.value_prescribed_dofs[i][j], count )
                    count += 1
                
        else:
            U_out = []
            print("Please, it's necessary to solve onde Harmonic Analysis if you pretend recover information about prescribed dofs !!!")

        return eigenVectors_Uxyz, eigenVectors_Rxyz, U_out
  
