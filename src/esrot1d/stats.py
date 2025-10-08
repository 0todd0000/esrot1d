
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


# # --- two-sample case --------
#
# def d2p_twosample_0d(d, n):
#     '''
#     Calculate probabilty associated with Cohen's d value for the
#     one-sample (or paired) case with a sample sizes of n
#     '''
#     from collections.abc import Iterable
#     from scipy import stats
#     if isinstance(d, Iterable):
#         return np.array( [d2p_twosample_0d(dd, n)  for dd in d] )
#     t = d2t_twosample(d, n)
#     v = 2*n - 2
#     p = stats.t.sf(t, v)
#     return p
#
#
# def d2p_twosample_1d(d, n, Q, fwhm):
#     import rft1d
#     v  = 2*n - 2
#     u  = d2t_twosample(d, n)
#     p  = rft1d.t.sf(u, v, Q, fwhm)
#     return p
#
# def d2t_twosample(d, n):
#     return d / (1/n + 1/n)**0.5
#
# def p2d_twosample_1d(p, n, Q, fwhm):
#     import rft1d
#     v  = 2*n - 2
#     t  = rft1d.t.isf(p, v, Q, fwhm)
#     d  = t2d_twosample(t, n)
#     return d
#
# def t2d_twosample(t, n):
#     return t * (1/n + 1/n)**0.5
