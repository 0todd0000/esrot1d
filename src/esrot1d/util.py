

import numpy as np


def custom_legend(ax, colors=None, labels=None, linestyles=None, linewidths=None, markerfacecolors=None, markersizes=None, **kwdargs):
    n      = len(colors)
    if linestyles is None:
        linestyles = ['-']*n
    if linewidths is None:
        linewidths = [1]*n
    if markerfacecolors is None:
        markerfacecolors = colors
    if markersizes is None:
        markersizes = [None]*n
    x0,x1  = ax.get_xlim()
    y0,y1  = ax.get_ylim()
    h      = [ax.plot([x1+1,x1+2,x1+3], [y1+1,y1+2,y1+3], ls, color=color, linewidth=lw, markerfacecolor=mfc, ms=ms)[0]   for color,ls,lw,mfc,ms in zip(colors,linestyles,linewidths,markerfacecolors,markersizes)]
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    return ax.legend(h, labels, **kwdargs)


def float2str(x):
    return r'$\infty$' if np.isinf(x) else f'{x:.1f}'

def unique_sorted(x):
    return np.sort( np.unique(x) )


def plot_critical_values(ax, type='0d', ylim=(-1,1)):
    ymin,ymax = ylim
    interps   = interpretations if type=='0d' else interpretations1
    labels    = [i[0] for i in interps]
    values    = [i[1] for i in interps]
    values   += [100]
    n         = len(values)
    colors    = plt.cm.hot( np.linspace(0, 1, n+2) )[2:]
    # oy        = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    for i,(s,c) in enumerate( zip(labels,colors) ):
        if values[i] < ymax:
            ax.axhline(values[i], color=c, ls='-', zorder=0)
            bbox = dict(facecolor='w', edgecolor="0.5", pad=2, alpha=0.6)
            ax.text( 80, values[i]+0.01, s, color=c, bbox=bbox, size=12 )
        # if values[i] < -ymin:
        #     ax.axhline(-values[i], color=c, ls='-', zorder=0)
    ax.set_ylim( -0.3, ymax )
