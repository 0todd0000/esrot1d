
import os,pathlib
import numpy as np
from matplotlib import pyplot as plt
import rft1d
import h5py
import esrot1d as e1d
e1d.set_plot_style()



def plot_interpretations(ax, dc, ymax=None):
    ymax      = 1e6 if (ymax is None) else ymax
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



# specify scenarios:
# dc0 = e1d.stats.d_critical(20, dim=0, design='2sample')  # baseline scenario
ns      = [20, 20,   52, 52,   52, 52]
designs = ['2sample', '1sample'] * 3
fwhms   = [21.9, 21.9,   21.9, 21.9,   73.3, 73.3]



# plot:
plt.close('all')
fig,axs = plt.subplots(3, 2, figsize=(8,8), tight_layout=True)


for i,(ax,n,design,fwhm) in enumerate( zip(axs.ravel(), ns, designs, fwhms) ):
    dc = e1d.stats.d_critical(n, dim=1, design=design, Q=101, fwhm=fwhm)  # proposed baseline scenario
    ax.plot( d, color='k' )
    ax.axhline(0, color='k', ls=':')
    

    
    plot_interpretations(ax, dc, ymax=0.8)
    # ax.legend( fontsize=12, loc='upper left' )
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.3, 0.93)
    
    ax.text(0.02, 0.93, f'({chr(97+i)})  n={n}, {design}, fwhm={fwhm}%', transform=ax.transAxes)




axs[0,0].text(0.03, 0.78, 'PROPOSED BENCHMARK SCENARIO', transform=axs[0,0].transAxes, fontweight='bold') 
axs[2,1].text(0.03, 0.83, 'ACTUAL SCENARIO', transform=axs[2,1].transAxes, fontweight='bold') 

# [ax.text(0.1, 0.83, label, transform=ax.transAxes, fontweight='bold')  for ax,label in zip([axs[0,0], axs[2,1]], labels)]

[ax.set_xlabel('Time (%)', size=12) for ax in axs[2]]
[ax.set_ylabel('Effect size', size=12)  for ax in axs[:,0]]
# [ax.set_ylabel(f'{s}\nEffect size', size=12)  for ax,s in zip(axs[:,0], ['n=20, fwhm=21.9%', 'n=52, fwhm=21.9%', 'n=52, fwhm=73.3%'])]
[ax.set_xticklabels([])   for ax in axs[:2].ravel()]
[ax.set_yticklabels([])   for ax in axs[:,1]]

[ax.set_title(s)  for ax,s in zip(axs[0], ['2-sample', '1-sample'])]


plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig_oa_es_posthoc.pdf'  )  )
plt.show()






