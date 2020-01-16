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
