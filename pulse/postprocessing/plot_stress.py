import numpy as np
import matplotlib
from matplotlib import cm, colors
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from scipy.linalg import norm

def get_stress_data(mesh, column):
    
    elements = mesh.structural_elements
    stresses = np.real(np.array([np.r_[i, elements[i].stress[:, column]] for i in elements ]))
    return stresses

def get_internal_loads_data(mesh, column):
    
    elements = mesh.structural_elements
    internal_loads = np.real(np.array([np.r_[i, elements[i].internal_load[:, column]] for i in elements ]))
    return internal_loads

def pipe_plot(mesh, data, stress, scf):

    connectivity = mesh.connectivity_matrix 
    coordinates = mesh.nodal_coordinates_matrix

    s = stress[:,1]

    u_def = data[:,1:] - coordinates[:,1:]
    r = np.sum(u_def**2, axis = 1)**(1/2)
    r_max = max(r)
    Coord_dn = coordinates[:,1:] + np.real(u_def*scf/r_max)

    ax_lim = np.zeros((2,3))
    ax_lim[0,:] = Coord_dn.min(axis=0) 
    ax_lim[1,:] = Coord_dn.max(axis=0) 

    a, lw = 1.1, 5
    
    norm = plt.Normalize(min(s), max(s), clip=False)
    cmap = matplotlib.cm.get_cmap('jet')
    line = Line3DCollection([], cmap=cmap, norm=norm, lw=lw)

    fig = plt.figure(figsize=[12,8])
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.add_collection(line)
    
    ax.set_xlim3d(round(a*ax_lim[0,0],1), round(a*ax_lim[1,0],1))
    ax.set_ylim3d(round(a*ax_lim[0,1],1), round(a*ax_lim[1,1],1))
    ax.set_zlim3d(round(a*ax_lim[0,2],1), round(a*ax_lim[1,2],1))

    ax.view_init(elev=26, azim=-37)
    
    font = {'family': 'arial',
            'color':  'black',
            'weight': 'bold',
            'size': 14}

    ax.set_xlabel(('Position x[m]'),fontdict=font)
    ax.set_ylabel(('Position y[m]'),fontdict=font)
    ax.set_zlabel(('Position z[m]'),fontdict=font)
    plt.tight_layout()

    m = matplotlib.cm.ScalarMappable(cmap='jet')
    m.set_array([])
    m.set_array(s)

    cb = fig.colorbar(m, shrink=0.8)
    cb.set_label('Amplitude [-]', fontdict=font)
    
    connectivity = np.array(connectivity[:,-2:],int)
    n_el = len(connectivity[:,1])
    segments_p = np.zeros((n_el,2,3))
    segments_u = np.zeros((n_el,2,3))


    for ind, (start, end) in enumerate(connectivity):
        segments_p[ind:ind+1,:,:] = np.array([coordinates[start,1:],coordinates[end,1:]])
        segments_u[ind:ind+1,:,:] = np.array([u_def[start],u_def[end]])
            
    ax.add_collection3d(line)
    segments = segments_p + segments_u*(scf/r_max)
    line.set_segments(segments)
    line.set_array(s)

    plt.show()