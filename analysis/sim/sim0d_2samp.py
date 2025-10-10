
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import esrot1d as e1d
d2p = e1d.stats.d2p_2sample_0d



# calculate theoretical probabilities for effect sizes:
n      = [6, 10, 20]
# n      = [6, 11, 21]
# n      = [10, 20, 40]
u0     = np.linspace(0, 2, 51)
sf0    = np.array([[d2p(uu,nn) for uu in u0]  for nn in n])



# simulate:
np.random.seed(0)
u1     = np.arange(0, 2.1, 0.25)
niter  = 10000
sf1    = []
for nn in n:
    d  = []
    for i in range(niter):
        y0  = np.random.randn(int(nn/2))
        y1  = np.random.randn(int(nn/2))
        d.append( e1d.stats.d_2sample(y0, y1) )
    d  = np.asarray( d )
    f  = np.array(   [(d>uu).mean()  for uu in u1]   )
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
ax.set_ylabel('log( P(d>u) )', size=14)
e1d.util.custom_legend(ax, colors=colors+['k','k'], labels=[f'n={nn}' for nn in n]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5])
plt.tight_layout()
plt.show()
