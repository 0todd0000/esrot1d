
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import esrot1d as e1d



def d_1samp(y, mu=0):
    d  = ( y.mean() - mu ) / y.std(ddof=1)
    return d

def p_1samp(d, n):
    t = d / (1/n)**0.5
    v = n - 1
    p = stats.t.sf(t, v)
    return p



# calculate theoretical probabilities for effect sizes:
n      = [5, 10, 20]
u0     = np.linspace(0, 2, 51)
sf0    = np.array([[p_1samp(uu,nn) for uu in u0]  for nn in n])



# simulate:
np.random.seed(0)
u1     = np.arange(0, 2.1, 0.25)
niter  = 10000
sf1    = []
for nn in n:
    d  = []
    for i in range(niter):
        y  = np.random.randn(nn)
        d.append( d_1samp(y) )
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
ax.set_ylabel('P(d>u)', size=14)
e1d.util.custom_legend(ax, colors=colors+['k','k'], labels=[f'n={nn}' for nn in n]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5])
plt.tight_layout()
plt.show()





