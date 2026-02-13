
import os

fnames = [
    'fig_oa',
    'fig_dp',
    'fig_randn1d',
    'fig_sim',
    'fig_oa_es',
    'fig_oa_res',
    'fig_oa_es_posthoc',
]


dir0 = os.path.dirname(__file__)
for fname in fnames:
    print( f'Generating {fname}.pdf...')
    fpath = os.path.join(dir0, f'{fname}.py')
    cmd   = f'python {fpath} pdf'
    os.system( cmd )
print('Done')
