
'''
Calculate d-values for 1- and 2-sample designs and convert between t- and d-values

* d_1sample(y)      # d-value for 1-sample case
* d_2sample(y0,y1)  # d-value for 2-sample case
* d2t(d,n)          # convert d- to t-values
* t2d(t,n)          # convert t- to d-values
'''



import numpy as np
from .. dec import _assert_design, _check_n_2sample, _nd_vectorize


def _isint(x): # check whether input argument is an integer
    return isinstance(x, (int, np.integer))



# ----- private functions ----------

@_nd_vectorize
def _d2t_1sample(d, n):
    return d / (1/n)**0.5

@_nd_vectorize
@_check_n_2sample
def _d2t_2sample(d, n):
    n0,n1 = (n/2, n/2) if _isint(n) else n 
    return d / (1/n0 + 1/n1)**0.5

@_nd_vectorize
def _t2d_1sample(t, n):
    return t * (1/n)**0.5

@_nd_vectorize
@_check_n_2sample
def _t2d_2sample(t, n):
    n0,n1 = (n/2, n/2) if _isint(n) else n 
    return t * (1/n0 + 1/n1)**0.5



# ----- public API ----------


def d_1sample(y, mu=0):
    y  = np.asarray(y, dtype=float)
    d  = ( y.mean(axis=0) - mu ) / y.std(axis=0, ddof=1)
    return d

def d_2sample(y0, y1):
    y0,y1 = [np.asarray(yy, dtype=float)  for yy in (y0,y1)]
    n0,n1 = y0.shape[0], y1.shape[0]
    m0,m1 = y0.mean(axis=0), y1.mean(axis=0)
    v0,v1 = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
    sp    = (  (  (n0-1)*v0 + (n1-1)*v1  )  /  (n0+n1-2)  )**0.5
    return (m0 - m1) / sp
    
@_assert_design
def d2t(d, n, design='1sample'):
    if design == '1sample':
        return _d2t_1sample(d, n)
    elif design == '2sample':
        return _d2t_2sample(d, n)

@_assert_design
def t2d(t, n, design='1sample'):
    if design == '1sample':
        return _t2d_1sample(t, n)
    elif design == '2sample':
        return _t2d_2sample(t, n)




if __name__ == '__main__':
    # d  = 2
    # n  = 20
    # t  = _d2t_2sample(d, n)
    # d1 = _t2d_2sample(t, n)
    # print( d, t, d1 )
    
    d  = 2
    n  = 20
    t  = d2t(d, n, design='2sample')
    d1 = t2d(t, n, design='2sample')
    print( d, t, d1 )
    
    
    
