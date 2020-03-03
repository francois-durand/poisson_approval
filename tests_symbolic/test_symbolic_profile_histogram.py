from poisson_approval import ProfileHistogram, StrategyThreshold


def test_main():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        >>> profile  # doctest: +NORMALIZE_WHITESPACE
        ProfileHistogram({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)}, {'abc': array([1]), \
'bac': array([1, 0]), 'cab': array([Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)],
            dtype=object)})
        >>> print(profile)
        <abc: 1/10 [1], bac: 3/5 [1 0], cab: 3/10 [Fraction(2, 3) 0 0 0 0 0 0 0 0 Fraction(1, 3)]> (Condorcet winner: b)
        >>> profile.abc
        Fraction(1, 10)
        >>> profile.d_ranking_share['abc']  # Alternate syntax for profile.abc
        Fraction(1, 10)
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
        >>> strategy = StrategyThreshold({'abc': 0, 'bac': 1, 'cab': Fraction(1, 2)}, profile=profile)
        >>> print(profile.tau_sincere)
        <a: 1/20, ab: 1/20, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> print(profile.tau_fanatic)
        <a: 1/10, b: 3/5, c: 3/10> ==> b
        >>> print(profile.tau_strategic(strategy))
        <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> print(profile.tau(strategy))
        <ab: 1/10, ac: 1/10, b: 3/5, c: 1/5> ==> b
        >>> profile.is_equilibrium(strategy)
        EquilibriumStatus.EQUILIBRIUM

        Bug: this strategy should lead to an FF tau-vector:

        >>> strategy = StrategyThreshold({'abc': 1, 'bac': 1, 'cab': Fraction(1, 2)}, profile=profile)
        >>> print(strategy)
        <abc: a, bac: b, cab: utility-dependent (1/2)> ==> b
        >>> strategy.print_weak_pivots()
        pivot_weak_ab:  <asymptotic = exp(- 0.108278753223296*n + ? log(n) + ? + o(1)), phi_a = 1.84172830809616, phi_b = 0.589621791959692, phi_c = 0.920875482125372, phi_ac = 1.69600244366199>
        pivot_weak_ac:  <asymptotic = exp(- 0.108278753228628*n + ? log(n) + ? + o(1)), phi_a = 1.84173522494675, phi_b = 0.589624616402563, phi_c = 0.920867612473376, phi_ac = 1.69599431940483>
        pivot_weak_bc:  <asymptotic = exp(n*(-9/10 + 3*sqrt(2)/5) - log(n)/2 - log(6*sqrt(2)*pi/5)/2 + o(1)), phi_a = 1, phi_b = sqrt(2)/2, phi_c = sqrt(2), phi_ac = sqrt(2)>
        trio:  <asymptotic = exp(- 0.108278753223296*n + ? log(n) + ? + o(1)), phi_a = 1.84172830809616, phi_b = 0.589621791959692, phi_c = 0.920875482125372, phi_ac = 1.69600244366199>
        >>> print(strategy.tau.focus)
        D

        # >>> profile.analyzed_strategies_group
        # Equilibria:
        # <abc: ab, bac: b, cab: utility-dependent (1/2)> ==> b (FF)
        # <abc: a, bac: ab, cab: c> ==> a (D)
        # <abc: a, bac: b, cab: ac> ==> b (FF)
        # <BLANKLINE>
        # Non-equilibria:
        # <abc: ab, bac: ab, cab: ac> ==> a (D)
        # <abc: ab, bac: ab, cab: utility-dependent (1/2)> ==> a (D)
        # <abc: ab, bac: ab, cab: c> ==> a, b (FF)
        # <abc: ab, bac: b, cab: ac> ==> b (FF)
        # <abc: ab, bac: b, cab: c> ==> b (FF)
        # <abc: a, bac: ab, cab: ac> ==> a (D)
        # <abc: a, bac: ab, cab: utility-dependent (1/2)> ==> a (D)
        # <abc: a, bac: b, cab: utility-dependent (1/2)> ==> b (FF)
        # <abc: a, bac: b, cab: c> ==> b (FF)

    Fictitious play and iterated do work with symbolic = True, but it is not recommended because it is slow:

        # >>> strategy_ini = StrategyThreshold({'abc': .5, 'bac': .5, 'cab': .5})
        # >>> cycle = profile.iterated_voting(strategy_ini, 100)['cycle_strategies']
        # >>> len(cycle)
        # 1
        # >>> print(cycle[0])
        # <abc: ab, bac: utility-dependent (0.719931614204618), cab: utility-dependent (0.280068385795382)> ==> b
        # >>> limit_strategy = profile.fictitious_play(strategy_ini, 100, perception_update_ratio=1)['strategy']
        # >>> print(limit_strategy)
        # <abc: ab, bac: utility-dependent (0.719931614204618), cab: utility-dependent (0.280068385795382)> ==> b
    """
    pass


def test_main_weak_orders():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10)},
        ...     {'abc': [1], 'bac': [1, 0]},
        ...     d_weak_order_share={'c~a>b': Fraction(3, 10)}, symbolic=True)
        >>> profile
        ProfileHistogram({'abc': Fraction(1, 10), 'bac': Fraction(3, 5)}, {'abc': array([1]), 'bac': array([1, 0])}, \
d_weak_order_share={'a~c>b': Fraction(3, 10)})
        >>> print(profile)
        <abc: 1/10 [1], bac: 3/5 [1 0], a~c>b: 3/10> (Condorcet winner: b)
    """
    pass


def test_have_ranking_with_utility_above_u():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=0)
        3/10
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=Fraction(1, 100))
        7/25
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=Fraction(99, 100))
        1/100
        >>> profile.have_ranking_with_utility_above_u(ranking='cab', u=1)
        0
    """
    pass


def test_have_ranking_with_utility_below_u():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=0)
        0
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=Fraction(1, 100))
        1/50
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=Fraction(99, 100))
        29/100
        >>> profile.have_ranking_with_utility_below_u(ranking='cab', u=1)
        3/10
    """
    pass


def test_repr():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10), symbolic=True)
        >>> profile
        ProfileHistogram({'abc': Fraction(1, 10), 'bac': Fraction(3, 5), 'cab': Fraction(3, 10)}, \
{'abc': array([1]), 'bac': array([1, 0]), 'cab': array([Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)],
              dtype=object)}, ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(1, 5))
    """
    pass


def test_str():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     ratio_sincere=Fraction(1, 10), ratio_fanatic=Fraction(2, 10), symbolic=True)
        >>> print(profile)
        <abc: 1/10 [1], bac: 3/5 [1 0], cab: 3/10 [Fraction(2, 3) 0 0 0 0 0 0 0 0 Fraction(1, 3)]> \
(Condorcet winner: b) (ratio_sincere: 1/10) (ratio_fanatic: 1/5)
    """
    pass


def test_eq():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        >>> profile == ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        True
    """
    pass


def test_standardized_version():
    """
        >>> from fractions import Fraction
        >>> profile = ProfileHistogram(
        ...     {'abc': Fraction(1, 10), 'bac': Fraction(6, 10), 'cab': Fraction(3, 10)},
        ...     {'abc': [1], 'bac': [1, 0], 'cab': [Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0, 0, Fraction(1, 3)]},
        ...     symbolic=True)
        >>> print(profile.standardized_version)
        <abc: 3/5 [1 0], bac: 1/10 [1], cba: 3/10 [Fraction(2, 3) 0 0 0 0 0 0 0 0 Fraction(1, 3)]> \
(Condorcet winner: a)
        >>> profile.is_standardized
        False
    """
    pass
