import numpy as np
import matplotlib.pyplot as plt

kx_min = -13*np.pi/12
kx_max = 13*np.pi/12
ky_min = -13*np.pi/12
ky_max = 13*np.pi/12

grid_size = 200# in one direction!

kx_arr = np.linspace(kx_min, kx_max, grid_size)
ky_arr = np.linspace(ky_min, ky_max, grid_size)

KY, KX = np.meshgrid(kx_arr, ky_arr)


def dispersion(kx, ky):

    E = np.sqrt(3 + 2*np.cos(np.sqrt(3)*ky)+4*np.cos(np.sqrt(3)*ky/2)*np.cos(3*kx/2))

    return (E, -E )

bands = np.zeros((2, grid_size, grid_size))

for i in range(0, grid_size):

    for j in range(0, grid_size): 

        bands[0][i][j], bands[1][i][j] = dispersion(KX[i][j], KY[i][j])


fig, ax = plt.subplots()

c = ax.pcolormesh(KX, KY, bands[1])
colorbar = fig.colorbar(c, ax=ax)

levels = np.linspace(-3,0,10)

contours = plt.contour(KX, KY, bands[1], levels = levels, colors = "black", linestyle = "solid", linewidth = 0.5)

# Broíllouin zone
ax.plot([-2*np.pi/3, 0, 2*np.pi/3, 2*np.pi/3, 0, -2*np.pi/3, -2*np.pi/3], [-2*np.pi/(3*np.sqrt(3)), -4*np.pi/(3*np.sqrt(3)),-2*np.pi/(3*np.sqrt(3)), 2*np.pi/(3*np.sqrt(3)), 4*np.pi/(3*np.sqrt(3)), 2*np.pi/(3*np.sqrt(3)), -2*np.pi/(3*np.sqrt(3))], c = "black", ls  = "--", lw =2 ) 

# Gamma point
ax.scatter(0, 0, marker = "x", color = "black")
ax.text(0 + 0.2, 0 + 0.2, r"$\Gamma$", ha = "center", va = "center", weight = "bold", fontsize = "xx-large")

# K-point
ax.scatter( 2*np.pi/3, 2*np.pi/(3*np.sqrt(3)), marker = "x", color = "black" )
ax.text( 2*np.pi/3 +0.175 , 2*np.pi/(3*np.sqrt(3)) + 0.2, "K", ha = "center", va = "center", weight = 400 , fontsize = "xx-large")


ax.set_xticks([-np.pi, 0, np.pi])
ax.set_xticklabels([r"$-\pi$", "0", r"$\pi$"])
ax.set_yticks([-np.pi, 0, np.pi])
ax.set_yticklabels([r"$-\pi$", "0", r"$\pi$"])
ax.set_xlabel(r"$p_x$", fontsize = "x-large")
ax.set_ylabel(r"$p_y$", fontsize = "x-large")

colorbar.set_label("E", rotation = 0, labelpad = 10, size = "x-large")
fig.savefig("/home/erick/Documents/Uni/Master-Project/wiki/WARB_presentation/pictures/dispersion_honeycomb.png", bbox_inches="tight", pad_inches=0.02, dpi=300)

plt.show()
