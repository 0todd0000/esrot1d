
'''
Calculate within-subject means for between-subject analysis
'''

import os
import numpy as np
import esrot1d as e1d




# load imported data:
dir0    = os.path.join( os.path.dirname(__file__), 'data' )
fpathH5 = os.path.join(dir0, 'imported.h5')
d       = e1d.io.load_h5( fpathH5 )



# calculate means:
usubj   = e1d.util.unique_sorted( d['subj'] )
m       = []
subj    = []
group   = []
aff     = []
sess    = []
limb    = []
for sb in usubj:
    for ss in [0,1]:
        for ll in [0,1]:
            b  = (d['subj']==sb) & (d['sess']==ss) & (d['limb']==ll)
            y  = d['y'][b]
            if y.shape[0] > 1:
                m.append( y.mean(axis=0) )
                subj.append( sb )
                sess.append( ss )
                limb.append( ll )
                group.append( d['group'][b][0] )
                aff.append( d['affected_limb'][b][0] )
m      = np.vstack(m)
subj,sess,limb,group,aff = [np.asarray(x)  for x in (subj,sess,limb,group,aff)]



# save means:
d      = dict(y=m, subj=subj, sess=sess, limb=limb, group=group, affected_limb=aff)
fpath1 = os.path.join(dir0, 'means.h5')
e1d.io.save_h5(fpath1, d)



