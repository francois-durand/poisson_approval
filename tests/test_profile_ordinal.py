from fractions import Fraction
from poisson_approval import ProfileOrdinal, StrategyOrdinal, PLURALITY, ANTI_PLURALITY, initialize_random_seeds


def test_normalization():
    profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1})
    assert profile.abc == 0.5


def test_plurality():
    """
        >>> profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1}, voting_rule=PLURALITY)
        >>> profile
        ProfileOrdinal({'abc': Fraction(1, 2), 'acb': Fraction(1, 2)}, voting_rule='Plurality')
        >>> print(profile)
        <abc: 1/2, acb: 1/2> (Condorcet winner: a) (Plurality)
        >>> profile.tau_fanatic
        TauVector({'a': Fraction(1, 1)}, voting_rule='Plurality')
    """
    pass


def test_anti_plurality():
    """
        >>> profile = ProfileOrdinal(d_ranking_share={'abc': 1, 'acb': 1}, voting_rule=ANTI_PLURALITY)
        >>> profile
        ProfileOrdinal({'abc': Fraction(1, 2), 'acb': Fraction(1, 2)}, voting_rule='Anti-plurality')
        >>> print(profile)
        <abc: 1/2, acb: 1/2> (Condorcet winner: a) (Anti-plurality)
        >>> profile.tau_fanatic
        TauVector({'ab': Fraction(1, 2), 'ac': Fraction(1, 2)}, voting_rule='Anti-plurality')
    """
    pass


def test_d_ballot_share_weak_voters_fanatic():
    """
        >>> profile = ProfileOrdinal({'a~b>c': Fraction(7, 10), 'c>a~b': Fraction(3, 10)})
        >>> profile.d_ballot_share_weak_voters_fanatic
        {'a': Fraction(7, 20), 'b': Fraction(7, 20), 'c': Fraction(3, 10), 'ab': 0, 'ac': 0, 'bc': 0}
        >>> profile.voting_rule = PLURALITY
        >>> profile.d_ballot_share_weak_voters_fanatic
        {'a': Fraction(7, 20), 'b': Fraction(7, 20), 'c': Fraction(3, 10), 'ab': 0, 'ac': 0, 'bc': 0}
        >>> profile.voting_rule = ANTI_PLURALITY
        >>> profile.d_ballot_share_weak_voters_fanatic
        {'a': 0, 'b': 0, 'c': 0, 'ab': Fraction(7, 10), 'ac': Fraction(3, 20), 'bc': Fraction(3, 20)}
    """
    pass


def test_d_ballot_share_weak_voters_sincere():
    """
        >>> profile = ProfileOrdinal({'a~b>c': Fraction(7, 10), 'c>a~b': Fraction(3, 10)})
        >>> profile.d_ballot_share_weak_voters_sincere
        {'a': 0, 'b': 0, 'c': Fraction(3, 10), 'ab': Fraction(7, 10), 'ac': 0, 'bc': 0}
        >>> profile.voting_rule = PLURALITY
        >>> profile.d_ballot_share_weak_voters_sincere
        {'a': Fraction(7, 20), 'b': Fraction(7, 20), 'c': Fraction(3, 10), 'ab': 0, 'ac': 0, 'bc': 0}
        >>> profile.voting_rule = ANTI_PLURALITY
        >>> profile.d_ballot_share_weak_voters_sincere
        {'a': 0, 'b': 0, 'c': 0, 'ab': Fraction(7, 10), 'ac': Fraction(3, 20), 'bc': Fraction(3, 20)}
    """
    pass


def test_no_equilibrium():
    """
        >>> profile = ProfileOrdinal({'abc': Fraction(2, 5), 'bca': Fraction(2, 5), 'cab': Fraction(1, 5)})
        >>> profile.analyzed_strategies_ordinal.winners_at_equilibrium
        Winners()
    """
    pass


def test_strategy_weak_order():
    """
        >>> profile = ProfileOrdinal({'abc': Fraction(1, 7), 'a~b>c': Fraction(2, 7), 'c>a~b': Fraction(4, 7)})
        >>> strategy = StrategyOrdinal({'abc': 'a'}, profile=profile)
        >>> print(strategy.tau)
        <a: 1/7, ab: 2/7, c: 4/7> ==> c
    """
    pass
