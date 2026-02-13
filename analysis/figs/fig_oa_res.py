
'''
Depiction of the functional residuals for the OA hip flexion dataset.
'''


from esrot1d.dec import _fig2pdf

@_fig2pdf
def create_figure():

    import os,pathlib
    import numpy as np
    import matplotlib.pyplot as plt
    import h5py
    import spm1d
    import esrot1d as e1d
    f2s = e1d.util.float2str
    e1d.set_plot_style()




    # load imported data:
    dirREPO = pathlib.Path( __file__ ).parent.parent.parent
    dir0    = os.path.join(dirREPO, 'analysis', 'Bertaux2022', 'data')
    fpathH5 = os.path.join(dir0, 'means.h5')
    d       = dict()
    with h5py.File(fpathH5, 'r') as f:
        for k in f.keys():
            d[k] = np.array(f[k])



    # separate data into groups (right limb only;  results are similar for left-limb only)
    # group 0:  healthy (group=0)
    # group 1:  OA, month 0 (group=1, sess=0)
    # group 2:  OA, month 6 (group=1, sess=1)
    limb   = 1
    y0     = d['y'][  (d['group']==0) & (d['limb']==limb) ]
    oasubj = e1d.util.unique_sorted( d['subj'][(d['affected_limb']==limb) & d['sess']==1] )
    y1     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==0) ]  for u in oasubj])
    y2     = np.vstack([d['y'][  (d['subj']==u) & (d['limb']==limb) & (d['sess']==1) ]  for u in oasubj])


    # calculate residuals:
    y      = y2 - y1
    r      = y - y.mean(axis=0)
    lkc    = e1d.smoothness.estimate_lkc(r)
    fwhm   = e1d.smoothness.estimate_fwhm(r)





    # plot:
    plt.close('all')
    plt.figure(figsize=(6,4))
    ax = plt.axes()
    ax.plot( r.T, color='b', lw=0.5 )
    ax.axhline(0, color='k', ls='--')
    s  = f'FWHM = {f2s(fwhm)}\nLKC = {f2s(lkc)}'
    ax.text(0.35, 0.90, s, transform=ax.transAxes, bbox=dict(color='w', alpha=0.8))
    ax.set_xlabel('Time (%)', size=12)
    ax.set_ylabel('Residual (deg)', size=12)
    plt.tight_layout()



if __name__ == '__main__':
    create_figure()








