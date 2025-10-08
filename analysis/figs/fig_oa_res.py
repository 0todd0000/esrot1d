
'''
Calculate effect size and its simple and functional interpretations
'''

import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import h5py
import spm1d



def unique_sorted(x):
    return np.sort( np.unique(x) )




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
oasubj = unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])


# calculate residuals:
y      = y2 - y1
r      = y - y.mean(axis=0)



# plot:
plt.close('all')
plt.figure(figsize=(6,4))
ax = plt.axes()
ax.plot( r.T, color='b', lw=0.5 )
ax.axhline(0, color='k', ls='--')
# ax.legend()
ax.set_xlabel('Time (%)', size=12)
ax.set_ylabel('Residual (deg)', size=12)
plt.tight_layout()
fpath = os.path.join( os.path.dirname(__file__), 'pdf', 'fig_oa_res.pdf' )
plt.savefig(fpath)
plt.show()







