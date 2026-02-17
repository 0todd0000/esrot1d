
'''
Classes for collections of critical d-values and their interpretation labels.
'''


import numpy as np


class CriticalValues(dict):
    def __init__(self, d, p, labels=None):
        self.d = np.asarray(d, dtype=float).flatten()
        self.p = np.asarray(p, dtype=float).flatten()
        self.labels = self._init_labels( labels, self.d, self.p )
        super().__init__( zip(self.labels, self.d) )
        
        
    def __repr__(self):
        s = f'{self.__class__.__name__}\n'
        for (k,v),pp in zip( self.items(), self.p):
            s += f'{k:>12} = {self._v2str(v)}  (p={pp:0.05})\n'
        return s
    
    @staticmethod
    def _init_labels(labels, d, p):
        if labels is None:
            assert d.size==6, f'\nIf no labels are specified, d must have size 6.\nActual size of d: {d.size}'
            assert p.size==6, f'\nIf no labels are specified, p must have size 6.\nActual size of p: {p.size}'
            labels = ['Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge']
        else:
            from collections.abc import Iterable
            assert isinstance(labels, Iterable), '\n"labels" must be a list of strings'
            labels = list(labels)
            assert np.all([isinstance(x,str) for x in labels]), '\n"labels" must be a list of strings'
            n = len(labels)
            assert d.size==n, f'\nThere are {n} labels, so d must have size {n}.\nActual size of d: {d.size}'
            assert p.size==n, f'\nThere are {n} labels, so p must have size {n}.\nActual size of p: {p.size}'
        return labels
    
    @staticmethod
    def _v2str(x):
        return '< 0.001' if ( x < 0.001) else f'{x:0.3f}'
        
    def plot_hlines(self, ax, ymax=None, colors=None, textx=0.8):
        if colors is None:
            import matplotlib.pyplot as plt
            colors = plt.cm.jet( np.linspace(0, 1, len(self)) )
        for c,(key,value) in zip(colors, self.items()):
            if (ymax is None) or (value < ymax):
                ax.axhline(value, color=c, ls='-', zorder=0)
                bbox = dict(facecolor='w', edgecolor="0.5", pad=2, alpha=0.6)
                ax.text( textx, value+0.01, key, color=c, bbox=bbox, size=12 )
    
    def toarray(self):
        return self.d.copy()
        
    def tolist(self):
        return list( zip( self.keys(), self.values() ) )


class BaselineScenario(CriticalValues):
    '''
    This class represents a baseline scenario from which critical values can be calculated
    for other scenarios, where these critical values include d-value, t-values and p-values.

    The assumed baseline scenario is:

        * A two-sample test
        * Total sample size of n=20
        * Equal group sizes and variances
        * Critical d-values of [0.01, 0.2, 0.5, 0.8, 1.2, 2.0] from Sawilowsky (2009)
        * Interpretations of 'Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge', respectively

    For this scenario the probability values associated with the critical d-values are:

        p = [0.4912, 0.33003, 0.13913, 0.045241, 0.0075904, 0.00014728]

    These values ( "_pc" below) can be calculated using the following snippet:

        import numpy as np
        from scipy import stats

        n = 20   # presumed total sample size for a 2-sample design
        d = np.array(  [0.01, 0.2, 0.5, 0.8, 1.2, 2.0]  )  # critical d-values
        t = d / (1/(n/2) + 1/(n/2))**0.5   # critical t-values
        p = stats.t.sf(t, n-2)
    '''

    def __init__(self, params=None):
        if params is None:
            d = [0.01, 0.2, 0.5, 0.8, 1.2, 2.0]
            p = [0.4912, 0.33003, 0.13913, 0.045241, 0.0075904, 0.00014728]  # pre-calculated for this baseline scenario (5 significant digits)
            labels = None
        else:
            d,p,labels = params
        super().__init__(d, p, labels)

    
    @classmethod
    def custom(cls, d, p, labels=None):
        return cls( (d, p, labels) )



if __name__ == '__main__':
    d      = [0.1, 0.5, 1]
    p      = [0.4, 0.1, 0.001]
    labels = ['A', 'BB', 'CCC']
    cv     = CriticalValues(d, p, labels)
    print( cv )
    print( cv['A'], cv['CCC'] )


