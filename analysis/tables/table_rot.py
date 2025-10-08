
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import esrot1d as e1d
d2p = e1d.stats.d2p_onesample_0d


# calculate probabilities for effect sizes:
interps  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
labels,d = zip(*interps)
n        = [5, 12, 20, 100]
p        = np.array([[d2p(dd, nn) for dd in d]  for nn in n]) 

print( np.around(p,3).T )


