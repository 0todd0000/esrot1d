
import os
import numpy as np
from matplotlib import pyplot as plt
import esrot1d as e1d
e1d.set_plot_style()



# set parameters:
np.random.seed(0)
niter  = 100
Q      = 101
fwhm   = 20
fwhms  = [5, 20, 50]
N1     = 15
N2     = 8
ns1    = [9, 19, 39]  # df:  8, 18, 38
ns2    = [5, 10, 20]  # df:  8, 18, 38
u      = np.arange(0, 2.1, 0.2)
u0     = np.linspace(0, 2, 51)




# load sim results:
fpath     = os.path.join( os.path.dirname(__file__), 'results_sim.h5' )
d         = e1d.io.load_h5( fpath )
sf10      = d['sf10']
sf11w     = d['sf11w']
sf11n     = d['sf11n']
sf20      = d['sf20']
sf21w     = d['sf21w']
sf21n     = d['sf21n']
sf10_an   = d['sf10_an']
sf11n_an  = d['sf11n_an']
sf11w_an  = d['sf11w_an']
sf20_an   = d['sf20_an']
sf21n_an  = d['sf21n_an']
sf21w_an  = d['sf21w_an']



# plot:
plt.close('all')
fig,axs = plt.subplots( 3, 2, figsize=(8,8), tight_layout=True )
colors  = ['r', 'g', 'b']


sf_ans  = [sf10_an, sf20_an, sf11n_an, sf21n_an, sf11w_an, sf21w_an]
sfs     = [sf10, sf20, sf11n, sf21n, sf11w, sf21w]
for ax,sf_an,sf in zip(axs.ravel(), sf_ans, sfs):
    for i,c in enumerate(colors):
        ax.plot(u0, np.log(sf_an[i]), color=c)
        ax.plot(u, np.log(sf[i]), 'o', color=c )


[ax.set_xticklabels([])  for ax in axs[:2,:2].ravel()]
[ax.set_yticklabels([])  for ax in axs[:,1]]
plt.setp(axs, ylim=(-8, 0.2))


[ax.set_xlabel('u', size=14) for ax in axs[2]]
# [ax.set_ylabel(f'[{pref}]  log( P(d{suff}>u) )', size=14) for ax,pref,suff in zip(axs[:,0],['0D', '1D', '1D'],['','_max','_max'])]
[ax.set_ylabel(f'[{pref}]   log(p)', size=14) for ax,pref in zip(axs[:,0],['0D', '1D', '1D'])]
e1d.util.custom_legend(axs[0,0], colors=colors+['k','k'], labels=[f'n={nn}' for nn in ns1]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5])
e1d.util.custom_legend(axs[1,0], colors=colors, labels=[f'n={nn}' for nn in ns1], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
e1d.util.custom_legend(axs[2,0], colors=colors, labels=[f'FWHM={w}' for w in fwhms], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)

e1d.util.custom_legend(axs[0,1], colors=colors, labels=[f'n={nn*2}' for nn in ns2], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
e1d.util.custom_legend(axs[1,1], colors=colors, labels=[f'n={nn*2}' for nn in ns2], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
e1d.util.custom_legend(axs[2,1], colors=colors, labels=[f'FWHM={w}' for w in fwhms], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)

[ax.text(0.12, 1.02, f'FWHM = {fwhm}', transform=ax.transAxes)  for ax in axs[1]]
[ax.text(0.12, 1.02, f'n = {nn}', transform=ax.transAxes)  for ax,nn in zip(axs[2],[N1,2*N2])]

[ax.set_title(s)  for ax,s in zip(axs[0],['One-sample', 'Two-sample'])]

[ax.text(0.02, 1.02, f'({chr(97+i)})', transform=ax.transAxes) for i,ax in enumerate(axs.ravel())]


fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_sim.pdf' )
plt.savefig(fpath)

plt.show()






