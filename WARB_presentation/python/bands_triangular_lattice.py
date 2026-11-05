import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


kx_min = -13*np.pi/12
kx_max = 13*np.pi/12
ky_min = -13*np.pi/12
ky_max = 13*np.pi/12

grid_size = 3300 # in one direction!

kx_arr = np.linspace(kx_min, kx_max, grid_size)
ky_arr = np.linspace(ky_min, ky_max, grid_size)

KY, KX = np.meshgrid(kx_arr, ky_arr)


def dispersion(kx, ky):

    E = 2*np.sqrt(np.sin(kx)*np.sin(np.sqrt(3)*ky) + np.cos(kx)**2 + 1)

    return (E, -E )

bands = np.zeros((2, grid_size, grid_size))

for i in range(0, grid_size):

    for j in range(0, grid_size): 

        bands[0][i][j], bands[1][i][j] = dispersion(KX[i][j], KY[i][j])


fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

surf_bottom = ax.plot_surface(KX, KY, bands[0], color = '#0072B2', alpha = 0.9, linewidth = 0, antialiased = True, edgecolor = 'none', shade= True)
surf_top = ax.plot_surface(KX, KY, bands[1], color = '#D55E00', alpha = 0.9, linewidth = 0, antialiased = True, edgecolor = 'none', shade = 'True')

ax.set_xticks([])
ax.set_yticks([])

ax.view_init(elev=7, azim=70, vertical_axis = 'z')


ax.set_xlabel(f"$p_x$", size = "x-large")
ax.set_ylabel(f"$p_y$", size = "x-large")
ax.zaxis.set_rotate_label(False)
ax.set_zlabel("E", rotation = "horizontal" ,  size = "x-large")


fig.savefig("/home/erick/Documents/Uni/Master-Project/wiki/WARB_presentation/pictures/bands_triangular_lattice.png", bbox_inches="tight", pad_inches=0.02, dpi=1200)
plt.show()
