from pytest import fixture
from fractions import Fraction
from poisson_approval import ProfileTwelve, StrategyTwelve, StrategyThreshold, EquilibriumStatus


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
