import matplotlib.pyplot as plt
from matplotlib.lines import Line2D 
import numpy as np
import pathlib

def plot_comparison(control,control_sim,modulated,modulated_sim, num_models,ylabel,title,x_ticks=tuple(),parameterID=None,dir_path=None,save=False,filename=None):

    fig, ax = plt.subplots(1, figsize=(7,9))
    for i in range(num_models):

        ax.errorbar(i, modulated['mean'], 
                xerr=0, yerr=modulated['std'], 
                fmt='rs',capsize=5,markersize=10,elinewidth=2)
        
        ax.errorbar(i, control['mean'], 
                xerr=0, yerr=control['std'], 
                fmt='bs',capsize=2,markersize=5,elinewidth=1)

        x=i*np.ones(len(modulated_sim[i]))
        modulated_sim[i]=np.sort(modulated_sim[i])
        print(modulated_sim[i])
        z=np.zeros(len(modulated_sim[i]))
        
        j=0
        while j <= (len(modulated_sim[i])-2):
            k=0
            while j+k+1<=(len(modulated_sim[i])-1) and modulated_sim[i][j+k]==modulated_sim[i][j+k+1]:
              k=k+1
            z[j]=k+1
            j=j+k+1

        #print('z',z[z>0])
        sumnj = 0
        dx = 0.1
        for j in range(len(z)):
            nj = int(z[j])
            ev = 0
            if np.mod(nj,2)==0:
                ev = dx*0.5
            for k in range(nj):
                pos = np.ceil(k/2)*(-1)**(np.mod(k,2))
                x[sumnj+k] = i+dx*pos+ev
            sumnj = sumnj+nj

        #print('x',x)
        plt.plot(x,modulated_sim[i],'ok')
        plt.plot(i,control_sim[i],'og')
        
        plt.xlim([-15*dx,15*dx])



        
    ind = np.arange(num_models) 
    plt.xticks(ind, x_ticks, rotation=60)
    plt.ylabel(ylabel)
    plt.title(title)

    #legend
    legend_elements = [Line2D([0], [0], marker='s', color='w', label='Control Data',
                              markerfacecolor='b', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Optimised models',
                              markerfacecolor='g', markersize=10),
                       Line2D([0], [0], marker='s', color='w', label='Modulated Data',
                              markerfacecolor='r', markersize=10),
                       Line2D([0], [0], marker='o', color='w', label='Optimised Modulated models',
                              markerfacecolor='k', markersize=10),]
    ax.legend(handles=legend_elements, loc='upper right')

    if save:
        plt.savefig(pathlib.Path(dir_path) / filename,
                    dpi=None, facecolor='w', edgecolor='w',
                    orientation='portrait', papertype=None, format=None,
                    transparent=False, bbox_inches=None, pad_inches=0.1,
                    frameon=None, metadata=None)
    else:
        plt.show()
