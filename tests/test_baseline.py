
import pytest
import numpy as np
import esrot1d as e1d


def test_rot_p():
    '''
    Ensure that esrot1d reproduces rules-of-thumb
    probabilities for the proposed baseline case
    '''
    d = [0.01, 0.2, 0.5, 0.8, 1.2, 2.0]
    p = [0.49120, 0.33003, 0.139126, 0.045241, 0.0075904, 0.00014728]
    for dd,pp0 in zip(d, p):
        pp1 = e1d.stats.d2p(dd, 20, dim=0, design='2sample')
        assert pp1  == pytest.approx(pp0, rel=1e-4)


