
'''
Calculate effect size and its simple and functional interpretations
'''

import os,pathlib
import numpy as np
import matplotlib.pyplot as plt
import spm1d
import esrot1d as e1d


# load imported data:
dir0    = os.path.join( os.path.dirname(__file__), 'data' )
fpathH5 = os.path.join(dir0, 'means.h5')
d       = e1d.io.load_h5( fpathH5 )



# separate data into groups (right limb only;  results are similar for left-limb only)
# group 0:  healthy (group=0)
# group 1:  OA, month 0 (group=1, sess=0)
# group 2:  OA, month 6 (group=1, sess=1)
limb   = 1
y0     = d['y'][  (d['group']==0) & (d['limb']==limb) ]
oasubj = e1d.util.unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])


# conduct functional hypothesis test using SPM
spm    = spm1d.stats.ttest_paired( y2, y1 ).inference(0.05)
fwhm   = spm.fwhm


# calculate effect size and their probabilities:
y     = y2 - y1     # pairwise differences
n,Q   = y.shape     # sample size, domain size
d     = y.mean(axis=0) / y.std(ddof=1, axis=0)  # functional Cohen's d value
t     = e1d.stats.d2t(d, n, design='1sample')  # functional t-value (also calculated above using spm1d.stats.ttest_paired;  this is just a check)
# p0    = e1d.stats.d2p(-d, n, design)
# p1    = e1d.stats.d2p_1sample_1d(-d, n, Q, fwhm)
#
#
# calculate interpretations:
labels = ('Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge')
dth0   = (0.01, 0.2, 0.5, 0.8, 1.2, 2.0)  # d-value thresholds for 0D case
nn,ww  = 10, 25   # approximations from recommended guidelines;  see paper for a discussion
pth    = e1d.stats.d2p( dth0, nn, dim=0, design='1sample' )
dth1   = e1d.stats.p2d( pth, nn, dim=1, design='1sample', Q=Q, fwhm=ww )
#
# print( fwhm )
# print( d.min() )
# print( dth0 )
# print( np.around(dth1,3) )
#
#
#
# # plot:
# plt.close('all')
# fig,axs = plt.subplots( 2, 2, figsize=(8,6), tight_layout=True )
# ax0,ax1,ax2,ax3 = axs.ravel()
#
# ax0.plot( y1.T, color='r', lw=0.2 )
# ax0.plot( y2.T, color='c', lw=0.2 )
# ax0.plot( y0.mean(axis=0), color='k', lw=5, label='Healthy' )
# ax0.plot( y1.mean(axis=0), color='r', lw=5, label='OA, Month 0' )
# ax0.plot( y2.mean(axis=0), color='c', lw=5, label='OA, Month 6' )
# ax0.legend()
# ax0.set_xlabel('Time (%)')
# ax0.set_ylabel('Hip flexion (deg)')
#
#
#
# spm.plot( ax=ax1 )
# ax1.plot( t, 'r')
# ax1.set_xlabel('Time (%)', size=10)
# ax1.set_ylabel('t-value', size=10)
#
#
# ax2.plot( d )
# for dd0,dd1,ss in zip(dth0,dth1,labels[:3]):
#     ax2.axhline(-dd0, color='k', linestyle=':')
#     ax2.axhline(-dd1, color='r', linestyle=':')
# ax2.set_xlabel('Time (%)', size=10)
# ax2.set_ylabel('Effect size (d-value)', size=10)
#
#
#
# # ax3.plot( p0, label='Uncorrected' )
# # ax3.plot( p1, label='RFT-corrected' )
# ax3.plot( np.log(p0), label='Uncorrected' )
# ax3.plot( np.log(p1), label='RFT-corrected' )
# ax3.legend()
# # ax3.set_ylim(0, 0.2)
# ax3.set_xlabel('Time (%)', size=10)
# ax3.set_ylabel('log-probability', size=10)
#
#
# plt.show()







