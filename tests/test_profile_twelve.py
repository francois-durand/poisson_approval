import numpy as np
from fractions import Fraction
from poisson_approval import ProfileTwelve, StrategyTwelve, StrategyThreshold, EquilibriumStatus


def test():
    """
    Iterated voting with verbose option:

        >>> from fractions import Fraction
        >>> profile = ProfileTwelve(d_type_share={'a_bc': Fraction(1, 2), 'ab_c': Fraction(1, 2)})
        >>> strategy = StrategyThreshold(d_ranking_threshold={'abc': 0})
        >>> result = profile.iterated_voting_strategies(strategy_ini=strategy, n_max_episodes=100,
        ...                                             update_ratio=1, verbose=True)
        -1
        <abc: ab> ==> a, b
        0
        <abc: a> ==> a
        1
        <abc: a> ==> a
        >>> result = profile.iterated_voting_taus(strategy_ini=strategy, n_max_episodes=100,
        ...                                       update_ratio=1, verbose=True)
        -1
        <ab: 1> ==> a, b
        0
        <a: 1> ==> a
        1
        <a: 1> ==> a
    """

    # Check that normalization works as expected
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    assert profile.a_bc == 0.5

    # Check a strategy that is not an equilibrium
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    strategy = StrategyTwelve(d_ranking_ballot={'abc': 'ab'})
    assert profile.is_equilibrium(strategy) == EquilibriumStatus.NOT_EQUILIBRIUM

    # Case without convergence: iterated_voting_strategies
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    strategy = StrategyThreshold(d_ranking_threshold={'abc': 0})
    result = profile.iterated_voting_strategies(strategy_ini=strategy, n_max_episodes=1, update_ratio=1)
    assert result['cycle_taus'] == []

    # Case without convergence: iterated_voting_taus
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    strategy = StrategyThreshold(d_ranking_threshold={'abc': 0})
    result = profile.iterated_voting_taus(strategy_ini=strategy, n_max_episodes=1, update_ratio=1)
    assert result['cycle_taus'] == []
