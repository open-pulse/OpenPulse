import numpy as np
import matplotlib
from matplotlib import animation
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d.art3d import Line3DCollection

""" 
----------------------------------------------------------------------------------------------------------------------------------
|    This fucntion loads nodal coordinates (x_p, y_p, z_p), nodal displacements (u_x, u_y, u_z) and plots or animate results in  |
|    graph figures for both deformed or undeformed shapes.                                                                       |
----------------------------------------------------------------------------------------------------------------------------------
"""

def modeshape_plot(coordinates, connectivity, eigvects, freq_n, scf = 0.4, Show_nodes = True, Undeformed = True, Deformed = False, Animate_Mode = True, Save = False):

    # u_def = eigvects[:,mode-1]
    
    # u_x = np.array( [ u_def[6*i    ] for i in range(int( u_def.shape[0] / 6 )) ])
    # u_y = np.array( [ u_def[6*i + 1] for i in range(int( u_def.shape[0] / 6 )) ])
    # u_z = np.array( [ u_def[6*i + 2] for i in range(int( u_def.shape[0] / 6 )) ])
    
    u_def = eigvects
    u_x, u_y, u_z = u_def[:,0], u_def[:,1], u_def[:,2]

    r = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    r_max = max(r)

    x_p, y_p, z_p = coordinates[:,0], coordinates[:,1], coordinates[:,2]
    Coord_dn = np.transpose(np.array([x_p, y_p, z_p]) + np.array([u_x, u_y, u_z])*scf/r_max)
    x_def,y_def,z_def = Coord_dn[:,0], Coord_dn[:,1],Coord_dn[:,2] 
    
    ax_lim = np.zeros((2,3))
    ax_lim[0,:] = Coord_dn.min(axis=0) 
    ax_lim[1,:] = Coord_dn.max(axis=0) 

    a, lw, e_lw, marker_size = 1.1, 2, 0, 50
    
    norm = plt.Normalize(-0.0, max(r),clip=False)
    # norm = plt.Normalize(min(r), max(r),clip=True)
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
            'size': 14,
            }

    ax.set_title((r'Modal shape - $\mathbf{f_n}$ =' + str(round(freq_n,2)) + r'Hz'),fontsize=18,fontweight='bold')

    ax.set_xlabel(('Position x[m]'),fontdict=font)
    ax.set_ylabel(('Position y[m]'),fontdict=font)
    ax.set_zlabel(('Position z[m]'),fontdict=font)
    plt.tight_layout()

    m = matplotlib.cm.ScalarMappable(cmap=matplotlib.cm.jet)
    m.set_array([])
    m.set_array(r)

    cb = fig.colorbar(m, shrink=0.8)
    cb.set_label('Amplitude [-]', fontdict=font)
    dict(zip(coordinates[:,0], coordinates[:,1:]))

    connectivity = np.array(connectivity[:,-2:],int)
    n_el = len(connectivity[:,1])
    segments_p = np.zeros((n_el,2,3))
    segments_u = np.zeros((n_el,2,3))
    r_m = np.zeros(n_el)  

    dict(zip())

    ind = int(0)

    np.arange()

    for start, end in connectivity:

        ind += 1
        segments_p[ind-1:ind,:,:] = np.array([[x_p[start-1], y_p[start-1], z_p[start-1]],[x_p[end-1], y_p[end-1], z_p[end-1]]])
        segments_u[ind-1:ind,:,:] = np.array([[u_x[start-1], u_y[start-1], u_z[start-1]],[u_x[end-1], u_y[end-1], u_z[end-1]]])
        r_m[ind-1] = (r[start-1]+r[end-1])/2

    if Undeformed:

        line.set_segments(segments_p)
        line.set_color([0,0,0])
     
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=lw)
        
        if Show_nodes:
   
            ax.scatter3D(x_p,y_p,z_p,zdir='z',zorder=2,marker='s',color=[0,0,0],norm='none',alpha=1,edgecolors='face',lw=e_lw,s=marker_size)           

    if Deformed:
        
        ax.add_collection3d(line)
        segments = segments_p + segments_u*(scf/r_max)
        line.set_segments(segments)
        line.set_array(r_m)
    
        if Show_nodes:
   
            ax.scatter3D(x_def,y_def,z_def,zdir='z',zorder=2,marker='s',norm=norm,c=r,cmap=cmap,alpha=1,edgecolors='face',lw=e_lw,s=marker_size)

    if Animate_Mode:

        frames = 180
        delay_ms = 1000/60
        # delay_ms = 20
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=lw)
        ax.add_collection3d(line)

        # Set-up scatter3D plot  
        if Show_nodes:

            graph = ax.scatter3D(x_def,y_def,z_def,zdir='z',zorder=1,marker='s',norm=norm,c=r,cmap=cmap,alpha=1,edgecolors='face',lw=e_lw,s=marker_size)
  
        # initialization function: plot the background of each frame

        def init():

            line.set_segments([])
            return

        # animation function.  This is called sequentially
        t=1
        def animate(i):

            segments_i = segments_p + segments_u*(scf/r_max)*np.cos(2 * np.pi * (i*4/frames)*t)
            r_i = r_m*np.abs(np.cos(2 * np.pi * (i*4/frames)*t))

            line.set_segments(segments_i)
            line.set_array(r_i)
            line.set_zorder(2)

            if Show_nodes:

                r_ii = r*np.abs(np.cos(2 * np.pi * (i*4/frames)*t))
                Coord_anima = np.transpose(np.array([x_p, y_p, z_p]) + np.array([u_x, u_y, u_z])*(scf/r_max)*np.cos(2 * np.pi * (i*4/frames)*t))
                x_i, y_i, z_i = Coord_anima[:,0],Coord_anima[:,1],Coord_anima[:,2]
    
                graph._offsets3d = x_i, y_i, z_i
                graph.set_array(r_ii)
                graph.set_zorder(1)
                # graph._facecolor3d = [0,0,0] 
                # graph._edgecolor3d = graph.get_facecolor()
                # graph.set_linewidths(lw=lw)
                            
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=delay_ms, blit=False)
        
        if Save:

            anim.save('Modal_shape_3d.gif', writer='pillow')
        
        plt.show()
    
    else:
        
        plt.show()
    
    return

# if __name__ == "__main__":

#     # Load nodal results from different files 
#     mode = 32 
#     connectivity = np.array(np.loadtxt('Ex_02/connect.dat')[:,1:],int)
#     coordinates = np.array(np.loadtxt('Ex_02/coord.dat')[:,1:])
#     u_def = np.array(np.loadtxt('Ex_02/u_def.dat')[:,1+(mode-1)*3:3+(mode-1)*3+1])

   
#     # Choose the information to plot/animate
#     Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, False, False, True, True

#      # Scalling amplitude factor
#     scf=0.4

#     # Call function to plot nodal results [dynamic]
#     modeshape_plot(coordinates, connectivity, u_def, mode, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)