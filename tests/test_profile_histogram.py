from fractions import Fraction
import numpy as np
from poisson_approval import ProfileHistogram, StrategyThreshold, StrategyOrdinal, EquilibriumStatus, PLURALITY, \
    ANTI_PLURALITY


def test_normalization():
    profile = ProfileHistogram(d_ranking_share={'abc': 1, 'acb': 1},
                               d_ranking_histogram = {'abc': [1, 1], 'acb': [1]})
    assert profile.abc == 0.5
    assert np.all(profile.d_ranking_histogram['abc'] == [0.5, 0.5])


def test_not_equilibrium():
    profile = ProfileHistogram(d_ranking_share={'abc': 0.5, 'acb': 0.5},
                               d_ranking_histogram = {'abc': [1], 'acb': [1]})
    strategy = StrategyThreshold(d_ranking_threshold={'abc': 0, 'acb': 0})
    assert profile.is_equilibrium(strategy) == EquilibriumStatus.NOT_EQUILIBRIUM


def test_plurality():
    """
        >>> profile = ProfileHistogram(d_ranking_share={'abc': 1, 'acb': 1},
        ...                            d_ranking_histogram = {'abc': [1, 1], 'acb': [1]},
        ...                            voting_rule=PLURALITY)
        >>> profile
        ProfileHistogram({'abc': 0.5, 'acb': 0.5}, {'abc': array([0.5, 0.5]), 'acb': array([1])}, \
voting_rule='Plurality')
        >>> print(profile)
        <abc: 0.5 [0.5 0.5], acb: 0.5 [1]> (Condorcet winner: a) (Plurality)
    """
    pass


def test_anti_plurality():
    """
        >>> profile = ProfileHistogram(d_ranking_share={'abc': 1, 'acb': 1},
        ...                            d_ranking_histogram = {'abc': [1, 1], 'acb': [1]},
        ...                            voting_rule=ANTI_PLURALITY)
        >>> profile
        ProfileHistogram({'abc': 0.5, 'acb': 0.5}, {'abc': array([0.5, 0.5]), 'acb': array([1])}, \
voting_rule='Anti-plurality')
        >>> print(profile)
        <abc: 0.5 [0.5 0.5], acb: 0.5 [1]> (Condorcet winner: a) (Anti-plurality)
    """
    pass


def test_strategy_weak_order():
    """
        >>> profile = ProfileHistogram(d_ranking_share={'abc': Fraction(1, 7)}, d_ranking_histogram = {'abc': [1]},
        ...                            d_weak_order_share={'a~b>c': Fraction(2, 7), 'c>a~b': Fraction(4, 7)})
        >>> strategy = StrategyOrdinal({'abc': 'a'}, profile=profile)
        >>> print(strategy.tau)
        <a: 1/7, ab: 2/7, c: 4/7> ==> c
    """
    pass
