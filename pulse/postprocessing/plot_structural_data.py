import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL

# this is temporary, and will be changed a lot
def get_frf(mesh, solution, node, dof):
    position = mesh.nodes[node].global_index * DOF_PER_NODE_STRUCTURAL + dof
    results = np.abs(solution[position])
    return results

def get_structural_response(mesh, solution, column, scf=0.2, gain=[], Normalize=True):

    data = np.real(solution)
    rows = int(data.shape[0]/DOF_PER_NODE_STRUCTURAL)
    cols = int(1 + (DOF_PER_NODE_STRUCTURAL/2)*data.shape[1])
    ind = np.arange( 0, data.shape[0], DOF_PER_NODE_STRUCTURAL )
    Uxyz = np.zeros((rows, cols))
    Rxyz = np.zeros((rows, cols))
    Uxyz[:,0] = np.arange( 0, rows, 1 )
    Rxyz[:,0] = np.arange( 0, rows, 1 )

    for j in range( data.shape[1] ):
            
        Uxyz[:, 1+3*j], Uxyz[:, 2+3*j], Uxyz[:, 3+3*j] = data[ind+0, j], data[ind+1, j], data[ind+2, j]
        Rxyz[:, 1+3*j], Rxyz[:, 2+3*j], Rxyz[:, 3+3*j] = data[ind+3, j], data[ind+4, j], data[ind+5, j]

    u_x, u_y, u_z = Uxyz[:,1+3*(column)], Uxyz[:,2+3*(column)], Uxyz[:,3+3*(column)]
    r_def = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    
    if Normalize:
        r_max = max(r_def)
    else:
        r_max, scf = 1, 1

    coord_def = np.zeros((rows,4))
    coord = mesh.nodal_coordinates_matrix
    connect = mesh.connectivity_matrix

    if gain == []:
        factor = (scf/r_max)
    else:
        factor = gain*(scf/r_max)

    coord_def[:,0] = coord[:,0]
    coord_def[:,1] = coord[:,1] + u_x*factor
    coord_def[:,2] = coord[:,2] + u_y*factor
    coord_def[:,3] = coord[:,3] + u_z*factor
        
    return connect, coord_def, r_def, factor