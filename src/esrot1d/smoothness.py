
'''
Smoothness metrics calculation and conversion

Basic estimations of the following two metrics are supported:

- Lipschitz-Killing curvature (LKC)
- Full-width at half-maximum (FWHM)

References:

Barnes GR, Ridgway GR, Flandin G, Woolrich M, Friston K (2013). Set-level threshold-free tests on the intrinsic volumes of SPMs. NeuroImage 68:133-40.
https://doi.org/10.1016/j.neuroimage.2012.11.046

Taylor JE, Worsley KJ (2007). Detecting sparse signals in random fields, with an application to brain mapping. Journal of the American Statistical Association 102(479):913-28.
https://doi.org/10.1198/016214507000000815

'''

from math import log
import numpy as np
eps    = np.finfo(float).eps
_4log2 = 4 * log(2)


def fwhm2lkc(fwhm, Q):
    resels = (Q - 1) / (fwhm+eps)     # use (Q-1) for point-based sampling;  use (Q) for element-based sampling
    return resels2lkc( resels )

def lkc2resels(lkc, d=1):  # Barnes 2013, Eqn.9 (in text after equation)
    return _4log2 **(-d/2) * lkc

def lkc2fwhm(lkc, Q):
    resels = lkc2resels(lkc)
    return (Q - 1) / (resels+eps)    # use (Q-1) for point-based sampling;  use (Q) for element-based sampling

def resels2lkc(resels, d=1):
    x = resels / ( _4log2 **(-d/2) )
    x = np.inf if (x > 1e9) else float(x)
    return x

def estimate_fwhm(e):
    lkc  = estimate_lkc( e )
    fwhm = lkc2fwhm(lkc, e.shape[1])
    return fwhm
    
def estimate_lkc(e):
    '''
    Lipschitz–Killing curvature, Taylor & Worsley (2007) Eqns.4-6
    '''
    u   = e / (e**2).sum(axis=0)**0.5            # eqn.5
    d   = np.diff(u, axis=1)
    lkc = (  (d**2).sum(axis=0)**0.5  ).sum()    # eqn.6
    return lkc