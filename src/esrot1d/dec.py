
'''
Decorator class definitions
'''

import numpy as np




class _assert_design(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, x, n, *args, design='1sample', **kwargs):
        if design not in ['1sample', '2sample']:
            raise ValueError( f'Unknown design: "{design}". Only "1sample" and "2sample" supported.' )
        return self.f(x, n, *args, design=design, **kwargs)



class _check_n_2sample(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, d, n):
        if n%2 !=0:
            raise ValueError( f'Unsupported sample size: n = {n}. If just one sample size value is provided for a 2-sample design it must represent the total sample size and thus be divisible by 2.')
        return self.f(d, n)
        

class _nd_vectorize(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, a, b, *args, **kwargs):
        from collections.abc import Iterable
        ia  = isinstance(a, Iterable)
        ib  = isinstance(b, Iterable)
        if ia:
            a = np.ravel(a)
        if ib:
            b = np.ravel(b)
        
        if ia and ib:
            x = np.array(  [[self.f(aa, bb, *args, **kwargs)  for aa in a] for bb in b]  )
        elif ia:
            x = np.array(  [self.f(aa, b, *args, **kwargs)  for aa in a]  )
        elif ib:
            x = np.array(  [self.f(a, bb, *args, **kwargs)  for bb in b]  )
        else:
            x = float( self.f(a, b, *args, **kwargs) )
        return x



