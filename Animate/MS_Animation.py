import numpy as np
import matplotlib
from matplotlib import cm
from matplotlib import animation
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.mplot3d.art3d import Line3DCollection

def MS_animation(coordinates, connectivity, u_def, scf = 0.4, Undeformed = True, Deformed = False, Animate_Mode = True, Save = False):
    
    u_x, u_y, u_z = u_def[:,0], u_def[:,1], u_def[:,2]

    r = ((u_x)**2 + (u_y)**2 + (u_z)**2)**(1/2) 
    r_max = max(r)

    x_p, y_p, z_p = coordinates[:,0], coordinates[:,1], coordinates[:,2]
    Coord_dn = np.array([x_p + u_x*scf/max(r), y_p + u_y*scf/max(r), z_p + u_z*scf/max(r)])
    
    ax_lim = np.zeros((2,3))
    ax_lim[0,:] = Coord_dn.min(axis=1) 
    ax_lim[1,:] = Coord_dn.max(axis=1) 

    fig = plt.figure(figsize=[12,8])
    ax = fig.add_subplot(1,1,1, projection='3d')

    norm = plt.Normalize(min(r), max(r))
    cmap = matplotlib.cm.get_cmap('jet')

    line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)

    a = 1.1
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

    if Undeformed:
        
        line.set_segments(segments_p)
        line.set_color([0,0,0])
        ax.add_collection3d(line)
        plt.draw()
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)
        
    ind = int(0)

    for start, end in connectivity:

        ind += 1
        r_m[ind-1] = (r[start-1]+r[end-1])/2

        segments_u[ind-1:ind,:,:] = np.array([[u_x[start-1], u_y[start-1], u_z[start-1]],[u_x[end-1], u_y[end-1], u_z[end-1]]])
        segments_p[ind-1:ind,:,:] = np.array([[x_p[start-1], y_p[start-1], z_p[start-1]],[x_p[end-1], y_p[end-1], z_p[end-1]]])

    if Deformed:
                
        segments = segments_p + segments_u*(scf/r_max)
        line.set_segments(segments)
        line.set_array(r_m)
        ax.add_collection3d(line)
        plt.draw()
        line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)
    
    if Animate_Mode:

        frames = 200
        delay_ms = 1000/60

        cmap = 'jet'
        norm = plt.Normalize(min(r_m), max(r_m))

        line = Line3DCollection([], cmap=cmap, norm=norm, lw=2)
        ax.add_collection(line)

        # initialization function: plot the background of each frame

        def init():
            line.set_segments([])
            return

        # animation function.  This is called sequentially

        def animate(i):
            segments_i = segments_p + segments_u*(scf/r_max)*np.cos(2 * np.pi * (i*4/frames))
            r_i = r_m*np.abs(np.cos(2 * np.pi * (i*4/frames)))
            line.set_segments(segments_i)
            line.set_array(r_i)
            return
              
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=delay_ms, blit=False)
        
        if Save:
            anim.save('Modal_shape_3d.gif', writer='pillow')
        
        plt.show()
    
    else:
        plt.show()
    
    return

# def show_points(coordinates):
#     for point in coordinates:
#         ax.scatter(*point, color='red')


if __name__ == "__main__":

    # Exemplo       
    connectivity = np.array(np.loadtxt('connect.dat')[:,-2:],int)
    coordinates = np.loadtxt('coord.dat')
    u_def = np.loadtxt('u_def.dat')
   
    # Scalling amplitude factor
    scf=0.4

    Undeformed, Deformed, Animate_Mode, Save = True, False, True, False
    
    # Call function to plot Deformed models [dynamic]
    MS_animation(coordinates, connectivity, u_def)
    
