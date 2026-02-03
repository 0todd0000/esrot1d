
import os,pathlib
import numpy as np
from matplotlib import pyplot as plt
import rft1d
import h5py
import esrot1d as e1d
e1d.set_plot_style()



interpretations  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
interpretations1 = [['Very small',0.58], ['Small',0.76], ['Medium',1.03], ['Large',1.32], ['Very large',1.73], ['Huge',2.62]]




def plot_interpretations(ax, type='0d', ylim=(-1,1)):
    ymin,ymax = ylim
    interps   = interpretations if type=='0d' else interpretations1
    labels    = [i[0] for i in interps]
    values    = [i[1] for i in interps]
    values   += [100]
    n         = len(values)
    colors    = plt.cm.hot( np.linspace(0, 1, n+2) )[2:]
    # oy        = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    for i,(s,c) in enumerate( zip(labels,colors) ):
        if values[i] < ymax:
            ax.axhline(values[i], color=c, ls='-', zorder=0)
            bbox = dict(facecolor='w', edgecolor="0.5", pad=2, alpha=0.6)
            ax.text( 80, values[i]+0.01, s, color=c, bbox=bbox, size=12 )
        # if values[i] < -ymin:
        #     ax.axhline(-values[i], color=c, ls='-', zorder=0)
    ax.set_ylim( -0.3, ymax )




# load imported data:
dirREPO = pathlib.Path( __file__ ).parent.parent.parent
dir0    = os.path.join(dirREPO, 'analysis', 'Bertaux2022', 'data')
fpathH5 = os.path.join(dir0, 'means.h5')
d       = dict()
with h5py.File(fpathH5, 'r') as f:
    for k in f.keys():
        d[k] = np.array(f[k])



# separate data into groups (right limb only;  results are similar for left-limb only)
# group 0:  healthy (group=0)
# group 1:  OA, month 0 (group=1, sess=0)
# group 2:  OA, month 6 (group=1, sess=1)
limb   = 1
y0     = d['y'][  (d['group']==0) & (d['limb']==limb) ]
oasubj = e1d.util.unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])

d      = e1d.stats.d_1sample(y1 - y2)





# PLOT:
plt.close('all')
fig,axs = plt.subplots(1, 2, figsize=(10,4))

axs[0].plot( d, color='k' )
axs[1].plot( d, color='k' )
[ax.axhline(0, color='k', ls=':')  for ax in axs]

ylim = -0.3, 0.89
plot_interpretations(axs[0], type='0d', ylim=ylim)
plot_interpretations(axs[1], type='1d', ylim=ylim)
# ax.legend( fontsize=12, loc='upper left' )
axs[1].set_yticklabels([])
[ax.set_xlim(0, 100)  for ax in axs]
[ax.set_xlabel('Time (%)', size=12)  for ax in axs]
axs[0].set_ylabel("Effect size (Cohen's d-value)", size=12)
# ax.grid(None)
labels = 'Sawilowsky (2009) rules of thumb', 'Proposed functional rules of thumb'
[ax.text(0.02, 0.95, f'({chr(97+i)}) {s}', transform=ax.transAxes, size=12)   for i,(ax,s) in enumerate(zip(axs,labels))]

plt.tight_layout()
# plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig_oa_es.pdf'  )  )
plt.show()






