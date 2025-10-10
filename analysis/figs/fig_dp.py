
'''
Calculate effect size and its simple and functional interpretations
'''

import os
import numpy as np
import matplotlib.pyplot as plt
import esrot1d as e1d



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
loc    = [(25,-0.4,0), (25,-1.8,-5), (25,-5.3,-22), (25,-9.1,-40), (23,-14.5,-58), (14.5,-14.5,-67)]
for pp,cc,ss,lc in zip(p1.T,colors,labels,loc): 
    ax.plot( n1, np.log(pp), color=cc, lw=2, zorder=1 )
    x,y,a = lc
    ax.text(x, y, ss, rotation=a, color=cc)
vlines = [3, 4, 7, 13, 70]
dx     = [-0.5, 0, 0, 0, 0]
dy     = [0, 0, 0, 2, 0]
for vl,ddx,ddy in zip(vlines, dx, dy):
    ha = 'right' if vl==3 else 'left'
    ax.plot([vl,vl], [-15,np.log(0.05)], color='r', ls=':', zorder=0)
    ax.text(vl+ddx, -11+ddy, fr'$n$ = {vl}', rotation=-90, ha=ha, va='top', color='r')
ax.axhline( np.log(0.05), color='r', ls='--', label=r'$\alpha$=0.05', zorder=0)
ax.legend( bbox_to_anchor=(0.5,0.78) )



# two-sample case:
ax     = axs[1]
loc    = [(60,-0.4,0), (70,-1.5,-2), (70,-4.0,-7), (60,-6.7,-18), (50,-10.9,-25), (32,-14.1,-49)]
for pp,cc,ss,lc in zip(p2.T,colors,labels,loc):
    ax.plot( n2, np.log(pp), color=cc, lw=2, zorder=1 )
    x,y,a = lc
    ax.text(x, y, ss, rotation=a, color=cc)
vlines = [6, 10, 20, 46]
for vl in vlines:
    ax.plot([vl,vl], [-15,np.log(0.05)], color='r', ls=':', zorder=0)
    ax.text(vl, -11, fr'$n$ = {vl}', rotation=-90, ha='left', va='top', color='r')
ax.axhline( np.log(0.05), color='r', ls='--', label=r'$\alpha$=0.05', zorder=0)
ax.set_yticklabels([])



[ax.set_xlim( 0, 82 )  for ax in axs]
[ax.set_ylim( -15, 0.5 )  for ax in axs]
[ax.set_xlabel(f'Sample size ($n$)', size=12)  for ax in axs]
axs[0].set_ylabel('log( p-value )', size=12)

panel_labels = '(a) One-sample', '(b) Two-sample'
[ax.text(0.02, 1.02, s, size=12, transform=ax.transAxes)  for ax,s in zip(axs,panel_labels)]



fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_dp.pdf' )
plt.savefig(fpath)
plt.show()






