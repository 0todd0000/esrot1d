
'''
Calculate effect size and its simple and functional interpretations
'''


from esrot1d.dec import _fig2pdf

@_fig2pdf
def create_figure():

    import os
    import numpy as np
    import matplotlib.pyplot as plt
    import h5py
    import esrot1d as e1d
    e1d.set_plot_style()





    # load imported data:
    dir0    = os.path.join(e1d.dirREPO, 'analysis', 'Bertaux2022', 'data')
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





    # plot:
    plt.close('all')
    plt.figure(figsize=(6,4))
    ax = plt.axes()
    colors = '0', 'r', 'b'
    ax.plot( y1.T, color=colors[1], lw=0.2 )
    ax.plot( y2.T, color=colors[2], lw=0.5, ls=':' )
    ax.plot( y0.mean(axis=0), color=colors[0], lw=5, label='Healthy datum' )
    ax.plot( y1.mean(axis=0), color=colors[1], lw=5, label='OA, Month 0' )
    ax.plot( y2.mean(axis=0), color=colors[2], lw=5, ls=':', label='OA, Month 6' )
    ax.legend( facecolor='w' )
    ax.set_xlabel('Time (%)', size=12)
    ax.set_ylabel('Hip flexion (deg)', size=12)
    plt.tight_layout()
    ax.grid(None)



if __name__ == '__main__':
    create_figure()




