from poisson_approval import ProfileTwelve, StrategyTwelve


def test_main():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile
        ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(3, 5), 'c_ab': Fraction(1, 5), \
'ca_b': Fraction(1, 10)})
        >>> print(profile)
        <ab_c: 1/10, b_ac: 3/5, c_ab: 1/5, ca_b: 1/10> (Condorcet winner: b)
        >>> profile.c_ab
        Fraction(1, 5)
        >>> profile.d_type_share['c_ab']  # Alternate syntax for profile.c_ab
        Fraction(1, 5)
        >>> profile.cab
        Fraction(3, 10)
        >>> profile.d_ranking_share['cab']  # Alternate syntax for profile.cab
        Fraction(3, 10)
        >>> profile.weighted_maj_graph
        array([[0, Fraction(-1, 5), Fraction(2, 5)],
               [Fraction(1, 5), 0, Fraction(2, 5)],
               [Fraction(-2, 5), Fraction(-2, 5), 0]], dtype=object)
        >>> profile.condorcet_winners
        Winners({'b'})
        >>> profile.is_profile_condorcet
        1.0
        >>> profile.has_majority_favorite  # Is one candidate 'top' in a majority of ballots?
        True
        >>> profile.has_majority_ranking  # Does one ranking represent a majority of ballots?
        True
        >>> profile.is_single_peaked  # Is the profile single-peaked?
        True
        >>> profile.support_in_rankings
        {'abc', 'bac', 'cab'}
        >>> profile.is_generic_in_rankings  # Are all rankings there?
        False
        >>> profile.analyzed_strategies_pure
        Equilibria:
        <abc: a, bac: b, cab: ac> ==> b (FF)
        <abc: a, bac: ab, cab: c> ==> a (D)
        <abc: ab, bac: b, cab: utility-dependent> ==> b (FF)
        <BLANKLINE>
        Non-equilibria:
        <abc: a, bac: b, cab: c> ==> b (FF)
        <abc: a, bac: b, cab: utility-dependent> ==> b (FF)
        <abc: a, bac: ab, cab: ac> ==> a (D)
        <abc: a, bac: ab, cab: utility-dependent> ==> a (D)
        <abc: ab, bac: b, cab: c> ==> b (FF)
        <abc: ab, bac: b, cab: ac> ==> b (FF)
        <abc: ab, bac: ab, cab: c> ==> a, b (FF)
        <abc: ab, bac: ab, cab: ac> ==> a (D)
        <abc: ab, bac: ab, cab: utility-dependent> ==> a (D)
        >>> print(profile.analyzed_strategies_pure.winners_at_equilibrium)
        a, b
    """
    pass


def test_main_sincere():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)},
        ...                         ratio_sincere=Fraction(1, 3), symbolic=True)
        >>> tau_sincere = profile.tau_sincere
        >>> print(tau_sincere)
        <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> strategy = StrategyTwelve({'abc': 'a', 'bac': 'b', 'cab': 'utility-dependent'})
        >>> tau_strategic = profile.tau_strategic(strategy)
        >>> print(tau_strategic)
        <a: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> tau = profile.tau(strategy)
        >>> print(tau)
        <a: 1/15, ab: 1/30, ac: 1/10, b: 3/5, c: 1/5> ==> b
    """
    pass


def test_main_weak_orders():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10)},
        ...                         d_weak_order_share={'a~b>c': Fraction(3, 10)}, symbolic=True)
        >>> profile
        ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(3, 5)}, d_weak_order_share={'a~b>c': Fraction(3, 10)})
        >>> print(profile)
        <ab_c: 1/10, b_ac: 3/5, a~b>c: 3/10> (Condorcet winner: b)
    """
    pass


def test_have_ranking_with_utility_above_u():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=.5)
        Fraction(1, 10)
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=0)
        Fraction(3, 10)
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=1)
        0
    """
    pass


def test_have_ranking_with_utility_u():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.have_ranking_with_utility_u(ranking='cab', u=.5)
        0
    """
    pass


def test_have_ranking_with_utility_below_u():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=.5)
        Fraction(1, 5)
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=1)
        Fraction(3, 10)
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=0)
        0
    """
    pass


def test_repr():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)},
        ...                         ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5), symbolic=True)
        >>> profile
        ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(3, 5), 'c_ab': Fraction(1, 5), \
'ca_b': Fraction(1, 10)}, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5))
    """
    pass


def test_str():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)},
        ...                         ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5), symbolic=True)
        >>> print(profile)
        <ab_c: 1/10, b_ac: 3/5, c_ab: 1/5, ca_b: 1/10> (Condorcet winner: b) (ratio_sincere: 1/10) (ratio_fanatic: 1/5)
    """
    pass


def test_eq():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile == ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                           'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        True
    """
    pass


def test_standardized_version():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> print(profile.standardized_version)
        <a_bc: 3/5, ba_c: 1/10, c_ba: 1/5, cb_a: 1/10> (Condorcet winner: a)
        >>> profile.is_standardized
        False
    """
    pass


def test_has_majority_type():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.has_majority_type
        True

        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10)}, d_weak_order_share={'b>a~c': Fraction(9, 10)},
        ...                         symbolic=True)
        >>> profile.has_majority_type
        False
    """
    pass


def test_support_in_types():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.support_in_types
        {'ab_c', 'b_ac', 'c_ab', 'ca_b'}
    """
    pass


def test_is_generic_in_types():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> profile.is_generic_in_types
        False
    """
    pass


def test_tau_strategic():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> strategy = StrategyTwelve({'abc': 'ab', 'bac': 'b', 'cab': 'utility-dependent'})
        >>> tau_strategic = profile.tau_strategic(strategy)
        >>> print(tau_strategic)
        <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
    """
    pass


def test_is_equilibrium():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileTwelve({'ab_c': Fraction(1, 10), 'b_ac': Fraction(6, 10),
        ...                          'c_ab': Fraction(2, 10), 'ca_b': Fraction(1, 10)}, symbolic=True)
        >>> strategy = StrategyTwelve({'abc': 'ab', 'bac': 'b', 'cab': 'utility-dependent'})
        >>> profile.is_equilibrium(strategy)
        EquilibriumStatus.EQUILIBRIUM
    """
    pass
