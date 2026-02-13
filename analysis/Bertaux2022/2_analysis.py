
'''
Preliminary analysis script conducting a paired t-test on the attached OA dataset.
These results are not directly related to effect size so are not reported in the main manuscript.
'''

import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import esrot1d as e1d


# load imported data:
dir0    = os.path.join( os.path.dirname(__file__), 'data' )
fpathH5 = os.path.join(dir0, 'means.h5')
d       = e1d.io.load_h5( fpathH5 )



# separate data into groups (right limb only;  results are similar for left-limb only)
# group 0:  healthy (group=0)
# group 1:  OA, month 0 (group=1, sess=0)
# group 2:  OA, month 6 (group=1, sess=1)
limb   = 1
y0     = d['y'][  (d['group']==0) & (d['limb']==limb) ]
oasubj = e1d.util.unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])


# conduct functional hypothesis test using SPM
spm    = spm1d.stats.ttest_paired( y2, y1 ).inference(0.05)



# plot:
plt.close('all')
fig,axs = plt.subplots( 1, 2, figsize=(8,3), tight_layout=True )
ax0,ax1 = axs

# plot summary statistics
ax0.plot( y1.T, color='r', lw=0.2 )
ax0.plot( y2.T, color='c', lw=0.2 )
ax0.plot( y0.mean(axis=0), color='k', lw=5, label='Healthy' )
ax0.plot( y1.mean(axis=0), color='r', lw=5, label='OA, Month 0' )
ax0.plot( y2.mean(axis=0), color='c', lw=5, label='OA, Month 6' )
ax0.legend()
ax0.set_xlabel('Time (%)')
ax0.set_ylabel('Hip flexion (deg)')

# plot spm results
spm.plot( ax=ax1 )
ax1.plot( spm.z, 'r')
ax1.set_xlabel('Time (%)', size=10)
ax1.set_ylabel('t-value', size=10)

plt.show()







