import numpy as np
from fractions import Fraction
from poisson_approval import ProfileHistogram


def test():
    # Check that normalization works as expected
    profile = ProfileHistogram(d_ranking_share={'abc': 1, 'acb': 1},
                               d_ranking_histogram = {'abc': [1, 1], 'acb': [1]})
    assert profile.abc == 0.5
    assert np.all(profile.d_ranking_histogram['abc'] == [0.5, 0.5])
