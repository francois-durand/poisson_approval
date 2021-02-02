import pytest
from poisson_approval import ANTI_PLURALITY, PLURALITY
from poisson_approval import ProfileHistogram, RandProfileHistogramUniform
from poisson_approval import frequency_cw_wins
from poisson_approval import initialize_random_seeds


def test_no_convergence():
    rand_profile = RandProfileHistogramUniform(n_bins=1, voting_rule=ANTI_PLURALITY)
    with pytest.raises(ValueError):
        f = frequency_cw_wins(factory=rand_profile, n_samples=3, n_max_episodes=3,
                              conditional_on_convergence=True)


def test_convergence_sometimes():

    class RandProfileWeird:

        def __init__(self):
            self.never_called = True

        def __call__(self):
            if self.never_called:
                self.never_called = False
                return ProfileHistogram({('abc', (1,)): 1}, voting_rule=ANTI_PLURALITY)
            else:
                return ProfileHistogram({('abc', (1,)): 1}, voting_rule=PLURALITY)

    initialize_random_seeds()
    f = frequency_cw_wins(factory=RandProfileWeird(), n_samples=2, n_max_episodes=1000,
                          conditional_on_convergence=True)
    assert (0 <= f <= 1)
