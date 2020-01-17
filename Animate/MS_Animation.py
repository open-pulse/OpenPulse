import numpy as np
import matplotlib
from matplotlib import cm
from matplotlib import animation
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.mplot3d.art3d import Line3DCollection

""" 
----------------------------------------------------------------------------------------------------------------------------------
|    This fucntion loads nodal coordinates (x_p, y_p, z_p), nodal displacements (u_x, u_y, u_z) and plots or animate results in  |
|    graph figures for both deformed or undeformed shapes.                                                                       |
----------------------------------------------------------------------------------------------------------------------------------

"""

def MS_animation(coordinates, connectivity, u_def, scf = 0.4, Show_nodes = True, Undeformed = True, Deformed = False, Animate_Mode = True, Save = False):

    u_x, u_y, u_z = u_def[:,0], u_def[:,1], u_def[:,2]

    r = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    r_max = max(r)

    x_p, y_p, z_p = coordinates[:,0], coordinates[:,1], coordinates[:,2]
    Coord_dn = np.transpose(np.array([x_p, y_p, z_p]) + np.array([u_x, u_y, u_z])*scf/r_max)
    x_def,y_def,z_def = Coord_dn[:,0], Coord_dn[:,1],Coord_dn[:,2] 
    
    ax_lim = np.zeros((2,3))
    ax_lim[0,:] = Coord_dn.min(axis=0) 
    ax_lim[1,:] = Coord_dn.max(axis=0) 

    norm = plt.Normalize(min(r), max(r),clip=True)
    cmap = matplotlib.cm.get_cmap('jet')
    line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)

    fig = plt.figure(figsize=[12,8])
    ax = fig.add_subplot(1,1,1, projection='3d')
    ax.add_collection(line)

    a, lw, marker_size = 1.1, 0, 50

    if Show_nodes:

        graph = ax.scatter3D(x_p*0,y_p*0,z_p*0,zdir='z',zorder=1,marker='s',norm=norm,c=r,cmap=cmap,alpha=1,edgecolors='face',s=marker_size)
    
 
    ax.set_xlim3d(round(a*ax_lim[0,0],1), round(a*ax_lim[1,0],1))
    ax.set_ylim3d(round(a*ax_lim[0,1],1), round(a*ax_lim[1,1],1))
    ax.set_zlim3d(round(a*ax_lim[0,2],1), round(a*ax_lim[1,2],1))

    ax.set_title(('Forma modal - ' + str('??') + 'º modo'),fontsize=18,fontweight='bold')
    ax.set_xlabel(('Posição x[m]'),fontsize=14,fontweight='bold')
    ax.set_ylabel(('Posição y[m]'),fontsize=14,fontweight='bold')
    ax.set_zlabel(('Posição z[m]'),fontsize=14,fontweight='bold')

    n_el = len(connectivity[:,1])
    segments_p = np.zeros((n_el,2,3))
    segments_u = np.zeros((n_el,2,3))
    r_m = np.zeros(n_el)  

    ind = int(0)

    for start, end in connectivity:

        ind += 1
        segments_p[ind-1:ind,:,:] = np.array([[x_p[start-1], y_p[start-1], z_p[start-1]],[x_p[end-1], y_p[end-1], z_p[end-1]]])
        segments_u[ind-1:ind,:,:] = np.array([[u_x[start-1], u_y[start-1], u_z[start-1]],[u_x[end-1], u_y[end-1], u_z[end-1]]])
        r_m[ind-1] = (r[start-1]+r[end-1])/2

    if Undeformed:

        line.set_segments(segments_p)
        line.set_color([0,0,0])
        # ax.add_collection3d(line)
     
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)
        
        if Show_nodes:
   
            ax.scatter3D(x_p,y_p,z_p,zdir='z',zorder=2,marker='s',color=[0,0,0],norm='none',alpha=1,edgecolors='face',lw=lw,s=marker_size)
            
        plt.draw()
       
    if Deformed:
 
        ax.add_collection3d(line)
        segments = segments_p + segments_u*(scf/r_max)
        line.set_segments(segments)
        line.set_array(r_m)
    
        if Show_nodes:
   
            ax.scatter3D(x_def,y_def,z_def,zdir='z',zorder=2,marker='s',norm=norm,c=r,cmap=cmap,alpha=1,edgecolors='face',lw=lw,s=marker_size)
            
        plt.draw()

    if Animate_Mode:

        frames = 300
        delay_ms = 1000/60
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)
        ax.add_collection3d(line)

        # initialization function: plot the background of each frame

        def init():

            graph._offsets3d = [],[],[]
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
                graph.set_linewidths(lw=lw)
             
                # plt.draw()
                        
            return
              
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=delay_ms, blit=False)
        
        if Save:

            anim.save('Modal_shape_3d.gif', writer='pillow')
        
        plt.show()
    
    else:
        
        plt.show()
    
    return

if __name__ == "__main__":

    # Load nodal results from different files      
    connectivity = np.array(np.loadtxt('connect.dat')[:,-2:],int)
    coordinates = np.loadtxt('coord.dat')
    u_def = np.loadtxt('u_def.dat')
   
    # Choose the information to plot/animate
    Show_nodes, Undeformed, Deformed, Animate_Mode, Save = True, True, False, True, False

     # Scalling amplitude factor
    scf=0.4

    # Call function to plot nodal results [dynamic]
    MS_animation(coordinates, connectivity, u_def, scf, Show_nodes, Undeformed, Deformed, Animate_Mode, Save)