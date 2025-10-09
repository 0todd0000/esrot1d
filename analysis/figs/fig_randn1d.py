
import os
import numpy as np
import matplotlib.pyplot as plt
import rft1d
import esrot1d as e1d


def scalar2color(x, cmap=plt.cm.jet, xmin=None, xmax=None):
    x          = np.asarray(x, dtype=float)
    if xmin is None:
        xmin   = x.min()
    if xmax is None:
        xmax   = x.max()
    xn         = (x - xmin)  / (xmax-xmin)
    xn        *= 255
    xn         = np.asarray(xn, dtype=int)
    colors     = cmap(xn)
    return colors

def float2str(x):
    return r'$\infty$' if np.isinf(x) else f'{x:.1f}'


#(0) Generate data:
seed        = [18]*5 + [0]
nResponses  = 8
nNodes      = 101
FWHM        = [0, 5, 10, 20, 50, np.inf]
LKC         = [e1d.smoothness.fwhm2lkc(x, nNodes)  for x in FWHM]


colors      = scalar2color(range(nResponses+3), cmap=plt.cm.PuRd)
Y           = []
for s,w in zip(seed,FWHM):
    np.random.seed(s)
    Y.append(rft1d.random.randn1d(nResponses, nNodes, w))



#(1) Plot results:
plt.close('all')
### create axes:
fig,axs     = plt.subplots(2, 3, figsize=(10,6), tight_layout=True)
### plot:
[ax.plot(yy, lw=0.8, color=c)   for ax,y in zip(axs.ravel(),Y) for yy,c in zip(y,colors[3:])]
[ax.hlines(0, 0, 100, color='k', linestyle='-', lw=2)  for ax in axs.ravel()]
plt.setp(axs, xlim=(0,100), ylim=(-4.5, 4.5))
### set ticklabels:
plt.setp(axs[0], xticklabels=[])
plt.setp(axs[:,1:], yticklabels=[])
### axes labels:
[ax.set_xlabel('Domain position  (%)')    for ax in axs[1]]
# [ax.set_ylabel('Continuum height')    for ax in (ax0,ax3)]
[ax.set_ylabel('Residual value')  for ax in axs[:,0]]
### panel labels:
for i,(ax,w,lkc) in enumerate(zip(axs.ravel(),FWHM,LKC)):
    s  = f'({chr(97+i)})  FWHM = {float2str(w)}\n      LKC = {float2str(lkc)}'
    ax.text(0.05, 0.87, s, transform=ax.transAxes)
plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig-randn1d.pdf'  )  )
plt.show()


