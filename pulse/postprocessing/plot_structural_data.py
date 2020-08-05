import numpy as np

from pulse.preprocessing.node import DOF_PER_NODE_STRUCTURAL

# this is temporary, and will be changed a lot
def get_structural_frf(mesh, solution, node, dof, absolute=False, real=False, imaginary=False):
    position = mesh.nodes[node].global_index * DOF_PER_NODE_STRUCTURAL + dof
    if absolute:
        results = np.abs(solution[position])
    elif real:
        results = np.real(solution[position])
    elif imaginary:
        results = np.imag(solution[position])
    else:
        results = solution[position]
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
        if r_max==0:
            r_max=1
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

def get_reactions(mesh, reactions, node, dof, absolute=False, real=False, imaginary=False):
    #reactions: dictionary with all reactions and global dofs are the keys of dictionary
    key = mesh.nodes[node].global_index * DOF_PER_NODE_STRUCTURAL + dof
    # print("Node ID: {} - key: {}".format(node,key))
    if absolute:
        results = np.abs(reactions[key])
    elif real:
        results = np.real(reactions[key])
    elif imaginary:
        results = np.imag(reactions[key])
    else:
        results = reactions[key]
    return results

def get_stress_spectrum_data(stresses, element_id, stress_key, absolute = False, real = False, imaginary = False):
    if absolute:
        return np.abs(np.array(stresses[element_id][stress_key,:]))
    elif real:
        return np.real(np.array(stresses[element_id][stress_key,:]))
    elif imaginary:
        return np.imag(np.array(stresses[element_id][stress_key,:]))
    else:
        return np.array(stresses[element_id][stress_key,:])

# def get_internal_loads_data(mesh, column, absolute=False, real=False, imaginary=False):

#     elements = mesh.structural_elements
#     internal_loads = [np.r_[i, elements[i].internal_load[:, column]] for i in elements ]
#     if absolute:
#         return np.abs(np.array(internal_loads))
#     elif real:
#         return np.real(np.array(internal_loads))
#     elif imaginary:
#         return np.imag(np.array(internal_loads))
#     else:
#         return np.array(internal_loads) 