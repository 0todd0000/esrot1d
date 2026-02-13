
import numpy as np


class BaselineScenario(object):
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
    
    def __init__(self):
        self.dc     = np.array([0.01, 0.2, 0.5, 0.8, 1.2, 2.0])
        self.pc     = np.array([0.4912, 0.33003, 0.13913, 0.045241, 0.0075904, 0.00014728])  # pre-calculated for this baseline scenario (5 significant digits)
        self.n      = 20
        self.v      = self.n - 2  # degrees of freedom
        self.design = 'two-sample'
        self.cv     = CriticalValues( self.dc, self.pc )
        
    def __repr__(self):
        s  =  'BaselineScenario:\n'
        s += f'    design = {self.design}\n'
        s += f'    n      = {self.n}\n'
        s += f'    v      = {self.v}\n'
        s += f'    dc     = {self.dc}\n'
        s += f'    pc     = {self.pc}\n'
        return s
    
    @property
    def critical_values(self):
        return self.cv
        
    


class CriticalValues(dict):
    def __init__(self, d, p):
        labels = 'Very small', 'Small', 'Medium', 'Large', 'Very large', 'Huge'
        d      = [float(dd) for dd in d]
        super().__init__( zip(labels, d) )
        self.p = [float(pp) for pp in p]
        
    def __repr__(self):
        s = 'Critical d-values:\n'
        for (k,v),pp in zip( self.items(), self.p):
            s += f'{k:>12} = {self._v2str(v)}  (p={pp:0.05})\n'
        return s
    
    @staticmethod
    def _v2str(x):
        return '< 0.001' if ( x < 0.001) else f'{x:0.3f}'
        
    def toarray(self):
        return np.asarray(list(self.values()), dtype=float)
        
    def tolist(self):
        return list( zip( self.keys(), self.values() ) )



if __name__ == '__main__':
    
    bs = BaselineScenario()
    # print( bs )
    print( bs.critical_values )
    
