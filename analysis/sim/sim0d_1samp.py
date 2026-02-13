
import numpy as np
from matplotlib import pyplot as plt
import esrot1d as e1d




# calculate theoretical probabilities for effect sizes:
n      = [5, 10, 20]
u0     = np.linspace(0, 2, 51)
sf0    = np.array([[e1d.stats.d2p(uu,nn, dim=0, design='1sample') for uu in u0]  for nn in n])



# simulate:
np.random.seed(1)
u1     = np.arange(0, 2.1, 0.25)
niter  = 1000
sf1    = []
for nn in n:
    d  = []
    for i in range(niter):
        y  = np.random.randn(nn)
        d.append( e1d.stats.d_1sample(y) )
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





