import numpy as np
from fractions import Fraction
from poisson_approval import ProfileTwelve, StrategyTwelve, StrategyThreshold, EquilibriumStatus


def test():
    """
    Iterated voting with verbose option:

        >>> from fractions import Fraction
        >>> profile = ProfileTwelve(d_type_share={'a_bc': Fraction(1, 2), 'ab_c': Fraction(1, 2)})
        >>> strategy = StrategyThreshold(d_ranking_threshold={'abc': 0})
        >>> result = profile.iterated_voting(strategy_ini=strategy, n_max_episodes=100,
        ...                                  ballot_update_ratio=1, verbose=True)
        t = 0
        strategy: <abc: ab> ==> a, b
        tau_actual: <ab: 1> ==> a, b
        t = 1
        tau_perceived: <ab: 1> ==> a, b
        strategy: <abc: a> ==> a
        tau_full_response: <a: 1> ==> a
        tau_actual: <a: 1> ==> a
        t = 2
        tau_perceived: <a: 1> ==> a
        strategy: <abc: a> ==> a
        tau_full_response: <a: 1> ==> a
        tau_actual: <a: 1> ==> a
        t = 3
        tau_perceived: <a: 1> ==> a
        strategy: <abc: a> ==> a
        tau_full_response: <a: 1> ==> a
        tau_actual: <a: 1> ==> a
        >>> result = profile.fictitious_play(strategy_ini=strategy, n_max_episodes=100,
        ...                                  perception_update_ratio=1, ballot_update_ratio=1, verbose=True)
        t = 0
        strategy: <abc: ab> ==> a, b
        tau_actual: <ab: 1> ==> a, b
        tau_perceived: <ab: 1> ==> a, b
        t = 1
        tau_perceived: <ab: 1> ==> a, b
        strategy: <abc: a> ==> a
        tau_full_response: <a: 1> ==> a
        tau_actual: <a: 1> ==> a
        t = 2
        tau_perceived: <a: 1> ==> a
        strategy: <abc: a> ==> a
        tau_full_response: <a: 1> ==> a
        tau_actual: <a: 1> ==> a
    """

    # Check that normalization works as expected
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    assert profile.a_bc == 0.5

    # Check a strategy that is not an equilibrium
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    strategy = StrategyTwelve(d_ranking_ballot={'abc': 'ab'})
    assert profile.is_equilibrium(strategy) == EquilibriumStatus.NOT_EQUILIBRIUM

    # Case without convergence: iterated_voting
    profile = ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})
    strategy = StrategyThreshold(d_ranking_threshold={'abc': 0})
    result = profile.iterated_voting(strategy_ini=strategy, n_max_episodes=1, ballot_update_ratio=1)
    assert result['cycle_taus_actual'] == []
