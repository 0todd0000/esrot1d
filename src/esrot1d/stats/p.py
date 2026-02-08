
'''
Probability (and inverse probability) calculations

Note that conversions involving d-values require sample-size (n)
and not degrees of freedom (v) because n is required to
calculate t-values;  v is assumed to be n-2 for the two-sample case
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

# def _d2p_1sample_0d(d, n):
#     from collections.abc import Iterable
#     from . d import d2t
#     if isinstance(d, Iterable):
#         import numpy as np
#         return np.array( [_d2p_1sample_0d(dd, n)  for dd in d] )
#     t = d2t(d, n, design='1sample')
#     p = t2p(t, n-1, dim=0)
#     return p



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


# def _d2p_2sample_0d(d, n):
#     from . d import d2t
#     from collections.abc import Iterable
#     if isinstance(d, Iterable):
#         import numpy as np
#         return np.array( [_d2p_2sample_0d(dd, n)  for dd in d] )
#     t = d2t(d, n, design='2sample')
#     p = t2p(t, n-2)
#     # p = stats.t.sf(t, n-2)
#     return p


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
    if baseline is None:
        from .. baseline import BaselineScenario, CriticalValues
        pc  = BaselineScenario().pc  # critical p-values for the baseline scenario
    else:
        assert isinstance(baseline, BaselineScenario)
    d  = p2d(pc, n, dim=dim, design=design, Q=Q, fwhm=fwhm)
    return CriticalValues( d, pc )



    
if __name__ == '__main__':
    # print( p2t(0.05, 8, dim=0) )
    # print( p2t(0.05, 8, dim=1, Q=101, fwhm=50) )
    #
    # print( t2p(1.5, 8, dim=0) )
    # print( t2p(2.9, 8, dim=1, Q=101, fwhm=50) )
    

    # print( _d2p_1sample_0d(0.5, 10) )
    # print( _d2p_1sample_1d(0.5, 10, 101, 25) )
    # print( _d2p_2sample_0d(0.5, 20) )
    # print( _d2p_2sample_1d(0.5, 20, 101, 25) )
    #
    # print()
    # print( d2p(0.5, 10, dim=0, design='1sample') )
    # print( d2p(0.5, 10, dim=1, Q=101, fwhm=25, design='1sample') )
    # print( d2p(0.5, 20, dim=0, design='2sample') )
    # print( d2p(0.5, 20, dim=1, Q=101, fwhm=25, design='2sample') )


    # print( _p2d_1sample_0d(0.05, 20) )
    # print( _p2d_1sample_1d(0.05, 10, 101, 25) )
    # print( _p2d_2sample_0d(0.05, 20) )
    # print( _p2d_2sample_1d(0.05, 20, 101, 25) )
    #
    # print()
    # print( p2d(0.05, 20, dim=0, design='1sample') )
    # print( p2d(0.05, 10, dim=1, Q=101, fwhm=25, design='1sample') )
    # print( p2d(0.05, 20, dim=0, design='2sample') )
    # print( p2d(0.05, 20, dim=1, Q=101, fwhm=25, design='2sample') )
    
    
    # print()
    # print( d_critical( 19, dim=0, design='1sample' )  )
    # print( d_critical( 20, dim=0, design='2sample' )  )
    # print( d_critical( 19, dim=1, design='1sample', Q=101, fwhm=25 )  )
    # print( d_critical( 20, dim=1, design='2sample', Q=101, fwhm=25 )  )
    
    
    print( d_critical( 10, dim=1, design='1sample', Q=101, fwhm=25 )  )
    print( d_critical( 50, dim=1, design='1sample', Q=101, fwhm=25 )  )
    
    
    
    
    