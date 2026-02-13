
import esrot1d as e1d


# sample size to make "Large" effect significant at alpha=0.05
baseline = e1d.BaselineScenario()
d_medium = baseline.cv['Large']  # large: 0.8
n        = 4  # initial sample size
while e1d.stats.d2p(d_medium, n, dim=0, design='2sample') > 0.05:
    n += 2
print( f'\nMinimum sample size for significant LARGE effect: {n}\n\n' )


# calculate analogous critical functional d-max values for an average
#    smoothness of fwhm=21.9
dc = e1d.stats.d_critical(n, dim=1, design='2sample', Q=101, fwhm=21.9)


# assemble table:
print("Label       Cohen's d    Functional d    p-value   ")
print("-----------------------------------------------")
for (ss,dd0),pp,dd1 in zip(baseline.cv.items(), dc.p, dc.values()):
    print( f'{ss:10}  {dd0:9}     {dd1:.2f}     {pp:.3f}      ' )
    

