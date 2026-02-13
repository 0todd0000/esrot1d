
'''
Estimate smoothness metrics for the attached OA dataset:
- Lipschitz-Killing curvature (LKC)
- Full-width at half-maximum (FWHM)
'''

import os
import numpy as np
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


# calculate residuals:
y      = y2 - y1
r      = y - y.mean(axis=0)



lkc    = e1d.smoothness.estimate_lkc(r)
fwhm   = e1d.smoothness.estimate_fwhm(r)
print( f'Estimated LKC  = {lkc:.3f}')
print( f'Estimated FWHM = {fwhm:.3f}')


