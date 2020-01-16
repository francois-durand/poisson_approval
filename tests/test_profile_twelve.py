import numpy as np
from fractions import Fraction
from poisson_approval import ProfileTwelve


def test():
    # Check that normalization works as expected
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    assert profile.a_bc == 0.5

    # Misc

