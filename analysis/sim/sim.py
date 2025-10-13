
import os
import numpy as np
from matplotlib import pyplot as plt
import rft1d
import esrot1d as e1d


def get_numerical_sf(d, u):
    d  = np.asarray( d )
    sf = np.array(   [(d>uu).mean()  for uu in u]   )
    sf[sf==0] = np.nan
    return sf



np.random.seed(0)
niter  = 10000
Q      = 101
fwhm   = 20
fwhms  = [5, 20, 50]
N1     = 15
N2     = 8
ns1    = [9, 19, 39]  # df:  8, 18, 38
ns2    = [5, 10, 20]  # df:  8, 18, 38
u      = np.arange(0, 2.1, 0.2)
u0     = np.linspace(0, 2, 51)


# one-sample 0d
sf10   = []
for n in ns1:
    d  = []
    for i in range(niter):
        y  = np.random.randn(n)
        d.append( e1d.stats.d_1sample(y) )
    sf10.append( get_numerical_sf(d, u) )
sf10    = np.array( sf10 )
sf10_an = np.array([[e1d.stats.d2p_1sample_0d(uu,nn) for uu in u0]  for nn in ns1])



# one-sample 1d (constant FWHM)
sf11n = []
for n in ns1:
    d  = []
    for i in range(niter):
        y  = rft1d.randn1d(n, Q, fwhm)
        d.append( e1d.stats.d_1sample(y).max() )
    sf11n.append( get_numerical_sf(d, u) )
sf11n    = np.array( sf11n )
sf11n_an = np.array([[e1d.stats.d2p_1sample_1d(uu,nn,Q,fwhm) for uu in u0]  for nn in ns1])


# one-sample 1d (constant n)
sf11w = []
for w in fwhms:
    d  = []
    for i in range(niter):
        y  = rft1d.randn1d(N1, Q, w)
        d.append( e1d.stats.d_1sample(y).max() )
    sf11w.append( get_numerical_sf(d, u) )
sf11w    = np.array( sf11w )
sf11w_an = np.array([[e1d.stats.d2p_1sample_1d(uu,N1,Q,w) for uu in u0]  for w in fwhms])




# two-sample 0d
sf20   = []
for n in ns2:
    d  = []
    for i in range(niter):
        y0  = np.random.randn(n)
        y1  = np.random.randn(n)
        d.append( e1d.stats.d_2sample(y0, y1) )
    sf20.append( get_numerical_sf(d, u) )
sf20    = np.array( sf20 )
sf20_an = np.array([[e1d.stats.d2p_2sample_0d(uu,nn*2) for uu in u0]  for nn in ns2])


# two-sample 1d  (constant FWHM)
sf21n  = []
for n in ns2:
    d  = []
    for i in range(niter):
        y0  = rft1d.randn1d(n, Q, fwhm)
        y1  = rft1d.randn1d(n, Q, fwhm)
        d.append( e1d.stats.d_2sample(y0, y1).max() )
    sf21n.append( get_numerical_sf(d, u) )
sf21n    = np.array( sf21n )
sf21n_an = np.array([[e1d.stats.d2p_2sample_1d(uu,nn*2,Q,fwhm) for uu in u0]  for nn in ns2])


# two-sample 1d  (constant n)
sf21w  = []
for w in fwhms:
    d  = []
    for i in range(niter):
        y0  = rft1d.randn1d(N2, Q, w)
        y1  = rft1d.randn1d(N2, Q, w)
        d.append( e1d.stats.d_2sample(y0, y1).max() )
    sf21w.append( get_numerical_sf(d, u) )
sf21w    = np.array( sf21w )
sf21w_an = np.array([[e1d.stats.d2p_2sample_1d(uu,N2*2,Q,w) for uu in u0]  for w in fwhms])



# save:
fpath = os.path.join( os.path.dirname(__file__), 'results_sim.h5' )
d     = dict(sf10=sf10, sf11w=sf11w, sf11n=sf11n, sf20=sf20, sf21w=sf21w, sf21n=sf21n)
d_an  = dict(sf10_an=sf10_an, sf11n_an=sf11n_an, sf11w_an=sf11w_an, sf20_an=sf20_an, sf21n_an=sf21n_an, sf21w_an=sf21w_an)
d.update( d_an )
e1d.io.save_h5(fpath, d)




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


# fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_sim.pdf' )
# plt.savefig(fpath)

plt.show()






