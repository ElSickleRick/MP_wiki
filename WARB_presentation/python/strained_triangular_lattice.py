import sys
sys.path.insert(0, '/home/kuerschner/Documents/Master-Project/python')
import numpy as np
import scipy.linalg as la 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
import matplotlib.patches as ptch
import matplotlib.colors as clr
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import os
import pickle
from system_init import system_init
from analysis import post_analysis

path_head = "/home/kuerschner/Documents/Master-Project/data/strain_var"

save_path = "/home/kuerschner/Documents/Master-Project/wiki/WARB_presentation/pictures/gif"


def sort(arr):

    sorted_arr = np.array(np.sort(arr), dtype = object)

    zeros = np.where(sorted_arr == 0)[0]
    for i in zeros:
        sorted_arr[i] = int(0)
    
    return sorted_arr




def plot(C):
    
    fig_heigth = 4 # 8/27
    fig_width = 12

    fig = plt.figure(figsize=(fig_width, fig_heigth))
    
    factor = 1.25
    heigth = 8/10
    width = 4/15
    ax1 = fig.add_axes([0, 0, factor*width, factor*heigth])       # Square
    ax2 = fig.add_axes([0.05 + width + 0.1, 0.1, 2 * width, heigth]) # rectangle

    ax2.set_adjustable('datalim')

    with open(os.path.join(size_path, "pop_link_dict.pkl"), "rb") as f:
        pop_link_dict = pickle.load(f)

    with open(os.path.join(size_path, "mu_arr.pkl"), "rb") as f:
        mu_arr = pickle.load(f)

    with open(os.path.join(size_path, "eival.pkl"), "rb") as f:
        eival = pickle.load(f)

    with open(os.path.join(size_path, "eivec.pkl"), "rb") as f:
        eivec = pickle.load(f)

    eivec_avs = np.absolute(eivec)**2

    with open(os.path.join(size_path, "info.pkl"), "rb") as f:
        info = pickle.load(f)

    T = info["T"]
    kappa = info["kappa"]
    beta = info["beta"]
    C = info["C"]
    mag_elas = info["mag_elas"]
    theta = info["theta"]

    with open(os.path.join(size_path, "miscellaneous.pkl"), "rb") as f:
        miscellaneous = pickle.load(f)

    seed = miscellaneous["seed"]
    chi_init, elas_variant, chi_noise_scale, mu_noise_scale = miscellaneous["init paras"]
        
    rng = np.random.default_rng(seed) # This is possably questionable but the functions I want to call actually does not need rng       
    sys_init = system_init(T, kappa, rng, C, mag_elas, theta, elas_variant)
    strain_cord_dict = sys_init.strain_cord_gen()
    plaqu_dict = sys_init.plaqu_dict_gen()
    ul_dict = sys_init.link_dict_gen()

    grid = np.empty((0,2))

    for i in range(1, int((T+1)*(T+2)/2+1)):
            
        cords = np.array([strain_cord_dict[i][1]])
        grid = np.append(grid, cords, axis = 0)

    pos = int(np.floor(2*T/3)*(np.floor(2*T/3)-1)/2 + np.ceil(T/3)+1)
    
    def real_space_plot(i):

        lw = 2

        cmap = clr.LinearSegmentedColormap.from_list("greenred", ["purple", "blue", "green", "yellow", "red"])
        norm = clr.Normalize(vmin = 0.33, vmax = 1.66)

        for link in pop_link_dict:

            s, e, J, chi = pop_link_dict[link]

            x = [grid[s-1][0], grid[e-1][0]]
            y = [grid[s-1][1], grid[e-1][1]]
            length = np.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)
            color = cmap(norm(length))


            ax1.plot(x, y, c = color, linewidth = lw, zorder = 3)
            ax1.scatter(grid[pos-1][0], grid[pos-1][1], c = "red", zorder = 4) 
        return

    lim = 2*T/(2*np.sqrt(3))
    y_offset = T/(4*np.sqrt(3))

    ax1.set_xlim(-lim, lim)
    ax1.set_ylim(-lim+y_offset, lim+y_offset)
    
    ax1.axis('off')
    
    real_space_plot(C)

    bins = 120

    ax2.hist(eival, bins = bins, weights = eivec_avs[pos-1, :], ec = 'black', fc = 'green')
    
    ax2.set_xlim(-3, 3.5)
    ax2.set_ylim(0, 0.065)
    
    ax2.set_xticks([0])
    ax2.set_xticklabels([r"$E_F$"])
    ax2.set_yticks([])

    # plt.tight_layout()
    plt.show()

    picture_path = os.path.join(save_path, f"C={C}.png")
    fig.savefig(picture_path, dpi = 1200, facecolor = "white")

    plt.close(fig)

    return 



if __name__ == "__main__":


    projects = {
            # 'T=45_lin_minus_pi_half_1008_01' : "-pi/2, lin",
            # 'T=45_exp_minus_pi_half_1008_01' : "-pi/2, exp",
            # 'T=45_exp_pi_half_0508_01' : "pi/2, exp",
            # 'T=45_lin_pi_half_0508_01' : "pi/2, lin",
            # 'T=47_exp_pi_half_1108_01'  : "T=47",
            # 'T=45_exp_up_1308_01' : "T=45, exp, up",
            'T=65_exp_up_1308_01' : "T=65, exp, up",            
            # 'T=65_lin_up_1708_01' : "T=65, lin, up",
            # 'T=45_exp_rot_pi_half_1708_01' : "T=45 exp, rot, pi/2", 
            # 'T=65_exp_rot_up_1708_01' : "T=65 exp, rot, up", # bad convergence!!
            # 'T=65_exp_rot_up_1808_01' : "T=65 exp, rot, up",

            }

    for project in projects:
        project_path = os.path.join(path_head, project)
       
    for path in os.listdir(project_path):

        size_path = os.path.join(project_path, path)
        with open(os.path.join(size_path, "info.pkl"), "rb") as f:
            info = pickle.load(f)  

            C = info["C"]

        plot(C)

        
    """ 
    C = 0.6

    for project in projects:
        project_path = os.path.join(path_head, project) 

    size_path = os.path.join(project_path, f"C = {C}")

    plot(C)
    """



