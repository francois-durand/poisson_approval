from pytest import fixture
from fractions import Fraction
from poisson_approval import ProfileTwelve, StrategyTwelve, StrategyThreshold, EquilibriumStatus, PLURALITY, \
    ANTI_PLURALITY, UTILITY_DEPENDENT


def test_iterative_voting_verbose():
    """
    >>> from fractions import Fraction
    >>> profile = ProfileTwelve(d_type_share={'a_bc': Fraction(1, 2), 'ab_c': Fraction(1, 2)})
    >>> strategy = StrategyTwelve(d_ranking_ballot={'abc': 'ab'})
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
    pass


@fixture()
def my_profile():
    return ProfileTwelve(d_type_share={'a_bc': 1, 'ab_c': 1})


@fixture()
def my_strategy():
    return StrategyTwelve(d_ranking_ballot={'abc': 'ab'})


def test_normalization(my_profile):
    assert my_profile.a_bc == 0.5


def test_not_equilibrium(my_profile, my_strategy):
    assert my_profile.is_equilibrium(my_strategy) == EquilibriumStatus.NOT_EQUILIBRIUM


def test_iterated_voting_without_convergence(my_profile, my_strategy):
    result = my_profile.iterated_voting(strategy_ini=my_strategy, n_max_episodes=1, ballot_update_ratio=1)
    assert result['cycle_taus_actual'] == []


def test_fictitious_play_without_convergence(my_profile, my_strategy):
    result = my_profile.fictitious_play(strategy_ini=my_strategy, n_max_episodes=1)
    assert result['tau'] is None


def test_plurality():
    """
        >>> profile = ProfileTwelve(
        ...     d_type_share={'a_bc': Fraction(1, 5), 'ba_c': Fraction(3, 5), 'c_ab': Fraction(1, 5)},
        ...     voting_rule=PLURALITY)
        >>> profile
        ProfileTwelve({'a_bc': Fraction(1, 5), 'ba_c': Fraction(3, 5), 'c_ab': Fraction(1, 5)}, voting_rule='Plurality')
        >>> print(profile)
        <a_bc: 1/5, ba_c: 3/5, c_ab: 1/5> (Condorcet winner: b) (Plurality)
        >>> profile.tau_sincere
        TauVector({'a': Fraction(1, 5), 'b': Fraction(3, 5), 'c': Fraction(1, 5)}, voting_rule='Plurality')
        >>> profile.tau_fanatic
        TauVector({'a': Fraction(1, 5), 'b': Fraction(3, 5), 'c': Fraction(1, 5)}, voting_rule='Plurality')
        >>> strategy = StrategyTwelve({'abc': 'a', 'bac': 'b', 'cab': 'c'}, profile=profile)
        >>> strategy.is_equilibrium
        EquilibriumStatus.EQUILIBRIUM
    """
    pass


def test_anti_plurality():
    """
        >>> profile = ProfileTwelve(
        ...     d_type_share={'ab_c': Fraction(2, 5), 'b_ca': Fraction(2, 5), 'ca_b': Fraction(1, 5)},
        ...     voting_rule=ANTI_PLURALITY)
        >>> profile
        ProfileTwelve({'ab_c': Fraction(2, 5), 'b_ca': Fraction(2, 5), 'ca_b': Fraction(1, 5)}, \
voting_rule='Anti-plurality')
        >>> print(profile)
        <ab_c: 2/5, b_ca: 2/5, ca_b: 1/5> (Anti-plurality)
        >>> profile.tau_sincere
        TauVector({'ab': Fraction(2, 5), 'ac': Fraction(1, 5), 'bc': Fraction(2, 5)}, voting_rule='Anti-plurality')
        >>> profile.tau_fanatic
        TauVector({'ab': Fraction(2, 5), 'ac': Fraction(1, 5), 'bc': Fraction(2, 5)}, voting_rule='Anti-plurality')
        >>> strategy = StrategyTwelve({'abc': 'ab', 'bca': 'bc', 'cab': 'ac'}, profile=profile)
        >>> strategy.is_equilibrium
        EquilibriumStatus.EQUILIBRIUM
    """
    pass
