import numpy as np
import pytest
from poisson_approval import Asymptotic


def test():
    assert np.isnan(Asymptotic(mu=np.nan, nu=51, xi=69).limit)
    assert np.isposinf(Asymptotic(mu=0, nu=51, xi=69).limit)

    asymptotic = Asymptotic(mu=np.nan, nu=51, xi=69) + Asymptotic(mu=42, nu=51, xi=69)
    assert np.isnan(asymptotic.mu)
    assert np.isnan(asymptotic.nu)
    assert np.isnan(asymptotic.xi)

    assert not Asymptotic(mu=42, nu=51, xi=69).isclose(144)
    with pytest.raises(ValueError):
        Asymptotic(mu=np.nan, nu=51, xi=69).isclose(Asymptotic(mu=42, nu=51, xi=69))


def test_str_small_magnitudes():
    asymptotic = Asymptotic(mu=-2E-10, nu=0, xi=0)
    assert str(asymptotic) == 'exp(- 2e-10 n + o(1))'


def test_limit_ratio_with_small_magnitudes():
    numerator = Asymptotic(mu=-2E-10, nu=0, xi=0)
    denominator = Asymptotic(mu=-1E-10, nu=0, xi=0)
    ratio = numerator / denominator
    assert ratio.limit == 0
