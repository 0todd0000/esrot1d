
'''
Conversions amongst effect size (Cohen's d-values), t-values
and p-values for the one- and two-sample cases under an
assumption of normality.

Function names are organized as:
    {x}2{y}_{design}_{n}d

where:
    {x} : input variable
    {y} : output variable
    {design} : experimental design ("onesample" or "twosample")
    {n} : dependent variable dimensionality (0 or 1)

For example, the function:

    d2p_onesample_0d

converts d-values to p-values for the one-sample, simple scalar
(i.e., 0D) case

Note that d2t and t2d conversion function names exclude the "_{n}d" suffix
because they do not depend on dependent variable dimensionality.
'''


import numpy as np



# --- one-sample case --------

def d_1sample(y, mu=0):
    d  = ( y.mean(axis=0) - mu ) / y.std(axis=0, ddof=1)
    return d


def d2t_onesample(d, n):
    return d / (1/n)**0.5


def d2p_onesample_0d(d, n):
    '''
    Calculate probabilty associated with Cohen's d value for the
    one-sample (or paired) case with a sample sizes of n
    '''
    from collections.abc import Iterable
    from scipy import stats
    if isinstance(d, Iterable):
        return np.array( [d2p_onesample_0d(dd, n)  for dd in d] )
    t = d2t_onesample(d, n)
    v = n - 1
    p = stats.t.sf(t, v)
    return p
    

def d2p_onesample_1d(d, n, Q, fwhm):
    import rft1d
    v  = n - 1
    u  = d2t_onesample(d, n)
    p  = rft1d.t.sf(u, v, Q, fwhm)
    return p


def p2d_onesample_1d(p, n, Q, fwhm):
    import rft1d
    v  = n - 1
    t  = rft1d.t.isf(p, v, Q, fwhm)
    d  = t2d_onesample(t, n)
    return d


def t2d_onesample(t, n):
    return t * (1/n)**0.5



# --- two-sample case --------

def d_2sample(y0, y1):
    n0,n1 = y0.shape[0], y1.shape[0]
    m0,m1 = y0.mean(axis=0), y1.mean(axis=0)
    v0,v1 = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
    sp    = (  (  (n0-1)*v0 + (n1-1)*v1  )  /  (n0+n1-2)  )**0.5
    return (m0 - m1) / sp
    

def d2p_twosample_0d(d, n):
    '''
    Calculate probabilty associated with Cohen's d value for the
    one-sample (or paired) case with a sample size of n
    '''
    from collections.abc import Iterable
    from scipy import stats
    if isinstance(d, Iterable):
        return np.array( [d2p_twosample_0d(dd, n)  for dd in d] )
    t = d2t_twosample(d, n)
    v = n - 2
    p = stats.t.sf(t, v)
    return p
    

def d2p_twosample_1d(d, n, Q, fwhm):
    import rft1d
    v  = n - 2
    u  = d2t_twosample(d, n)
    p  = rft1d.t.sf(u, v, Q, fwhm)
    return p

def d2t_twosample(d, n):
    return d / (1/(n/2) + 1/(n/2))**0.5

def p2d_twosample_1d(p, n, Q, fwhm):
    import rft1d
    v  = n - 2
    t  = rft1d.t.isf(p, v, Q, fwhm)
    d  = t2d_twosample(t, n)
    return d

def t2d_twosample(t, n):
    return t * (1/(n/2) + 1/(n/2))**0.5

