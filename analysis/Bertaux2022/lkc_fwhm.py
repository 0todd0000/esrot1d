
'''
Calculate smoothness metrics:
- Lipschitz-Killing curvature (LKC)
- Full-width at half-maximum (FWHM)

References:

Barnes GR, Ridgway GR, Flandin G, Woolrich M, Friston K (2013). Set-level threshold-free tests on the intrinsic volumes of SPMs. NeuroImage 68:133-40.
https://doi.org/10.1016/j.neuroimage.2012.11.046

Taylor JE, Worsley KJ (2007). Detecting sparse signals in random fields, with an application to brain mapping. Journal of the American Statistical Association 102(479):913-28.
https://doi.org/10.1198/016214507000000815

'''

import os
from math import log
import numpy as np
import esrot1d as e1d
_4log2 = 4 * log(2)


def fwhm2lkc(fwhm, Q):
    resels = (Q - 1) / fwhm     # use (Q-1) for point-based sampling;  use (Q) for element-based sampling
    return resels2lkc( resels )

def lkc2resels(lkc, d=1):  # Barnes 2013, Eqn.9 (in text after equation)
    return _4log2 **(-d/2) * lkc

def lkc2fwhm(lkc, Q):
    resels = lkc2resels(lkc)
    return (Q - 1) / resels    # use (Q-1) for point-based sampling;  use (Q) for element-based sampling

def resels2lkc(resels, d=1):
    return resels / ( _4log2 **(-d/2) )
    

def estimate_lkc(e):
    '''
    Lipschitz–Killing curvature, Taylor & Worsley (2007) Eqns.4-6
    '''
    u   = e / (e**2).sum(axis=0)**0.5            # eqn.5
    d   = np.diff(u, axis=1)
    lkc = (  (d**2).sum(axis=0)**0.5  ).sum()    # eqn.6
    return lkc


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



lkc    = estimate_lkc(r)
fwhm   = lkc2fwhm( lkc, r.shape[1] )
print( f'Estimated LKC  = {lkc:.3f}')
print( f'Estimated FWHM = {fwhm:.3f}')



