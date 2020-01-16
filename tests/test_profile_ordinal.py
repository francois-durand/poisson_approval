import numpy as np
from fractions import Fraction
from poisson_approval import ProfileOrdinal


def test():
    # Check that normalization works as expected
    profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1})
    assert profile.abc == 0.5
