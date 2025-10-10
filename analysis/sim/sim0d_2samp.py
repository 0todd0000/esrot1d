
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import esrot1d as e1d



def d_2samp(y0, y1):
    n0,n1 = y0.shape[0], y1.shape[0]
    m0,m1 = y0.mean(axis=0), y1.mean(axis=0)
    v0,v1 = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
    sp    = (  (  (n0-1)*v0 + (n1-1)*v1  )  /  (n0+n1-2)  )**0.5
    return (m0 - m1) / sp
    

def p_2samp(d, n):
    t = d / (1/(n/2) + 1/(n/2))**0.5
    v = n - 2
    p = stats.t.sf(t, v)
    return p



# calculate theoretical probabilities for effect sizes:
n      = [6, 10, 20]
# n      = [6, 11, 21]
# n      = [10, 20, 40]
u0     = np.linspace(0, 2, 51)
sf0    = np.array([[p_2samp(uu,nn) for uu in u0]  for nn in n])



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
        d.append( d_2samp(y0, y1) )
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
