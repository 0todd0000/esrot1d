
'''
Probability (and inverse probability) calculations including critical d-values given critical p-values

Conversions involving d-values require sample-size (n)
and not degrees of freedom (v);  v is assumed to
be n-2 for the two-sample case
'''


from .. dec import _assert_design, _check_n_2sample, _nd_vectorize





# ---- p2t conversions ----------
# convert p-values to t-values

@_nd_vectorize
def _p2t_0d(p, v):
    from scipy import stats
    return stats.t.isf(p, v)

@_nd_vectorize
def _p2t_1d(p, v, Q, fwhm):
    import rft1d
    return rft1d.t.isf(p, v, Q, fwhm)

@_nd_vectorize
def p2t(p, v, dim=0, Q=None, fwhm=None):
    if dim==0:
        return _p2t_0d(p, v)
    else:
        return _p2t_1d(p, v, Q, fwhm)



# ---- t2p conversions ----------
# convert t-values to p-values

def _t2p_0d(t, v):
    from scipy import stats
    return stats.t.sf(t, v)

def _t2p_1d(t, v, Q, fwhm):
    import rft1d
    return rft1d.t.sf(t, v, Q, fwhm)

@_nd_vectorize
def t2p(t, v, dim=0, Q=None, fwhm=None):
    if dim==0:
        return _t2p_0d(t, v)
    else:
        return _t2p_1d(t, v, Q, fwhm)



# ---- d2p conversions ----------
# convert d-values to p-values

def _d2p_1sample_0d(d, n):
    from . d import d2t
    t = d2t(d, n, design='1sample')
    p = t2p(t, n-1, dim=0)
    return p

def _d2p_1sample_1d(d, n, Q, fwhm):
    from . d import d2t
    t = d2t(d, n, design='1sample')
    p = t2p(t, n-1, dim=1, Q=Q, fwhm=fwhm)
    return p

def _d2p_2sample_0d(d, n):
    from . d import d2t
    t = d2t(d, n, design='2sample')
    p = t2p(t, n-2)
    return p

def _d2p_2sample_1d(d, n, Q, fwhm):
    from . d import d2t
    t  = d2t(d, n, design='2sample')
    p = t2p(t, n-2, dim=1, Q=Q, fwhm=fwhm)
    return p

@_nd_vectorize
@_assert_design
def d2p(d, n, dim=0, Q=None, fwhm=None, design='1sample'):
    if dim==0 and design=='1sample':
        return _d2p_1sample_0d(d, n)
    elif dim==0 and design=='2sample':
        return _d2p_2sample_0d(d, n)
    elif dim==1 and design=='1sample':
        return _d2p_1sample_1d(d, n, Q, fwhm)
    elif dim==1 and design=='2sample':
        return _d2p_2sample_1d(d, n, Q, fwhm)
        


# ---- p2d conversions ----------
# convert p-values to d-values

def _p2d_1sample_0d(p, n):
    from . d import t2d
    t  = p2t(p, n-1, dim=0)
    d  = t2d(t, n, design='1sample')
    return d

def _p2d_1sample_1d(p, n, Q, fwhm):
    from . d import t2d
    t  = p2t(p, n-1, dim=1, Q=Q, fwhm=fwhm)
    d  = t2d(t, n, design='1sample')
    return d

def _p2d_2sample_0d(p, n):
    from . d import t2d
    t  = p2t(p, n-2, dim=0)
    d  = t2d(t, n, design='2sample')
    return d

def _p2d_2sample_1d(p, n, Q, fwhm):
    from . d import t2d
    t  = p2t(p, n-2, dim=1, Q=Q, fwhm=fwhm)
    d  = t2d(t, n, design='2sample')
    return d

@_nd_vectorize
@_assert_design
def p2d(p, n, dim=0, Q=None, fwhm=None, design='1sample'):
    if dim==0 and design=='1sample':
        return _p2d_1sample_0d(p, n)
    elif dim==0 and design=='2sample':
        return _p2d_2sample_0d(p, n)
    elif dim==1 and design=='1sample':
        return _p2d_1sample_1d(p, n, Q, fwhm)
    elif dim==1 and design=='2sample':
        return _p2d_2sample_1d(p, n, Q, fwhm)
    


# ---- baseline conversions ----------
# calculate critical d-values for a given scenario based on an assumed baseline scenario


# @_assert_design
def d_critical(n, dim=0, design='1sample', Q=None, fwhm=None, baseline=None):
    _assert_design(design)
    from .. baseline import BaselineScenario, CriticalValues
    if baseline is None:
        baseline = BaselineScenario()
        p  = baseline.p  # critical p-values for the baseline scenario
    else:
        assert isinstance(baseline, BaselineScenario)
        p  = baseline.p
    d  = p2d(p, n, dim=dim, design=design, Q=Q, fwhm=fwhm)
    return CriticalValues( d, p, labels=baseline.labels )



    
if __name__ == '__main__':
    # print( p2t(0.05, 8, dim=0) )
    # print( p2t(0.05, 8, dim=1, Q=101, fwhm=50) )
    # print( t2p(1.5, 8, dim=0) )
    # print( t2p(2.9, 8, dim=1, Q=101, fwhm=50) )
    pass
