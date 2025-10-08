
import os
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import rft1d


plt.style.use('bmh')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family']     = 'Arial'

colors = ['#348ABD', '#A60628', '#7A68A6', '#467821', '#D55E00', '#CC79A7', '#56B4E9', '#009E73', '#F0E442', '#0072B2']
interpretations = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]


def custom_legend(ax, colors=None, labels=None, linestyles=None, linewidths=None, markerfacecolors=None, markersizes=None, **kwdargs):
    n      = len(colors)
    if linestyles is None:
        linestyles = ['-']*n
    if linewidths is None:
        linewidths = [1]*n
    if markerfacecolors is None:
        markerfacecolors = colors
    if markersizes is None:
        markersizes = [None]*n
    x0,x1  = ax.get_xlim()
    y0,y1  = ax.get_ylim()
    h      = [ax.plot([x1+1,x1+2,x1+3], [y1+1,y1+2,y1+3], ls, color=color, linewidth=lw, markerfacecolor=mfc, ms=ms)[0]   for color,ls,lw,mfc,ms in zip(colors,linestyles,linewidths,markerfacecolors,markersizes)]
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    return ax.legend(h, labels, **kwdargs)


def cohen_d(y0, y1):
    n0,n1 = y0.shape[0], y1.shape[0]
    m0,m1 = y0.mean(axis=0), y1.mean(axis=0)
    v0,v1 = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
    sp    = (  (  (n0-1)*v0 + (n1-1)*v1  )  /  (n0+n1-2)  )**0.5
    return (m0 - m1) / sp

def p_effect(d, n):
    # 1-sample:
    # v      = 2*n -2
    # t      = d * sqrt(n)
    # 2-sample:
    v      = 2*n -2
    t      = d / (1.0/n + 1.0/n)**0.5
    return stats.t.sf(t, v)


def p_effect_mv(d, n, ndv=1):
    v      = 2*n -2
    t      = d / (1.0/n + 1.0/n)**0.5
    pu     = stats.t.sf(t, v)     # uncorrected p value
    p      = 1 - ( 1 - pu )**ndv  # corrected p value (Bonferroni)
    p      = max(0, min(1, p))    # constrain to the range [0,1]
    return p


def calc_interpretation(n):
    _,d = zip(*interpretations)
    p   = np.array(  [[p_effect(dd, nn) for dd in d]  for nn in n]  )
    return d,p

def calc_theoretical(n):
    d   = np.linspace(0.01, 2, 51)
    p   = np.array(  [[p_effect(dd, nn) for dd in d]  for nn in n]  )
    return d,p
    

def calc_sim_single_n(n, niter=1000, u=np.linspace(0.01, 2, 51)):
    d = []
    for i in range(niter):
        y0 = np.random.randn(n)
        y1 = np.random.randn(n)
        d.append( cohen_d(y0,y1) )
    d = np.asarray( d )
    p = np.array(   [(d>uu).mean()  for uu in u]   )
    return u, p

def calc_sim(n, niter=1000, u=np.linspace(0.01, 2, 51)):
    p = np.array([calc_sim_single_n(nn, niter=niter, u=u)[1]  for nn in n])
    return u,p




def calc_interpretation_mv(m, n=10):
    _,d = zip(*interpretations)
    p   = np.array(  [[p_effect_mv(dd, n, ndv=mm) for dd in d]  for mm in m]  )
    return d,p


def calc_theoretical_mv(m, n=10):
    d   = np.linspace(0.01, 2, 51)
    p   = np.array(  [[p_effect_mv(dd, n, ndv=mm) for dd in d]  for mm in m]  )
    return d,p


def calc_sim_single_m_mv(m, n=10, niter=1000, u=np.linspace(0.01, 2, 51)):
    d = []
    for i in range(niter):
        dd = []
        for ii in range(m):
            y0 = np.random.randn(n)
            y1 = np.random.randn(n)
            dd.append( cohen_d(y0,y1) )
        d.append( max(dd) )
    d = np.asarray( d )
    p = np.array(   [(d>uu).mean()  for uu in u]   )
    return u, p

def calc_sim_mv(m, n=10, niter=1000, u=np.linspace(0.01, 2, 51)):
    p = np.array([calc_sim_single_m_mv(mm, n=n, niter=niter, u=u)[1]  for mm in m])
    return u,p


#(0) Calculate probabilities for effect sizes:
np.random.seed(0)
n         = [10, 30, 100]
di,pi     = calc_interpretation(n)
dt,pt     = calc_theoretical(n)
ds,ps     = calc_sim(n, niter=1000, u=np.linspace(0.05, 1.9, 15))

m         = [1, 3, 10]
dim,pim   = calc_interpretation_mv(m, n=10)
dtm,ptm   = calc_theoretical_mv(m, n=10)
dsm,psm   = calc_sim_mv(m, n=10, niter=1000, u=np.linspace(0.05, 1.9, 15))





#(1) Plot:
plt.close('all')
fig,(ax0,ax1) = plt.subplots(1, 2, figsize=(12,4))


# plot d probabilities:
ax      = ax0
for ppt,pps,ppi,cc in zip(pt,ps,pi,colors):
    ax.plot(dt, ppt, '-', color=cc)
    ax.plot(ds, pps, 'o', color=cc, ms=5, mfc='w')
    ax.plot(di, ppi, 'o', color=cc, ms=9)
ax.set_xlabel("Cohen's d", size=14)
ax.set_ylabel('Probability', size=14)


# plot interpretation labels:
labelsi,_ = zip(*interpretations)
# ox,oy     = -0.01, 0.03
# for xx,pp,ss in zip(di,pi[0],labelsi):
#     ax.text( xx+ox , pp+oy, ss, size=11 )
ox,oy     = [0.03, 0.03, 0.03, 0.01, 0.01, 0.01], [0.03, 0.03, 0.04, 0.06, 0.06, 0.06]
ha        = ['left']*5 + ['right']
for xx,oxx,oyy,pp,ss,haa in zip(di,ox,oy,pi[0],labelsi,ha):
    ax.text( xx+oxx , pp+oyy, ss, size=10, name='Arial', ha=haa, bbox=dict(facecolor='w', edgecolor="0.5", pad=3) )


# custom legend:
lcolors = colors[:3] + ['k', 'k']
llabels = [f'Theoretical $(N = {nn})$'  for nn in n] + ['Simulated', 'Interpretation']
lls     = ['-', '-', '-', 'o', 'o']
llw     = [2, 2, 2, 1, 1]
lmfc    = [None, None, None, 'w', 'k']
lms     = [None, None, None, 5, 9]
custom_legend(ax, colors=lcolors, labels=llabels, linestyles=lls, linewidths=llw, markerfacecolors=lmfc, markersizes=lms)


# plot d probabilities (multivariate):
ax = ax1
for ppt,pps,ppi,cc in zip(ptm,psm,pim,colors):
    ax.plot(dtm, ppt, '-', color=cc)
    ax.plot(dsm, pps, 'o', color=cc, ms=5, mfc='w')
    ax.plot(dim, ppi, 'o', color=cc, ms=9)


# plot interpretation labels:
labelsi,_ = zip(*interpretations)
ox,oy     = [0.03, 0.03, 0.03, 0.01, 0.01, 0.01], [0.03, 0.03, 0.04, 0.13, 0.13, 0.06]
ha        = ['left']*5 + ['right']
for xx,oxx,oyy,pp,ss,haa in zip(dim,ox,oy,pim[0],labelsi,ha):
    ax.text( xx+oxx , pp+oyy, ss, size=10, name='Arial', ha=haa, bbox=dict(facecolor='w', edgecolor="0.5", pad=3) )


# custom legend:
lcolors = colors[:3] + ['k', 'k']
llabels = [f'Theoretical $(M = {mm})$'  for mm in m] + ['Simulated', 'Interpretation']
lls     = ['-', '-', '-', 'o', 'o']
llw     = [2, 2, 2, 1, 1]
lmfc    = [None, None, None, 'w', 'k']
lms     = [None, None, None, 5, 9]
custom_legend(ax, colors=lcolors, labels=llabels, linestyles=lls, linewidths=llw, markerfacecolors=lmfc, markersizes=lms)


ax.set_xlabel("Cohen's d", size=14)
ax.set_yticklabels([])


panel_labels = ['(a)  Sample size ( $N$ ) dependence;   $M=1$', '(b) Dependent variable count ( $M$ ) dependence;   $N=10$']
[ax.text(0.0, 1.08, s, size=14, transform=ax.transAxes)   for ax,s in zip([ax0,ax1], panel_labels)]

plt.setp([ax0,ax1], ylim=(-0.03, 1.03))


plt.tight_layout()
plt.show()


# plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig1-sim.pdf'  )  )