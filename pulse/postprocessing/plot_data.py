import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE

# this is temporary, and will be changed a lot
def get_frf(mesh, solution, node, dof):
    position = mesh.nodes[node].global_index * DOF_PER_NODE + dof
    y = np.abs(solution[position])
    return y

def get_displacement_matrix(mesh, solution, column, scf=0.4):

    data = np.real(solution)
    rows = int(data.shape[0]/DOF_PER_NODE)
    cols = int(1 + (DOF_PER_NODE/2)*data.shape[1])
    ind = np.arange( 0, data.shape[0], DOF_PER_NODE )
    Uxyz = np.zeros((rows, cols))
    Rxyz = np.zeros((rows, cols))
    Uxyz[:,0] = np.arange( 0, rows, 1 )
    Rxyz[:,0] = np.arange( 0, rows, 1 )

    for j in range( data.shape[1] ):
            
        Uxyz[:, 1+3*j], Uxyz[:, 2+3*j], Uxyz[:, 3+3*j] = data[ind+0, j], data[ind+1, j], data[ind+2, j]
        Rxyz[:, 1+3*j], Rxyz[:, 2+3*j], Rxyz[:, 3+3*j] = data[ind+3, j], data[ind+4, j], data[ind+5, j]

    u_x, u_y, u_z = Uxyz[:,1+3*(column)], Uxyz[:,2+3*(column)], Uxyz[:,3+3*(column)]
    r_def = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    r_max = max(r_def)

    coord = np.zeros((rows,4))
    coord_def = np.zeros((rows,4))
    count = 0
    
    for i, node in mesh.nodes.items():
        # index = mesh.nodes[i].global_index
        coord[count,0] = i
        coord_def[count,0] = i
        coord[count,1:4] = node.x, node.y, node.z
        count += 1
        
    coord_def[:,1] = coord[:,1] + u_x*(scf/r_max)
    coord_def[:,2] = coord[:,2] + u_y*(scf/r_max)
    coord_def[:,3] = coord[:,3] + u_z*(scf/r_max)
        
    return coord_def, r_def