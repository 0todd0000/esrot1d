
'''
Calculate effect size and its simple and functional interpretations
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import esrot1d as e1d
e1d.set_plot_style()



# calculate effect-size p-values for one-sample case:
interps  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
labels,d = zip(*interps)
# one-sample n-p relation:
n1       = np.arange(2,80)
p1       = np.array([[e1d.stats.d2p_1sample_0d(dd, nn) for dd in d]  for nn in n1]) 
# two-sample n-p relation:
n2       = np.arange(4,80,2)
p2       = np.array([[e1d.stats.d2p_2sample_0d(dd, nn) for dd in d]  for nn in n2]) 




# plot:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(10,4), tight_layout=True)
colors  = plt.cm.gray( np.linspace(0,1,10)  )[:6]

# one-sample case:
ax     = axs[0]
loc    = [(60,-0.2,0), (55,-1.1,-5), (50,-3.7,-30), (27,-4.1,-45), (15,-4.5,-61), (7.8,-3.9,-70)]
for pp,cc,ss,lc in zip(p1.T,colors,labels,loc): 
    ax.plot( n1, np.log10(pp), color=cc, lw=2, zorder=1 )
    x,y,a = lc
    ax.text(x, y, ss, rotation=a, color=cc)
vlines = [3, 4, 7, 13, 70]
dx     = [-0.5, 0, 0, 0, 0]
dy     = [0, 0, 0, 0, 1]
for vl,ddx,ddy in zip(vlines, dx, dy):
    ha = 'right' if vl==3 else 'left'
    ax.plot([vl,vl], [-15,np.log10(0.05)], color='r', ls=':', zorder=0)
    ax.text(vl+ddx, -4+ddy, fr'$n$ = {vl}', rotation=-90, ha=ha, va='top', color='r')
ax.axhline( np.log10(0.05), color='r', ls='--', label=r'$\alpha$=0.05', zorder=0)
ax.legend( bbox_to_anchor=(0.6,0.68), facecolor='w' )



# two-sample case:
ax     = axs[1]
loc    = [(60,-0.2,0), (65,-0.65,-3), (65,-1.7,-9), (60,-2.9,-19), (48,-4.6,-36), (22,-4.5,-55)]
for pp,cc,ss,lc in zip(p2.T,colors,labels,loc):
    ax.plot( n2, np.log10(pp), color=cc, lw=2, zorder=1 )
    x,y,a = lc
    ax.text(x, y, ss, rotation=a, color=cc)
vlines = [6, 10, 20, 46]
dy     = [0, 0, 1.5, 1.5, 0]
for ddy,vl in zip(dy,vlines):
    ax.plot([vl,vl], [-15,np.log10(0.05)], color='r', ls=':', zorder=0)
    ax.text(vl, -4+ddy, fr'$N$ = {vl}', rotation=-90, ha='left', va='top', color='r')
ax.axhline( np.log10(0.05), color='r', ls='--', label=r'$\alpha$=0.05', zorder=0)
ax.set_yticklabels([])



[ax.set_xlim( 0, 82 )  for ax in axs]
[ax.set_ylim( -5, 0.5 )  for ax in axs]
[ax.set_xlabel(f'Sample size (${nn}$)', size=12)  for ax,nn in zip(axs,['n','N'])]
axs[0].set_ylabel(r'log$_{10}$ ( p-value )', size=12)

panel_labels = '(a) One-sample', '(b) Two-sample'
[ax.text(0.02, 1.02, s, size=12, transform=ax.transAxes)  for ax,s in zip(axs,panel_labels)]
[ax.grid(None) for ax in axs]


# fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_dp.pdf' )
# plt.savefig(fpath)
plt.show()






