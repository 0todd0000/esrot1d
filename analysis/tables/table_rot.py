
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



# # calculate probabilities for effect sizes:
# interps  = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]
# labels,d = zip(*interps)
# n        = [5, 12, 20, 100]
# p        = np.array([[d2p(dd, nn) for dd in d]  for nn in n])
#
# print( np.around(p,3).T )


# find the minimum sample size n0 for which a ‘Large’ effect has a probability of less than α=0.05
d_medium  = interps['Large']
n         = 4
while e1d.stats.d2p_2sample_0d(d_medium, n) > 0.05:
    n += 2
print( f'Minimum sample size for significant LARGE effect: {n}' )

# calculate p-values for other effect sizes
p = [e1d.stats.d2p_2sample_0d(x, n)  for x in interps.values()]
    
    
# use fwhm=21.9% to find the functional dmax values whose probabilities match these p0 values
Q    = 101
fwhm = 21.9
d    = [e1d.stats.p2d_twosample_1d(pp, n, Q, fwhm)  for pp in p]

print("Label       Cohen's d    Functional d    p-value   ")
print("-----------------------------------------------")
for (ss,dd0),pp,dd1 in zip(interps.items(),p,d):
    print( f'{ss:10}  {dd0:9}     {dd1:.2f}     {pp:.3f}      ' )