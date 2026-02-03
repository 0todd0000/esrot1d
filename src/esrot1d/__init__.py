
from . baseline import BaselineScenario
from . import io
from . import smoothness
from . import stats
from . import util


_keys   = ['Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge']
_values = [0.01, 0.2, 0.5, 0.8, 1.2, 2.0]
rots    = dict( zip(_keys, _values) )

def set_plot_style():
    from matplotlib import pyplot as plt
    plt.style.use('bmh')
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['xtick.labelsize'] = 'small'
    plt.rcParams['ytick.labelsize'] = 'small'
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family']     = 'Arial'
