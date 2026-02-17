
'''
Interpretation of OA hip flexion effect sizes according to (a) the Sawilowsky (2009) rules-of-thumb and (b) the proposed functional rules-of-thumb.
'''


from esrot1d.dec import _fig2pdf

@_fig2pdf
def create_figure():


    import os
    import numpy as np
    from matplotlib import pyplot as plt
    import rft1d
    import h5py
    import esrot1d as e1d
    e1d.set_plot_style()


    cv0  = e1d.BaselineScenario()
    cv1  = e1d.stats.d_critical(20, dim=1, design='2sample', Q=101, fwhm=21.9)


    # load imported data:
    dir0    = os.path.join(e1d.dirREPO, 'analysis', 'Bertaux2022', 'data')
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

    d      = e1d.stats.d_1sample(y1 - y2)





    # plot:
    plt.close('all')
    fig,axs = plt.subplots(1, 2, figsize=(10,4), tight_layout=True)

    axs[0].plot( d, color='k' )
    axs[1].plot( d, color='k' )
    [ax.axhline(0, color='k', ls=':')  for ax in axs]

    
    ylim   = -0.3, 0.89
    colors = plt.cm.hot( np.linspace(0, 1, 8) )[1:-1]
    cv0.plot_hlines(axs[0], ymax=ylim[1], colors=colors, textx=80)
    cv1.plot_hlines(axs[1], ymax=ylim[1], colors=colors, textx=80)

    axs[1].set_yticklabels([])
    plt.setp(axs, xlim=(0,100), ylim=ylim)
    [ax.set_xlabel('Time (%)', size=12)  for ax in axs]
    axs[0].set_ylabel("Effect size (Cohen's d-value)", size=12)
    # ax.grid(None)
    labels = 'Sawilowsky (2009) rules of thumb', 'Proposed functional rules of thumb'
    [ax.text(0.02, 0.95, f'({chr(97+i)}) {s}', transform=ax.transAxes, size=12)   for i,(ax,s) in enumerate(zip(axs,labels))]




if __name__ == '__main__':
    create_figure()





