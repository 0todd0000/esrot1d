
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
N1     = 19
N2     = 10
ns1    = [9, 19, 39]  # df:  8, 18, 38
ns2    = [5, 10, 20]  # df:  8, 18, 38
u      = np.arange(0, 2.1, 0.2)



# one-sample 0d
sf10   = []
for n in ns1:
    d  = []
    for i in range(niter):
        y  = np.random.randn(n)
        d.append( e1d.stats.d_1sample(y) )
    sf10.append( get_numerical_sf(d, u) )
sf10   = np.array( sf10 )


# one-sample 1d (constant FWHM)
sf11f = []
for n in ns1:
    d  = []
    for i in range(niter):
        y  = rft1d.randn1d(n, Q, fwhm)
        d.append( e1d.stats.d_1sample(y).max() )
    sf11f.append( get_numerical_sf(d, u) )
sf11f   = np.array( sf11f )



# one-sample 1d (constant n)
sf11w = []
for w in fwhms:
    d  = []
    for i in range(niter):
        y  = rft1d.randn1d(N1, Q, w)
        d.append( e1d.stats.d_1sample(y).max() )
    sf11w.append( get_numerical_sf(d, u) )
sf11w   = np.array( sf11w )





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



# two-sample 1d  (constant FWHM)
sf21f  = []
for n in ns2:
    d  = []
    for i in range(niter):
        y0  = rft1d.randn1d(n, Q, fwhm)
        y1  = rft1d.randn1d(n, Q, fwhm)
        d.append( e1d.stats.d_2sample(y0, y1).max() )
    sf21f.append( get_numerical_sf(d, u) )
sf21f    = np.array( sf21f )



# two-sample 1d  (constant n)
sf21n  = []
for w in fwhms:
    d  = []
    for i in range(niter):
        y0  = rft1d.randn1d(N2, Q, w)
        y1  = rft1d.randn1d(N2, Q, w)
        d.append( e1d.stats.d_2sample(y0, y1).max() )
    sf21n.append( get_numerical_sf(d, u) )
sf21n    = np.array( sf21n )




plt.close('all')
fig,axs = plt.subplots( 3, 2, figsize=(8,8), tight_layout=True )
colors  = ['r', 'g', 'b']

for ax,sf in zip(axs[:,0], [sf10, sf11f, sf11w]):
    for i,c in enumerate(colors):
        # ax.plot(u0, np.log(sf0[i]), color=c )
        ax.plot(u, np.log(sf[i]), 'o', color=c )
    ax.set_ylim(-10, 0)
    # ax.set_xlabel('u', size=14)
    # ax.set_ylabel('log( P(d>u) )', size=14)
    # e1d.util.custom_legend(ax, colors=colors+['k','k'], labels=[f'n={nn}' for nn in n]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5])
    

for ax,sf in zip(axs[:,1], [sf20,sf21f,sf21n]):
    for i,c in enumerate(colors):
        # ax.plot(u0, np.log(sf0[i]), color=c )
        ax.plot(u, np.log(sf[i]), 'o', color=c )
    ax.set_ylim(-10, 0)


plt.tight_layout()

plt.show()






