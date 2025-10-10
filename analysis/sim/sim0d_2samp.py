
from math import sqrt
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt



def d_2samp(y0, y1):
    n0,n1 = y0.shape[0], y1.shape[0]
    m0,m1 = y0.mean(axis=0), y1.mean(axis=0)
    v0,v1 = y0.var(axis=0, ddof=1), y1.var(axis=0, ddof=1)
    sp    = (  (  (n0-1)*v0 + (n1-1)*v1  )  /  (n0+n1-2)  )**0.5
    return (m0 - m1) / sp
    

# plt.savefig(  os.path.join(  os.path.dirname(__file__) , 'pdf', 'fig1-sim.pdf'  )  )