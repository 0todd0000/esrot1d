
'''
Ensure that key functions return appropriate output argument types
and array sizes for four different input argument type possibilities.

The wrapped function must be of the form:

    def fn(a, b, **kwargs):
        pass

The four possibilities are:

1. "a" scalar and "b"  scalar
2. "a" iterable and "b" scalar
3. "a" scalar and "b" iterable
4. "a" iterable and "b" iterable
'''


import pytest
import numpy as np
import esrot1d as e1d


darray = np.array([0.01, 0.2, 0.5, 0.8, 1.2, 2.0])
narray = [6, 10, 30]
Q      = 101
fwhm   = 20

# d,n,dim,design,_type,shape
cases = [
    (0.5, 20, 0, '1sample', float, None),
    (0.5, narray, 0, '1sample', np.ndarray, (3,)),
    (0.5, list(narray), 0, '1sample', np.ndarray, (3,)),
    (0.5, tuple(narray), 0, '1sample', np.ndarray, (3,)),
    (darray, 20, 0, '1sample', np.ndarray, (6,)),
    (list(darray), 20, 0, '1sample', np.ndarray, (6,)),
    (tuple(darray), 20, 0, '1sample', np.ndarray, (6,)),
    (darray, narray, 0, '1sample', np.ndarray, (3,6)),

    (0.5, 20, 0, '2sample', float, None),
    (0.5, narray, 0, '2sample', np.ndarray, (3,)),
    (darray, 20, 0, '2sample', np.ndarray, (6,)),
    (darray, narray, 0, '2sample', np.ndarray, (3,6)),

    (0.5, 20, 1, '1sample', float, None),
    (0.5, narray, 1, '2sample', np.ndarray, (3,)),
    (darray, 20, 1, '2sample', np.ndarray, (6,)),
    (darray, narray, 1, '2sample', np.ndarray, (3,6)),
    
]





def test_d2t():
    for (d,n,_,design,_type,shape) in cases:
        x   = e1d.stats.d2t(d, n, design=design)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape

def test_d2p():
    for (d,n,dim,design,_type,shape) in cases:
        q,w = (Q,fwhm) if (dim==1) else (None,None)
        x   = e1d.stats.d2p(d, n, dim=dim, design=design, Q=q, fwhm=w)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape


def test_p2d():
    for (d,n,dim,_,_type,shape) in cases:
        q,w = (Q,fwhm) if (dim==1) else (None,None)
        x   = e1d.stats.p2d(d, n, dim=dim, Q=q, fwhm=w)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape

def test_p2t():
    for (d,n,dim,_,_type,shape) in cases:
        q,w = (Q,fwhm) if (dim==1) else (None,None)
        x   = e1d.stats.p2t(d, n, dim=dim, Q=q, fwhm=w)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape


def test_t2d():
    for (d,n,_,design,_type,shape) in cases:
        x   = e1d.stats.t2d(d, n, design=design)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape

def test_t2p():
    for (d,n,dim,_,_type,shape) in cases:
        q,w = (Q,fwhm) if (dim==1) else (None,None)
        x   = e1d.stats.t2p(d, n, dim=dim, Q=q, fwhm=w)
        assert isinstance(x, _type)
        if _type == np.ndarray:
            assert x.shape == shape





