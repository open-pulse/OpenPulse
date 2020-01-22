import numpy as np
import matplotlib
from matplotlib import cm, colors
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import norm

fig = plt.figure(figsize=[12,8])
ax = fig.add_subplot(111, projection='3d',)
origin = np.array([0, 0, 0])

def pipe_plot(coordinates, connectivity, u_def, mode, scf, radius, thickness, n_div_theta, n_div_t):

    # u_def = eigvects[:,mode-1]
    
    # u_x = np.array( [ u_def[6*i    ] for i in range(int( u_def.shape[0] / 6 )) ])
    # u_y = np.array( [ u_def[6*i + 1] for i in range(int( u_def.shape[0] / 6 )) ])
    # u_z = np.array( [ u_def[6*i + 2] for i in range(int( u_def.shape[0] / 6 )) ])

    u_x, u_y, u_z = u_def[:,0], u_def[:,1], u_def[:,2]

    r = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    r_max = max(r)

    x_p, y_p, z_p = coordinates[:,0], coordinates[:,1], coordinates[:,2]
    Coord_dn = np.transpose(np.array([x_p, y_p, z_p]) + np.array([u_x, u_y, u_z])*scf/r_max)
    x_def, y_def, z_def = Coord_dn[:,0], Coord_dn[:,1], Coord_dn[:,2] 
    
    ax_lim = np.zeros((2,3))
    ax_lim[0,:] = Coord_dn.min(axis=0) 
    ax_lim[1,:] = Coord_dn.max(axis=0) 

    a, lw, e_lw, marker_size = 1.1, 2, 0, 50
    
    ax.set_xlim3d(round(a*ax_lim[0,0],1), round(a*ax_lim[1,0],1))
    ax.set_ylim3d(round(a*ax_lim[0,1],1), round(a*ax_lim[1,1],1))
    ax.set_zlim3d(round(a*ax_lim[0,2],1), round(a*ax_lim[1,2],1))

    str_ord = ['st','nd','rd']

    if mode-1 <= 2:
        ordinary = str_ord[mode-1]
    else:
        ordinary = 'th'

    ax.set_title(('Modal shape - ' + str(mode) + ordinary + ' mode'), fontsize=18, fontweight='bold')
    ax.set_xlabel(('Position x[m]'), fontsize=14, fontweight='bold')
    ax.set_ylabel(('Position y[m]'), fontsize=14, fontweight='bold')
    ax.set_zlabel(('Position z[m]'), fontsize=14, fontweight='bold')

    connectivity = np.array(connectivity[:,-2:],int)
    n_el = len(connectivity[:,1])
    n_nodes = len(coordinates[:,1])

    r_out = np.ones((n_el,1))*radius
    p_res = []
    p_res = r
    norm = colors.Normalize(np.min(p_res),np.max(p_res), clip = False)

    ind = int(0)  
    
    for start, end in connectivity:

        ind += 1

        # create an intensity vector c for each pipe segment based on nodal scalar value evaluated  
        c = np.ones((n_div_theta+1,n_div_t))*np.interp(np.linspace(0,1,n_div_t), [0,1], np.array([p_res[start-1],p_res[end-1]]), left=None, right=None, period=None)

        #axis and radius
        p0, p1 = coordinates[start-1,:], coordinates[end-1,:]
        p0, p1 = Coord_dn[start-1,:], Coord_dn[end-1,:]
        R = r_out[ind-1]
        
        #vector in direction of axis
        v = p1 - p0

        #find magnitude of vector
        mag = np.linalg.norm(v)

        #unit vector in direction of axis
        v = v / mag
        
        #make some vector not in the same direction as v
        not_v = np.array([1, 0, 0])

        if (v == not_v).all():
            not_v = np.array([0, 1, 0])

        #make vector perpendicular to v
        n1 = np.cross(v, not_v)

        #normalize n1
        n1 = n1/np.linalg.norm(n1)
        
        #make unit vector perpendicular to v and n1
        n2 = np.cross(v, n1)

        #surface ranges over t from 0 to length of axis and 0 to 2*pi
        t = np.linspace(0, mag, n_div_t)
        theta = np.linspace(0, 2 * np.pi, n_div_theta+1)

        #use meshgrid to make 2d arrays
        t, theta = np.meshgrid(t, theta)

        #generate coordinates for outer and inner surfaces
        
        X, Y, Z    = [p0[i] + v[i] * t + R * np.sin(theta) * n1[i] + R * np.cos(theta) * n2[i] for i in [0, 1, 2]]
        Xi, Yi, Zi = [p0[i] + v[i] * t + (R-thickness) * np.sin(theta) * n1[i] + (R-thickness) * np.cos(theta) * n2[i] for i in [0, 1, 2]]    
        
        graph = []
        graph.append(ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.jet(norm(c)), antialiased=False, shade=False))    
        graph.append(ax.plot_surface(Xi, Yi, Zi, rstride=1, cstride=1, facecolors=cm.jet(norm(c)), antialiased=False, shade=False))    
        graph.append(ax.plot_surface(np.array([Xi[:,0],X[:,0]]),np.array([Yi[:,0],Y[:,0]]),np.array([Zi[:,0],Z[:,0]]), rstride=1, cstride=1, facecolors=cm.jet(norm(np.array([c[:,0],c[:,0]]))), antialiased=False, shade=False))
        graph.append(ax.plot_surface(np.array([Xi[:,-1],X[:,-1]]),np.array([Yi[:,-1],Y[:,-1]]),np.array([Zi[:,-1],Z[:,-1]]), rstride=1, cstride=1, facecolors=cm.jet(norm(np.array([c[:,-1],c[:,-1]]))), antialiased=False, shade=False))
        
        for i in range (len(graph)): 
            graph[i].set_edgecolors([0,0,0])
            graph[i].set_linewidths(0.0)

        ax.plot(*zip(p0, p1), color = 'red')

    m = cm.ScalarMappable(cmap=cm.jet)
    m.set_array([])
    m.set_array(r)

    cb = fig.colorbar(m, shrink=0.8)
    cb.set_label('Amplitude [-]', fontsize=14, fontweight='bold')

    plt.show()

if __name__ == "__main__":

    # Example       

    radius = 0.05
    thickness = 0.01

    n_div_theta = 10
    n_div_t = 3

    # Load nodal results from different files      
    connectivity = np.array(np.loadtxt('connect.dat')[:,-2:],int)
    coordinates = np.loadtxt('coord.dat')
    u_def = np.loadtxt('u_def.dat')
    mode = 1
   
    # Scalling amplitude factor
    scf=0.4

    # Call function to plot cylinders
    pipe_plot(coordinates, connectivity, u_def, mode, scf, radius, thickness, n_div_theta,n_div_t)