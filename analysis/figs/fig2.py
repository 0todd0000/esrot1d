
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patheffects as pe
import rft1d

plt.style.use('bmh')
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['xtick.labelsize'] = 'small'
plt.rcParams['ytick.labelsize'] = 'small'
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family']     = 'Arial'



interpretations = [['Very small',0.01], ['Small',0.2], ['Medium',0.5], ['Large',0.8], ['Very large',1.2], ['Huge',2.0]]



def cohens_d(yA, yB):
	mA,mB  = yA.mean(axis=0), yB.mean(axis=0)
	sA,sB  = yA.std(axis=0, ddof=1), yB.std(axis=0, ddof=1)
	nA,nB  = yA.shape[0], yB.shape[0]
	s      = (   (  (nA-1)*sA*sA + (nB-1)*sB*sB  )  /  ( nA+nB-2 )   )**0.5
	d      = (mA - mB) / s
	return d

def plot_interpretations(ax, ymax=None):
    labels = [i[0] for i in interpretations]
    values = [i[1] for i in interpretations]
    values += [100]
    print(values)
    # values = [0] + values
    n      = len(values)
    colors = plt.cm.hot( np.linspace(0, 1, n+2) )[:-2]
    oy     = [0.05, 0.1, 0.1, 0.15, 0.3, 0.2]
    for i,(s,c,oyy) in enumerate( zip(labels,colors,oy) ):
        ax.axhspan(values[i], values[i+1], alpha=0.3, color=c, ec=None)
        ax.axhline(values[i], color='0.7', ls='-', zorder=0)
        # bbox = None if i>0 else dict(facecolor='w', edgecolor="0.5", pad=1, alpha=0.5)
        bbox = dict(facecolor='w', edgecolor="0.5", pad=2, alpha=0.6)
        ax.text( 50, values[i]+oyy, s, color=c, bbox=bbox )
        # ax.text( 0, values[i], s, color=c, bbox=dict(facecolor='w', edgecolor="0.5", pad=3) )
    if ymax is None:
        ymax = ax.lines[0].get_ydata().max() + 1
    ax.set_ylim( -0.01, ymax )

def p_effect(d, n, fwhm, Q=101):  # 2-sample
    v      = 2*n -2
    t      = d / (1.0/n + 1.0/n)**0.5
    return rft1d.t.sf(t, v, Q, fwhm)



def sim(J, Q, W=20, niter=200, pad=False):
    d = []
    for i in range(niter):
        y0 = rft1d.randn1d(J, Q, W, pad=pad)
        y1 = rft1d.randn1d(J, Q, W, pad=pad)
        d.append( cohens_d(y0, y1) )
    d      = np.array(d)
    u  = [i[1] for i in interpretations] + [np.inf]
    p  = [((d>=u[i]) & (d<u[i+1])).any(axis=1).mean()  for i in range(len(u)-1)]
    return u[:-1], p







# generate random datasets:
J,Q,WA,WB = 10, 101, 25, 5
np.random.seed(3)
yA0 = rft1d.randn1d(J, Q, WA, pad=True)
yA1 = rft1d.randn1d(J, Q, WA, pad=True)
dA  = cohens_d(yA0, yA1)
np.random.seed(6)
yB0 = rft1d.randn1d(J, Q, WB, pad=True)
yB1 = rft1d.randn1d(J, Q, WB, pad=True)
dB  = cohens_d(yB0, yB1)



# run simulations:
np.random.seed(0)
niter = 1000
uA,pA = sim(J, Q, W=WA, niter=niter, pad=False)
uB,pB = sim(J, Q, W=WB, niter=niter, pad=False)




# PLOT:
plt.close('all')
fig,AX = plt.subplots( 2, 2, figsize=(8,6) )
ax0,ax1,ax2,ax3 = AX.flatten()

# plot datasets:
c0,c1 = 'k', 'c'
for ax,y0,y1 in zip([ax0,ax1],[yA0,yB0],[yA1,yB1]):
    ax.plot(y0.T, color=c0, lw=0.3)
    ax.plot(y1.T, color=c1, lw=0.3)
    ax.plot(y0.mean(axis=0), color=c0, lw=5, label='Group 1 sample mean')
    ax.plot(y1.mean(axis=0), color=c1, lw=5, label='Group 2 sample mean')
    ax.set_xlabel('Domain position (%)')
    ax.set_ylabel('Dependent variable value')
    if ax==ax0:
        ax.legend( fontsize=8 )
plt.setp([ax0,ax1], ylim=(-3.5, 3.5))


# plot effect sizes:
c0,c1   = 'k', 'w'
pe0,pe1 = None, [pe.Stroke(linewidth=5, foreground='0.7'), pe.Normal()]
ax2.plot( np.abs(dA), color=c0, label='FWHM=25', path_effects=pe0, zorder=1)
ax2.plot( np.abs(dB), color=c1, label='FWHM=5', path_effects=pe1, zorder=2)
ax2.text(93, 1.55, r'$d_{max}$', color=c0)
ax2.text(20, 1.8, r'$d_{max}$', color=c1, path_effects=pe1)
plot_interpretations(ax2)
ax2.legend( fontsize=8, loc='upper left' )
ax2.set_xlabel('Domain position (%)')
ax2.set_ylabel("Cohen's d-value")
ax2.set_ylim(0, 2.5)
ax2.grid(None)




# plot probabilities
### theoretical probabilities:
dt  = np.linspace(0.01, 2, 51)
pt0 = np.array([p_effect(dd, J, 25, 101)  for dd in dt] )
pt1 = np.array([p_effect(dd, J, 5, 101)  for dd in dt] )
ax3.plot(dt, pt0, color=c0, path_effects=pe0, zorder=1, label='Theoretical (FWHM=25)' )
ax3.plot(dt, pt1, color=c1, path_effects=pe1, zorder=1, label='Theoretical (FWHM=5)' )
### simulation probabilities:
ax3.plot( uA , pA, 'o', color=c0, ms=5, path_effects=pe0, zorder=2, label='Simulation' )
ax3.plot( uB , pB, 'o', color=c1, ms=3, path_effects=pe1, zorder=2 )
### interpretations:
labels = [i[0] for i in interpretations]
ox,oy = [0.02, 0.02, 0.02, 0.01, 0.01, 0.01], [0.01, 0.01, 0.03, 0.03, 0.04, 0.07]
ha    = ['left']*5 + ['right']
for xx,pp,ss,oxx,oyy,haa in zip(uA,pA,labels,ox,oy,ha):
    ax3.text( xx+oxx , pp+oyy, ss, size=8, ha=haa )
### annotate:
ax3.legend( fontsize=8, loc='upper right' )
ax3.set_ylim(-0.03, 1.03)
ax3.set_xlabel( r"Threshold  [ $u$ ]")
ax3.set_ylabel( r'Probability:   $P (d_{max} > u)$')




panel_labels = ['(a)  Random functional dataset (FWHM=25)', '(b)  Random functional dataset (FWHM=5)', '(c)  Absolute effect size', '(d)  Effect size probabilities']
[ax.text(0.0, 1.08, s, size=11, transform=ax.transAxes)   for ax,s in zip([ax0,ax1,ax2,ax3], panel_labels)]



plt.tight_layout()
plt.show()




# plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig2.pdf'  )  )

