
'''
Summary of simulation results. Simulations aimed to estimate the survival function of the domain-wise maximum Cohen's d-value for
one- and two-sample scenarios, including changes in sample size and functional smoothness.
'''



from esrot1d.dec import _fig2pdf

@_fig2pdf
def create_figure():


    import os
    import numpy as np
    from matplotlib import pyplot as plt
    import esrot1d as e1d
    e1d.set_plot_style()



    # set parameters:
    np.random.seed(0)
    Q      = 101
    fwhm   = 20
    fwhms  = [5, 20, 50]
    N1     = 15
    N2     = 8
    ns1    = [9, 19, 39]  # df:  8, 18, 38
    ns2    = [5, 10, 20]  # df:  8, 18, 38
    u      = np.arange(0, 2.1, 0.2)
    u0     = np.linspace(0, 2, 51)




    # load sim results:
    fpath     = os.path.join( e1d.dirREPO, 'analysis', 'sim', 'results_sim.h5')
    d         = e1d.io.load_h5( fpath )
    sf10      = d['sf10']
    sf11w     = d['sf11w']
    sf11n     = d['sf11n']
    sf20      = d['sf20']
    sf21w     = d['sf21w']
    sf21n     = d['sf21n']
    sf10_an   = d['sf10_an']
    sf11n_an  = d['sf11n_an']
    sf11w_an  = d['sf11w_an']
    sf20_an   = d['sf20_an']
    sf21n_an  = d['sf21n_an']
    sf21w_an  = d['sf21w_an']



    # plot:
    plt.close('all')
    # fig,axs = plt.subplots( 3, 2, figsize=(8,8), tight_layout=True )

    fig     = plt.figure( figsize=(8,8) )
    axw,axh = 0.45, 0.28
    axx,axy = [0.07, 0.54], np.linspace(0.69, 0.05, 3)
    axs     = np.array(  [[plt.axes([xx,yy,axw,axh])  for xx in axx]  for yy in axy]  )


    colors  = ['r', 'g', 'b']


    sf_ans  = [sf10_an, sf20_an, sf11n_an, sf21n_an, sf11w_an, sf21w_an]
    sfs     = [sf10, sf20, sf11n, sf21n, sf11w, sf21w]
    for ax,sf_an,sf in zip(axs.ravel(), sf_ans, sfs):
        for i,c in enumerate(colors):
            ax.plot(u0, np.log10(sf_an[i]), color=c)
            ax.plot(u, np.log10(sf[i]), 'o', color=c )
        ax.axhline( np.log10(0.05), color='k', ls='--')
    axs[0,0].text(0.44, 0.72, r'$\alpha$=0.05', zorder=0, transform=axs[0,0].transAxes)
    # axs[0,0].legend( [h], [r'$\alpha$=0.05'], bbox_to_anchor=(0.1,0.1), facecolor='w' )


    [ax.set_xticklabels([])  for ax in axs[:2,:2].ravel()]
    [ax.set_yticklabels([])  for ax in axs[:,1]]
    plt.setp(axs, ylim=(-4.5, 0.2))


    [ax.set_xlabel('d', size=14) for ax in axs[2]]
    # [ax.set_ylabel(f'[{pref}]  log( P(d{suff}>u) )', size=14) for ax,pref,suff in zip(axs[:,0],['0D', '1D', '1D'],['','_max','_max'])]
    log10 = r'log$_{10}$'
    [ax.set_ylabel(f'[{pref}]   {log10}(p)', size=14) for ax,pref in zip(axs[:,0],['0D', '1D', '1D'])]
    # e1d.util.custom_legend(axs[0,0], colors=colors+['k','k'], labels=[f'n={nn}' for nn in ns1]+['Analytical','Simulation'], linestyles=['-','-','-','-','o'], linewidths=[2,2,2,2,None], markersizes=[None,None,None,5,5], framealpha=0.95, fancybox=True)
    leg0 = e1d.util.custom_legend(axs[0,0], colors=colors, labels=[f'n={nn}' for nn in ns1], linestyles=['-','-','-'], linewidths=[2,2,2], markersizes=[None,None,None], framealpha=0.95, fancybox=True)
    leg1 = e1d.util.custom_legend(axs[0,1], colors=['k','k'], labels=['Analytical','Simulation'], linestyles=['-','o'], linewidths=[2,None], markersizes=[None,5], framealpha=0.95, fancybox=True, bbox_to_anchor=(0.15,0.5), facecolor='w')



    e1d.util.custom_legend(axs[1,0], colors=colors, labels=[f'n={nn}' for nn in ns1], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
    e1d.util.custom_legend(axs[2,0], colors=colors, labels=[f'FWHM={w}' for w in fwhms], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)

    leg01 = e1d.util.custom_legend(axs[0,1], colors=colors, labels=[f'N={nn*2}' for nn in ns2], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
    e1d.util.custom_legend(axs[1,1], colors=colors, labels=[f'N={nn*2}' for nn in ns2], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)
    e1d.util.custom_legend(axs[2,1], colors=colors, labels=[f'FWHM={w}' for w in fwhms], linestyles=['-']*3, linewidths=[2]*3, markersizes=[None]*3)

    axs[0,1].add_artist(leg1)

    [ax.text(0.12, 1.02, f'FWHM = {fwhm}', transform=ax.transAxes)  for ax in axs[1]]
    [ax.text(0.12, 1.02, f'{nlabel} = {nn}', transform=ax.transAxes)  for ax,nlabel,nn in zip(axs[2],['n','N'],[N1,2*N2])]

    [ax.set_title(s)  for ax,s in zip(axs[0],['One-sample', 'Two-sample'])]

    [ax.text(0.02, 1.02, f'({chr(97+i)})', transform=ax.transAxes) for i,ax in enumerate(axs.ravel())]



if __name__ == '__main__':
    create_figure()






