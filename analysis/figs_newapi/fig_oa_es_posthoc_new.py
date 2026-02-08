
import os,pathlib
import numpy as np
from matplotlib import pyplot as plt
import rft1d
import h5py
import esrot1d as e1d
e1d.set_plot_style()


# specify scenarios:
# dc0 = e1d.stats.d_critical(20, dim=0, design='2sample')  # baseline scenario

dc0 = e1d.stats.d_critical(20, dim=1, design='2sample', Q=101, fwhm=21.9)  # proposed baseline scenario
dc1 = e1d.stats.d_critical(20, dim=1, design='1sample', Q=101, fwhm=21.9)

dc2 = e1d.stats.d_critical(52, dim=1, design='2sample', Q=101, fwhm=21.9)
dc3 = e1d.stats.d_critical(52, dim=1, design='1sample', Q=101, fwhm=21.9)

dc4 = e1d.stats.d_critical(52, dim=1, design='2sample', Q=101, fwhm=73.3)
dc5 = e1d.stats.d_critical(52, dim=1, design='1sample', Q=101, fwhm=73.3)


# interpretations  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
# interpretations1 = [['Very small',0.13], ['Small',0.55], ['Medium',1.14], ['Large',1.75], ['Very large',2.59], ['Huge',4.13]]
#
# dc = e1d.stats.d_critical(20, dim=1, design='1sample', Q=101, fwhm=21.9)
# # dc = e1d.stats.d_critical(20, dim=1, design='1sample', Q=101, fwhm=73.3)
# dc = e1d.stats.d_critical(52, dim=1, design='2sample', Q=101, fwhm=73.3)

# interpretations1 = list( zip( dc.keys(), dc.values() ) )



def plot_interpretations(ax, dc, ylim=(-1,1)):
    ymin,ymax = ylim
    # interps   = interpretations if type=='0d' else interpretations1
    interps   = dc.tolist()
    labels    = [i[0] for i in interps]
    values    = [i[1] for i in interps]
    values   += [100]
    n         = len(values)
    colors    = plt.cm.hot( np.linspace(0, 1, n+5) )[2:-3]
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
fig,axs = plt.subplots(3, 2, figsize=(8,8), tight_layout=True)

dcs = [dc0, dc1, dc2, dc3, dc4, dc5]
for ax,dc in zip(axs.ravel(), dcs):
    ax.plot( d, color='k' )
    ax.axhline(0, color='k', ls=':')
    
    
    

    ylim = -0.3, 0.89
    plot_interpretations(ax, dc, ylim=ylim)
    # ax.legend( fontsize=12, loc='upper left' )
    ax.set_xlim(0, 100)
    # ax.set_xlabel('Time (%)', size=12)
    # ax.set_ylabel("Effect size (Cohen's d-value)", size=12)
    # # ax.grid(None)
    # label = 'Post hoc functional rules of thumb based on THA dataset'
    # ax.text(0.02, 0.95, label, transform=ax.transAxes, size=12)


# # plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig_oa_es_posthoc.pdf'  )  )
plt.show()






