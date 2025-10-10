
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import rft1d
import esrot1d as e1d



def d_1samp_1d(y, mu=0):
    d  = ( y.mean(axis=0) - mu ) / y.std(axis=0, ddof=1)
    return d

def p_1samp_1d(dmax, n, Q, fwhm):
    tmax = dmax / (1/n)**0.5
    v    = n - 1
    p    = rft1d.t.sf(tmax, v, Q, fwhm)
    return p


Q      = 101
fwhm   = 20



# calculate theoretical probabilities for effect sizes:
n      = [5, 10, 20]
u0     = np.linspace(0, 2, 51)
sf0    = np.array([[p_1samp_1d(uu,nn,Q,fwhm) for uu in u0]  for nn in n])



# simulate:
np.random.seed(0)
u1     = np.arange(0, 2.1, 0.25)
niter  = 10000
sf1    = []
for nn in n:
    d  = []
    for i in range(niter):
        y  = rft1d.randn1d(nn, Q, fwhm)
        d.append( d_1samp_1d(y).max() )
    dmax = np.asarray( d )
    f    = np.array(   [(dmax>uu).mean()  for uu in u1]   )
    f[f==0] = np.nan
    sf1.append( f )
sf1    = np.array( sf1 )



# plot:
plt.close('all')
ax      = plt.axes()
colors  = ['r', 'g', 'b']
for i,c in enumerate(colors):
    ax.plot(u0, np.log(sf0[i]), color=c )
    ax.plot(u1, np.log(sf1[i]), 'o', color=c )
ax.set_ylim(-10, 0)
ax.set_xlabel('u', size=14)
ax.set_ylabel('log( P(dmax > u) )', size=14)
e1d.util.custom_legend(ax, colors=colors+['k','k'], labels=[f'n={nn}' for nn in n]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5])
plt.tight_layout()
plt.show()





