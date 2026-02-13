
from . baseline import BaselineScenario
from . import io
from . import smoothness
from . import stats
from . import util


import pathlib
dirREPO = pathlib.Path( __file__ ).parent.parent.parent


def set_plot_style():
    from matplotlib import pyplot as plt
    plt.style.use('bmh')
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['xtick.labelsize'] = 'small'
    plt.rcParams['ytick.labelsize'] = 'small'
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family']     = 'Arial'

