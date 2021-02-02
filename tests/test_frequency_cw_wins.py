import pytest
from poisson_approval import ANTI_PLURALITY
from poisson_approval import RandProfileHistogramUniform
from poisson_approval import frequency_cw_wins


def test_no_convergence():
    rand_profile = RandProfileHistogramUniform(n_bins=1, voting_rule=ANTI_PLURALITY)
    with pytest.raises(ValueError):
        results = frequency_cw_wins(factory=rand_profile, n_samples=3, n_max_episodes=3,
                                    conditional_on_convergence=True)
