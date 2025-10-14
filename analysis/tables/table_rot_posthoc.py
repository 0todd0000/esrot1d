
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
import esrot1d as e1d


interps  = {
    'Very small'   : 0.01,
    'Small'        : 0.2,
    'Medium'       : 0.5,
    'Large'        : 0.8,
    'Very large'   : 1.2,
    'Huge'         : 2.0
}



# set THA dataset parameters:
n    = 52
Q    = 101
fwhm = 73.3


# calculate probabilities for all effect sizes:
p = [e1d.stats.d2p_1sample_0d(x, n)  for x in interps.values()]



# use fwhm=21.9% to find the functional dmax values whose probabilities match these p0 values
d    = [e1d.stats.p2d_twosample_1d(pp, n, Q, fwhm)  for pp in p]

print("Label       Cohen's d    Functional d    p-value   ")
print("-----------------------------------------------")
for (ss,dd0),pp,dd1 in zip(interps.items(),p,d):
    print( f'{ss:10}  {dd0:9}     {dd1:.2f}     {pp:.5f}      ' )