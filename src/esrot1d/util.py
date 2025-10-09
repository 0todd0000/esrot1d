

import numpy as np


def float2str(x):
    return r'$\infty$' if np.isinf(x) else f'{x:.1f}'

def unique_sorted(x):
    return np.sort( np.unique(x) )
